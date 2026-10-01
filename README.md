# Relic Mod

Rare, monumental discoveries for Minecraft: a desert obelisk and an overgrown, explorable machine colossus with a detached arm.

**Current playable build: 0.1.0-alpha.2 for Minecraft 26.2 / Fabric.** Python generators build the structures automatically. Alpha 2 adds weathering, vegetation, and shorter terrain transitions. Broader multi-seed acceptance testing for version 0.1 is still pending.

**Latest asset work, October 1, 2026:** reference-based Colossus v2/v3 and Obelisk v2/v3 have reproducible Blender → ObjToSchematic → NBT pipelines and verified block exports. The current design pair is **Colossus v3 and Obelisk v3**. Their integration into the mod build and natural world generation is still pending.

**Obelisk v3** revises the shape to a tapered square antiprism with eight triangular
faces, a 45-degree rotated crown, and only eight blocks of burial.

**[Titan Skull v3](relics/titan-skull/docs/TITAN_SKULL_V3.md)** develops the next asset study: a crowned,
weathered skull based on the opening of *D.E.A.D.*, now approximately Colossus-head
scale, with a broken, partly buried spine and its local grassy mound included in the export.

## Repository layout

```text
relics/
  colossus/       # README, docs/, design/, gameplay/
  obelisk/       # README, docs/, design/, gameplay/
  titan-skull/   # README, docs/, design/, gameplay/
  ruined-tower/  # Planning folders; no asset yet
  world-tree/    # Planning folders; no asset yet
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
asset configs, Blender/export files, and gameplay decisions. Moving design exports
does not select them for the playable mod build.

## Structures in Alpha 2

| Relic | Overall dimensions, including base (X/Y/Z) | Design |
| --- | --- | --- |
| Obelisk | 25 × 70 × 25 blocks | Connected cracks, broken edges, windblown sand, and small debris around the base |
| Colossus | 100 × 66 × 76 blocks | Broken helmet and chest armor with internal supports, damaged chest ring, denser vegetation on one side, accessible interior, and detached arm |

Both use vanilla blocks and generate in suitable new Overworld chunks. Each complete structure rotates as one unit. There is currently one prepared variant per type. Optional biome mappings support Terralith and Biomes O' Plenty; neither is a required dependency.

## Installation

| Requirement | Tested alpha version |
| --- | --- |
| Minecraft Java Edition | 26.2 |
| Java | 25 |
| Fabric Loader | 0.19.5 |
| Fabric API | 0.160.0+26.2 |
| Lithostitched | 1.8.0+beta6 for Fabric 26.2 |

See [Target environment](docs/technical/TARGET_ENVIRONMENT.md) for the recorded installation and [Alpha 2 test report](docs/testing/ALPHA_2_TEST_REPORT.md) for completed checks and their limits.

1. Install Fabric for Minecraft 26.2.
2. Put `relics-0.1.0-alpha.2+mc26.2.jar`, Fabric API, and Lithostitched in `mods/`.
3. Create a fresh test world with structure generation enabled. Relics are not retroactively added to existing chunks.

Dependencies are available from [Lithostitched](https://modrinth.com/mod/lithostitched) and [Fabric API](https://modrinth.com/mod/fabric-api). Their JARs are not bundled with our release.

To update, fully exit Minecraft and replace the old Relic JAR. Existing structures retain their previous appearance. Use a new test world or unexplored regions to see new geometry. Structure IDs and distribution rules are unchanged, so `/locate` may still return an old location.

With cheats or server operator permissions:

```mcfunction
/locate structure relics:obelisk
/locate structure relics:colossus
```

Searches may take time because suitable sites are rare. A successful `/locate` does not prove that every structure chunk has generated. In a separate creative test world, `/place template relics:obelisk` and `/place template relics:colossus` bypass site selection. The supplied position is the template's lower corner, not its intended ground level.

## Build and modify

Python 3.11 or newer is sufficient to generate, test, and package the mod. There is no custom Java code, so this build does not require Gradle, Loom, or Java compilation.

```shell
python tools/build.py
python -m unittest discover -s tests -v
```

On Windows, `./build.ps1` is also available. It looks for Python in PATH, then the existing Codex Python runtime path; it installs nothing.

Outputs are written to `dist/`, including `SHA256SUMS.txt`. The build regenerates NBT from source and uses fixed archive timestamps. Git tracks generators, worldgen data, and selected asset deliverables directly inside each `relics/<relic>/design/generated/<asset>/` directory: `*review.png`, `*-source.blend`, whole `.nbt` templates, `.schem` exports, `.design.json`, `.ots.json`, and `verification.json`. Render scenes, Blender backups, OBJ/MTL intermediates, individual renders, tile folders and manifests, build outputs, and local reference media are excluded through `.gitignore`.

The `obelisk()` and `colossus()` functions in [tools/relic_assets.py](tools/relic_assets.py) define the playable alpha's geometry, materials, rooms, and damage. Changes to dimensions or ground level require matching worldgen filter changes. Export manifests record dimensions, ground level, and checksums.

The exporter supports whole templates and rigid tiles. Natural generation uses only whole templates, so the arm cannot disappear because of a failed piece connection.

## Reference-based Blender assets

Review sheets, editable Blender sources, NBT/Schematic exports, and export metadata are kept in
each relic's `design/generated/<asset>/` directory under [relics/](relics/README.md), grouped by asset version. These are
design exports; their presence in the repository does not integrate them into worldgen.

The implemented asset pipeline is **Blender → triangulated OBJ → local, open-source ObjToSchematic 1.0 → Sponge `.schem` → Java `.nbt`**. Worldgen integration is the next step. Setup, materials, air handling, and commands are documented in [Blender workflow](docs/technical/BLENDER_WORKFLOW.md).

| Asset | Dimensions X/Y/Z | Blocks | Design |
| --- | --- | --- | --- |
| [Colossus v2](relics/colossus/docs/COLOSSUS_V2.md) | 181 × 160 × 227 | 182,734 | Bronze dome helmet, respirator hoses, broad armor, vegetation, and detached arm |
| [Colossus v3](relics/colossus/docs/COLOSSUS_V3.md) | 181 × 209 × 227 | 221,221 | Extends v2 underground to a torn hip; nominal surface at NBT Y ≈ 77 |
| [Obelisk v2](relics/obelisk/docs/OBELISK_V2.md) | 23 × 209 × 19 | 90,497 | Flat crown, warm mineral bands, solid sandstone core, and a 32-block buried foot |
| [Obelisk v3](relics/obelisk/docs/OBELISK_V3.md) | 25 × 185 × 25 | 93,153 | Tapered square antiprism, rotated crown, solid core, and an 8-block buried foot |
| [Titan Skull v1](relics/titan-skull/docs/TITAN_SKULL_V1.md) | 185 × 203 × 103 | 103,943 | Organic crown, hollow cranium, open jaw, and curved lateral spur; nominal ground Y ≈ 13 |
| [Titan Skull v2](relics/titan-skull/docs/TITAN_SKULL_V2.md) | 117 × 80 × 105 | 149,894 | Approximately 76-block skull, complete rear, and solid exported mound; nominal ground Y8 |
| [Titan Skull v3](relics/titan-skull/docs/TITAN_SKULL_V3.md) | 121 × 79 × 203 | 264,355 | Same skull scale, nine partly buried vertebrae, two fractures, and extended exported hill |

Dimensions include buried geometry and, for the Colossus, the detached arm. Absolute scale is an artistic estimate from the references. Previews render actual exported NBT blocks in Blender. Titan Skull v2/v3 include their local hills in the export; distant scenery and scale figures are presentation aids. These assets have not been tested in-game. The alpha build still uses `tools/relic_assets.py`.

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

Profiles are `rare`, `normal`, and `frequent`. Repeat `--disable` for `obelisk` and `colossus` as needed. Put `dist/relics-settings.zip` in the world's datapack directory with higher priority than the mod data. Load settings at world/server startup; `/reload` alone is not assumed sufficient for these worldgen changes.

Existing relics remain. While a type is disabled, `/locate` cannot find its existing sites either; re-enabling restores searches and future generation. Profiles control candidates, not guaranteed discoveries: biomes and terrain reject unsuitable sites. There is no settings menu or built-in rejection statistics.

## Known alpha limits

- Grid-based terrain checks can miss small pools and edges between sample points.
- The interior route is traversable within the template; the terrain-to-entrance transition may have a step.
- Precise collision checks against Dungeons & Taverns or other structures are not implemented.
- Shapes are fixed. Seed-dependent generator variants are a development tool, not selected per discovery.
- There is no new loot, movement mechanic, quest system, or custom sound.
- The titan skull is a separate exported asset study, not yet a playable structure.
  The ruined tower and world tree are not implemented.

## Documentation

- [Shared documentation index](docs/README.md)
- [Relic design and gameplay index](relics/README.md)
- [Technical implementation plan](docs/project/UMSETZUNGSPLAN.md)
- [Lore bible and design guide](docs/project/LORE-BIBLE.md)
- [Concept and reference catalog](docs/project/Minecraft-Relikte-Modplan.md)
- [Alpha world generation](docs/technical/WORLDGEN.md)
- [Blender workflow](docs/technical/BLENDER_WORKFLOW.md)
- [Alpha 2 test report](docs/testing/ALPHA_2_TEST_REPORT.md)
- [Historical Alpha 1 test report](docs/testing/ALPHA_TEST_REPORT.md)
- [Changelog](CHANGELOG.md)

Documentation is maintained in English. Links and pipeline paths follow the per-relic layout above.

An open-source license has not yet been selected; mod metadata uses `All-Rights-Reserved`. Third-party reference images and mod JARs are not included in the published package.
