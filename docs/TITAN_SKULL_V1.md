# Titan Skull v1 — crowned fossil among green hills

Updated: October 1, 2026.

The later **[Titan Skull v2](TITAN_SKULL_V2.md)** reduces the skull to approximately
Colossus-head scale and includes a solid local hill in the export. This page
records the original, much larger v1 study. Its section preview is intentionally
clipped; the complete v1 export includes the posterior wall.

## Reference and design

The source is the opening **0–5 seconds** of
[D.E.A.D. / remains of dead gods — The Archive In Between](https://www.instagram.com/reel/DXM3J4sgqJl/).
The video was downloaded locally and three opening frames were inspected. Local
reference media stays in `.work/references/` and is not distributed with the mod.

The opening shows a long, weathered skull with an organic crown, deep eye sockets,
a triangular nasal opening, a wide-open jaw, and a prominent backward-curving
lateral spur. Green hills and mist obscure its lowest portions. This asset follows
that particular head rather than later skeletal motifs in the reel.

| Reference feature | Asset interpretation |
| --- | --- |
| Rounded eroded cranial vault | Hollow, uneven organic shell with local fissures |
| Unequal crown projections | Seven tapered, bent bony outgrowths fused into the vault |
| Deep eyes and triangular nose | Actual geometric openings, not dark decorative inserts |
| Tall open mouth and long jaw edges | Connected oral cavity, exposed mandibular rails, sparse irregular teeth |
| Side spur and basal remnants | One tall curved spur, a shorter broken counterpart, partly buried bone remnants |
| Aged mineral surfaces | Dripstone, sandstone, tuff, and localized moss |

Anatomical pieces are fused with voxel remeshing and smoothed before OBJ export,
so the source reads as a continuous fossil rather than separate primitive joints.
The back, internal cavity layout, opposite spur, and buried underside are inferred
design additions. The asset contains no complete body or separate skeleton.

## Scale and export

| Metric | Titan Skull v1 |
| --- | --- |
| Overall dimensions X/Y/Z | **185 × 203 × 103 blocks** |
| Placed blocks | **103,943** |
| Used block types | **4** |
| Nonempty 32-block tiles | **98** |
| Nominal ground plane | **NBT Y ≈ 13** |
| Height at/above nominal ground | Approximately **190 layers**, including crown |
| Export DataVersion | **3105** |

This is an artistic scale estimate. The foreground traveler cannot directly
calibrate the distant skull. The size-comparison preview places the skull beside
Colossus v3 at the same block size and aligns their template bottoms; it is not
a comparison of their buried surface levels. A two-block traveler in the landscape
provides a separate scale cue.

The irregular lowest 13 layers are intended for burial. Terrain in the presentation
varies around that nominal plane. Hills and the scale figure are preview-only.
The crown, teeth, spurs, jaw, and small moss patches are part of the block export.

## Cavities and verification

The model contains a hollow cranial vault and oral chamber. No enclosed-volume
fill is enabled: ObjToSchematic voxelizes the inner and outer surfaces.
`--air omit` leaves those cavity positions absent from NBT. It does **not** clear
existing terrain from them when placed in a world.

The inspector checks source/export hashes, every schematic/NBT block coordinate
and state, palette counts, bounds, and lossless tile reconstruction. Skull-specific
checks confirm empty 3 × 3 × 3 samples at the eyes, nose, and mouth, plus a clear
5 × 5 inspection channel from the mouth toward the chamber. These checks establish
geometric openings, not a walkable route or completed in-game terrain clearing.

## Reproduce

Use the dependencies in [Blender workflow](BLENDER_WORKFLOW.md). From the repository root:

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
& $blender --background --python-exit-code 1 --python tools/create_titan_skull_v1.py
node tools/obj_to_schem.cjs design/titan-skull-v1.json
python tools/schem_to_nbt.py design/generated/titan-skull-v1/titan-skull-v1.schem design/generated/titan-skull-v1/titan-skull-v1.nbt --air omit --tile-size 32
& $blender --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config design/titan-skull-v1.json
python tools/inspect_ots_result.py --config design/titan-skull-v1.json
```

Outputs are in `design/generated/titan-skull-v1/`:

- `titan-skull-v1-source.blend`: editable fossil mesh and moss objects.
- `titan-skull-v1.obj`, `.mtl`, `.schem`, `.nbt`: source and conversion outputs.
- `titan-skull-v1.design.json`, `.ots.json`, `.manifest.json`, `verification.json`: design assumptions, settings, counts, hashes, and checks.
- `titan-skull-v1-blocks.blend`: actual NBT surface mesh with packed atlas.
- `titan-skull-v1-landscape.blend`, `05-blocks-landscape.png`: illustrative green valley.
- `titan-skull-v1-section.blend`, `07-skull-section.png`: actual NBT cutaway.
- `06-size-comparison.png`: comparison with Colossus v3; requires that NBT locally.
- `titan-skull-v1-review.png`: source and three block views.
- `titan-skull-v1-reference-review.png`: reference, landscape, section, and scale comparison; requires the configured local reference frame.

## Status

Asset-generation study only. The alpha build/worldgen still contains its earlier
Obelisk and Colossus. No skull structure ID, biome mapping, or natural placement
has been added. In-game palette validation, air clearing, accessible routes,
placement offsets, and terrain/height checks remain future integration work.
Blender previews are not Minecraft screenshots.
