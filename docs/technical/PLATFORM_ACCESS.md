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
read back; status remains `draft` with zero versions. The earlier unknown-license
observation above is historical. No project was submitted for review.

The existing release workflow still publishes only to GitHub. A separate
`publish-platforms.yml` workflow now plans platform uploads by default and
requires an explicit publish selection for an exact approved GitHub release.
It has not uploaded any files. See [platform publication](PLATFORM_PUBLICATION.md)
for the checks, persistent receipts and rerun behavior. The Survival acceptance,
final artifacts, platform eligibility review and explicit public beta approval
remain required before release.
