# Relic design and gameplay index

Each relic has its own folder. Keep shared workflows in [docs/](../docs/README.md)
and implementation code in `src/`, `tools/`, and `tests/`.

| Relic | Current status |
| --- | --- |
| [Colossus](colossus/README.md) | V3 selected in Alpha 3; core, magnet, and head-trial gameplay not implemented |
| [Obelisk](obelisk/README.md) | V3 selected in Alpha 3; archaeology, collectibles, and Colossus maps not implemented |
| [Titan Skull](titan-skull/README.md) | V3 selected in Alpha 3 with worldgen; authored ordinary-mob exploration not implemented |
| [Ruined Tower](ruined-tower/README.md) | Concept only |
| [World Tree](world-tree/README.md) | Concept only |

## In-game demos

- [Colossus V3 shader demo](colossus/demo/README.md): three actual Minecraft
  screenshots in normal terrain, separate from generated Blender previews.

## V4 studies from in-game inspection

The V3 models remain selected in Alpha 3. The following documents record the
agreed visual findings and revision direction. Colossus V4 now has two offline
[export variants](colossus/docs/COLOSSUS_V4_EXPORTS.md), with B / open machine frame
selected by the user. [Obelisk V4](obelisk/docs/OBELISK_V4_EXPORTS.md) and the four
[Titan Skull V4 variants](titan-skull/docs/TITAN_SKULL_V4_EXPORTS.md) are exported
and checked offline. The latest approved versions are listed below; integration remains pending.

Latest corrections: [Colossus V4.1](colossus/docs/COLOSSUS_V4_1.md) replaces the
raised wrist with a palm-up right hand and curled fingers;
[Obelisk V4.1](obelisk/docs/OBELISK_V4_1.md) replaces contrasting patches with
consistent sandstone facets and larger actual cracks. Previous exports are retained.

The user has **visually accepted Colossus V4.1, Obelisk V4.2 and all four Titan
Skull V4 terrain variants**. Game integration and in-game checks remain pending.

**Next design priority:** create the remaining planned relics before starting
V5 architectural interiors. The original catalog still has two unmodeled motifs:
the Ruined Tower and World Tree. A second smaller Colossus has an archived starting
model. A [second independent Titan Skull reference](titan-skull/docs/TITAN_SKULL_2_CONCEPT.md)
is now selected; further skull/bone variants remain future extensions. The order
among these new studies has not yet been selected.

- [Colossus V4](colossus/docs/COLOSSUS_V4.md): preserve the overall design; focus on
  damaged rear armor, a readable hand with potentially raised fingers, and removal
  or replacement of the simple chest-interior cylinder.
- [Obelisk V4](obelisk/docs/OBELISK_V4.md): weathering, material readability and
  a naturally buried archaeological site at the foot.
- [Titan Skull V4](titan-skull/docs/TITAN_SKULL_V4.md): organic mound transitions,
  biome-compatible surfaces and clearer fossil/bone materials.

## Discovery hierarchy and lore

A [Colossus material/salvage study B](colossus/docs/COLOSSUS_MATERIAL_STUDY_B.md)
retains 25,423 copper blocks and 90 raw iron items without changing any V4.1
occupied position. Mining reveals armour openings while preserving the head/body
connection and all surviving component connections. The user accepted this
material version and its post-salvage appearance on October 2, 2026.

The intended discovery order is **Titan skulls and future bone/skull variants
(most common) -> Obelisks (clearly rarer) -> the unique large Colossus**. The large
Colossus should occur **once per game world/save**, shared by all players. Planned
**smaller Colossi may occur multiple times**, with separate rarity/loot decisions
still open. Alpha 3 has provisional repeatable candidate rates and does not yet
enforce uniqueness; future skull/bone variants share a family-level density target.

Obelisk maps initially lead to the same large site. Its vault preserves per-player
core eligibility for multiplayer; the shared magnet chest and archaeology still
need later-visitor reward policies. The
[lore/gameplay review](../docs/project/LORE_GAMEPLAY_REVIEW.md) tracks material
economy, historical trial integration, lasting core usefulness, visible lore
links, multiplayer distribution, and measured discovery effort as open tasks.

The working history connects the three: a Colossus was sent to kill the Titans,
while Obelisks served as wayfinders or marked destroyed Titans. Details remain
open in the [lore bible](../docs/project/LORE-BIBLE.md).

## Folder convention

```text
<relic>/
  README.md             # Entry point, status, and links
  docs/                 # Design decisions and version history
  design/
    <asset>.json        # Export/material/preview configuration
    generated/<asset>/  # Blender models, exports, reviews, and provenance
  gameplay/             # Items, loot, encounters, and other gameplay decisions
  demo/                 # Optional in-game screenshots and presentation gallery
```

Future hand-edited sources can live in `<relic>/design/blender/`, separate from
generator outputs. Run pipeline commands from the repository root: config paths
inside JSON remain **repository-root-relative**, not relative to the config file.

Generated folders retain their existing version names, including the Colossus's
original `ots/` experiment. Git includes selected source models, whole exports,
review sheets, and provenance; intermediate files and tile exports stay local.
Do not regenerate assets just to move them.

The playable Alpha 3 explicitly selects the three V3 exports using
`tools/integrate_v3.py`; see [V3 integration](../docs/technical/V3_INTEGRATION.md).
Organizing an asset here alone does not select it or implement proposed gameplay.
