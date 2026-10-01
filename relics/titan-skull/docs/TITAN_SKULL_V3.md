# Titan Skull v3 — broken, partly buried spine

Updated: October 1, 2026.

## Design

V3 extends [Titan Skull v2](TITAN_SKULL_V2.md) with a fallen spinal remnant.
The crowned skull keeps its v2 source geometry and scale: approximately **76
blocks including the crown**, about 20% taller than the Colossus helmet shell.
The spine is an original addition requested by the user; the skull reference
remains the opening of [D.E.A.D.](https://www.instagram.com/reel/DXM3J4sgqJl/).

- Three cervical vertebrae extend from the rear of the skull.
- A large fracture separates them from a displaced, curved five-vertebra chain.
- A second break leaves one loose terminal vertebra.
- Broken process fragments lie beside the dislocations.
- Lower vertebral bodies are buried in the exported hill; arches and dorsal and
  lateral processes remain exposed. Rotation and uneven burial vary by vertebra.

The moss/soil/stone mound extends behind the head to support the entire remnant.
Its interior uses the same dense terrain slices as v2, preserving skull cavities
without globally filling the asset. Bone geometry continues below the local
surface. “Half-buried” describes the visual treatment rather than exactly 50%
of each vertebra's volume.

## Verified export

| Metric | Value |
| --- | --- |
| Overall X/Y/Z, including spine and hill | **121 × 79 × 203 blocks** |
| Placed blocks | **264,355** |
| Terrain blocks | **244,825** |
| Remaining bone/mineral/vegetation blocks | **19,530** |
| Used block types | **7** |
| Nonempty 32-block tiles | **37** |
| Nominal ground | **NBT Y8** |
| DataVersion | **3105** |

The voxelizer height setting remains 80; the actual occupied export is 79 layers
high. Source skull bounds and geometric block scale are preserved from v2.
The longer footprint comes from the spine and its supporting terrain.

Validation covers source/export hashes, full schematic/NBT equality, palette,
bounds, and lossless tile reconstruction. Geometry checks cover six empty cavity
samples, the 5 × 5 mouth inspection channel, nine posterior-wall rays, and five
groups of solid terrain columns. Each of the nine vertebral regions must contain
bone samples both below and above its local surface. Two fracture planes must
remain free of bone, confirming that no bone bridge crosses either break.

These are offline geometry checks. Natural placement and in-game testing remain
pending. As in v2, `--air omit` does not clear pre-existing terrain from cavities.

## Reproduce

Follow [Blender workflow](../../../docs/technical/BLENDER_WORKFLOW.md). The local Colossus v3 source is
required for measuring the helmet; its NBT is required for the size comparison.
V3 reuses the v1/v2 builders in memory; their generated skull files are not needed.

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
& $blender --background --python-exit-code 1 --python tools/create_titan_skull_v3.py
node tools/obj_to_schem.cjs relics/titan-skull/design/titan-skull-v3.json
python tools/schem_to_nbt.py relics/titan-skull/design/generated/titan-skull-v3/titan-skull-v3.schem relics/titan-skull/design/generated/titan-skull-v3/titan-skull-v3.nbt --air omit --tile-size 32
& $blender --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config relics/titan-skull/design/titan-skull-v3.json
python tools/inspect_ots_result.py --config relics/titan-skull/design/titan-skull-v3.json
```

Outputs are under `relics/titan-skull/design/generated/titan-skull-v3/`: editable `.blend`, OBJ/MTL,
schematic, whole NBT, tiles, metadata, verification, and rendered previews.

- `05-blocks-landscape.png`: complete export in illustrative surroundings.
- `06-size-comparison.png`: whole export beside Colossus v3 at the same block scale.
- `09-spine-overview.png`: complete rear view with both fractures visible.
- `10-spine-detail.png`: cropped NBT inspection of the vertebral chain. Straight
  terrain edges in this detail are crop boundaries, not edges of the full asset.
- `titan-skull-v3-reference-review.png`: reference, landscape, rear overview, and
  spine detail; requires the configured local reference image.

Skull, spine, fragments, and local hill are exported blocks. Distant scenery,
staging planes, and the traveler are preview aids. Review sheets, the editable
source Blender model, whole NBT and schematic exports, design/converter metadata,
and verification records are included in Git alongside generators, configuration,
and documentation. Render scenes, backups, OBJ/MTL intermediates, and tiles with
their conversion manifest remain local.
