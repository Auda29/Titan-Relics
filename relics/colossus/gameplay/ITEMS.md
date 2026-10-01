# Colossus gameplay items: Machine Core and Salvage Magnet

## Status and scope

Recorded: October 1, 2026.

This document records the agreed gameplay direction for two custom Colossus loot
rewards and their dedicated trial key. None of these items or the encounter is
implemented yet. Numeric values below are initial tuning targets, not final
balance commitments. Repair and charging recipes remain open.

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

The Colossus should be **very rare**, reflecting the value of its special items.
The frequency order is skull/bone variants first, clearly rarer Obelisks second,
and Colossi as the rarest of these three families. In the
[working lore](../../../docs/project/LORE-BIBLE.md), a Colossus was sent to the
planet to kill the Titans; the sender and wider history remain open.
The [Obelisk's archaeology rewards](../../obelisk/gameplay/README.md) include an
expedition map to a Colossus so players can seek one deliberately. Maps aid
discovery; they do not bypass the head trial or vault-key requirement.

Exact generation rates remain open. This is a design goal, not a change to the
current alpha's worldgen settings.

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

### Dedicated key and vault behavior

- The Colossus Key is a **custom item**, not a renamed vanilla Trial Key.
- Vanilla Trial Keys and Ominous Trial Keys must not unlock the Colossus vault.
- The key is consumed on a successful opening, following the normal vault model.
- Preserve individual-player vault eligibility; one visitor must not empty the
  special reward for everyone else. Repeated trials must not let a player reopen
  an already claimed vault merely by acquiring another key.
- A key may be used at another Colossus. It is **not bound to the individual
  spawner, participant, or structure location** in the initial design.
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

Functional custom items require additional mod code; the current data-only mod
and Blender conversion pipeline do not implement these behaviors. Trial spawner
and vault configuration use block-entity data and custom loot tables; the current
schematic converter rejects block entities, so the build pipeline will need to
preserve or inject those data in a separate supported step. This document records
design decisions only and does not change the playable build.
