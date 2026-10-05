# Alpha 4.2 — latest models and terrain placement correction

Candidate: `relics-0.1.0-alpha.4.2+mc26.2.jar`, Minecraft 26.2 / Fabric.
See the [terrain implementation](../technical/ALPHA_4_2_TERRAIN.md).

**Final showcase and strict natural-placement verification passed.** The verified
artifact is installed in “Relic Test”, with an Alpha 4 backup and a separate new
showcase save. The separate terrain inspection copy also passed reload,
editability, saved-mask and strict block verification. Previous Alpha 4.1 failures remain recorded in
[its report](ALPHA_4_1_TEST_REPORT.md); earlier failed Alpha 4.2 intermediates are
not reclassified as passes.

Final SHA-256 (identical default and `--skip-generation` builds):

```text
1279c9fd1b167fe58aeacadcfd50e232943bef56072cfd47077ce0ddad653e94
```

## Automated checks

- The full **64-test Python suite** passed after adding the placement checks.
- New Python tests cover safe reservations, matching ground processors, actual
  dry-land conditions, overlap detection, installation gates and stale/escaping
  Java class rejection.
- The actual headless Java processor/candidate tests pass **738 assertions**:
  downhill air gaps, water, stable sand/red-sand/gravel fills, planned model cells,
  untouched void columns, high moss, chunk boundaries, dimension minimum, protected
  blocks, falling native gravel, early grid rejection and brute-force family/self
  reservation checks across seeds/negative coordinates, exact-cell protection-mask
  persistence and invalid mask rejection.
- All five JavaScript material/voxel-fill tests pass.

## Final Minecraft runtime checks — passed

Minecraft 26.2, Fabric Loader 0.19.5, Java 25, Fabric API 0.160.0+26.2 and
Lithostitched 1.8.0+beta6. Isolated servers, no third-party terrain mods.
Both final runs exited normally (code 0) with no blocking log errors.

- Flat showcase `run-20261005-115236-9cd0c2cc0426`: **1,842,457 exported blocks**
  checked across all ten raw templates, **zero mismatches**, no missing/incomplete
  checked chunks. Only valid persistent-leaf distance recalculation is normalized.
- Natural run `run-20261005-115236-5642fe7af87a`, seed **731204**: all ten requested
  variants located and fully generated, **1,986,324 non-excluded blocks** checked,
  **zero mismatches**, **115,603 foundation columns**, **zero unsupported columns**,
  **no horizontal relic overlaps** and matching complete bounds in every rotation
  actually encountered. Every one of **2,996,136 non-air natural-template cells**
  also has its exact saved protection-mask bit. No read or verification errors.

| Natural template | Checked blocks | Mismatches | Unsupported columns |
| --- | ---: | ---: | ---: |
| Colossus | 259,038 | 0 | 0 |
| Obelisk | 117,510 | 0 | 0 |
| Meadow Skull | 21,475 | 0 | 0 |
| Dry Skull | 28,435 | 0 | 0 |
| Sand Skull | 290,661 | 0 | 0 |
| Rock Skull | 290,661 | 0 | 0 |
| Small Colossus V5 | 242,065 | 0 | 0 |
| World Tree V3 | 296,912 | 0 | 0 |
| Ruined Tower V3 | 399,407 | 0 | 0 |
| Titan Skull 2 V1 | 40,160 | 0 | 0 |

The natural comparison preserves the historical dirt/grass/azalea-leaf exclusions
listed by the verifier; it is not a claim that random-ticking terrain never
changes. Raw showcase comparisons do check the original soil cells. Bounds and
mask checks use the exact padded/rotated natural templates, not raw-box guesses.
The installer qualified the final artifact **without** `--allow-feature-overwrites`.

Locator times were approximately 0.8–74 seconds. The rock locator took 74 seconds;
the isolated server had a recorded 180-second watchdog limit. This is not a
performance acceptance for a dedicated server's default 60-second watchdog or
the complete personal modpack. Use the pre-generated inspection sites below;
broader terrain-mod compatibility and client visual approval remain separate.

## Preserved failed intermediates

The unprotected intermediate `60d6c616e4d54e5ef582f7d3b910d6094dcd32c0089b4832cf889c271c16bb71`
completed a full vanilla run (`run-20261005-113121-5c3a7a4ca64c`, seed 731204): all
ten variants located, zero unsupported columns and no overlaps, exit 0, no
blocking errors. Strict block verification still failed: Colossus 2,205,
rock Skull 3,059 (1.0524%), sand Skull 94 differences. The others had zero.
The one-percent installation gate correctly refused this intermediate. The
protected candidate passes without relaxing that gate. Its first rock-only
regression (`run-20261005-114925-9047f62c623d`, intermediate checksum
`9dfc5ee700ccd9f97d22bfec492b64b8f15416090479a01fcfd45ff1df9471af`)
already had zero block mismatches and zero unsupported columns.

Other intermediates include a locator watchdog, rejection of a dry coastal Y63
site by the old Y64 floor, and five dry-Skull cave contacts whose native gravel
fell away. Early grid rejection, actual sampled water checks and stable supports
address these separate findings. All completed runs, including failures, are
preserved in [hash-linked evidence](alpha4-2-evidence.json).

## Test-profile installation

- Installed JAR: `E:\Roaming\ModrinthApp\profiles\Relic Test\mods\relics-0.1.0-alpha.4.2+mc26.2.jar`.
- Alpha 4 JAR backed up and hash-verified under
  `build/profile-backups/0.1.0-alpha.4.2-upgrade-20261005-120234/`.
- New flat save: **Relic Alpha 4.2 Showcase 20261005-120234**.
- New natural save: **Relic Alpha 4.2 Terrain 20261005-120242**, seed 731204,
  creative/cheats, normal difficulty, mobs and random ticks enabled. Spawn:
  `[-53411, 80, 45280]`, yaw 90, facing the naturally placed large Colossus.
- Terrain copy reloaded the persisted masks and passed the full strict verifier
  again. A protected art cell at `[-53636, 196, 45278]` was successfully removed
  and restored through normal server-level commands, proving the guard does not
  block ordinary building edits. The final exact state is `green_terracotta`.
- All six existing worlds were independently checked against the pre-install
  inventory: **37,305 files unchanged**. Both other mod JARs are also hash-identical.
- Full terrain-copy evidence remains local at
  `build/terrain-preview/20261005-120242/report.json`.

New-model viewpoints in the flat save:

```mcfunction
/tp @s 2361 80 -48 0 0
/tp @s 2775 90 -48 0 0
/tp @s 3127 90 -48 0 0
```

These are Small Colossus V5, World Tree V3 and Ruined Tower V3 respectively.
New-model viewpoints in the natural save:

```mcfunction
/tp @s -3155 100 -5248 -90 0
/tp @s 18625 100 -33728 90 0
/tp @s 10470 100 2752 90 0
```

The order is again Small Colossus, World Tree and Ruined Tower. Fly higher/further
back to inspect the tall tree and tower. These commands avoid new slow locator
searches and point at the revised naturally generated models, not old saves.
