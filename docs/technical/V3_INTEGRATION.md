# V3 visual integration — Alpha 3

Recorded: October 1, 2026. Target: Minecraft 26.2 / Fabric 0.19.5,
Fabric API 0.160.0+26.2, Lithostitched 1.8.0+beta6, Java 25.

## Build selection

`python tools/build.py` now calls `tools/integrate_v3.py`. It selects checked-in
whole V3 templates without changing their bytes:

| Structure ID | Size X/Y/Z | Ground Y | Start-height offset |
| --- | --- | --- | --- |
| `relics:colossus` | 181 / 209 / 227 | 77 | -76 |
| `relics:obelisk` | 25 / 185 / 25 | 8 | -7 |
| `relics:titan_skull` | 121 / 79 / 203 | 8 | -7 |

Each remains a single rigid template, rotated as a unit. The Colossus arm and
the Skull's hill/spine are included. Source paths and SHA-256 checksums are
written to `structures-src/generated/manifest.json`.

Raw `relics:<name>` templates remain unchanged for manual placement. Natural
pools instead select derived `<name>_worldgen` templates with one named jigsaw
anchor at `[size_x // 2, 0, size_z // 2]`. `start_jigsaw_name: relics:center`
centers the whole template around the start chunk. The anchor resolves to the
original block at that cell, or to omitted structure void; it does not add a
visible block, child piece or gameplay mechanic. Keeping it at Y0 also preserves
the height/stub correction above. This is necessary because structure references
only reach eight chunks away from the start: a corner-anchored 227-block model
would be partially missing even when its full bounding box is loaded.

The Skull generates in `top_layer_modification`, after ores and vegetation in
its own chunk. This reduces edits to its exported hill, but features from later
neighboring chunks can still change some stone. The other two relics retain
`surface_structures`. See the [test report](../testing/ALPHA_3_TEST_REPORT.md)
for exact observed edits; strict natural block acceptance remains open.

The source DataVersion **3105 is preserved**. Minecraft loads templates through
its normal data fixer; changing the version number alone is not a migration.
Palette materials are vanilla full blocks. Runtime tests are still necessary.

## Natural placement

Offsets and surface-check corrections use `1 - ground_y` and `ground_y - 1`.
Footprint grids cover either horizontal orientation:

| Relic | Grid radius / spacing | Required samples | Height deviation | Maximum ocean-floor Y |
| --- | --- | --- | --- | --- |
| Colossus | 114 / 57 | 25 | ±16 | 175 |
| Obelisk | 12 / 6 | 25 | ±4 | 130 |
| Titan Skull | 102 / 51 | 25 | ±12 | 230 |

These are conservative initial integration settings, not final balance.
High sites are restricted so models fit below the Overworld ceiling with
dimension padding. Oceans and rivers are rejected at sample points. Finite
grids can still miss local water, slopes, or cliffs. Large footprints may have
few valid sites and slow `/locate` searches.

Candidate distribution stays 64/32 chunks for Obelisks and 80/40 for Colossi.
The new Skull uses provisional 48/24, salt 206091303, to put it ahead of the
other families in candidate frequency. Actual discovery rates depend on site
rejection. Density presets and `--disable titan_skull` are supported.

## Viewing in Minecraft

Use a fresh creative world with cheats, or new unexplored chunks. Old structures
are not replaced; old `/locate` results may still point to Alpha 2 geometry.

```mcfunction
/locate structure relics:colossus
/locate structure relics:obelisk
/locate structure relics:titan_skull
```

For direct comparisons on a flat world whose first air layer is Y64:

```mcfunction
/place template relics:obelisk 0 56 0
/place template relics:colossus 256 -13 0
/place template relics:titan_skull 768 56 0
```

Load the entire footprint first. The supplied position is the lower template
corner; `/place template` does not apply natural site filters or burial offsets.
Do not run placement commands in a valued world.

`python tools/smoke_server.py --accept-eula --showcase` builds an isolated flat
creative comparison world at those coordinates and compares saved blocks with
the launched JAR. Terrain is Y64: 128 layers above minimum Y-64. The normal
smoke run separately checks natural starts and saved blocks.

After both reports pass, `tools/install_test_profile.py` can install the matching
JAR and copy a new showcase save into an existing test profile. It verifies the
artifact hashes, backs up only old Relic JARs, leaves other mods/existing saves
untouched, and enables cheats only in the new showcase copy. Close Minecraft first.

For visual-test installation only, `--allow-feature-overwrites` explicitly allows
documented minor natural edits (under 1% per complete instance) while retaining
the failed strict natural report. Runtime errors or missing/incomplete models
are never accepted by that override. The current Alpha 3 profile installation
uses this limited path; the showcase itself has zero block differences.

## Deliberately unchanged

- Current V3 models are used as-is. Missing NBT cells preserve terrain; there is
  no rectangular air carving or newly authored interior route.
- No machines, magnet, keys, trials, archaeology rewards, maps, or custom mobs.
- No retroactive world updates, custom Java code, or extra player dependencies.
- Server checks do not substitute for client visual inspection, multi-seed
  acceptance, terrain-mod tests, shaders, or performance measurements.

The [Alpha worldgen page](WORLDGEN.md) records the old Alpha 2 contracts;
this page supersedes its sizes, burial offsets and site filters for Alpha 3.
