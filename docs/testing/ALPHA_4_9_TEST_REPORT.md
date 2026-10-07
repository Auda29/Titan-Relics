# Alpha 4.9 — shallow Skull footprint and sparse Tree roots

October 7, 2026. Minecraft 26.2 / Fabric.

The user requested integrating the new structure updates, a separate natural
terrain showcase, a push and a release tag. The two exact
[cave-contact candidates](CAVE_CONTACTS_20261007.md) are selected in the default
build. No additional artistic changes, gameplay or terrain-mod compatibility
claims are introduced. All historical source exports remain preserved.

## Subsequent client visual acceptance — October 7

After inspecting the updates, the user stated: "habe wieder ein paar screenshots
gemacht von den updates. finde das die beiden relikte so jetzt abgenommen sind."
**Skull 2 and World Tree are therefore visually accepted in their released
Alpha 4.9 appearance and terrain integration.** The
[acceptance record](../project/reviews/alpha4-9-user-acceptance-20261007.json)
pins the existing commit, JAR and template hashes, with eight 1920 × 1054 user
screenshots from 12:23:32–12:25:07 (three Skull, five Tree). Unchanged native copies
and two numbered contact sheets remain in the local screenshot-review archive.

This subsequent documentation does not modify models, placement/runtime policy,
packaged resources, the installed JAR or saves. It does not approve other relic
revisions or complete gameplay. Intentional cave clearances and the three native
Skull 2 leaves remain in the technical evidence below. Candidate/manifests retain
their pre-acceptance metadata; no rebuild, commit, push or tag change is part of
recording this acceptance.

## Selection and explicit cave policy

- **World Tree V4.3 strands:** 289,005 raw cells. The accepted art is retained
  under the existing +12 Y export translation; ground Y24 and world pose are
  unchanged. Replace the later 37,005-cell extrusion with **1,883 attached wood
  cells along 50 tapered strand/fork paths**.
- **Skull 2:** the complete 32,569-cell embedded-v1 raw anatomy/sword export and
  ground Y28 are unchanged. Its natural template alone omits 7,309 deeply buried
  cells below raw Y22, leaving 25,260 authored natural cells and preserving native
  cave rock/air in that slice.
- Both profiles add only short contacts up to two cells using the adjoining
  authored material. Tree contacts start within three blocks below ground;
  Skull contacts within six. Long gaps are left entirely open without hanging
  partial stubs; deep root endpoints do not generate foundation piers.
- Eight other raw/natural template pairs, including rock Skull, are unchanged.
  Skull 2's raw export also remains byte-identical. Dependencies, density,
  biomes, burial/anchors, slopes, separation and the 25-point grid are unchanged.

**Intentional cave clearances are not "zero gaps anywhere" acceptance.** The
verifiers retain raw observations, classify permitted deep/long clearances for
these two explicit profiles, reject missing saved cells and reject unfilled
short surface contacts. Other profiles retain their previous strict behavior.
An independent saved-mask audit checks attachment, native substrate, materials,
surface band and the actual length of every added support run.

The established omitted-air policy preserves the three native leaves in Skull
2's face probe. Same-site cavity contents must match Alpha 4.8; a regression
fails. The strict air-only category remains separately false, not relabeled as
passing. Extra Skull burial from the rejected Y30 candidate is not selected.

## Build and regression checks

Final default artifact: `dist/relics-0.1.0-alpha.4.9+mc26.2.jar`.
SHA-256: `3dbffadf501cbc3dee3ffa66ca78f04fa5b6c6032c66f511832c47aa9d45ba22`.

The final full Python suite passes **97 tests**; Java runtime tests pass **755
assertions** and JavaScript tests pass **7 tests**. Default and skip-generation
JARs are byte-identical. The new strands and preserved Alpha 4.8 rooted contracts,
NBT/schematic bytes and provenance reproduce exactly in an isolated directory.
All candidate templates, worldgen resources and Java runtime classes match the
final default JAR; its version/revision/runtime-policy manifest is distinct.
Historical generators explicitly exclude the later cave-policy flags so their
previous geometry and placement contracts remain reproducible.

## Fresh runtime and installation

The [runtime evidence](alpha4-9-evidence.json) records two fresh complete
**ten-variant** runs of the final artifact, with seed **731204** and the ordinary
**60000 ms watchdog**:

- Raw showcase `run-20261007-120404-a465bce0759b`: **1,499,248 checked raw blocks**,
  zero mismatches, complete bounds/chunks and normal exit 0.
