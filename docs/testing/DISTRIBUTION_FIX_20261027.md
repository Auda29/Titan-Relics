# Distribution correction, October 27, 2026

The [original audit](DISTRIBUTION_AUDIT_20261027.txt) found 13 accepted repeatable
sites in 30 fixed 120,000 by 120,000 block windows and reproduced a natural
generation crash. That audit remains the record of the original artifact.

## Chunk generation

An asynchronous structure-start continuation previously ran on Minecraft's
generic background executor. Chunk generation expects its dependency updates on
the native serial worldgen dispatcher. The continuation now re-enters that
dispatcher with the affected chunk's native queue priority. An already completed
planning future keeps the synchronous native path.

The exact original failure is seed `1979312429623454326`, Skull 2 at
`39640, -9416`, with an unavailable `STRUCTURE_STARTS` dependency during
`STRUCTURE_REFERENCES`. The fixed build successfully loads and saves this area.
A copied v1 world also retains its policy, saved target, original spawn and
generator fingerprint. Source worlds are never opened or modified by these tests.

## Local terrain search

Fresh worlds use `relics-distribution-v2-local64-r3072`. Each cell retains its
original ticket, priority and rotation. It tests the original position first,
then up to 63 distinct deterministic chunk centers within 3,072 blocks, inside
the original cell and its 256-block margin. It takes the first terrain-valid
position, then applies the existing final region and distance checks once.

The 5,000-block cell size, family ticket ranges, all terrain predicates,
2,000-block general separation, 15,000-block Obelisk separation and 30,000-block
large-Colossus minimum spawn distance remain unchanged. No family is rerolled.
A final spacing rejection leaves the opportunity empty. A relocated site that
would change family at an Obelisk-region boundary is also rejected.

Existing journals explicitly marked `relics-distribution-v1` retain their original
single-position decisions. Worlds without a journal retain legacy placement.
The large-Colossus search, saved destination and map identity are unchanged.

The chunk gate distinguishes terrain selection from final acceptance. It only
requests final acceptance at the selected start chunk. Neighborhood enumeration
includes the local search radius and filters actual distances before asking for
the large-site decision. This prevents irrelevant distant candidates from
blocking the initial spawn search.

## Existing-world limits

The copied original v1 failure site contains all 25,260 fixed Skull-2 model
blocks and their protection bits with no mismatches. Its separate foundation
contact check reports two unsupported underside locations, `39597,64,-9399`
and `39599,62,-9393`. The generation crash is fixed, but this old placement is
not a complete passing contact proof. V1 coordinates and authored geometry
remain frozen; this correction does not retrofit terrain into existing saves.

An isolated copied world with no distribution journal logs the legacy-placement
path, retains the absence of a journal and successfully loads the original
failure rectangle. This is compatibility evidence, not retrogen evidence.

## Validation record

All 30 corrected-world runs completed successfully in isolated Minecraft
26.2/Fabric servers with the normal 60-second watchdog and no error log entries.
The [machine-readable comparison](distribution-fix-20261027.json) retains
checksums, seed results, natural block proofs and separate lifecycle regressions.
No launcher profile or user world was opened or changed.

| Accepted family | Original artifact | Corrected artifact |
| --- | ---: | ---: |
| Obelisk | 10 | 279 |
| Crowned skull | 0 | 15 |
| Skull 2 | 1 | 7 |
| Ruined tower | 2 | 17 |
| Small Colossus | 0 | 31 |
| World Tree | 0 | 2 |
| Total | 13 | 351 |

These are the same 17,277 nominal opportunities in 30 fixed 120,000 by 120,000
block windows. Empty test windows decrease from 20 to zero. All original
candidates, initial spawns, generator fingerprints and selected large-Colossus
targets match the original audit. Independent reverse-order production planning
agrees in every world. General and Obelisk separation checks pass for every
accepted pair in each opportunity set.

The nearest accepted repeatable site is between 4,226 and 33,060 blocks from
the initial spawn, with a median of 15,362 blocks. The large Colossus counts
separately. Obelisks still dominate this finite sample; these results establish
improved availability, not completed survival balancing or terrain-mod coverage.

Nine naturally generated instances, covering all six repeatable families and
four crowned-skull palettes, pass full block, protection and contact checks.
The comparison checks 1,120,642 fixed model blocks with no mismatches. The old
v1 crash-site contact failure above remains a separate failing contact proof.

The comparison selects the same cells by each cell's original nominal position
inside the window. A moved accepted center can cross that window's edge. Counts
therefore describe the same opportunity set, not a complete census of every
physical center inside the rectangle. The raw audit outcome
`neighbor_spacing_or_priority` also includes final region-boundary rejection.
Whole-window diagnostic timings include extra explanations and independent
reverse-order planning; they are not ordinary per-chunk latency measurements.

Completed unit checks:

- 1,008 executor ownership and dependency-publication assertions, including
  1,000 concurrent planner completions serialized through one generation lane.
- 675,716 versioned local-search assertions, including signed cells, probe
  identity, cell margins, shifted spacing, exploration order, initial-spawn
  dependency bounds and rejection at a region boundary without a family reroll.
- 198,920 existing distribution assertions across 30 synthetic-terrain seeds.
- 648 gameplay assertions, 755 worldgen assertions and 42 static mixin contracts.
- All 121 tracked Python tests pass. Local untracked NeoForge work is outside
  this change and remains byte-identical to the task-start snapshot.
- Two independent player builds are byte-identical, SHA-256
  `cbaaca73805f28d4c6affc9e42dbcf7dfe62ea23b21b7065e7264bf69a11bc3f`.
  All 57 shipped structure and worldgen resource entries match the original
  artifact. Diagnostic and test classes are absent from the player artifact.

The production lifecycle run at
`build/distribution-runtime/731204-224004bf/evidence.json` passes controlled
interruption, saved-cursor resume, restart, unchanged datapack reload,
`setworldspawn`, global locate from two origins, copied map IDs and exactly one
saved natural large-Colossus start. The repeatable locate result agrees with its
saved natural geometry across restart. The cold repeatable locate took 11.266
seconds in this run and completed asynchronously; this is a measured example,
not a guaranteed latency bound. The unique target remained `96136,48504`.

The finite-border run at
`build/distribution-runtime/731204-a5bab44b/evidence.json` exhausts the allowed
domain and preserves the unavailable state across restart without inventing a
destination, structure or map target.

Synthetic and static tests do not establish real Minecraft terrain acceptance.
The native proofs above validate the listed instances. Other planned sites,
terrain mods and multiplayer behavior still need their own runtime acceptance.

## Repeating the checks locally

Use the checksum-verified local JDK 25 and an explicit path to the corrected
artifact. Audit and probe commands create isolated worlds under `build/`.

```powershell
python tools/test_distribution.py --java-home <jdk25>
python tools/audit_distribution.py --accept-eula --java-home <jdk25> --artifact dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar --jobs 2
python tools/test_distribution_server.py --accept-eula --java <jdk25>/bin/java.exe --artifact dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar --seed 731204 --interrupt
```

`tools/summarize_distribution_audit.py` compares the original and corrected
completed run directories. It verifies per-file checksums, identical nominal
candidates and initial spawns, unchanged large targets and generator fingerprints,
reverse-order agreement, all selected natural block proofs and unchanged shipped
worldgen resources before writing the comparison. The original run includes its
failed natural-generation test; the summary does not turn it into a passing run.
