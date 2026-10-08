# Relic design and gameplay index

Each relic has its own folder. Keep shared workflows in [docs/](../docs/README.md)
and implementation code in `src/`, `tools/`, and `tests/`.

| Relic | Current status |
| --- | --- |
| [Colossus](colossus/README.md) | Alpha 4.6 retains V4.1 materials B and selects Small Colossus V7 ground-v3 with deeper burial; gameplay/uniqueness pending |
| [Obelisk](obelisk/README.md) | Alpha 4.6 retains V4.2; archaeology, collectibles and maps pending |
| [Titan Skull](titan-skull/README.md) | Existing interiors/access accepted; natural mob spawning unchanged, no authored encounters; exports unchanged |
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

The updated relative tiers are **Obelisks + both skull designs -> rarer Tower +
small Colossi + World Tree -> the unique large Colossus**. All relics must remain
genuinely rare and widely separated, with exact rates/distances deferred to visual
review. This supersedes the earlier Obelisks-clearly-rarer-than-skulls rule. The large
Colossus should occur **once per game world/save**, shared by all players. Planned
**smaller Colossi may occur multiple times**, with separate rarity/loot decisions
still open. Alpha 4 has provisional repeatable candidate rates and does not yet
enforce uniqueness; future skull/bone variants share a family-level density target.

Planned Obelisk maps initially lead to the same large site. Its future vault must preserve per-player
core eligibility for multiplayer; the arm magnet and Obelisk archaeology are
shared finite finds, while small sites may yield repair-required magnets. The
[lore/gameplay review](../docs/project/LORE_GAMEPLAY_REVIEW.md) tracks material
economy, historical trial integration, lasting core usefulness, visible lore
links, multiplayer distribution, and measured discovery effort as open tasks.

**Approved history, October 8:** all Colossi were crewed; the large machine was
central and the smaller ones its companions. The head golem was a cockpit defense
robot. Obelisks marked territories cleared of Titans, with skulls scattered across
the broad surroundings. The unfinished tower organized the campaign. Titans
worshipped the World Tree and drew strength/size from it; the Colossi's builders
failed to destroy it. Thousands of years later no living Titans remain, and mobs/
players reuse the relics. Titan nature and the campaign's motive are lost to time.
This supersedes the old Obelisk/golem-role alternatives and independent tower/tree
history. See the [lore bible](../docs/project/LORE-BIBLE.md).

Document gameplay, interiors, reward placement and remaining lore for all seven
designs, then reconcile documentation before implementing on **26.2/Fabric first**.
Crew sizes are now fixed: five in the large Colossus, two in each smaller one,
approximately player-sized and possibly a little larger. Keep the large cavity;
develop its cockpit/hatch, with player-found/built ascent. Small machines are
enterable but have severely decayed interiors and effectively lost cockpits from
weaker materials. The [smaller Colossus plan](colossus/gameplay/SMALL_COLOSSUS.md)
remains separate from the large site's core/trial; approved starting loot is a
10% per-site chance for one broken magnet requiring repair, with placement and
repair state handling still pending. The large defense golem should attack autonomously after automatic
trial-spawner activation, without a console; scoped detection/targeting needs testing.
Tower stair gaps require building. Ordinary mobs stay natural; the extra Enderman
method is delegated (a small one-time generation group is recommended). Shared
finite Ender loot is 5% eye, otherwise 4–6 pearls, with site-level roll assumptions
recorded in the Tower plan.
Both skulls retain their accepted existing interiors and current accessibility
unchanged for now; no additional access/terrain-clearing review is selected.
Their mobs spawn naturally with no extra spawners, placed enemies or spawning changes;
neither skull gets loot chests. The World Tree should have more pigs/chickens/sheep/
cows through modest natural spawning, no animal spawners or farm-like refill.
Ordinary hostiles stay natural, with dark spawning reduced through lighting; the
effect is reward enough, without Tree loot. Approved effect starting values:
Regeneration I within about 24 blocks
of the trunk, refreshed during the stay and lasting five minutes after leaving.
Exact spawn/aura geometry/refresh rules, regional placement and reward positions
remain open. None of these systems is implemented.

The selected World Tree light palette is glow berries, glow lichen, firefly bushes
and sparse shroomlights. Lighting stays at the trunk/base and roots, rising
irregularly at most 15 blocks up the trunk, with broad natural ground-level spread
and no upper-branch/crown lights. Exact spread/positions/quantities remain open;
amethyst clusters are optional. The approved shaped core recharge uses
the depleted core in the middle, a coal block on each side and one amethyst shard
above, yielding one fully charged core (provisional 256 operations). Earlier
24-coal and three-coal-block proposals are superseded; recipe code/balance testing
remain pending.

**Latest reward decisions:** Obelisk archaeology is shared finite loot, with an
original cosmetic armor-trim template and copyable/shareable expedition map; trim
motif follows geometric Obelisk forms, with exact artwork open. Duplication uses
one template + seven diamonds + one copper block -> two templates. The Vault core starts fully charged and usable,
with no initial restoration. Magnet full repair uses a crafting table and four
iron ingots plus one amethyst shard instead of two redstone, repairing the existing
magnet fully without creating a second item.

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
