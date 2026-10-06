# Alpha 4.6 — deeper embedding, Skull 2 V2 and Tower V7

October 6, 2026. Minecraft 26.2 / Fabric, candidate
`relics-0.1.0-alpha.4.6+mc26.2.jar`.
The user requested integration of the latest model updates into “Relic Test”.
The user subsequently authorized committing and pushing the current work.

**Models integrated and showcase passed; installation is blocked by natural placement/contact failures.**
Six variants pass core natural block/mask/foundation verification, but supplemental
root/buried-contact audits fail and the four crowned Skulls lack natural acceptance.
“Relic Test” remains on Alpha 4.5; no new inspection saves were installed.
Historical Alpha 4.5 tests do not certify the changed exports or placement contracts.

## Selection and scope

| Template | Selected export | X × Y × Z | Raw blocks | Ground Y | Slope |
| --- | --- | --- | ---: | ---: | ---: |
| Crowned Skull meadow/dry/sand, each | V4 ground-v3 | 117 × 79 × 179 | 111,328 | 16 | 4 |
| Crowned Skull rock | V4 ground-v3 | 117 × 79 × 179 | 111,288 | 16 | 6 |
| Small Colossus | V7 ground-v3 | 111 × 80 × 113 | 233,448 | 13 | 4 |
| World Tree | V4.1 ground-v3 | 187 × 216 × 185 | 291,903 | 8 | 6 |
| Ruined Tower | V7 ground-v3 | 111 × 232 × 93 | 272,528 | 12 | 6 |
| Titan Skull 2 | V2 | 99 × 136 × 99 | 46,922 | 22 | 4 |

All eight changed selections exactly match the
[candidate index](../project/embedding-candidates-20261006.json), including hashes,
dimensions, block counts, deeper burial and narrower slope envelopes.
Large Colossus V4.1 materials B and Obelisk V4.2 retain their Alpha 4.5 hashes.
The crowned Skulls are eight blocks deeper; Small Colossus is four blocks deeper.
Skull 2 V2 uses its own smaller dimensions and posed ground line, not V1's.

Seven block-space derivatives lower central terrain, rather than eroding only
their margins. Tree low moss pads are explicitly part of the mutable terrain
scope. Every other art cell matches its preserved derivative input exactly;
all accepted V4 Tree wood and foliage remain unchanged. Tower V7 and Skull 2 V2
are newly authored source revisions, not ground-only copies of V6/V1.
See [artwork rationale and export checks](../project/EMBEDDING_20261006.md).

Density, salts, biome mappings, terrain-support policy and gameplay are unchanged.
Natural reservations and padding are derived from the new dimensions/contracts.
Fabric API **0.161.0+26.2** and stable Lithostitched **1.8.0** stay unchanged.

## Build and regression checks

```powershell
python tools/build.py
python tools/build.py --skip-generation --output build/reproducibility/alpha4-6
python -m unittest discover -s tests -v
python tools/test_worldgen_java.py
node --test tests/material_proxy.test.cjs tests/voxel_fill.test.cjs tests/voxel_material_priority.test.cjs
```

The default and skip-generation JARs have the same SHA-256:

```text
0124c3556984881c185891ec0d2405e123970ca05634b60f8ed5b7651b4cca81
```

The Java placement tests passed **738 assertions** and JavaScript tests passed
**7 tests**. The complete Python suite passed **87 tests**, including the new
buried-contact and candidate-input cases. Regression coverage includes pinned source identity, raw-template
byte identity, derived supports, 101,038 low-art underside comparisons, immutable
art with the explicit low-moss exception, and the candidate placement contracts.

The older ground-v2 builder now pins its historical burial, slope and dimensions
as well as its input exports. Alpha 4.6's changed selection must not silently
change reproduction of the preserved Alpha 4.5 derivatives or before/after views.

All seven ground-v3 exports were rebuilt in an isolated mirror under
`build/reproducibility/alpha4-6/derivative-mirror-20261006-130812/`.
Their NBT bytes and complete verification/provenance records match exactly.
No exports under `relics/` were regenerated or overwritten. The result is in
`build/reproducibility/alpha4-6/derivative-reproduction.json`.

## Fresh runtime validation

The full flat showcase `run-20261006-130647-b17cf30069b0` passed all ten templates:
**1,607,656 raw blocks**, **zero mismatches**, complete bounds/chunks, exit code 0
and no blocking log errors. Raw soil cells are included; computed persistent-leaf
distance normalization remains the only authored-state comparison adjustment.

