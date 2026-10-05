# Alpha 4.2 — terrain contact and relic separation

October 5, 2026. The user requested the latest models in Minecraft and chose to
correct natural placement before updating the test profile. Alpha 4.1 remains a
failed placement baseline; its exports and evidence are preserved.

## Unchanged model selection

Small Colossus **V5**, World Tree **V3**, Ruined Tower **V3**, Colossus V4.1
materials B, Obelisk V4.2, crowned Skull V4 in four biome palettes and Skull 2 V1.
The ten manual templates remain byte-identical to their source exports, including
DataVersion 3105. No artistic revisions, interiors, gameplay or old-chunk edits.

## Why static foundations were insufficient

Alpha 4.1 extended near-ground earth columns to a fixed depth and added an
eight-block tapered toe. Its 25 height samples can miss a ravine, small pool or
cavity between samples. A deeper fixed skirt cannot guarantee contact with real
terrain. Raising the grid to 81 samples triggered a locator watchdog.

Alpha 4.2 keeps the 25-point early site filter and the static tapered foundation.
A short-circuiting `relics:all_grid` checks exactly the same 25 positions but stops
at the first failure instead of evaluating the rest of an already-rejected site.
The sampled solid-floor minimum is 63 rather than 64; `relics:dry_land` requires
the actual base surface and solid-floor heights to agree. This admits dry coastal
ground at the real sea-level edge while rejecting sampled water, including high
inland pools that the earlier fixed minimum could miss. Biome, slope and ceiling
checks still apply. The old rock regression site failed only its coastal Y63
sample, not a water surface or an excessive slope.

A small `relics:terrain_support` structure processor then examines the actual
blocks **only in the current placement chunk**. Below each lowest near-ground
earth cell it extends dirt, stable sandstone/red sandstone or stone through
air, water and replaceable vegetation until it reaches an existing solid or
protected block, a planned model cell, the placement box or the dimension floor.
Native falling sand/gravel is replaced with stable fill rather than treated as
a support that can subsequently fall into a cavity.
It never reads neighbouring chunks, rewrites source cells or fills unrelated
void columns. High decorative moss does not start new pillars. Dynamic extension
is beneath the declared template; it does not change the template's burial,
rotation, bounding box, ceiling checks or eight-chunk horizontal reference limit.

The policy is `near-ground-soil-columns-v4-protected-runtime-contact`, with a matching
per-template processor list and ground offset recorded in the packaged manifest.
This is placement infrastructure, not a game-tick, excavation or reward system.

## Late features must not overwrite placed relics

The first complete terrain run found every variant, with zero unsupported
columns and no overlaps, but neighbouring chunk decoration still wrote ores,
stone blobs, fossils and lava into previously placed base cells. The rock Skull
exceeded the old one-percent allowance. That failed report is retained; the
allowance was not raised or used to declare strict success.

New natural placements record their exact non-air model/support cells as sparse
4096-bit section masks in a persistent Fabric chunk attachment,
`relics:placed_cells`. Unspecified cells, rooms and the surrounding landscape are
not masked. Small Minecraft-26.2 mixins guard world-generation block writes and
ore's direct section-write eligibility; own relic template placement is scoped
with exception-safe thread-local state. Same-block state updates (including leaf
distance) remain allowed. Masks survive proto-chunk conversion and save reloads.

Only `WorldGenRegion` writes are guarded: players can still freely mine/build
these vanilla blocks, with no tick handlers or ongoing repairs. Existing chunks
receive no retroactive masks or changes. Other mods that bypass both write paths
remain outside this acceptance scope; unrelated structure compatibility still
needs separate testing.

## Preventing relic/relic overlap

`relics:separated` wraps the existing terrain condition. Each family reserves the
nearby random-spread candidate sites of earlier families in catalog order:
Colossus, Obelisk, crowned Skull, Small Colossus, Tree, Tower, Skull 2.

The clearance radius includes both rotation-independent padded footprints and
adversarial start-chunk offsets. Candidate lookup uses the world's actual
structure-set spacing, salts and seed, including negative coordinates. It needs
no terrain generation or recursive structure lookup. One-way priority avoids
cycles; an empty disabled set releases its reservation. The four crowned-Skull
palettes still share one set. Reservations are deliberately conservative: an
unsuitable higher-priority candidate can still suppress a nearby lower-priority
candidate. Density presets remain candidate budgets, not guaranteed find rates.
This does **not** prevent overlap with vanilla or unrelated mod structures.
Same-family candidates use a lexicographic chunk priority, never excluding the
current candidate itself. This also prevents self-overlap under frequent or
older/custom density packs; normal and rare presets already have larger spacing.

## Build and verification

The gap in existing data-only placement facilities requires small Java
components and three scoped mixins in `src/main/java/de/relics/`. Minecraft 26.2 ships named classes, so
JDK **25** compiles them directly without Gradle or remapping. Python packaging
still has fixed archive metadata and embeds only checksum-verified current
classes. Stale source/class manifests are rejected.

With local Minecraft/Fabric/Lithostitched caches available:

```shell
python tools/build.py --java-home <JDK-25-directory>
python -m unittest discover -s tests -v
python tools/test_worldgen_java.py
python tools/smoke_server.py --accept-eula --quiet --showcase
python tools/smoke_server.py --accept-eula --quiet --command-timeout 300
```

`JAVA_HOME` can replace `--java-home`. For a clean checkout, explicit
`python tools/setup_worldgen_build.py --accept-downloads` prepares a separate,
checksum-verified compile cache from official Minecraft/Fabric downloads and the
pinned Lithostitched/Fabric API releases and loader libraries. Nothing is installed into a user profile. CI uses
this portable setup; ordinary builds do not automatically download dependencies.

The saved-world verifier reports every unsupported foundation column and
horizontal relic overlap, and verifies the saved protection bit for every
non-air template cell. None can use the installer's minor-feature-edit
allowance. Every template/variant must still be complete and verified before
installation. A different locator origin is recorded explicitly by
`--locate-from X Z`; this does not manually place a natural relic.
The terrain-copy tool reloads the masks and tests removing/replacing one actual
protected art cell through normal server-level commands, restoring its exact
state before the final saved-block comparison. Existing saves are never edited.

Runtime acceptance and installation status belong to the
[Alpha 4.2 test report](../testing/ALPHA_4_2_TEST_REPORT.md), not the algorithm
description or synthetic tests alone.
