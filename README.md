# Titan Relics

*Colossal ruins of a forgotten age*

Explore monumental remains in Minecraft's Overworld: abandoned colossi,
weathered obelisks, titan skulls, a World Tree and a ruined tower. Investigate
archaeological sites, follow expedition maps and recover useful machinery.
The landscape leaves much of its history for you to interpret.

## Downloads and release status

The published baseline is **Alpha 5.0.5**, available for all four targets from
the [GitHub release](https://github.com/Auda29/Relic-Mod/releases/tag/v0.1.0-alpha.5.0.5).
Choose exactly one matching JAR. Dependencies are installed separately.
The repository is currently private, so these GitHub downloads, documentation
and issue links require repository access. Public download and support destinations
must be established before announcing the beta.

| Minecraft | Loader | Alpha 5.0.5 filename | Java |
|---|---|---|---|
| 1.21.1 | Fabric | `relics-0.1.0-alpha.5.0.5+mc1.21.1.jar` | 21+ |
| 26.2 | Fabric | `relics-0.1.0-alpha.5.0.5+mc26.2.jar` | 25+ |
| 1.21.1 | NeoForge | `relics-0.1.0-alpha.5.0.5+mc1.21.1-neoforge.jar` | 21+ |
| 26.2 | NeoForge | `relics-0.1.0-alpha.5.0.5+mc26.2-neoforge.jar` | 25+ |

An **unpublished beta candidate** adds an explained rejection of incompatible
world setups and makes Discoveries the factory preset for new worlds without
saved choices. Four-target client and bounded compatibility checks are recorded
in the [current status](docs/project/CURRENT_STATUS_AND_ROADMAP.md). These results
do not mean the published Alpha JARs contain those changes. The full Survival
playthrough and public beta approval remain pending. There are no beta download
links or public Modrinth/CurseForge listings announced here yet.

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

Fabric and NeoForge on **1.21.1 and 26.2** are the four release targets. The
1.21.1 builds use ferns and ordinary chests in place of unavailable 26.2 blocks.
Other game versions and cross-loader save conversion are not offered.

Read the [known limits and tested mod combinations](docs/technical/MOD_COMPATIBILITY.md)
before changing a modpack. In particular, DH 3.3.3 `FEATURES` can omit relics
during distant generation; `INTERNAL_SERVER` is the tested alternative for new
distant generation. The candidate's compatibility results are bounded tests,
not FPS, memory or all-modpack guarantees.

Report problems through the [issue tracker](https://github.com/Auda29/Relic-Mod/issues/new/choose).
Include exact versions, reproduction steps and the complete relevant log.
The [reporting guide](docs/players/INSTALLATION.md#reporting-a-problem) explains
which files to attach and what private information to remove.

## Development and publication

- [Documentation index](docs/README.md), [current status](docs/project/CURRENT_STATUS_AND_ROADMAP.md)
  and [beta roadmap](docs/project/PUBLIC_BETA_ROADMAP.md).
- [Release workflow and local checks](docs/releases/RELEASE_CI.md).
- [Publication preparation, Modrinth and CurseForge drafts](docs/releases/PUBLIC_BETA_PREPARATION.md).
- [Name decision and earlier proposals](docs/project/NAMING.md). The selected name is Titan Relics;
  the internal mod ID remains `relics`.
- [Relic design index](relics/README.md) and [archived README/development history](docs/project/README_HISTORY_20261105.md).

The metadata currently declares `All-Rights-Reserved`. A public license and an
explicit modpack policy are still decisions for the author; this preparation
does not grant redistribution permissions or change the license.
