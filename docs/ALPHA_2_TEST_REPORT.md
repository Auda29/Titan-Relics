# Alpha 2: weathering and terrain transitions

Recorded: September 13, 2026. English translation: October 1, 2026.
Version: `0.1.0-alpha.2`, Minecraft 26.2, Fabric Loader 0.19.5, Java 25.
This report covers the procedural alpha assets, not the later Blender designs.

## Changes and visual inspection

The user's Alpha 1 Minecraft screenshots confirmed the visible basic shapes.
They also showed large uniform surfaces and a long rectangular Colossus approach.
Alpha 2 therefore changes the generators:

- The Obelisk has connected cuts, broken corners, sand drifts, and small base debris.
- Larger helmet and chest-armor sections are missing from the Colossus, exposing
  recessed basalt supports. The chest ring and detached forearm are damaged.
- Moss and persistent leaves concentrate on one side; the other remains mostly
  dark and exposed.
- Outer paving is only nine blocks long, with irregular, partly mossy edges.
  A continuous three-block-wide route leads from local entrance `[40,10,14]`
  into the machine room. Soil supports and ground shapes surround the paving.

New geometry previews were rendered from actual generated blocks and inspected.
They show shape, damage, and vegetation before terrain placement. They are not
new Minecraft screenshots. Visual Alpha 2 client acceptance remains pending.

## Automated checks

**18 tests** cover export repeatability, tile reconstruction, block states,
walkable access, the bounded forecourt, openings before internal supports,
settings datapacks, and the Anvil world reader. The server selects the JAR matching
current project metadata by default, avoiding accidental tests of an older file
retained in `dist/`.

Runtime checks used fresh local worlds with seed `731204`, previously granted
EULA acceptance, and the existing harness. The base run loaded Fabric API and
Lithostitched. Integration added Tectonic, Terralith, Biomes O' Plenty, Dungeons &
Taverns, and required dependencies at the recorded versions. The settings run
tested more frequent Obelisks and a disabled Colossus.

Every run compares saved natural-start world blocks with the exact launched JAR.
Dirt, grass blocks, and azalea leaves remain explicitly excluded from strict
comparison; fixed materials and stored air are compared. A preliminary run found
grass on moss within the cleared entrance width. The boundary between exterior
moss decoration and interior paving was corrected; the air comparison was not relaxed.

Artifact hashes, run IDs, results, and cell counts are in
[testing/alpha2-evidence.json](testing/alpha2-evidence.json).
The [Alpha 1 report](ALPHA_TEST_REPORT.md) remains historical evidence.

All **18 tests and three final server runs passed**. Every server exited with code
0. Base and integration each confirmed **4,737 Obelisk cells** and **82,672 Colossus
cells**, with no mismatches or missing chunks. The settings run produced the full
Obelisk and no result for the disabled Colossus. Its generic `world_blocks.passed`
sub-result is false because that checker expects both types; the harness's overall
result accounts for the intentional deactivation.

The tested and installed JAR has SHA-256:

```text
cc978cdb382ec5f7ad82cfcaddb1dbdc30d27fd3e3e56949729911e347c27dfa
```

A full repeat build produced the same hash. Test counts above describe the
recorded Alpha 2 run, not a claim about the current repository's expanded suite.

## Updating and remaining limits

Structure IDs, dimensions, and site rules are unchanged. Updating does not alter
saved structures. Fully restart Minecraft after replacing the JAR, then use a
fresh test world or ungenerated regions. `/locate` can still return an old site.

Ground geometry remains a fixed template. Soil supports and shorter edges improve
transitions but cannot accommodate every slope, stream, or third-party building.
Further seeds, human visual review, shader/LOD checks, and reliable performance
measurements remain part of acceptance.

The known Windows Perflib diagnostic remains separately identified in logs; it
was not suppressed through operating-system changes. Build, tests, and repeat-build
comparison are also covered by Linux GitHub Actions. CI does not upload additional
Actions artifacts; downloads use GitHub Releases.

The October 2026 Colossus v2/v3 and Obelisk v2 exports were verified separately at
the asset level. They have not undergone these server/worldgen checks and are not
part of the recorded Alpha 2 JAR.
