# Relic Mod

Rare, monumental discoveries for Minecraft: a desert obelisk and an overgrown, explorable machine colossus with a detached arm.

**Current playable build: 0.1.0-alpha.2 for Minecraft 26.2 / Fabric.** Python generators build the structures automatically. Alpha 2 adds weathering, vegetation, and shorter terrain transitions. Broader multi-seed acceptance testing for version 0.1 is still pending.

**Latest asset work, October 1, 2026:** reference-based Colossus v2/v3 and Obelisk v2 now have reproducible Blender → ObjToSchematic → NBT pipelines and verified block exports. Their integration into the mod build and natural world generation is still pending.

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

See [Target environment](docs/TARGET_ENVIRONMENT.md) for the recorded installation and [Alpha 2 test report](docs/ALPHA_2_TEST_REPORT.md) for completed checks and their limits.

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

Outputs are written to `dist/`, including `SHA256SUMS.txt`. The build regenerates NBT from source and uses fixed archive timestamps. Git tracks generators and worldgen data. Generated structures, Blender files, previews, release files, and local reference media are excluded through `.gitignore`.

The `obelisk()` and `colossus()` functions in [tools/relic_assets.py](tools/relic_assets.py) define the playable alpha's geometry, materials, rooms, and damage. Changes to dimensions or ground level require matching worldgen filter changes. Export manifests record dimensions, ground level, and checksums.

The exporter supports whole templates and rigid tiles. Natural generation uses only whole templates, so the arm cannot disappear because of a failed piece connection.

## Reference-based Blender assets

The implemented asset pipeline is **Blender → triangulated OBJ → local, open-source ObjToSchematic 1.0 → Sponge `.schem` → Java `.nbt`**. Worldgen integration is the next step. Setup, materials, air handling, and commands are documented in [Blender workflow](docs/BLENDER_WORKFLOW.md).

| Asset | Dimensions X/Y/Z | Blocks | Design |
| --- | --- | --- | --- |
| [Colossus v2](docs/COLOSSUS_V2.md) | 181 × 160 × 227 | 182,734 | Bronze dome helmet, respirator hoses, broad armor, vegetation, and detached arm |
| [Colossus v3](docs/COLOSSUS_V3.md) | 181 × 209 × 227 | 221,221 | Extends v2 underground to a torn hip; nominal surface at NBT Y ≈ 77 |
| [Obelisk v2](docs/OBELISK_V2.md) | 23 × 209 × 19 | 90,497 | Flat crown, warm mineral bands, solid sandstone core, and a 32-block buried foot |

Dimensions include buried geometry and, for the Colossus, the detached arm. Absolute scale is an artistic estimate from the references. Previews render actual exported NBT blocks in Blender; landscapes and scale figures are presentation aids. These assets have not been tested in-game. The alpha build still uses `tools/relic_assets.py`.

### Convert a schematic

Sponge v2/v3 schematics can be converted without Minecraft or extra Python packages:

```shell
python tools/schem_to_nbt.py model.schem design/imported/model.nbt --air omit
```

- `--air omit` skips all air and preserves existing terrain there, including inside modeled rooms.
- `--air keep` includes all air in the export box and can clear terrain outside the silhouette.
- `minecraft:structure_void` is always omitted.
- `--tile-size 32` adds tiles and relative origins in `model.manifest.json`.

The air policy is mandatory. The converter does not automatically distinguish room air from exterior air. Coordinates are local to the lower model corner; the schematic offset is recorded rather than added. Block names, states, and `DataVersion` are preserved without migration. Entities and block entities, such as filled chests, are rejected with an error.

ObjToSchematic exports currently use DataVersion **3105**, while the target game uses **4903**. Target-game validation remains necessary. Obelisk v2 explicitly fills enclosed cells before schematic export; the Colossus assets use surface voxelization.

### Previews

The optional alpha renderer uses Pillow and simplified block colors:

```shell
python -m pip install Pillow
python tools/render_preview.py
```

Images are written to `design/generated/`. They are geometry previews, not Minecraft screenshots, and are not needed for the mod build. The Blender asset pages provide commands for textured NBT previews and reference comparison sheets.

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
- The ruined tower, titan skull, and world tree are not implemented.

## Documentation

- [Technical implementation plan](UMSETZUNGSPLAN.md)
- [Lore bible and design guide](LORE-BIBLE.md)
- [Concept and reference catalog](Minecraft-Relikte-Modplan.md)
- [Alpha world generation](docs/WORLDGEN.md)
- [Blender workflow](docs/BLENDER_WORKFLOW.md)
- [Alpha 2 test report](docs/ALPHA_2_TEST_REPORT.md)
- [Historical Alpha 1 test report](docs/ALPHA_TEST_REPORT.md)
- [Changelog](CHANGELOG.md)

Documentation is maintained in English. Existing document filenames are retained to preserve links.

An open-source license has not yet been selected; mod metadata uses `All-Rights-Reserved`. Third-party reference images and mod JARs are not included in the published package.
