# Obelisk V4.1 — consistent facets and larger cracks

October 2, 2026. User-requested revision; exported and checked offline, awaiting review.

[Before/after and crack detail](../design/generated/obelisk-v4-1/obelisk-v4-1-changes-review.png)
· [Full model review](../design/generated/obelisk-v4-1/obelisk-v4-1-review.png)
· [Previous V4](OBELISK_V4_EXPORTS.md)

## Revised direction

The user rejected V4's alternating, strongly contrasting patches as tiger-like.
Keep the individual sides visually coherent with local weathering, and allow
larger cracks than the original very restrictive damage brief.

V4.1 assigns sandstone, cut sandstone and smooth sandstone to the original
antiprism facets. Broad terracotta patches are removed. Abrasion is confined
to small areas around **three branching surface fissures**, with darker
dripstone restricted to recessed damaged faces. Main fissures span
25–35 source units vertically and are 3.1 units wide, with thinner branches,
different paths and staggered heights. These are
actual Boolean-cut openings, not painted crack stripes.

**Four larger edge spalls** replace V4's tiny chips. The monolith loses **0.607%**
of its original source volume, versus 0.01155% in V4. It keeps its height,
upright antiprism, rotated crown, supporting foot and continuous sandstone core.
All **five V4 scenery meshes** (solid sand deposits and three foundation fragments)
are fingerprint-preserved. V4 exports remain available separately.

| Property | V4.1 |
| --- | --- |
| Overall X/Y/Z | **59 × 185 × 60** |
| Blocks | **94,593** |
| Block types / 32-block tiles | **5 / 24** |
| Enclosed sandstone fill | **75,751 cells** |
| Nominal ground / DataVersion | **NBT Y8 / 3105** |

## Reproduction

From repository root with the existing local tools:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/create_obelisk_v4_1.py
node tools/obj_to_schem.cjs relics/obelisk/design/obelisk-v4-1.json
python tools/schem_to_nbt.py relics/obelisk/design/generated/obelisk-v4-1/obelisk-v4-1.schem relics/obelisk/design/generated/obelisk-v4-1/obelisk-v4-1.nbt --air omit --tile-size 32
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config relics/obelisk/design/obelisk-v4-1.json
python tools/inspect_ots_result.py --config relics/obelisk/design/obelisk-v4-1.json
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/render_v4_1_details.py
python tools/review_v4_1.py
```

The generator uses the V4 source scenery and original V3 monolith. The final
two commands also require Colossus V4.1. Shared setup is documented in
[Blender workflow](../../../docs/technical/BLENDER_WORKFLOW.md).

## Checks

Passed source/export hashes, schematic/NBT equality, palette/bounds, lossless tile
reconstruction, square foot, rotated crown, supported sand and the continuous
7 × 185 × 7 core prism. Each crack has actual removed surface samples relative
to the undamaged V3 NBT and solid backing at every checked sample four blocks
inward. The source mesh remains watertight.

The review shows actual NBT in Blender. Crack close-ups are explicitly cropped;
their flat top/bottom are inspection cuts. In-game placement and visual acceptance
remain pending. Source X/Z zero still maps to NBT X31/Z32. Alpha 3 selects V3.
