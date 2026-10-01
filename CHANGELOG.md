# Changelog

## Unreleased — asset pipeline and documentation

- Added Obelisk v3: a tapered square antiprism with eight triangular faces, a
  45-degree rotated square crown, and an 8-block buried foot. Added full-height
  ground-line inspection and exported base/crown geometry checks.
- Recorded the current v3 design pair and its above-ground height comparison:
  approximately 177 layers for the Obelisk versus 132 for the Colossus. Updated
  English documentation, reproduction commands, and integration status.

- Added a local Blender → OBJ → ObjToSchematic 1.0 → Sponge schematic → Java NBT pipeline, replacing the proposed VoxelVision dependency.
- Added reference-based Colossus v2 (181 × 160 × 227 blocks) and Colossus v3 (181 × 209 × 227), with an underground abdomen and torn hip in v3.
- Added Obelisk v2 (23 × 209 × 19), inspired by Josh White's *Painted Desert*, with a flat crown, mineral bands, and a 32-block buried foot.
- Added opt-in enclosed-volume filling, used for the Obelisk's solid sandstone core, with flood-fill tests.
- Added textured previews from actual exported NBT blocks, landscape presentations, scale comparisons, underground inspections, and block-exact export verification.
- Added a Sponge v2/v3 converter with explicit air handling, optional tiles, and conversion manifests.
- Updated project status and translated repository documentation into English.

These are asset-development changes. The new Blender assets are not yet selected by the mod build or natural world generation. Alpha 2 remains the current playable build. Generated files and local reference media are excluded from Git.

## 0.1.0-alpha.2

- Added connected cracks, deeper edge damage, sand drifts, and base debris to the Obelisk.
- Added a broken helmet, exposed chest supports, a damaged chest ring, and notches in the detached Colossus arm.
- Concentrated denser moss and leaves on one side, with moss traces on vertical surfaces.
- Moved the approach 14 blocks inward. The short, irregularly paved entrance is edged with soil and fallen plates; a three-block-wide route to the machine room stays clear.
- Made the test server select the current project-version artifact by default, preventing accidental tests of retained older JARs.

New shapes appear only in newly generated areas. Existing relics are not rebuilt. Dependencies, structure IDs, and distribution are unchanged. See the [Alpha 2 test report](docs/ALPHA_2_TEST_REPORT.md).

## 0.1.0-alpha.1

First implemented alpha for Minecraft 26.2 with Fabric.

- Automatically generated an Obelisk and a Colossus with an arm and interior.
- Added deterministic NBT exports, whole templates, optional tiles, and checksum manifests.
- Added natural placement through Lithostitched biome, height, and grid conditions.
- Added optional biome mappings for Terralith and Biomes O' Plenty.
- Added generated settings datapacks for density profiles and disabled relic types.
- Added a reproducible data-only Fabric build without custom Java classes.
- Added geometry previews, tests, and an isolated test-server workflow.

This alpha tests generation and integration. Visual design, terrain transitions, and density require further playtesting. See the [historical Alpha 1 test report](docs/ALPHA_TEST_REPORT.md) for checks actually performed.
