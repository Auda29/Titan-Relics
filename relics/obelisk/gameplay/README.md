# Obelisk gameplay: archaeology and expedition maps

Recorded: October 1, 2026. This is an approved gameplay direction, not an
implemented system. Exact layouts, loot tables, and generation rates remain open.

## Role in exploration

The Obelisk rewards careful investigation and leads to a rarer, more demanding
Colossus expedition. Its rewards emphasize discovery rather than combat power.

- The **Colossus should be very rare**, reflecting the value of its Machine Core
  and Salvage Magnet rewards.
- The Obelisk provides an additional way to find a Colossus through an expedition
  map. It should be **clearly rarer than the skull/bone family**, but more
  accessible than the Colossus, without filling the world with monuments.
- A player may still discover and explore a Colossus without finding an Obelisk
  first. The map is a discovery aid, not a progression lock.
- Relative rarity is an agreed goal; no numeric spacing, separation, probability,
  or biome-filter changes have been selected or applied.

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

### Expedition map to a Colossus

- A recovered map or earlier expedition record points to a naturally placed
  Colossus, making the valuable but very rare structure easier to discover.
- The map is static navigation, not teleportation or a permanent scanner for all
  relics. It does not make the Colossus's encounters or reward requirements easier.
- The map target may vary between sites; the initial target type is Colossus.
- The working lore connects the relics through the Titan conflict: a Colossus
  was sent to kill Titans, and Obelisks served as wayfinders or marked destroyed
  Titans. The map can be evidence of later visitors investigating these traces;
  builders, sender, and the exact role of the Obelisks remain open.
- Technical target selection must be validated: the destination must correspond
  to a valid natural Colossus placement, not an unverified candidate or an extra
  Colossus spawned solely to satisfy the map.

Handling unavailable or excessively distant targets, repeated destinations, and
search cost remains open. The desired outcome is a reliable, useful map, not an
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

## Open decisions

- Concrete rarity values and expected effort to find each relic.
- Map generation, valid-target verification, distance bounds, and fallback rules.
- The collectible's final form and presentation.
- Archaeology layout, loot distribution, and any recovered map container.
- Multiplayer sharing or individual rewards, particularly for archaeological
  finds and maps; no per-player loot system is assumed.

Related decisions: [Colossus items and trials](../../colossus/gameplay/ITEMS.md).
Shared atmosphere and exploration guidance remain in the
[lore bible](../../../docs/project/LORE-BIBLE.md), including the family-level
discovery hierarchy.
