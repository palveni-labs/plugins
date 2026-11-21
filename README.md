# Palveni Plugins

This repository distributes official skins for Palveni Server and welcomes community skin submissions. Each skin includes light and dark appearances.

| Skin | Source | Appearance |
| --- | --- | --- |
| Native | [skin-native](skin-native/) | Neutral gray surfaces, navy accents and a labeled sidebar |
| Paper & Ink | [skin-ink](skin-ink/) | Paper tones, serif headings and vermilion accents |
| Equipment | [skin-gear](skin-gear/) | Graphite surfaces, compact typography and amber indicators |

## Install a skin

Open **Apps → Appearance** in the dashboard to install an official skin. The server verifies its SHA-256 digest. You can also download a tar archive from [Releases](https://github.com/palveni-labs/plugins/releases) and use **Upload skin** for a community package.

## Submit a plugin

To submit a skin, open a pull request with its source directory or a link to a versioned source repository. Include the plugin ID, version, license, and the source and license for each font, image or other bundled asset. For a downloadable archive, include its versioned URL and SHA-256 digest.

The current server installs resource-only skins. See the [Ink manifest](skin-ink/plugin.toml) and [skin definition](skin-ink/skin.json). Choose a unique plugin ID, set `runtime = "none"`, and place `plugin.toml` and `skin.json` at the root of an uncompressed POSIX tar file. The maximum archive size is 16 MiB.

## Media sources and rights

A plugin's software license covers its code. Recordings, lyrics, artwork and access to a provider's service may require separate permission. For a media-source proposal, identify the provider, link to its published API terms or distribution permission, and explain whether the integration streams, caches or downloads content. Keep credentials and personal media out of submissions.

Community authors may maintain their own repositories. The same review applies to external listings and code submitted here. Maintainers review the requested permissions, asset provenance and intended use before listing a plugin. We decline submissions that rely on unauthorized redistribution or bypass a provider's access controls. Use the repository's issue tracker to report a listing with missing or incorrect licensing information.

## License

Official skins use the [Mozilla Public License 2.0](LICENSE). Each skin includes its font licenses in its `fonts/` directory.
