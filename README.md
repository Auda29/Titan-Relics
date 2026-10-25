# Relic Mod

Rare, monumental discoveries for Minecraft: colossi, an obelisk, titan skulls,
a world tree and a ruined tower.

**Development code integrated into `main`, October 8:** `0.1.0-alpha.5.0-dev` adds the four
custom items, original sprites/Monolith masks, maintenance/smithing recipes and
opt-in golem/Vault/map/Tree-aura adapters. **Not a tested gameplay release:** no
server/client was started during that item implementation. Natural interior/reward
marker integration remains pending. **October 25:** fresh 26.2/Fabric worlds now
use the shared rarity plan, a single saved large-Colossus destination and linked
expedition maps. Existing worlds retain legacy generation. See the
[distribution implementation and runtime evidence](docs/testing/DISTRIBUTION_IMPLEMENTATION_20261025.md)
and the [earlier item implementation boundaries](docs/testing/GAMEPLAY_IMPLEMENTATION_20261008.md).
The structure agent's [five interior candidates and marker handoff](docs/project/GAMEPLAY_INTERIORS_HANDOFF.md)
are preserved alongside this code, with editable Blender sources, NBT/schematic
and hash-bound sidecars. Git integration does not activate these candidates in
natural generation or constitute visual/runtime acceptance.
The following Alpha 4.9 section remains the preserved visual-release baseline.

**Latest art follow-up:** [Open cave contacts and sparse Tree root strands](docs/testing/CAVE_CONTACTS_20261007.md)
address the Alpha 4.8 screenshots. Skull 2's raw anatomy/sword remains exact;
accepted Tree art and world pose are preserved while later root additions change.

**Current visual-alpha build: 0.1.0-alpha.4.9 for Minecraft 26.2 / Fabric.** Seven relic
designs are selected: **Colossus V4.1 materials B, Obelisk V4.2, Titan Skull V4
(four biome variants), Small Colossus V7, World Tree V4.3 strands, Ruined Tower V7
and Titan Skull 2 V2 embedded-v1**. Rock Skull uses embedded-v1; meadow/dry/sand
Skulls, Small Colossus and Tower retain their ground-v3 derivatives.
This is a visual integration build, not planned gameplay. **The user visually
accepted Skull 2 and World Tree, including their current terrain integration,
on October 7 after the Alpha 4.9 screenshot review.** See the
[acceptance and eight screenshot hashes](docs/project/reviews/alpha4-9-user-acceptance-20261007.json).
This does not extend to other relic revisions or gameplay completion.
The [Alpha 4.2 terrain correction](docs/technical/ALPHA_4_2_TERRAIN.md) adds
chunk-local ground supports and conservative relic separation. Current validation
is recorded in the [Alpha 4.9 test report](docs/testing/ALPHA_4_9_TEST_REPORT.md).
Alpha 4.9 replaces the Tree's later bulk root extrusion with 1,883 attached cells
along 50 sparse strand/fork paths. Skull 2's natural template alone omits 7,309
deeply buried cells below raw Y22; its complete raw export and ground Y28 remain.
Both profiles bridge only complete short gaps of up to two cells in the adjoining
art material. Deep root undersides and longer caves deliberately remain open,
with explicit clearance classification instead of dirt walls or wooden piers.
Alpha 4.7's surface biome anchors, full dry-land grid, site tolerances, density
and separation remain active. Eight other raw/natural template pairs are unchanged.
The omitted-air policy still preserves native vegetation in unoccupied cells;
the historical three-leaf Skull 2 cavity observation remains documented as a
failed strict air-only probe, not missing art or a failed support contact.
“Relic Test” now has the verified Alpha 4.9 JAR, with Alpha 4.8 backed up and
the separate **`Relic Alpha 4.9 Terrain 20261007-121429`** inspection save.
All ten variants pass complete source acceptance and post-reload verification;
bounded cave clearances remain explicitly classified, not silently filled.
See [installation, preservation and TP commands](docs/testing/alpha4-9-installation.json).
All 18 pre-existing worlds and source exports are preserved; no extra flat save
is added. The current JAR is `dist/relics-0.1.0-alpha.4.9+mc26.2.jar`.
The [54-image user screenshot review](docs/project/ALPHA_4_7_SCREENSHOT_REVIEW.md)
records remaining visual ground skirts and Tower-wall refinements; these are
proposals, not implemented changes or new user artistic approval.
Real client photographs from an isolated photo copy are available in the
[model/site overview](docs/project/reviews/alpha4-6-client-overview.png) and
[contact-problem details](docs/project/reviews/alpha4-6-client-contacts.png).
The [saved-world contact comparison](docs/project/reviews/alpha4-7-contact-fix.png)
shows the repaired connections at the same locations.
Fabric API 0.161.0 / stable Lithostitched 1.8.0 remain unchanged. Gameplay and
density are still at the visual-alpha baseline. Historical evidence stays in the
[Alpha 4.8 baseline](docs/testing/ALPHA_4_8_TEST_REPORT.md),
[Alpha 4.7 baseline](docs/testing/ALPHA_4_7_TEST_REPORT.md),
[Alpha 4.6 baseline](docs/testing/ALPHA_4_6_TEST_REPORT.md),
[Alpha 4.5 baseline](docs/testing/ALPHA_4_5_TEST_REPORT.md),
[Alpha 4.4 baseline](docs/testing/ALPHA_4_4_TEST_REPORT.md) and
[Alpha 4.3 baseline](docs/testing/ALPHA_4_3_TEST_REPORT.md).
Earlier evidence is also preserved in the
[Alpha 4.2 baseline](docs/testing/ALPHA_4_2_TEST_REPORT.md); client artistic approval
remains separate.
The failed natural-placement baseline remains in the
[Alpha 4.1 test report](docs/testing/ALPHA_4_1_TEST_REPORT.md).
The [Alpha 4 integration](docs/technical/ALPHA_4_INTEGRATION.md) and
[test report](docs/testing/ALPHA_4_TEST_REPORT.md) preserve the preceding artifact's evidence.

