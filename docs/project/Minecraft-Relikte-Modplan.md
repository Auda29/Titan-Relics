# Minecraft relics: concept and development plan

Original concept: September 12, 2026. Updated: October 2, 2026.

Goal: a structure expansion for a modpack using Terralith, Tectonic, Biomes O'
Plenty, and Dungeons & Taverns. **Alpha 3 selects Colossus, Obelisk, and Titan Skull
V3 for Minecraft 26.2 / Fabric; accepted V4 studies await integration.**
This page preserves the creative catalog and long-term goals. See the
[README](../../README.md) for current implementation and the
[technical plan](UMSETZUNGSPLAN.md) for remaining acceptance work.

**New asset review:** [four V1s](NEW_RELICS_V1.md) are now modeled and exported:
Ruined Tower (111 × 192 × 93), World Tree (193 × 216 × 169), the archive-derived
Small Colossus (101 × 76 × 87), and sword-bearing Titan Skull 2 (105 × 144 × 107).
They await visual acceptance and game integration. Proposed dimensions below
remain the pre-modeling baseline.

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
- Current asset work: [Colossus v2](../../relics/colossus/docs/COLOSSUS_V2.md) follows the visible form;
  [v3](../../relics/colossus/docs/COLOSSUS_V3.md) extends it underground to a torn hip and is selected
  in Alpha 3. V4.1 is visually accepted offline; integration remains pending.
- Occurrence: **one large Colossus per game world**. Smaller Colossi may occur
  multiple times; frequency and loot remain separate decisions. Their current
  [Vigilant-Class reference brief](../../relics/colossus/docs/SMALL_COLOSSUS_V4_REFERENCE.md)
  replaces the archived first-concept direction.
  Large-site uniqueness is not yet implemented.

**October 4 small-Colossus reference update:** after finding V2 too similar to the
large machine and V3 too skeletal, the user selected
[Vigilant-Class Archaean Colossi — The Archive In Between](https://www.instagram.com/reel/Da-s0zqi7OQ/)
as the new primary visual reference for the smaller design. The archive-derived
and slender-sentinel briefs are historical approaches, not the next model's target.

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
- Current asset work: [Obelisk v3](../../relics/obelisk/docs/OBELISK_V3.md), a tapered square antiprism,
  25 × 185 × 25 blocks, with a solid core and only eight blocks below ground.
  It replaces the rectangular design of [v2](../../relics/obelisk/docs/OBELISK_V2.md) as the current
  design study and is selected in Alpha 3; accepted V4.2 integration remains pending.

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

The [pre-modeling brief](../../relics/ruined-tower/docs/REFERENCE_DESIGN_STUDY.md)
now proposes a 112 × 192 × 96 site with a 180-block visible main tower. The top
is cropped in the reference and will be authored; the departing aircraft is excluded.

### 4. Giant skull among green hills

**Reference:** [D.E.A.D. / remains of dead gods — The Archive In Between](https://www.instagram.com/reel/DXM3J4sgqJl/),
especially the opening 0–5 seconds.

**Visible:** A gigantic crowned skull emerges from misty green terrain, nearly
the scale of a landscape feature. A walking person is tiny by comparison.

**Minecraft interpretation:** A weathered titan skull with its lower part buried.
Eye sockets and mouth become explorable spaces. In the selected working lore,
these are remains of Titans a Colossus was sent to kill; the wider history remains
open in the [lore bible](LORE-BIBLE.md).

- Environment: broad valleys and open grasslands.
- Variants: broken teeth/crown projections, erosion, and vegetation.
- Discovery: a seemingly geological shape becomes recognizable as a face.
- Gameplay direction: ordinary mobs inhabit the decaying remains; no exclusive
  item or custom boss is required. See [gameplay decisions](../../relics/titan-skull/gameplay/README.md).
- Technical focus: organic block forms and a readable silhouette despite erosion.
- Current asset study: [Titan Skull v3](../../relics/titan-skull/docs/TITAN_SKULL_V3.md), a roughly
  76-block skull with an organic crown and open jaw, sized as a plausible opponent
  for the Colossus. The full 121 × 79 × 203 export includes a broken, partly buried
  nine-vertebra spine and a solid local hill.
  V3 natural placement is selected in Alpha 3; authored encounters and rewards
  remain planning. Accepted V4 ground variants await integration.

#### Second independent Titan Skull

**Selected reference:** [The Archive In Between — reel Db9KCtWi0eG](https://www.instagram.com/reel/Db9KCtWi0eG/),
specifically the skull in the opening few seconds selected by the user.

This is a separate second design, not another version or terrain palette of the
existing crowned skull. It is recorded in the
[concept page](../../relics/titan-skull/docs/TITAN_SKULL_2_CONCEPT.md). Opening
frames are now verified: a moss-covered skull with a huge diagonal embedded sword
in a cavern/grotto. The working brief proposes a 104 × 144 × 116 site, with
64 visible blocks of skull plus about 68 of weapon rise. Modeling remains deferred.

Both skull designs and future bone sites share the Titan-remains family budget.
Their variety should communicate multiple fallen Titans, not require living
Titans, additional custom bosses, or a special reward for every specimen.

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

The [pre-modeling brief](../../relics/world-tree/docs/REFERENCE_DESIGN_STUDY.md)
now proposes a 192 × 216 × 176 envelope, with a 208-block visible tree, layered
crown and broad root arches. The reference is a montage, not one measured tree.

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

### Working history and discovery frequency

The agreed lore direction is that a Colossus was sent to the planet to kill the
Titans. Skull and bone relics are their remains. Obelisks served as wayfinders or
marked places where Titans had already been destroyed; the precise interpretation
and builders are not settled.

The intended order is **skull/bone variants most common, Obelisks clearly rarer,
and one unique large Colossus per game world**. Smaller Colossi may occur multiple
times; their rarity and loot are undecided. Skull/bone variants share a family-level
frequency budget. This is a design target, not an implemented uniqueness or
numeric worldgen change; future variants do not exist merely because they are
included in this plan. Obelisk maps initially point to the same large landmark;
its per-player core vault supports multiplayer, while magnet and archaeology
sharing remain open.

The [lore/gameplay review](LORE_GAMEPLAY_REVIEW.md) records six follow-up tasks:
material economy, the golem trial's historical function, visible conflict traces,
lasting core utility, multiplayer reward distribution, and actual discovery effort.
Suggested solutions remain proposals; they do not authorize model changes or
gameplay implementation.

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
dependencies in [Target environment](../technical/TARGET_ENVIRONMENT.md). Earlier 1.21.1
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
every slope. The implemented alpha sequence is described in [Worldgen](../technical/WORLDGEN.md).

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
