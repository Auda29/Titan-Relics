# Alpha 4.9 — Minecraft 1.21.1 compatibility release

October 7, 2026. The user requested a historical Alpha 3 release and a separate
Minecraft 1.21.1 release, and selected **the current Alpha 4.9** as the port's
baseline. This is a real older-API/remapped Fabric build, not relabeled 26.2
bytecode. The primary 26.2 artifact and existing launcher installations stay
unchanged. No existing save is downgraded or opened by these checks.

## Requirements and source identity

- Minecraft **1.21.1**, Java **21+**, Fabric Loader **0.19.5+**.
- Fabric API **0.116.17+1.21.1** and Lithostitched **1.8.0-fabric-21.1**.
  Lithostitched bundles Apollib 1.2.0; dependencies are distributed separately.
- Artifact `dist/relics-0.1.0-alpha.4.9+mc1.21.1.jar`, SHA-256:
  `02383c41431dde7328bcb0245437208c4e36305a154b3318caac8f8df10edfe7`.
- All **20 raw/natural NBT templates** are exact Alpha 4.9 byte matches,
  including the selected Skull 2 natural clipping and Tree V4.3 strands.
  DataVersion 3105 is preserved, not restamped.
- Biomes, density/salts, anchors, slope/dry-land sampling, separation and bounded
  cave-contact profiles are unchanged. Native omitted cells still preserve terrain.

The prior [client acceptance](../project/reviews/alpha4-9-user-acceptance-20261007.json)
applies to the original 26.2 Skull 2/Tree inspection. This port preserves those
templates but does not claim a new client visual, shader or terrain-mod acceptance.

## Compatibility changes

[Separate build profile](../../compat/mc1.21.1/README.md): Gradle 9.5+, Loom
1.17.21, official Mojang development mappings and production intermediary
remapping. All 11 included runtime classes have Java 21 class-file major **65**;
no Minecraft or Fabric dependency classes are bundled.

The adapter bridges ResourceLocation, registries, chunk positions/dirty marking,
dimension minimum, write-zone API and the old abstract StructureProcessor/type
registration. **Old full-template finalization is clipped to the placement
bounding box before support reads and protection-mask writes**, preserving
chunk-local safety. Static mixin selectors are intermediary-remapped; no missing
legacy refmap is declared. The pack uses 1.21.1 data format **48** and its older
resource-loader module. Main Java and model files are not rewritten.

## Build and regression checks

- Shared Java processor/protection/grid/reservation tests pass **755 assertions
  on Java 21**, against the actual 1.21.1 APIs. The legacy outside-box case verifies
  clipping with zero neighboring reads rather than retaining an unplaced cell.
- The final complete Python suite passes **105 tests**, including eight
  compatibility/identity/chunk-locality/fail-closed release checks.
- A forced compilation/remap reproduces the identical launched JAR SHA-256.
- Seven JavaScript regressions pass. A separate skip-generation 26.2 build still
  reproduces the unchanged installed artifact SHA-256
  `3dbffadf501cbc3dee3ffa66ca78f04fa5b6c6032c66f511832c47aa9d45ba22`.
- Packaging verifies target metadata, all 20 NBT hashes, template completeness,
  Java 21 class headers and production mixin selectors before copying to `dist/`.
- Extracting the reusable support-mask audit helper reproduces the previously
  published complete 26.2 cave audit exactly; no historical verdict is changed.

## Isolated Java 21 runtime

The 1.21.1 smoke profile has a separate cache/world/report directory under
`build/smoke-mc1.21.1/`. It uses normal Minecraft's **60000 ms watchdog**, vanilla
terrain and only Fabric API/Lithostitched dependencies. Old gamerule names are
used; the 26.2 harness defaults remain unchanged.

The [complete runtime evidence](alpha4-9-mc1.21.1-evidence.json) records two fresh
Java 21 runs with seed **731204** and matching final JAR/dependency hashes:

- Showcase `run-20261007-124539-c04eb1712f35`: all ten templates,
  **1,499,248 blocks**, zero mismatches, missing/incomplete chunks or blocking
  log errors, normal exit 0.
