# Colossus gameplay items: Machine Core and Salvage Magnet

## Status and scope

Recorded: October 1, 2026. Updated: October 8, 2026.

This document records the agreed gameplay direction for two custom Colossus loot
rewards and their dedicated trial key. Standalone item code/assets and opt-in
encounter adapters were developed in a separate worktree and integrated into `main`; see
[implementation evidence and remaining gates](../../../docs/testing/GAMEPLAY_IMPLEMENTATION_20261008.md).
They are not yet Minecraft-runtime accepted or integrated into natural sites.
Capacity/durability values below are initial tuning targets, not
final balance commitments. Charging and repair ingredients/output are selected;
the shaped layouts and technical starting state handling are specified, while
runtime integration and balance tests remain outstanding. See
[runtime contract](../../../docs/technical/GAMEPLAY_RUNTIME.md),
[builder markers](../../../docs/technical/GAMEPLAY_MARKERS.md) and
[future acceptance](../../../docs/testing/GAMEPLAY_ACCEPTANCE_PLAN.md).

**Asset status:** [material study B](../docs/COLOSSUS_MATERIAL_STUDY_B.md) is the
selected, visually accepted material version of V4.1 and is integrated in Alpha
4.9. Gameplay implementation targets **26.2 / Fabric first**, after all-relic
documentation and consistency review. Core utility/cost balance and implementation
of the approved multiplayer reward policy/unique-large-site generation remain open. The cockpit defense-robot
history is now approved below; natural encounter integration remains pending.

## Approved crewed-machine history — October 8, 2026

The large Colossus was the **central machine**, accompanied by smaller Colossi.
**All were crewed**, not autonomous. The head of the large machine was its cockpit,
and the iron golem represents its original **cockpit defense robot**. **Five crew
members operated the large Colossus; two operated each smaller companion.** They
were approximately player-sized, possibly a little larger. Exact height/species
and detailed station dimensions are not established; do not infer a giant crew
from the machine's overall scale.

Thousands of years later there are no living Titans. Current mobs and players
inhabit or reuse the wrecks; their presence does not identify them as original
crews. The Titans' exact nature and campaign motive are lost to time. The tower
was the unfinished organizing base; the Obelisks marked cleared territories; the
World Tree was the Titans' source of strength and size and survived the builders'
attempt to destroy it. See the [shared lore](../../../docs/project/LORE-BIBLE.md).

The approved interior scope is below. No new aggression logic, additional rewards,
or model changes are implemented by these documents. Plan original cockpit
features separately from any later reuse.

## Approved interior and access direction — October 8, 2026

- **Keep the existing large body cavity.** It already fits the desired impression;
  do not replace it with a multi-deck interior or invent extensive crew quarters.
- **Develop the head as the former cockpit for five operators**, including the
  historically selected defense robot and planned trial/vault. Exact stations,
  retained machinery, damage, room bounds and block positions remain open.
- Provide an **identifiable hatch as the intended cockpit entrance**. Its position,
  approach and dimensions remain to be selected. Players should not have to break
  through an arbitrary helmet wall to recognize the intended way in.
- **Players find their own climb or build their own ascent to the hatch.** A
  complete authored stairway from the ground/body to the head is not required or
  selected. This supersedes earlier suggestions of a ready-made internal ascent.
- The hatch is an invitation, not protection: ordinary building/mining remains
  allowed. No mandatory climbing tool, key for entry, or magnet prerequisite is added.
- Plan targeted clearing for the cockpit and hatch opening so existing terrain
  cannot fill the actual encounter/entry. Do not clear the entire model bounds or
  carve a guaranteed ground-to-head tunnel to manufacture an ascent.

The detached arm remains a separate short exploration to its magnet chest, with
no key or second trial. Its recognizable rupture and precise chest/access layout
still need planning; the self-built head ascent does not replace that arm route.

The items should feel like useful machinery salvaged from an ancient mechanical
relic, rather than generic stronger equipment. The user approved these **final
German and English display names** (now registered in standalone development code):

| English name | German name | Role |
| --- | --- | --- |
| Machine Core | Maschinenkern | Rechargeable, long-lasting furnace fuel |
| Salvage Magnet | Bergungsmagnet | Passive offhand item collection |
| Colossus Key | Colossus-Schlüssel | Dedicated key for the Colossus vault |

### Approved item presentation directions

