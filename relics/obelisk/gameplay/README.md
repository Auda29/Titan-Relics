# Obelisk gameplay: archaeology and expedition maps

Recorded: October 1, 2026. Updated: October 8, 2026. This is an approved gameplay direction, not an
implemented system. Exact layouts, loot tables, and generation rates remain open.

## Role in exploration

The Obelisk rewards careful investigation and leads to an expedition to the
unique large Colossus. Its rewards emphasize discovery rather than combat power.

- The **large Colossus is intended to occur once per game world**, shared by all
  players. Smaller Colossi may repeat, with an approved starting 10% per-site chance
  for a broken magnet; their site frequency and exact loot placement remain open.
- The Obelisk provides an additional way to find the large Colossus through an expedition
  map. Obelisks and both skull designs now share the **relatively most frequent
  tier**, ahead of the rarer Tower/small-Colossus/Tree tier and the unique landmark.
  **Every relic remains genuinely rare**, with wide gaps between discoveries.
  This supersedes the earlier skulls-first/Obelisks-clearly-rarer ordering.
- A player may still discover and explore a Colossus without finding an Obelisk
  first. The map is a discovery aid, not a progression lock.
- Relative rarity is an agreed goal; no numeric spacing, separation, probability,
  or biome-filter changes have been selected or applied by this planning decision. Alpha 4.9 does not yet
  enforce the newly approved large-Colossus uniqueness rule.

## Archaeological site

### Approved original role and later reuse

Obelisks marked **territories cleared of Titans by the Colossi**. Skull relics
therefore occur across their broad surroundings, not necessarily beside each
foundation. This supersedes the old wayfinder-versus-single-kill-site alternatives.
The campaign happened thousands of years ago; no living Titans remain. Today's
mobs, players and later explorers reuse or investigate the monuments.

Define regional distances, counts, biome compatibility and valid site selection
during placement planning; no new adjacency/spawn rule is implemented here. A
cleared territory does not mean the present-day site must be free of ordinary mobs.

**Latest regional direction:** the user proposes concentrating the combined skull
chance around Obelisks: **30% of shared relic opportunities in a broad region**,
with much lower chance outside. The assistant starting proposal is a **6,000-block
radius**, **5% combined skull chance outside** and retention of the proposed
2,000-block cross-relic separation floor. These exact radius/outside-rate values
still await visual review. **Natural Obelisk regions must neither overlap nor
touch**. The user selected **at least 15,000 blocks between Obelisk centers**,
leaving **3,000 blocks between edges** with the proposed equal 6,000-block radius.
This stronger pair-specific rule replaces the general 2,000-block floor for
Obelisk–Obelisk pairs; if radius changes, centers must still be farther apart than
the sum of the radii. Actual Obelisk frequency must be reviewed alongside this
stronger exclusion. Do not add extra opportunities or
require a skull beside every marker. Use valid natural Obelisks
as anchors and deterministic planning, not only already-explored monuments.

Keep the Obelisk's solid monument intact. Gameplay takes place at its foot and
among traces of earlier visitors, rather than in a newly hollowed tower.

The intended exploration flow is:

1. Discover a small, partly buried archaeological site beside the foundation.
2. Recognize promising locations through exposed masonry and earlier excavation
   traces, rather than blind digging.
3. Investigate suspicious sand and gravel with a brush.
4. Recover ordinary finds, an exclusive armor-trim smithing template, and an
   expedition map leading to a Colossus.

The challenge is attentive exploration and careful excavation. No mandatory
combat trial or large dungeon beneath every Obelisk is planned. The exact access
route, site size, and reward-container arrangement will be designed later.

## Special rewards

### Expedition map to the unique large Colossus

- A recovered map or earlier expedition record points to a naturally placed
  large Colossus, making the unique structure easier to discover.
- The map is static navigation, not teleportation or a permanent scanner for all
  relics. It does not make the Colossus's encounters or reward requirements easier.
- Initially all such maps lead to the **same unique large site**. Repeated
  destinations are intentional; maps are not a promise of fresh shared loot or
  another large Colossus. Maps to smaller Colossi are not currently selected.
- Players may copy and share recovered maps using normal map-copying behavior;
  copies keep the same destination and do not replenish the site's rewards.
- The working lore connects the relics through the Titan conflict: a Colossus
  and its smaller crewed companions killed Titans; Obelisks marked cleared
  territories. Maps represent later visitors' investigation, not the monument's
  original military function. The makers' identities remain unknown and the
  campaign's motive is lost to time; the Obelisk's role is now settled.
- Technical target selection must be validated: the destination must correspond
  to a valid natural Colossus placement, not an unverified candidate or an extra
  Colossus spawned solely to satisfy the map.
- Resolve the single destination consistently with natural generation and saved
  world state, even if its chunks have not yet been explored. Searching from
  another Obelisk or receiving another map must not create an additional site.

