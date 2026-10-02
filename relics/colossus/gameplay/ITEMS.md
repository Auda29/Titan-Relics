# Colossus gameplay items: Machine Core and Salvage Magnet

## Status and scope

Recorded: October 1, 2026. Updated: October 2, 2026.

This document records the agreed gameplay direction for two custom Colossus loot
rewards and their dedicated trial key. None of these items or the encounter is
implemented yet. Numeric values below are initial tuning targets, not final
balance commitments. Repair and charging recipes remain open.

**Asset status:** [material study B](../docs/COLOSSUS_MATERIAL_STUDY_B.md) is the
selected, visually accepted material version of V4.1. It is exported and checked
offline, **not integrated into Alpha 3 or tested in Minecraft**. Alpha 3 still
packages V3. Golem history, core utility/final costs, multiplayer reward policy,
and unique-large-site generation remain open; this material choice implements
none of them.

The items should feel like useful machinery salvaged from an ancient mechanical
relic, rather than generic stronger equipment. Their working names are:

| English working name | German working name | Role |
| --- | --- | --- |
| Machine Core | Maschinenkern | Rechargeable, long-lasting furnace fuel |
| Salvage Magnet | Bergungsmagnet | Passive offhand item collection |
| Colossus Key | Colossus-Schlüssel | Dedicated key for the Colossus vault |

Armor trim design is explicitly deferred and is not part of this document.
The Machine Core is a guaranteed vault reward in the Colossus's head. One
functional Salvage Magnet is guaranteed in a copper chest inside the detached
arm; the exact chest position and access route remain open.

### Loot containers and deferred interior design

- **Copper chests** are the selected containers for the Salvage Magnet and
  ordinary salvage loot, rather than ordinary wooden chests.
- The Machine Core instead comes from a **trial vault in the head**. This
  supersedes the earlier decision to place both special rewards in copper chests.
- Copper chests should read as old technical storage containers and visually
  match the Colossus's copper machinery and armor.
- Chest count, exact positions, oxidation stages, and remaining loot distribution
  remain open.
- The detailed interior layout, rooms, exploration routes, and visual treatment
  will be designed later. The head is the trial/vault area; the detached arm is
  the magnet's exploration-based salvage area.

## Head trial, vault, and Colossus Key

### Rarity and discovery

The **large Colossus is unique: one natural site per game world/save**, shared by
all players, rather than a repeatable structure with very wide spacing. Planned
**smaller Colossi may occur multiple times**; their rarity, encounters, and loot
are separate open decisions. These item/trial decisions apply to the large site,
not automatically to every smaller Colossus.

