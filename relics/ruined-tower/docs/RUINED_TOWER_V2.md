# Ruined Tower V2 — 220 visible blocks

**October 5 follow-up:** the height works in-game, but the user agreed that the
uniform facade and empty interior need detail. [V3](../../../docs/project/SCREENSHOT_REVISIONS_20261005.md)
adds broken storeys, stair flights and facade courses at the same height.

**Integration update:** selected in Alpha 4 for Minecraft review, with a safe
placement height limit. Artistic acceptance remains pending. See
[integration](../../../docs/technical/ALPHA_4_INTEGRATION.md) and
[runtime status](../../../docs/testing/ALPHA_4_TEST_REPORT.md).

October 4, 2026. **Exported visual candidate; user acceptance pending.** The user
requested a taller ruin and selected 220 visible blocks at approximately the
existing width.

- [Four-view review](../design/generated/ruined-tower-v2/ruined-tower-v2-review.png)
- [Base and crown details](../design/generated/ruined-tower-v2/ruined-tower-v2-detail-review.png)
- [Editable source](../design/generated/ruined-tower-v2/ruined-tower-v2-source.blend)
- [NBT](../design/generated/ruined-tower-v2/ruined-tower-v2.nbt) /
  [Schematic](../design/generated/ruined-tower-v2/ruined-tower-v2.schem)
- [Configuration](../design/ruined-tower-v2.json) /
  [Verification](../design/generated/ruined-tower-v2/verification.json)

Actual export: **111 × 232 × 93**, **317,633 blocks**, seven block types, 71 tiles.
Nominal ground is NBT Y12: **220 visible layers**, versus V1's 180 (+22.2%).

The generator loads the published V1 source and extends only source heights above
Y48 by a factor of 172/132. Lower ruins, thresholds, foundations and horizontal
source coordinates stay fixed. The broken upper terminations, facade openings
and upper supporting piers extend together. Source geometry below the transition
is preserved; rerasterization can still change individual boundary voxels.

Validation checks the exact schematic/NBT state grid, source/export hashes,
lossless tile reconstruction, open cavity probes, structural samples, 12-layer
burial and 220 visible layers. Closed wall volumes receive explicit infill.

For later placement under Minecraft's Y319 ceiling, a conservative ground ceiling
of **Y83** leaves a 16-block design margin. Natural placement, terrain-clearing
interiors and Minecraft visual testing remain pending.

Reproduce with `python tools/build_relic_v2.py tower` using the documented local
Blender/Node/Python environment. See [V1](RUINED_TOWER_V1.md) for the original design.