- **Machine Core:** a compact, angular **copper housing with an inset visible
  violet energy element**, linking the Colossus palette and recharge amethyst.
  It should read as a salvaged machine component, not a fuel lump. Exact pixel
  sprites are generated in development; client rendering acceptance remains pending. This is an appearance
  direction, not a new recipe ingredient or permission to alter material study B.
- **Salvage Magnet:** a compact **rectangular copper collection device with an
  iron front and a violet indicator**, not a U-shaped horseshoe magnet or round
  module. Preserve passive offhand behavior; its original sprite now exists and state
  feedback is selected below. These visible materials do not change the approved repair recipe.
- **Colossus Key:** an **angular copper key with a geometric head, toothed shaft
  and small violet inset**. It remains a distinct custom item, consumed by the
  compatible vault; the visual direction does not change key eligibility/binding
  rules. Its original generated-item sprite/model exists; in-game review remains pending.
- **Core/magnet state display:** **exact remaining values in the tooltip plus
  changing inventory icons**, with distinguishable full, partly used and empty/
  broken states. **No inventory status bar** is selected. The core tooltip reports
  remaining processing operations; the magnet reports remaining durability. Name
   the empty/broken inactive condition explicitly. Technical thresholds are full
   at capacity, partial above zero and below capacity, empty/broken at zero; artwork
   exists in development, with in-game validation still pending. This does not authorize particles, emitted
  light, a new charge system for the magnet or a capacity increase.

The selected Monolith trim is specified in the Obelisk plan, not as Colossus loot.
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
- Detailed cockpit/hatch, trial/vault and detached-arm positions remain to be
  designed within the approved scope above. The body cavity is retained rather
  than rebuilt as a chain of rooms; reaching the head may require player building.

## Head trial, vault, and Colossus Key

### Rarity and discovery

The **large Colossus is unique: one natural site per game world/save**, shared by
all players, rather than a repeatable structure with very wide spacing. Planned
**smaller Colossi may occur multiple times**, but must still be rare; ordinary
salvage and their selected 10% magnet chance are documented separately. These
large-site item/trial decisions apply to the large site,
not automatically to every smaller Colossus.

