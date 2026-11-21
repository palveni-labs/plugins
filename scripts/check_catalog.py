"""Verify the official resource packages against the catalogue and their pinned Git sources."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tomllib


ROOT = Path(__file__).resolve().parents[1]
MAX_PACKAGE_BYTES = 16 * 1024 * 1024
DOWNLOAD_PREFIX = "https://raw.githubusercontent.com/palveni-labs/plugins/"


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)


def check_release(root, entry, release, checked_out_version):
    sid = entry["skinId"]
    version = release["version"]
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("Invalid skin version")
    filename = f"packages/skin-{sid}-{version}.tar"
    address = re.fullmatch(re.escape(DOWNLOAD_PREFIX) + r"([a-f0-9]{40})/" + re.escape(filename), release["url"])
    if not address:
        raise ValueError("Invalid download revision or package URL")
    revision = address[1]
    archive = root / filename
    size = archive.stat().st_size
    if not 0 < size <= MAX_PACKAGE_BYTES or size != release["size"]:
        raise ValueError(f"Archive size differs for {sid}")
    sha = hashlib.sha256(archive.read_bytes()).hexdigest()
    pinned = git(root, "show", f"{revision}:{filename}")
    if sha != release["sha256"] or hashlib.sha256(pinned).hexdigest() != sha:
        raise ValueError(f"Archive digest differs for {sid}")
    folder = f"skin-{sid}"
    src = f"{revision}:{folder}"
    manifest = tomllib.loads(git(root, "show", src + "/plugin.toml").decode())
    skin = json.loads(git(root, "show", src + "/skin.json"))
    plugin = manifest["plugin"]
    if (release["runtime"] != "none" or plugin["runtime"] != "none" or manifest["provides"].get("skin") != "skin.json"
            or release["api"] != manifest["compat"]["api"] or release["permissions"] != {}
            or manifest.get("permissions", {}) != {} or skin["id"] != sid or entry["id"] != plugin["id"]
            or version != plugin["version"]):
        raise ValueError(f"Catalogue metadata differs for {sid}")
    if not datetime.fromisoformat(release["publishedAt"]).tzinfo:
        raise ValueError("Release date must include a time zone")
    tree = git(root, "ls-tree", "-rz", src)
    source_files = {}
    for line in tree.split(b"\0"):
        if line:
            meta, path = line.split(b"\t", 1)
            mode, kind, oid = meta.split()
            if mode != b"100644" or kind != b"blob":
                raise ValueError(f"Invalid source file for {sid}")
            source_files[path.decode()] = oid.decode()
    checked_out = {}
    if version == checked_out_version:
        source_dir = root / folder
        for source in source_dir.rglob("*"):
            if source.is_symlink() or not (source.is_file() or source.is_dir()):
                raise ValueError(f"Invalid source file in checkout for {sid}")
            if source.is_file():
                checked_out[source.relative_to(source_dir).as_posix()] = source
        if checked_out.keys() != source_files.keys():
            raise ValueError(f"Checked-out file list differs for {sid}")
    with tarfile.open(archive, "r:") as tar:
        members = tar.getmembers()
        if len(members) != len(source_files) or {m.name for m in members} != source_files.keys():
            raise ValueError(f"Archive file list differs for {sid}")
        for m in members:
            if not m.isfile() or m.size > MAX_PACKAGE_BYTES:
                raise ValueError(f"Invalid archive member in {sid}")
            content = tar.extractfile(m).read()
            if checked_out and checked_out[m.name].read_bytes() != content:
                raise ValueError(f"Checked-out file differs from package: {folder}/{m.name}")
            if hashlib.sha1(f"blob {len(content)}\0".encode() + content).hexdigest() != source_files[m.name]:
                raise ValueError(f"Archive content differs from Git source for {sid}")
    return filename


def check(registry, root=ROOT):
    if registry["schema"] != 1 or not registry["name"] or not datetime.fromisoformat(registry["generatedAt"]).tzinfo:
        raise ValueError("Invalid catalogue header")
    seen = set()
    paths = set()
    for entry in registry["plugins"]:
        sid = entry["skinId"]
        if not re.fullmatch(r"[a-z0-9][a-z0-9.-]{1,62}", sid) or ".." in sid:
            raise ValueError("Invalid skin identifier")
        if entry["id"] in seen or not entry["releases"]:
            raise ValueError("Duplicate plugin or missing releases")
        seen.add(entry["id"])
        src = root / f"skin-{sid}"
        skin = json.loads((src / "skin.json").read_text())
        if entry["name"] != skin["name"]["en"] or entry["description"] != skin["description"]["en"]:
            raise ValueError(f"Catalogue description differs for {sid}")
        checked_out_version = tomllib.loads((src / "plugin.toml").read_text())["plugin"]["version"]
        if not any(r["version"] == checked_out_version for r in entry["releases"]):
            raise ValueError(f"Missing release for checked-out version of {sid}")
        for release in entry["releases"]:
            filename = check_release(root, entry, release, checked_out_version)
            if filename in paths:
                raise ValueError("Duplicate package")
            paths.add(filename)
    if not paths or paths != {p.relative_to(root).as_posix() for p in (root / "packages").glob("*.tar")}:
        raise ValueError("Catalogue must cover all current packages")


if __name__ == "__main__":
    try:
        catalog = json.loads((ROOT / "catalog.json").read_text())
        check(catalog)
        print(f"Verified {len(catalog['plugins'])} plugins")
    except (ValueError, KeyError, OSError, tarfile.TarError, subprocess.CalledProcessError) as e:
        sys.exit(str(e))
