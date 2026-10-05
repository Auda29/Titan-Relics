# World Tree V1

Status: **revision required following user review on October 4, 2026**.

The user finds V1 insufficiently natural. The next revision needs a more natural
growth form; the exact modeling treatment has not yet been agreed.
The subsequent [V2 candidate](WORLD_TREE_V2.md) develops fine branch-grown foliage
and irregular tapered roots for review.

- [Four-view review](../design/generated/world-tree-v1/world-tree-v1-review.png)
- [Roots and leaf-hidden skeleton](../design/generated/world-tree-v1/world-tree-v1-detail-review.png)
- [Blender source](../design/generated/world-tree-v1/world-tree-v1-source.blend)
- [NBT](../design/generated/world-tree-v1/world-tree-v1.nbt) / [Schematic](../design/generated/world-tree-v1/world-tree-v1.schem)
- [Configuration](../design/world-tree-v1.json) / [Verification](../design/generated/world-tree-v1/verification.json)

**Actual export: 193 × 216 × 169, 503,048 blocks, ten block types, 140 tiles**,
with nominal ground at NBT Y9 and about
207 visible blocks. The working envelope was 192 × 216 × 176; the authored crown
is slightly shallower. The verification record contains the exact inventory.

## Design and construction

Following the [reference brief](REFERENCE_DESIGN_STUDY.md), V1 has a twisted,
fluted trunk, five primary crown limbs, high central forks, eight unequal foliage
masses, broken leaf edges, six grounding roots, one old branch scar and three
worked stones near the base. The crown is living and layered rather than a
single leaf sphere. The leaf-hidden detail shows the underlying structure.

The trunk, primary/secondary branches and roots include internal slices spaced
0.68 source units apart, producing solid wood rather than giant empty tubes.
Root arches reserve open space near the base; worked stones sit beside those
openings. Local deposits follow root contacts rather than covering the full
crown footprint with a flat platform.

Foliage uses nested uneven shelves plus smaller overlapping edge cushions.
**Both native leaf types have `persistent=true`**. Log states specify `axis=y`;
future axis-aware log placement may improve the appearance of diagonal branches.
The asset contains no iron/copper resource deposit or predefined reward.

## Preview and review focus

The legacy converter atlas lacks these leaf block names. Semantic proxies are
remapped to exact native leaf/log states in the schematic. The independent
preview atlas adds the two leaf textures using fixed tints and opaque rendering;
it does not simulate biome coloration, transparent leaf rendering or lighting
from a Minecraft client. See [shared V1 technical notes](../../../docs/project/NEW_RELICS_V1.md).

Review priorities: crown fullness and tiering, relative trunk thickness, readable
branch supports, and open root passages. The broad branch/leaf treatment is V1,
not a claim of exact reconstruction of the reference montage. Later biome,
world-height and performance testing must account for its large canopy.

Reproduce with `python tools/build_new_relic_v1.py tree`. The generator remains
independent of the existing accepted relics and does not create V5 routes or rooms.
