# October 7 — Skull 2 cave footprint and branching Tree roots

The user selected two findings from the twelve Alpha 4.8 screenshots: Skull 2's
earth belt/deep cave intrusion and the Tree's broad wooden cave curtains. The
rock Skull is explicitly deferred. This is a separate **Alpha 4.9 candidate**;
its index overrides only Skull 2 and Tree in the review JAR.

The later integration request selects these exact contracts in
[the default Alpha 4.9 build](ALPHA_4_9_TEST_REPORT.md). The subset candidate runs
below remain historical and are not promoted to complete installation acceptance.

- [Candidate contracts](../project/cave-candidates-20261007.json)
- [Surface before/after](../project/reviews/cave-contacts-surface-20261007.png)
- [Root cave cutaway](../project/reviews/cave-roots-cutaway-20261007.png)
- [Cutaway provenance](../project/reviews/cave-roots-cutaway-20261007.json)
- [Exact world-coordinate slices](../project/reviews/cave-contacts-20261007.png)
- [Overview/slice provenance](../project/reviews/cave-contacts-20261007.json)
- [Runtime evidence](cave-contacts-20261007-evidence.json)
- [Independent support/cave audit](cave-contacts-20261007-audit.json)
- [Tree contact classifications](cave-contacts-20261007-tree.json)

## Changes

### Skull 2

The 32,569-cell raw anatomy/sword export is byte-identical to Alpha 4.8, including
the brown anatomical material. Ground remains **Y28**. Only the derived natural
template omits the buried slice below raw **Y22**, six blocks below nominal ground.
This excludes **7,309** deeply buried cells from natural placement, leaving
**25,260** authored natural cells. Native rock and cave air remain in that deep
slice. The complete original export remains available in the raw showcase.

The contact processor adds at most two cells per short gap, using the adjoining
bone, calcite, dripstone or moss state. It no longer paints a dirt wall under
these anatomical contacts. Longer gaps are left wholly open, without a partial
two-block hanging column. The profile operates only within six blocks below
nominal ground, not down to the dimension floor.

### World Tree

The new `world-tree-v4-3-strands` derives from the pinned pre-extrusion
`world-tree-v4-1-ground-v3` export. Every accepted V4 log and leaf is exact after
the same +12 Y export translation used by Alpha 4.8. World placement stays at
Y24, so the accepted Tree shape does not shift. Only the mutable earth/low moss
pads and the later root additions are replaced.

Instead of 37,005 added wood cells extruded beneath the entire low footprint,
there are **1,883 new face-connected wood cells** along **50 curved strand/fork
paths**. Their radii taper toward the tips. Sparse branching leaves open space
between the roots. The total raw/natural export is **289,005 cells**.

Runtime root contact is also limited to two cells and starts only within three
blocks below nominal ground. Deep root endpoints and longer cave gaps do not
grow vertical piers. The saved-world audit checks every actual added run for its
length, material/state, authored attachment, native substrate and surface band.

All eight other raw and derived natural templates, including the rock Skull and
the Tower, compare byte-for-byte with Alpha 4.8. Their processor settings retain
the unbounded legacy defaults. Biomes, density, slopes, separation and the
25-point terrain grid are unchanged.

## Explicit contact semantics

This design deliberately permits open root undersides in caves. It must not be
reported as the old "zero gaps anywhere at/below nominal ground" result.

The verifier still records all observed clearances. For the two limited profiles,
an unfilled short surface gap fails; deep root clearances or gaps longer than
the configured maximum are reported as intentional. Missing saved cells fail
closed. Old profiles retain their strict foundation/contact behavior.

The Tree's lowest-log audit records **3,995 direct contacts**, **169 intentional
clearances at/below nominal ground**, and **174 raised edges** above nominal
ground. No expected wood is missing and there are zero unexpected short gaps.
The separate exposed-run audit checks every low underside, including multiple
runs in one column; its counts therefore differ from the lowest-log audit.

## Same-site cave checks and iteration history

The seed remains **731204**, with the actual Alpha 4.8 Skull 2 and Tree candidate
chunks. Tests use natural starts at the same horizontal origins/rotations.
The scoped cave boxes are fixed world-coordinate regions recorded in the audit.

- The deep Skull cave region previously contained 465 protected relic cells;
  the corrected footprint leaves that region to native cave/rock generation.
- In the north Tree cave, added geometry drops from **1,686 to 159** cells.
  All **523** accepted source-art cells in that box remain.