The first natural run `run-20261006-130647-e43665a90c84`, seed **731204**, failed.
Large Colossus and Obelisk were completely generated with zero mismatches and
passing foundations/masks. The meadow Skull locator took **167.454 seconds**
and found no site in its search area. The following dry Skull search triggered
the **180-second server watchdog**; the process exited 1. No profile replacement
was performed, and this failed run is retained in
[compact runtime evidence](alpha4-6-evidence.json).

The old broad command-response pattern also matched `Unknown Source` in crash
stack frames after the watchdog. Those lines are not successful locate results;
the run remains failed. The smoke harness now requires server INFO command replies
and stops when an enabled locator finds no site, rather than accepting trace lines.

A read-only vanilla terrain survey nominates random-spread candidate chunks with
the unchanged spacing/salts, sampled heights/biomes and reservations. Nominations
are not runtime acceptance. The smoke harness can generate their actual chunks
naturally, require a saved start of the correct ID at each nominated anchor, then
force its full actual bounding box. This bypasses long global `/locate` searches,
not placement conditions, and never uses `/place structure` for natural evidence.
Two preliminary candidate runs also failed cleanly, without a crash: no Colossus
start appeared at their nominated anchors (`run-20261006-132030-82fce6697e77` and
the diagnostic `run-20261006-132341-45f0e0596ff8`). An atmospheric/sea-level survey
is not enough to certify the delegate's buried start-position biome. These failed
nominations are retained, not relabeled as natural success. The refined survey
queries that buried biome explicitly. It finished through **250 random-spread
region rings**, seed 731204, nominating six templates but none of the four crowned
Skull categories. An earlier independent seed-42 survey through 160 rings found
one meadow-Skull nomination, but no dry/sand/rock candidates. These read-only
surveys do not prove that such sites are impossible; full natural acceptance is
still absent. See the [refined nomination summary](alpha4-6-site-survey.json).
Global locator performance remains failed, and subset success cannot pass the
installation gate.

### Targeted six-template run and failed supplemental contacts

The targeted `run-20261006-132644-6687254943f2`, seed 731204, generates six
**actual natural starts** with the unmodified candidate artifact and rules:
Large Colossus, Obelisk, Small Colossus, World Tree, Ruined Tower and Skull 2.
This is not manual natural placement and does not certify the missing four Skulls.

- **1,178,950 non-excluded blocks**, zero mismatches, complete bounds/chunks.
- **35,206 soil-foundation columns**, zero unsupported soil contacts.
- **1,346,976 saved-mask cells**, zero unprotected cells; no overlaps or read errors.
- Normal server exit 0; no blocking log errors.

Natural comparison retains the documented dirt/grass/azalea-leaf exclusions.
The fresh showcase separately checks all raw authored cells. These passing core
checks do **not** certify art undersides outside/away from those soil foundations.

The actual Tree audit fails: 3,560 low root columns, 3,337 direct contacts,
**170 gaps at/below nominal ground**, plus 53 raised edges (one at +1, 52 at +2).
Expected wood is present; the underlying terrain/contact is absent. See
[Tree root evidence](alpha4-6-tree-contacts.json).

The separate raw-Y0 audit also fails after checking all **5,159 art cells**:
**15 Small Colossus**, **11 Tree** and **80 Tower** undersides have air/water below,
**106 in total**. All expected art is present. The eleven Tree boundary failures
overlap its root audit; these two audits must not be summed as unique failures.
See [buried-underside evidence](alpha4-6-buried-contacts.json).

The exported in-grid low-support tests remain valid, but their documented native
substrate exclusions are now measured runtime failures, not pending acceptance.
No pillars, out-of-bounds authored soil, relaxed slopes or source-model changes
were introduced to hide them. Correcting placement/foundations requires follow-up
work and a fresh full natural test before installation.

Installation requires
strict zero-mismatch acceptance without `--allow-feature-overwrites`, no overlaps,
complete structures, supported foundations and exact saved protection masks.

Supplemental checks audit actual Tree root contacts and all **5,159 buried raw-Y0
art undersides** identified by the derivative reports: 1,367 Small Colossus,
1,324 Tree and 2,468 Tower. Their finite-template undersides are not assumed
supported merely because template/foundation checks pass. The new saved-world
audit verifies the expected art and immediate non-air/non-fluid substrate,
without inventing out-of-bounds blocks or filling higher intentional arches.
The same supplemental checks must be repeated on a future installed terrain copy;
none was created because the current audits fail.

