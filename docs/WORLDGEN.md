# Alpha world generation

Updated: October 1, 2026. This page describes **the playable Alpha 2 resources**.
The newer Colossus v2/v3 and Obelisk v2 Blender assets are not integrated into
these placement rules.

The alpha uses Minecraft 26.2 on Fabric with Lithostitched 1.8.0+beta6. Each relic
is a complete rigid NBT template, with no custom Java code. The selected profile,
`E:\Roaming\ModrinthApp\profiles\Relic Test`, was empty at inventory time. Format
checks used JARs from the existing TerraVista profile; that does not establish
compatibility with the entire personal modpack.

## Resources

| Resource | Purpose |
| --- | --- |
| `data/relics/structure/obelisk.nbt` | Whole Obelisk, 25 × 70 × 25 blocks |
| `data/relics/structure/colossus.nbt` | Whole Colossus including arm, 100 × 66 × 76 blocks |
| `worldgen/template_pool/<id>.json` | Exactly one rigid template with weight 1 |
| `worldgen/structure/<id>.json` | Lithostitched site checks around a vanilla jigsaw start |
| `worldgen/structure_set/<id>.json` | Independent seed-based distribution |
| `tags/worldgen/biome/has_structure/<id>.json` | Allowed start biomes |
| `tags/worldgen/structure/relics.json` | Shared structure tag for searches and datapack extensions |

Jigsaw `size: 1` places the start element. Templates have no jigsaw blocks, so no
additional pieces attach. Head, torso, and arm cannot disappear because of failed
connections. The engine stores one `PoolElementStructurePiece` with the full
bounding box and processes the template in each generation chunk. Optional
32-block tile exports are editing/debug assets; natural generation references
only the whole templates.

`StructureTemplate.load`, `JigsawStructure`, and `JigsawPlacement` from the local
Minecraft 26.2 JAR were inspected with `javap`. The NBT loader accepts the three
size values without the structure-block UI limit. Lithostitched substitutes its
`AlternateJigsawGenerator`, which retains a start element even at depth 0;
unmodified vanilla returns early there. The alpha uses depth 1. With no connector
blocks, it still produces a single template. Jigsaw projects height using the
center of the rotated bounding box. Cross-chunk appearance also requires game testing.

## Ground level and rotation

Alpha 2 retains the original dimensions, biomes, distribution, and height offset.
New cracks and armor ruptures are explicitly stored air cells. The Colossus
entrance starts locally at `[40,10,14]` instead of `[40,10,0]`. The former broad
air corridor before the short forecourt is gone; soil supports and irregular
ground surround the paving. This improves the fixed template without adapting
to every individual terrain block.

Minecraft chooses one of four horizontal rotations for the entire structure.
There is no mirroring or independent random selection of body parts.

Local `ground_y` denotes the first air layer above intended ground. Vanilla pool
elements have `groundLevelDelta = 1`, so `start_height.absolute = 1 - ground_y`.

| Relic | `ground_y` | Start height relative to surface | Terrain-check Y correction |
| --- | --- | --- | --- |
| Obelisk | 3 | -2 | +2 |
| Colossus | 10 | -9 | +9 |

The template origin is therefore at `surface_height - ground_y`. The Lithostitched
check point is shifted back to surface height. Template ground-level changes must
update both structure-JSON offsets and the manifest contract.

## Site filters

Filters sample a square grid centered on the rotated structure. Squares cover
both orientations of the rectangular Colossus footprint.

| Rule | Obelisk | Colossus |
| --- | --- | --- |
| Grid radius | 12 blocks | 50 blocks |
| Grid spacing | 6 blocks | 25 blocks |
| Required passing points | All 25 | All 25 |
| Maximum deviation from center surface height | 4 blocks | 8 blocks |
| Ocean-floor heightmap range | 64–230 | 64–230 |
| Ocean/river biome at sample | Disallowed | Disallowed |

Vanilla also requires the full start body to fit with an eight-block margin from
vertical dimension bounds. `terrain_adaptation: none` avoids a rectangular terrain
mound. Irregular bases belong to the templates. Omitted NBT positions preserve
terrain; explicit air clears the interior and entrance. `ignore_waterlogging`
prevents existing fluids being inherited by new waterloggable blocks.

These grids do not guarantee a dry entrance or contact at every edge. Small pools,
narrow ledges, and hills between samples can be missed. Heights come from terrain
generation before later vegetation and other structures. High inland water can
pass the sea-level filter. Collision checks against Dungeons & Taverns and other
structures are not implemented.

## Biomes and terrain mods

Vanilla biome entries are required. Optional Terralith and Biomes O' Plenty entries
use `required: false`, so the mod loads without them. IDs were checked against
Terralith 2.6.4 and Biomes O' Plenty 26.2.0.0.28. Tectonic needs no separate biome
mapping: height filters query the active chunk generator.

Mappings are deliberately explicit. A broad Overworld tag would allow Colossi in
dense forests and Obelisks in unsuitable climates. Datapacks can extend the same
tags. Defaults are not designed for other dimensions or world presets with a
different sea level.

## Frequency and diagnostics

| Relic | `spacing` (chunks) | `separation` (chunks) | Salt |
| --- | --- | --- | --- |
| Obelisk | 64 | 32 | 206091301 |
| Colossus | 80 | 40 | 206091302 |

These distribute candidates, not guaranteed finds. Terrain and biomes reject
candidates. There is no built-in rejection-reason counter. Changes affect future
chunks; existing structures remain. `tools/configure.py` produces overrides for
`rare`, `normal`, or `frequent` profiles and disabled types; see the [README](../README.md).

With cheats or operator permissions:

```mcfunction
/locate structure relics:obelisk
/locate structure relics:colossus
```

Searches can be slow in rare biomes or rough terrain. Targeted template checks in
a separate creative test world bypass site selection:

```mcfunction
/place template relics:obelisk ~ ~ ~
/place template relics:colossus ~ ~ ~
```

The supplied position is the lower template corner; the command ignores
`ground_y`. These are not natural-generation evidence. Visual acceptance includes
four rotations, entrance access, ground contact, chunk boundaries, and reloads.

## Format evidence and validation limits

Minecraft 26.2 `version.json` reports DataVersion 4903, datapack format 107.1, and
Java 25. Lithostitched 1.8.0+beta6 declares `fabricloader >=0.17` and
`minecraft ~26.2`, with Apollib 1.1.4 bundled. Fabric API 0.160.0+26.2 includes
mod-datapack resource loaders. Completed runs are recorded in the
[Alpha 2 report](ALPHA_2_TEST_REPORT.md) and [historical Alpha 1 report](ALPHA_TEST_REPORT.md).

The upstream [structure types](https://github.com/Apollounknowndev/lithostitched/wiki/Structure-Types)
and [placement conditions](https://github.com/Apollounknowndev/lithostitched/wiki/Placement-Conditions)
documentation explains the delegating wrapper and grid filters. Field names were
also checked against codecs in the local JAR. Loading resources successfully does
not by itself establish visual or full-modpack acceptance.

## Integrating the new Blender assets

The new assets have different footprints, burial depths, and total heights. They
also currently retain DataVersion 3105 from the legacy exporter. Before selecting
them in a build, validate their block states in the target game, define interior
air, update the template references and ground offsets, and replace the alpha
footprint/height checks with rules appropriate to the chosen model. Recheck
natural placement rather than reusing the alpha reports as evidence.
