# Alpha 4.7 — ground contacts and Skull placement

October 6, 2026. Minecraft 26.2 / Fabric.

The user requested one final terrain-contact and locator correction before
turning to gameplay. The Alpha 4.6 photographs and saved-world audits are the
regression baseline. **The final build passes the complete ten-variant showcase,
strict natural generation, saved masks, foundations and supplemental contacts.**
Global searches pass with Minecraft's normal 60-second watchdog in the tested
seed. “Relic Test” has not been upgraded during this task.

## Implementation

- `TerrainSupportProcessor` now fills exposed solid-model undersides at or below
  nominal ground, including wood, masonry, bone and metal. It also handles a low
  art run separated from an authored soil cell farther down the same column.
- The processor retains every authored cell, stops at solid substrate or the
  dimension/placement boundary, skips foliage and block entities, and never
  accesses another chunk. Added cells enter the existing saved generation mask.
- Fill is stable dirt, sandstone for the Obelisk/sand Skull, or stone for the
  rock Skull. Raised art above nominal ground does not create new supports.
- The replaceable Jigsaw anchor moves to derived `ground_y - 1`. Vanilla Jigsaw
  still puts the piece base at `surface - ground_y`, but now checks its biome at
  the surface. Previously the query could hit a cave biome below a suitable site.
  The former terrain-condition vertical offset is therefore removed.
- Crowned Skull downhill site tolerance is **12 blocks** (previously 4, rock 6). Their
  burial stays **Y16**, and generated foundations use the same revised tolerance.
  Uphill tolerance is 12 for meadow/dry/sand and **18 for rock**. Small Colossus
  admits **12 uphill, still only 4 downhill**, with its original Y13 burial and
  foundation depth. This permits hills rising behind a buried model without
  increasing its permitted downhill skirt. Other relics retain their slopes.
  The dry/sand/meadow palette checks, full 25-point dry-land grid, ceiling,
  separation, density and variant biome tags remain active.
- The raw exports are byte-identical to Alpha 4.6. Tree wood/foliage and the
  Tower's 220 visible layers retain their prior geometry. The historical
  [candidate index](../project/embedding-candidates-20261006.json) and derivative
  provenance preserve their original slopes; the current runtime selection is
  `tools/relic_catalog.py` and the packaged `relics.integration.json`.

## Why the site tolerance changed

The surface-anchor correction alone did not make crowned Skulls locatable.
The first fresh run, `run-20261006-144809-404d6c32e0c7`, hit Minecraft's normal
60-second watchdog during the meadow-Skull search. A read-only seed-731204 survey
through 100 region rings nominated the other six templates but no crowned Skull.
An 8-block diagnostic found meadow, sand and rock (rock at 12), but no dry Skull.
At 12 all four received nominations, but the next global run
`run-20261006-145430-0358b5918b07` still hit the normal watchdog on rock after
successfully finding meadow, dry and sand. Allowing a higher rocky bank reduced
the survey's first rock candidate from ring 77 to ring 46. A separate Small
Colossus locator also exceeded 60 seconds with its symmetric 4-block tolerance
(`run-20261006-150923-27119e953a57`). Its uphill-only adjustment moves the survey's
first nomination from ring 75 to ring 24.
The intermediate full run `run-20261006-150923-b472cf53e94b` already verified all
four crowned Skulls with zero mismatches; rock took **24.032 seconds**. That run
then failed on the unchanged Small Colossus locator, motivating its final
uphill-only correction. Its partial success is retained as failed-run evidence.

Diagnostic alternatives (8/12/16 symmetric slopes, extra rocky biomes, narrower
corner sampling and 32-chunk Skull spacing) were examined read-only or in an
unlaunched diagnostic build. The final artifact keeps the original biomes,
density and full 25-point grid. Nominations alone are not natural acceptance;
actual saved starts, complete models, masks and contacts must pass afterward.

The reproducible read-only survey is `tools/survey_natural_sites.py`; its output
can feed the smoke harness's explicit candidate mode. Ordinary global `/locate`
is tested separately with the default **60000 ms** watchdog.

## Same-site contact regression

Intermediate artifact SHA-256:
`c710699e6ec6ef7dac6caf37d99928c19190ca214d6deb2db5afce64617cc266`.
This has the final contact processor and surface anchors but the original Skull
tolerances. It is recorded separately from the later final artifact.

Fresh run `run-20261006-145034-5da0ddca05b7` naturally regenerated the old Small
Colossus, World Tree and Tower problem sites using their known candidate chunks.
It passed strict block, foundation, saved-mask and overlap checks.

