# Alpha 4.3 — latest structure integration

Candidate: `relics-0.1.0-alpha.4.3+mc26.2.jar`, Minecraft 26.2 / Fabric.
October 5, 2026. The user requested the latest Structures-thread exports in the
mod and the existing “Relic Test” inspection workflow.

**Full showcase and strict natural-placement verification passed.** The tested
artifact is installed in “Relic Test”, with a verified Alpha 4.2 backup and
separate new showcase/terrain saves. The terrain copy also passed reload,
saved-mask, normal-editability and strict block verification.
No prior Alpha 4.2 result is reused as acceptance of this artifact.

## Selected changes

| Template | Export | X × Y × Z | Raw blocks | Ground Y |
| --- | --- | --- | ---: | ---: |
| Small Colossus | V6 | 111 × 80 × 113 | 234,956 | 9 |
| World Tree | V4 | 187 × 216 × 185 | 291,433 | 8 |
| Ruined Tower | V4 | 111 × 232 × 93 | 321,087 | 12 |

The other seven exports retain their Alpha 4.2 hashes. All manual templates are
byte-identical to their source NBT and retain DataVersion 3105. The three revised
models remain visual candidates, not user-approved final art.

The default build re-derives foundations, grid bounds and reservations from the
new dimensions. In particular, the Tree's natural padded footprint is 203 × 201
blocks. Ground supports and persistent exact-cell feature masks retain the
[Alpha 4.2 implementation](../technical/ALPHA_4_2_TERRAIN.md). Density, biome
mappings, gameplay and existing generated relics are unchanged.

## Build and automated checks

Default and `--skip-generation` builds have the same SHA-256:

```text
5a4d4e47e82c3141a192b788fca5c10d8a52fc6d002b1892969de2030db4e585
```

- Headless Java support/reservation/mask tests: **738 assertions passed**.
- JavaScript conversion/material tests: **7 passed**, including the Tree's
  structural wood/leaf overlap adapter and exception-safe restoration.
- Full Python regression suite: **65 passed**, including pinned current selection,
  preserved seven exports and all-rotation footprint/reference limits.

## Runtime and profile safety

The flat showcase run `run-20261005-124958-e7339eb31735` passed: **1,796,559 raw
exported blocks**, all ten templates, **zero mismatches**, no missing/incomplete
checked chunks. Persistent-leaf distance normalization remains the documented
exception; original soil cells are included in the flat comparison.

The natural run `run-20261005-124958-97f7626d565d`, seed **731204**, passed:

- All ten expected variants located and fully generated; complete matching bounds.
- **1,934,683 non-excluded blocks**, **zero mismatches**, no read/verification errors.
- **110,450 foundation columns**, **zero unsupported contacts**, no relic overlaps.
- Saved protection masks cover every one of **2,868,069 non-air template cells**.
- Normal server exit (code 0), no blocking log errors in either final run.

Natural comparison retains the documented dirt/grass/azalea-leaf exclusions;
the flat comparison checks raw soil cells. Both runs are preserved in
[hash-linked compact evidence](alpha4-3-evidence.json), including the exact tested
artifact and complete-report hashes. Installation passed without
`--allow-feature-overwrites`.

Fresh, isolated flat-showcase and natural-terrain server runs cover all ten
templates with Fabric API 0.160.0+26.2, Lithostitched 1.8.0+beta6, Fabric Loader
0.19.5 and Java 25. They do not include third-party terrain mods or the personal
modpack. Strict zero-mismatch checks, complete bounds/chunks, supported foundation
contacts, non-overlap and saved protection masks gate installation.

Before integration, inventories were saved for all 65,427 existing save files,
the three installed mod JARs and 1,257 source-asset files. Subsequent SHA-256 checks
confirmed all **65,427 files in eight existing worlds**, both unrelated mod JARs
and all **1,257 source assets** unchanged. The installed artifact and previous-JAR
backup match their recorded checksums. Local preservation evidence is saved in
`build/profile-inventory/alpha4-3-profile-preservation.json` and
`build/profile-inventory/alpha4-3-source-preservation.json`.

## Test-profile installation

- Installed JAR: `E:\Roaming\ModrinthApp\profiles\Relic Test\mods\relics-0.1.0-alpha.4.3+mc26.2.jar`.
- Previous Alpha 4.2 JAR backed up under
  `build/profile-backups/0.1.0-alpha.4.3-upgrade-20261005-130025/`; SHA-256
  `1279c9fd1b167fe58aeacadcfd50e232943bef56072cfd47077ce0ddad653e94`.
- New flat save: **Relic Alpha 4.3 Showcase 20261005-130025**.
- New natural save: **Relic Alpha 4.3 Terrain 20261005-130055**, seed 731204,
  creative/cheats, normal difficulty, mobs and random ticks enabled. Spawn:
  `[-53411, 80, 45280]`, yaw 90, facing the large Colossus.
- The terrain copy reloaded its persistent masks and again verified all ten
  variants, 1,934,683 non-excluded blocks, zero mismatches, zero unsupported
  foundation contacts, no overlaps and complete protection-mask coverage.
- A protected art cell at `[-53636, 196, 45278]` was removed and restored through
  normal server-level commands; its exact final state is `green_terracotta`.
  Reload/editability/full-verification evidence is kept under
  `build/terrain-preview/20261005-130055/report.json`.
- Existing saved relics are not retroactively updated; use the new inspection
  saves to review V6/V4/V4. Source exports and all earlier inspection saves remain
  intact. No commit or push was requested or performed.

Flat viewpoints, in Small Colossus / Tree / Tower order:

```mcfunction
/tp @s 2359 80 -48 0 0
/tp @s 2781 90 -48 0 0
/tp @s 3127 90 -48 0 0
```

Natural-run viewpoints, in the same order:

```mcfunction
/tp @s -3152 100 -5248 -90 0
/tp @s -41268 100 20672 -90 0
/tp @s 10470 100 2752 90 0
```

The wider Tree uses a different natural site from Alpha 4.2. Fly higher or
farther back to view its crown and the Tower's top. Use the prepared sites rather
than generating new chunks with slow `/locate` searches.

## Acceptance limits

Locator times were approximately 0.8–72.6 seconds; the rock Skull locator used
72.6 seconds with the isolated server's 180-second watchdog. This is not an
acceptance of default-60-second dedicated-server performance, third-party terrain
mods or a full personal modpack. Player artistic review and gameplay acceptance
remain separate. No gameplay, rewards or broader balancing were implemented.