Titan remains retain a combined family budget. **Obelisks and both skull designs
share the relatively most frequent tier**, followed by rarer **Tower, small Colossi
and Tree**, then the unique landmark. All relics must remain genuinely rare and
widely separated; the approved starting distribution is in the shared implementation
plan and is not yet implemented in worldgen.
The large landmark has a single destination, not a density target.
The user additionally requires that destination to be **far from the shared world/
initial player spawn**, with an approved **30,000-block horizontal minimum to the
site's center**. The delegated resolver prefers 30,000–60,000 blocks, then searches
outward 20,000-block annuli subject to the physical border, with no arbitrary
maximum-distance cutoff; see [distribution](../../../docs/technical/RELIC_DISTRIBUTION.md).
personal beds/respawn points do not relocate the unique site. The updated schematic
shows about 43,012 blocks only as an illustrative distance, not an approved bound.
The user subsequently accepted this journey's overall distance scale after the
travel-time comparison. Retain it as the planning baseline, without turning the
example into an exact placement or hard minimum for every save.
In the
[working lore](../../../docs/project/LORE-BIBLE.md), a Colossus was sent to the
planet to kill the Titans; the sender and wider history remain open.
The [Obelisk's archaeology rewards](../../obelisk/gameplay/README.md) include an
expedition map to the unique large Colossus so players can seek it deliberately. Maps aid
discovery; they do not bypass the head trial or vault-key requirement.

Repeatable-family starting rates and the large site's 30,000-block spawn floor
are approved; deterministic site selection is specified but unimplemented. Alpha
4.9 does not enforce uniqueness; this documentation changes no worldgen settings.

### Agreed encounter and reward flow

1. A **trial spawner in the Colossus's head** automatically detects eligible nearby
   players and spawns an **iron golem** when ready. No console/manual activation
   is required; detection range, sightline and cooldown need target-version testing.
2. The designated defense golem **attacks players on its own**; the player fights
   it and completes the trial. The player need not strike it first.
3. The spawner's custom reward loot table guarantees **one Colossus Key per
   eligible trial participant**, rather than a random chance of a vanilla key.
4. A nearby vault accepts the Colossus Key and guarantees **one fully charged,
   immediately usable Machine Core per eligible opening** through its own loot table.

The target flow is: **defeat the golem -> receive Colossus Key -> unlock vault ->
salvage Machine Core**.

**Approved normal encounter size and multiplayer rule:** **one defense golem per
trial**, not a group or successive waves. Its health and damage remain unchanged
with multiple participants; cooperation may make the fight easier. Do not add
enemies, health or damage based on player count. The guaranteed key for each
eligible participant is retained. **No ominous variant is selected:** Trial Omen
must not change this encounter's golem count/stats, key or fully charged core.
This is scoped to the Colossus; ordinary vanilla trials retain their behavior.

**Approved pursuit rule:** preserve the golem's **normal movement, pathfinding,
combat and pursuit**, with only the designated trial golem's initial player
aggression changed: it attacks eligible players without first being struck.
It may pursue players out of the cockpit according to normal targeting/pathfinding
limits. No custom cockpit leash, forced return, invisible boundary or return
teleportation is selected. This is not unlimited/global pursuit and does not
change ordinary village/player-created golems. Trial activation, rewards and
reset/cooldown handling are separate from this movement decision.

**October 8 revision:** autonomous aggression is preferred and selected as the
design direction, replacing the earlier player-initiated/retaliation-only plan.
It is feasible with targeted Fabric AI/behavior code, **not guaranteed by a trial
spawner configuration alone**. Scope the change to designated Colossus defense
golems; ordinary village/player-created golems must not become hostile globally.
Use automatic trial-spawner activation rather than a separate control console.
The technical baseline selects Survival/Adventure registration at 14 blocks with
vanilla visibility and a 30-minute completed-trial cooldown. Target switching follows
normal AI; persistence/reset and target-version behavior require the runtime proof
tests. Pursuit follows normal
behavior without a custom cockpit boundary. Normal-trial count and multiplayer
scaling are selected above: one golem, without waves or player-count stat scaling.
The target-game implementation still requires validation before release.

### Review follow-up: the golem's historical role

**Selected history:** the golem was a defense robot in the crewed Colossus's
cockpit. Earlier maintenance/later-installation alternatives are superseded.
Design the five-operator cockpit, intended hatch, activation cues, key and reward
presentation around that function. Why/how it remains operational remains unknown;
present-day encounter activation uses the trial spawner's automatic player detection.
The designated golem should attack autonomously; exact detection/targeting settings
are in the runtime contract and need testing. The retaliation-only plan is superseded.
The rest of the wreck does not activate. See the
[lore/gameplay review](../../../docs/project/LORE_GAMEPLAY_REVIEW.md).

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
- **No ominous Colossus variant:** Trial Omen does not strengthen or add golems,
  change key/core rewards or grant an ominous bonus. Validate the custom spawner/
  vault integration so the effect cannot substitute vanilla keys/loot or bypass
  eligibility. Do not disable ominous behavior for unrelated vanilla trials.

The room's appearance, exact block positions, and key artwork are deferred.

## Machine Core

### Agreed gameplay

- The player salvages an old machine energy-storage component from the Colossus.
- The Vault reward is **already fully charged and operational**, with no initial
  restoration or payment required before use. Full capacity remains the provisional
  256-operation target below, not a newly approved capacity increase.
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
The approved recharge uses **two coal blocks plus one amethyst shard**. Two coal
blocks alone supply 160 operations; the full core provides **96 more (60% more)**,
in exchange for the additional shard and acquiring the core. Further benefits are
reuse, stored remaining charge, and no idle drain.
Reaching the unique site and head, completing the trial, and recurring charging
could otherwise cost more effort than the reward saves. The now-approved fully
charged reward removes the previously proposed initial restoration cost.

Define the practical everyday problem solved by the core first, then tune capacity
and recharge costs together through survival and automation tests.
The 256-operation target remains provisional. The user has now selected the recharge
recipe below; this review does not approve a capacity increase, speed bonus or
free-fuel mechanism.

### Charge consumption

Charge is consumed by actual processing, not by elapsed burn time. An idle
appliance must not waste the remaining charge.

Removing or reinserting the core, transferring it through hoppers, saving and
loading the world, or unloading a chunk must preserve its charge. Normal hopper
use should be supported without resetting or duplicating fuel capacity.

The runtime contract specifies commit-only operation accounting, appliance-local
progress, progress reset on core/mode switching and depleted-core hopper extraction.
Implement and test those rules; ordinary burn ticks alone cannot satisfy them.

### Initial condition and recharging

**Approved initial condition:** the Vault core is fully charged and immediately
usable. The earlier damaged-core restoration proposal, including possible diamond/
iron/redstone costs, is superseded and must not gate the first use.

**Approved shaped crafting-table recharge recipe:**

| Empty | Amethyst shard | Empty |
| --- | --- | --- |
| Coal block | Depleted Machine Core | Coal block |
| Empty | Empty | Empty |

Input: **one depleted core, two coal blocks and one amethyst shard**. Output:
**one fully charged Machine Core**, with the provisional capacity of **256 completed
operations**. The shard sits directly above the core, and the coal blocks directly
left/right. Consume the fuel/shard and return the existing core recharged, not a
second core plus the original depleted item. No recurring diamonds or redstone
are part of this selected recipe.

The selected fuel is coal blocks (18 coal to craft), not loose coal or charcoal;
there is no vanilla charcoal-block equivalent. Additional fuel variants or charging
interfaces are not selected. Exact state handling and survival balance need testing.

The intended loop is: **claim charged core -> use -> deplete -> recharge**.

**Superseded proposals:** 24 loose coal/charcoal plus four redstone, and then three
coal blocks plus an amethyst shard. A normal crafting recipe consumes one item per
occupied ingredient slot, not 24 coal from a stack; the approved two-block recipe
fits the grid without counted stack inputs. Recharge still needs mod support to
validate depletion, preserve the existing core's state and prevent duplication or
overcharging. This document does not implement the recipe.

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
- Ordinary technical salvage in the Colossi should consist of **modest distributed
  copper and iron finds**, with possible **amethyst and redstone**. Use shared finite
  containers; exact item amounts/locations remain tuning/builder details. This is
  item loot, not permission to add more copper/raw-iron fields or alter material B.
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
The large arm's guaranteed magnet remains a shared find; no per-player chest
system or replenishment is selected. **Additional rare magnet finds in smaller
Colossi are now the chosen acquisition direction**, using a percentage loot chance
rather than a guarantee at every smaller site.
With only one large Colossus per world, later visitors cannot look for another
large arm with fresh loot, but may search the repeatable smaller sites. The approved
starting target is **10% per small-Colossus site**, with the magnet initially broken
and requiring repair. Container/position remains open; repair ingredients are
selected below, subject to survival tuning.
Do not confuse loot chance with
small-Colossus worldgen frequency or spawn loose magnets endlessly. This supplies
more acquisition opportunities, not a guaranteed magnet for every visitor.

### Additional acquisition: smaller Colossi

Smaller Colossi have an approved starting **10% loot chance per site** to yield
**one broken/inactive Salvage Magnet**, requiring repair before use. This is a
site-level chance, not 10% independently for every chest, player or visit. The
site's outcome must not reroll through reopening, reloads or newly arriving players.
The shared magnet-repair recipe below applies: four iron ingots plus one amethyst
shard. Exact salvage placement and quantities for the selected copper/iron theme
with possible amethyst/redstone remain tuning/builder details.
This does not copy the large site's core, key, vault or trial into smaller sites,
nor change the magnet's existing offhand/range/wear/repair design. See the
[smaller Colossus plan](SMALL_COLOSSUS.md).

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
| Durability budget | 1,000 successfully collected individual items |
| Durability cost | One point per individual item inserted by the magnet |

On October 28 the user changed wear accounting to individual items. A full
64-item stack costs 64 points. A partial pickup costs exactly the number inserted.
One assisted insertion cannot exceed the remaining budget. Failed pickups and
items that are merely attracted consume nothing. Ordinary nonmagnetic pickup
remains available after depletion. This replaces the earlier per-stack rule.

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
- **Approved full-repair recipe at a crafting table:** the existing damaged/broken
  magnet + **four iron ingots + one amethyst shard -> one fully repaired magnet**.
  Amethyst replaces the earlier two-redstone proposal; the Ender Pearl alternative
  is not selected. This applies to initial small-site repairs and subsequent wear.
  Preserve the existing item rather than creating a second magnet. The user selected
  the **shaped layout below**, not a shapeless recipe. State handling and survival
   balance still need implementation/testing; state handling is in the runtime contract.
- For the first version, enchantments must not bypass the intended wear and
  repair loop.
- No separate energy charge is planned for the magnet; durability supplies its
  maintenance cost.

The intended loop is: **equip in offhand -> collect nearby drops -> wear out ->
repair**.

**Approved shaped full-repair layout:**

| Empty | Amethyst shard | Empty |
| --- | --- | --- |
| Iron ingot | Existing damaged/broken Salvage Magnet | Iron ingot |
| Iron ingot | Empty | Iron ingot |

Use one iron ingot in each of the four iron slots; all three Empty slots must be
empty. Consume the four ingots/shard and return **one fully repaired existing
magnet**, preserving its applicable item state without leaving a duplicate input.
This applies both to broken small-site finds and later wear of the functional magnet.

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
material version with the stated inventory. It is selected in Alpha 4.9;
offline post-salvage previews remain simulations, not survival-balance acceptance.

The V3 export contains **141,523 copper-based blocks and 5,609 raw iron blocks**.
These historical counts are verified for V3, not asserted for material study B.
Estimate recoverable resources from the selected export and compare them with
the core and magnet's useful value. Bulk mining could overshadow the special
rewards and dismantle the only large landmark for everyone else.

Selected study B implements the material response: removable copper armour regions
and economically less significant bulk fields, preserving intact V4.1 geometry.
Its palette and inventory are approved; actual Minecraft appearance, recoverable
resource value, and balance against the core/magnet still need validation. Normal
mining is not prohibited. Existing worldgen-feature protection is not player-mining
protection; no indestructible-landmark mechanic is approved. Coordinate with
[Colossus design goals](../docs/COLOSSUS_V4.md) and the
[shared review](../../../docs/project/LORE_GAMEPLAY_REVIEW.md).

## Remaining deliverables and acceptance checks

### No further fundamental gameplay round required

Technical defaults now cover icon thresholds, full arm-magnet durability, modest
site-wide ordinary salvage, state-preserving crafting, furnace progress/hoppers,
magnet motion/accounting, trial eligibility/cooldown and durable Vault claims.
These are delegated starting choices, not extra user approvals or implemented code.

Remaining deliverables are original item artwork/tooltip wording, builder-bound
arm/cockpit/hatch/chest coordinates and target-version implementation/proof tests.
Validate survival usefulness, material-B mining value, 10% small-site loot and
multiplayer/protection compatibility against the acceptance matrix. Do not add
feedback effects or conflict traces merely because older review lists proposed them.

### Acceptance checks

- Both items provide useful convenience without increasing combat strength.
- The arm's intended access route is identifiable and leads to a copper chest
  with one immediately usable magnet, without requiring a key or scripted fight.
- The core processes the intended number of operations without idle drain,
   speed bonuses, or charge-reset exploits.
- Vault cores start fully charged/usable, with no initial restoration requirement.
- Recharge follows the agreed shaped recipe (amethyst above, coal blocks left/right,
  depleted core in the middle), returns one fully charged core and consumes the
  two coal blocks/shard without duplication. Validate depleted-core inputs/state.
- Core state survives transfer, item drops, save/load, and chunk unloads.
- Core/magnet tooltips show the correct remaining values and explicit empty/broken
  states; icons update across consumption, repair/recharge and save/load. Do not
  show an inventory status bar in place of the selected icon-state presentation.
- The magnet activates only in the offhand and respects its range and walls.
- Full inventories and failed pickups do not create repeated wear or noisy
  attraction loops.
- Depleted or broken items remain recoverable and can be restored without
  duplication or loss.
- Collection and furnace processing remain practical in multiplayer and under
  normal automation loads.
- In Minecraft 26.2, verify golem spawning, trial completion tracking, guaranteed
  key rewards, key consumption, and the guaranteed Machine Core vault reward.
- Verify designated defense golems attack without being struck; ordinary golems
  retain normal behavior. Test encounter entry/exit, multiple players and reloads.
- Reject vanilla keys and preserve per-player vault eligibility across save/load.
- Check both normal and ominous paths for incompatible rewards or repeat-claim
  exploits.
- Test late arrivals and a large player population at the same vault, including
  save/load and eligibility retention; previously claimed rewards must not reset.
- Implement/test the selected distinct shared-chest reward policy before finalizing loot.
- Test the smaller-site magnet loot chance against its agreed roll unit and site
   frequency; no generation/load/reopening duplication or automatic refill.
- Small-site finds are broken/inactive until repaired; the large arm's guaranteed
  magnet remains immediately functional. Verify the 10% chance applies per site.
- Confirm the landmark's resource economy does not unintentionally make the
  planned core/magnet rewards irrelevant; document any deliberate salvage tradeoff.

Functional custom items require additional mod code; the current placement-only
runtime and Blender conversion pipeline do not implement these behaviors. Trial spawner
and vault configuration use block-entity data and custom loot tables; the current
schematic converter rejects block entities, so the build pipeline will need to
preserve or inject those data in a separate supported step. This document records
design decisions only and does not change the playable build.