**Design decision, October 2:** the large Colossus should be **unique per game
world**, shared by all players; planned smaller Colossi may occur multiple times.
Alpha 4.9 does not enforce uniqueness yet. Its future per-player core vault and
Obelisk maps will serve the same large landmark. Material economy, cockpit/trial design,
core utility, and multiplayer loot remain follow-up tasks in the
[lore/gameplay review](docs/project/LORE_GAMEPLAY_REVIEW.md); no models or generation
rules are changed by that review.

**Lore decisions, October 8:** all Colossi were crewed; the large machine was
central and the smaller ones its companions. The head golem was a cockpit defense
robot. Obelisks marked cleared territories, with skulls scattered widely around
them; the unfinished tower organized the campaign. Titans worshipped the World
Tree and drew strength/size from it, and the Colossi's builders failed to destroy
it. Thousands of years later no living Titans remain; today's mobs and players
reuse the relics. Exact Titan nature and the campaign's motive are lost to time.
See [approved lore](docs/project/LORE-BIBLE.md). Plan all relics' gameplay and
interiors and reconcile documentation before implementing on 26.2/Fabric first.

**Planning closure, October 8:** all seven gameplay plans, technical starting
defaults and documentation reconciliation are recorded in the
[planning review](docs/project/GAMEPLAY_PLAN_REVIEW.md),
[runtime contract](docs/technical/GAMEPLAY_RUNTIME.md),
[builder marker handoff](docs/technical/GAMEPLAY_MARKERS.md) and
[shared distribution/unique-site resolver](docs/technical/RELIC_DISTRIBUTION.md).
The [gameplay acceptance matrix](docs/testing/GAMEPLAY_ACCEPTANCE_PLAN.md) lists
future tests, not completed Minecraft evidence. No gameplay, artwork, exports,
worlds or generation settings changed in that completed planning round. The user
subsequently requested the separate-worktree implementation described above and
its integration into `main`. Structure construction belongs to the separate builder;
custom items/artwork and integration belong to the mod work.

