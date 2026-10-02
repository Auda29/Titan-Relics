# Ruined Tower V1

Status: **first exported visual candidate; user review pending**.

- [Four-view review](../design/generated/ruined-tower-v1/ruined-tower-v1-review.png)
- [Base/crown details](../design/generated/ruined-tower-v1/ruined-tower-v1-detail-review.png)
- [Blender source](../design/generated/ruined-tower-v1/ruined-tower-v1-source.blend)
- [NBT](../design/generated/ruined-tower-v1/ruined-tower-v1.nbt) / [Schematic](../design/generated/ruined-tower-v1/ruined-tower-v1.schem)
- [Configuration](../design/ruined-tower-v1.json) / [Verification](../design/generated/ruined-tower-v1/verification.json)

**Actual export: 111 × 192 × 93, 276,868 blocks, seven block types, 59 tiles.**
Nominal ground is NBT Y12, leaving about 180 visible blocks. The working site
envelope was 112 × 192 × 96; tapered deposits account for the small difference.

## Design

Based on the [reference brief](REFERENCE_DESIGN_STUDY.md): dark vertical piers,
deep flutes/sky slots, unequal broken terminations, large facade breaches, one
rounded opening, two lower ruins and a restrained pale ground join. The reference
does not show the top; the V1 crown is an authored completion. The departing
aircraft is excluded.

The shell is hollow with thick surviving piers. A lower threshold and limited
ledge remnants reserve later architectural opportunities. Wall/debris volumes
use deepslate variants and sealed-volume infill (**160,386 filled cells**); the
opening probes remain empty. This is not a finished tower route or repeated
floor-stack interior.

Review priorities: height/width ratio, silhouette from the rear, amount of large
negative space and whether the upper termination feels sufficiently broken.
The proposed 30–35% wall-loss budget has not been measured as a final statistic.

Reproduce with `python tools/build_new_relic_v1.py tower`. Shared technical notes
and the overview are in [Four new relics V1](../../../docs/project/NEW_RELICS_V1.md).
