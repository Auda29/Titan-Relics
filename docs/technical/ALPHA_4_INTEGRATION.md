# Alpha 4 — current relic integration

The current [Alpha 4.2 terrain correction](ALPHA_4_2_TERRAIN.md) adds runtime
contact supports and non-overlap reservations while preserving the later models.

**Historical baseline:** the October 5 [Alpha 4.1 screenshot revision](../project/SCREENSHOT_REVISIONS_20261005.md)
selects Small Colossus V5, Tree V3 and Tower V3 and adds padded soil-column
foundations to natural templates. The tables and 25-point placement description
below describe the original Alpha 4 artifact, not Alpha 4.1.

October 4, 2026. This is a **visual integration**, not a gameplay release.
Model generation finished in the Structures thread before integration began.
Its uncommitted exports are preserved, not regenerated or overwritten.

## Selected assets

| Template ID (`relics:`) | Export | X × Y × Z | Blocks | Ground Y | Visible layers |
| --- | --- | --- | ---: | ---: | ---: |
| `colossus` | V4.1 materials B | 181 × 209 × 235 | 223,161 | 77 | 132 |
| `obelisk` | V4.2 | 59 × 185 × 60 | 94,422 | 8 | 177 |
| `titan_skull` | V4 meadow | 117 × 79 × 179 | 136,569 | 8 | 71 |
| `titan_skull_dry` | V4 dry | 117 × 79 × 179 | 136,569 | 8 | 71 |
| `titan_skull_sand` | V4 sand | 117 × 79 × 179 | 136,569 | 8 | 71 |
| `titan_skull_rock` | V4 rock | 117 × 79 × 179 | 136,569 | 8 | 71 |
| `small_colossus` | V4 | 113 × 84 × 103 | 215,766 | 9 | 75 |
| `world_tree` | V2 | 179 × 216 × 175 | 412,702 | 8 | 208 |
| `ruined_tower` | V2 | 111 × 232 × 93 | 317,633 | 12 | 220 |
| `titan_skull_2` | V1 | 105 × 144 × 107 | 85,224 | 12 | 132 |

Small Colossus V4, World Tree V2 and Ruined Tower V2 are **visual candidates**.
Including them for Minecraft review does not claim user artistic approval.
Rejected Small Colossus V2/V3, older models and the post-salvage simulation are
not selected. The intact accepted material-B Colossus is selected.

## Build contracts

- `tools/relic_catalog.py` pins source paths, hashes, dimensions, burial depth,
  family, visual-approval status, biome tags and provisional placement limits.
- `tools/integrate_relics.py` first validates **all ten** source exports against
  the pinned contract and their `verification.json`, then copies the manual
  templates **byte-for-byte**. Source DataVersion **3105** is preserved.
- Natural `_worldgen` templates add only a named center jigsaw at local Y0.
  It restores the original block/state, or becomes omitted `structure_void`.
  All occupied corners stay within Minecraft's eight-chunk reference radius
  in every rotation and at any anchor offset within the start chunk.
- Generated resources and `src/main/resources/relics.integration.json` are
  deterministic. The manifest is included in the JAR. `--skip-generation` checks
  their current hashes/contracts and rejects stale selection or modified assets.
- Only the twenty selected raw/natural NBT files are packaged; stale debug/tile
  exports in the local resource directory are not silently shipped.
- Missing NBT cells still **preserve native terrain**. No automatic excavation,
  interior redesign, loot, trial, map or per-world uniqueness system is added.

## Natural placement

All models use rigid whole templates and a late `top_layer_modification` stage.
Nominal surface placement follows the established `start_height = 1 - ground_y`
contract. Twenty-five grid samples check slope, land height and ocean/river
exclusion across a rotation-independent square footprint. Samples can still miss
small pools, structures or height changes between grid points.

Upper sampled floor bounds reserve at least eight blocks below the Overworld
ceiling. World Tree is limited to floor Y104, Ruined Tower to Y92; high ground is
rejected instead of cutting off their crowns. Obelisk is capped at Y135 and the
large Colossus at Y180. The other assets are capped at Y230 or their lower safe
height limit. These are placement restrictions, not changes to authored scale.

