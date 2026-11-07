# Beta 1.0.0 publication record

## Author decision, 6 November 2026

The author explicitly authorized building and publishing the first public beta
on GitHub, Modrinth and CurseForge. The full natural Survival playthrough will
use this beta. It is deferred to the public beta phase, not recorded as passed.
Later beta updates will address findings from that playthrough.

The shared version is `1.0.0-beta.1`, tag `v1.0.0-beta.1`. All four target files
use the Beta channel. The former `0.1.0-beta.1` was an unreleased preparation
candidate, not a previous public beta.

The tag workflow builds and tests all four targets and publishes only after its
checks pass. The GitHub release will contain the four JARs and SHA256SUMS.txt.
Source revision, workflow result and platform file IDs will be recorded after
the operations complete. Existing Alpha release assets are not replaced.

## Modrinth eligibility review

The [content rules](https://modrinth.com/legal/rules), checked again on
6 November 2026, sections 6.1 and 6.2 require an AI disclosure and exclude
projects whose content is primarily or entirely AI output or derived from it.
They also exclude page images created or derived from generative AI output.

Available provenance:

- Java sources and asset-generator scripts are present in the repository.
  Development used Codex, including code, generator and documentation changes.
  Commit authors are not a reliable measure of the share of human versus AI work.
- Selected structure exports have pinned hashes and local conversion/generation
  records. This establishes the build inputs, not independent human authorship
  or permission for the referenced visual designs.
- The icon is a deterministic crop of the author's Minecraft screenshot.
  The three gallery images are original shader captures from 1 October 2026.
  This proves capture provenance, not a policy exemption for the assets depicted.
- Visual references are credited to The Archive In Between and Josh White.
  Credits do not establish their permission or endorsement. No reference artwork
  is being newly downloaded or directly packaged for this beta.

The current evidence does not establish eligibility for public search/listing
under the restriction on predominantly AI-derived content. The official
[AI guidance](https://support.modrinth.com/en/articles/16551575-disclosure-and-usage-of-ai)
also explains that some such projects may be hosted unlisted. This is a platform
assessment, not an approval that this repository can grant itself.

The author explicitly requested a moderation submission. The intended path is
therefore to disclose code, assets and text formally, provide the provenance
context in the disclosure note, upload the four beta files to the existing draft
and request moderation. This asks the platform for its decision and does not
assert that the project has already passed eligibility review. No direct change
to approved/public status is made by the uploader.

The [official disclosure route](https://github.com/modrinth/code/blob/main/apps/labrinth/src/routes/v3/disclosures.rs)
and [schema](https://github.com/modrinth/code/blob/main/apps/labrinth/src/models/v3/disclosures.rs)
provide `GET/PATCH /v3/project/{id}/disclosures`. The planned declaration is
`ai_content` with `code`, `assets` and `text`, explaining substantial Codex
contributions, maintainer design/review/testing, source screenshots and visual
references. This is distinct from claiming an LLM is required at game runtime.
Existing moderator locks and unrelated disclosures must be preserved.

The earlier prepared question is handled in the authorized moderation context;
no separate email, support ticket or other external message has been sent.

## CurseForge page access

The documented author API supports file uploads and file metadata, not general
project-page editing. The shared preview browser could not start because
of the host's AppArmor restriction. The separate browser remained on CurseForge's
security verification page and could not reach the author dashboard. Description, MIT, source/issues/wiki links, Colossus icon and
captioned shader images are prepared in the repository for the dashboard.

The author has approved uploading the beta files. Upload responses and moderation
state must be recorded independently of whether the project page can be edited.
No moderation approval or public download is assumed from an accepted upload.

## Verified GitHub release

- Source revision: `9f6f2afe98b91f7aaaecd29f058350eda796cdf1`.
- Tag: `v1.0.0-beta.1`.
- [Release CI](https://github.com/Auda29/Titan-Relics/actions/runs/42209876403): success.
- [Published prerelease](https://github.com/Auda29/Titan-Relics/releases/tag/v1.0.0-beta.1): four JARs and SHA256SUMS.txt.
- All four release downloads were independently revalidated against the manifest,
  target metadata, class versions, MIT and the current canonical credits.
- CI passed 187 Python tests, 764 worldgen assertions, 65 static mixin target
  contracts, 677 headless gameplay assertions, the distribution/planning tests
  and native Fabric 26.2 gameplay/recipe-packet/server-restart checks.
- The native server evidence binds to the Fabric 26.2 SHA-256 below. No completed
  natural Survival playthrough or new graphical client acceptance is claimed.

| Artifact | SHA-256 |
| --- | --- |
| `relics-1.0.0-beta.1+mc26.2.jar` | `7929d739661865eefb5c6655984109c60143c53988cee79ee59de9d8436e2946` |
| `relics-1.0.0-beta.1+mc1.21.1.jar` | `4f50ab03024d10f2bdf6ae3d69b6ed450bb03f4f945c94c9069016f8b4f0e167` |
| `relics-1.0.0-beta.1+mc1.21.1-neoforge.jar` | `6b4bf215957be9bf588b73233b6933b31aa0f1038843ad63d4305349dfecf01e` |
| `relics-1.0.0-beta.1+mc26.2-neoforge.jar` | `d6597e10afe58fa020c479f6df7e492e67f6a0f1ad7ef5a15ca66f900428dd68` |

## CurseForge uploads

The author API accepted all four uploads to project `1785231`. Each returned ID
was saved in `platform-upload-state.json` on the GitHub release. The first public
download verification was pending; acceptance of an upload does not establish
moderation approval or a verified public download.

| Artifact | File ID |
| --- | --- |
| `relics-1.0.0-beta.1+mc26.2.jar` | `9472906` |
| `relics-1.0.0-beta.1+mc1.21.1.jar` | `9472912` |
| `relics-1.0.0-beta.1+mc1.21.1-neoforge.jar` | `9472918` |
| `relics-1.0.0-beta.1+mc26.2-neoforge.jar` | `9472923` |

## Modrinth submission

All four uploads have verified SHA-256 hashes matching the GitHub beta bundle.
The formal `ai_content` disclosure contains `code`, `assets` and `text`, with an
explanation of the substantial Codex contribution and the image/asset provenance.
It was read back through the v3 API. Existing unrelated disclosures were not removed.

On 6 November 2026 at 11:48:13 UTC, the project update requesting `processing`
was accepted. A readback confirmed `processing`, `requested_status: approved`,
four versions and no approval timestamp or moderator message. No direct request
to set `approved` was made. Public eligibility and the moderation decision remain
pending; upload/download verification is not moderation approval.

| Artifact | Modrinth version ID |
| --- | --- |
| `relics-1.0.0-beta.1+mc26.2.jar` | `q3mOZDVk` |
| `relics-1.0.0-beta.1+mc1.21.1.jar` | `pO4LS3zQ` |
| `relics-1.0.0-beta.1+mc1.21.1-neoforge.jar` | `2vAzauJb` |
| `relics-1.0.0-beta.1+mc26.2-neoforge.jar` | `B3gFvc5t` |

## Remaining external state

A second check of the existing CurseForge file IDs still could not verify public
downloads. No files were uploaded again. The dashboard alignment initially
remained unverified because the author API cannot perform those page edits.
The updated image/description handoff is available locally under
`build/platform-preparation/titan-relics-platform-images-20261106.zip`.

A one-time follow-up is scheduled in this conversation for **6 November 2026,
12:21 UTC**, to read moderation state and recheck known downloads without
reuploading or changing publication/AI settings. If still pending, it will report
the state without creating further recurring work.

## Author confirmation of CurseForge page completion

On 6 November 2026, the author confirmed in this conversation that all instructed
CurseForge dashboard steps were completed, including the description, images,
logo, MIT and project links. The screenshot upload initially failed at the 2 MB
limit; smaller PNG copies were provided before the confirmation.

The page-alignment task is therefore complete on the author's confirmation.
It has not been independently inspected through an authenticated browser.
This confirmation does not establish moderation approval or public download
availability. The planned follow-up should check those external states and must
not present the page alignment as a remaining manual task for the author.

## Read-only follow-up, 7 November 2026

The interrupted one-time follow-up was completed on 7 November. The check began
at `2026-11-07T09:31:20.814472+00:00`. The release receipt was downloaded again and its tag,
project IDs and four SHA-256 values matched the local published beta bundle.
All existing upload IDs above were retained.

- Modrinth remains `processing`, with no approval timestamp and no moderator
  message. All four known version files were downloaded successfully and matched
  the approved SHA-256 values. This does not establish project approval.
- A read-only v3 disclosure check confirmed `ai_content` still includes `code`,
  `assets` and `text`. No disclosure or project setting was changed.
- All four known CurseForge file URLs returned HTTP 403. Percent-encoding the
  filename's plus sign produced the same result. No public file hash could be
  verified. These responses do not establish a moderation rejection or its cause.
- The public CurseForge project page was inaccessible through the web retrieval
  tool. The author's confirmation of completed dashboard work remains valid;
  the page alignment is not reopened as a manual task.

No files were uploaded, no publication status or visibility was changed, no tags
or releases were created, and the remote upload receipt was not modified. The
check evidence is retained locally at
`build/platform-preparation/moderation-check-20261107/result.json`.
No further automation was created. GitHub remains the verified public beta
download destination while these external states are unresolved.
