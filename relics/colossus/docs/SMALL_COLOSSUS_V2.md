# Small Colossus V2 — a relative of the large machine

October 4, 2026. **Revision required: too similar to the large Colossus.** The user
found V1 too close to the original test Colossus and selected a new design in the
accepted large Colossus's visual family, with its own proportions and pose.

After reviewing V2, the user clarified that this candidate resembles the large
Colossus too closely. The next design needs a clearly distinct appearance. The
user selected a **slender sunken sentinel**: elongated mask, narrower torso,
stepped shoulder plates, long arms and a sideways sunken pose. Shared family
identity alone is not visual acceptance of V2.
The resulting [V3 candidate](SMALL_COLOSSUS_V3.md) is available for review.

- [Four-view review](../design/generated/small-colossus-v2/small-colossus-v2-review.png)
- [Hand and upper-body details](../design/generated/small-colossus-v2/small-colossus-v2-detail-review.png)
- [Editable source](../design/generated/small-colossus-v2/small-colossus-v2-source.blend)
- [NBT](../design/generated/small-colossus-v2/small-colossus-v2.nbt) /
  [Schematic](../design/generated/small-colossus-v2/small-colossus-v2.schem)
- [Configuration](../design/small-colossus-v2.json) /
  [Verification](../design/generated/small-colossus-v2/verification.json)

Actual export: **89 × 80 × 89**, **39,538 blocks**, eleven block types, 18 tiles.
Nominal ground is NBT Y8, leaving **72 visible layers**. V1 had 67 visible layers
and a 101 × 76 × 87 footprint including its detached arm and deposits.

## New form

The model is built from new geometry with shared modeling helpers, using neither
archived meshes nor a scaled copy of the large asset. A listed dome helmet, curved
visor lips, side filters, ribbed respirator and rolled collar establish kinship.
The compact curved cuirass, unequal shoulders, bent supporting left arm and short
forward detached right sleeve give it a separate stance.

A lower off-center armour tear replaces the test design's central circular chest
window. Rear damage exposes an internal supporting frame. The detached right hand
has an upward-facing palm, four curled fingers, an opposing thumb and articulated
knuckles. Local moss, patina and interrupted deposits ground the assembly.

Terracotta supplies most bronze-coloured armour; the export contains **1,906 copper
blocks** and no raw-iron deposit. This is an asset inventory, not final repeatable
site salvage balancing. Core/Magnet rewards are not assigned to this smaller family.

## Verification and reproduction

Exact schematic/NBT states, source/export hashes, palette, bounds and tile
reconstruction pass. Additional probes check chest/rear cavities, structural
members, right-hand orientation and fingers. A six-neighbor flood traversal
confirms a structural connection from the collar to the buried body.

Run `python tools/build_relic_v2.py small-colossus` in the documented local tool
environment. Game integration and in-game review remain pending. The
[archive-derived V1](SMALL_COLOSSUS_V1.md) records the superseded approach.