Titan remains retain a combined family budget and are most common; Obelisks are
clearly rarer. The large landmark has a single destination, not a density target.
In the
[working lore](../../../docs/project/LORE-BIBLE.md), a Colossus was sent to the
planet to kill the Titans; the sender and wider history remain open.
The [Obelisk's archaeology rewards](../../obelisk/gameplay/README.md) include an
expedition map to the unique large Colossus so players can seek it deliberately. Maps aid
discovery; they do not bypass the head trial or vault-key requirement.

Repeatable-family rates and the unique site's selection rules remain open. Alpha
3 does not enforce uniqueness; this documentation changes no worldgen settings.

### Agreed encounter and reward flow

1. A **trial spawner in the Colossus's head** spawns an **iron golem**.
2. The player fights the golem and completes the trial.
3. The spawner's custom reward loot table guarantees **one Colossus Key per
   eligible trial participant**, rather than a random chance of a vanilla key.
4. A nearby vault accepts the Colossus Key and guarantees **one Machine Core per
   eligible opening** through its own loot table.

The target flow is: **defeat the golem -> receive Colossus Key -> unlock vault ->
salvage Machine Core**.

The iron golem does not need custom aggression logic for the initial design:
the player can initiate combat and the golem retaliates. Exact enemy counts,
multiplayer scaling, and spawn conditions remain to be configured and tested.

### Review follow-up: the golem's historical role

The trial needs a visible connection to the inactive wreck. Residual security,
maintenance machinery, and a later installation are candidate explanations;
none is selected. Choose the role internally and derive the room, activation
cues, key, and reward presentation from it during later interior design.
A player-initiated, retaliating golem does not actively guard access; do not
describe it as an active guardian without matching behavior. The current trial
flow remains approved; this review does not require custom aggression or activate
the entire machine. See the [lore/gameplay review](../../../docs/project/LORE_GAMEPLAY_REVIEW.md).

### Dedicated key and vault behavior

- The Colossus Key is a **custom item**, not a renamed vanilla Trial Key.
- Vanilla Trial Keys and Ominous Trial Keys must not unlock the Colossus vault.
- The key is consumed on a successful opening, following the normal vault model.
- Preserve individual-player vault eligibility; one visitor must not empty the
  special reward for everyone else. Repeated trials must not let a player reopen
  an already claimed vault merely by acquiring another key.
- The unique landmark's vault is intended to serve later visitors to the same
  site. Verify eligibility persistence, target-version remembered-player limits,
  and larger server populations; do not assume unlimited per-player access from
  the vanilla block alone.
- The key remains **not bound to the individual spawner, participant, or structure
  location**. If another compatible vault is deliberately introduced later, keys
  may be used there. The unique-site rule means there is no second natural large
  Colossus to seek; smaller-Colossus vaults and shared key support are not approved.
- A vault validates the key, not proof that its adjacent golem was killed by
  the opening player. Strict local completion enforcement is not planned.
- Normal and ominous configurations must be considered together so an ominous
  effect cannot accidentally substitute incompatible keys or vanilla loot. The
  precise ominous encounter behavior remains open.

The room's appearance, exact block positions, and key artwork are deferred.

## Machine Core

### Agreed gameplay

- The player salvages an old machine energy-storage component from the Colossus.
- The core provides a large but **finite** amount of furnace fuel. Infinite fuel
  is not the selected design.
- It works in furnaces, blast furnaces, and smokers.
- It does not increase processing speed; each appliance retains its normal speed.
- A depleted core remains as an item and can be recharged. The rare find is not
  destroyed through ordinary use.
- It does not power unrelated machines or require a separate energy mod.

### Initial tuning target

A full charge supplies **256 completed smelting or cooking operations**, counting
operations rather than input-stack size. For comparison, one coal normally fuels
eight operations and a lava bucket fuels 100.

The core should be convenient and may offer a modest fuel-efficiency benefit,
but recharging must require meaningful resources. It must not turn a trivial
amount of redstone into effectively free industrial fuel.

### Review follow-up: everyday benefit before final balance

At the initial target, 256 operations equal the nominal fuel output of **32 coal**.
The distinctive value is reuse, stored remaining charge, and no idle drain.
Reaching the unique site and head, completing the trial, possible restoration,
and recurring charging could otherwise cost more effort than the reward saves.

Define the practical everyday problem solved by the core first, then tune capacity
and restoration/recharge costs together through survival and automation tests.
The 256-operation target remains provisional; no increase, recipe, speed bonus,
or free-fuel mechanism is approved by the review.

### Charge consumption

Charge is consumed by actual processing, not by elapsed burn time. An idle
appliance must not waste the remaining charge.

Removing or reinserting the core, transferring it through hoppers, saving and
loading the world, or unloading a chunk must preserve its charge. Normal hopper
use should be supported without resetting or duplicating fuel capacity.

The exact behavior of interrupted operations, appliance progress, and automatic
handling of depleted cores must be specified during implementation.

### Restoration and recharging

Separate the initial restoration of a damaged salvage item from later recharges:

- **Initial restoration:** May be expensive. A diamond, iron, and redstone were
  suggested as possible ingredients, but no recipe has been approved.
- **Repeat recharging:** Requires fuel, such as coal or charcoal, plus technical
  materials, such as redstone and some iron. Exact ingredients and amounts remain
  open.
- Do not require diamonds for every recharge; recurring costs should not make
  the reward too expensive to use in ordinary play.

The intended loop is: **salvage -> restore -> use -> deplete -> recharge**.

## Salvage Magnet

### Acquisition: exploration inside the detached arm

- Place a copper chest in a former maintenance area inside the **detached arm**,
  near the hand or its actuator machinery. Exact coordinates and presentation
  are deferred to the later interior design.
- An identifiable rupture provides an intended entrance. The chest should not
  be directly accessible from outside; finding it requires a short exploration
  of the arm.
- The chest guarantees **one functional Salvage Magnet**, accompanied by some
  ordinary technical salvage. Initial durability and additional loot remain to
  be tuned; the magnet must be usable immediately without an initial repair.
- No key, second trial, or dedicated guarded combat encounter is required.
  The Colossus Key remains reserved for the Machine Core vault. Ordinary mob
  spawning is not ruled out by this design.
- The intended route should be discoverable without blindly mining the outer
  shell. Players may still build or mine their own access; do not prohibit normal
  Minecraft interaction to enforce the route.

The suggested exploration order is **arm -> magnet -> head trial -> Machine
Core**. This is an invitation, not a progression gate: the magnet is not required
to reach or complete the head trial.

A normal copper chest has shared, finite contents, unlike a per-player vault.
Whether multiplayer needs an individual magnet reward remains an open decision;
no per-player chest system is approved or implemented.
With only one large Colossus per world, later visitors cannot look for another
large arm with fresh loot. Resolve late-arrival/group access before final loot
distribution; replenishment, individual rewards, or magnets in smaller Colossi
are not assumed. The per-player core vault does not solve this chest asymmetry.

### Agreed gameplay

- The magnet is **passive while equipped in the offhand** (the shield slot).
- It is inactive in the main hand or normal inventory.
- No right-click activation, charging gesture, or manual magnetic pulse is
  required. This replaces the earlier active-use proposal.
- Equipping it deliberately competes with carrying a shield, a totem, or another
  offhand item.
- It attracts dropped item entities toward the player. Items move visibly and
  are collected through normal pickup behavior, rather than being extracted
  directly from inventories.
- It can collect all dropped item types, not only metal.

### Initial tuning targets

| Property | Starting value |
| --- | --- |
| Attraction radius | 8 blocks |
| Durability budget | Approximately 1,000 successfully collected item stacks |
| Durability cost | One point per collected item stack, not per individual item |

These values need survival testing. The exact accounting for partial pickups,
merging item entities, and repeated attraction attempts is still to be defined.
Items that are merely attracted but never picked up must not consume durability.

### Boundaries

- Do not pull items through closed walls.
- Do not take items from chests or other inventories.
- Do not mine blocks or pull players, mobs, or experience orbs.
- Respect normal pickup delays for freshly dropped items.
- Do not repeatedly attract items that the player's inventory cannot accept.
- The magnet is a collection aid, not an automatic mining tool.

### Wear and repair

- Wear occurs through successful collection, not simply through time spent
  equipped. Walking without collecting anything does not cost durability.
- At zero durability the magnet becomes **broken and inactive**, rather than
  disappearing. The player retains the rare salvage item.
- Repair restores the existing magnet using **iron and redstone**. Exact amounts
  and the repair interface are not decided; a dedicated recipe is one option.
- For the first version, enchantments must not bypass the intended wear and
  repair loop.
- No separate energy charge is planned for the magnet; durability supplies its
  maintenance cost.

The intended loop is: **equip in offhand -> collect nearby drops -> wear out ->
repair**.

## Review follow-up: salvage economy of the whole landmark

**Historical study A — superseded by B:** the user authorized a separate material
study with the entire accepted form preserved. The
[candidate and exact inventory](../docs/COLOSSUS_MATERIAL_STUDY.md)
retain 197 copper blocks and 10 raw iron blocks at three connected salvage sites,
with zero changed occupied positions. This comparison is not selected; its
earlier pending-approval status does not apply to B. Neither study defines final
loot rules or changes the packaged build by being exported.

**Current approved asset choice — study B:** the user requested more copper, explicitly below 50,000
copper blocks and 256 raw iron **items**. [Study B](../docs/COLOSSUS_MATERIAL_STUDY_B.md)
retains 25,423 copper blocks in removable armour regions and ten raw iron blocks
(90 items). Complete metal removal must preserve the head/body connection and
not split surviving components; the candidate passes these geometry checks.
Study A above is retained as a historical comparison. The user visually accepted
B, including its post-salvage appearance, on October 2, 2026. It is the selected
material version with the stated inventory. Build integration and Minecraft
validation remain pending; offline post-salvage previews are simulations only.

The V3 export contains **141,523 copper-based blocks and 5,609 raw iron blocks**.
These historical counts are verified for V3, not asserted for material study B.
Estimate recoverable resources from the selected export and compare them with
the core and magnet's useful value. Bulk mining could overshadow the special
rewards and dismantle the only large landmark for everyone else.

Selected study B implements the material response: removable copper armour regions
and economically less significant bulk fields, preserving intact V4.1 geometry.
Its palette and inventory are approved; actual Minecraft appearance, recoverable
resource value, and balance against the core/magnet still need validation. Normal
mining is not prohibited and no block-protection mechanism is approved. Coordinate with
[Colossus design goals](../docs/COLOSSUS_V4.md) and the
[shared review](../../../docs/project/LORE_GAMEPLAY_REVIEW.md).

## Open decisions and acceptance checks

### Decisions still needed

1. Final item names, models, textures, and feedback effects.
2. Exact arm chest placement and access route, ordinary-loot contents, initial
   core condition, and the functional magnet's starting durability.
3. Exact core restoration and recharge recipes, and magnet repair costs.
4. Charge and durability display, such as tooltips and a visible status bar.
5. Core progress accounting, fuel-slot behavior, and hopper handling.
6. Magnet pull speed, line-of-sight behavior, and pickup accounting.
7. Multiplayer behavior and compatibility with relevant protection systems.
8. Golem counts, multiplayer scaling, ominous behavior, and the head trial's
   detailed layout and presentation.
9. In-game validation and survival salvage balance of selected material study B
   relative to special rewards; its palette/inventory choice is already approved.
10. Historical function of the golem and visible links to the Titan conflict.
11. The core's everyday use case and combined acquisition/restoration/recharge cost.
12. Later-visitor reward policy for the unique site's shared magnet and ordinary loot.

### Acceptance checks

- Both items provide useful convenience without increasing combat strength.
- The arm's intended access route is identifiable and leads to a copper chest
  with one immediately usable magnet, without requiring a key or scripted fight.
- The core processes the intended number of operations without idle drain,
  speed bonuses, or charge-reset exploits.
- Core state survives transfer, item drops, save/load, and chunk unloads.
- The magnet activates only in the offhand and respects its range and walls.
- Full inventories and failed pickups do not create repeated wear or noisy
  attraction loops.
- Depleted or broken items remain recoverable and can be restored without
  duplication or loss.
- Collection and furnace processing remain practical in multiplayer and under
  normal automation loads.
- In Minecraft 26.2, verify golem spawning, trial completion tracking, guaranteed
  key rewards, key consumption, and the guaranteed Machine Core vault reward.
- Reject vanilla keys and preserve per-player vault eligibility across save/load.
- Check both normal and ominous paths for incompatible rewards or repeat-claim
  exploits.
- Test late arrivals and a large player population at the same vault, including
  save/load and eligibility retention; previously claimed rewards must not reset.
- Resolve and test the distinct shared-chest reward policy before finalizing loot.
- Confirm the landmark's resource economy does not unintentionally make the
  planned core/magnet rewards irrelevant; document any deliberate salvage tradeoff.

Functional custom items require additional mod code; the current data-only mod
and Blender conversion pipeline do not implement these behaviors. Trial spawner
and vault configuration use block-entity data and custom loot tables; the current
schematic converter rejects block entities, so the build pipeline will need to
preserve or inject those data in a separate supported step. This document records
design decisions only and does not change the playable build.
