# Relic design and gameplay index

Each relic has its own folder. Keep shared workflows in [docs/](../docs/README.md)
and implementation code in `src/`, `tools/`, and `tests/`.

| Relic | Current status |
| --- | --- |
| [Colossus](colossus/README.md) | Alpha 4.6 retains V4.1 materials B and selects Small Colossus V7 ground-v3 with deeper burial; gameplay/uniqueness pending |
| [Obelisk](obelisk/README.md) | Alpha 4.6 retains V4.2; archaeology, collectibles and maps pending |
| [Titan Skull](titan-skull/README.md) | Skull 2's Alpha 4.9 appearance and shallow terrain footprint visually accepted October 7; all raw Skull exports unchanged; encounters pending |
| [Ruined Tower](ruined-tower/README.md) | V7 ground-v3 collapsed-side-bay candidate with 220 visible layers selected in Alpha 4.6 |
| [World Tree](world-tree/README.md) | Alpha 4.9 V4.3 strands and terrain integration visually accepted October 7; 1,883 tapered low-root cells along 50 paths and bounded cave contacts |

Alpha 4.9 changes two natural profiles and the later Tree root additions; eight
other raw/natural template pairs remain exact Alpha 4.8 matches.
Alpha 4.7's surface anchors, site tolerances and density remain unchanged.

The [subsequent user acceptance](../docs/project/reviews/alpha4-9-user-acceptance-20261007.json)
records eight new screenshots and applies only to Skull 2 and World Tree in the
released Alpha 4.9 build. Models, runtime and historical test findings remain unchanged.

See the [October 6 embedding revisions](../docs/project/EMBEDDING_20261006.md) and
[current runtime evidence](../docs/testing/ALPHA_4_9_TEST_REPORT.md). Earlier models
and the historical Alpha 4 design decisions below remain preserved.

## In-game demos

- [Colossus V3 shader demo](colossus/demo/README.md): three actual Minecraft
  screenshots in normal terrain, separate from generated Blender previews.

## V4 studies from in-game inspection

The V3 models were selected in Alpha 3; Alpha 4 selects the latest successors.
The following documents record the
agreed visual findings and revision direction. Colossus V4 now has two offline
[export variants](colossus/docs/COLOSSUS_V4_EXPORTS.md), with B / open machine frame
selected by the user. [Obelisk V4](obelisk/docs/OBELISK_V4_EXPORTS.md) and the four
[Titan Skull V4 variants](titan-skull/docs/TITAN_SKULL_V4_EXPORTS.md) are exported
and checked offline. See [Alpha 4 integration](../docs/technical/ALPHA_4_INTEGRATION.md)
for the original Alpha 4 selection and [runtime evidence](../docs/testing/ALPHA_4_TEST_REPORT.md).

Latest corrections: [Colossus V4.1](colossus/docs/COLOSSUS_V4_1.md) replaces the
raised wrist with a palm-up right hand and curled fingers;
[Obelisk V4.1](obelisk/docs/OBELISK_V4_1.md) replaces contrasting patches with
consistent sandstone facets and larger actual cracks. Previous exports are retained.

The user has **visually accepted Colossus V4.1, Obelisk V4.2 and all four Titan
Skull V4 terrain variants**. Their latest exports are selected in Alpha 4;
client visual acceptance of the integrated build remains separate.

**Next design priority:** review the [four new V1 assets](../docs/project/NEW_RELICS_V1.md)
before starting V5 architectural interiors. Ruined Tower, World Tree, the separate
archive-derived smaller Colossus and independent sword-bearing Titan Skull 2 now
have editable models and exports. Further skull/bone variants remain extensions.

**October 4 review:** Titan Skull 2 V1 is visually accepted for now. Small Colossus
needs a new direction beyond the original test design, World Tree needs a more
natural appearance, and Ruined Tower should be taller. See the
[recorded feedback](../docs/project/NEW_RELICS_V1.md#user-feedback--october-4-2026).
The resulting [V2 candidates and V1/V2 comparisons](../docs/project/RELICS_V2_REVIEW.md)
are available for the next visual review.
The user subsequently found Small Colossus V2 too similar to the large machine
and selected the [V3 slender sentinel](colossus/docs/SMALL_COLOSSUS_V3.md) direction.
V3 was then rejected as too skeletal. The latest
[Small Colossus V4](colossus/docs/SMALL_COLOSSUS_V4.md) follows the user's new
Vigilant-Class reel and its massive dormant plated specimen. V4 is a visual
candidate; Tree V2 and Tower V2 still await feedback.

The user requested [reference, size, proportion and damage studies for all four](../docs/project/NEXT_FOUR_RELIC_DESIGN_STUDY.md)
before any Blender work. Those working briefs are available; the user subsequently
requested all four V1s. Skull 2's opening scene is verified and includes an embedded sword.

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
still open. Alpha 4 has provisional repeatable candidate rates and does not yet
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

Alpha 4 explicitly pins seven designs/ten templates using `tools/relic_catalog.py`
and `tools/integrate_relics.py`; see [current integration](../docs/technical/ALPHA_4_INTEGRATION.md).
Organizing an asset here alone does not select it or implement proposed gameplay.
