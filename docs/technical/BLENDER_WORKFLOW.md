# From Blender to Minecraft relics

Updated: October 2, 2026.

## Pipeline and current status

**Blender → OBJ → ObjToSchematic 1.0 → Sponge `.schem` → Java `.nbt`** is implemented.
Alpha 3 selects the three V3 exports through `tools/integrate_v3.py`; see
[V3 integration](V3_INTEGRATION.md). **Colossus V4 B / open machine frame is the
selected design**, awaiting later integration; A is retained for comparison.
Titan Skull V4 now has four ground palettes, and Obelisk V4 has restrained
weathering and foundation scatter; both await visual acceptance.
The subsequent [Colossus V4.1](../../relics/colossus/docs/COLOSSUS_V4_1.md) and
[Obelisk V4.1](../../relics/obelisk/docs/OBELISK_V4_1.md) revisions correct the
hand pose and surface contrast. Separate generators load the published V4 sources.
Colossus V4.1 is now visually accepted. [Obelisk V4.2](../../relics/obelisk/docs/OBELISK_V4_2.md)
warms the palette and adds missing chunks without special crack-lining blocks.

We use the free, open-source **ObjToSchematic 1.0** locally. VoxelVision is no
longer required. The current 2.0 web product and its Pro features are not needed.

The pipeline was run with **Blender 5.2.2**, **Node 24.16.0**, and ObjToSchematic
commit `b611b52c7a87cad99127908598bab019fe9e7c3f`.

| Asset | Config under `relics/<relic>/design/` | Dimensions X/Y/Z | Blocks | Block types | Tiles |
| --- | --- | --- | --- | --- | --- |
| Archived first Blender experiment | `../archive/first-concept/colossus-ots.json` | 99 × 66 × 71 | 26,169 | 9 | 19 |
| [Colossus v2](../../relics/colossus/docs/COLOSSUS_V2.md) | `colossus-v2.json` | 181 × 160 × 227 | 182,734 | 11 | 100 |
| [Colossus v3](../../relics/colossus/docs/COLOSSUS_V3.md) | `colossus-v3.json` | 181 × 209 × 227 | 221,221 | 11 | 124 |
| [Colossus V4 A: open](../../relics/colossus/docs/COLOSSUS_V4_EXPORTS.md) | `colossus-v4-open.json` | 181 × 209 × 223 | 221,452 | 11 | 119 |
| [Colossus V4 B: frame](../../relics/colossus/docs/COLOSSUS_V4_EXPORTS.md) | `colossus-v4-frame.json` | 181 × 209 × 223 | 222,621 | 11 | 119 |
| [Obelisk v2](../../relics/obelisk/docs/OBELISK_V2.md) | `obelisk-v2.json` | 23 × 209 × 19 | 90,497 | 6 | 7 |
| [Obelisk v3](../../relics/obelisk/docs/OBELISK_V3.md) | `obelisk-v3.json` | 25 × 185 × 25 | 93,153 | 4 | 6 |
| [Titan Skull v1](../../relics/titan-skull/docs/TITAN_SKULL_V1.md) | `titan-skull-v1.json` | 185 × 203 × 103 | 103,943 | 4 | 98 |
| [Titan Skull v2](../../relics/titan-skull/docs/TITAN_SKULL_V2.md) | `titan-skull-v2.json` | 117 × 80 × 105 | 149,894 | 7 | 22 |
| [Titan Skull v3](../../relics/titan-skull/docs/TITAN_SKULL_V3.md) | `titan-skull-v3.json` | 121 × 79 × 203 | 264,355 | 7 | 37 |
| [Titan Skull V4](../../relics/titan-skull/docs/TITAN_SKULL_V4_EXPORTS.md) | `titan-skull-v4-{meadow,dry,sand,rock}.json` | 117 × 79 × 179 | 136,569 each | 7 / 7 / 6 / 6 | 31 |
| [Obelisk V4](../../relics/obelisk/docs/OBELISK_V4_EXPORTS.md) | `obelisk-v4.json` | 59 × 185 × 60 | 95,038 | 6 | 24 |
| [Colossus V4.1](../../relics/colossus/docs/COLOSSUS_V4_1.md) | `colossus-v4-1-frame.json` | 181 × 209 × 235 | 223,161 | 11 | 127 |
| [Obelisk V4.1](../../relics/obelisk/docs/OBELISK_V4_1.md) | `obelisk-v4-1.json` | 59 × 185 × 60 | 94,593 | 5 | 24 |
| [Obelisk V4.2](../../relics/obelisk/docs/OBELISK_V4_2.md) | `obelisk-v4-2.json` | 59 × 185 × 60 | 94,422 | 4 | 24 |

