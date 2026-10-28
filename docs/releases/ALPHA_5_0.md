# Relic Mod 0.1.0-alpha.5.0 — Minecraft 26.2 / Fabric

Alpha 5 adds natural relic encounters and finite rewards to the monumental
structures, with shared distribution and persistent exploration targets.

## Included

- One saved natural large Colossus per world. Expedition maps and asynchronous
  relic locating use the same terrain-valid targets.
- A hostile defense golem, native Trial Spawner/Vault phases and personal
  physical reward drops. The Vault consumes its key immediately and ejects
  the Machine Core separately.
- Machine Core processing with 256 operations, and a Salvage Magnet active in
  either selected hand. Wear counts each inserted item, including partial
  pickups. Maintenance recipes appear in the recipe book.
- Obelisk archaeology with Monolith armor-trim and expedition-map rewards.
  The revised trim follows native armor UVs and material palettes.
- Large Colossus V7, Small Colossus V11, Tower V10, Obelisk V6, World Tree V5
  and the corrected sword-bearing Skull 2. Chest sites have visible framing;
  the Small Colossus lower entry is shorter and Skull 2's isolated side chip is removed.
- World Tree Regeneration II and Resistance II in an 80-block sphere with a
  five-minute departure tail. Firefly bushes follow safe nearby ground.
- Bounded extra ordinary natural attempts for pigs, chickens, sheep and cows
  near registered Trees. Native habitat, player distance, collision and global/
  local caps apply. No refill timer or guaranteed herd.

## Requirements and installation

- Minecraft **26.2**, Java **25**, Fabric Loader **0.19.5 or newer**.
- Fabric API **0.161.0+26.2**.
- Lithostitched **1.8.0 for Fabric 26.2**.

Install `relics-0.1.0-alpha.5.0+mc26.2.jar` and matching dependencies in `mods/`,
replacing the previous Relic Mod JAR. Dependencies are not bundled. This release
is for Fabric 26.2; the separate 1.21.1 visual release remains available.

Use a **new world for all Alpha 5 structures and gameplay**. Existing worlds
keep their saved revision, even for further chunks. Old structures are not
automatically upgraded or refilled. Registered Tree effects update in existing
gameplay worlds. Back up saves before changing mod versions.

Use default distribution spacing. Legacy frequent/rare spacing datapacks and
unknown custom generators are not supported by the gameplay planner. Rare relic
searches run in the background and may lead to distant destinations.

## Validation and alpha limits

The release is checked from a separate Git export, including model/handoff
hashes, reproducible packaging, natural generation and save/restart behavior,
personal rewards, magnet accounting, Tree effects and native animal caps.
The user confirmed visual/functional tests and **two real Minecraft clients
with reconnect**, without problems. Automated multiplayer checks use simulated
server players and are reported separately.

This remains an alpha. Long-term Survival balance, arbitrary modpacks, shaders/
LOD renderers and hard process termination across all player/entity/journal saves
are not general compatibility or transaction guarantees.

See the [release report](../testing/ALPHA_5_RELEASE_20261028.md) for exact
checksums and evidence. No test fixtures or third-party JARs enter the player artifact.
