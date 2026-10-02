# Obelisk gameplay: archaeology and expedition maps

Recorded: October 1, 2026. Updated: October 2, 2026. This is an approved gameplay direction, not an
implemented system. Exact layouts, loot tables, and generation rates remain open.

## Role in exploration

The Obelisk rewards careful investigation and leads to an expedition to the
unique large Colossus. Its rewards emphasize discovery rather than combat power.

- The **large Colossus is intended to occur once per game world**, shared by all
  players. Smaller Colossi may repeat, with their own still-undecided loot/rates.
- The Obelisk provides an additional way to find the large Colossus through an expedition
  map. It should be **clearly rarer than the skull/bone family**, but more
  accessible than the unique landmark, without filling the world with monuments.
- A player may still discover and explore a Colossus without finding an Obelisk
  first. The map is a discovery aid, not a progression lock.
- Relative rarity is an agreed goal; no numeric spacing, separation, probability,
  or biome-filter changes have been selected or applied. Alpha 3 does not yet
  enforce the newly approved large-Colossus uniqueness rule.

## Archaeological site

Keep the Obelisk's solid monument intact. Gameplay takes place at its foot and
among traces of earlier visitors, rather than in a newly hollowed tower.

The intended exploration flow is:

1. Discover a small, partly buried archaeological site beside the foundation.
2. Recognize promising locations through exposed masonry and earlier excavation
   traces, rather than blind digging.
3. Investigate suspicious sand and gravel with a brush.
4. Recover ordinary finds, an exclusive archaeological collectible, and an
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
- The working lore connects the relics through the Titan conflict: a Colossus
  was sent to kill Titans, and Obelisks served as wayfinders or marked destroyed
  Titans. The map can be evidence of later visitors investigating these traces;
  builders, sender, and the exact role of the Obelisks remain open.
- Technical target selection must be validated: the destination must correspond
  to a valid natural Colossus placement, not an unverified candidate or an extra
  Colossus spawned solely to satisfy the map.
- Resolve the single destination consistently with natural generation and saved
  world state, even if its chunks have not yet been explored. Searching from
  another Obelisk or receiving another map must not create an additional site.

Handling unavailable or excessively distant targets, repeated destinations, and
search cost remains open. A missing/disabled unique target must have an explicit
fallback policy, not silently spawn a substitute. The desired outcome is a reliable, useful map, not an
empty map or a pointer to a rejected structure site.

### Exclusive archaeological collectible

- Provide a recognizable, original find that can be displayed at the player's
  base; a renamed ordinary item alone is not enough.
- Decorated sherds, a small stele, or a displayable stone plate are candidate
  forms. The final item, model, texture, and display mechanics are not selected.
- The reward is a souvenir, not a combat or production upgrade.

A complete investigation should reliably yield the special rewards. Randomness
may vary ordinary loot and collectible variants, but should not leave a thorough
excavation with only low-value common items. Exact reward placement and generation
rules still need to be specified and tested.

## Lore review follow-up

Decide internally whether the ancient Obelisks primarily guided travel or marked
destroyed Titans, then derive consistent spatial/environmental clues. Those roles
are still alternatives; the review does not settle their builders or purpose.
Players may remain uncertain after the internal design is fixed. Later explorers'
maps are a plausible link to the machine without making those maps original
Obelisk machinery or imposing a mandatory progression order.

Before final loot distribution, resolve whether late multiplayer visitors can
obtain maps and collectibles after shared archaeological finds have been brushed.
The large site's per-player core vault does not replenish the archaeology or arm
chest. No per-player archaeology or replenishment system is approved. Measure
actual search effort with/without maps, not just candidate spacing; repeated
destinations now reflect intentional uniqueness. See the
[shared review](../../../docs/project/LORE_GAMEPLAY_REVIEW.md).

## Open decisions

- Concrete rarity values and expected effort to find each relic.
- Map generation, valid-target verification, distance bounds, and fallback rules.
- Consistent single-site resolution across maps, natural generation, and save/load.
- Internally chosen Obelisk purpose and corresponding spatial clues.
- The collectible's final form and presentation.
- Archaeology layout, loot distribution, and any recovered map container.
- Multiplayer sharing or individual rewards, particularly for archaeological
  finds and maps; no per-player loot system is assumed.

Related decisions: [Colossus items and trials](../../colossus/gameplay/ITEMS.md).
Shared atmosphere and exploration guidance remain in the
[lore bible](../../../docs/project/LORE-BIBLE.md), including the family-level
discovery hierarchy.