Colossus v2 follows the original reference; v3 adds the buried abdomen and torn
hip while keeping almost the same above-ground scale. Obelisk v2 follows *Painted
Desert*, with a solid core and a 32-block buried foot. All dimensions are export
bounds, including the detached arm where applicable.

Obelisk v3 corrects the stele to a tapered square antiprism based on the supplied
diagrams and reduces burial to eight blocks. Its scale comparison uses the v2 NBT.

Titan Skull v1 follows the opening of *D.E.A.D.* with an organic crown, open jaw,
and hollow cranial vault. It uses surface voxelization without solid fill, and
has a separate green-hills presentation and actual-block cutaway. Its asset page
provides generation commands; its scale comparison requires the Colossus v3 NBT.

Titan Skull v2 scales the skull to approximately 76 blocks and exports a solid
local mound with it. Its generator requires the Colossus v3 source for a measured
head-size reference; comparisons also require that NBT. The mound uses dense
interior slices rather than global filling, preserving the skull's open cavities.
Its main review shows the complete rear instead of a cutaway.

Titan Skull v3 adds nine partly buried vertebrae, two open fractures, and an
extended exported hill at the same skull scale. Its review includes a complete
rear overview and a cropped spine detail; see its asset page for commands.

Previews render the actual converted NBT with Minecraft textures in Blender.
They are not in-game evidence.

V4 ground materials use distinct atlas proxies during voxelization, then exact
state remapping before schematic export (`tools/material_proxy.cjs`). This keeps
bone materials independent and supports grass absent from the legacy atlas.
Covered grass becomes dirt; unsupported sand/gravel becomes stable terrain.
The grass preview is an explicitly approximate dirt/moss composite with tint;
the actual export uses the native grass block. `node --test tests/*.test.cjs`
checks the remapping and sealed-volume fill utilities.

## 1. Set up local tools

Install Blender, Git, Node.js with npm, and Python 3.11 or newer. Pillow is used
to assemble review sheets (`python -m pip install Pillow`). Run all commands from
the repository root. PowerShell examples:

```powershell
git clone --branch ots-1.0 https://github.com/LucasDower/ObjToSchematic.git .work/ObjToSchematic
git -C .work/ObjToSchematic checkout b611b52c7a87cad99127908598bab019fe9e7c3f
npm.cmd --prefix .work/ObjToSchematic install --no-audit --no-fund
```

