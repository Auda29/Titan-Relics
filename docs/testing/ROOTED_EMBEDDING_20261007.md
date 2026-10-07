# October 7 — deeper, platform-free model candidates

The user requested changes to three Alpha 4.7 screenshot findings: rock Skull
(image 40), Skull 2 (53/54), and World Tree roots (48). The resulting **Alpha 4.8
candidate** uses the natural ground surface and deeper model burial. It is an
isolated review package, built by `tools/package_rooted_candidates.py`; the
standard asset selection/build remained Alpha 4.7 during candidate preparation.
The later user request now selects these same exports in
[Alpha 4.8 integration](ALPHA_4_8_TEST_REPORT.md); the subset evidence below stays
historical and is not promoted to full-pack acceptance.

- [Same-site before/after comparison](../project/reviews/rooted-embedding-20261007.png)
- [Comparison provenance and texture fallbacks](../project/reviews/rooted-embedding-20261007.json)
- [Pinned candidate selection](../project/rooted-candidates-20261007.json)
- [Completed runtime evidence](rooted-embedding-20261007-evidence.json)
- [Tree contacts](rooted-embedding-20261007-tree-contacts.json)
- [Runtime additions and strict cavity audit](rooted-embedding-20261007-runtime-audit.json)

## Model changes

| Relic | Removed authored ground | Additional burial | Result |
| --- | ---: | ---: | --- |
| Rock Skull | 91,157 stone/gravel cells | 6 blocks | 20,131 art cells; ground Y22 |
| Skull 2 | 14,353 dirt/rooted-dirt/grass cells | 6 blocks | 32,569 art cells; ground Y28 |
| World Tree | 4,755 earth + 26 low moss cells | 4 blocks | 324,127 cells, including 37,005 new wood cells |

Both Skulls retain every anatomical block and its coordinates. Skull 2's brown
terracotta is anatomy, not removed ground. Its rigid sword, bone contact and
four raw-NBT cavity probes are preserved. Greater burial reduces exposed low
anatomy, particularly the rock Skull's trailing vertebrae.

The Tree keeps every accepted V4 wood/leaf cell under a declared uniform +12 Y
export translation. This adds space below the old export for roots; ground moves
to Y24, equivalent to old-source Y12, so the accepted art sits four blocks lower
in the world. The extension continues 3,560 low wood columns with depth based on
footprint thickness and adds 14 tapering forks along seven existing root groups.
All 37,005 added cells are face-connected to original wood. Existing branches,
root curves and foliage are retained; only new low wood and the explicitly
mutable ground/low moss pads differ.

New exports are NBT/schematic derivatives with reproducible block-authoring
scripts and source hashes. Earlier exports remain available. No replacement
Blender source is claimed for these block-level derivatives.

## Natural embedding

`foundation_mode=embedded_art` bypasses authored soil-column/toe generation,
preventing the stripped platforms from regrowing around anatomical moss or
sword stone. Only padded original art is exported into the natural template.
The existing surface anchor, dry-land grid, biome, density, separation and slope
rules still apply.

The optional `root_support` processor flag continues exposed low log undersides
using their own block state, rather than dirt. Other low anatomical contacts use
the existing local stone/dirt contact processor; raised arches remain open.
The flag defaults to false and is enabled only for this Tree candidate.
The saved Tree has 1,469 extra runtime log cells and 23 dirt cells beneath
non-log contacts. Rock Skull adds 1,441 runtime stone cells; Skull 2 adds 1,197
dirt cells. These local contact fills all lie below nominal ground; there is no
authored perimeter platform or generated talus toe.

## Saved-world verification

Natural run `run-20261007-083649-7249c75a1654` regenerated the three Alpha 4.7
sites in seed **731204**, using nominated candidate chunks through the normal
natural-start pipeline. Origins match horizontally, rotations match, and
nominal world surface heights match the baseline.