## Preservation and installation

Before integration, the inventory recorded **150,458 files in fourteen existing worlds**, three
mod JARs and **2,625 source-asset files**. The inventory is
`build/profile-inventory/alpha4-6-before-20261006-130127.json`.
Older worlds, sources and dependencies must remain unchanged; only relic-index
README status updates are allowed within the inventoried source tree.
Post-integration hashes confirm all **2,620 non-index source files** unchanged,
with only the five intended README status updates. The passing record is
`build/profile-inventory/alpha4-6-source-preservation.json`.

Profile installation is **blocked, not performed**. The full strict installation
gate rejects this subset natural report, and supplemental contacts also fail.
No backup/replacement or new saves were needed. A future accepted installation
must back up Alpha 4.5 and create separate new flat/natural inspection saves,
then pass reload, masks, normal editability and final contact checks.

Post-test SHA-256 verification confirms all **150,458 files in fourteen existing
worlds** unchanged and all three installed JARs unchanged. The profile still uses
Alpha 4.5; no new profile saves or replacement artifact were installed. The passing
preservation result is `build/profile-inventory/alpha4-6-profile-preservation.json`.

## Authorized isolated client photographs

The user subsequently requested another computer-use attempt and explicitly
selected a separate Alpha 4.6 photo copy. The new launcher profile is
`Relic Alpha 4.6 Foto - isoliert`, Minecraft 26.2/Fabric. This is **not** an upgrade
of “Relic Test” or an exception to its strict installation gate.

The candidate JAR and both unchanged dependency JARs were hash-verified. Copies
of the passing ten-template showcase and the incomplete six-template natural
world were verified byte-for-byte before changing only their `LevelName` and
`allowCommands` metadata. Original saves and server evidence were never opened
in the client. Both photo worlds were saved and returned to the main menu.

**25 native F2 photographs** were collected through real Windows computer use:
14 showcase views covering all ten templates, six natural-site overviews and
five root/substrate detail views. Windows-MCP observed and navigated the UI;
its short UIA key events were ineffective in Minecraft, so a narrowly scoped
Win32 scan-code helper sent F1/F2 and camera/chat commands to the verified photo
client. Each native PNG was hash-copied, its PNG stream checked, and its world
and TP viewpoint recorded. The archive is
`build/screenshot-review/20261006-alpha4-6-computer-use/`; `capture-manifest.json`
records the native images and `photo-verification.json` records the validation.
`uebersicht.png` and `kontaktprobleme.png` are labeled thumbnail montages, not
unmodified native screenshots.

Published copies are available in the repository:

- [Client overview: ten showcase variants and six natural sites](../project/reviews/alpha4-6-client-overview.png),
  SHA-256 `a74c48081f01c26d0103c81e3d944198a3d3d93f97d435d63119094db4ff7dd7`.
- [Diagnostic root and buried-contact details](../project/reviews/alpha4-6-client-contacts.png),
  SHA-256 `f223a982462aac679684f94f6bdd87c150b202e5a461f7ed4a16d8aad6278a5d`.

The 25 full-resolution native PNGs, copied worlds, launcher profile and local
inventories remain local; publishing these two sheets does not include test saves
or build artifacts.

No models were replaced, blocks edited, supports added or cavities excavated.
The isolated camera used spectator mode, enabled spectator chunk loading,
32-chunk rendering and disabled clouds. Four explicitly labeled diagnostic
close-ups use temporary night vision; the effect was cleared afterward.
Underground views use existing air/water pockets, not fabricated cutaways.
The four crowned Skulls still have **no natural-placement photographic coverage**.
These photographs neither pass the failed contact audits nor grant installation.

Post-photo hashes again confirm all **150,458 original save files**, all three
installed JARs, the original `options.txt` and both source server worlds unchanged.
The record is `build/screenshot-review/20261006-alpha4-6-computer-use/preservation.json`.
The later commit/push request does not authorize profile replacement or relax
the failed acceptance gates.

## Acceptance limits

This is visual integration, not artistic approval, authored gameplay or broad
balancing. Tighter slope envelopes can change natural sites and locator timing;
Alpha 4.5's TP positions must not be reused without checking the new run.
Default 60-second server-watchdog performance and full third-party modpack
compatibility are not certified by the isolated base-profile test.
