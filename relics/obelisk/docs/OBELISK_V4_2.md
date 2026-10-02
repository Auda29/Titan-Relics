# Obelisk V4.2 — warmer stone and missing pieces

October 2, 2026. User-requested revision, exported and checked offline.
**Visually accepted by the user.** Game integration and in-game validation remain pending.

[Before/after and damage detail](../design/generated/obelisk-v4-2/obelisk-v4-2-changes-review.png)
· [Full model review](../design/generated/obelisk-v4-2/obelisk-v4-2-review.png)
· [Previous V4.1](OBELISK_V4_1.md)

## Revision

The user found V4.1 too white and asked for small genuinely missing pieces
without differently colored replacement blocks in the damaged areas.

The monument now uses **yellow terracotta and terracotta** as ochre/clay stone
facets, closer to the earlier warm desert palette. Every original facet retains
its own material. Recessed fracture faces inherit the nearest original side's
stone instead of a special dark crack lining. The solid core uses ochre too;
exposed interiors do not reveal white sandstone. Sand and foundation scenery
retain their V4.1 geometry and materials.

Three branching fissures and four edge spalls remain. **Two additional angular
edge chunks are actually removed**, leaving open notches. Comparing the exports
finds 73 and 98 removed blocks around these two cuts, respectively. There is no
decorative replacement block in the missing volume. Shape and lighting make the
recesses visible. The total source monolith volume loss is **0.847%**.

| Property | V4.2 |
| --- | --- |
| X/Y/Z | **59 × 185 × 60** |
| Blocks | **94,422** |
| Block types / tiles | **4 / 24** |
| Enclosed core fill | **75,555 ochre cells** |
| Nominal ground / DataVersion | **NBT Y8 / 3105** |

The antiprism bounds, height, rotated crown, solid core and five scenery meshes
are preserved. Earlier exports remain available in their own version folders.

## Reproduce

From repository root, using the existing local tools:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/create_obelisk_v4_2.py
node tools/obj_to_schem.cjs relics/obelisk/design/obelisk-v4-2.json
python tools/schem_to_nbt.py relics/obelisk/design/generated/obelisk-v4-2/obelisk-v4-2.schem relics/obelisk/design/generated/obelisk-v4-2/obelisk-v4-2.nbt --air omit --tile-size 32
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config relics/obelisk/design/obelisk-v4-2.json
python tools/inspect_ots_result.py --config relics/obelisk/design/obelisk-v4-2.json
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/render_v4_1_details.py -- --obelisk-only --obelisk-stem obelisk-v4-2
python tools/review_obelisk_v4_2.py
```

The generator loads the V4.1 source, with V3 as the original facet reference.
The before/after sheet uses the previous V4.1 front render.

## Verification

Passed source/export hashes, exact schematic/NBT equality, palette and bounds,
lossless tile reconstruction, rotated crown, square base, supported sand and
continuous 7 × 185 × 7 core. All three fissures remain open over solid backing.
The two new notches survive voxelization and core filling; the monument above
the foundation contains only its two side materials, without pale or dark inserts.

Reviews render actual NBT in Blender. Detail panels are inspection crops, not
separate broken sections. `--air omit` preserves pre-existing terrain at omitted
positions; worldgen clearing and placement remain integration work. Alpha 3
still selects V3. Source X/Z zero maps to NBT X31/Z32.
