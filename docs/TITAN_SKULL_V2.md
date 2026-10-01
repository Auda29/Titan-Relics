# Titan Skull v2 — Colossus-head scale and an exported mound

Updated: October 1, 2026.

[Titan Skull v3](TITAN_SKULL_V3.md) extends this design with a broken, partly
buried spine and a longer supporting hill, preserving the skull's source scale.

## Revision goal

The user imagines the Colossus as a plausible opponent of the living titan.
The skull should therefore be around the size of the Colossus's head, slightly
larger, rather than nearly the height of its entire torso assembly.

V2 retains the crowned fossil design from [v1](TITAN_SKULL_V1.md), reduces its
scale, and adds a **solid local hill to the actual block export**. The reference
remains the opening 0–5 seconds of
[D.E.A.D. — The Archive In Between](https://www.instagram.com/reel/DXM3J4sgqJl/).
The implied conflict is a design premise, not a new gameplay mechanic.

## Measured scale

The generator reads the saved Colossus v3 source, measures transformed vertices
of its round helmet shell, and applies that asset's recorded block scale. This
measurement excludes hoses, filters, vegetation, and the neck. The comparison
render includes the visible NBT head region with those accessories.

| Measure | Height |
| --- | --- |
| Colossus v3 helmet shell | **63.24 block units** |
| Titan Skull v2, including crown and basal bone remnants | **75.77 block units** |
| Relative height | **1.20×**, approximately 20% taller |
| Whole v2 template, including hill foundation | **80 block layers** |

The skull is approximately 37.3% of v1's geometric block height. Its width,
including side spurs, is about 69 blocks; the mound's footprint is larger.
Scale remains a chosen relationship between the creatures, not a measurement
established by the separate Instagram references.

## Complete rear and terrain

The apparently removed rear in the earlier review was the deliberately clipped
`07-skull-section.png` inspection view. V1's complete export already had a rounded
posterior wall. V2 presents the **full rear view**, with no clipping, in its main
reference sheet; no cutaway is generated for this version.

The exported mound rises behind the skull and around its lower sides. The forward
mouth channel is kept clear. It has an irregular footprint, a moss surface,
soil beneath, and a stone foundation extending to source Y−8. Moss is used as
the grassy surface because the pinned legacy atlas has no `grass_block` entry.
Small green deposits on the skull itself use green terracotta.

The local hill is included in the OBJ, schematic, and NBT. Only the more distant
landscape and the two-block traveler are presentation aids. The broad foundation
is intended to meet future terrain near NBT Y8, not to sit exposed on a flat slab.

### Solid terrain without filling the skull

The source includes a terrain heightfield and clipped horizontal interior slices
spaced 0.75 source units apart, less than the final voxel spacing. Surface
voxelization therefore writes the mound's interior as well as its outer surface.
No global enclosed-volume fill is enabled, so the skull cavities remain open.

As before, `--air omit` preserves existing world terrain at absent positions.
The generated mound leaves the mouth inspection channel clear, but placement
into an existing hill still needs a future explicit air-clearing policy.

## Verified export

| Metric | Titan Skull v2 |
| --- | --- |
| Overall X/Y/Z, including hill | **117 × 80 × 105 blocks** |
| Placed blocks | **149,894** |
| Terrain blocks: moss, dirt, stone | **136,988** |
| Remaining skull/vegetation blocks | **12,906** |
| Used block types | **7** |
| Nonempty 32-block tiles | **22** |
| Nominal surface | **NBT Y8** |
| DataVersion | **3105** |

Checks cover source/export hashes, all schematic/NBT coordinates and states,
palette counts, bounds, and lossless tile reconstruction. Additional checks verify:

- Empty 3 × 3 × 3 samples at eyes, nose, and mouth.
- A clear 5 × 5 mouth inspection channel.
- Three groups of 25 solid terrain columns from near the foundation to interior samples.
- Nine posterior-wall rays that must encounter bone material.
- A skull/helmet height ratio between 1.0 and 1.3.

These establish exported geometry, not completed in-game access or placement.

## Reproduce

Use [Blender workflow](BLENDER_WORKFLOW.md) to set up dependencies. First generate
the [Colossus v3](COLOSSUS_V3.md) source and NBT: v2 reads its source for measurement
and its NBT for comparisons. V1 skull output files are not required; v2 calls the
shared v1 geometry builder without writing its outputs.

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
& $blender --background --python-exit-code 1 --python tools/create_titan_skull_v2.py
node tools/obj_to_schem.cjs design/titan-skull-v2.json
python tools/schem_to_nbt.py design/generated/titan-skull-v2/titan-skull-v2.schem design/generated/titan-skull-v2/titan-skull-v2.nbt --air omit --tile-size 32
& $blender --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config design/titan-skull-v2.json
python tools/inspect_ots_result.py --config design/titan-skull-v2.json
```

Outputs are in `design/generated/titan-skull-v2/`, including editable source,
OBJ/MTL, schematic, NBT, tiles, and verification metadata.

- `04-blocks-back.png`: complete rear and actual exported hill.
- `05-blocks-landscape.png`: exported skull/mound in illustrative surroundings.
- `06-size-comparison.png`: whole skull/mound beside the complete Colossus v3.
- `08-head-comparison.png`: skull/mound beside a spatial crop of the actual
  Colossus head, at identical block scale and independently aligned base heights.
  The mound is retained so removing its materials does not expose artificial
  holes at skull/soil intersections.
- `titan-skull-v2-reference-review.png`: reference, landscape, complete rear,
  and head-scale comparison. Requires the configured local reference frame.
- `titan-skull-v2-head-comparison.blend`: editable head-comparison scene.

Build/worldgen integration remains pending. The playable alpha still generates
its original two relics. No automatic fight, titan entity, or world placement is
added by this asset revision.
