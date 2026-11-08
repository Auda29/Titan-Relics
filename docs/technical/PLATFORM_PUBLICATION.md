# Platform setup and release uploads

## Automatic release-tag path

Every new canonical `v<VERSION>` release tag runs
[release.yml](../../.github/workflows/release.yml). It builds and tests all four
Fabric/NeoForge targets, publishes the verified GitHub release, then calls
[publish-platforms.yml](../../.github/workflows/publish-platforms.yml) with that
exact tag and publication enabled. A failed build/test/GitHub-release job prevents
platform uploads. Branch pushes and pull requests do not publish versions.
A manual run of **Release all targets** remains build-only.

The platform workflow downloads the four player JARs, SHA256SUMS.txt and release
notes from the published GitHub release. It does not build another bundle. It
validates target metadata, class versions, MIT and checksums, resolves pinned
Modrinth dependencies and checks CurseForge's game/loader/Java tags before writes.

The user's November 8 instruction authorizes this release-tag publication path.
CI passes the tag as both `--approved-tag` and `PLATFORM_PUBLICATION_APPROVED`.
The helper still refuses noncanonical tags, conflicting project IDs, incomplete
bundles, checksum mismatches, unsupported release channels and unresolved release
note markers. Beta 1's Survival test was explicitly deferred to the public beta;
its notes state that honestly. The old unreleased preparation notes with
`SURVIVAL_ACCEPTANCE: pending` remain unsuitable for publishing.

## Separate platform jobs and credentials

Modrinth and CurseForge have separate upload jobs, with `fail-fast: false`.
One platform's upload failure does not cancel the other's job. `max-parallel: 1`
serializes their writes to the shared release journal. The reusable workflow's
per-tag concurrency group also serializes automatic and manual platform runs.
Do not run a local uploader against the same tag while CI is uploading it.

Repository secrets `MODRINTH_TOKEN` and `CURSEFORGE_TOKEN` and variables
`MODRINTH_PROJECT_ID=F6QDr5Vr`, `CURSEFORGE_PROJECT_ID=1785231` are already configured.
The caller passes only those two platform secrets. GitHub's built-in token has
`contents: write` in upload jobs to save receipts on the existing release;
no personal GitHub token is stored in CI. Editing workflow files requires an
appropriately authorized GitHub account/app, separately from these CI credentials.
See [credential access](PLATFORM_ACCESS.md); never print credential values.

## Receipts, moderation and retries

`platform-upload-state.json` on the GitHub release binds the tag, both project
IDs and all four hashes. An upload intent is saved before each POST and the
returned platform ID immediately afterward. Existing player JARs are not replaced.
An exact existing Modrinth version is reused after checking hashes and metadata.
An ambiguous previous POST without a confirmed ID stops for investigation.

Public downloads must match the approved SHA-256. CurseForge changes `+` in
uploaded filenames to `-`; its verifier uses the published spelling confirmed
against all four public Beta 1 file IDs. This does not change the JAR bytes or
GitHub filenames. Modrinth download URLs come from version metadata.

The CLI returns 2 when accepted uploads are awaiting public download verification.
CI records this as a warning, with IDs and pending state in the run summary,
rather than claiming that moderation passed. The JSON result also records the
IDs, phases and pending files. Real API failures and checksum/metadata mismatches
fail the job. Neither workflow changes project visibility, submits the project
again or removes content disclosures.

Use **Re-run failed jobs** for actual failed uploads. A successful or pending
upload receipt prevents duplicate uploads on a retry. To recheck pending
availability without rebuilding, use the manual workflow below; it reuses IDs.
Moderation and first-project approval remain external platform decisions.

## Manual plan or recovery

Open **Actions → Plan or publish platform versions → Run workflow**. Select the
workflow ref containing the current uploader and enter an existing GitHub release
tag. Leave `publish` false for a read-only plan. Set it true only to upload or
resume/check that release. The same per-tag lock and receipt protection apply.
The publisher code comes from the selected workflow ref; player files and notes
always come from the requested published release. This allows current verification
fixes to check an older release without moving its tag or replacing its JARs.

Local read-only equivalent:

```shell
python3 tools/publish_platforms.py --tag v1.0.0-beta.1 --directory dist/public-beta-1.0.0 --notes docs/releases/1.0.0-beta.1.md --output build/platform-preparation/upload-plan.json
```

For an authorized local upload, also pass `--execute --approved-tag <TAG>` and set
`PLATFORM_PUBLICATION_APPROVED` to that tag. `--platform curseforge` or
`--platform modrinth` selects one service; both are selected by default.

## Project-page editing

The Modrinth draft helper prepares license, text, categories, links and the
Colossus screenshot icon; it refuses non-draft projects and never submits review.
The published project's code/assets/text AI disclosures must remain intact.
CurseForge's documented author API edits files, not general project pages.
The author confirmed its description, images, logo, MIT and links in the dashboard.
[Beta 1's publication record](../releases/BETA_1_0_0_PUBLICATION.md) retains the
historical setup, exact file IDs, moderation checks and verified download hashes.

API references: [GitHub reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows),
[Modrinth versions](https://docs.modrinth.com/api/operations/createversion/),
[CurseForge uploads](https://support.curseforge.com/support/solutions/articles/9000197321-curseforge-upload-api).
