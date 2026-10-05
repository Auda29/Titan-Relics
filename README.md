# Relic Mod

Rare, monumental discoveries for Minecraft: colossi, an obelisk, titan skulls,
a world tree and a ruined tower.

**Latest art follow-up:** [World Tree V4, Small Colossus V6 and Ruined Tower V4](docs/project/ALPHA_4_2_ART_FOLLOWUP.md)
address the Alpha 4.2 screenshots; exported visual candidates with before/after reviews.

**Current candidate build: 0.1.0-alpha.4.3 for Minecraft 26.2 / Fabric.** Seven relic
designs are selected: **Colossus V4.1 materials B, Obelisk V4.2, Titan Skull V4
(four biome variants), Small Colossus V6, World Tree V4, Ruined Tower V4 and
Titan Skull 2 V1**. This is a visual integration build, not planned gameplay.
Small Colossus, Tree and Tower remain visual candidates. See the
[Alpha 4.2 art follow-up](docs/project/ALPHA_4_2_ART_FOLLOWUP.md).
The [Alpha 4.2 terrain correction](docs/technical/ALPHA_4_2_TERRAIN.md) adds
chunk-local ground supports and conservative relic separation. Current validation
is recorded in the [Alpha 4.3 test report](docs/testing/ALPHA_4_3_TEST_REPORT.md).
Alpha 4.3 selects the new art without changing gameplay, density or terrain support
policy. Full showcase and strict natural-placement verification passed, and the
tested JAR is installed in “Relic Test” with an Alpha 4.2 backup and new showcase
and natural-terrain saves. The terrain copy also passed reload and normal-editability
checks. Existing worlds, source exports and other mods remain unchanged.
Its own evidence is separate from the passing
[Alpha 4.2 baseline](docs/testing/ALPHA_4_2_TEST_REPORT.md); client artistic approval
remains separate.
The failed natural-placement baseline remains in the
[Alpha 4.1 test report](docs/testing/ALPHA_4_1_TEST_REPORT.md).
The [Alpha 4 integration](docs/technical/ALPHA_4_INTEGRATION.md) and
[test report](docs/testing/ALPHA_4_TEST_REPORT.md) preserve the preceding artifact's evidence.

**Design decision, October 2:** the large Colossus should be **unique per game
world**, shared by all players; planned smaller Colossi may occur multiple times.
Alpha 4 does not enforce uniqueness yet. Its future per-player core vault and
Obelisk maps will serve the same large landmark. Material economy, trial history,
core utility, and multiplayer loot remain follow-up tasks in the
[lore/gameplay review](docs/project/LORE_GAMEPLAY_REVIEW.md); no models or generation
rules are changed by that review.

**Latest integration work, October 5, 2026:** all ten selected exports are copied
byte-for-byte for manual placement. Derived worldgen templates add soil-column
foundations and a replaceable center anchor, with matching vertical-padding and
burial contracts. A 25-point grid checks the padded natural footprint.
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

## Structures in Alpha 4.3 (raw exports)

| Relic | Overall dimensions, including base (X/Y/Z) | Design |
| --- | --- | --- |
| Obelisk V4.2 | 59 × 185 × 60 | Warm weathered antiprism with missing stone and sandy foot; ground Y8 |
| Colossus V4.1 materials B | 181 × 209 × 235 | Damaged rear, open machine chest, palm-up hand and salvageable armour; ground Y77 |
| Titan Skull V4 | 117 × 79 × 179 each | Crowned skull, broken spine and interrupted deposits; four biome palettes; ground Y8 |
| Small Colossus V6 | 111 × 80 × 113 | Overlapping chamfered armour, slumped helmet and darker pincers; candidate; ground Y9 |
| World Tree V4 | 187 × 216 × 185 | Spreading branch fans, connected woody skeleton and irregular foliage; candidate; ground Y8 |
| Ruined Tower V4 | 111 × 232 × 93 | Fractured crown, broken stair and inner masonry relief, 220 visible layers; candidate; ground Y12 |
| Titan Skull 2 V1 | 105 × 144 × 107 | Independent skull with embedded sword; ground Y12 |

All use vanilla blocks and have natural generation resources for new Overworld
chunks. Each rotates as one unit. Optional Terralith/Biomes O' Plenty mappings
remain provisional; neither mod is required. Runtime coverage is recorded in the test report.

## Installation

| Requirement | Tested alpha version |
| --- | --- |
| Minecraft Java Edition | 26.2 |
| Java | 25 |
| Fabric Loader | 0.19.5 |
| Fabric API | 0.160.0+26.2 |
| Lithostitched | 1.8.0+beta6 for Fabric 26.2 |

See [Target environment](docs/technical/TARGET_ENVIRONMENT.md), the current
[Alpha 4.3 test report](docs/testing/ALPHA_4_3_TEST_REPORT.md) and historical
[Alpha 3 test report](docs/testing/ALPHA_3_TEST_REPORT.md).

1. Install Fabric for Minecraft 26.2.
2. Put `relics-0.1.0-alpha.4.3+mc26.2.jar`, Fabric API, and Lithostitched in `mods/` after runtime validation.
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