**Approved map exceptions:** keep pointing to the valid
unique natural site regardless of distance; for temporarily unresolved targets,
retain an explicitly unconfirmed map and resolve it later without publishing
unverified coordinates; if the destination is genuinely unavailable, use **three
emeralds instead of the map** while retaining the trim reward. Do not misclassify
an existing valid site as unavailable merely because future generation is disabled
or players mined it. This needs custom pending-map/claim/retry handling; copied
pending maps must not create extra compensation claims. Technical search cost,
retry feedback and claim state remain integration details, not unresolved choices
between the three policies. Details and the shared regional rarity-budget proposal:
[implementation plan](../../../docs/project/UMSETZUNGSPLAN.md#distribution-proposal-and-approved-map-exceptions).

### Selected exclusive reward: armor trim

- The user selected a **special armor trim**, acquired as an original smithing
  template through the Obelisk's exterior archaeology. This replaces the earlier
  sherd, miniature-stele and displayable-stone-plate proposals; no separate
  display-only collectible is required.
- The trim is **cosmetic**, not an armor-stat, combat or production upgrade.
  Its approved motif follows the **angular, geometric forms of the Obelisk**.
  Exact pixel artwork, name and icon remain open. A renamed vanilla template
  alone is not the intended exclusive design.
- **Approved duplication:** follow the vanilla template-copying principle:
  **one existing template + seven diamonds + one copper block -> two templates**.
  Copper replaces the suggested sandstone as a visual/material connection to the
  Colossi; this does not establish who originally made the template. No free
  copies or new non-vanilla smithing system are selected. Exact crafting layout
  and smithing application data still need specification/target-version testing.

A complete investigation should reliably yield the special rewards. Randomness
may vary ordinary loot, but should not leave a thorough
excavation with only low-value common items. Exact reward placement and generation
rules still need to be specified and tested.

### Ordinary finds: delegated modest starting pool

The user requests ordinary **vanilla pottery sherds and modest common loot**, not
another special item or rich chest-equivalent payout, and delegates choosing the
pool. The exclusive trim/map remain the special rewards.

**Assistant-defined starting specification:** reserve **six ordinary brushable
finds per fresh site**, in addition to the separate reliable trim-template and
map finds. Each ordinary block yields **one item**, with the following weights:

| Ordinary find | Weight / percentage |
| --- | --- |
| Vanilla pottery sherd, varied among suitable existing designs | 25 |
| Clay ball | 20 |
| Brick | 15 |
| Bone | 10 |
| String | 10 |
| Wheat seeds | 10 |
| Iron nugget | 5 |
| Copper ingot | 5 |

These quantities/weights are delegated assistant starting values, subject to
balance/archaeology tests, not numbers specified by the user. No diamonds, enchanted
books, extra exclusive collectibles or high-value treasure pool. Ordinary randomness
must not replace the reliable template/map, and all finds remain shared finite loot.
The builder supplies the exact exposed/partly buried locations; the mod assigns
the loot roles without requiring a large excavation or extra interior.

## Lore review follow-up

The original purpose was selected on October 8: **cleared-territory markers**.
Derive consistent spatial/environmental clues, including broadly surrounding
Titan remains. Exact regional distribution and what players can infer are still
open. Later explorers' maps link to the unique machine without making those maps
original Obelisk machinery or imposing a mandatory progression order.

**Approved multiplayer policy:** archaeology finds, including the trim template
and map, are **shared and finite**. Once brushed/claimed, they do not replenish for
later players; visitors may seek another Obelisk or share existing finds/maps.
Map copying is allowed; trim templates may be duplicated with the approved
seven-diamond/copper-block recipe, not through archaeological replenishment.
The guarantee of special finds applies to a complete investigation of a fresh
site, not independently to every visiting player. The large site's per-player core
vault does not replenish archaeology or the arm chest. No per-player archaeology
or refill system is selected. Measure
actual search effort with/without maps, not just candidate spacing; repeated
destinations now reflect intentional uniqueness. See the
[shared review](../../../docs/project/LORE_GAMEPLAY_REVIEW.md).

## Open decisions

- Concrete rarity values and expected effort to find each relic.
- Map generation/valid-target verification and implementing the approved distant/
  pending/unavailable policies, including retry/claim state; no distance cutoff.
- Consistent single-site resolution across maps, natural generation, and save/load.
- Spatial clues and regional skull-placement rules for the selected cleared-
  territory role; purpose is no longer undecided.
- Armor-trim name/icon/exact geometric artwork and smithing application data;
  duplication ingredients/output are selected, crafting layout/testing remains.
- Builder-supplied archaeology positions and distribution of the delegated
  ordinary pool versus reliable map/template finds.
- Exact finite reward quantities/placement and persistent depletion behavior;
  shared archaeology and copyable/shareable maps are selected, not individual loot.

Related decisions: [Colossus items and trials](../../colossus/gameplay/ITEMS.md).
Shared atmosphere and exploration guidance remain in the
[lore bible](../../../docs/project/LORE-BIBLE.md), including the family-level
discovery hierarchy.