- Tree: **0 ground-level gaps**, down from 170; 53 raised edges remain above
  ground and are reported separately.
- All **5,159 buried raw-Y0 art cells**: **0 unsupported contacts**, down from
  106 (15 Small Colossus, 11 Tree, 80 Tower).
- Expected art is present. The previous eleven buried Tree failures are part
  of the root category, not eleven additional unique errors.

Reports live beside that run as `tree-contacts.json` and `buried-contacts.json`.
The [same-position comparison](../project/reviews/alpha4-7-contact-fix.png) shows
three actual saved-world block sections, with source hashes in the adjacent JSON.
These are diagnostic sections, not new client screenshots. Reproduce with
`tools/review_runtime_contacts.py` using `.work/python/Scripts/python.exe` (Pillow).

## Final-artifact runtime acceptance

Fresh seed **731204**, final artifact hash below:

- Showcase `run-20261006-151402-51ca86a2927c`: all **10 templates**,
  **1,607,656 raw blocks**, **zero mismatches**. Raw terrain is included.
- Natural `run-20261006-151402-0cdd8e0578b2`: all **10 actual natural starts**,
  found by ordinary global `/locate` from the harness's default spawn origin.
  No candidate nominations or manual structure placement substitute for them.
- **1,504,559 non-excluded natural blocks**, **zero mismatches**,
  **79,903 soil-foundation columns**, **zero unsupported columns**.
- **1,900,198 template protection-mask cells**, **zero unprotected cells**;
  complete bounds/chunks, no overlaps or read errors.
- Both servers exited normally with code 0 and no blocking log errors.
  The normal **60000 ms** watchdog remained enabled throughout.
- [Final Tree audit](alpha4-7-tree-contacts.json): **0 ground-level gaps**,
  53 raised edges above nominal ground. Expected wood is present.
- [Final buried-contact audit](alpha4-7-buried-contacts.json): all **5,159**
  raw-Y0 art cells supported; **zero missing art or unsupported contacts**.

Natural block comparison retains the established dirt/grass/azalea-leaf
exclusions; the separate showcase verifies all raw cells. Persistent-leaf
distance normalization is the existing state-comparison adjustment.

| Global search | Seconds |
| --- | ---: |
| Large Colossus | 10.969 |
| Obelisk | 1.078 |
| Meadow Skull | 7.797 |
| Dry Skull | 2.687 |
| Sand Skull | 21.922 |
| Rock Skull | 24.172 |
| Small Colossus | 9.109 |
| World Tree | 12.313 |
| Ruined Tower | 1.469 |
| Skull 2 | 19.000 |

The [compact evidence](alpha4-7-evidence.json) preserves seven completed runs,
including the failed intermediate locators and the successful same-site subset.
The strict ten-variant installation gate accepts the final natural/showcase pair,
and both loaded JAR hashes equal the current artifact. This is one-seed base-Fabric
acceptance, not a general latency guarantee or a fresh terrain-mod compatibility test.

## Build and automated checks

Default, skip-generation and isolated reproducibility builds match:
`e2d384b8ab6ea4abc379487e993d40b9f355e08db610a32e6e7bef614169dfa9`.

The final full Python suite passed **87 tests**, including preserved export
provenance, current asymmetric tolerances and stale-anchor/packaging rejection.
Java runtime tests passed **748 assertions**, including
water-filled raw-Y0 contacts, separate low art/soil runs, material selection,
authored-cell preservation, duplicate prevention and raised-arch exclusions.
The integration/push check repeated both suites and passed all **7 JavaScript
tests**, Python compilation, documentation links and `git diff --check`.
The rebuilt default/skip-generation JARs match the final tested artifact exactly;
all seven compact runtime records and both contact audits were checked against
their existing reports. No additional server run or test world was created.

```powershell
python tools/build.py
python tools/build.py --skip-generation --output build/reproducibility/alpha4-7
python -m unittest discover -s tests -v
python tools/test_worldgen_java.py
python tools/smoke_server.py --accept-eula --quiet --showcase
python tools/smoke_server.py --accept-eula --quiet
```

## Scope

Existing profile worlds and source exports are retained. The working artifact is
`dist/relics-0.1.0-alpha.4.7+mc26.2.jar`; “Relic Test” is still on Alpha 4.5.
Client visual acceptance and gameplay implementation are follow-up work.
The subsequent request authorizes integration and Git push only, not a profile
upgrade, additional world generation or gameplay work.
