# Small Colossus V3 — the slender sunken sentinel

October 4, 2026. **Rejected in visual review: too skeletal.** After reviewing
V2, the user found its likeness to the large Colossus too strong and selected a
slender sentinel with an elongated mask, a narrow torso/waist, stepped shoulder
plates, long arms and a sideways sunken pose.

The user subsequently found the result too skeleton-like and supplied a new
primary reference: [Vigilant-Class Archaean Colossi — The Archive In Between](https://www.instagram.com/reel/Da-s0zqi7OQ/).
The next small Colossus should be modeled after this reference rather than the
slender exposed-frame brief. V3 remains a record of that superseded experiment.
See the [V4 reference-led candidate](SMALL_COLOSSUS_V4.md).

- [V2/V3 same-scale comparison](../design/generated/small-colossus-v3/small-colossus-v3-comparison-review.png)
- [Four-view review](../design/generated/small-colossus-v3/small-colossus-v3-review.png)
- [Mask, waist and arm details](../design/generated/small-colossus-v3/small-colossus-v3-detail-review.png)
- [Editable Blender source](../design/generated/small-colossus-v3/small-colossus-v3-source.blend)
- [NBT](../design/generated/small-colossus-v3/small-colossus-v3.nbt) /
  [Schematic](../design/generated/small-colossus-v3/small-colossus-v3.schem)
- [Configuration](../design/small-colossus-v3.json) /
  [Verification and inventory](../design/generated/small-colossus-v3/verification.json)

Actual export: **97 × 84 × 81 blocks**, **24,449 placed blocks**, eight block types
and 14 tiles. Ground is NBT Y8, leaving **76 visible layers**. The central waist
measures about **41% of chest width** in the inspected torso bands; the upper mask
envelope is about **1.57 times as tall as wide**. The export contains 722 copper
blocks; repeatable-site resource balancing remains open.

## Distinct silhouette

The new geometry uses a tapered, long mask with two individual recessed eyes and
a vertical facial keel. A faceted chest narrows into an exposed articulated waist
above a half-buried pelvis and folded upper-leg remnants. Flat, stepped shoulder
plates overlap above two long attached arms: one spreads outward into a grounded
supporting hand; the other rests forward with a relaxed palm-up hand.

A continuous sideways/forward list carries the mask, body and arms into the
sunken posture. Local plate losses expose the frame, with growth restricted to
sheltered ledges. Muted mineral armour, patinated metal couplings and dark joints
provide family continuity. This is an authored design from the user's chosen
brief; the original reel supplies family context rather than a V3 blueprint.

## Checks

The inspector checks exact schematic/NBT state and coordinate equality, source
hashes, palette, bounds and lossless tiles. Additional checks cover chest/rear
openings, waist/neck samples, right-hand orientation/fingers, a face-connected
collar-to-buried-body path, a connected mask and both attached arms. Exported central torso bands
measure waist/chest width; the upper mask envelope is checked for an elongated
height/width ratio. These are geometry checks, not a substitute for visual review.

## Reproduction

Use the established Blender/OBJ/ObjToSchematic pipeline and Python with Pillow:

```powershell
python tools/build_relic_v2.py small-colossus-v3
python tools/review_small_colossus_v3.py
```

The builder's explicit `small-colossus-v3` selection produces this candidate;
its `all` selection continues to reproduce the three original V2 revisions.
This workstation uses `.work/python/Scripts/python.exe` for Pillow-based steps.

The comparison renders actual exported NBTs with one camera and common block
scale/nominal ground. The detail sheet uses inspection crops; its cut planes are
not breaks in the complete model. Game integration, final traversal and rewards
remain later work. [V2](SMALL_COLOSSUS_V2.md) records the earlier family-likeness study.
