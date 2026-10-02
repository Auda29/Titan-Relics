# Colossus V4 — rear damage, raised right hand, and chest candidates

Created: October 2, 2026. **B — open machine frame selected by the user on October 2.**
Alpha 3 still selects V3. These assets do not change gameplay, worldgen resources,
or the build selection.

## Scope

The approved direction is recorded in [V4 review notes](COLOSSUS_V4.md): preserve
the accepted Colossus, revise the clean rear, make its right hand readable, and
compare removing the plain chest cylinder with replacing it by open machinery.

`tools/create_colossus_v4.py` loads the checked-in V3 source model and derives both
candidates without regenerating or overwriting V3. It checks that **397 existing
mesh objects** retain their vertex positions, faces, materials, and transforms.
These include the helmet assembly, original forearm and cuff, and buried hip.
The original palette, body scale, and nominal ground level are retained.

## Rear armour

Three irregular breaches cut through the posterior cuirass and rear shoulder
armour. The cuts stay in the rear half of the body. Torn plate lips expose metal
thickness; bent supports, an interrupted diagonal brace, and severed conduits
provide depth behind the openings. The rounded heavy silhouette remains.

## Anatomically right hand

Source coordinates use front **−Z**, up **+Y**, and the Colossus's right **+X**.
The original forearm endpoints are retained at `(48, 19, −88)` and
`(−10, 17, −144)`. The hand is rebuilt around its existing wrist with **64° wrist
extension**, leaving the sleeve in its original fallen position.

The palm has four separately articulated fingers and a separate opposed thumb.
Finger lengths and curling differ; the thumb is on the same anatomical side as
the V3 palm-down hand. The coordinate basis is a proper rotation with determinant
**+1**, not a reflection. With `T` toward the thumb, `D` toward the fingertips,
and `P` pointing out of the palm, **T × D = P**. All digits share this transform.

Dedicated actual-NBT views show both sides: the thumb is on image right in the
palm-side view and on image left in the opposite view. A preview ground plane at
the nominal surface shows the fingers rising out of the soil. This plane is not
part of the export. Final terrain-dependent access through the arm remains V5
structural work; no chest, loot, spawner, or vault data is authored here.

## Chest decision: A or B

The changed V3 part is **`Buried chest piston`**, the plain exposed cylinder at
the low front chest tear: source endpoints `(24, 4, −20)` to `(24, 31, −20)`,
radius 13. The neck well/collar is retained.

| Candidate | Treatment | Export |
| --- | --- | --- |
| **A — open** | Remove the piston; retain the existing internal ribs and footing | `colossus-v4-open` |
| **B — frame** | Replace it with three interrupted bearings, slender broken supports, and one disconnected copper line | `colossus-v4-frame` |

Both have an open center rather than a solid replacement cylinder. **B is the
selected V4 design; A remains a comparison alternative.** The selected asset is
`relics/colossus/design/generated/colossus-v4-frame/colossus-v4-frame.nbt`.
Chest comparison panels use identical
source-coordinate inspection crops, including below-ground geometry with terrain
removed. They are not newly enlarged exterior openings or gameplay rooms.

## Export measurements and verification

| Measure | A — open | B — frame |
| --- | --- | --- |
| X/Y/Z, including arm and buried hip | **181 × 209 × 223** | **181 × 209 × 223** |
| Placed blocks | **221,452** | **222,621** |
| Used block types | **11** | **11** |
| Nonempty 32-block tiles | **119** | **119** |
| Nominal ground Y | **77** | **77** |
| DataVersion | **3105** | **3105** |

The horizontal Z footprint is four blocks shorter than V3 because the fingers
now rise upward instead of extending along the ground; the body is not rescaled.
The export scale remains **0.930987896 blocks/source unit**, matching V3.

Checks validate source/export hashes, all schematic/NBT block states and positions,
palette counts, bounds, and lossless tile reconstruction. V4 checks additionally
cover the right-handed basis, all five digit tips, three separate finger-gap
samples, three open rear-breach samples, and a clear 5 × 5 × 5 chest-center sample.
Source generation checks the 397 preserved objects against V3, whose source hash
is retained in metadata.

The A/B comparison finds **1,218 differing block positions**, all confined to
the chest mechanism region. Everything else in their NBT block maps is identical.
These are offline geometry checks, not Minecraft placement or navigation tests.

## Reproduce

Use the shared [Blender workflow](../../../docs/technical/BLENDER_WORKFLOW.md).
The checked-in V3 source Blender model, design metadata, and NBT provide the
baseline; the pinned local ObjToSchematic checkout supplies conversion and textures.

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
& $blender --background --python-exit-code 1 --python tools/create_colossus_v4.py
foreach ($variant in @("open", "frame")) {
    $stem = "colossus-v4-$variant"
    $config = "relics/colossus/design/$stem.json"
    $out = "relics/colossus/design/generated/$stem"
    node tools/obj_to_schem.cjs $config
    python tools/schem_to_nbt.py "$out/$stem.schem" "$out/$stem.nbt" --air omit --tile-size 32
    & $blender --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config $config
    python tools/inspect_ots_result.py --config $config
}
& $blender --background --python-exit-code 1 --python tools/render_colossus_v4_details.py
python tools/inspect_colossus_v4.py --sheets
```

Use `--check-only` on the generic inspector to skip sheet assembly. Reference
sheets are conditional on the local reference frame being present. The V4 detail
sheet needs only the V3/V4 NBTs, metadata, and atlas, not the Instagram media.

## Review and editable outputs

- [V4 change/decision sheet](../design/generated/colossus-v4-open/colossus-v4-changes-review.png):
  V3/V4 rear comparison, both sides of the right hand, and original/A/B chest.
- [Candidate A](../design/generated/colossus-v4-open/): source Blender, whole NBT,
  schematic, metadata, and review sheets.
- [Candidate B](../design/generated/colossus-v4-frame/): equivalent deliverables.

The regular views show the full export and an illustrative landscape. Detail
views are explicitly cropped NBT inspections. Preview scenery and scale markers
are not exported. The candidates use `--air omit`; omitted cells do not clear
pre-existing world terrain. Minecraft/Modrinth are not required or installed by
this workflow. Gameplay data and custom item behavior belong to the other agent;
future V5 structural work can provide routes, room geometry, and placement coordinates.
