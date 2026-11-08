# Automatic releases

Push a shared version tag after the intended changes are on `main`:

```shell
git tag -a v1.0.1-beta.1 -m "Titan Relics 1.0.1-beta.1"
git push origin v1.0.1-beta.1
```

The [Release all targets workflow](../../.github/workflows/release.yml) builds
Fabric and NeoForge for **Minecraft 1.21.1, 1.21.11, 26.2 and 26.3**, then attaches all eight
player JARs and one `SHA256SUMS.txt` to a single GitHub release. The first verified
automated release was [Alpha 5.0.3](https://github.com/Auda29/Titan-Relics/releases/tag/v0.1.0-alpha.5.0.3).

The tag supplies the artifact version through `RELICS_RELEASE_VERSION`. Filenames,
Fabric metadata, NeoForge metadata, test-mod dependencies and Gradle archive
versions use the same value. Normal development builds default to the version
in `src/main/resources/fabric.mod.json`. Source metadata is not rewritten in CI.
Historical `v<VERSION>+mc26.2`, `+mc1.21.1` and their `-neoforge` forms are also
accepted, but new releases should use one shared `v<VERSION>` tag.

Tags with a prerelease suffix, including `-alpha` and `-beta`, create GitHub
prereleases. Plain versions such as `v0.1.0` create stable releases. A per-release
`docs/releases/<VERSION>.publication.json` can explicitly set `github_latest`.
GitHub Latest requires the normal release flag, so Beta 2 uses that flag while
its name, notes and mod-platform channel remain Beta. Other beta tags retain
the prerelease default; stable tags retain the Latest default. Add curated
notes at `docs/releases/<VERSION>.md`; otherwise the workflow uses GitHub's
generated commit notes and adds the supported loader/game targets.

## Checks before publication

The workflow generates and verifies frozen resources, builds all eight targets,
runs Python resource/packaging/release tests and Java worldgen/gameplay/planning
checks, then runs the native Fabric 26.2 packet/gameplay/restart suite. The
1.21.1 and 1.21.11 JARs target Java 21; 26.2 and 26.3 target Java 25.
The additional profiles are built twice for identical checksums and run gameplay,
restart, seven world-load rejection cases, recovery and natural-structure checks
through `tools/check_additional_ports.py`. Gradle 9.6.0 is required. Builds run sequentially
because NeoForge 1.21.1 reuses generated Fabric 1.21.1 sources.

The release bundle rejects incomplete sets, wrong versions/loaders/game targets,
wrong class targets and diagnostic classes. Publication creates a draft, uploads
the verified files, downloads them again and compares every SHA-256 before
making the release visible. Failed uploads leave a draft that a rerun can resume.
A published release is never overwritten: an exact rerun verifies the downloads;
a mismatch or incomplete published release stops with an error.

The workflow uses the built-in `GITHUB_TOKEN` with `contents: write`; no personal
token is needed. Release files are uploaded directly from the build job, so
GitHub Actions artifact-storage quota does not block publication. Branch/PR
validation stays in `build.yml`, which no longer runs a duplicate build on tags.

Branch pushes and pull requests containing only Markdown files (`**/*.md`)
skip the full mod build. A mixed change containing any other file still builds,
including JSON manifests, structure assets, test/build scripts and workflow
configuration. Manual builds remain available. Release-tag builds are independent
of this filter and continue to build and validate all eight targets.

## Automatic platform uploads

After the GitHub release succeeds on a tag push, the workflow calls the reusable
`publish-platforms.yml` for the same tag. It downloads exactly the published player
JARs and checksum manifest, resolves dependencies and uploads to Modrinth and
CurseForge. Separate, sequential platform jobs keep shared receipts consistent
and let the other platform continue if one fails. Pending public downloads are
reported with IDs and a warning; moderation is not treated as completed.

The repository already contains the platform tokens and project-ID variables.
Manual dispatch of this build workflow still does not publish. The platform
workflow has a separate manual plan/recovery entry point, read-only by default.
See [platform publication](../technical/PLATFORM_PUBLICATION.md) for required
credentials, receipt-based retries and the distinction between uploads and
public project approval. No existing release tag needs to be moved.

Historical Alpha releases and `1.0.0-beta.1` retain their four-file contracts.
Subsequent 1.x versions, including `1.0.0-beta.2`, require all eight targets.
The uploader can still verify the old releases and receipts without adding files.

## Build-only test

Run **Actions → Release all targets → Run workflow** on the desired ref and
enter a version tag, for example `v0.1.0-alpha.5.0.3`. Manual dispatch builds and
tests the selected ref with that version and **never publishes a release**.
Optional three-day workflow downloads may be unavailable if the account's
Actions artifact quota is full; checksums remain in the run summary.

```shell
gh workflow run release.yml --ref main -f tag=v0.1.0-alpha.5.0.3
```

Local helper checks do not publish:

```shell
python -m unittest discover -s tests -p "test_release_ci.py" -v
python tools/release_ci.py prepare --tag v0.1.0-alpha.5.0.3
python tools/release_ci.py bundle
```

Local verification on October 28: both workflows pass actionlint 1.7.12; eleven
release-boundary tests pass. The four normal-version artifacts retain their
previously runtime-tested SHA-256 values after the shared-version change. A
separate NeoForge 26.2 build with version `0.1.0-alpha.5.0.3-ci.1` also passes
metadata, asset and class-target checks. Nothing was published by these tests.

GitHub references: [tag triggers](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow),
[token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token),
[release creation](https://cli.github.com/manual/gh_release_create).