Crowned Skull variants are mutually exclusive:

- `titan_skull`: plains, sunflower plains, meadow and optional grassy mod biomes.
- `titan_skull_dry`: savanna and optional steppe/scrubland.
- `titan_skull_sand`: desert and explicitly listed optional dry/desert biomes.
- `titan_skull_rock`: windswept hills/gravelly hills, stony shore/peaks and optional
  rocky mountains, only where the same land/slope checks succeed. Coastal ocean
  samples and high/steep alpine sites are still rejected.

Meadow/dry/sand tags must match at every sampled point, rejecting sampled biome
boundaries instead of randomly choosing an incompatible surface. Rock is selected
by the start biome: its mineral deposits may cross a rocky-biome edge, while the
same all-site terrain checks still apply. Requiring a pure rocky biome over the
entire 180-block site yielded no natural match in two seeds. The four
variants share **one structure set and density budget**. Desert/rock mappings are
new provisional integration settings, not established modpack compatibility.

All seven relic families have independent structure sets, stable salts, density
presets and disable settings. Default spacing/separation in chunks:

| Family | Normal | Rare | Frequent |
| --- | --- | --- | --- |
| Obelisk | 64 / 32 | 96 / 48 | 32 / 16 |
| Large Colossus | 80 / 40 | 120 / 60 | 40 / 20 |
| Crowned Skull (all four variants) | 48 / 24 | 72 / 36 | 24 / 12 |
| Small Colossus | 48 / 24 | 72 / 36 | 24 / 12 |
| World Tree | 96 / 48 | 144 / 72 | 48 / 24 |
| Ruined Tower | 80 / 40 | 120 / 60 | 40 / 20 |
| Skull 2 | 64 / 32 | 96 / 48 | 32 / 16 |

These are provisional candidate rates, not measured discovery frequency or final
economy balance. Large-Colossus uniqueness remains unimplemented. Skull 2 has an
independent provisional rate; a shared budget for the broader skull/bone family
remains future design work.

## Inspection

```shell
python tools/build.py
python -m unittest discover -s tests -v
node --test tests/material_proxy.test.cjs tests/voxel_fill.test.cjs
python tools/smoke_server.py --accept-eula --showcase
python tools/smoke_server.py --accept-eula --command-timeout 300
```

The showcase places all ten templates on a Y64 flat surface, spaced by 384 blocks.
Its saved-world comparison checks **every exported block**, including soil and
vegetation. Persistent leaf `distance` is a computed neighbour value: the verifier
accepts a valid distance 1–7 while still requiring the same block and
`persistent=true`. Recalculated values are explicitly counted, not mismatches
hidden by excluding the tree. Manual placements and natural starts are distinguished in evidence.
Normal-terrain runs locate each structure, save the real rotated bounding box,
generate its full footprint and compare saved blocks against the **launched JAR**.
`--structure <id>` limits diagnostic runs; subset runs cannot qualify installation
as a fully tested build. Natural comparison explicitly counts its historical
soil/vegetation exclusions. Terrain-feature overwrites are not counted as a pass.

Commands in a fresh creative world:

```mcfunction
/locate structure #relics:relics
/locate structure #relics:titan_skull
/locate structure relics:small_colossus
/locate structure relics:world_tree
/locate structure relics:ruined_tower
/locate structure relics:titan_skull_2
```

`/locate structure relics:titan_skull` now targets the **meadow** structure only;
use the family tag for any crowned-Skull variant. Other original structure IDs
remain unchanged. Existing generated V3 structures are not replaced. Locators
can find an old site in an old world; use a new test world for current geometry.

For manual placement, use `/place template relics:<id> X Y Z`, where Y is the
desired surface level minus Ground Y from the table. Do not manually place the
derived `_worldgen` template; its anchor is meant for jigsaw worldgen.

Runtime results and installation status are recorded separately in
[the Alpha 4 test report](../testing/ALPHA_4_TEST_REPORT.md). Previous limitations
and V3 evidence remain in [the Alpha 3 report](../testing/ALPHA_3_TEST_REPORT.md).
