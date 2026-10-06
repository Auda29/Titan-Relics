# Alpha 4.5 — deposit relief and lower Tower walls

October 6, 2026. Candidate: `relics-0.1.0-alpha.4.5+mc26.2.jar`, Minecraft 26.2 / Fabric.
The user requested integration of the latest structure updates into “Relic Test”
and subsequently authorized committing and pushing all pending project work.

**Fresh showcase, strict natural placement and actual root-contact checks passed.**
The verified artifact is installed in “Relic Test”, with an Alpha 4.4 backup and
separate new showcase/terrain saves. The terrain copy also passed reload,
strict block/mask verification, normal editability and the root-contact check.
The passing Alpha 4.4 runs do not certify the changed templates.

## Selection and scope

| Template | Selected export | X × Y × Z | Raw blocks | Ground Y |
| --- | --- | --- | ---: | ---: |
| Crowned Skull, four biome variants | V4 meadow/dry/sand/rock `ground-v2` | 117 × 79 × 179 each | 123,861 each | 8 |
| Small Colossus | V7 `ground-v2` | 111 × 80 × 113 | 233,492 | 9 |
| World Tree | V4.1 `ground-v2` | 187 × 216 × 185 | 292,646 | 8 |
| Ruined Tower | V6 `ground-v2` | 111 × 232 × 93 | 297,352 | 12 |
| Titan Skull 2 | V1 `ground-v2` | 105 × 144 × 107 | 85,152 | 12 |

Large Colossus V4.1 materials B and Obelisk V4.2 retain their Alpha 4.4 hashes.
The eight ground derivatives interrupt regular authored soil/rock contours.
Tower V6 also breaks the rectangular lower annex walls and adds lower shell
breaches, while keeping 220 visible layers. See the
[art and derivation record](../project/DEPOSIT_RELIEF_20261006.md).

Ground derivatives are explicit block-space operations on preserved exports,
not fresh OBJ conversions. Every non-terrain cell must match its pinned source
exactly; the Tower's source is the separately authored V6. Tree wood, foliage,
moss and root stones also remain exactly identical to accepted V4.
Shared terrain/art materials, including Skull 2 moss, remain protected as art.
All ten raw templates are shipped byte-for-byte, retaining DataVersion 3105.

Density, biome mappings, burial, dimensions, placement policy, reservations and
persistent exact-cell masks remain unchanged. Gameplay, rewards and broader
balancing are outside scope. New terrain derivatives remain visual candidates.

## Reproduction and regression checks

Integration pins the eight selected derivative hashes. The ground builder now
also pins its preserved Alpha 4.4 inputs independently of the current mod
selection, so rebuilding cannot erode a derivative a second time. The comparison
renderer still uses Alpha 4.4 on the left and the new derivative on the right.

Regression coverage includes all ten raw identities, eight selected versions,
two unchanged exports, exact non-terrain state preservation, prior art underside
contacts after deriving foundations, accepted Tree identity and immutable builder
inputs. Existing terrain, mask, placement, archive and installation gates remain.

Default and `--skip-generation` artifacts are byte-identical, SHA-256:

```text
0f930c9a311e3995a53a912a31f44f2a67f3ef17a638fbc800f33e355d0efcc2
```

Direct JAR inspection confirms all ten raw templates match their source exports
byte-for-byte: **1,721,669 authored blocks** in total. **77 Python tests**,
**738 Java assertions** and **7 JavaScript tests** passed. The Python suite directly
rechecked all **791,876 previously supported art-cell undersides** against the
newly shipped derived templates: no new air beneath any of these cells.

All eight ground exports were also rebuilt in an isolated mirror under
`build/reproducibility/alpha4-5/derivative-mirror-20261006-104853/`:
their NBT bytes and complete verification/provenance records match the selected
exports exactly. No files under `relics/` were regenerated or overwritten.
The result is in `build/reproducibility/alpha4-5/derivative-reproduction.json`.

## Dependency baseline

Unchanged: Minecraft 26.2, Fabric Loader 0.19.5, Java/JDK 25,
Fabric API **0.161.0+26.2**, Lithostitched **1.8.0 stable**.
The user's dependency JARs must not be replaced during installation.

## Fresh runtime validation

The fresh showcase `run-20261006-104446-8e47787878f4` passed: **all ten templates**,
**1,721,669 raw blocks**, **zero mismatches**, complete bounds/chunks, exit code 0
and no blocking log errors.
Persistent-leaf distance normalization remains the only documented authored-state
comparison adjustment in the raw showcase; authored soil cells are included.

The natural run `run-20261006-104446-781ff9011d44`, seed **731204**, passed:

- All ten expected variants located and completely generated, with matching bounds.
- **1,767,353 non-excluded blocks**, **zero mismatches**; no read/verification errors.
- **104,103 soil-foundation columns**, **zero unsupported contacts**, no relic overlaps.
- Exact saved-mask coverage for all **2,671,611 non-air template cells**.
- Normal server exit (code 0), no blocking log errors.

