# October 5 — revisions from the in-game screenshot review

The later Alpha 4.2 screenshots led to another
[art follow-up: Tree V4, Small Colossus V6 and Tower V4](ALPHA_4_2_ART_FOLLOWUP.md).
The candidates and runtime discussion below describe the earlier revision.

The user supplied six contact sheets (22 screenshots) under
`build/screenshot-review/20261005/` and agreed with the review priorities:
terrain joins, the small Colossus's toy-like symmetry, the World Tree's compact
leaf pads, and the tower's uniform facades and empty shaft.

The screenshot candidates remain preserved. New revisions are visual candidates,
not user-approved replacements. The reel Da-s0zqi7OQ remains the small Colossus's
[primary reference](../../relics/colossus/docs/SMALL_COLOSSUS_V4_REFERENCE.md).

## Review images

- [Three same-scale before/after comparisons](reviews/screenshot-revisions-20261005.png)
- [Controlled downhill foundation comparison](reviews/terrain-foundations-20261005.png)
- [Small Colossus V5](../../relics/colossus/design/generated/small-colossus-v5/small-colossus-v5-review.png)
- [World Tree V3](../../relics/world-tree/design/generated/world-tree-v3/world-tree-v3-review.png)
- [Tower V3 interior cutaway and facade details](../../relics/ruined-tower/design/generated/ruined-tower-v3/ruined-tower-v3-detail-review.png)

These are Blender renders of actual exported NBT, not new Minecraft screenshots.
The original in-game screenshots remain local, under `build/`.

| Raw export | Dimensions X × Y × Z | Blocks | Ground Y | Visible layers |
| --- | --- | ---: | ---: | ---: |
| Small Colossus V5 | 115 × 84 × 119 | 248,549 | 9 | 75 |
| World Tree V3 | 175 × 216 × 147 | 311,602 | 8 | 208 |
| Ruined Tower V3 | 111 × 232 × 93 | 333,223 | 12 | 220 |

## Small Colossus V5

V4's continuous armour and six optics are retained, with a continuous sideways
list and forward slump, deeper local dents, staggered dorsal plates and coherent
weathering patches. Low hand contacts stay grounded rather than being lifted by
the upper-body deformation. Bright yellow terracotta becomes muted terracotta,
brown/gray mineral weathering and exposed-copper trim. Burial is higher on one side.

Source: `tools/create_small_colossus_v5.py`; config:
[small-colossus-v5.json](../../relics/colossus/design/small-colossus-v5.json).
The V4 Blender file is read-only and its hash is checked after generation.

## World Tree V3

Ten unequal primary boughs carry 70 secondary branches distributed along their
lengths, 280 fine terminal forks and 840 smaller foliage sprays. Exposed terminal
twigs and uneven crown gaps replace the large closed end cushions. The trunk,
root system and overall export height remain based on V2. Leaves are persistent.

Source: `tools/create_world_tree_v3.py`; config:
[world-tree-v3.json](../../relics/world-tree/design/world-tree-v3.json).

## Ruined Tower V3

The 220 visible layers and original footprint are retained. Six unequal partial
storeys, corbels, three broken stair flights, interrupted facade ribs/stringcourses
and further chipped crown edges now articulate the structure. Original threshold,
arch and sky-slot probe locations stay open. These are architectural remnants,
not a finished playable dungeon route.

Source: `tools/create_ruined_tower_v3.py`; config:
[ruined-tower-v3.json](../../relics/ruined-tower/design/ruined-tower-v3.json).

## Terrain joins in natural generation

`tools/terrain_foundations.py` extends near-ground authored terrain columns down
to four blocks below the permitted downhill surface difference. It adds no whole
rectangular platform. Earth uses dirt; sandy contacts use stable sandstone;
rock/gravel contacts use stone. Raw model exports stay byte-identical in manual
templates. Only derived natural templates gain the foundation, vertical padding
and matching placement-height adjustment. An eight-block-wide stepped toe falls
two blocks per outward step, softening downhill skirts; the natural template is
padded horizontally to contain it. Missing cells still preserve native terrain.

The placement grid retains 25 samples across the padded footprint. An 81-point
trial triggered a locator watchdog and was rejected. Small unsampled ravines and
caves remain possible; the saved-world verifier now explicitly checks every
lowest terrain column for solid contact below it and reports unsupported columns.
It compares the actual natural template, including its Y padding, rather than
incorrectly comparing that placement to an unshifted raw model.

Existing generated structures are not retroactively changed. Manual `/place
template` still places the raw art export; use natural generation to review the
foundation correction.

## Reproduce

```powershell
.work/python/Scripts/python.exe tools/build_relic_v2.py small-colossus-v5
.work/python/Scripts/python.exe tools/build_relic_v2.py world-tree-v3
.work/python/Scripts/python.exe tools/build_relic_v2.py ruined-tower-v3
.work/python/Scripts/python.exe tools/review_screenshot_revisions.py
.work/python/Scripts/python.exe tools/review_terrain_foundations.py
python tools/build.py
python -m unittest discover -s tests -v
```

The candidate artifact is Alpha 4.1. Prior Alpha 4 evidence remains historical
and does not establish runtime acceptance for this new artifact.
The raw Minecraft showcase passed; **natural terrain placement failed** with
remaining unsupported foundation columns. The terrain correction is incomplete.
See the [Alpha 4.1 runtime report](../testing/ALPHA_4_1_TEST_REPORT.md) for the new
checksum, showcase, natural-terrain results and rejected intermediate trial.
