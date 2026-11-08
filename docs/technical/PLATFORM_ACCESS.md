# Platform API access

Configured and checked on 6 November 2026. Credentials are not stored in Git.

## Project identifiers and CI settings

| Platform | Project ID | GitHub Actions secret | GitHub Actions variable |
|---|---|---|---|
| Modrinth | `F6QDr5Vr` | `MODRINTH_TOKEN` | `MODRINTH_PROJECT_ID` |
| CurseForge | `1785231` | `CURSEFORGE_TOKEN` | `CURSEFORGE_PROJECT_ID` |

Both projects use the slug `titan-relics`. The user supplied both identifiers.
The Modrinth ID was independently confirmed through the authenticated project API.
Secret names and variable values were read back from GitHub after setup; secret
values were not retrieved or printed.

For direct API use on this machine, credentials are stored outside the repository
under `~/.config/titan-relics/`: `modrinth.token` and `curseforge.token`, with
`projects.json` holding the project identifiers. The directory is mode `0700`;
these files are mode `0600`. Read tokens within the calling process and send them
in API headers. Do not print them, embed them in URLs, commit them, or include
them in command-line arguments. GitHub Actions secrets cannot be read back for
local API use. Rotate the local file and GitHub secret together when replacing a token.

## Initial read-only verification

- Modrinth `GET /v2/project/titan-relics` succeeded with authentication and returned
  ID `F6QDr5Vr`, title `Titan Relics`, status `draft`, and license
  `LicenseRef-Unknown`. The platform license still needs alignment with the
  repository's MIT decision; this setup did not modify it.
- CurseForge's authenticated `GET /api/game/versions` succeeded and returned a
  game-version list. The same endpoint returned HTTP 401 without a token. This
  verifies authentication, not permission to upload into project `1785231` or
  the project's moderation state.
- No project description, license field, icon, gallery, version or file was
  changed on either platform during credential setup.

## Subsequent configuration and automation

After the initial credential checks, the user authorized the remaining setup.
`configure_modrinth.py --apply --icon` configured the draft with MIT, prepared
text, categories, links and the Colossus screenshot icon. The interim gallery
uses the three original V3 shader captures, with the river view featured. The values were
read back; at that point status was `draft` with zero versions. The earlier unknown-license
observation above is historical. No project was submitted for review.

On November 8, the author requested automatic platform uploads for each new
release tag. `release.yml` now calls `publish-platforms.yml` after the tested
GitHub release succeeds. The reusable workflow uploads the same four JARs in
separate serialized platform jobs. Manual platform runs still default to a
read-only plan. Existing secrets and variables were retained; no additional
personal token was stored in CI. The connected GitHub app activated both workflow
files, resolving the earlier OAuth workflow-edit permission limitation.
See [platform publication](PLATFORM_PUBLICATION.md) for receipts and retries.

Activation commit: `a740cf13fa877b7ef5f1b858c91b73b24b23ef71`. The
[read-only CI plan](https://github.com/Auda29/Titan-Relics/actions/runs/42462817545)
passed against all four existing Beta 1 files, with upload jobs skipped. Local
checks passed 27 publication/release tests and actionlint; the fixed verifier
also confirmed all four real CurseForge file hashes. No new release tag or
player-file upload was used to test the integration. The automatic tag path
will first execute for a new tag containing this workflow revision.

## Beta 1 publication update

The author subsequently approved the public `1.0.0-beta.1` before the full
Survival playthrough. GitHub is published, all four Modrinth uploads have verified
download hashes and the project is submitted for review with formal AI
disclosures. The CurseForge API accepted four uploads to project `1785231`.
The author completed the dashboard page, and public CurseForge downloads were
subsequently verified. Current moderation/download evidence is
in the [publication record](../releases/BETA_1_0_0_PUBLICATION.md).
