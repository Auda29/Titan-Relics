# Obelisk v2 — Painted Desert

Updated: October 1, 2026.

The later **[Obelisk v3](OBELISK_V3.md)** replaces the rectangular shaft with a
tapered square antiprism and shortens the buried foot to eight blocks. This page
records the retained v2 design.

## Reference and shape

The reference is [Painted Desert by Josh White](https://www.instagram.com/p/Da0NEq7kUAO/).
Both published paintings and the accompanying process animation were inspected.
Local reference images are stored under `.work/references/`.

Its key features are an extremely slender stele, a flat crown, nearly parallel
large faces, warm mineral colors, and strong contrast between the shaded main
face and bright side. Horizontal weathering is restrained; the base disappears
into layered desert hills.

The model uses a continuous, parallel-sided stone mass, **22 × 18 source units**
from foot to crown. A trial taper produced a conspicuous middle step in the block
grid, so parallel faces were chosen to preserve the quiet silhouette. Small edge
losses and restrained mineral bands add wear. Yellow terracotta, sandstone,
brown mineral traces, and a lighter exposed side form the palette. Landscape and
lighting are additional presentation elements.

## Dimensions and burial

| Metric | Obelisk v2 |
| --- | --- |
| Export dimensions X/Y/Z | **23 × 209 × 19 blocks** |
| Visible source height above ground | Approximately **176 blocks** |
| Buried foot | **32 blocks** |
| Placed blocks | **90,497** |
| Used block types | **6** |
| Nonempty 32-block tiles | **7** |
| Interior cells added by filling | **73,883** |
| Blocks below the nominal surface | **13,856** |

Scale is an artistic estimate. Neither a reliably measurable person nor known
aircraft dimensions are available in the artwork. Visible height to projected
width is approximately 7:1. The comparison preview shows the previous 70-block
Obelisk beside v2 at the same block scale. A two-block person appears in the landscape.

The entire stele, including its buried foot, is included in `.schem` and `.nbt`.
The hills, person, and turquoise surface marker are preview-only objects.

## Solid core

ObjToSchematic first voxelizes surfaces. `design/obelisk-v2.json` explicitly enables
`"fill_enclosed": "core"`. The local adapter fills sealed interior cells with the
core material's atlas color before assigning Minecraft blocks and writing `.schem`.
Here, `core` maps to sandstone.

The algorithm flood-fills exterior air through the six face-connected neighbors;
only unreachable interior cells become solid. Open chambers remain unfilled.
This option is intended for solid structures and is not enabled for the Colossus
models. It does not define or clear explorable room air for worldgen. Its working
grid is limited to 32 million cells.

The export check verifies a continuously occupied central **7 × 209 × 7-block**
prism. `07-solid-foot-section.png` shows a cutaway of the actual NBT with its core exposed.

## Generate and verify

Dependencies and setup: [Blender workflow](BLENDER_WORKFLOW.md).

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
& $blender --background --python-exit-code 1 --python tools/create_obelisk_v2.py
node tools/obj_to_schem.cjs design/obelisk-v2.json
python tools/schem_to_nbt.py design/generated/obelisk-v2/obelisk-v2.schem design/generated/obelisk-v2/obelisk-v2.nbt --air omit --tile-size 32
& $blender --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config design/obelisk-v2.json
python tools/inspect_ots_result.py --config design/obelisk-v2.json
node --test tests/voxel_fill.test.cjs
```

Important outputs under `design/generated/obelisk-v2/`:

- `obelisk-v2-source.blend`: editable Blender source.
- `obelisk-v2.obj`, `obelisk-v2.schem`, `obelisk-v2.nbt`: geometry and block exports.
- `obelisk-v2.design.json`, `obelisk-v2.ots.json`, `obelisk-v2.manifest.json`, `verification.json`: scale assumptions, settings, block counts, and hashes.
- `obelisk-v2-blocks.blend`: NBT surface mesh with the packed Minecraft atlas.
- `obelisk-v2-landscape.blend`: NBT and an illustrative desert landscape.
- `obelisk-v2-foot-section.blend`: actual block cutaway with solid core.
- `obelisk-v2-review.png`, `obelisk-v2-reference-review.png`: labeled overview sheets; the reference sheet requires the local reference image.
- `05-blocks-landscape.png`, `06-size-comparison.png`, `07-solid-foot-section.png`: landscape, scale comparison, and foot section.

Schematic/NBT agreement, palette, coordinates, bounds, tiles, and the solid core
were checked against the real export. Three Node tests cover separate sealed
chambers, negative coordinates, open chambers, and thin surfaces.

This remains an asset prototype with legacy DataVersion 3105. Build/worldgen
integration and in-game acceptance are pending. Its height and 32-block burial
require appropriate placement offsets and vertical-bound checks in the target world.
