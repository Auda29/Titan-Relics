# Alpha 4.4 screenshots — deposit relief and lower Tower walls

The user selected the two remaining issues from the 35-image Alpha 4.4 review:
regular concentric soil/rock terraces, and the Tower's rectangular lower walls.

## Ground derivatives

The concentric forms are largely authored into the raw deposits, not just the
runtime foundation. `tools/deposit_relief.py` sculpts these exported block fields
with coherent, unequal erosion patches and shallow channels. It lowers outer
surfaces, interrupts repeated contour rings and varies exposed surface material
using the existing biome palette. It does not scatter isolated random holes.

All non-terrain blocks are preserved exactly. Materials shared between terrain
and anatomy are protected as art (notably Skull 2 moss). Contact columns adjacent
to bones, roots and masonry are locked, including soil above buried root tips.
The builder additionally compares the old/new derived foundations: if a root tip
relies on a neighboring foundation toe, that toe's source soil is locked and
erosion recalculated. A build fails if any formerly supported art cell acquires
air below it. This caught low Tree root edges during development.

Eight candidates cover the four crowned-Skull palettes, Small Colossus V7,
World Tree V4.1, Tower V6 and Skull 2 V1. Their names append `-ground-v2` to the
preserved source version. Dimensions, nominal burial and DataVersion remain
unchanged. The accepted Tree wood and foliage remain exact exported-block matches.

These are explicitly **block-space terrain derivatives**, not fresh OBJ exports.
Each stores source checksum, schematic, NBT, lossless tiles, design/derivation
metadata and verification. The original editable Blender models remain their
source art. The reproducible ground operation is applied after their export.
The converter configurations are identified by `authoring: block-terrain-derivative`;
use the dedicated builder below rather than passing them to ObjToSchematic.

## Ruined Tower V6

Both lower annexes now have large losses entering from above, unequal wall stubs,
opened lower breaches, exposed masonry and fallen fragments. This removes the
continuous rectangular outer-wall silhouette visible in screenshots 31 and 33.
The lower main shell also receives three substantial breaches. Side cuts go
through both shell and grounding skirt, and rear stringcourses are broken at
the opening rather than left floating across it.
The upper tower retains 220 visible layers. Its baseline V6 export is
111 × 232 × 93, 298,355 blocks and 69 tiles. Thirteen void probes and 16 structural
probes pass, including both new upper annex losses.

V6 is authored in Blender and exported through the existing OBJ → schematic →
NBT pipeline. The final `ruined-tower-v6-ground-v2` then applies the same terrain
operation as the other seven candidates.

## Measured final derivatives

| Candidate | Blocks | Removed soil cells | Modified soil columns |
| --- | ---: | ---: | ---: |
| Crowned Skull, each of four palettes | 123,861 | 12,708 | 5,536 |
| Small Colossus V7 ground-v2 | 233,492 | 2,441 | 1,843 |
| World Tree V4.1 ground-v2 | 292,646 | 1,045 | 994 |
| Tower V6 ground-v2 | 297,352 | 1,003 | 884 |
| Skull 2 V1 ground-v2 | 85,152 | 72 | 71 |

The eight derivatives remove 55,393 soil cells in total. Every non-terrain cell
matches its source exactly (Tower uses the newly authored V6 as its source).
791,876 art-cell underside checks find no new air after deriving foundations.
Source hashes, full schematic/NBT equality and lossless tile reconstruction pass
for all eight exports. These metrics measure geometry and support preservation,
not aesthetic acceptance or runtime terrain placement.

## Reproduction

```powershell
.work/python/Scripts/python.exe tools/build_relic_v2.py ruined-tower-v6
.work/python/Scripts/python.exe tools/build_deposit_relief.py --tower-v6
.work/python/Scripts/python.exe tools/review_deposit_relief.py
python -m unittest discover -s tests -v
```

The comparison uses actual NBT at identical scale within each pair. The Tree row
focuses on the root feet and the Tower row on the lower 60 visible layers.
Full-size comparison renders and the build index are local under
`.work/deposit-relief-review/` and `build/deposit-relief/`.

[Open the before/after review](reviews/deposit-relief-20261006.png).

## Scope of validation

The erosion and support checks operate on raw and derived templates. They do not
certify a new Minecraft world-generation run. Alpha 4.4 and its saved-world
evidence describe the preceding exports. The user requested integration of all
new updates; Alpha 4.5 selects the eight final derivatives. Its separate runtime
validation and installation are recorded in the
[Alpha 4.5 report](../testing/ALPHA_4_5_TEST_REPORT.md).

The full Python regression suite passed **75 tests**, including three new
erosion/contact-preservation cases and the typed block-derivative asset layout.
An earlier run found the new schema was not yet handled by the layout test;
that failure was corrected and the complete suite rerun successfully.
