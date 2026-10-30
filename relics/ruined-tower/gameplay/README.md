# Ruined Tower gameplay planning

> **Current status, October 30, 2026:** The selected gameplay is released; current models, implemented values, evidence and remaining tuning are recorded centrally. See the
> [Alpha 5.0.3 status and roadmap](../../../docs/project/CURRENT_STATUS_AND_ROADMAP.md). Approved design requirements
> remain specifications; dated pending/unimplemented claims below are historical
> where superseded by the released implementation and linked evidence.

Updated: October 8, 2026. The visual V7 ground-v3 asset is integrated in Alpha 4.9;
the directions below are planning, not implemented traversal, loot or encounters.
Technical choices are in the [runtime contract](../../../docs/technical/GAMEPLAY_RUNTIME.md)
and [builder marker handoff](../../../docs/technical/GAMEPLAY_MARKERS.md).

## Approved lore

The tower was the **base from which the Titan-clearing campaign was organized**.
It was **never completed**, accounting for its intended stronger dilapidation
relative to the Colossi. Do not interpret every gap as later battle damage or
present it as a once fully finished building unless a specific detail is agreed.
The reason construction stopped and original room functions are still open.
Colossus crews were approximately player-sized, possibly somewhat larger; this
does not specify the tower staff count or exact room dimensions.

The campaign occurred thousands of years ago. No living Titans remain. Modern
Minecraft mobs and players inhabit or otherwise reuse the relics; this does not
identify them as the original builders or campaign staff.

## Approved gameplay and builder deliverables

### Approved traversal and occupation direction

- The tower is **predominantly abandoned**, not an agreed populated settlement.
  Modern occasional inhabitants remain compatible with that overall condition.
- **Incomplete stairs lead toward an upper level. Players must build to bridge
  parts of the route.** A finished continuous stairway is not required. Exact
  upper level, gaps and connected rooms remain to be planned.
- No mandatory path through arbitrary solid walls is selected; ordinary player
  building and mining remain allowed. Clearly distinguish intentional broken
  stairs from unintended inaccessible/missing structure parts.

### Approved lower dungeon direction: natural mobs with an Enderman accent

**Ordinary mobs spawn naturally and remain unchanged.** No dungeon spawner,
custom enemy roster or forced hostility is selected. The user wants more Endermen
and delegates choosing between local frequency adjustment and a few entities
placed during natural generation.

**Selected integration baseline under that delegation:** place a one-time group of
**five ordinary Endermen per natural Tower** at
builder-supplied lower-area markers. This avoids replacing the biome's ordinary
monster list or introducing a recurring mob source. Current structure data has
empty `spawn_overrides`; a category override would replace a spawn list rather
than simply add Endermen. No entity-placement system is implemented yet; validate
safe positions, worldgen timing, rotation and saved one-time placement state in 26.2.
The user selected five instead of the earlier two-Enderman proposal. Spread the
five positions through the lower dungeon using builder markers, not all at one
point; do not increase other ordinary mobs or add recurring spawners.
If that approach proves unreliable, reconsider a locally scoped natural-weight
adjustment without changing unrelated mobs/biomes; do not apply both automatically.

Endermen retain vanilla neutrality, teleportation, block pickup and despawning;
they are not captive guaranteed enemies or hostile like the defense golem.
No forced persistence, respawning on reload/revisit, global Enderman behavior
change, custom boss, End portal or mandatory combat gate is selected. Present-day
occupants are not original campaign staff or evidence of living Titans.

### Approved finite loot and provisional roll scope

The user's loot rule is **5% Eye of Ender, otherwise 4–6 Ender Pearls**, in
**shared finite chests**. No per-player opening/replenishment is selected.

**Assistant-defined starting interpretation:** use **one Ender-reward roll per
Tower site**: 5% yields **one eye**, 95% yields **4–6 pearls** (uniform quantity),
not both guaranteed together. Distribute that one result into the designated
reward chest; adding incidental chests must not multiply the eye chance or pearl
budget. The one-eye quantity/site-level roll are implementation baselines, not
separately user-specified values. Persist loot/depletion; reopening/reloading must
not reroll or refill it. Exact chest markers remain a builder deliverable; no other
ordinary Tower loot is in the initial pool. Eyes affect End progression, so validate the site's rarity
and reward amounts together rather than creating a repeatable eye farm.

### Remaining builder and runtime evidence

- Original room functions/reason construction stopped may stay unknown; builder
  details must support the selected incomplete ascent, not explain every room.
- Entrance, connected rooms/levels, stair gaps and the intended upper destination.
- Builder markers and implementation validation for the recommended one-time
  Enderman group; ordinary natural spawning and vanilla behavior are retained.
- Reward chest marker and balance testing of 5% eye /
  otherwise 4–6 pearls under the documented starting roll scope.
- Exploration difficulty through layout rather than added mob-spawner systems.
- Visible campaign/unfinished-construction clues; validating Tower frequency and any regional links.

**Approved distribution starting value:** **2% per shared repeatable-relic opportunity**,
inside or outside Obelisk regions, equal to small Colossi and World Trees. This is
not an independent per-chunk roll or a world-wide site cap; placement rejection
can reduce the realized frequency.

The abandoned condition, incomplete player-built ascent, natural ordinary mobs,
Enderman accent and finite reward rule are selected; exact construction belongs
to the building agent, with entity-placement/loot integration still pending. First
target is 26.2/Fabric. The [planning review](../../../docs/project/GAMEPLAY_PLAN_REVIEW.md)
closes the documentation gate, not implementation authorization/runtime acceptance.
Shared history: [lore bible](../../../docs/project/LORE-BIBLE.md).
