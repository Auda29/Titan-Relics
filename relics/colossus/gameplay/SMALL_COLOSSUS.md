# Small Colossus — lore and gameplay planning

Recorded: October 8, 2026. Current visual asset: V7 ground-v3 in Alpha 4.9.
Gameplay/interior implementation is not authorized until the all-relic planning
and documentation consistency gate is complete. First gameplay target: 26.2/Fabric.

## Approved history

- Smaller Colossi were **companions of the central large Colossus** in the ancient
  Titan-clearing campaign. **All Colossi were crewed**, not autonomous machines.
- Each smaller Colossus had **two operators**, approximately player-sized and
  possibly a little larger, like the large machine's five operators. Exact crew
  height/species and station dimensions are not selected.
- Their original construction used **weaker materials than the large Colossus**.
  This explains their more severely decayed interior and near-loss of the cockpit;
  it is not a selected replacement palette, hardness change or new block type.
- The conflict occurred thousands of years ago. The Titans' exact nature and the
  reason for the campaign are lost to time; original crew identity remains unknown.
- No living Titans remain. Current mobs and players inhabit or otherwise reuse
  the relics; modern residents are not assumed to be the original crews.
- Smaller Colossi **may occur multiple times** per world. Only the large landmark
  has the approved one-natural-site rule; neither rule settles exact smaller-site rates.

This connection is lore, not authorization to add live/moving machines, a boss,
or automatically copy the large site's trial, core or vault into smaller sites.
**Rare magnet loot is now explicitly selected below**, not inherited by default.

## Decisions still needed

### Approved interior direction

Smaller Colossi **can be entered**. Their interiors are very dilapidated, with
the original cockpit **effectively no longer present**. Do not restore an intact
two-seat operating room just because they historically had two crew members.
Exact residual cockpit traces and decay geometry still need design.

### Selected loot direction: rare Salvage Magnet

The user proposed **percentage-based magnet loot** in smaller Colossi, chosen as
the additional acquisition direction so the item stays rare. The large arm still
has its guaranteed shared magnet; repeatable smaller sites provide opportunities
for additional/late multiplayer visitors, not guaranteed per-player rewards.

**Approved starting values:** **10% chance per small-Colossus site** for **one
broken/inactive magnet**, which must be repaired before use. The shared repair
recipe is full repair at a crafting table using the existing magnet plus **four
iron ingots and one amethyst shard**, replacing the proposed two redstone. The chance
is not per chest, player or visit;
reopening/reloading must not reroll a site or refill its shared reward.

Container and location remain open, and the chance needs survival tuning against
actual site frequency. Do not implement a chance to create extra Colossi or endless
dropped-item spawning instead of loot. No
Machine Core, key, trial or per-player vault is selected for these sites. Ordinary
salvage uses the selected copper/iron theme, with possible amethyst/redstone,
in modest distributed shared finite finds. Exact amounts and positions remain
to be tuned/supplied; this does not add new bulk mineral fields to the model.

### Remaining decisions

- Entrance, explorable extent and targeted terrain clearing for the ruined interior.
- Remaining machinery/crew traces without rebuilding a working or intact cockpit.
- Exact material/decay presentation of the weaker construction while preserving
  the accepted exterior unless a separate change is approved.
- Later inhabitants/reuse, if authored; mob roster, spawning and persistence.
- Magnet placement/container, repair crafting layout/state handling and survival tuning of the approved
  10% per-site starting chance; initial condition is broken, not undecided.
- Modest copper/iron salvage amounts, optional amethyst/redstone and shared
  finite container positions alongside the magnet.
- Visible companion-machine/campaign clues and final repeatable-site rarity.

Related: [large Colossus items and cockpit trial](ITEMS.md),
[shared lore](../../../docs/project/LORE-BIBLE.md), and
[all-relic planning gate](../../../docs/project/UMSETZUNGSPLAN.md#current-planning-gate--october-8-2026).
