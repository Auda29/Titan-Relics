# Small Colossus V4 — reference-led dormant plated specimen

**October 5 follow-up:** in-game screenshots exposed overly rounded/symmetric
forms and a toy-like bright palette. The user agreed with that assessment;
[V5 and the screenshot revision](../../../docs/project/SCREENSHOT_REVISIONS_20261005.md)
address posture, weathering and burial. V4 is preserved as the comparison baseline.

**Integration update:** selected in Alpha 4 for Minecraft review. Artistic
acceptance remains pending. See [integration](../../../docs/technical/ALPHA_4_INTEGRATION.md)
and [runtime status](../../../docs/testing/ALPHA_4_TEST_REPORT.md).

October 4, 2026. **Visual candidate; user acceptance pending.** The user rejected
V3 as too skeletal and requested a new model based on
[Vigilant-Class Archaean Colossi](https://www.instagram.com/reel/Da-s0zqi7OQ/).
The [reference study](SMALL_COLOSSUS_V4_REFERENCE.md) records the inspected frames,
observed features and limits of the partly hidden opening specimen.

- [Four-view review](../design/generated/small-colossus-v4/small-colossus-v4-review.png)
- [Face, grille and pincer details](../design/generated/small-colossus-v4/small-colossus-v4-detail-review.png)
- [V3/V4 same-scale comparison](../design/generated/small-colossus-v4/small-colossus-v4-comparison-review.png)
- [Editable Blender source](../design/generated/small-colossus-v4/small-colossus-v4-source.blend)
- [NBT](../design/generated/small-colossus-v4/small-colossus-v4.nbt) /
  [Schematic](../design/generated/small-colossus-v4/small-colossus-v4.schem)
- [Configuration](../design/small-colossus-v4.json) /
  [Verification and inventory](../design/generated/small-colossus-v4/verification.json)

Actual export: **113 × 84 × 103 blocks**, **215,766 placed blocks**, ten block
types and 29 lossless tiles. Nominal ground is Y9, leaving **75 visible layers**.
The palette contains **1,671 copper blocks**; 157,928 enclosed voxels receive
explicit terracotta infill.

## Reference translation

The opening 0–4.5 s dormant specimen guides the new massing and identifying forms:

- A large rounded head integrated into a thick continuous torso and protected shoulders.
- Six dark convex head optics: two large oval eyes, two small upper eyes and two
  cheek ports, each in a raised metal housing.
- A protruding central muzzle ending in an arched grille with seven modeled
  vertical ribs, sized to remain readable in blocks.
- Heavy forearms with short banded joint sections and broad domed pincer casings.
  Each hand has three optical ports, two long curved outer blades and one shorter
  authored opposing tine.
- Shallow panel incisions, small fasteners, local weathering and restrained growth.

The material palette suggests aged brass/bronze through warm terracotta and
mineral blocks, with real copper limited to trim and couplings. The rear, lower
buried completion, second arm connection, precise pincer anatomy and local soil
contacts are authored; the reference is not a complete multi-view blueprint.

Closed volumes receive explicit infill. The candidate prioritizes plated body
mass; future interiors will require deliberate excavation and authored routes.
No whole cliff or reference landscape is exported.

## Validation

Checks cover exact schematic/NBT coordinates and states, source/export hashes,
palette, bounds and lossless tiles. Additional probes verify solid head/body
cores, six head optics and hand lenses, grille ribs, connected head/pincers/tine
tips, burial and substantial central torso widths. The Blender generator also
checks that shallow decorative cuts leave a closed head with the expected volume.

These are offline asset checks. Game integration, final resource balancing,
traversal, rewards and Minecraft visual testing remain later work.

## Reproduction and reference review

```powershell
python tools/build_relic_v2.py small-colossus-v4
```

Use the documented local Blender/Node/Python-with-Pillow environment; this
workstation uses `.work/python/Scripts/python.exe`. The explicit V4 selector uses
its dedicated inspector. Existing builder selectors retain their version targets.
The V4 build also creates the comparison; `python tools/review_small_colossus_v4.py`
repeats only that comparison from existing exports.

The published comparison shows our actual NBTs at the same block scale. If the
local reference extraction is present, the review script also writes
`.work/references/small-colossus-v4/reference-and-v4.png`: original opening frame
beside the new NBT landscape preview, individually framed. That reference-image
comparison stays local under the existing publication policy.
