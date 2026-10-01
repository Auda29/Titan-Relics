# Obelisk v3 — tapered square antiprism

Updated: October 1, 2026.

## Shape correction

This revision follows the user's two antiprism diagrams alongside
[Josh White's Painted Desert](https://www.instagram.com/p/Da0NEq7kUAO/).
Unlike [v2](OBELISK_V2.md), it has **eight long planar triangular sides** between
two square caps. The top square is rotated **45 degrees** relative to the base
and its edge length is **67%** of the base edge. This is an elongated, tapered
square antiprism, not a regular equal-edge solid or a box with painted diagonals.

The base edge is 24 source units; the top edge is 16.08. The visible source height
remains 176 units. Quiet ochre, terracotta, and sandstone faces emphasize the
diagonal geometry. The source mesh has eight vertices, eight lateral triangles,
and two square caps; normals and closed manifold edges are checked during generation.

The revised design was visually approved from the previews. That approval covers
the design study; Minecraft placement and gameplay acceptance remain pending.

## Shallower burial

The foot now extends only **8 blocks below the nominal surface**, rather than
v2's 32. Total sampled height is **185 blocks**, with approximately 176 source
units visible above ground. The original v2 half-height-looking cutaway showed
only its lower 68 layers, not the whole 209-block structure. The new full-height
burial overview makes the actual proportion explicit.

The turquoise plane in `08-burial-overview.png` marks NBT Y8. The separate
`07-solid-foot-section.png` is deliberately a cropped lower-44-layer core section.
Illustrative terrain is level immediately around the foot, then blends into hills.
Terrain and markers are not exported.

## Height relative to Colossus v3

| Height measure | Obelisk v3 | Colossus v3 |
| --- | --- | --- |
| Total exported height | 185 blocks | 209 blocks |
| Below nominal ground | 8 layers | Approximately 77 layers |
| At/above nominal ground | 177 layers | Approximately 132 layers |

The Obelisk rises approximately **45 blocks (34%) higher above terrain**. The
Colossus remains taller overall but is buried more deeply. A taller, slender
stele alongside a broader, partially buried machine fits the intended visual
contrast; the separate references do not establish an exact relative scale.

The source's visible geometric span is 176 units; the voxel export includes both
end surfaces, producing 177 occupied height layers from NBT Y8 through Y184.

## Export

| Metric | Obelisk v3 |
| --- | --- |
| Dimensions X/Y/Z | **25 × 185 × 25 blocks** |
| Placed blocks | **93,153** |
| Used block types | **4** |
| Nonempty 32-block tiles | **6** |
| Interior cells added by solid fill | **79,343** |
| Nominal ground level | **NBT Y8** |
| Blocks below the surface | **4,972 (5.34%)** |

The sandstone core uses the existing opt-in enclosed-volume fill. Verification
checks source/export hashes, all schematic/NBT coordinates and states, palette,
bounds, lossless tile reconstruction, a continuous 7 × 185 × 7 central core,
square base corners, rotated crown tips, and shallow burial in the actual export.

## Reproduce

Set up the tools using [Blender workflow](BLENDER_WORKFLOW.md), then run:

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
& $blender --background --python-exit-code 1 --python tools/create_obelisk_v3.py
node tools/obj_to_schem.cjs design/obelisk-v3.json
python tools/schem_to_nbt.py design/generated/obelisk-v3/obelisk-v3.schem design/generated/obelisk-v3/obelisk-v3.nbt --air omit --tile-size 32
& $blender --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config design/obelisk-v3.json
python tools/inspect_ots_result.py --config design/obelisk-v3.json
```

Outputs are under `design/generated/obelisk-v3/`, including editable
`obelisk-v3-source.blend`, `.obj`, `.schem`, `.nbt`, manifests, and verification.
The landscape, core section, and full burial overview also have editable `.blend`
scenes. The size comparison requires the existing v2 NBT; the reference sheet
requires the configured local Instagram reference image.

These are Blender renders of the exported blocks. In-game validation and
build/worldgen integration remain pending. The legacy exporter still writes
DataVersion 3105, and the alpha build still uses its procedural Obelisk.
