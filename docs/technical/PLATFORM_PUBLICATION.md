# Platform setup and release uploads

The [access setup](PLATFORM_ACCESS.md) records credential locations and project IDs.
Never put token values in source files, command arguments, screenshots or logs.

## Edit the Modrinth draft

`python3 tools/configure_modrinth.py` prints the intended fields without changes.
`--apply` writes the prepared description, MIT license, categories and project
links to draft `F6QDr5Vr`, then reads them back. The helper refuses an approved,
processing or otherwise non-draft project. It does not send status changes,
submit the project for review or create a version. The original project JSON is
retained under ignored `build/platform-preparation/` before the first edit.
`--apply --icon` additionally uploads the Colossus screenshot icon from
[branding assets](../../assets/branding/README.md).

The draft gallery uses the three original shader captures listed in the branding
notes, with the river view featured. They show the earlier V3 model and carry
that caption. The description's opening image uses the same river capture.
The gallery was configured through the documented
[gallery-image API](https://docs.modrinth.com/api/operations/addgalleryimage/).

Modrinth now derives its supported environments from versions. The upload
metadata explicitly specifies `client_and_server` on every target. The project
description explains the matching client/server installation before versions exist.

The documented [CurseForge author API](https://support.curseforge.com/support/solutions/articles/9000197321-curseforge-upload-api)
supports file uploads and file metadata updates, not general project-page editing.
Its description, MIT selection, source/issue links and project icon must therefore
be applied in the author dashboard using the [prepared page](../releases/CURSEFORGE_DRAFT.md).
The project ID and token are already configured; no extra credentials are needed
for the documented version-upload API.

## Plan platform uploads

The workflow file is prepared locally. The current GitHub OAuth credential lacks
the `workflow` scope and GitHub rejected a push containing the new workflow.
Normal code/docs can be pushed, but activating this workflow still requires that
additional GitHub permission. No platform upload has been triggered.

The new **Plan or publish platform versions** workflow runs only on manual
dispatch. It takes the tag of an already existing GitHub release. Its `publish`
input defaults to false. The plan job downloads only the four player JARs and
`SHA256SUMS.txt`, reads the release notes and validates the full set. There are no
platform POST/PATCH calls in this mode. The existing build/release workflow's
manual dispatch remains build-only.

Local equivalent with an existing complete bundle:

```shell
python3 tools/publish_platforms.py --tag v0.1.0-beta.1 --directory dist/release --notes docs/releases/0.1.0-beta.1.md --output build/platform-preparation/upload-plan.json
```

The beta tag in this example has not been created or released. Before any
upload, the helper checks all four filenames, target metadata, class versions,
MIT license, credits and SHA-256 manifest. It resolves the pinned Fabric API and
Lithostitched versions for Modrinth and confirms the game/loader/Java tags exist
on CurseForge. Each file gets exactly its own game version and loader; Fabric API
is required only for Fabric. Version channels follow the approved alpha/beta/
release version, and development suffixes are rejected.

CurseForge's documented relation format names a required project, not a specific
dependency file. Its launcher selection therefore cannot be pinned to the exact
Lithostitched version through this relation field; the installation guide keeps
the tested exact version explicit. Modrinth dependencies are pinned by version ID.

## Upload only after approval

For Beta 1.0.0, the author has explicitly approved publication before the natural
Survival playthrough. The [publication record](../releases/BETA_1_0_0_PUBLICATION.md)
supersedes the former pre-release Survival gate for this beta. The release notes
state the outstanding test honestly. The old unreleased candidate notes retain
their pending marker and must not be used for this release.

Use `--platform curseforge` or `--platform modrinth` to act on just one platform
when the other's access or eligibility is unresolved. The default remains both.
Receipts are kept in the same release journal and retain duplicate protection.

After the Survival result, final release approval and platform eligibility checks,
publish the verified GitHub release through the existing tag workflow. Then run
the platform workflow for that exact tag with `publish` enabled. The upload job
starts only after the plan succeeds. The helper also requires both the exact
`--approved-tag` and `PLATFORM_PUBLICATION_APPROVED` value to match the tag.
Unresolved Survival/source/download markers in release notes prevent execution.
The current beta notes deliberately retain `SURVIVAL_ACCEPTANCE: pending`.

No upload job runs on a branch push, pull request or ordinary build-only dispatch.
Setting up secrets or editing the draft does not authorize a public beta release.
Uploading a first version does not itself guarantee project moderation approval.

## Receipts, reruns and verification

`platform-upload-state.json` is maintained as an extra asset on the existing
GitHub release. It binds the tag, both project IDs and the four file hashes.
The upload intent is saved **before** each POST; the returned platform ID is
saved immediately afterward. Only that receipt asset is overwritten. Existing
player JARs are never replaced. GitHub concurrency serializes runs for a tag.

An exact Modrinth version already present with matching hashes, target metadata
and dependencies is reused. A conflicting version stops the run before uploads.
CurseForge uses the saved file ID to retry download verification rather than
uploading again. If a previous POST has an unknown outcome and no receipt ID,
the helper stops for investigation; do not blindly delete the intent and retry.

Both platforms' downloaded bytes must match the approved SHA-256. Moderation
can delay availability. In that case the ID stays recorded, the run reports
pending verification and a rerun checks again without creating another upload.
It is not reported as a verified public release until downloads actually match.

API references: [Modrinth project editing](https://docs.modrinth.com/api/operations/modifyproject/),
[Modrinth versions](https://docs.modrinth.com/api/operations/createversion/),
[CurseForge uploads and file metadata](https://support.curseforge.com/support/solutions/articles/9000197321-curseforge-upload-api).
