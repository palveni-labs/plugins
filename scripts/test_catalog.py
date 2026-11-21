import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from check_catalog import ROOT, check


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((ROOT / "catalog.json").read_text())

    def test_all_packages_match_sources_and_immutable_downloads(self):
        check(self.registry)

    def test_damaged_digest_is_rejected(self):
        self.registry["plugins"][0]["releases"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "digest differs"):
            check(self.registry)

    def test_unlisted_package_is_rejected(self):
        self.registry["plugins"].pop()
        with self.assertRaisesRegex(ValueError, "cover all"):
            check(self.registry)

    def test_duplicate_is_rejected(self):
        self.registry["plugins"].append(copy.deepcopy(self.registry["plugins"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            check(self.registry)

    def test_mutable_revision_is_rejected(self):
        release = self.registry["plugins"][0]["releases"][0]
        release["url"] = release["url"].replace(release["url"].split("/")[-3], "main")
        with self.assertRaisesRegex(ValueError, "revision"):
            check(self.registry)

    def test_source_change_requires_repackaging(self):
        read_bytes = Path.read_bytes
        def changed_source(path):
            data = read_bytes(path)
            if path == ROOT / "skin-native" / "preview.png":
                return data + b"changed"
            return data

        with patch.object(Path, "read_bytes", changed_source):
            with self.assertRaisesRegex(ValueError, "Checked-out file differs"):
                check(self.registry)
