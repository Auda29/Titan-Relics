# October 4 relic revisions — V2 review

The user **visually accepted Titan Skull 2 V1 for now**, requested a more natural
World Tree, selected the large Colossus's visual family for a rebuilt smaller
machine, and chose **220 visible blocks** for the Ruined Tower.

## Review candidates

| Candidate | Actual X × Y × Z | Visible layers | Blocks |
| --- | --- | ---: | ---: |
| Small Colossus V2 | 89 × 80 × 89 | 72 | 39,538 |
| World Tree V2 | 179 × 216 × 175 | 208 | 412,702 |
| Ruined Tower V2 | 111 × 232 × 93 | 220 | 317,633 |

- [V1/V2 same-scale comparison](reviews/relics-v2-review.png): each pair uses
  actual NBT blocks, one orthographic camera and a shared nominal ground plane.
  V1 is on the left, V2 on the right. Different pairs are framed independently.
- [Small Colossus V2](../../relics/colossus/docs/SMALL_COLOSSUS_V2.md): new domed
  helmet, curved visor, respirator and bronze-coloured armour; compact asymmetrical
  stance, detached right sleeve and connected internal frame.
- [World Tree V2](../../relics/world-tree/docs/WORLD_TREE_V2.md): tapering trunk,
  irregular root forks and a fine branch-grown canopy with mid-bough foliage.
- [Ruined Tower V2](../../relics/ruined-tower/docs/RUINED_TOWER_V2.md): 220 visible
  layers rather than 180, with the same horizontal source geometry.

**Small Colossus V2 requires revision:** the user finds it too similar to the large
Colossus and wants a more distinct appearance. World Tree V2 and Ruined Tower V2
remain visual candidates awaiting user review. The approved
[sword-bearing skull V1](../../relics/titan-skull/docs/TITAN_SKULL_2_V1.md) retains
its existing geometry. The playable Alpha 3 still selects its three V3 assets.

For the next small Colossus, the user chose the slender sunken sentinel direction:
an elongated mask, narrow waist, stepped armour and long arms.
See the [Small Colossus V3 candidate](../../relics/colossus/docs/SMALL_COLOSSUS_V3.md)
and its separate V2/V3 comparison.

**Later feedback:** V3 was rejected as too skeletal. The user supplied a new
[Vigilant-Class reference](../../relics/colossus/docs/SMALL_COLOSSUS_V4_REFERENCE.md),
now developed as the [Small Colossus V4 candidate](../../relics/colossus/docs/SMALL_COLOSSUS_V4.md).

## Reproduction

Use the [Blender workflow](../technical/BLENDER_WORKFLOW.md), including pinned
ObjToSchematic and a Python environment with Pillow:

```powershell
python tools/build_relic_v2.py all
python tools/review_relic_v2.py
```

The builder accepts `tower`, `tree` or `small-colossus`. `--skip-model` reuses the
OBJ but repeats conversion; `--review-only` validates and renders existing exports.
All commands run from the repository root. This workstation uses the isolated
`.work/python/Scripts/python.exe` environment for Pillow-based review assembly.

Each asset includes source Blender, schematic, whole NBT, design/converter
metadata, verification and overview/detail review images. The pipeline remains
Blender → triangulated OBJ → pinned ObjToSchematic → schematic → Java NBT,
with DataVersion 3105 retained. Renderer shader setup now resolves nodes by type
so translated Blender node names do not break the preview workflow.

The dedicated inspector checks exact round-trip states, hashes, bounds, palette
and lossless tiles, then feature-specific cavities, supports, tower height,
persistent leaves/branch tips and Colossus hand/body structure. These checks are
offline export evidence; worldgen, architectural interiors and Minecraft visual
acceptance are subsequent work.
