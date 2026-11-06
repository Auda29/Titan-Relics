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

## Read-only verification

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

## Automation remains to be implemented

The existing release workflow currently publishes only to GitHub. Storing these
credentials does not add Modrinth/CurseForge uploads or trigger a release.
Future tooling can use the identifiers above. Keep project-page edits separate
from release uploads, and preserve the build-only manual-dispatch behavior.
The Survival acceptance, final artifacts, platform eligibility review and explicit
public beta approval in the [publication checklist](../releases/PUBLIC_BETA_PREPARATION.md)
remain required before release.
