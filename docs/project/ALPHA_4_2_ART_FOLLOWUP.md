# Alpha 4.2 screenshots — art follow-up

October 5, 2026. The user supplied 13 in-game screenshots in
`build/screenshot-review/20261005-alpha4-2/` and approved the proposed follow-up:
rebuild the cactus-like Tree crown, replace the Small Colossus's round primitive
forms with overlapping armour, and refine the Tower's upper breaks and interior.
Approval to revise is not visual acceptance of the new candidates.

## Actual-block review

- [Same-scale before/after comparison](reviews/alpha42-art-followup-20261005.png)
- [World Tree V4 overview](../../relics/world-tree/design/generated/world-tree-v4/world-tree-v4-review.png)
- [World Tree V4 roots and exposed woody skeleton](../../relics/world-tree/design/generated/world-tree-v4/world-tree-v4-detail-review.png)
- [Small Colossus V6 overview](../../relics/colossus/design/generated/small-colossus-v6/small-colossus-v6-review.png)
- [Ruined Tower V4 broken stairs and crown](../../relics/ruined-tower/design/generated/ruined-tower-v4/ruined-tower-v4-detail-review.png)

These are Blender renders of the exported NBT. Each comparison pair shares a
camera, block scale and nominal ground plane; different rows are framed separately.
The in-game screenshots remain the review baseline, not pictures of these new exports.

| Candidate | X × Y × Z | Blocks | Ground Y | Visible layers | Tiles |
| --- | --- | ---: | ---: | ---: | ---: |
| World Tree V4 | 187 × 216 × 185 | 291,433 | 8 | 208 | 124 |
| Small Colossus V6 | 111 × 80 × 113 | 234,956 | 9 | 71 | 33 |
| Ruined Tower V4 | 111 × 232 × 93 | 321,087 | 12 | 220 | 69 |

## World Tree V4

The primary limbs bend outward, then divide into four branching orders: nine
primary boughs, 45 secondary forks, 135 tapering branches and 405 leaf-bearing
twigs. The 810 irregular foliage sprays are offset laterally at the ends of
twig fans. Unequal rising and descending shoots break up flat tiers and leave
the proximal branch segments exposed. Low elongated soil deposits follow the
root buttresses instead of making separate round grass hummocks.

The conversion also exposed a real material-overlap defect: ObjToSchematic's
first-hit rule sometimes assigned leaves to voxels occupied by both leaves and
thin woody branches, breaking the exported wood path. V4 explicitly prioritizes
the wood/bark/cut materials **only in cells intersected by those source meshes**.
This adds no invented branch geometry. The scoped adapter restores the upstream
method after conversion and is enabled only in the V4 Tree config. The inspector
checks paths through face-connected wood from the trunk to the branch probes.
The final conversion preserved structural wood in 5,638 overlapping cells;
all 450 fork/tip probes reach the trunk through face-connected exported logs.

## Small Colossus V6

Authored chamfered cross-sections replace the ellipsoid torso, shoulder cores,
helmet core and hip. Twenty-five closed shield-like plates overlap across the
chest, shoulders, back, temple and hand heels. The continuous heavy plated body,
six lenses, arched grille and grounded pincers remain tied to the
[Vigilant reference](../../relics/colossus/docs/SMALL_COLOSSUS_V4_REFERENCE.md).

The upper body pitches farther forward and compresses downward into the chest;
low hand contacts remain grounded. The smaller export has 71 visible layers
rather than V5's 75. Light-gray terracotta replaces pale sandstone on the blade
tines, and plated heels visually join them to the grippers. The rear remains an
authored completion of anatomy obscured in the reference.

## Ruined Tower V4

The height remains 220 visible layers. Front and rear upper walls now end on
different irregular fracture profiles, with additional losses along the sky
slots. The previously complete lowest stair has a six-tread central break,
chipped surviving noses and fallen masonry. Five interrupted inner masonry
patches and narrow repair seams add relief to the broad wall faces. Original
threshold and arch void probes remain open; the new stair gap is also checked.

## Reproduction and selection

```powershell
.work/python/Scripts/python.exe tools/build_relic_v2.py world-tree-v4
.work/python/Scripts/python.exe tools/build_relic_v2.py small-colossus-v6
.work/python/Scripts/python.exe tools/build_relic_v2.py ruined-tower-v4
.work/python/Scripts/python.exe tools/review_alpha42_art.py
node --test tests/*.test.cjs
```

Each candidate has an editable source Blender file, OBJ/MTL, schematic, whole
NBT, lossless tiles, metadata, verification and actual-block renders. Preserved
V3/V5 comparison-source hashes are checked. Conversion uses the pinned upstream
commit and keeps DataVersion 3105.

The packaged Alpha 4.2 selection and its terrain/runtime evidence describe the
earlier V5/V3/V3 models. The user requested integration of the new candidates;
Alpha 4.3 now selects V6/V4/V4. Its own runtime and installation evidence is kept
in the [Alpha 4.3 report](../testing/ALPHA_4_3_TEST_REPORT.md). Client visual
acceptance is still pending; Alpha 4.2's evidence does not certify the new art.

## Verification

All three build pipelines passed source/export hashes, exact schematic/NBT
block-state equivalence, palette/bounds checks and lossless tile reconstruction.
Feature checks passed: 450 trunk-connected woody probes, 25 connected armour-plate
probes plus six lenses/grille/pincers and filled cores, and four Tower void probes
plus 16 structural probes and the exact 220-layer visible height. The seven Node
regressions passed, including both overlap hit orders and restoration after a
failed conversion. The comparison sources were hash-checked without regenerating them.

NBT SHA-256 values:

```text
World Tree V4     3f19512d5d1d97ccd5efa2af59d30ef8ffa48c0269535ff472ec2586063f16e8
Small Colossus V6 003075edc4e29e940c4fcdefb16da1c16202f7551a73be8a39a028e228771bab
Ruined Tower V4   9bacd9d4792b37239d35a03ef4944c907d5d3ae49e217223eab127b962fd377c
```
