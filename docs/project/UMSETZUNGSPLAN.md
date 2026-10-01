# Relic Mod: technical implementation plan

Updated: October 1, 2026.

This is the implementation and acceptance plan for version 0.1. **The current
playable build is 0.1.0-alpha.2 for Minecraft 26.2 / Fabric 0.19.5.** It provides
two procedural relics, weathering, and terrain transitions. New reference-based
Blender assets have been exported and verified but are not integrated into the
build or worldgen. Completing individual checks does not satisfy every acceptance
criterion below.

The [README](../../README.md) describes current use; the [Alpha 2 report](../testing/ALPHA_2_TEST_REPORT.md)
records actual game-server checks. The [lore bible](LORE-BIBLE.md) defines the
design goals, and the [concept plan](Minecraft-Relikte-Modplan.md) preserves the
reference catalog. Proposed tests and future decisions are identified as such.

## 1. Goal and scope

Version 0.1 adds two rare natural Overworld structures: a desert Obelisk and an
overgrown Colossus. Both initially use vanilla blocks. The Colossus should have
an accessible interior and a related detached component.

The intended environment includes Terralith, Tectonic, Biomes O' Plenty, and
Dungeons & Taverns. Those mods provide large-scale terrain and biomes; this
project handles templates, site selection, local embedding, and frequency.

| Scope | Content |
| --- | --- |
| Version 0.1 | Obelisk and Colossus; one finished base form each; natural generation; terrain checks; reproducible orientation; configurable types and density |
| After a validated base form | A second controlled variant per type if it can receive equivalent testing |
| Later expansion | Ruined tower and titan skull, then a separate world-tree prototype |
| Optional later ideas | Independently placed machine fragments, an enclosed Ancient One, a split monument |
| Outside 0.1 | Moving mechs, bosses, dimensions, new materials, quests, custom sounds, retroactive generation in existing chunks |

An arm belonging to a Colossus is part of that structure. An independently
generated arm with its own site selection would be a separate relic type.

## 2. Confirmed environment and remaining inventory

The target is now recorded in [Target environment](../technical/TARGET_ENVIRONMENT.md):
Minecraft **26.2**, Fabric Loader **0.19.5**, Java **25**, Fabric API
**0.160.0+26.2**, and Lithostitched **1.8.0+beta6**. Earlier Minecraft 1.21.1
assumptions are superseded. One version/loader combination is supported initially.

| Evidence | Status |
| --- | --- |
| Target profile and game/loader versions | Recorded from the selected profile |
| Dependency versions and hashes | Recorded; base and selected integration server runs passed |
| Worldgen format | Checked against target JARs; NBT DataVersion 4903, datapack format 107.1 |
| Reproducible build | Python data-only packaging implemented; repeat builds checked |
| Full personal modpack and custom configs | Not fully accepted; integration tests used a selected default-config subset |
| World preset, extra datapacks, graphics, shaders/LOD | Must be recorded for broader acceptance |
| Test hardware, JVM memory, storage, performance baseline | Must be fixed before comparative measurements |

Do not commit credentials, account data, personal saves, or third-party mod JARs.
Additional loaders and game versions should follow a working first release.

## 3. Architecture

| Layer | Current responsibility |
| --- | --- |
| Mod packaging | Fabric metadata, dependencies, and resources; no custom Java classes |
| Structure sources | Procedural alpha geometry and separate Blender source generators |
| Worldgen data | Biomes, rigid template pools, distribution, and placement conditions |
| Lithostitched | Delegating structure type, grid/height/biome conditions, and jigsaw placement |
| Development tools | Conversion, manifests, export checks, previews, settings packs, and server/world verification |
| Custom runtime code | Add only for a demonstrated gap that cannot reasonably be covered by existing facilities |

