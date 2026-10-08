# Gameplay acceptance plan — future evidence, not results

Prepared: October 8, 2026. Target: **Minecraft 26.2 / Fabric**, Java 25, Loader
0.19.5, Fabric API 0.161.0+26.2 and stable Lithostitched 1.8.0 baseline. Record
actual artifact/dependency hashes at test time. These tests are **not yet run**;
Alpha 4.9 placement reports do not prove planned gameplay.

Owners/specifications: [Runtime](../technical/GAMEPLAY_RUNTIME.md),
[markers](../technical/GAMEPLAY_MARKERS.md),
[distribution](../technical/RELIC_DISTRIBUTION.md). Implementation needs a separate
request and builder deliverables; this plan adds no gameplay/test code.

## 1. Small automated proof gates

| Area | Required cases / pass condition |
| --- | --- |
| Marker format | Reject wrong hash/revision/size/ground, unknown roles/schema, missing/duplicate roles, out-of-bounds/reversed regions, invalid placeholders and jigsaw conflicts; no skull markers or clearance additions |
| Transforms | Raw-to-natural offset, four rotations/facings, non-square bounds, negative world coordinates and chunk-edge feet/anchors agree with actual template transforms |
| Tickets | Exhaustively enumerate 10,000 tickets for each region case; exact approved shares, no extra roll for palette/chest/disabled type |
| Priority planner | Two/three-neighbor chains, tie-breaks, negative cells, complete dependency halo, rejected/unknown anchors, equality boundaries and cross-family separation; queries are bounded and exploration-order independent |
| Unique resolver | Preferred/outward annuli, earlier unknown candidate, timeout/resume, concurrent requests, border constraints, no candidate below 30,000; never treat an exhausted time budget as definitive absence |
| Item state | Bounds, single-item stacks, component migration, full/partial/zero icons/tooltips, no inventory bar and no name-only spoofing |
| Crafting | Both shaped layouts and trim copy layout; reject extras/wrong state, normal/Shift-click/result preview, preserve state and consume once without duplicate remainder |
| Core processing | Count successful recipe operations, not output count/time; invalid input, full output, partial recipe, mode changes, removal, hopper transfer, device break, last charge and normal appliance speed |
| Magnet | Zero wear on failed pulls, collision shapes/closed doors/glass, ownership/delay, partial pickup/merge, two-player contention, stale inventory/entity state and broken-item retention |
| Grants/maps | Per-player Vault history beyond native list limits, participant queue, stable claim/delivery IDs, pending map copies and one origin compensation, no old-copy reactivation after compensation |
| Tree | Exact 24-radius 3-D boundary through blocks, per-player refresh/expiry, stronger potion/hidden-effect/milk/death behavior, persistent anchor after removal and no aura from copied blocks |
| Entity initialization | Five one-time ordinary Endermen, pending UUID reconciliation, no regeneration after despawn/reload, no injected entities from raw template copies |

Use deterministic fixtures before expensive whole-world tests. Tests of a spec
example or browser geometry are not tests of the future Minecraft implementation.

## 2. Target-version runtime scenarios

Run both integrated and dedicated servers with at least two real clients, ordinary
world saving and disconnect/rejoin. Begin without terrain mods, then record an
explicit Terralith/Tectonic/Biomes O' Plenty/Dungeons & Taverns matrix. Preserve
personal saves; use isolated disposable copies/new worlds, never downgrade 26.2.

| Scenario | Acceptance |
| --- | --- |
| Single-golem trial | Solo/group/late joiner, with/without Trial Omen: exactly one vanilla-strength golem, attacks without retaliation, normal pursuit outside cockpit; ordinary golems unchanged |
| Trial abandonment | Flee, unload golem/spawner separately, reload, defeat outside cockpit, remove entity without death: no healing/forced return, duplicate living golem, premature completion or repeated participant grant |
| Vault | Transfer keys, reject vanilla keys, full inventory/disconnect, repeat opening and many UUIDs: consume once per successful opening, fully charged core, no forgotten previous claims |
| Core automation | Each of furnace/blast furnace/smoker, recipe outputs >1, output blockage, hoppers, extraction mid-job and controlled reload: correct remaining charge and no idle loss/free residual heat |
| Finite loot | Large arm one functional magnet, small sites one 10% outcome per site, site-wide modest salvage, Tower one Ender roll, Obelisk six ordinary plus specials; no revisit/player/chest multiplication |
| Tree | Inside/outside/above/below sphere, walls/caves, removed whole Tree/amethyst, copied wood elsewhere and multiple players: persistent original aura only, unchanged natural hostiles, no universal safe zone |
| Animal adjustment | Same seed/route paired with adjustment off/on, pre-full creature cap, valid/invalid habitats and unrelated species: ordinary caps respected, only selected species modestly increased, no timer refill or forced herd |
| Lighting/trim | Root/base scope and 15-block maximum, ground spawnable darkness probes; Monolith on all supported armor pieces/materials, no statistics, original art and exact duplication ingredients/output |
| Pending maps | Timeout/disconnect/reload and several copies before resolution: explicit unconfirmed state, same verified target or one three-emerald compensation, trim unaffected |
| Existing alpha saves | Detect no-ledger/multiple-large state without modifying art/containers; gameplay initialization requires explicit future migration, no automatic retrofit |

For each deferred initializer simulate a stop/reload before and after its action.
Crash-test reward delivery across player/world save boundaries; pass only with
documented reconciliation, not a claim that vanilla saves are one transaction.
For unknown/ambiguous grants, fail closed with a recoverable diagnostic rather
than issue duplicate loot or silently lose the promised grant.

## 3. Distribution and exploration evidence

1. Initial fixed seeds: `731204`, `-48291736`, `20260913`; log each actual initial
   spawn and planner snapshot. These are planned gameplay tests, not reused alpha results.
2. Survey a **120,000 × 120,000-block** window centered on initial spawn using the
   pure planner across **at least 30 predetermined seeds**. This is a diagnostic
   sample, not a mandated per-world relic count or world-size limit. Do not replace
   low-count seeds or renormalize rejected outcomes.
3. Generate representative accepted sites in matching fresh worlds from different
   exploration orders. Compare planner versus real natural-start validity, centers,
   rotations and per-chunk initialization; manual fixtures do not satisfy this step.
4. Verify distances on all accepted pairs, including outside the survey window's
   dependency halo: 2,000 general, 15,000 Obelisk, non-touching 6,000 regions and
   30,000 unique spawn floor. Exactly one committed natural large destination.
5. Report raw tickets, validation/spacing losses, region coverage, materialized
   frequencies and route/travel effort with/without maps. The relative hierarchy
   is an aggregate goal; it need not order every finite seed sample.

Repeated valid map destinations are expected, not a search failure or promise of
another fresh shared magnet. A pending unique search must not let worldgen finalize
conflicting sites or publish a guessed map target; prove scheduling is safe.

## 4. Performance, artifacts and approval

Measure clean paired routes with the same seed/configuration/JVM/render conditions:
planner evaluations/cache size, server tick impact, chunk latency, unique-search
stalls, marker initialization and magnet/entity load. The resolver's 2 ms slice
target is a profiling goal, not a demonstrated bound. Establish release budgets
from the baseline before calling performance accepted.

Record artifact/source/marker hashes, logs and failures in a **new dated report**;
do not rewrite historical alpha evidence. Inspect installed/downloaded JAR contents
and client/dedicated resource loading. Preserve original exports, 1.21.1 port and
existing worlds. No release claim until correctness, API proof gates, survival
balance and actual builder/interior acceptance have passed.
