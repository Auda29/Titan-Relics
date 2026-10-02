# Colossus V4.1 — palm-up right hand

October 2, 2026. User-requested revision of selected **B / open machine frame**.
Exported and checked offline. **Visually accepted by the user on October 2, 2026.**
Game integration and in-game validation remain pending.

[Hand comparison](../design/generated/colossus-v4-1-frame/colossus-v4-1-hand-review.png)
· [Full model review](../design/generated/colossus-v4-1-frame/colossus-v4-1-frame-review.png)
· [Previous V4](COLOSSUS_V4_EXPORTS.md)

## Pose

The previous 64-degree raised wrist looked like Iron Man firing a beam and was
rejected. V4.1 **supinates the anatomical right hand**, laying its palm almost
horizontal and upward, with four loosely curled rising fingers and a separate
thumb. This is a determinant-positive rotation, not a reflected left hand.
The thumb therefore changes world-space side as a real rolled-over hand would.

The palm normal has Y=0.99805. The fingers rise roughly 15–22 source units from
their roots; their tips lie at source Y33.40 / 37.83 / 40.01 / 35.70. Nominal
ground is source Y20. A separate review panel raises the illustrative ground to
Y28, approximately 7.45 blocks above nominal, covering the palm while leaving
the fingertips visible. This does not establish compatibility with arbitrary
worldgen slopes or heights.

All **434 non-hand V4 source meshes** are fingerprint-identical, including the
forearm, helmet, body, rear armour damage and selected chest frame. The published
V4 A/B assets remain available. The scale stays at **0.930987896 blocks/source
unit**; the hand's flatter reach lengthens the template rather than rescaling it.

| Property | V4.1 frame |
| --- | --- |
| X/Y/Z | **181 × 209 × 235** |
| Blocks | **223,161** |
| Block types / 32-block tiles | **11 / 127** |
| Nominal ground / DataVersion | **NBT Y77 / 3105** |

## Reproduction

From repository root with the existing Blender and pinned ObjToSchematic setup:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/create_colossus_v4_1.py
node tools/obj_to_schem.cjs relics/colossus/design/colossus-v4-1-frame.json
python tools/schem_to_nbt.py relics/colossus/design/generated/colossus-v4-1-frame/colossus-v4-1-frame.schem relics/colossus/design/generated/colossus-v4-1-frame/colossus-v4-1-frame.nbt --air omit --tile-size 32
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config relics/colossus/design/colossus-v4-1-frame.json
python tools/inspect_ots_result.py --config relics/colossus/design/colossus-v4-1-frame.json
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/render_v4_1_details.py
python tools/review_v4_1.py
```

The last two commands also use the Obelisk V4.1 export and renders. The generator
loads the checked-in V4 frame Blender source. Previous sources remain untouched.

Checks pass for schematic/NBT equality, source/export hashes, palette, bounds,
tile reconstruction, anatomical chirality, upward palm, curled fingertips,
all five digits, three finger gaps, three rear breaches and the open chest center.
Reviews are actual-NBT Blender renders, not in-game screenshots. Existing terrain
is preserved at omitted-air positions. Alpha 3 still selects V3; the new footprint
requires explicit integration before use in natural generation.
