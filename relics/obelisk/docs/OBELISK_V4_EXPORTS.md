# Obelisk V4 — stable weathered monument

October 2, 2026. Offline design export, awaiting visual acceptance and integration.

[V3/V4 review](../design/generated/obelisk-v4/obelisk-v4-changes-review.png)
· [German revision brief](OBELISK_V4.md)

## Implemented design

The V3 tapered square antiprism remains upright, with its 45-degree rotated crown,
24-unit base, 16.08-unit crown, 176-unit above-ground source height and eight-unit
buried foot. Four shallow edge abrasions remove **0.01155%** of the source monolith
volume. Its bounds remain identical to V3; subdivision only gives weathering finer
material resolution on the original planes.

Sandstone, terracotta, smooth/cut sandstone and sparse darker mineral seams form
coherent weathering zones. Three low asymmetric sand drifts and three separated
foundation fragments establish the archaeological site. Damage is superficial;
the foot and solid body remain continuous.

| Property | Export |
| --- | --- |
| Overall X/Y/Z, including sand and fragments | **59 × 185 × 60** |
| Monolith source bounds | **24 × 184 × 24**, unchanged |
| Blocks | **95,038** |
| Block types / tiles | **6 / 24** |
| Enclosed cells filled with sandstone | **76,307** |
| Nominal ground / DataVersion | **NBT Y8 / 3105** |

The expanded X/Z template bounds represent the sand and foundation scatter,
not a wider monolith. Integration must account for the shifted template origin:
source X/Z zero maps to local **X31/Z32**, rather than the template midpoint.

## Reproduce

Use the checked-in V3 Blender source and existing pinned conversion setup.

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/create_obelisk_v4.py
node tools/obj_to_schem.cjs relics/obelisk/design/obelisk-v4.json
python tools/schem_to_nbt.py relics/obelisk/design/generated/obelisk-v4/obelisk-v4.schem relics/obelisk/design/generated/obelisk-v4/obelisk-v4.nbt --air omit --tile-size 32
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config relics/obelisk/design/obelisk-v4.json
python tools/inspect_ots_result.py --config relics/obelisk/design/obelisk-v4.json
python tools/inspect_relic_v4.py --sheets
```

The final combined review command also requires the four Skull V4 exports and
their previews, plus existing Skull/Obelisk V3 previews. Intermediate renders,
OBJ/MTL, tile folders and manifests stay local; source `.blend`, whole exports,
reviews and selected verification metadata follow the repository publication policy.

## Validation and scope

Passed source/export hashes, exact schematic/NBT equality, palette/bounds and
lossless tile reconstruction. Geometry checks cover the square foot, rotated
crown, continuous **7 × 185 × 7** core prism and every full-height monolith layer.
Sand has no unsupported exported blocks. The source monolith remains watertight.

Reviews are actual-NBT Blender renders, with an illustrative surrounding plane.
The foundation panel is explicitly a cropped inspection view. Placement on uneven
terrain and in-game rotations still need external game testing. Archaeology,
collectibles and map data remain the gameplay integration agent's scope. Alpha 3
continues to select V3.
