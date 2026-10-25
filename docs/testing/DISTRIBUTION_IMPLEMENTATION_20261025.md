# Gameplay distribution implementation, October 25, 2026

Target: **Minecraft 26.2 / Fabric / Java 25**, development version
`0.1.0-alpha.5.0-dev`. This change implements the distribution and destination
portion of [the approved contract](../technical/RELIC_DISTRIBUTION.md).
Interior selection, natural reward/encounter markers and map acquisition remain
separate work. No interior, skull, selected raw/natural NBT or launcher profile is
changed. This is not the completed Alpha 5.0 gameplay release.

## Behavior

New noise-based Overworlds receive a frozen planning snapshot. Existing worlds
without one retain legacy placement. There is no automatic conversion, retrogen,
deletion of old Colossi or reinitialization of existing containers.

- One repeatable opportunity per 5,000-block cell. Independent versioned seed
  streams choose position, ticket, unsigned priority and rotation. Chunk-center
  positions remain at least 256 blocks inside each cell; signed floor division
  works across zero. Loot does not consume these streams.
- Exact inside/outside ticket ranges from the contract; one crowned-skull ticket
  chooses its sole compatible biome palette. Disabled or rejected results stay
  empty. Partial family/weight and legacy density overrides are rejected.
- Terrain-valid Obelisks undergo finite 15,000-block priority thinning before
  becoming 6,000-block regional anchors. Other terrain-valid candidates use
  2,000-block thinning and the full nested dependency halo. Raw priority losers
  can suppress neighbors; no quota or replacement roll repairs the resulting holes.
- The independent large-Colossus search begins in `[30,000,60,000)` around the
  original shared spawn, then continues through 20,000-block annuli in stable
  priority order. It has no 60,000-block cutoff. The entire rotated footprint must
  fit the frozen border/build-height domain. Exhausting time alone is never absence.
- The selected site and resumable search cursor are committed atomically before
  they are published. All natural generation, expedition-map origins and relic
  `/locate` queries use this destination. Bed changes and `/setworldspawn` cannot
  relocate it. Doubled center coordinates preserve half-block parity.

The existing Alpha 4.9 templates remain selected pending interior review. Their
accepted biome, full 25-point terrain grid, slope, height, water and ceiling
checks are reused. Single pinned pool elements are transformed explicitly around
the planned center, then the validated immutable result constructs the actual
native `StructureStart`. Normal processor/placement/protection code still runs.
Manual `/place` copies do not become additional natural destinations.

## Scheduling and persistence

One serialized planning worker owns base-height and noise-biome queries. It does
not call `getChunk`, decorate terrain, create a server-level fixture or mutate
gameplay inventories. Templates are preloaded before it starts. The initial
adapter accepts the native noise-based generator; custom generator classes are
rejected rather than treated as proven compatible.

Before `STRUCTURE_STARTS`, candidate chunks receive a `CompletableFuture`
dependency. Neither the server thread nor a generation worker waits by blocking
on that future. The original structure-start method runs after its result is
available; a pending or failed plan is not silently finalized as an empty chunk.

Vanilla's initial spawn finder itself generates chunks. During that bounded
search, a repeatable decision may complete only when its entire relevant
dependency query can prove separation from **every possible future large site**,
using the 30,000-block spawn floor and a verified 128-block spawn uncertainty.
Otherwise it stays pending. The actual final shared spawn freezes the search
snapshot before the large resolver starts. A changed spawn-finder contract fails
explicitly, rather than producing a deadlock or retroactively inserting a relic.

`<world>/data/relics_distribution_v1.json` contains a SHA-256-checked envelope,
seed, initial spawn, generator/biome/tag/pool/processor/template fingerprint,
initial enabled families, border domain, annulus cursor and unique site. Unknown,
corrupt or incompatible snapshots stop planning. Writes flush a temporary file
and atomically replace the journal. Brief Windows delete-sharing locks retry the
same atomic operation for a bounded total of 63 ms; no non-atomic/stale fallback
exists. Clean shutdown drains the current writer before closing the executor.

The resolver evaluates at most eight candidates per slice and checks a **2 ms
soft deadline between evaluations**. A single native terrain query can exceed
that target. This work does not claim a 2 ms hard latency bound. Diagnostics
record the slowest evaluation, candidate count and slice count. Caches are bounded;
their eviction changes cost, not decisions. Query counters are not world counts.

Successful datapack reloads retain the plan only when its fingerprint and enabled
families remain identical. Incompatible changes pause planning with an explicit
error; restore the frozen setup and restart, or use a fresh world. There is no live
planning-epoch migration. Keep the complete world/journal/gameplay/map data together
when backing up; deleting the journal is not a supported reset operation.

