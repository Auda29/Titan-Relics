# CurseForge publication draft

Prepared 5 November 2026. Local review copy only; no external project exists as
part of this preparation. The selected name is Titan Relics. Slug availability, license and public beta
approval remain pending. The [shared preparation checklist](PUBLIC_BETA_PREPARATION.md) applies.
The repository is now public at https://github.com/Auda29/Titan-Relics.
The source, player documentation and issue tracker use that public destination.

## Proposed project fields

| Field | Draft value |
|---|---|
| Game / class | Minecraft Java Edition / Mods |
| Name | Titan Relics |
| Tagline | Colossal ruins of a forgotten age |
| Slug / project ID | `titan-relics` proposed; availability unchecked, no project created |
| Summary | Explore colossal ruins, uncover archaeology and follow expedition maps to recover ancient machinery. |
| Main category | World Gen; confirm current portal options |
| Additional categories | Structures; Adventure and RPG, if available and appropriate |
| License | Decision pending; current metadata is All-Rights-Reserved |
| Source | https://github.com/Auda29/Titan-Relics |
| Issues | External tracker: https://github.com/Auda29/Titan-Relics/issues |
| Wiki | https://github.com/Auda29/Titan-Relics/blob/main/docs/players/PLAYER_GUIDE.md |
| Logo | Original 400 × 400 PNG to meet moderation guidance; final artwork pending |
| Distribution / modpack permissions | Author decision pending; review separately from license |

## Description draft

*Colossal ruins of a forgotten age*

Discover the remains of an age of giants. Titan Relics adds monumental structures
to Minecraft's Overworld: abandoned colossi, weathered obelisks, titan skulls,
a World Tree and a ruined tower.

Bring a brush to investigate archaeological remains, follow recovered expedition
maps and search ancient machinery. Recover a rechargeable Machine Core for
furnaces, blast furnaces and smokers, or use a repairable Salvage Magnet to gather
nearby dropped items while held. Each landmark offers part of a history that the
landscape never fully explains.

### World settings

Select Expedition, Balanced or Discoveries before creating a world. You can also
edit distances, family shares and biome rules. Worlds retain their saved settings,
including in unexplored chunks. Suitable terrain may be far away, so minimum
distances are not maximum journey lengths. Expedition maps share the same unique
large Colossus destination in a supported world.

### Requirements

Use the file matching both your Minecraft version and loader:

- Minecraft 1.21.1: Java 21, Fabric or NeoForge.
- Minecraft 26.2: Java 25, Fabric or NeoForge.
- All targets need the matching Lithostitched 1.8.0 build.
- Fabric targets additionally need the matching Fabric API. NeoForge targets do not.

Install the mod and dependencies on the server and every player client. A new
world with structures enabled gives the complete current selection. The 1.21.1
builds use ferns and ordinary chests instead of unavailable 26.2 blocks.

### Status and support

This is a beta-page draft, not an available beta download. The full natural
Survival playthrough is awaiting acceptance. Shared archaeology and ordinary
containers are finite; updates and later visitors do not refill them. Back up
worlds before changing mods or datapacks. Frozen plans are not automatically
migrated to a different modpack setup.

DH 3.3.3 FEATURES can omit relics in distant generation; INTERNAL_SERVER passed
for new distant generation. Large Voxy pregeneration settings, old LOD-cache
repairs and long-term FPS/memory behavior remain unverified. Compatibility
evidence applies to the documented setups and versions.

Read the [installation instructions](https://github.com/Auda29/Titan-Relics/blob/main/docs/players/INSTALLATION.md),
[player guide](https://github.com/Auda29/Titan-Relics/blob/main/docs/players/PLAYER_GUIDE.md)
and [compatibility notes](https://github.com/Auda29/Titan-Relics/blob/main/docs/technical/MOD_COMPATIBILITY.md).
Submit bugs through the [issue tracker](https://github.com/Auda29/Titan-Relics/issues/new/choose)
with exact versions, logs and steps to reproduce.

### Inspirations and credits

Titan Relics draws visual inspiration from
[The Archive In Between](https://www.instagram.com/thearchiveinbetween/),
especially its overgrown colossi, titan remains and monumental trees.
The Obelisk and Ruined Tower also draw on references by Josh White.
See the [credits and original reference links](https://github.com/Auda29/Titan-Relics/blob/main/CREDITS.md).

## File settings at release

Upload each of the four JARs in the
[shared matrix](PUBLIC_BETA_PREPARATION.md#gemeinsame-dateizuordnung) as its own
Minecraft mod file. Do not wrap the mod JAR in a modpack ZIP. Each file gets only
its actual game version and loader, a distinct display name such as
`Titan Relics VERSION / NeoForge / Minecraft 26.2`, **Beta** release type and the final
release notes. Keep automatic publication disabled until explicit approval.

Add [Lithostitched](https://www.curseforge.com/minecraft/mc-mods/lithostitched)
as a required related project on all four files and
[Fabric API](https://www.curseforge.com/minecraft/mc-mods/fabric-api) only on
Fabric files. Verify matching dependency files and available game-version tags
in the portal before upload. No project IDs are invented in this draft.

The official [submission guide](https://support.curseforge.com/support/solutions/articles/9000197241-creating-and-submitting-a-project)
requires English titles/descriptions and explains that a file upload enters
moderation. It also documents launcher visibility limits for beta-only projects.
Keep the truthful Beta classification and confirm current visibility behavior
before announcing launcher installation. Moderation acceptance is not guaranteed.

Before submission, check name availability and resolve the license/modpack choices, replace the draft
status paragraph with the approved state and verify public documentation links.
Review the current [submission tips](https://support.curseforge.com/support/solutions/articles/9000199552-project-submission-guide-and-tips)
and [moderation policies](https://support.curseforge.com/support/solutions/articles/9000197279-moderation-policies).