The alpha uses one whole rigid template per relic. No required part depends on a
random jigsaw connection. See [Worldgen](../technical/WORLDGEN.md) for actual codecs,
offsets, and grid values. Upstream documentation provides context:
[Placement Conditions](https://github.com/Apollounknowndev/lithostitched/wiki/Placement-Conditions)
and [Structure Types](https://github.com/Apollounknowndev/lithostitched/wiki/Structure-Types).
The original documentation review was September 13, 2026; the installed version's
codecs remain authoritative.

### Technical prototype gates

The initial prototype asks whether resources load and package correctly, the
Obelisk generates naturally, the Colossus remains complete across chunks, and
invalid sites can be rejected without generation loops or long stalls. Alpha
server evidence addresses these for one seed and selected configurations. It
does not prove the substantially larger Blender assets work under the same rules.

If a requirement cannot be met, record the failed attempt, smallest necessary
code change, and test cost before expanding the architecture. A successful
Obelisk does not substitute for testing the Colossus.

### Client and server

Generation must work on both integrated and dedicated servers. Determine minimal
client dependencies through a connection test. Using vanilla blocks alone does
not prove that every required mod can be installed server-side only.

## 4. Maintainable structure sources

### Repository layout

| Area | Role |
| --- | --- |
| `docs/project/` | Shared concept, lore, and implementation plan |
| `docs/technical/` | Environment records, Blender workflow, and worldgen |
| `docs/testing/` | Test reports and evidence |
| `relics/<relic>/docs/` | Relic-specific design history and asset pages |
| `relics/<relic>/design/` | Asset configs and versioned Blender/export/preview outputs; selected deliverables are tracked |
| `relics/<relic>/gameplay/` | Loot, items, encounters, and gameplay decisions |
| `structures-src/` | Structure source area; ignored generated alpha manifests |
| `src/main/resources/` | Packaged Fabric metadata and worldgen resources; generated NBT is ignored |
| `tools/` | Generators, converters, renderers, validators, build and server tools |
| `tests/` | Automated tests and synthetic fixtures |
| `.work/` | Ignored upstream checkout, local reference media, and experiments |
| `build/`, `dist/` | Ignored runtime/build evidence and packaged output |

These areas already exist. A custom `src/main/java/` tree is not needed for the
current data-only implementation. Local worlds and runtime data remain outside
tracked sources. Reference media is not shipped with the mod.

### Build and export workflow

The alpha build uses `tools/relic_assets.py`. New designs use **Blender → triangulated
OBJ → local ObjToSchematic 1.0 → Sponge `.schem` → Java `.nbt`**, with optional
rigid tiles and manifests. VoxelVision is not required. See
[Blender workflow](../technical/BLENDER_WORKFLOW.md) for the implemented pipeline.

Both pipelines are reproducible from tracked generators/configs. Generated files
are not authoritative hand-edited sources: copy a model to a maintained source
location before manual edits, and incorporate intended changes into its generation
or export process. Repeated exports should preserve geometry; variable metadata
must be identified and normalized where applicable.

An optional creative-world workflow remains available:

1. Use a separate build world for the target version and record the export tool/version.
2. Establish the silhouette and compare it with a player-sized marker.
3. Mark origin, facing, ground plane, entrances, and associated parts.
4. Reimport into a clean world and compare states, dimensions, and air handling.
5. Split only where export/placement requires it; inspect seams with a simple palette.
6. Record source revision, export tool, and file hashes for packaged resources.

### Per-structure metadata

The namespace is **`relics`**, with stable IDs `relics:obelisk` and
`relics:colossus`. Each maintained design should record:

- Relic and variant ID, source revision, and export version.
- Dimensions, origin, nominal ground level, and permitted palette.
- Required/optional parts and their connections, transforms, and rotations.
- Ground-contact surfaces and the full footprint, including arm and debris.
- Entrances, sight openings, and interior volumes that must remain clear.

### Air, terrain, and sensitive blocks

Distinguish positions that preserve terrain from explicit clearing volumes. A
rectangular export must not accidentally carve a rectangular cave into a hill.
The schematic converter requires `--air omit` or `--air keep`: neither option
automatically defines a playable interior. Colossus exports currently omit air.
Obelisk v2/v3 explicitly fill sealed interiors with sandstone before conversion.

Check water, falling blocks, persistent leaves, vines, waterlogging, and copper
aging after placement and reload. Use ticking blocks and block entities only
where they serve a visible purpose. Worlds alone are not source backups.

## 5. Current designs and acceptance contracts

Dimensions below are X/Y/Z in blocks, including the full export bounds.

| Design | Dimensions | Current status |
| --- | --- | --- |
| Alpha Obelisk | 25 × 70 × 25 | Packaged and server-tested with natural placement |
| Alpha Colossus | 100 × 66 × 76 | Packaged and server-tested, including arm and interior |
| Colossus v2 | 181 × 160 × 227 | Reference-based Blender/NBT asset; 182,734 blocks |
| Colossus v3 | 181 × 209 × 227 | Adds buried abdomen/torn hip; 221,221 blocks; nominal surface Y ≈ 77 |
| Obelisk v2 | 23 × 209 × 19 | Flat crown and solid core; 90,497 blocks; 32-block buried foot |
| Obelisk v3 | 25 × 185 × 25 | Tapered square antiprism; 93,153 blocks; 8-block buried foot |
| Titan Skull v1 | 185 × 203 × 103 | Crowned fossil asset study; 103,943 blocks; hollow cranium/open jaw; integration pending |
| Titan Skull v2 | 117 × 80 × 105 | Skull at Colossus-head scale plus exported solid mound; 149,894 blocks; integration pending |
| Titan Skull v3 | 121 × 79 × 203 | Broken, partly buried spine and extended hill; 264,355 blocks; integration pending |

The first Blender experiment remains separately reproducible at 99 × 66 × 71.
The asset version names do not change the playable mod version.

The current design pair is Colossus v3 and Obelisk v3. At their nominal surface
levels, they expose approximately 132 and 177 block layers respectively. The
Obelisk's extra 45 visible blocks are a deliberate scale choice; the references
provide no shared absolute scale. Obelisk v3 received visual approval from its
previews, while in-game acceptance remains pending.

The Obelisk must preserve a slender flat-topped silhouette, credible ground
contact, and open views of a major face. The Colossus must retain a readable head
and torso, a buried lower body, a detached arm, and an accessible main room.
The reference-based exports have not yet demonstrated the last requirement in terrain.

Review all forms from several distances in a flat test world and in target
terrain. Adjust pose, scale, or assembly when those fail before multiplying
variants. Required parts must never disappear through random selection. A new
pose is a separate design with its own acceptance work.

## 6. Site selection and generation

### Reproducible sequence

The intended model is:

1. Derive a candidate from the world seed and distribution rules.
2. Select a prepared type/variant/orientation reproducibly.
3. Derive its complete footprint and critical contact points.
4. Check biomes, terrain heights, water, vertical clearance, and relevant distances.
5. Reject any failed mandatory condition.
6. Place all required parts and their defined local embedding together.
7. Add optional details from the same reproducible random basis.

The actual engine sequence must match target-version APIs. Checks must cover
the chosen rotated form; a checked narrow footprint cannot later become a wider
unchecked pose. Initially allow only four horizontal quarter-turns. Mirroring
needs separate tests. Do not use wall-clock time or global exploration-order-dependent randomness.

### Terrain requirements

| Condition | Obelisk | Colossus |
| --- | --- | --- |
| Environment | Open dry desert or suitable badlands | Open grassland and broad moderately rolling hills |
| Ground contact | Partly buried foundation; no floating base | Torso and arm contact evaluated separately |
| Height variation | Limited local intervention around a narrow base | Entire pose must suit the large footprint |
| Water | No unintended flooded base | No flooded entrance or required parts accidentally in a river |
| Vertical bounds | Crown below the dimension limit with margin | Highest part and deepest burial both fit |
| Access | Exterior exploration remains reachable | At least one intended entrance remains clear |

Biome tags, height queries, and actual surface conditions are different checks.
A biome alone proves neither dryness nor an open view. Supplement grids with
entrance, edge, and arm-contact samples where possible. Coarse sampling cannot
guarantee detection of small streams or ledges.

Queries must not trigger uncontrolled neighbor generation or cyclic dependencies.
If a needed condition is unavailable at the placement stage, explicitly revise
the requirement or implementation.

### Embedding and overlap

Sand, buried armor, soil, fracture debris, and sheltered vegetation belong to
the design and have bounded extent. Large-scale flattening to fit every pose is
not intended. Spacing between our relics and collisions with other structures
are separate issues: a structure-set exclusion is not precise geometry collision.
Record the chosen approach and remaining limitations.

## 7. Density and configuration

`tools/configure.py` implements datapack overrides for `rare`, `normal`, and
`frequent`, plus individual type deactivation. No runtime menu is implemented.
Current values distribute candidates and still need wider exploration-based tuning.

| Behavior | Rule |
| --- | --- |
| Activation | Load settings at world/server startup; affect future generation |
| Existing relics | Remain after a type is disabled |
| Existing chunks | No retroactive generation |
| Disabled type search | `/locate` cannot find that type while its structure-set entries are removed |
| Invalid input | Reject with a readable error and documented bounds |
| Multiplayer | Server data determines generation |
| Diagnostics | Effective settings/rejection statistics remain a development requirement |

Density studies should count candidates, rejections, and placements, with causes
such as biome, water, slope, build height, and spacing. The current library/tooling
does not provide the desired built-in statistics. Evaluate a development tool or
small diagnostic addition before promising that capability.

## 8. Phases and current progress

| Phase | Deliverable | Current state / completion gate |
| --- | --- | --- |
| P0: Environment | Reproducible target and baseline | Versions recorded; selected test environments start; performance baseline open |
| P1: Project/export | Loadable artifact and complete import/export | Alpha build and schematic converter implemented |
| P2: Obelisk | Several natural sites without manual repair | One-seed server evidence; broader visual acceptance open |
| P3: Colossus placement | Complete body/arm, access, rotations, terrain, chunk boundaries | Alpha server evidence exists; large Blender design integration still open |
| P4: Design | Both motifs satisfy lore/design criteria | Alpha weathering plus reference-based exports complete; in-game review pending |
| P5: Distribution | Tuned profiles and explainable acceptance/rejection rates | Settings packs implemented; density studies/diagnostics pending |
| P6: Integration | Full pack, client/server, reloads, performance | Selected default-config integration passed; full matrix incomplete |
| P7: Release | Tested artifact, installation, license, changelog, checksum | Alpha packaging documented; full 0.1 release gates remain |

Design work may run ahead of integration, but it does not close placement gates.
For new Colossus assets, isolate failure causes before changing pose or scale.

## 9. Version 0.1 test plan

### Resources and build

- Validate JSON and actual resource loading in the target version.
- Catch missing references, wrong namespaces, and unknown block states.
- Check NBT dimensions, required parts, joins, and allowed palettes.
- Build from a clean checkout and inspect the resulting artifact.
- Start a dedicated server and verify client connection with documented dependencies.

Automated tests focus on custom logic and error-prone data relationships. Visual
acceptance happens in Minecraft, not only in Blender.

### Generation and playability

Proposed fixed seeds: `731204`, `-48291736`, and `20260913`. **Only `731204` has
the recorded alpha server evidence.** Define the same bounded exploration area
or route per seed before measuring.

| Case | Procedure | Acceptance |
| --- | --- | --- |
| Natural sites | At least five examples per type in total, across at least three seeds | Required parts, embedding, and access work |
| Too few finds | Complete the agreed area and inspect candidate/rejection rates | Explain cause and adjust rules before renewed acceptance |
| Four rotations | Place the same template in every allowed orientation | Joins, arm, and access remain correct |
| Chunk boundaries | Inspect critical transitions across chunks | No clipped or shifted parts |
| Exploration order | Generate matching seed/area from different directions in fresh worlds | Same decisions/geometry for identical versions/configs |
| Save/reload | Save partially explored regions, reload, and complete them | No gaps, duplicates, or broken references |
| Terrain edges | Cover plains, slopes, water margins, and biome boundaries | Valid sites fit; invalid ones are rejected for understood reasons |
| Other structures | Inspect proximity to Dungeons & Taverns and others | No observed severe overlap; residual limits documented |
| Settings | Disable types and test profiles in fresh regions | Effective settings match generation |
| Exploration | Follow planned routes without flying | Main Colossus room reachable without mining or special equipment |

Manual placement is for targeted boundary tests and must be distinguished from
natural finds. Do not silently enlarge the search area until a low find rate is hidden.

### Appearance and performance

Inspect without shaders and with the actual graphics profile. Initial comparison
distances are 32, 96, and 192 blocks, where render settings permit; these are
camera positions, not guaranteed draw distances.

Use fresh paired worlds per seed: the complete pack without Relic Mod and the
same environment with it. Keep routes, JVM settings, and other configuration
fixed. After warm-up, plan three comparable measurement pairs.

Record total time for the agreed chunk count, per-chunk timing where measurable,
stalls, peak memory, and logs. Compare the same relic camera view for rendering.
Document instruments and attribution limits. Set time/memory budgets after the
baseline and before acceptance. Without those budgets, performance acceptance is
open. Crashes, repeated generation errors, and reproducibly incomplete structures
block release regardless of averages.

## 10. Changes and release

Keep released resource IDs stable. Document distribution, template, or random
selection changes as affecting new chunks. A shared seed does not guarantee the
same world across mod versions.

Relic Mod is the current project name; an open-source license remains undecided
and metadata uses `All-Rights-Reserved`. Keep original sources separate from
third-party reference media. Releases need installation instructions, exact
dependencies, known limits, a changelog, and the tested artifact's checksum.

Verify the Git tag, uploaded artifact, and downloaded checksum at release time.
A successful upload request alone is not proof of public availability.

## 11. Next work and open decisions

1. Confirm Colossus v3 and Obelisk v3 as the build inputs when beginning integration.
2. Validate their palette/states in Minecraft 26.2; address legacy DataVersion
   3105, copper aging, wall thickness, and interior clearing.
3. Add explicit build source selection and matching template references.
4. Recalculate footprint checks, ground offsets, and vertical clearance for the
   selected assets, including the buried hip or foot.
5. Run targeted placement, rotation, reload, and natural-generation checks.
6. Complete multi-seed visual review, density tuning, and performance baselines.
7. Decide additional variants, diagnostic needs, license, and full-release destination.

Environment discovery and basic export are already complete; the next technical
milestone is integration and in-game acceptance of the selected new assets.
