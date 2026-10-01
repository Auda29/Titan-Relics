# Minecraft relics: concept and development plan

Original concept: September 12, 2026. Updated and translated: October 1, 2026.

Goal: a structure expansion for a modpack using Terralith, Tectonic, Biomes O'
Plenty, and Dungeons & Taverns. **The project now has a playable Alpha 2 for
Minecraft 26.2 / Fabric and a separate reference-based Blender asset pipeline.**
This page preserves the creative catalog and long-term goals. See the
[README](README.md) for current implementation and the
[technical plan](UMSETZUNGSPLAN.md) for remaining acceptance work.

## 1. Five motifs from the Instagram references

Observed imagery and proposed Minecraft interpretations are described separately.
Reference titles identify the inspiration; our structures use their own designs.

### 1. Overgrown Colossus in rolling hills

**Reference:** [Archaean Colossi — The Archive In Between](https://www.instagram.com/reel/DaoBxUEiBNa/),
especially the opening 0–5 seconds.

**Visible:** An enormous damaged machine body rises between green hills. A
detached arm lies in the foreground. Soil and vegetation cover armor. A foreground
person contributes to the sense of scale, but cannot directly establish the
distant machine's absolute dimensions.

**Minecraft interpretation:** A static block-built mech with a partly buried
lower body, damaged armor, and detached arm. A torso opening should allow interior exploration.

- Environment: broad grasslands, gentle hills, suitable plateaus.
- Variants: controlled burial, missing armor plates, different vegetation.
- Discovery: notice a strange distant silhouette, then realize its size while approaching.
- Technical focus: large footprint and convincing body-to-terrain transitions.
- Priority: first demanding prototype.
- Current asset work: [Colossus v2](docs/COLOSSUS_V2.md) follows the visible form;
  [v3](docs/COLOSSUS_V3.md) extends it underground to a torn hip. Neither replaces
  the alpha's smaller model yet.

### 2. A solitary Obelisk in a vast desert

**Reference:** [Painted Desert — Josh White](https://www.instagram.com/p/Da0NEq7kUAO/).

**Visible:** A very slender geometric stele above open, color-layered desert
terrain. A flat crown and clear vertical form dominate the largely empty setting.

**Minecraft interpretation:** A monumental narrow-footprint Obelisk with a few
large surface forms and a partly buried base. Restrained weathering preserves
the silhouette.

- Environment: extensive deserts, dry plains, suitable badlands.
- Variants: surface palettes, small edge damage, controlled burial.
- Discovery: a single unexplained object dominates the horizon.
- Technical focus: distant readability, open surroundings, spacing from other major relics.
- Priority: first simple prototype.
- Current asset work: [Obelisk v3](docs/OBELISK_V3.md), a tapered square antiprism,
  25 × 185 × 25 blocks, with a solid core and only eight blocks below ground.
  It replaces the rectangular design of [v2](docs/OBELISK_V2.md) as the current
  design study. Build/worldgen integration remains pending.

### 3. Monumental sci-fi ruined tower above a pale plain

**Reference:** [Sci-fi animation — Josh White](https://www.instagram.com/reel/DbqXYoVx2hR/),
particularly the background tower architecture.

**Visible:** A huge dark angular tower with openings and damaged sections over
a bright open area. More architecture appears in haze; an aircraft moves through
the scene.

**Minecraft interpretation:** A ruined tower complex with large breaches,
broken floors, and a few lower building sections. Pale surroundings and dark
architecture jointly create the composition.

- Environment: pale dry plains, suitable desert edges, open basins.
- Variants: controlled height, damaged side sections, buried lower floors.
- Discovery: a person feels tiny beside architecture of uncertain purpose.
- Technical focus: modular parts, safe transitions, readable large forms.
- Priority: expansion after the first prototypes; not implemented.

### 4. Giant skull among green hills

**Reference:** [D.E.A.D. / remains of dead gods — The Archive In Between](https://www.instagram.com/reel/DXM3J4sgqJl/),
especially the opening 0–5 seconds.

**Visible:** A gigantic crowned skull emerges from misty green terrain, nearly
the scale of a landscape feature. A walking person is tiny by comparison.

**Minecraft interpretation:** A weathered titan skull with its lower part buried.
Eye sockets and mouth become explorable spaces. It may be a petrified body or an
ancient monument; that question can remain open.

- Environment: broad valleys and open grasslands.
- Variants: broken teeth/crown projections, erosion, and vegetation.
- Discovery: a seemingly geological shape becomes recognizable as a face.
- Technical focus: organic block forms and a readable silhouette despite erosion.
- Current asset study: [Titan Skull v1](docs/TITAN_SKULL_V1.md), 185 × 203 × 103
  blocks, with an organic crown and open jaw. Exported and previewed separately;
  natural placement and gameplay integration remain future work.

### 5. World tree on an open coast

**Reference:** [World Tree Cypress / Gaia's Nursery — The Archive In Between](https://www.instagram.com/reel/DaBgsX0C9s4/).

**Visible:** A single enormous tree shapes a green coast. Other scenes show
massive roots, winding passages, waterways, and worked stone near the roots.

**Minecraft interpretation:** A very rare giant tree with a broad irregular
trunk, major root arches, and an accessible base, standing as a monument within
the existing landscape.

- Environment: suitable green coasts and broad open river valleys.
- Variants: crown shape, broken branches, overgrown root passages.
- Discovery: a living natural monument feels as ancient and overwhelming as machine ruins.
- Technical focus: block count, crown silhouette, world height, and leaf behavior.
- Priority: later separate prototype with high design/integration cost; not implemented.

**Initial scope remains Obelisk and Colossus.** This catalog is not a promise to
deliver all five motifs in version 0.1.

## 2. Intent and visual language

Rare monumental discoveries should suggest an incomprehensibly large past.
Existing worldgen mods provide large-scale landforms and biomes. Relics should:

- Have clear, interesting silhouettes from a distance.
- Sit credibly within soil, water, and vegetation.
- Reveal closer detail and selected accessible spaces.
- Suggest a related world through limited recurring materials and forms.
- Leave wide ordinary landscapes between major discoveries.

References guide atmosphere, composition, and proportions. Fog, lighting, and
extreme sightlines are not automatic effects of a Minecraft structure. Block
design must remain convincing without special shaders.

## 3. Initial scope

Included: static vanilla-block relics, deliberately designed base forms and
controlled variants, biome/height/terrain/frequency rules, local debris or detached
parts, modpack integration, and configurable types/density.

Possible later additions: more catalog motifs, optional Biomes O' Plenty material
variants, subtle sounds, rare lights, small narrative finds, and specialized
generation techniques for very large structures.

Moving or controllable mechs, combat systems, custom dimensions, and wholesale
terrain regeneration are outside the first implementation.

## 4. Technical direction

The project is an installable, data-driven Fabric structure mod. Lithostitched
provides additional placement conditions and structure functionality. Custom code
should be added only when a demonstrated need cannot be handled adequately by
existing features.

| Layer | Responsibility |
| --- | --- |
| Existing worldgen mods | Terrain and biomes |
| Structure templates | Shapes, palettes, interiors, and components |
| Structure/variant rules | Assembly, orientation, damage, and distribution |
| Lithostitched | Additional placement conditions and structure support |
| Custom code if needed | Specific missing capabilities |

References: [Lithostitched project](https://modrinth.com/mod/lithostitched),
[Placement Conditions](https://github.com/Apollounknowndev/lithostitched/wiki/Placement-Conditions),
[Structure Types](https://github.com/Apollounknowndev/lithostitched/wiki/Structure-Types).
Biome, height, and repeated-grid checks provide a foundation, not automatic proof
that every large footprint is suitable. Packaging as a mod alone does not expand
generation limits. A future datapack edition would still require Lithostitched
where its features are used.

The target is now confirmed as Minecraft 26.2 / Fabric 0.19.5, with exact
dependencies in [Target environment](docs/TARGET_ENVIRONMENT.md). Earlier 1.21.1
assumptions are obsolete. Initial palettes use vanilla blocks to avoid extra
material dependencies. Compatibility requires explicit tests.

## 5. Generation principles

### Site selection

1. Define appropriate biomes/tags per type.
2. Select a candidate under configured frequency rules.
3. Check relevant heights, relief, and unsuitable areas such as water.
4. Choose/check a compatible prepared variant and orientation.
5. Place through normal world generation.
6. Add associated local detail reproducibly.

Reject unsuitable sites. Do not arbitrarily deform a recognizable pose to fit
every slope. The implemented alpha sequence is described in [Worldgen](docs/WORLDGEN.md).

### Variation

Use designed alternatives: damaged components, present/absent optional parts,
prepared poses, environment-appropriate surfaces and plants, and bounded burial.
Free random recombination is not the objective. Every allowed variant must stay
coherent and recognizable. The alpha currently has one prepared form per type.

### Size and embedding

Use a few fixed sizes and validate silhouette, structure limits, and generation
cost. The latest Blender dimensions are measured export bounds, but their worldgen
suitability is still unproven. Site checks and terrain modification are separate:
a valid site does not automatically create a convincing transition. Design burial,
exposed parts, and local companion features explicitly.

Assembly must remain reproducible across chunks. Do not assume larger height or
size settings alone solve placement problems.

## 6. Modpack integration

| Component | Review focus |
| --- | --- |
| Terralith | Suitable biomes, surface materials, transitions |
| Tectonic | Relief, broad valleys, slopes, available build height |
| Biomes O' Plenty | Biome mapping, vegetation, possible material variants |
| Dungeons & Taverns | Overall discovery density and unwanted overlaps |
| Graphics / distance mods | Silhouette readability at actual viewing distances |

Investigate overlaps explicitly and implement distance/exclusion rules supported
by the chosen technology. Global collision freedom is not assumed. Shaders and
long sightlines may strengthen good geometry, not replace it.

## 7. Development phases

| Phase | Deliverable / completion criterion |
| --- | --- |
| 0 — Environment | Reproducible target, exact dependencies, separate test world |
| 1 — Design | Recognizable Obelisk/Colossus silhouettes, limited palettes, established dimensions |
| 2 — Technical prototype | Natural Obelisk and complete cross-chunk Colossus placement |
| 3 — Embedding and variants | Site checks, burial, vegetation, convincing placement in different suitable terrain |
| 4 — Integration | Full-pack generation, tuned frequency, performance/errors checked; playable version 0.1 |
| 5 — More motifs | Ruined tower and titan skull integrated and accepted |
| 6 — World tree | Dedicated tree/root/leaf/generation prototype, added if cost and effect justify it |

The alpha has completed initial implementation and selected server checks.
Reference-based asset design has progressed separately. Remaining work centers on
their integration and broader acceptance, not restarting environment discovery.

**First full milestone:** a new world in the intended pack naturally produces
both a readable desert Obelisk and a convincingly embedded Colossus without manual repair.

## 8. Version 0.1 acceptance

### Design

- Both relics read at close, medium, and normal configured viewing distances.
- Major relics do not unintentionally form a dense collection in one view.
- Terrain transitions and exposed parts look intentional.
- Intended interiors are actually accessible.

### Generation and compatibility

- Use at least three fixed seeds and several natural examples of each type.
- Test plains, slopes, water margins, and biome boundaries.
- Cover chunk boundaries and different exploration directions.
- Save, reload, and continue generating adjacent chunks.
- Inspect overlap with Dungeons & Taverns and other installed structures.
- Use new chunks; retroactive insertion is a separate feature.

### Performance

Compare equivalent fresh full-pack worlds with and without Relic Mod. Record
chunk-generation time, stalls, memory, and errors. Set budgets from the baseline
before acceptance. Static structures need no movement or AI simulation, but
generation and rendering many blocks still have costs.

## 9. Decisions still open

- Which new designs should replace the alpha assets, and at what final game scale.
- Terrain tolerances, density, and spacing after exploration tests.
- Additional variants and any required custom placement/diagnostic code.
- Full-release licensing and publication details.

Target versions and the basic pipeline are now established. Design choices and
test evidence should resolve the remaining questions.

## 10. Additional references

These remain supplementary inspiration, not automatic additions to the first catalog:

- [Warden-Class Archaean Colossi](https://www.instagram.com/reel/DcwuU3SB5gc/) — additional bodies, weathering, and architecture.
- [Fragment of the Fallen](https://www.instagram.com/reel/DbD0PB7iD2Q/) — later construction on Colossus remains.
- [The Ancient One](https://www.instagram.com/p/DcoGiYTkWjH/) — a glowing relic in a dark ravine.
- [Pilgrimage to the Finger of God](https://www.instagram.com/p/Db8UdK1kXdJ/) — extreme proportions, open landscape, and enigmatic geometry.

The original review sampled the six reels across their duration and used available
process animations for the three image posts; it did not assume complete carousel
coverage. The later Obelisk study additionally inspected both published *Painted
Desert* paintings and its process animation. The lore bible records the scope of
its separate visual review.
