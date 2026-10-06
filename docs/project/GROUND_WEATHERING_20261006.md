# October 6 — root contacts, tower sides and weathered Colossus

The user reviewed the 13 Alpha 4.3 screenshots, accepted the World Tree's form
and foliage, and limited its follow-up to ground connections. The user agreed
with the Tower side-wall/foot critique and requested a more weathered, overgrown
Small Colossus resembling the dormant reference specimen.

## Small Colossus V7

V6's body and pose are retained. The editable model now has localized rust,
patina and weathering runs, moss on sheltered ledges and close-fitting irregular
moss mantles over shoulders, rear plates and hands. Growth is projected onto
the actual surfaces rather than arranged as separate spherical bushes. The
reference at 3 seconds particularly shows accumulated material and growth on
the foreground hand; coverage of the obscured back is an authored completion.

The exported body is 111 × 80 × 113, with 235,933 blocks and 71 visible layers.
There are 6,047 moss/green-terracotta cells above nominal ground +4, alongside
weathered copper patina. Six head lenses, the grille, pincers, filled cores and
25 connected armour-plate probes pass validation.

**Buried anatomy:** the raw model includes nine layers below its nominal ground
line, containing 9,717 structural cells below that line. The solid lower torso
and hip continue into this region; it is not a
fully modeled buried pair of legs. Natural placement adds earth foundations and
runtime supports to real terrain. Those supports are soil, not hidden anatomy.

## Ruined Tower V5

Four new ragged openings break the broad side elevations at unequal heights.
Recessed partial panels, interrupted stringcourses and exposed masonry ends
add actual relief. Lower annexes also have side damage. The pale sandstone
apron is replaced with lower grass/rooted-earth deposits and dark rubble trails.

Export: 111 × 232 × 93, 307,417 blocks, 69 tiles, **220 visible layers**.
All eight void probes (including the four side breaches) and 16 structural
probes pass. The preserved V4 source remains hash-checked.

## World Tree ground audit and V4.1

Read-only inspection uses the saved Alpha 4.3 natural run
`build/smoke/run-20261005-124958-97f7626d565d/world`, not the live player save.
The Tree instance has 8,933 soil-foundation columns, all supported in the runtime
report. Inspecting lowest wood cells at/below nominal ground +2 separately found
3,472 direct contacts and 88 columns with 1–4 blocks of air beneath them.
Of these, nine are at nominal ground -1, 20 at ground, 14 at +1 and 45 at +2.
These are low root edges/arches, not disconnected wood components or failing
earth-support columns. Taller intentional arches are outside this sample.

V4.1 adds only two narrow, low earth transitions at the affected root-foot
regions. Its validator requires every non-terrain exported cell—including
wood, foliage, moss and root stones—to match accepted V4 exactly. The source
tree is imported directly; branches and crown are not regenerated.

Changing the soil mesh can reorder two coincident wood/bark ray hits in the
voxelizer. The ground-only conversion therefore restores accepted wood/wood
material ties from the checksum-verified V4 schematic. This pass rejects changed
non-terrain positions and changes involving any other material; it cannot hide
a moved branch or lost foliage. The final schematic and NBT must still match
every accepted non-terrain cell exactly.

Local audit output and labeled saved-world cross sections are in
`build/screenshot-review/20261006-alpha4-3/ground-audit/`.
Any candidate overlay on that world is a read-only projection, not a fresh
Minecraft generation test.

The final V4.1 export is 187 × 216 × 185 with 293,691 blocks and 124 tiles.
Every non-terrain block is exactly identical to V4; all 450 woody probes remain
trunk-connected. The saved-site projection closes 52 of the 88 sampled gaps,
including **all 29 at or below nominal ground**. The 36 remaining gaps are under
raised root edges at ground +1/+2. The two low deposits extend below the wood
so that their earth columns can be recognized by the support processor.

## Review and reproduction

[Before/after actual-block comparison](reviews/ground-weathering-20261006.png)
shows the Colossus, a side-biased Tower view, and the ground-only Tree revision.
Each pair shares block scale and camera. Rendered surrounding terrain is illustrative.

```powershell
.work/python/Scripts/python.exe tools/build_relic_v2.py small-colossus-v7
.work/python/Scripts/python.exe tools/build_relic_v2.py ruined-tower-v5
.work/python/Scripts/python.exe tools/build_relic_v2.py world-tree-v4-1
.work/python/Scripts/python.exe tools/audit_tree_ground.py --candidate
.work/python/Scripts/python.exe tools/review_oct06_art.py
```

These are new art exports for review. Alpha 4.3 and its recorded runtime
acceptance select Small Colossus V6, Tree V4 and Tower V4. The user requested
integration of V7/V4.1/V5 and a push of all pending project work. Alpha 4.4 now
selects those exports; its own runtime, ground-contact and installation results
are kept in the [Alpha 4.4 report](../testing/ALPHA_4_4_TEST_REPORT.md).

## Checks

All three final exports passed complete source/hash, schematic/NBT equivalence,
palette, bounds and lossless-tile checks, as well as their structural/feature
probes. The Python regression run passed 64 of 65 tests initially; its only
failure was the comparison image link before that render existed. All four
repository-layout/link tests passed after rendering. Both new preservation
regressions pass: wood-hit normalization preserves soil edits, while moved wood
and changed foliage are rejected. Python compilation and whitespace checks pass.

Final NBT SHA-256:

```text
Small Colossus V7 c48bb70ea3643070e94a44008721cb5c08fda74f80b4efee2e063a44b5436bb4
Ruined Tower V5   5be62afb4d6a3968e37c61b54e21941273c795921441dc9db8e705ced9f2765f
World Tree V4.1   b8235fd957029d39a534eef2f13924bc850155e46fd5872fc40f51ecce8eea37
```