- Natural `run-20261007-124544-a66edad878c4`: all ten actual starts found through
  ordinary global `/locate`, **1,379,680 checked non-excluded model cells**,
  zero mismatches, missing/incomplete chunks, overlaps, read/verification or
  blocking log errors; normal exit 0.
- **67,209 exposed support undersides** checked with zero unexpected unsupported
  contacts; the same bounded profiles explicitly classify **178 Skull and 177
  Tree intentional clearances** rather than claiming direct ground everywhere.
- **1,682,709 persisted template protection-mask cells** checked, zero missing
  mask cells. Established natural-material exclusions and persistent-leaf
  distance normalization remain explicitly counted.
- Global locators take **1.016–21.828 seconds** in this seed. The ordinary full
  strict installation acceptance validator also passes, with no overwrite
  allowance; no installation into a launcher profile is performed.

[Tree contacts](alpha4-9-mc1.21.1-tree-contacts.json) separately record 3,994 direct
lowest-log contacts, 171 intentional at/below-ground openings, 173 raised edges,
zero missing wood or unexpected short gaps. [Buried contacts](alpha4-9-mc1.21.1-buried-contacts.json)
pass all 3,835 retained Small-Colossus/Tower boundary cells.

The [independent saved-mask audit](alpha4-9-mc1.21.1-support-audit.json) checks all
**448 Skull** and **293 Tree runtime additions**. Every run is attached to authored
art, stays within its surface band, reaches substrate and is at most two cells
long. Materials/states match the adjoining art; no dirt wall is added. All 108
Skull face-probe cells are present. This **1.21.1** site has **two unprotected native
oak leaves**, so its separately reported strict air-only category remains **false**.
The historical **26.2 three-leaf** observation stays unchanged in its own report.
Neither is relabeled as an all-air pass by client visual approval or port validation.

Natural site coordinates and scenery belong to **1.21.1**, not the old 26.2 TP
world. Cross-version fixed-coordinate cave boxes are not treated as same-site
regression evidence. Supplemental Tree/buried contacts and actual added support
runs are checked on the port's own saved natural sites. Air-only cavity findings
are reported separately; no scenery is manually cleared to force a pass.

## Historical Alpha 3 release

The requested [Alpha 3 pre-release](https://github.com/Auda29/Relic-Mod/releases/tag/v0.1.0-alpha.3)
is published from its actual historical commit
`7f10ccc3f9b41fb13ca7add0f37a85b64b1a5dba`, not from the current main branch.
An isolated reconstruction passes all **32 historical tests** and reproduces
`relics-0.1.0-alpha.3+mc26.2.jar` exactly, SHA-256
`530be00274f815d9f7fe93dab6dde3570988b1b1f0c1d21f007d2a0b5042671c`.
The release includes its JAR and matching checksum file. Its known failed strict
natural comparison (13 Colossus and 995 Skull feature edits) is disclosed in the
release notes and [historical test report](ALPHA_3_TEST_REPORT.md), not relabeled
as a pass. It remains a **26.2 / Java 25** release.

## Publication and limits

The separate annotated port marker is **`v0.1.0-alpha.4.9+mc1.21.1`**, with its
own [GitHub pre-release](https://github.com/Auda29/Relic-Mod/releases/tag/v0.1.0-alpha.4.9%2Bmc1.21.1),
JAR and checksum. Its source/tag push follows completed natural validation and
final source checks. The release source also publishes the earlier
local Skull 2/Tree visual-acceptance documentation. It does not retag or rebuild
the original 26.2 artifact. Existing Relic Test mods/saves and model exports are
not modified; only ignored isolated build/test directories and the new port JAR
are created locally. The installed 26.2 JAR still matches its accepted bytes;
all **2,901 model/source files** match the preserved source inventory.
Gameplay remains unfinished; Forge/NeoForge, terrain-mod packs, multiple seeds,
all natural rotations, systematic client/LOD/shader performance and general
locator-latency guarantees are outside this evidence.

**Do not load a Minecraft 26.2 world in 1.21.1.** Use a new or backed-up native
1.21.1 save, the matching dependencies and only one Relic Mod JAR.