Upstream [ObjToSchematic](https://github.com/LucasDower/ObjToSchematic) is licensed
under BSD-3-Clause. Keep its source and license in `.work/`; neither it nor its
dependencies are packaged in the mod JAR. The legacy branch no longer receives
regular updates. Its lockfile needs an `fsevents` addition with the tested npm,
which is why the command uses `install` rather than `ci`. Each project config
records the checked upstream revision.

The upstream headless entry point does not await its now-asynchronous import or
write the export result to disk. `tools/obj_to_schem.cjs` directly uses the upstream
importer, voxelizer, and exporter, with Node loaders for Webpack resources.
No upstream source changes are required.

## 2. Generate, convert, and preview an asset

For the current Colossus v3:

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
& $blender --background --python-exit-code 1 --python tools/create_colossus_v3.py
node tools/obj_to_schem.cjs relics/colossus/design/colossus-v3.json
python tools/schem_to_nbt.py relics/colossus/design/generated/colossus-v3/colossus-v3.schem relics/colossus/design/generated/colossus-v3/colossus-v3.nbt --air omit --tile-size 32
& $blender --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config relics/colossus/design/colossus-v3.json
python tools/inspect_ots_result.py --config relics/colossus/design/colossus-v3.json
```

[Colossus v2](../../relics/colossus/docs/COLOSSUS_V2.md), [Obelisk v2](../../relics/obelisk/docs/OBELISK_V2.md), and the current
[Obelisk v3](../../relics/obelisk/docs/OBELISK_V3.md) have complete commands on their asset pages.
Full rendering can take more than two minutes. Optional
renderer flags include `--source-only`, `--blocks-only`, `--landscape-only`, and
`--presentation-only`; the last renders the landscape and scale comparison.

The [archived original experiment](../../relics/colossus/archive/first-concept/)
is preserved as the basis for a second, smaller Colossus and remains reproducible:

```powershell
& $blender --background --python-exit-code 1 --python tools/create_blender_colossus.py
node tools/obj_to_schem.cjs relics/colossus/archive/first-concept/colossus-ots.json
python tools/schem_to_nbt.py relics/colossus/archive/first-concept/generated/colossus.schem relics/colossus/archive/first-concept/generated/colossus.nbt --air omit --tile-size 32
& $blender --background --python-exit-code 1 --python tools/render_ots_preview.py
python tools/inspect_ots_result.py
```

### Output files

Versioned assets write to `relics/<relic>/design/generated/<asset>/`; the original experiment
uses `relics/colossus/archive/first-concept/generated/` with the stem `colossus`.

| Output | Purpose |
| --- | --- |
| `<asset>-source.blend` | Editable Blender model |
| `<asset>.obj`, `<asset>.mtl` | Triangulated geometry and exported materials |
| `<asset>.schem` | Actual ObjToSchematic Sponge v2 output |
| `<asset>.ots.json` | Upstream revision, settings, counts, and SHA-256 hashes |
| `<asset>.nbt`, `<asset>.manifest.json` | Whole Java template and conversion metadata |
| `<asset>_tiles/` | Nonempty rigid tiles, at most 32 blocks per edge |
| `<asset>-blocks.blend` | NBT surface mesh with packed texture atlas |
| `01-blender-source.png` | Source model with simple material colors |
| `02-blocks-front.png` through `04-blocks-back.png` | Actual NBT block views |
| `<asset>-review.png` | Labeled overview |
| `verification.json` | Block-exact schematic/NBT/tile comparison |

Additional landscape, reference, scale, and cutaway views are listed on each asset
page. Reference sheets require the local image named by `reference_frame`; that
media is not included in a fresh checkout. The inspector skips reference-sheet
creation when the image is unavailable. Export validation still works with
`--check-only`.

Scale comparisons also need their earlier model locally: the Colossus views use
`relics/colossus/archive/first-concept/generated/colossus.nbt` from the original experiment; Obelisk v2 uses
`src/main/resources/data/relics/structure/obelisk.nbt`, generated by
`python tools/build.py`. Generate the relevant baseline before rendering to obtain
`06-size-comparison.png`. The renderer skips that comparison if its baseline is absent.

Large staging planes, figures, and illustrative landscapes are not exported.
Small earth features modeled into the asset itself are included. Lighting and
textures come from Blender and a legacy atlas.

Rerunning generators overwrites matching generated outputs. Before manual edits,
copy the `.blend` to a separate source location, such as `relics/<relic>/design/blender/`, and
use your own OBJ path/config. Scripts and JSON configs are the reproducible sources.

### Published asset files

Git includes these files directly inside `relics/<relic>/design/generated/<asset>/`:

The same publication policy applies to `relics/<relic>/archive/<concept>/generated/`.

| File pattern | Purpose |
| --- | --- |
| `*review.png` | Review sheets, including reference and underground comparisons |
| `*-source.blend` | Editable source model, ready to open in Blender |
| `*.nbt` | Whole Java structure template |
| `*.schem` | Sponge schematic for compatible editing and placement tools |
| `*.design.json` | Design measurements, scale, ground level, and geometry metadata |
| `*.ots.json` | Converter version, settings, palette, and export hashes |
| `verification.json` | Recorded export checks and checksums |

Keep these deliverables up to date when regenerating an asset so collaborators
can inspect, edit, or download the result without rebuilding the entire pipeline.
Verification records describe checks performed on the generated outputs; checks
requiring ignored OBJ files or tiles need those files regenerated locally.

Intermediate OBJ/MTL files, render-scene `.blend` files, `.blend1` backups, individual
renders, nested tile folders, and their `*.manifest.json` conversion manifests
remain ignored. Tiles and manifests can be rebuilt with the documented conversion
commands. The alpha build's generated structure directory is also ignored;
published design NBTs are separate from build inputs.

## 3. Models, materials, and coordinates

- Generators use Minecraft XYZ, facing **−Z**. Blender coordinates are `(X, −Z, Y)`;
  OBJ export uses Forward `NEGATIVE_Z` and Up `Y`.
- Export triangulated OBJ. Keep associated parts, especially the arm and torso,
  in the same export and coordinate system.
- Configured height scales the entire model. Adding deeper geometry changes that
  scale unless the export height is adjusted. Read actual bounds from the manifest.
- The CLI supports **named, flat-color OBJ materials**. Configs map names to atlas
  blocks; their average colors drive voxelization. OTS then assigns blocks from
  the allowed palette with no dithering, color resolution 255, and first-surface
  overlap handling. This is not a general textured-MTL import pipeline.
- Unknown materials or blocks absent from the atlas fail explicitly. Palettes are
  asset-specific: the reference Colossus uses copper, terracotta, dark joints,
  and vegetation; the Obelisk uses terracotta and sandstone.
- The legacy atlas lacks `waxed_weathered_cut_copper`. Review copper aging and
  explicitly migrate to suitable waxed states before game use if colors must stay fixed.

The BVH-ray voxelizer rasterizes **surfaces**. Even a solid Blender cube initially
becomes a block shell. Colossus wall thickness, breaks, and interior space need
separate validation. The adapter does not generate stairs or slabs.

### Optional solid fill

`fill_enclosed` names a material in the config's `materials` map. A six-connected
exterior flood fill identifies sealed empty cells and fills them before block
assignment. Obelisk v2/v3 use sandstone through `"fill_enclosed": "core"`.
Colossus configs do not enable this option. The flood-fill grid is capped at
32 million cells. See [Obelisk v3](../../relics/obelisk/docs/OBELISK_V3.md) for core, rotated-crown, and
shallow-burial verification; [v2](../../relics/obelisk/docs/OBELISK_V2.md) records the earlier design.

## 4. Air policy and NBT conversion

The converter independently accepts Sponge v2/v3, gzip-compressed or uncompressed,
without extra Python packages:

```powershell
python tools/schem_to_nbt.py model.schem relics/colossus/design/imported/model.nbt --air omit
```

| Option / block | Effect |
| --- | --- |
| `--air omit` | Skip air; retain terrain at those positions, including rooms |
| `--air keep` | Preserve all air; exterior air inside the export box also clears terrain |
| `minecraft:structure_void` | Always omit; preserve existing terrain |

The air option is mandatory. Neither surface voxelization nor conversion defines
which room air must clear terrain. Solid filling is not an interior-air policy.
A clear room in an empty-stage render therefore does not prove correct burial.

Block states are preserved without rotation. Schematic offsets are recorded in
the manifest rather than added to coordinates. Entities and block entities are
rejected explicitly. Large exports are loaded entirely into memory.

The legacy exporter writes **DataVersion 3105** (Minecraft 1.19), retained in NBT;
the target game 26.2 uses **4903**. No registry validation or version migration is
performed. Changing the number alone is not migration. Validate blocks and their
appearance in the target game before integration.

`--tile-size 32` adds tiles and relative origins (allowed edge lengths: 1–128).
Empty tiles are skipped and the whole template is retained. A manifest is not a
Minecraft placement definition; worldgen would need to place and rotate parts together.

## 5. Verification and integration

```powershell
python tools/inspect_ots_result.py --config relics/colossus/design/colossus-v3.json --check-only
python tools/inspect_ots_result.py --config relics/obelisk/design/obelisk-v3.json --check-only
python -m unittest discover -s tests -p test_schem_to_nbt.py -v
node --test tests/voxel_fill.test.cjs
```

Export checks compare all block coordinates/states, dimensions, data versions,
palettes, source/export hashes, and lossless tile reconstruction. Asset-specific
checks cover burial and the Obelisk core. Converter tests cover synthetic v2/v3
inputs, air policies, states, multi-byte indices, errors, and deterministic NBT.

`python tools/build.py` still regenerates the earlier `obelisk.nbt` and
`colossus.nbt`. Supporting these new assets requires explicit build source
selection and matching template-pool references, footprints, ground levels,
vertical offsets, biome/slope conditions, and any tile transforms. Existing alpha
placement settings are documented in [Worldgen](WORLDGEN.md).

Next acceptance work: finish wall thickness and interior air, check terrain joins,
then test the palette, four rotations, accessibility, chunk boundaries, and reloads
in Minecraft. Natural generation is a separate acceptance test.
