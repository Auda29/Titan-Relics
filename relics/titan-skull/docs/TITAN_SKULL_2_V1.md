# Titan Skull 2 V1 — the embedded sword

Status: **first independent skull/sword export; visual review pending**.

- [Four-view review](../design/generated/titan-skull-2-v1/titan-skull-2-v1-review.png)
- [Face/weapon details](../design/generated/titan-skull-2-v1/titan-skull-2-v1-detail-review.png)
- [Blender source](../design/generated/titan-skull-2-v1/titan-skull-2-v1-source.blend)
- [NBT](../design/generated/titan-skull-2-v1/titan-skull-2-v1.nbt) / [Schematic](../design/generated/titan-skull-2-v1/titan-skull-2-v1.schem)
- [Configuration](../design/titan-skull-2-v1.json) / [Verification](../design/generated/titan-skull-2-v1/verification.json)

**Actual export: 105 × 144 × 107, 85,224 blocks, twelve block types, 38 tiles.**
Nominal ground is NBT Y12; the complete skull/sword composition rises about 132
blocks above it. The 104 × 144 × 116 planning envelope allowed more rear deposit
space; this V1 is nine blocks shallower rather than padding it with a pedestal.

## Reference identity

The [opening reference segment](TITAN_SKULL_2_CONCEPT.md) shows a rounded,
overgrown skull with a huge diagonally embedded sword. V1 follows that composition:
large empty eye sockets, triangular nose, open jaw, uneven missing teeth and a
complete rounded rear. It contains **no organic crown, lateral horns or spine**.

The sword leans toward image-left in the primary front view. Its blade extends
into the skull through a real impact opening; a broad curved guard, wrapped grip,
pommel and attached growth keep the weapon readable. The blade/guard use low-value
mineral blocks rather than solid iron, gold or diamond. Four weapon-section
probes include the buried blade. Eye/nose/mouth probes remain empty.
Two surviving bone lips clamp the blade at the entry, with 44 exported
weapon-to-bone face contacts verified in addition to those section probes.

Bone, calcite and mineral staining combine with broad moss patches and separate
damp deposits. The exterior is authored for a lush grotto/open sinkhole, but the
review stages it in neutral green surroundings to keep the actual model readable;
**no cavern shell, roof or water system is exported**.

Review priorities: skull-to-sword scale, whether the jaw looks sufficiently
natural, the amount of growth, and blade/cranial contact. Percent bone-loss targets
from the brief remain unmeasured authoring goals, not claimed verification results.

Reproduce with `python tools/build_new_relic_v1.py skull-2`. See
[shared V1 workflow](../../../docs/project/NEW_RELICS_V1.md). Current crowned-skull
V4 assets and their accepted terrain variants remain separate.
