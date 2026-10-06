# Alpha 4.4 — weathering, tower sides and Tree root contacts

October 6, 2026. Candidate: `relics-0.1.0-alpha.4.4+mc26.2.jar`, Minecraft 26.2 / Fabric.
The user requested the latest Structures-thread exports, an updated “Relic Test”
installation and then a commit/push of all pending project work.

**Fresh showcase, strict natural placement and actual root-contact checks passed.**
The verified artifact is installed in “Relic Test”, with an Alpha 4.3 backup and
separate new showcase/terrain saves. The terrain copy also passed reload,
strict block/mask verification, normal editability and the root-contact check.
Earlier Alpha 4.3 or dependency-only test results do not certify these new templates.

## Selection

| Template | Export | X × Y × Z | Raw blocks | Ground Y |
| --- | --- | --- | ---: | ---: |
| Small Colossus | V7 | 111 × 80 × 113 | 235,933 | 9 |
| World Tree | V4.1 | 187 × 216 × 185 | 293,691 | 8 |
| Ruined Tower | V5 | 111 × 232 × 93 | 307,417 | 12 |

The other seven exports retain their previous hashes. All ten raw templates are
copied byte-for-byte and preserve DataVersion 3105. The Tree's accepted V4 wood,
foliage, moss and root stones are unchanged cell-for-cell; only grass/rooted-dirt/
dirt terrain cells differ. Small Colossus and Tower remain visual candidates;
the Tree's changed ground contacts still require in-game review.

See the [October 6 art and ground audit](../project/GROUND_WEATHERING_20261006.md).
Dimensions, burial, biome mappings and density remain unchanged. Derived soil
foundations and persistent masks retain the [Alpha 4.2 policy](../technical/ALPHA_4_2_TERRAIN.md).
No gameplay, reward system or broader balancing is included.

## Dependency baseline

- Minecraft 26.2, Fabric Loader 0.19.5, Java/JDK 25.
- Fabric API **0.161.0+26.2**, SHA-256
  `e5b858ceb13290c274e31cb888ff5a1a40cb91067e7ffab0b5b775aec51e216a`.
- Lithostitched **1.8.0 stable for Fabric 26.2**, SHA-256
  `4d74a8ec2023657352ae051f1a6270bff474bf3cc46013100eff5f9ddbbdd024`.

The user updated these dependencies after the isolated Alpha 4.3 compatibility
checks. Alpha 4.4 build-cache setup, local-cache fallback and smoke-server filenames
now pin the same new baseline. Official downloads are checksum-verified.
The user's two updated dependency JARs must remain unchanged during installation.

## Build and automated checks

Default and `--skip-generation` builds are byte-identical, SHA-256:

```text
a5aeaba7f3c313c09acfdb438a7d7a3d38de2a702adff21e0b28cc5500115dc3
```

- **738 headless Java assertions passed** against the updated compilation dependencies.
- **7 JavaScript tests passed**, including scoped structural wood/leaf priority.
- **72 Python tests passed**, including new Tree material-preservation,
  accepted non-terrain identity, updated dependency pins and root-contact tests.
- The initial full-suite run passed 71/72 tests; its only failure was the new
  report link while this document was being created concurrently. A fresh full
  run with the completed documentation passed all 72 tests; that earlier failure is not
  reclassified as a pass.
- Separate fresh flat-showcase and normal-terrain runs inspect all ten variants.
- A supplemental saved-world root audit checks lowest wood at/below nominal
  ground +2. Air/water gaps at/below ground fail; raised +1/+2 arches are reported
  rather than silently filled. Taller intentional arches are outside that sample.

The flat showcase `run-20261006-090811-5e8719cd2f57` passed: **1,786,124 raw
exported blocks** across all ten templates, **zero mismatches**, complete matching
bounds/chunks and no blocking log errors. The documented persistent-leaf distance
normalization is retained; raw authored soil cells are included in this comparison.

The natural run `run-20261006-090811-71d7369d50b5`, seed **731204**, passed:

- All ten expected variants located and completely generated; matching bounds.
- **1,854,045 non-excluded blocks**, **zero mismatches**; no read/verification errors.
- **111,748 soil-foundation columns**, **zero unsupported contacts**, no relic overlaps.
- Exact saved-mask coverage for every one of **2,876,936 non-air template cells**.
- Normal server exit (code 0), no blocking log errors in either final run.