- In the west Tree cave, added geometry drops from **2,376 to 201** cells.
  All **304** accepted source-art cells in that box remain.

An initial diagnostic incorrectly applied a 75% reduction target to *all* Tree
relic cells, including accepted source roots that must be preserved. Its north
box retained 30.9% and failed that total-volume heuristic. The archived result
is `build/cave-contacts/20261007/initial-total-volume-audit.json`. The final audit
keeps the raw totals, proves original-art preservation separately, and applies
the same reduction target to the later extrusion/support geometry. This is an
audit-scope correction, not removal of accepted roots to satisfy a threshold.

The first candidate also lowered Skull 2 two additional blocks (Y30). Its core
natural/showcase checks passed, but a 108-cell face-opening check found nine
native grass blocks, three short-grass cells and one leaf in the lowered probe.
That extra burial was rejected. The intermediate JAR, index and probe record
remain under `build/cave-contacts/20261007/initial-deeper-skull/`; its two runtime
runs remain in the compact evidence. The final Y28 profile must retain exactly
the baseline probe contents, including the previously documented three native
leaves; a regression is a failure. This is not an air-only opening claim.

## Validation and reproduction

Final-artifact natural run `run-20261007-114624-97e7a0fcf6f1` verifies **314,265
model/mask cells**, zero mismatches, zero missing/incomplete chunks or overlaps.
Its limited-contact audit reports 176 intentionally open Tree undersides;
the independent lowest-log result above describes the 169 unique lowest-column
clearances rather than every separate exposed run. Skull 2 reports 178 longer
clearances; these are deliberately not bridged by new columns. Both profiles
report zero unsupported short surface gaps under the stated bounded policy.
Final showcase `run-20261007-114624-f39200957f1a` verifies **321,574 complete raw
model cells**, zero mismatches. Both servers exit normally with code 0 and the
standard **60000 ms watchdog**.

The final saved additions comprise 448 short Skull contacts (bone, dripstone,
moss and calcite) and 293 Tree contacts (271 log and 22 mossy-stone-brick cells).
There are **zero added dirt cells** and no added run longer than two cells.
All 108 face-probe cells have the same contents as Alpha 4.8; the existing three
native leaves remain explicitly recorded as a failed strict air-only category.

The full Python suite passed **95 tests**, Java checks passed **755 assertions**.
Focused cave/Tree tests were repeated after the explicit clearance/missing-cell
checks and final Skull burial constraint were tightened. The sources and prior
exports are preserved; no profile installation is part of this candidate task.

```powershell
python tools/build_cave_candidates.py
python tools/package_rooted_candidates.py --selection docs/project/cave-candidates-20261007.json --output build/cave-contacts/20261007 --version 0.1.0-alpha.4.9-candidate --revision 2026-10-07-open-caves-and-root-strands
python -m unittest discover -s tests -v
python tools/test_worldgen_java.py
```

Artifact: `build/cave-contacts/20261007/relics-0.1.0-alpha.4.9-candidate+mc26.2.jar`.
SHA-256: `e573c5bc972118953606ca95ffdebd6b67b69dca135fec58b6e2d1aaddcc0794`.
During candidate preparation, regenerating the Tree/index and rebuilding the
package reproduced those bytes exactly. The later default integration uses its
own version/revision and explicitly versioned runtime policy; it checks the
candidate templates, resources and Java classes rather than claiming a
byte-identical historical candidate JAR. Documentation links and `git diff --check` pass. The final
root-cutaway crops are byte-identical to the first candidate's crops; their
rendered pixels are reused with final-report provenance. The changed Skull
surface overview and matched slices were regenerated from the final world.

The natural smoke command uses `--structure titan_skull_2 --structure world_tree`
and the original same-site nominations, with `--artifact` pointing to that JAR.
The raw showcase uses the same structures/artifact plus `--showcase`.
`tools/audit_cave_candidates.py` and `tools/review_cave_contacts.py` accept explicit
`--before`/`--after` reports; `tools/render_cave_cutaway.py` accepts those too.

Images show saved block geometry at matched sites. Surface views have approximate
preview textures and omit small plants. The detailed 3D cutaway hides the native
foreground half-space **only for the view**, retaining every relic cell in its
crop; the worlds are not edited. The slices use schematic material colours.
These are diagnostic renderings, not new client screenshots or artistic approval.
The two-template candidate runs do not constitute the ten-template installation
gate, global-locator timing acceptance or terrain-mod compatibility tests.