**Latest integration work, October 7, 2026:** all ten selected exports are copied
byte-for-byte for manual placement. Derived worldgen templates retain matching
padding/burial contracts and a replaceable surface-query center anchor. Soil
profiles add foundations; the embedded profiles preserve native terrain, with
explicit clipping/short-contact cave policy only for Skull 2 and Tree.
A 25-point grid checks the padded natural footprint.
Alpha 4.2 rejects failing grids early, checks sampled water directly, extends
supports to actual ground and reserves space around other relic candidates.
Placed model/support cells are protected from late world-generation features,
not from player mining or building.
Crowned Skull variants use disjoint biome tags and one shared structure set.
Legacy DataVersion 3105 is preserved, not relabeled as 4903.

**Obelisk v3** revises the shape to a tapered square antiprism with eight triangular
faces, a 45-degree rotated crown, and only eight blocks of burial.

**[Titan Skull v3](relics/titan-skull/docs/TITAN_SKULL_V3.md)** develops the next asset study: a crowned,
weathered skull based on the opening of *D.E.A.D.*, now approximately Colossus-head
scale, with a broken, partly buried spine and its local grassy mound included in the export.

## In-game demo

**New offline asset studies, October 2:** [Colossus V4](relics/colossus/docs/COLOSSUS_V4_EXPORTS.md)
adds rear armour damage and a raised right hand. **B / open machine frame is the
selected V4 design**; A remains available for comparison. [View the comparison](relics/colossus/design/generated/colossus-v4-open/colossus-v4-changes-review.png).
[Titan Skull V4](relics/titan-skull/docs/TITAN_SKULL_V4_EXPORTS.md) adds interrupted
deposits in meadow, dry-earth, sand and rock palettes.
[Obelisk V4](relics/obelisk/docs/OBELISK_V4_EXPORTS.md) adds restrained weathering
and a sandy foundation site. Latest revisions:
[Colossus V4.1](relics/colossus/docs/COLOSSUS_V4_1.md) lays the right palm upward
with curled fingers; [Obelisk V4.1](relics/obelisk/docs/OBELISK_V4_1.md) uses
consistent sandstone sides and larger cracks. **Colossus V4.1 is visually accepted.**
The latest [Obelisk V4.2](relics/obelisk/docs/OBELISK_V4_2.md) uses warmer ochre
stone and missing pieces without contrasting crack lining. **Obelisk V4.2 and all
four Titan Skull V4 variants are also visually accepted.** Next design priority:
remaining relic concepts before V5 interiors. Alpha 4 now selects the latest versions.

**Colossus V3 in normal terrain with shaders**, captured in Minecraft by the
user on October 1, 2026. These are Alpha 3 screenshots, not Blender previews
or the new V4 studies.

![Colossus V3 viewed across water in a savanna, with shaders](relics/colossus/demo/colossus-v3-shaders-river.png)

See the [three-image demo gallery](relics/colossus/demo/README.md) for the savanna
approach, river view and landscape overview. Shader details were not recorded;
these images do not establish performance or general shader compatibility.

## Repository layout

```text
relics/
  colossus/       # README, docs/, design/, gameplay/, demo/
  obelisk/       # README, docs/, design/, gameplay/
  titan-skull/   # README, docs/, design/, gameplay/
  ruined-tower/  # V1/V2 design candidates, exports and review
  world-tree/    # V1/V2 design candidates, exports and review
docs/
  project/       # Shared concept, lore, and implementation plan
  technical/     # Blender workflow, target environment, and worldgen
  testing/       # Test reports and evidence
src/             # Mod source and packaged resources, kept separate
tools/           # Shared generators, converters, renderers, and build tools
tests/           # Automated checks
structures-src/  # Alpha structure-source metadata
```

Start with the [relic index](relics/README.md) or the
[shared documentation index](docs/README.md). Each relic groups its design history,
asset configs, Blender/export files, and gameplay decisions. Build selection is
explicitly pinned by `tools/relic_catalog.py` and `tools/integrate_relics.py`;
moving exports alone does not select them.

## Structures in Alpha 4.9 (raw exports)