- Natural `run-20261007-120415-8ab6c782fdc6`: all ten actual starts found through
  ordinary global `/locate`, **1,379,680 checked non-excluded model cells**,
  zero mismatches, missing/incomplete chunks, overlaps or read/verification errors.
- **67,209 support undersides** are examined. No unexpected unsupported contacts
  remain. The bounded profiles explicitly report **178 Skull clearances and 177
  Tree clearances**, not direct substrate contact at every underside.
- **1,682,709 template protection-mask cells** checked; zero unprotected cells.
  Persistent-leaf distance normalization and natural dirt/grass/azalea-leaf
  exclusions retain the established comparison rules.
- Both servers exit normally with code 0 and no blocking log errors. Global
  locators take **1.047–23.547 seconds** in this seed, not a general locator
  latency guarantee or a new terrain-mod compatibility certification.

The [independent cave audit](alpha4-9-cave-audit.json) passes every actual added
run: **448 Skull contacts** in bone/dripstone/moss/calcite, **293 Tree contacts**
in spruce logs/mossy stone bricks, zero added dirt and no run longer than two
cells. The deep Skull cave has **zero relic-mask cells**, versus 465 before.
Additional Tree geometry drops from **1,686 to 159** in the north box and
**2,376 to 201** in the west box; every accepted source-art cell there survives.
All eight other raw/natural template pairs compare byte-for-byte with Alpha 4.8.
All 108 face-probe contents match the baseline, including its three native leaves;
the strict air-only category remains false while the regression category passes.

[Lowest Tree-log contacts](alpha4-9-tree-contacts.json) record 3,995 direct
contacts, 169 intentionally open columns at/below ground, 174 raised edges and
zero unexpected short gaps or missing wood. Its unique-column counts differ
from the full exposed-underside count above. [Buried raw-Y0 contacts](alpha4-9-buried-contacts.json)
pass all 3,835 retained Small-Colossus/Tower cells. The earlier subset candidate
evidence remains historical, not a substitute for these full-pack runs.

The final artifact is installed in "Relic Test" after this complete acceptance,
with a hash-verified Alpha 4.8 backup under
`build/profile-backups/0.1.0-alpha.4.9-upgrade-20261007-121420/`.
The new `--no-showcase-world` option avoids adding an unrequested flat save while
retaining the complete raw-showcase gate. No overwrite exception is used;
Fabric API and Lithostitched remain unchanged.

The separate installed save is **`Relic Alpha 4.9 Terrain 20261007-121429`**,
with creative mode and cheats enabled. Seven recorded manual-placement regions
are omitted from this new copy only. All ten natural starts pass again after
reload, with the same 1,379,680 checked model cells, zero mismatches, complete
chunks/bounds, support classifications and protection masks.

The [installation record and ten TP commands](alpha4-9-installation.json) link
the raw-showcase, natural, reload, preservation and supplemental-audit hashes.
Every TP camera has air at both feet and head in a fully generated chunk.
All **14,950 installed copy files** match the verified local reload copy exactly.
A persisted protected Colossus cell is removed and restored through normal
server commands in the new isolated copy only; both checks pass.

[Reloaded Tree contacts](alpha4-9-tree-reload-contacts.json),
[buried contacts](alpha4-9-buried-reload-contacts.json) and the
[independent cave audit](alpha4-9-cave-reload-audit.json) all pass their declared
categories. The same intentional clearances and three native leaves remain
explicit; no scenery is manually altered to force an air-only result.
The isolated reload server exits normally with code 0. Its existing 180000 ms
reload watchdog is recorded separately, not substituted for the source
acceptance servers' standard 60000 ms watchdog.

At preparation completion, all **18 pre-existing worlds / 180,890 save files**,
the remaining original profile files and all **2,901 model/source files** match
the fresh preservation baseline. Only the identified, backed-up Alpha 4.8 JAR
is replaced. No unexpected files occur outside the single new terrain save
and installed Relic JAR. The original profile inventory covered 181,159 files.
No old world is opened or edited, and no additional flat showcase save is added.

## Publication

The requested annotated release marker is **`v0.1.0-alpha.4.9`**. The final
implementation, current/historical evidence and review images are published
with an atomic main-branch/tag push after completed validation and terrain
preparation. Native screenshots, worlds, backups and JAR builds remain local;
no GitHub Release or downloadable asset is created by the tag operation.
At publication, the tag recorded the visual-alpha baseline, not client artistic
acceptance, gameplay completion or an air-only face cavity. The subsequent user
acceptance above applies to Skull 2 and Tree at that exact baseline; it does not
rewrite the tag or the historical runtime findings.
