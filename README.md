# Titan Relics

*Colossal ruins of a forgotten age*

![Large Colossus across a river, captured in Minecraft with shaders](relics/colossus/demo/colossus-v3-shaders-river.png)

*In-game shader capture, 1 October 2026. Earlier Colossus V3 model; interim preview.*

Explore monumental remains in Minecraft's Overworld: abandoned colossi,
weathered obelisks, titan skulls, a World Tree and a ruined tower. Investigate
archaeological sites, follow expedition maps and recover useful machinery.
The landscape leaves much of its history for you to interpret.

## Downloads and release status

The current release candidate is **1.0.0-beta.3**, built for all eight targets by
the [GitHub release workflow](https://github.com/Auda29/Titan-Relics/actions/workflows/release.yml).
The [Beta 3 release](https://github.com/Auda29/Titan-Relics/releases/tag/v1.0.0-beta.3)
receives downloads after validation. Choose one matching JAR and install its
dependencies separately. Verify downloads against that release's `SHA256SUMS.txt`.

The same tag uploads to [Modrinth](https://modrinth.com/project/titan-relics)
and [CurseForge](https://www.curseforge.com/minecraft/mc-mods/titan-relics).
Their moderation and public-download status are separate from GitHub publication.
CurseForge spells `+mc` as `-mc` in download filenames.

| Minecraft | Loader | Beta filename | Java |
|---|---|---|---|
| 1.21.1 | Fabric | `relics-1.0.0-beta.3+mc1.21.1.jar` | 21+ |
| 1.21.1 | NeoForge | `relics-1.0.0-beta.3+mc1.21.1-neoforge.jar` | 21+ |
| 1.21.11 | Fabric | `relics-1.0.0-beta.3+mc1.21.11.jar` | 21+ |
| 1.21.11 | NeoForge | `relics-1.0.0-beta.3+mc1.21.11-neoforge.jar` | 21+ |
| 26.2 | Fabric | `relics-1.0.0-beta.3+mc26.2.jar` | 25+ |
| 26.2 | NeoForge | `relics-1.0.0-beta.3+mc26.2-neoforge.jar` | 25+ |
| 26.3 | Fabric | `relics-1.0.0-beta.3+mc26.3.jar` | 25+ |
| 26.3 | NeoForge | `relics-1.0.0-beta.3+mc26.3-neoforge.jar` | 25+ |

Beta 3 redesigns the generation menu around simple play styles and an optional
advanced view. New presets favor skulls and search for a closer Colossus. Existing
worlds keep their saved rules; use a new world and explicitly select a preset to
test the new distribution. This testing release includes unresolved Sword Skull
ground-contact findings and has not completed visual menu or Survival acceptance.
See the [release notes](docs/releases/1.0.0-beta.3.md) for exact limits and test steps.
The [Beta 1 publication record](docs/releases/BETA_1_0_0_PUBLICATION.md) is historical;
new platform availability is recorded on each release's upload receipt.
The earlier [Alpha 5.0.5](https://github.com/Auda29/Titan-Relics/releases/tag/v0.1.0-alpha.5.0.5)
remains available as a historical release.

## Start playing

1. Follow the [installation and dependency table](docs/players/INSTALLATION.md)
   for your exact Minecraft version and loader. Install Titan Relics and its
   dependencies on the server and every player client for multiplayer.
2. Back up existing saves. Create a new Overworld with structure generation
   enabled for the complete current relic selection.
3. Open **Create World → World → Relic generation** to choose a preset before
   creating the world. The [short player guide](docs/players/PLAYER_GUIDE.md)
   explains the settings and basic systems without giving away every discovery.

Relics can be far apart. Minimum distances and search spacing do not guarantee
a nearby find. Each world's generation settings stay frozen, including for
unexplored chunks; changing installation defaults does not migrate an old world.
Existing structures and finite shared loot are not moved or replenished.

## Compatibility and feedback

Fabric and NeoForge support **1.21.1, 1.21.11, 26.2 and 26.3**.
The [port validation report](docs/releases/JAVA_1_21_11_26_3_PORTS.md) records the
additional targets' checks. The 1.21.1 builds use ferns and ordinary chests in place of unavailable 26.2 blocks.
Other game versions and cross-loader save conversion are not offered.

Read the [known limits and tested mod combinations](docs/technical/MOD_COMPATIBILITY.md)
before changing a modpack. In particular, DH 3.3.3 `FEATURES` can omit relics
during distant generation; `INTERNAL_SERVER` is the tested alternative for new
distant generation. The candidate's compatibility results are bounded tests,
not FPS, memory or all-modpack guarantees.

Report problems through the [issue tracker](https://github.com/Auda29/Titan-Relics/issues/new/choose).
Include exact versions, reproduction steps and the complete relevant log.
The [reporting guide](docs/players/INSTALLATION.md#reporting-a-problem) explains
which files to attach and what private information to remove.

## Inspirations and credits

Titan Relics draws visual inspiration from
[The Archive In Between](https://www.instagram.com/thearchiveinbetween/),
especially its overgrown colossi, titan remains and monumental trees.
The Obelisk and Ruined Tower also draw on references by Josh White.
See [credits and original reference links](CREDITS.md).

## Development and publication

- [Documentation index](docs/README.md), [current status](docs/project/CURRENT_STATUS_AND_ROADMAP.md)
  and [beta roadmap](docs/project/PUBLIC_BETA_ROADMAP.md).
- [Release workflow and local checks](docs/releases/RELEASE_CI.md).
- [Platform upload planning and explicit release controls](docs/technical/PLATFORM_PUBLICATION.md).
- [Publication preparation, Modrinth and CurseForge drafts](docs/releases/PUBLIC_BETA_PREPARATION.md).
- [Name decision and earlier proposals](docs/project/NAMING.md). The selected name is Titan Relics;
  the internal mod ID remains `relics`.
- [Relic design index](relics/README.md) and [archived README/development history](docs/project/README_HISTORY_20261105.md).

## License and modpacks

Titan Relics is licensed under the [MIT License](LICENSE). This covers the
project code, documentation and original project assets to the extent the
author holds the rights. Third-party works and visual references retain their
own rights; see [credits](CREDITS.md).

You may use, modify and redistribute the MIT-licensed project, including in
modpacks and commercially, while retaining its copyright and license notice.
No individual modpack permission request is needed. The original creators
listed in the credits are not granting rights through this project license.

This license decision applies to the current source and future builds. Existing
Alpha downloads have not been replaced or had their embedded notices rewritten.
