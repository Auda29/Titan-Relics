# Alpha 4.1 — October 5 screenshot revision tests

Candidate: `relics-0.1.0-alpha.4.1+mc26.2.jar`, Minecraft 26.2 / Fabric.
The [revision guide](../project/SCREENSHOT_REVISIONS_20261005.md) describes the
new models, soil foundations and preserved screenshot-era baselines.

Final candidate SHA-256:

```text
5c7554bcad7e6eb0cf3fd4b962f2100ae057ce216fe7b168c70647ce87c9a1aa
```

Default build and `--skip-generation` produced the same checksum.
No user profile or existing world was modified by this revision session.

## Automated and asset checks

- 55 Python tests passed, including original-source identity, padded natural
  template reconstruction, all-rotation/eight-chunk bounds, biome/settings
  contracts, stable foundation materials, downhill contacts and falling toe tops.
- All three revised Blender → schematic → NBT pipelines passed exact block/state,
  hash, palette, bounds and lossless tile checks.
- Small Colossus V5 retains its six optics, grille and connected head/pincers.
- World Tree V3 passes 280 exported woody-tip probes and persistent-leaf checks.
- Ruined Tower V3 retains 220 visible layers and open original void probes, with
  structural probes on the new floor and stair remnants.

## Minecraft showcase — passed

Run `run-20261005-095741-4de7e5afdfa3` loaded the final candidate with Fabric API
and Lithostitched on an isolated vanilla flat test world. All ten manual raw
templates match **1,842,457 exported blocks** exactly, allowing only the documented
valid persistent-leaf distance recalculation. No missing/incomplete checked
chunks, blocking log errors or process failures. Exit code 0.

| Raw template | Checked blocks | Mismatches |
| --- | ---: | ---: |
| Colossus | 223,161 | 0 |
| Obelisk | 94,422 | 0 |
| Crowned Skull, each of four palettes | 136,569 | 0 |
| Small Colossus V5 | 248,549 | 0 |
| World Tree V3 | 311,602 | 0 |
| Ruined Tower V3 | 333,223 | 0 |
| Titan Skull 2 | 85,224 | 0 |

This verifies raw exports, not natural foundation placement or client aesthetics.

## Natural terrain — failed; placement revision remains incomplete

Run `run-20261005-095705-b9a26115b8de` tested the final candidate on vanilla terrain,
seed 731204. The server completed and exited normally after reverting to the
25-point grid. Nine of ten requested template types were located; the rock Skull
was not found within the locator's search. Ten saved instances were inspected,
including an additional Small Colossus overlapping the dry Skull site.

The verifier checked 1,937,728 non-excluded blocks. Seven instances had zero
block mismatches, but **none passed the foundation-contact check**. There were
4,616 unsupported lowest terrain columns across the ten instances:

| Instance | Block mismatches | Unsupported terrain columns |
| --- | ---: | ---: |
| Colossus | 1,719 | 487 |
| Obelisk | 0 | 320 |
| Meadow Skull | 0 | 221 |
| Dry Skull | 0 | 370 |
| Sand Skull | 94 | 992 |
| Small Colossus, located site | 0 | 927 |
| Small Colossus, overlapping dry Skull | 30,888 | 339 |
| World Tree | 0 | 37 |
| Ruined Tower | 0 | 109 |
| Titan Skull 2 | 0 | 814 |

No checked model chunks were missing. Follow-up reads of example coordinates
confirmed real air/water beneath the foundations, rather than a coordinate-only
comparison error: the located Small Colossus has sampled gaps of 7–8 blocks,
the Tree 4 blocks, and the Tower water with solid ground 3–4 blocks lower. These
samples do not establish whether every reported gap is exposed at the surface;
the strict contact check also detects underground cavities.

Colossus differences are replacements by natural stone/ore/soil features. The
Sand Skull includes lava/cave-air replacements. The extra Small Colossus has
substantial replacements consistent with its overlap with the dry Skull.

**The static foundation depth and sparse height sampling do not ensure solid
contact on real terrain.** The controlled slope render is a fixture only. A
terrain-aware support/placement correction is still needed; neither that render
nor the successful raw showcase qualifies this artifact for natural-placement
acceptance. Cross-structure overlap and the unlocated rock variant also remain
unresolved in this run. No integration-mod terrain run was performed for Alpha 4.1.

## Rejected intermediate trial

Run `run-20261005-095042-a007e56c33e5` used intermediate checksum
`3748c6be9c176222d26266762c31bf3b58825ceb236f1dcf962ed82748529f42`.
The experimental 81-point placement grid caused a 180-second server watchdog
during the first Colossus locator. That trial is **failed** and the denser grid
was removed. The final candidate retains the 25-point grid over the padded
footprint, with tapered foundations supplying the terrain connection.

One attempted launch also raced a concurrent artifact rewrite and stopped before
Java started with `BadZipFile`; the subsequent test started only after packaging
completed. It is not counted as a Minecraft run or a pass.

Completed runs are preserved in [hash-linked evidence](alpha4-1-evidence.json).
Full reports, isolated worlds and logs remain local under `build/smoke/`.