Natural verification retains the documented dirt/grass/azalea-leaf exclusions;
the raw showcase separately checks authored soil cells. Source-report hashes,
artifact identities and all instance results are preserved in
[compact runtime evidence](alpha4-5-evidence.json). Installation passed the strict
gate without `--allow-feature-overwrites`.

Actual Tree root contacts also pass: **3,560 low root columns**, **3,525 direct
contacts**, no missing expected wood, **zero ground-level or ground +1 gaps**.
There are **35 raised edges at ground +2**, versus Alpha 4.4's 33. These are
explicitly reported higher root edges, not failing ground-level contacts or
unsupported soil foundations; they have not been silently filled with pillars.
See [actual Tree root evidence](alpha4-5-tree-contacts.json).

## Preservation and installation

Before integration, inventories recorded **122,103 files in twelve existing worlds**, three
mod JARs and **2,082 source-asset files**. Post-install SHA-256 checks confirm all
**122,103 files in twelve existing worlds** and both dependency JARs unchanged.
Installation backs up Alpha 4.4 and creates uniquely named new inspection saves.
Existing generated relics are not updated retroactively.

All 2,082 source files have already been inspected: **2,077 non-index source files
remain unchanged**; only the five intended relic-index README updates differ.
No source files were added or removed during integration. The user's new art
exports and complete earlier history were not rebuilt or overwritten.
Preservation records are local under `build/profile-inventory/alpha4-5-*.json`.

## Test-profile installation and inspection

- Installed JAR: `E:\Roaming\ModrinthApp\profiles\Relic Test\mods\relics-0.1.0-alpha.4.5+mc26.2.jar`.
- Previous Alpha 4.4 JAR is hash-verified under
  `build/profile-backups/0.1.0-alpha.4.5-upgrade-20261006-105546/`; SHA-256
  `a5aeaba7f3c313c09acfdb438a7d7a3d38de2a702adff21e0b28cc5500115dc3`.
- New flat save: **Relic Alpha 4.5 Showcase 20261006-105546**.
- New natural save: **Relic Alpha 4.5 Terrain 20261006-105552**, seed 731204,
  creative/cheats, normal difficulty, mobs and random ticks enabled. Spawn:
  `[-53411, 80, 45280]`, yaw 90, facing the large Colossus.
- The terrain copy reloaded its saved masks and passed full strict verification:
  all ten variants, 1,767,353 non-excluded blocks, zero mismatches, zero unsupported
  soil contacts, zero unprotected template cells and no relic overlaps.
- Normal server-level commands removed and restored the protected art cell at
  `[-53636, 196, 45278]`; its exact final state is `green_terracotta`. Evidence:
  `build/terrain-preview/20261006-105552/report.json`.
- A second root audit read the final installed terrain save: still zero ground-level
  gaps, no missing expected wood and 35 raised ground +2 edges. See
  [post-reload root evidence](alpha4-5-tree-reload-contacts.json).
- Both new saves have their exact unique title, creative mode and cheats verified.
  Earlier saves and already generated relics remain unchanged.

Natural sites and camera viewpoints are unchanged from Alpha 4.4. Use these in
the **new Alpha 4.5 terrain save**, not an older save with already generated relics:

| Structure | Viewpoint |
| --- | --- |
| Large Colossus | `/tp @s -53411 100 45280 90 0` |
| Small Colossus V7 ground-v2 | `/tp @s -3152 100 -5248 -90 0` |
| Obelisk | `/tp @s 4336 100 -7834 180 0` |
| Crowned Skull — meadow | `/tp @s -10400 100 -17503 180 0` |
| Crowned Skull — dry | `/tp @s 1888 100 -12095 180 0` |
| Crowned Skull — sand | `/tp @s -22832 100 -31855 180 0` |
| Crowned Skull — rock | `/tp @s -59089 100 26160 -90 0` |
| Titan Skull 2 V1 ground-v2 | `/tp @s 7501 100 -5664 90 0` |
| World Tree V4.1 ground-v2 | `/tp @s -41268 100 20672 -90 0` |
| Ruined Tower V6 ground-v2 | `/tp @s 10470 100 2752 90 0` |

Use creative flight; these are airborne viewpoints. Fly higher/back to see the
Tree crown and Tower top. For flat inspection, the Small Colossus / Tree / Tower
viewpoints also retain their previous positions:

```mcfunction
/tp @s 2359 80 -48 0 0
/tp @s 2781 90 -48 0 0
/tp @s 3127 90 -48 0 0
```

## Acceptance limits

Fresh runtime evidence covers vanilla terrain with the listed dependencies, not
a personal modpack or third-party terrain-mod acceptance. Isolated tests use a
180-second watchdog; slow locators do not establish default-60-second dedicated
server acceptance. Client artistic review remains separate from technical tests.
The rock Skull locator took **78.36 seconds**; default-watchdog performance
acceptance remains unresolved, rather than being implied by this passing run.