| Relic | Overall dimensions, including base (X/Y/Z) | Design |
| --- | --- | --- |
| Obelisk V4.2 | 59 × 185 × 60 | Warm weathered antiprism with missing stone and sandy foot; ground Y8 |
| Colossus V4.1 materials B | 181 × 209 × 235 | Damaged rear, open machine chest, palm-up hand and salvageable armour; ground Y77 |
| Titan Skull V4 ground-v3 (meadow/dry/sand) | 117 × 79 × 179 each | Preserved crowned skull/spine with low central deposits; ground Y16 |
| Titan Skull V4 rock embedded-v1 | 117 × 79 × 179 | Preserved anatomy without authored stone/gravel platform; ground Y22 |
| Small Colossus V7 ground-v3 | 111 × 80 × 113 | Preserved armour/growth with low soil and four blocks deeper burial; ground Y13 |
| World Tree V4.3 strands | 187 × 228 × 185 | Accepted art translated +12 Y; 1,883 sparse attached root cells along 50 paths, no ground platforms; ground Y24 |
| Ruined Tower V7 ground-v3 | 111 × 232 × 93 | Connected collapsed side bays, broken corner and low foot; 220 visible layers; ground Y12 |
| Titan Skull 2 V2 embedded-v1 | 99 × 136 × 99 | Complete preserved raw skull/sword; natural template alone omits the deep slice below Y22; ground Y28 |

All use vanilla blocks and have natural generation resources for new Overworld
chunks. Each rotates as one unit. Optional Terralith/Biomes O' Plenty mappings
remain provisional; neither mod is required. Runtime coverage is recorded in the test report.

## Installation

For Minecraft **1.21.1**, use the separate **Alpha 4.9 Fabric port**, not the
26.2 JAR. See [compatibility build/install instructions](compat/mc1.21.1/README.md)
and [its validation/release record](docs/testing/ALPHA_4_9_MC_1_21_1_TEST_REPORT.md).
It needs Java 21+, Fabric API 0.116.17+1.21.1 and Lithostitched 1.8.0 for 1.21.1.
**Never downgrade a 26.2 save to 1.21.1.** The requirements below describe the
primary 26.2 build.

