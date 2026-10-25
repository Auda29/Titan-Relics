# Shared relic distribution and unique-site resolver

Prepared: October 8, 2026. **Implemented October 25 for fresh 26.2/Fabric worlds;
production density and survival balance are not broadly measured.** See the
[implementation, scheduling and verification record](../testing/DISTRIBUTION_IMPLEMENTATION_20261025.md).
User approvals remain in the
[implementation plan](../project/UMSETZUNGSPLAN.md#distribution-proposal-and-approved-map-exceptions).
The algorithm below is a delegated engineering choice, not a new user-selected rate.

## 1. Frozen inputs and approved invariants

- Overworld only; one combined opportunity per approximately **5,000 × 5,000**
  horizontal blocks for repeatable relics, not an independent roll per family.
- Successful centers are **at least 2,000** blocks apart. Obelisk centers are
  **at least 15,000** apart; their **6,000-radius** regions neither touch nor overlap.
- Exactly one selected natural large-Colossus destination per supported enabled
  save, **at least 30,000 blocks from the initial shared world spawn**; independent
  of the repeatable budget. A missing valid destination never permits a fake one.
- Rejections remain empty. No count caps, filling quotas, extra skull rolls,
  replacement types, palette multiplier or favorable-seed resampling.
- Keep existing asset biome/terrain constraints until separately justified by
  tests; do not loosen them to manufacture sites at the requested density.

Snapshot seed, dimension, initial shared spawn, generator/biome settings, selected
asset hashes and placement policy version for the save. Later beds or changing
the shared spawn do not move the large site. The first gameplay distribution
targets **fresh worlds**; safe treatment of existing visual-alpha worlds is in
[Gameplay runtime](GAMEPLAY_RUNTIME.md#2-world-state-and-existing-saves).

The snapshot is the source for deterministic decisions, not the set of explored
chunks or wall-clock time. Freeze planning parameters for an existing gameplay
save: changing spacing, weights, terrain dependencies or asset transforms requires
a new world or a separately tested migration. Do not mix a changed policy with
old rewards/regions silently. Runtime generation disabling is discussed below.

## 2. Shared opportunity and exact ticket ranges

Use mathematical floor division for signed cell coordinates. Derive one position
per cell from independent versioned seed streams; keep a 256-block margin inside
the cell and snap to the owning chunk center. This margin prevents snapping into
another cell; it does not guarantee 2,000-block separation. Use independent
streams for tickets, priority, orientation, palette and loot so adding loot cannot
move geometry. Define/hash the serialization and tie-breaks in implementation tests.
Bind the planned center to the actual transformed natural footprint's horizontal
center, solving its origin before validation; do not use a lower corner/jigsaw
connector in the final distance checks. Record any deterministic half-block/parity
adjustment, keep it inside the cell margin and validate the **actual** placed center.

Draw one integer `u` in **0..9,999**:

| Tickets | Inside accepted Obelisk region | Outside |
| --- | --- | --- |
| 0..2,999 | Obelisk attempt | Obelisk attempt |
| 3,000..3,249 | Crowned skull | Crowned skull |
| 3,250..3,499 | Crowned skull | Skull 2 |
| 3,500..4,499 | Crowned skull | Empty |
| 4,500..5,999 | Skull 2 | Empty |
| 6,000..6,199 | Tower | Tower |
| 6,200..6,399 | Small Colossus | Small Colossus |
| 6,400..6,599 | World Tree | World Tree |
| 6,600..9,999 | Empty | Empty |

Thus inside shares are **30 / 15 / 15 / 2 / 2 / 2 / 34%** and outside shares
**30 / 2.5 / 2.5 / 2 / 2 / 2 / 59%**. Region classification cannot change an Obelisk
ticket into another type if its Obelisk attempt fails. Crowned palettes share one
design ticket; select a compatible palette once, with no new family roll.

## 3. Pure validation and finite-neighborhood acceptance

The existing `SeparatedPlacementCondition` reserves independent nominal candidates.
The browser illustration uses a finite, globally sorted example. **Neither is the
production algorithm.** Use bounded-neighborhood priority thinning instead of an
infinite recursive greedy scan or exploration-order-dependent reservations.

### Phase A: resolve the unique large site

Resolve and save the large center before publishing final repeatable decisions
near it. A temporarily unresolved large site leaves planning jobs pending; it does
not allow another resolver or an already-generated conflicting repeatable site.
Initialization must yield rather than stall chunk generation/server startup.
**Scheduling proof gate:** a structure-start job must not finalize its affected
chunk with an unresolved site decision and later retrofit a relic. Use safe
initialization/task dependencies before that generation stage; prove there is no
server-thread wait/deadlock or unlimited startup work. If target APIs cannot meet
this, block the feature rather than silently skip a would-be anchor or add retrogen.

### Phase B: accepted natural Obelisk anchors

1. Enumerate raw Obelisk-ticket candidates in the necessary neighborhood.
2. Check their exact orientation/footprint, enabled-at-planning policy, terrain,
   biome, height/water and distance from the committed large site.
3. A valid raw candidate becomes an accepted anchor only if **no other valid raw
   Obelisk candidate within the forbidden distance has a smaller stable priority**.
   Break equal priorities with signed cell coordinates. Distance 15,000 is allowed
   with equal 6,000 radii; always also require `distance > radiusA + radiusB`.
4. Only **accepted, validated natural placements** define regions. An invalid,
   unverified or priority-rejected candidate is never a region anchor.

This local-minimum method has a finite 15,000-block conflict neighborhood. A
terrain-valid candidate can suppress a higher-ranked candidate even if itself
suppressed by another neighbor; that conservative hole stays empty. There is no
recursive dependency on accepted neighbors and no density compensation.

### Phase C: remaining shared tickets

1. Determine membership using accepted Phase-B anchors within 6,000 blocks, then
   apply the same ticket once using the table above.
   Membership uses horizontal squared distance `<= 6,000²`, including the edge;
   the non-touching rule means no competing region ownership is needed.
2. Validate that resulting type/variant against terrain and its real footprint.
   Reject sites conflicting with the large site or accepted Obelisks at the
   2,000-block floor; do not reroll their type.
3. Thin the remaining valid raw candidates locally: accept only when no smaller
   priority eligible non-Obelisk candidate violates the 2,000-block floor/footprint.
   As in Phase B, do not recursively decide neighbors' final acceptance.

Validation of a Phase-C neighbor includes its region query. A query must therefore
cover the nested **2,000 + 6,000 + 15,000-block** dependency halo, plus cell-position
and footprint margins; never query only the rendered map rectangle. Cache pure
results by policy/seed/cell, with no need to load or decorate neighbor chunks.

**API proof gate:** the same base-terrain/biome/height/water predicates must run in
the planner and natural structure-start path, without generating neighbors or
depending on visited chunks. Compare their results against actual 26.2 generation.
Until that equivalence is demonstrated, a candidate is **unverified/pending**, not
a map destination or regional anchor. If a required terrain predicate cannot be
evaluated safely, fix the adapter or report the limitation; do not silently use
nominal anchors. Later player edits are not a reason to recalculate a committed site.

The approved browser map remains an **illustration of distances and rates**, not
a promise of identical coordinates/counts under this thinning method. Measure the
aggregate hierarchy over many seeds, including failed candidates and region coverage.

## 4. Unique large-Colossus search

Delegated search baseline: try a **preferred 30,000–60,000-block annulus** around
the frozen initial spawn, then consecutive outward annuli **20,000 blocks wide**.
This is a search preference, **not a 60,000-block cutoff** or an extra approved
distance constraint. Respect the actual world border/build limits.
Annuli are lower-inclusive/upper-exclusive, beginning `[30,000,60,000)`, then
`[60,000,80,000)` and so on; evaluate each center once, not once per intersecting
cell/annulus. A footprint must fit the allowed border/build-height domain.

Use a separate versioned candidate stream with one unique-search opportunity per
5,000-block search cell, not another repeatable-family ticket. For each annulus,
filter centers by distance/border and order candidates by stable seed rank/cell
tie-break. Select the **first fully validated** candidate; an unknown earlier
candidate blocks final commitment until resolved, not until another player searches.

One save-wide resolver owns a persisted `PENDING -> COMMITTED` transition; record
center, orientation, exact asset/validation version and natural start identity.
Persist cursor/annulus for resumable work. Budget **up to eight candidate evaluations
per scheduling slice, with a 2 ms soft deadline between evaluations** as a starting
target. One expensive evaluation may exceed it: profile and bound that adapter;
do not claim the deadline is already guaranteed. World-thread operations stay on
the correct thread; pure work may be offloaded only after thread-safety proof.

Time-budget expiry, unloaded chunks or an exhausted preferred annulus mean
**still pending**. Definitive absence requires a reason such as disabled-before-any
destination or an exhaustively evaluated finite allowed world-border domain.
Every map and `/locate` uses the same saved destination/resolver. Locating must
not create a second Colossus or force templates into rejected terrain.

## 5. Disabling, reloads and compatibility

- Initial disabled types leave their allocated tickets empty; never renormalize.
- For a gameplay save, runtime deactivation **pauses new uncommitted placements**,
  not an ownership reroll. Already committed valid sites/regions and destination
  identity remain, including the completion of their outstanding chunk actions.
  A planner must not commit a new disabled Obelisk as a regional anchor.
- For deterministic regional planning, the saved snapshot/committed planning batch
  is immutable. Type toggles affecting a still-unplanned area require a controlled
  new planning epoch with conservative boundary exclusions against committed sites;
  **live epoch migration is not in the first gameplay release**. Initially pause
  unplanned work while changed enable settings await a fresh world/explicit migration.
  Disabling the unresolved unique destination still invokes the approved unavailable
  map policy, without manufacturing a site; a committed destination remains valid.
- Re-enabling an unresolved unique resolver may resume the **same** search state,
  never undo an already paid map-origin compensation. No automatic retroactive
  placement in already generated chunks or conversion of old `/place` copies.
- Legacy alpha settings packs implement independent sets and are not equivalent
  to this shared-budget policy. Reject incompatible gameplay overrides clearly;
  preserve the old visual-alpha artifacts and document fresh-world testing.

The first implementation must log why planning is pending/paused rather than
silently return an empty map or reset its state. Existing-saves migration is a
compatibility feature, not permission to delete extra historical large starts.

## 6. Required diagnostics and release evidence

Count raw opportunities, assigned tickets, terrain-valid candidates, priority/
distance rejections, accepted anchors, region area and actually materialized sites
separately. Record the policy/asset/generator versions and unique-search effort.
Compare multiple exploration orders, save/reload, negative-coordinate cells,
border cases and simultaneous map requests. Do not infer world-level rarity from
three examples or interpret a seed's seven Trees/six Obelisks as a count-cap bug.

See [Gameplay acceptance](../testing/GAMEPLAY_ACCEPTANCE_PLAN.md). Implementation
and runtime performance proof remain future work; this document closes the
algorithm choice, not those evidence gates.