## Commands and maps

```text
/locate structure relics:colossus
/locate structure #relics:relics
/relicsdistribution status
/relicsdistribution plan <block-x> <block-z>
/relicsdistribution map
```

The operator map command supplies a persistent expedition map without requiring
unfinished archaeology/loot initialization. Ordinary players will acquire maps
through that later integration. Pending maps have no fabricated map ID/target.
Copies preserve the origin and share its map ID once resolved; separate origins
resolve to the same global destination. Existing compensation/claim safeguards
remain in the gameplay ledger. Native synchronous map lookups may return only the
committed global destination; they do not scan the old independent relic sets.

Relic-only `/locate` queries run asynchronously and report the result later.
Repeatable searches cover a bounded 100,000-block radius; the unique destination
is global. A failed finite repeatable search is not proof of world-wide absence.
Mixed third-party structure tags are outside this adapter. Command completion
returns scheduling success, so `/execute store result ... locate` is not a
synchronous distance API. Long-distance output uses overflow-safe arithmetic.

## Verification

See the [machine-readable runtime evidence](distribution-20261025-evidence.json) for the tested artifact,
seeds, commands, persisted start geometry, map checks and limitations. Test-only
loader classes are packaged separately, never in the player artifact.

The committed Python suite passes **121 tests**. Production Java checks pass
**198,920 distribution assertions** across 30 synthetic seeds, **648 gameplay
assertions**, **41 static mixin contracts** and the existing **755 worldgen
assertions**. Two independently rebuilt player JARs are byte-identical, SHA-256
`1d944ec074be0fe146069533f38ac3bb5e46c68576f0e3b135bcc16785b067f7`.

Native production-loader evidence uses three fixed seeds, ordinary 60,000 ms
watchdogs, exact saved natural-start geometry and real map storage/codecs:

| Seed | Shared initial spawn X/Z | Unique Colossus X/Z | Repeatable search |
| --- | --- | --- | --- |
| 731204 | -656 / 112 | 96136 / 48504 | Natural Obelisk at -11048 / -27911.5; exact saved half-block center |
| -48291736 | 0 / 0 | 5320 / 48040 | No confirmed repeatable site within 100,000 blocks |
| 20260913 | -816 / -32 | -57832 / 72808 | No confirmed repeatable site within 100,000 blocks |

These empty repeatable searches are actual observations, not hidden failures or
reasons to reroll/loosen the accepted terrain rules. Materialized rarity and
survival travel effort still need balancing evidence before a gameplay release.
The preferred unique-search annulus is exceeded in two seeds without inventing a
destination. All three targets survive restart and moving shared spawn; map copies
retain their origin/map IDs. Seed 731204 also resumes a deliberately interrupted
pending search. Unchanged datapack reload passes in all three worlds.

A separate world with `max-world-size=10000` exhausts the finite allowed domain:
the unavailable state persists over restart and creates no fake map, target or
natural Colossus. Local logs, command timings, slowest terrain queries and known
startup/save/reload lag warnings are retained in the JSON evidence. No client or
general performance acceptance is inferred from these runs.

Reproduce the automated checks with a JDK 25 and prepared verified dependencies:

```powershell
python tools/test_distribution.py --java-home "$env:JAVA_HOME"
python tools/test_gameplay.py --java-home "$env:JAVA_HOME"
python tools/test_worldgen_java.py
python -m unittest discover -s tests -v
python tools/build.py --skip-generation --output build/distribution-artifacts --java-home "$env:JAVA_HOME"
python tools/test_distribution_server.py --accept-eula --java "$env:JAVA_HOME/bin/java.exe" --artifact build/distribution-artifacts/relics-0.1.0-alpha.5.0-dev+mc26.2.jar --interrupt
```

The pure planner tests include 30 predetermined **synthetic-terrain** seeds over
120,000 by 120,000 blocks. They prove deterministic acceptance and spacing, not
actual biome frequencies or survival travel balance. Real runtime checks are
isolated production-loader worlds with normal watchdog settings, saved natural
starts and real server map codecs/storage. They are not connected-client visual,
multiplayer, full 30-seed native terrain or terrain-mod compatibility acceptance.

Compatibility validation here preserves the Fabric 1.21.1 preparation path.
Uncommitted NeoForge work and its separate compatibility gate are outside this
change's test/release scope; its files and historical artifacts are preserved.

API references: [Fabric 26.2 events](https://docs.fabricmc.net/develop/events/),
[Lithostitched structure types](https://github.com/Apollounknowndev/lithostitched/wiki/Structure-Types).
Exact method descriptors and behavior were also checked against the pinned local
26.2 server, Fabric 0.161.0 and Lithostitched 1.8.0 bytecode.