Natural verification retains the documented dirt/grass/azalea-leaf exclusions;
the raw showcase checks authored soil cells. The lower natural checked-block count
is not missing geometry: the revised Tower replaces much of its previously
checked sandy foundation with the documented excluded earth palette.
Full-report hashes and artifact identities are preserved in
[compact runtime evidence](alpha4-4-evidence.json). Installation passed without
`--allow-feature-overwrites`.

The supplemental root check was also run against the preserved Alpha 4.3 world
as an expected negative regression: it reports **29 ground-level gaps** and **59
raised +1/+2 gaps**, matching the original art-thread audit. That new root check
fails for the old model; Alpha 4.3's historical soil-foundation/runtime acceptance
is not retroactively relabeled. The baseline is preserved in
[root-contact evidence](alpha4-3-tree-baseline-contacts.json).

The actual Alpha 4.4 Tree has **3,560 low root columns**, **3,527 direct contacts**,
**zero missing expected wood** and **zero ground-level gaps**, versus the old 29.
All ground +1 gaps also closed. **33 raised edges at ground +2** remain reported;
they are not failing earth foundations and have not been filled with new wood or
pillars. The actual-world result is separate from the art-thread projection of
36 remaining gaps. See [new root-contact evidence](alpha4-4-tree-contacts.json).

## Safety and acceptance scope

Before changes, inventories recorded **93,728 files in ten existing worlds**, the
three profile mod JARs and **1,555 source-asset files**. Installation is gated by
strict natural block verification, complete bounds/chunks, solid soil-foundation
contacts, no relic overlap and saved exact-cell protection masks. Post-install
SHA-256 checks confirm all **93,728 files in ten existing worlds** and both updated
dependency JARs unchanged. Model/export assets remain preserved; only the four
relic-index README files are intentionally updated to describe Alpha 4.4. Final
source checks inspected all 1,555 files: **1,551 non-index files unchanged**, the
four expected documentation updates and no unexpected source/export changes.
Local preservation records are under `build/profile-inventory/alpha4-4-*-preservation.json`.

## Test-profile installation

- Installed JAR: `E:\Roaming\ModrinthApp\profiles\Relic Test\mods\relics-0.1.0-alpha.4.4+mc26.2.jar`.
- Previous Alpha 4.3 JAR hash-verified under
  `build/profile-backups/0.1.0-alpha.4.4-upgrade-20261006-091843/`; SHA-256
  `5a4d4e47e82c3141a192b788fca5c10d8a52fc6d002b1892969de2030db4e585`.
- New flat save: **Relic Alpha 4.4 Showcase 20261006-091843**.
- New natural save: **Relic Alpha 4.4 Terrain 20261006-091856**, seed 731204,
  creative/cheats, normal difficulty, mobs and random ticks enabled. Spawn:
  `[-53411, 80, 45280]`, yaw 90, facing the large Colossus.
- The terrain copy reloaded its saved masks and passed full strict verification:
  all ten variants, 1,854,045 non-excluded blocks, zero mismatches, zero unsupported
  soil contacts, zero unprotected template cells and no relic overlaps.
- Normal server-level commands removed and restored the protected art cell at
  `[-53636, 196, 45278]`; its exact final state is `green_terracotta`. Evidence:
  `build/terrain-preview/20261006-091856/report.json`.
- A second root-contact audit read the final installed terrain save: still zero
  ground-level gaps, no missing expected wood and 33 raised ground +2 edges. See
  [post-reload root evidence](alpha4-4-tree-reload-contacts.json).
- Both new saves have their exact unique title, creative mode and cheats verified.
  Existing generated relics are not updated retroactively; earlier saves remain intact.

Flat viewpoints, Small Colossus / Tree / Tower:

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

Fly higher/farther back to inspect the Tree crown and Tower top. These sites have
the revised models; old saves retain old generated structures.

## Acceptance limits

Runtime scope is vanilla terrain with the listed Fabric/Lithostitched baseline,
not a complete personal modpack or third-party terrain-mod acceptance. Slow
locators and default-watchdog performance remain separate from artistic review.
The rock Skull locator took **74.5 seconds** with the isolated server's 180-second
watchdog; this is not default-60-second dedicated-server performance acceptance.
Client visual approval of the revised ground/model art remains separate.
