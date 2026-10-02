# Changelog

## Unreleased — in-game review and demos

- Record per-relic V4 revision plans from the V3 in-game review; keep current
  models and build selection unchanged.
- Add three original Colossus V3 shader screenshots in a per-relic demo gallery,
  linked from the repository README and separated from Blender previews.
- Add normal-terrain preview-world preparation tooling and document the natural
  inspection world, viewpoints and remaining acceptance limits. Local saves,
  runtime logs and profile backups remain excluded from version control.

## 0.1.0-alpha.3 — V3 visual integration

- Select checked-in Colossus v3, Obelisk v3 and Titan Skull v3 exports in the
  default mod build, byte-for-byte, preserving source DataVersion for game migration.
- Add Titan Skull natural worldgen, biome tags, density presets and disable support.
- Update burial offsets, footprint grids and height limits for the large V3 models.
- Center natural templates on a replaceable named jigsaw so all parts stay within
  the engine's structure-reference range; place the Skull after terrain features
  to protect its authored hill. Keep raw manual templates and design exports intact.
- Expand integration tests and isolated server checks to all three structures;
  add a flat-world showcase mode with saved-block verification.
- Leave planned gameplay, final interiors and existing worlds unchanged.

See [V3 integration](docs/technical/V3_INTEGRATION.md) for contracts and viewing commands.

## Unreleased — asset pipeline and documentation

- Record visual acceptance of Obelisk V4.2 and all four Titan Skull V4 variants.
  Prioritize the remaining relic designs before V5 interior architecture.

- Record user visual acceptance of Colossus V4.1.
- Add Obelisk V4.2 with warmer ochre/clay sides, same-material fracture faces
  and two actual missing edge chunks. Preserve previous versions and verify
  that the notches survive export without contrasting replacement blocks.

- Added separate Colossus V4.1 frame export: supinated palm-up right hand with
  upward-curled fingers, preserving all 434 non-hand V4 meshes. Included a
  higher-ground inspection view and anatomical/export checks.
- Added separate Obelisk V4.1 export: consistent sandstone facets instead of
  contrasting patches, three branching surface cracks and four larger edge
  spalls. Preserved V4 scenery and verified open cracks over a solid core.

- Added four Titan Skull V4 exports (meadow, dry earth, sand, rock), preserving
  all 62 anatomy meshes while replacing the continuous hill with interrupted,
  tapered deposits and a lighter fossil palette. Reduced terrain by 52.44%.
- Added Obelisk V4 with restrained material weathering, four shallow edge chips,
  asymmetric sand and three foundation fragments; retained height, antiprism
  geometry, rotated crown and solid core. Both relics await visual acceptance.
- Added semantic terrain material remapping, supported sand/gravel and exposed
  grass rules, source/export validation, and V4 variant/comparison reviews.

- Added Colossus V4 open/frame export studies: asymmetrically damaged rear armour,
  a raised anatomically right hand, and two alternatives for the plain chest piston.
  Preserved 397 V3 source meshes and its body scale; added NBT detail comparisons,
  hand/rear/cavity checks, and a chest-only A/B difference check. Build selection
  remains V3. The user selected B / open machine frame on October 2, 2026;
  A remains available for comparison, and integration is pending.

- Archived the original Colossus concept under `relics/colossus/archive/first-concept/`
  as the basis for a second, smaller Colossus. Preserved models and exports and
  updated reproduction and size-comparison paths.

- Group each relic's design documents, asset configs, Blender/export files, and
  gameplay decisions under `relics/<relic>/`. Separate shared project, technical,
  and testing documentation under `docs/`; keep mod sources and tools separate.
  Update pipeline paths, asset provenance paths, ignore rules, and documentation
  links without changing geometry or the playable alpha. Add layout/link checks.

- Include generated review sheets, editable source Blender models, whole design
  NBTs, schematics, design/converter metadata, and verification records in version
  control so asset results can be viewed, edited, and downloaded without rebuilding
  the pipeline.

- Added Titan Skull v3 with nine partly buried vertebrae, two spinal fractures,
  loose fragments, and an extended solid hill. Preserved the v2 skull scale and
  added actual-NBT rear/detail views and burial/fracture checks.

- Added Titan Skull v2 at Colossus-head scale: approximately 76 blocks including
  crown, about 20% taller than the measured helmet shell. Added a solid exported
  moss/soil/stone mound, complete rear presentation, actual-NBT head comparison,
  and terrain-solidness/posterior-wall checks.

- Added Titan Skull v1 after the opening of *D.E.A.D.*: organic crown, hollow
  cranial vault, real eye/nose openings, long open jaw, teeth, and lateral spurs.
  Added its Blender/OBJ/schematic/NBT pipeline, green-hills presentation, cutaway,
  scale comparison, and exported cavity checks. Game integration remains pending.

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

These are asset-development changes. The new Blender assets are not yet selected by the mod build or natural world generation. Alpha 2 remains the current playable build. Selected asset deliverables are tracked; intermediate files and local reference media remain excluded from Git.

## 0.1.0-alpha.2

- Added connected cracks, deeper edge damage, sand drifts, and base debris to the Obelisk.
- Added a broken helmet, exposed chest supports, a damaged chest ring, and notches in the detached Colossus arm.
- Concentrated denser moss and leaves on one side, with moss traces on vertical surfaces.
- Moved the approach 14 blocks inward. The short, irregularly paved entrance is edged with soil and fallen plates; a three-block-wide route to the machine room stays clear.
- Made the test server select the current project-version artifact by default, preventing accidental tests of retained older JARs.

New shapes appear only in newly generated areas. Existing relics are not rebuilt. Dependencies, structure IDs, and distribution are unchanged. See the [Alpha 2 test report](docs/testing/ALPHA_2_TEST_REPORT.md).

## 0.1.0-alpha.1

First implemented alpha for Minecraft 26.2 with Fabric.

- Automatically generated an Obelisk and a Colossus with an arm and interior.
- Added deterministic NBT exports, whole templates, optional tiles, and checksum manifests.
- Added natural placement through Lithostitched biome, height, and grid conditions.
- Added optional biome mappings for Terralith and Biomes O' Plenty.
- Added generated settings datapacks for density profiles and disabled relic types.
- Added a reproducible data-only Fabric build without custom Java classes.
- Added geometry previews, tests, and an isolated test-server workflow.

This alpha tests generation and integration. Visual design, terrain transitions, and density require further playtesting. See the [historical Alpha 1 test report](docs/testing/ALPHA_TEST_REPORT.md) for checks actually performed.