| Relic | Checked model/mask cells | Exposed low undersides | Unsupported |
| --- | ---: | ---: | ---: |
| Rock Skull | 20,131 | 4,330 | 0 |
| Skull 2 | 32,569 | 9,173 | 0 |
| World Tree | 324,127 | 4,276 | 0 |
| Total | **376,827** | **17,779** | **0** |

All compared model cells match; all template mask cells are present. No missing
or incomplete chunks, overlapping structures or read errors were found. The
separate Tree check finds zero ground-level root gaps. It also reports 175
raised root edges one or two blocks above nominal ground; these are not treated
as ground-level contact failures or automatically filled.

Showcase run `run-20261007-084710-fc7993ec449d` independently placed the three
complete raw exports, including their buried geometry: **376,827 checked blocks,
zero mismatches**. Both candidate servers exited normally with code 0 and the
default **60000 ms watchdog**, using the same candidate artifact hash.

The strict air-only cavity audit deliberately remains **failed**: three native,
nonpersistent oak-leaf cells occupy the edge of one lowered Skull 2 cavity
probe. All three have exactly the same states at the same world coordinates in
the Alpha 4.7 baseline and have no relic protection bits in either world. The
old, higher probe positions were clear. This is retained native vegetation now
intersecting the lowered opening, not changed bone, added terrain or a filled
raw-NBT opening. The record preserves the failure and per-cell baseline evidence;
there is no claim that all natural cavity probes are air-only.

The comparison image renders actual saved-world block crops with identical
site bounds and scale. It uses approximate preview textures, omits listed small
non-cube plants, and shows only the Tree's root region. It is not a Minecraft
client screenshot or a claim of final artistic approval.

## Build and reproduction

Review JAR:
`build/rooted-embedding/20261007/relics-0.1.0-alpha.4.8-candidate+mc26.2.jar`

SHA-256: `071c9e83d308c489234b4d856d6fad9f9b502c62d16d2f1cfe40ebf54815a7fc`.

Regenerating all three candidates and rebuilding the JAR reproduces the same
candidate index, NBT hashes and JAR bytes. Java runtime tests pass **751
assertions**, including wood-only low-root continuation and retained higher
arches. The initial Python run exposed three configuration-layout errors: the
new block-derivative authoring type was being checked as an OBJ input. Its layout
check now validates source-NBT provenance, declared translation and zero authored
terrain using the new derivative metadata.
The final full Python suite passes **89 tests**, including documentation links
and exact retained art. `git diff --check` also passes. This does not reclassify
the separately documented strict air-only cavity observation as passing.

```powershell
python tools/build_rooted_candidates.py
python tools/package_rooted_candidates.py
python -m unittest discover -s tests -v
python tools/test_worldgen_java.py
python tools/smoke_server.py --accept-eula --quiet --artifact build/rooted-embedding/20261007/relics-0.1.0-alpha.4.8-candidate+mc26.2.jar --structure titan_skull_rock --structure titan_skull_2 --structure world_tree --natural-candidates build/rooted-embedding/20261007/same-sites.json
python tools/smoke_server.py --accept-eula --quiet --showcase --artifact build/rooted-embedding/20261007/relics-0.1.0-alpha.4.8-candidate+mc26.2.jar --structure titan_skull_rock --structure titan_skull_2 --structure world_tree
```

The nomination file uses seed 731204 with these chunk-aligned X/Z positions:
rock Skull `[-9024, 35664]`, Skull 2 `[-13168, 36272]`, Tree `[23712, -45504]`.
`tools/extract_rooted_sites.py` records the crop and report hashes in its manifest;
`tools/render_rooted_sites.py` builds the comparison. Additional audit commands
are `tools/verify_tree_contacts.py` and `tools/audit_rooted_sites.py` with the
natural report; the latter accepts `--baseline-report` for the leaf evidence
and returns exit code 1 while its strict air-only condition is unmet.

This is a three-model review candidate. These subset runs do not constitute the
full ten-variant installation gate, global-locator performance acceptance or
terrain-mod compatibility testing. No profile installation is included.
