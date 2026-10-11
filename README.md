# TMods bundles

The mods, configs and other bundles TMods installs. Every push that changes `bundles/`
zips them and publishes a GitHub Release with the manifest the app reads.

In TMods, set the manifest URL (first launch or Settings) to:

```
https://github.com/Trino11/TMods-bundles/releases/latest/download/manifest.json
```

## Adding a bundle

Make one folder per version under its category, with the files placed exactly where they
go in the game folder:

```
bundles/
  mods/
    1.0.0/
      mods/sodium.jar
      bundle.json        optional: description, target, changelog
      CHANGELOG.md       optional: the changelog as text
  configs/
    1.0.0/
      config/sodium-options.json
```

Categories: `mods`, `schematics`, `resourcepacks`, `configs`, `shaderpacks`.

Versions are listed newest first (numbers compared as numbers, so `1.10.0` comes before
`1.9.0`) and the first one is the latest. To pick another, add `bundles/bundles.json` with
`{ "latest": { "mods": "1.0.0" } }`.

## Rules

- To update a bundle, add a new version folder. Changing the files of a version that's
  already published won't reach players who installed it.
- Don't delete old releases: newer manifests can still link to zips in them.
- GitHub refuses files over 100 MB.

To check a change without publishing, run the workflow from the Actions tab with
"dry-run" ticked. Full guide:
[publish-bundles](https://github.com/Trino11/TMods-Downloader/blob/main/publish-bundles/README.md).
