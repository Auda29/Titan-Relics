# World Tree V2 — branch-grown canopy

**October 5 follow-up:** the user agreed that the in-game canopy still reads as
compact leaf pads. [V3](../../../docs/project/SCREENSHOT_REVISIONS_20261005.md)
redistributes smaller sprays along finer branches; V2 remains the comparison baseline.

**Integration update:** selected in Alpha 4 for Minecraft review, with a safe
placement height limit. Artistic acceptance remains pending. See
[integration](../../../docs/technical/ALPHA_4_INTEGRATION.md) and
[runtime status](../../../docs/testing/ALPHA_4_TEST_REPORT.md).

October 4, 2026. **Exported visual candidate; user acceptance pending.** The user
found V1 insufficiently natural. V2 rebuilds the tree's growth structure and crown.

- [Four-view review](../design/generated/world-tree-v2/world-tree-v2-review.png)
- [Roots and leaf-hidden skeleton](../design/generated/world-tree-v2/world-tree-v2-detail-review.png)
- [Editable source](../design/generated/world-tree-v2/world-tree-v2-source.blend)
- [NBT](../design/generated/world-tree-v2/world-tree-v2.nbt) /
  [Schematic](../design/generated/world-tree-v2/world-tree-v2.schem)
- [Configuration](../design/world-tree-v2.json) /
  [Verification and measured inventory](../design/generated/world-tree-v2/verification.json)

Actual export: **179 × 216 × 175**, **412,702 blocks**, ten block types, 115 tiles.
Nominal ground is NBT Y8, leaving **208 visible layers**. The nominal total height
is unchanged from V1; the canopy outline and footprint are newly modeled.

## Growth form

- A tapering, leaning trunk with asymmetric buttresses and restrained bark grooves.
- Nine curved primary boughs, 72 secondary/lateral boughs and 189 terminal sprays.
- 567 small irregular foliage clusters attached along terminal twigs; no giant
  parent leaf shelves. Mid-bough lateral growth connects the outer crown masses.
- Seven unequal root buttresses with ground-level forks, one healed branch scar,
  local moss and three partly enclosed worked stones.

The first V2 preview exposed too much bare upper branching; the final candidate
adds mid-bough growth to form a fuller living canopy. Root and branch volumes use
dense internal slices. The leaves use nested irregular skins and native persistent
spruce/oak states. The leaf-hidden review exposes the actual exported wood.

## Verification and limits

Checks cover exact schematic/NBT block coordinates and states, palette, bounds,
hashes, tile reconstruction, solid trunk samples and persistent leaf properties.
Branch-tip probes verify that the fine woody crown survives voxelization.

Preview foliage uses opaque textures and approximate tints. Log states currently
use `axis=y`; in-game biome tint, log orientation refinement, harvesting balance
and performance remain later work. The export omits air, so eventual placement
must define terrain clearing for any authored passages.

Reproduce with `python tools/build_relic_v2.py tree` using the documented local
tool environment. [V1](WORLD_TREE_V1.md) remains available for comparison.
