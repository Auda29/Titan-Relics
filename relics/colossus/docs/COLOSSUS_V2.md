# Colossus v2 — original reference-based design

Updated: October 1, 2026.

Colossus v2 is the first design based directly on the opening 0–5 seconds of
[Archaean Colossi — The Archive In Between](https://www.instagram.com/reel/DaoBxUEiBNa/).
It uses a bronze dome helmet, a narrow visor, respirator hoses, broad armor,
vegetation, and a detached foreground arm. The later extension with an underground
abdomen and torn hip is **[Colossus v3](COLOSSUS_V3.md)**.

| Metric | Colossus v2 |
| --- | --- |
| Dimensions X/Y/Z, including arm | 181 × 160 × 227 blocks |
| Placed blocks | 182,734 |
| Block types | 11 |
| Nonempty 32-block tiles | 100 |

The 160-block height is an artistic scale estimate, not a measured dimension of
the reference. This asset is separate from both the playable alpha's Colossus
and the first 66-block Blender experiment.

## Reproduce

Follow [Blender workflow](../../../docs/technical/BLENDER_WORKFLOW.md) for local dependencies. Run from
the repository root:

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
& $blender --background --python-exit-code 1 --python tools/create_colossus_v2.py
node tools/obj_to_schem.cjs relics/colossus/design/colossus-v2.json
python tools/schem_to_nbt.py relics/colossus/design/generated/colossus-v2/colossus-v2.schem relics/colossus/design/generated/colossus-v2/colossus-v2.nbt --air omit --tile-size 32
& $blender --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config relics/colossus/design/colossus-v2.json
python tools/inspect_ots_result.py --config relics/colossus/design/colossus-v2.json
```

The generator is a wrapper around the shared implementation in
`tools/create_colossus_v3.py`, selecting version 2 without the buried-hip extension.

- Configuration: `relics/colossus/design/colossus-v2.json`
- Outputs: `relics/colossus/design/generated/colossus-v2/`
- Editable source: `colossus-v2-source.blend`
- Block exports: `colossus-v2.schem`, `colossus-v2.nbt`
- Reference comparison: `colossus-v2-reference-review.png` (requires the local reference image)
- Verification: `verification.json`

Source/export hashes, block coordinates and states, palette counts, bounds, and
lossless reconstruction from tiles were checked. The images render exported NBT
in Blender, not Minecraft. Surface voxelization, omitted air, and legacy
DataVersion 3105 still require target-game review. Build and worldgen integration
remain pending.