Downloads: [Alpha 4.9 for Fabric 1.21.1](https://github.com/Auda29/Relic-Mod/releases/tag/v0.1.0-alpha.4.9%2Bmc1.21.1),
or the [historical Alpha 3 for Fabric 26.2](https://github.com/Auda29/Relic-Mod/releases/tag/v0.1.0-alpha.3).
Alpha 3 contains only the three original V3 designs and its documented natural
feature-overwrite limitations; it is not the current seven-design 26.2 build.

| Requirement | Tested alpha version |
| --- | --- |
| Minecraft Java Edition | 26.2 |
| Java | 25 |
| Fabric Loader | 0.19.5 |
| Fabric API | 0.161.0+26.2 |
| Lithostitched | 1.8.0 stable for Fabric 26.2 |

See [Target environment](docs/technical/TARGET_ENVIRONMENT.md), the current
[Alpha 4.9 test report](docs/testing/ALPHA_4_9_TEST_REPORT.md) and historical
[Alpha 3 test report](docs/testing/ALPHA_3_TEST_REPORT.md).

1. Install Fabric for Minecraft 26.2.
2. Put `relics-0.1.0-alpha.4.9+mc26.2.jar`, Fabric API, and Lithostitched in `mods/`.
3. Create a fresh test world with structure generation enabled. Relics are not retroactively added to existing chunks.

Dependencies are available from [Lithostitched](https://modrinth.com/mod/lithostitched) and [Fabric API](https://modrinth.com/mod/fabric-api). Their JARs are not bundled with our release.

To update, fully exit Minecraft and replace the old Relic JAR. Existing structures
retain their previous appearance. Use a new test world or unexplored regions.
The original IDs are retained, but Skull variant biome/distribution rules changed;
`/locate` can still return an old site. Old settings packs override new data;
regenerate them for Alpha 4 before testing the current family distribution.

With cheats or server operator permissions:

```mcfunction
/locate structure relics:obelisk
/locate structure relics:colossus
/locate structure relics:titan_skull
/locate structure #relics:titan_skull
/locate structure relics:small_colossus
/locate structure relics:world_tree
/locate structure relics:ruined_tower
/locate structure relics:titan_skull_2
```

Searches may take time because suitable sites are rare. A successful `/locate` does not prove that every structure chunk has generated. In a separate creative test world, `/place template relics:obelisk` and `/place template relics:colossus` bypass site selection. The supplied position is the template's lower corner, not its intended ground level.

## Build and modify

Python 3.11 or newer handles assets and packaging. Alpha 4.2 also needs **JDK 25**
(set `JAVA_HOME`) and Minecraft/Fabric/Lithostitched compile dependencies for its
small placement-only runtime components. No Gradle or remapping is needed. Local
game caches are reused; a clean checkout can explicitly prepare the isolated cache
with `python tools/setup_worldgen_build.py --accept-downloads`.

```shell
python tools/build.py
python -m unittest discover -s tests -v
python tools/test_worldgen_java.py
```

On Windows, `./build.ps1` is also available. It looks for Python in PATH, then the existing Codex Python runtime path; it installs nothing.

Outputs are written to `dist/`, including `SHA256SUMS.txt`. The build selects
existing NBT exports, derives centered natural templates and uses fixed archive
timestamps. It does not regenerate Blender models. Git tracks generators,
worldgen data and selected source deliverables in each relic's design folder.
Render scenes, OBJ intermediates, tiles, local test worlds and build outputs
remain excluded through `.gitignore`.

The selection contract in [tools/relic_catalog.py](tools/relic_catalog.py) defines
current sources, hashes, sizes, ground levels and matching worldgen resources.
The packaged `relics.integration.json` records provenance. Historical
`tools/integrate_v3.py` and `tools/relic_assets.py` remain regression tools,
not default build inputs.

The exporter supports whole templates and rigid tiles. Natural generation uses only whole templates, so the arm cannot disappear because of a failed piece connection.

## Reference-based Blender assets

[October 4 V2 revisions](docs/project/RELICS_V2_REVIEW.md): the small Colossus is
rebuilt as an independent relative of the large bronze machine; the World Tree
uses a branch-grown canopy; the Ruined Tower now has 220 visible block layers.
These are new visual candidates. **Titan Skull 2 V1 is visually accepted for now.**
The [Small Colossus V4 baseline](relics/colossus/docs/SMALL_COLOSSUS_V4.md) follows the
user's new [Vigilant-Class reference](relics/colossus/docs/SMALL_COLOSSUS_V4_REFERENCE.md):
a massive dormant plated specimen with multiple optical lenses and pincer hands.
V2 was judged too similar to the large Colossus; V3 was rejected as too skeletal.
The [October 5 screenshot revision](docs/project/SCREENSHOT_REVISIONS_20261005.md)
adds V5's slumped posture/weathering, the finer World Tree V3 canopy, Ruined Tower
V3's broken storeys and natural placement foundations.

[Four new V1 assets](docs/project/NEW_RELICS_V1.md) are available for visual review:
Ruined Tower, World Tree, the smaller archive-derived Colossus and independent
Titan Skull 2 with an embedded sword. Each includes editable Blender source,
NBT/schematic, verification and actual-block review images. Alpha 4 selects the
latest successors listed above, not rejected or superseded intermediate versions.

New [Colossus material study B](relics/colossus/docs/COLOSSUS_MATERIAL_STUDY_B.md):
exactly the accepted V4.1 form, with salvageable copper armour and permanent
supporting material. All 223,161 positions are unchanged; the candidate retains
25,423 copper blocks and 90 raw iron items. Post-mining connectivity checks pass;
the user accepted the intact and post-salvage appearance on October 2, 2026.

Review sheets, editable Blender sources, NBT/Schematic exports, and export metadata are kept in
each relic's `design/generated/<asset>/` directory under [relics/](relics/README.md), grouped by asset version. These are
design exports; Alpha 4's selection is pinned in its integration catalog.

The implemented asset pipeline is **Blender → triangulated OBJ → local, open-source ObjToSchematic 1.0 → Sponge `.schem` → Java `.nbt`**. Setup, materials, air handling, and commands are documented in [Blender workflow](docs/technical/BLENDER_WORKFLOW.md).

| Asset | Dimensions X/Y/Z | Blocks | Design |
| --- | --- | --- | --- |
| [Colossus v2](relics/colossus/docs/COLOSSUS_V2.md) | 181 × 160 × 227 | 182,734 | Bronze dome helmet, respirator hoses, broad armor, vegetation, and detached arm |
| [Colossus v3](relics/colossus/docs/COLOSSUS_V3.md) | 181 × 209 × 227 | 221,221 | Extends v2 underground to a torn hip; nominal surface at NBT Y ≈ 77 |
| [Colossus V4 A: open](relics/colossus/docs/COLOSSUS_V4_EXPORTS.md) | 181 × 209 × 223 | 221,452 | Rear damage, raised right hand, removed chest piston; comparison alternative |
| [Colossus V4 B: frame](relics/colossus/docs/COLOSSUS_V4_EXPORTS.md) | 181 × 209 × 223 | 222,621 | Earlier selected geometry, superseded by V4.1 materials B |
| [Obelisk v2](relics/obelisk/docs/OBELISK_V2.md) | 23 × 209 × 19 | 90,497 | Flat crown, warm mineral bands, solid sandstone core, and a 32-block buried foot |
| [Obelisk v3](relics/obelisk/docs/OBELISK_V3.md) | 25 × 185 × 25 | 93,153 | Tapered square antiprism, rotated crown, solid core, and an 8-block buried foot |
| [Obelisk V4](relics/obelisk/docs/OBELISK_V4_EXPORTS.md) | 59 × 185 × 60 | 95,038 | Same monolith, shallow chips, weathering, scattered sand and foundations |
| [Obelisk V4.1](relics/obelisk/docs/OBELISK_V4_1.md) | 59 × 185 × 60 | 94,593 | Consistent sandstone facets, three branching cracks, four larger edge spalls |
| [Obelisk V4.2](relics/obelisk/docs/OBELISK_V4_2.md) | 59 × 185 × 60 | 94,422 | Warm ochre/clay facets, same-material recesses, two additional missing edge chunks |
| [Colossus V4.1 frame](relics/colossus/docs/COLOSSUS_V4_1.md) | 181 × 209 × 235 | 223,161 | Palm-up right hand, curled fingers; preserved V4 B body and chest |
| [Titan Skull v1](relics/titan-skull/docs/TITAN_SKULL_V1.md) | 185 × 203 × 103 | 103,943 | Organic crown, hollow cranium, open jaw, and curved lateral spur; nominal ground Y ≈ 13 |
| [Titan Skull v2](relics/titan-skull/docs/TITAN_SKULL_V2.md) | 117 × 80 × 105 | 149,894 | Approximately 76-block skull, complete rear, and solid exported mound; nominal ground Y8 |
| [Titan Skull v3](relics/titan-skull/docs/TITAN_SKULL_V3.md) | 121 × 79 × 203 | 264,355 | Same skull scale, nine partly buried vertebrae, two fractures, and extended exported hill |
| [Titan Skull V4](relics/titan-skull/docs/TITAN_SKULL_V4_EXPORTS.md) | 117 × 79 × 179 | 136,569 each | Preserved anatomy, brighter fossil palette, interrupted deposits; four ground variants |

Dimensions include buried geometry and, for the Colossus, the detached arm.
Absolute scale is an artistic estimate. Blender previews show actual exported
blocks but are not Minecraft screenshots; client visual acceptance remains
separate from server checks. Older exports above are retained as design history.

At their nominal ground planes, Obelisk v3 exposes approximately **177 block
layers**, versus **132** for Colossus v3. It therefore rises about **45 blocks
(34%) higher above terrain**, although the Colossus is taller overall. This is
a chosen visual relationship, not a measured ratio between the separate references.

Titan Skull v2/v3 is approximately **76 blocks tall including its crown**, about
**20% taller than the Colossus's measured 63-block helmet shell**. Its total
template includes the supporting mound and foundation; the head-size comparison
uses actual NBT geometry at the same block scale.

### Convert a schematic

Sponge v2/v3 schematics can be converted without Minecraft or extra Python packages:

```shell
python tools/schem_to_nbt.py model.schem relics/colossus/design/imported/model.nbt --air omit
```

- `--air omit` skips all air and preserves existing terrain there, including inside modeled rooms.
- `--air keep` includes all air in the export box and can clear terrain outside the silhouette.
- `minecraft:structure_void` is always omitted.
- `--tile-size 32` adds tiles and relative origins in `model.manifest.json`.

The air policy is mandatory. The converter does not automatically distinguish room air from exterior air. Coordinates are local to the lower model corner; the schematic offset is recorded rather than added. Block names, states, and `DataVersion` are preserved without migration. Entities and block entities, such as filled chests, are rejected with an error.

ObjToSchematic exports currently use DataVersion **3105**, while the target game uses **4903**. Target-game validation remains necessary. Obelisk v2/v3 explicitly fill enclosed cells before schematic export; the Colossus assets use surface voxelization.

### Previews

The optional alpha renderer uses Pillow and simplified block colors:

```shell
python -m pip install Pillow
python tools/render_preview.py
```

Images are written to `relics/<relic>/design/generated/alpha/`. Use `--output <directory>` to collect them in a custom directory instead. They are geometry previews, not Minecraft screenshots, and are not needed for the mod build. The Blender asset pages provide commands for textured NBT previews and reference comparison sheets.

## Configure density and enabled relics

Generate a world-specific override datapack, for example more frequent discoveries without colossi:

```shell
python tools/configure.py --density frequent --disable colossus
```

Profiles are `rare`, `normal`, and `frequent`. Repeat `--disable` for `obelisk`,
`colossus`, `titan_skull`, `small_colossus`, `world_tree`, `ruined_tower` or
`titan_skull_2`. Disabling `titan_skull` disables all four crowned variants.
Put the generated settings ZIP in the world's datapack directory above mod data,
then restart; `/reload` alone is not assumed sufficient for worldgen changes.

Existing relics remain. While a type is disabled, `/locate` cannot find its existing sites either; re-enabling restores searches and future generation. Profiles control candidates, not guaranteed discoveries: biomes and terrain reject unsuitable sites. There is no settings menu or built-in rejection statistics.

## Known alpha limits

- Grid-based terrain checks can miss small pools and edges between sample points.
- Selected templates omit air and preserve terrain in unspecified cells. Buried cavities are not automatically excavated; final interiors and routes are not implemented.
- Precise collision checks against Dungeons & Taverns or other structures are not implemented.
- Shapes are fixed. Seed-dependent generator variants are a development tool, not selected per discovery.
- There is no new loot, movement mechanic, quest system, or custom sound.
- All seven models have worldgen resources, but no authored encounters or special
  loot. Large-Colossus uniqueness and the wider skull/bone-family budget remain open.

## Documentation

- [Shared documentation index](docs/README.md)
- [Relic design and gameplay index](relics/README.md)
- [Technical implementation plan](docs/project/UMSETZUNGSPLAN.md)
- [Lore bible and design guide](docs/project/LORE-BIBLE.md)
- [Concept and reference catalog](docs/project/Minecraft-Relikte-Modplan.md)
- [Alpha world generation](docs/technical/WORLDGEN.md)
- [Blender workflow](docs/technical/BLENDER_WORKFLOW.md)
- [Alpha 4 current relic integration](docs/technical/ALPHA_4_INTEGRATION.md)
- [Alpha 4 test report](docs/testing/ALPHA_4_TEST_REPORT.md)
- [Alpha 2 test report](docs/testing/ALPHA_2_TEST_REPORT.md)
- [Alpha 3 V3 integration test report](docs/testing/ALPHA_3_TEST_REPORT.md)
- [Historical Alpha 1 test report](docs/testing/ALPHA_TEST_REPORT.md)
- [Changelog](CHANGELOG.md)

Shared documentation is maintained in English; the V4 in-game review notes are
recorded in German. Links and pipeline paths follow the per-relic layout above.

An open-source license has not yet been selected; mod metadata uses `All-Rights-Reserved`. Third-party reference images and mod JARs are not included in the published package.
