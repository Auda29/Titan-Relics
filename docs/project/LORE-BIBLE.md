# Relic Mod: lore bible and design guide

Original design draft: September 13, 2026. Updated: October 1, 2026.

The five main motifs and version 0.1 scope come from the original concept.
The October gameplay decisions establish a relative discovery hierarchy and a
working history connecting the Colossus, Titan remains, and Obelisks. Detailed
history, working names, exploration routes, and small narrative motifs remain
proposals, not finalized canon. Alpha 2 implements the first two relics;
the newer Colossus v2/v3 and Obelisk v2/v3 are separate reference-based asset designs
awaiting integration.

This guide describes what the relics should communicate during play. Dimensions,
generation, and acceptance procedures are in the [technical plan](UMSETZUNGSPLAN.md).
The [concept plan](Minecraft-Relikte-Modplan.md) contains the reference catalog.

## 1. The feeling of the world

The forest ends on a rise. Between the next hills stands something rounded,
taller than the trees. Only as you approach do a shoulder, helmet, and cracked
chest plate become recognizable. Grass grows on metal. A detached arm lies so
deep in the ground that a stream follows its side. Daylight enters the torso
through a split. At the opening hang the remains of a much smaller wooden stair.

The landscape carries traces of things whose scale and purpose can only partly
be understood. Players may feel wonder, curiosity, and smallness. Enough ordinary
world should remain between discoveries for the next relic to be surprising.

The prevailing mood is quiet wonder with occasional unease. Decay and nature
should coexist. A damaged place can still feel welcoming when sunlight, grass,
and a reachable viewpoint invite exploration.

## 2. What is established and what remains open

### Established concept

- Relics are discoveries in the existing Overworld with deliberately different
  frequencies: Titan remains are the most common family, Obelisks are clearly
  rarer, and Colossi are very rare.
- The first structures are Obelisk and Colossus. Ruined tower, titan skull, and
  world tree may follow later.
- Initial structures use regular Minecraft blocks and original designs.
- Shape, ground contact, and close detail must work without special lighting.
- Selected areas are explorable. There is initially no mandatory story or new combat mechanic.

### Working history: the Titan conflict

The selected lore direction is that **a mechanical Colossus was sent to the
planet to kill the Titans**. Skull and bone relics are their weathered remains.
This supplies a connection between the machine and the organic remnants without
requiring a present-day Titan fight or an activating Colossus.

Obelisks were built as **wayfinding markers or markers of places where Titans
had already been destroyed**. These are still alternative interpretations; their
exact original purpose is not settled. Later excavation sites and expedition
maps can reflect subsequent visitors investigating this history.

Who sent the Colossus, who built the Obelisks, the reason for the mission, and the
fate of the machine remain open. The premise does not establish exactly one
Colossus spawn per world or a single builder for all relic types. Ruined towers
and world trees are not automatically assigned to this conflict.

### Relative discovery hierarchy

| Relic family | Intended relative frequency | Gameplay role |
| --- | --- | --- |
| Titan skulls and future skull/bone variants | Most common of these three families | Decaying remains to explore, with ordinary mobs; no special item required |
| Obelisks | Clearly rarer than Titan remains, but more accessible than Colossi | Archaeology, a collectible, and a map to a Colossus |
| Colossi | Very rare | Valuable technical salvage and the head trial |

Frequency is a **family-level** target: adding more skull or bone variants should
not multiply total encounter density unintentionally. Most common does not mean
that every landscape should be crowded with giant remains.

No numeric rates or worldgen settings are changed by this decision. Future
balancing must account for biome eligibility, terrain rejection, and actual
discovery effort, not only candidate spacing. Skull/bone variants are planned
extensions; this does not claim that additional models or placements exist yet.

Detailed gameplay decisions are maintained with each relic:
[Titan Skull](../../relics/titan-skull/gameplay/README.md),
[Obelisk](../../relics/obelisk/gameplay/README.md), and
[Colossus](../../relics/colossus/gameplay/ITEMS.md).

### Proposed guiding idea

Three layers of time can be read at a site: the original monument, its damage,
and later reuse by much smaller inhabitants. Nature grows through all three.

Tell this through construction. A small stair might rest on an old armor plate;
a low ring of loose stone near the Obelisk might suggest a much younger camp.
Such traces remain limited in version 0.1.

### Deliberately unanswered questions

- Who built and sent the Colossus, and why the Titans were to be killed.
- The Titans' nature and the details of the conflict.
- Whether world trees grew, were planted, or were altered.
- Who built the Obelisks and whether they primarily guided travel or marked
  destroyed Titans.
- Whether the relics fell in one event or over many ages.

There is no official map of an old empire, fixed list of gods, or global disaster
explaining every discovery. A structure may offer clues without resolving these questions.

## 3. Internal design background

These are working concepts, not necessarily in-game names.

| Layer | Building assumption | Visible evidence |
| --- | --- | --- |
| The old grandeur | Some structures served purposes and scales alien to present inhabitants | Huge material fields, unusual openings, components far beyond human scale |
| The fractures | Places suffered different forms of damage, abandonment, or burial | Sheared connections, collapsed rooms, exposed inner layers |
| Later reuse | Visitors used reachable parts as paths, shelter, or landmarks | Small steps, walls, repaired crossings, abandoned work areas |
| The present | Original purpose is uncertain; nature and travelers continue using the site | Grass on metal, roots in masonry, open routes, quiet interiors |

Not every relic needs every layer. A nearly untouched Obelisk needs no ruined
city at its base. A Colossus may be wholly abandoned. The shared experience is
deep time, not necessarily a shared origin.

## 4. Atmosphere and form rules

### 4.1 Large forms first

Each motif has a defining feature: the Obelisk's slender straight line, the
Colossus's posture, the skull's eye sockets, the tower's great openings, and the
tree's layered crown and massive base.

Avoid covering these with evenly distributed small detail. Concentrate breaks
and vegetation in selected areas. Large quiet surfaces make size legible.

### 4.2 Nature belongs somewhere specific

Soil collects on horizontal surfaces and buried parts. Plants grow in seams,
hollows, and damp areas. Major broken edges remain partly exposed. Uniform green
coverage removes the contrast between construction and landscape.

### 4.3 Scale needs comparisons

Normal trees, low walls, human-width entrances, and later stairs reveal size.
Inside, enormous components can sit beside a small path added much later.
Ancient machinery need not be comfortable everywhere, but the intended exploration
route must be reachable without mining. A huge machine chamber may be entered
through a comparatively recent access route.

Reference figures and aircraft do not supply reliable absolute dimensions when
their distance or size is unknown. Current Blender heights are artistic estimates;
two-block figures and same-block-scale previews make our chosen dimensions explicit.

### 4.4 A quiet world with local tension

Most exterior views are calm. Tension comes from entering a darker room, an
ambiguous opening, or imagining how large the complete body once was.
Version 0.1 adds no custom jump scares, bosses, or soundscapes. Sites are not
promised to be mob-free shelters. The mood must work within ordinary gameplay.

### 4.5 Light and color

Daylight, shadows, and surroundings carry the main effect. Custom light accents
would be a later restrained addition; the glowing Ancient One is not a 0.1 requirement.

| Material family | Design role | Initial vanilla palette options |
| --- | --- | --- |
| Dark supporting mass | Torso, tower, exposed technical layers | Deepslate, basalt, dark stone |
| Aged metal skin | Selected armor, rings, joints | Copper aging stages; test persistent states |
| Pale mineral mass | Skull, light erosion, monument faces | Calcite, bone blocks, sandstone, pale stone |
| Later small-scale interventions | Paths, supports, shelters | Wood, cobblestone, sparse ordinary lighting |
| Returning nature | Ground joins, seams, sheltered tops | Dirt, moss, grass, roots, suitable leaves |

This is a palette to try, not a requirement to use every material. Assess large
quantities of economically valuable blocks as part of exploration/resource balance.
The latest Colossus studies emphasize bronze/copper; Obelisk v2/v3 use warm
terracotta and sandstone instead of the alpha's darker treatment.

### 4.6 Related forms without a uniform design

Colossus and tower may share deep seams, recessed rings, and a distinct outer
skin. The Obelisk remains much simpler; skull and tree retain organic forms.
Similar small traces of later visitors may connect sites without implying that
one civilization created machines, bones, and trees alike.

## 5. How a relic is explored

Give each design a short exploration sequence before detailed construction:

1. **Distant view:** an unusual form justifies a detour.
2. **Approach:** terrain and familiar small objects reveal scale.
3. **Threshold:** a rupture, root arch, or base offers access or a viewpoint.
4. **Close discovery:** a detail hints at use or age while leaving the wider story open.
5. **Looking back:** another position makes the structure both clearer and larger.

Not every relic needs an interior or a chest. An Obelisk's close discovery can
sit at its base. Views, spatial discovery, and the structures themselves are the
primary version 0.1 rewards.

## 6. The five main structures

### 6.1 Desert Obelisk

**Working name:** The Silent Stele. **Scope:** version 0.1. **Technical ID:** `relics:obelisk`.

**Mood and silhouette:** A solitary, exceptionally slender form rises above a
broad dry landscape. Its crown is flat, its sides largely uninterrupted, with
few deep seams. Straight geometry contrasts with dunes and eroded slopes.

**Setting:** Open desert, dry plains, or suitable badlands. A partly sand-buried
base ties it to terrain. Comparable monuments should not crowd its distant view.

**Exploration:** The stele appears on the horizon. Its foot emerges between sand
ridges during the approach. An exposed corner shows continuation below ground.
A low, younger stone enclosure on the sheltered side might offer a resting place.
From there the player looks up an almost uninterrupted wall.

**Narrative core:** Generations have used it as a landmark. In the working
history, it was built for wayfinding or to mark the destruction of a Titan; the
choice between these interpretations remains open.

**Planned gameplay:** Archaeology at its foot yields a collectible and a map to
the very rare Colossus. See the [gameplay decisions](../../relics/obelisk/gameplay/README.md).

**Variants:** Burial depth and a bounded edge loss; begin with a mostly intact
form. A hollow tower with regular floors would be a different motif.

**Essential:** Simplicity, slender proportions, open surroundings, convincing base.
An interior is unnecessary.

**Avoid:** Dense runes, enormous glowing tips, identical adjacent steles, and an
automatic dungeon beneath every specimen.

**Earlier design:** [Obelisk v2](../../relics/obelisk/docs/OBELISK_V2.md) translates *Painted Desert*
into a flat-crowned, parallel-sided stele with restrained mineral bands, solid
sandstone core, and a 32-block buried foot. Landscape and rest-stop storytelling
remain separate from the exported stele.

**Current design:** [Obelisk v3](../../relics/obelisk/docs/OBELISK_V3.md) refines this using the supplied antiprism diagrams:
eight long triangular faces, a smaller square crown rotated 45 degrees, and only
eight blocks of burial. Broad quiet facets now carry the shape instead of a
rectangular shaft.

### 6.2 Overgrown Colossus

**Working name:** The Sunken Sentinel. **Scope:** version 0.1.
The name is a visitor's interpretation, not a confirmed historical function.
**Technical ID:** `relics:colossus`.

**Mood and silhouette:** A damaged machine body rests among green hills. Head,
broad shoulders, and chest remain readable. The lower body disappears into soil;
its posture conveys weight and long stillness.

**Setting:** Broad grassland and open hills. Soil covers the lower torso and parts
of a detached arm. Plants occupy shoulder surfaces and armor seams, leaving
substantial metal exposed.

**Exploration:** The head first resembles an unfamiliar hilltop. The nearer arm
makes the body readable. A torn chest plate offers a threshold. A short later
access route leads into a still room between enormous ribs/supports. Light enters
through an upper rupture; another opening looks back toward the arm and landscape.

**Interior:** One main room is enough initially. An inactive ring-shaped mechanism
and exposed conduits can suggest a technical purpose. A small younger resting
place on a sheltered edge may show that someone used the body as lodging.

**Narrative core:** Something overwhelming to humans has itself become ground,
roof, and path. The working history gives it a mission to kill Titans; its sender,
the reasons for that mission, and its own fall remain uncertain.

**Variants:** Begin with one pose and a fixed arm position. Later vary armor
ruptures and controlled vegetation. New poses are separately designed assets.

**Essential:** Readable posture, extensive ground contact, a detached component,
and an accessible main room.

**Avoid:** Randomly assembled limbs, floating parts, uniform greenery, and a fully
equipped cockpit that immediately explains every function. The machine does not
activate in version 0.1.

**Current design:** [Colossus v2](../../relics/colossus/docs/COLOSSUS_V2.md) has the reference's bronze
dome helmet, narrow visor, respirator hoses, and broad armor. [Colossus v3](../../relics/colossus/docs/COLOSSUS_V3.md)
continues below ground through the abdomen to an irregular torn hip, exposed
supports, and conduits, without legs. The surface silhouette is preserved at
almost the same block scale. An accessible in-terrain route for these new assets
still needs to be completed and tested.

### 6.3 Ruined tower

**Working name:** The Open Tower. **Scope:** planned expansion after version 0.1.

**Mood and silhouette:** A dark angular mass with major vertical openings stands
over a pale plain. Missing walls expose deep rooms and isolated surviving connections.

**Setting:** Dry open basins and suitable desert edges. A few independently
designed lower parts may emphasize the main tower's height.

**Exploration:** Sky is visible through the damaged facade. A broad breach leads
into a hall. A bounded walkable route reaches an open intermediate level, making
lower buildings and the approach appear small.

**Narrative core:** Original purpose is lost, but construction phases and repairs
show prolonged reuse.

**Variants:** Missing side sections, buried lower floors, limited height changes.
Do not create dead ends on required routes through free recombination.

**Essential:** Large negative spaces, dark mass against light terrain, and at least
one meaningful reachable viewpoint.

**Avoid:** A uniform skyscraper with copied floors and purely decorative doors.
The aircraft taking off in the reference is not a fixed annex.

### 6.4 Titan skull

**Working name:** The Face in the Valley. **Scope:** planned expansion after version 0.1.

**Current asset study:** [Titan Skull v3](../../relics/titan-skull/docs/TITAN_SKULL_V3.md) retains the fused
organic crown, hollow cranium, triangular nose, open jaw, and lateral spurs of v1,
but reduces the skull to approximately Colossus-head scale. The user's premise is
that the living titan could have fought the Colossus. This guides relative size
and the working Titan-conflict history without adding a fight mechanic. V3 includes
a complete posterior wall and a broken nine-vertebra spine, partly buried in an
extended solid local mound. Two dislocations and loose fragments suggest an
incomplete fallen skeleton. The exploration route below
remains a design goal pending terrain and gameplay integration.

**Mood and silhouette:** An eroded mineral form becomes recognizable as a skull.
Eye sockets, nose, and mouth determine its shape. A few broken projections suggest
a crown without explaining its origin.

**Setting:** Broad green valleys and grasslands. The lower jaw/face partly merges
with terrain. Pale bone or stone alternates with soil and growth.

**Exploration:** At first it resembles unusual geology. A side view reveals the
eye and jaw. The mouth opens into a large hollow; an internal route reaches an
eye socket framing the landscape like an enormous window.

**Narrative core:** The size of the fallen Titan is unsettling. Weathered skulls
and bones are the most frequent traces of the conflict in the working history.

**Planned gameplay:** Ordinary mobs inhabit the decaying remains. A special item,
boss, or trial is not required; see the [gameplay decisions](../../relics/titan-skull/gameplay/README.md).

**Variants:** A missing tooth, broken projection, partly collapsed socket, or
different burial. Ribs and a full skeleton remain later possibilities.

**Essential:** A face readable from several angles, irregular erosion, accessible hollow.

**Avoid:** Perfect symmetry, a decorative grin, overly fine tooth rows, or a label
identifying the corpse of a named god.

### 6.5 World tree

**Working name:** The Old Root Refuge. **Scope:** later expansion with its own prototype.

**Mood and silhouette:** A solitary giant tree has a broad irregular trunk and a
crown divided into major masses. Roots open into paths and rooms at its base.

**Setting:** Suitable green coasts or broad river valleys. It stands within the
landscape rather than automatically replacing an entire biome. Waterways are an
optional site variant, not mandatory for every tree.

**Exploration:** The crown appears first. Ordinary trees vanish against the trunk
as the player approaches. A root arch enters a sheltered area containing worked
stones held by roots. A short path or stream leads out to a second view of the base.

**Narrative core:** The tree lives while structures under its roots age. It is
uncertain whether the stones predate the tree.

**Variants:** Crown shape, a broken major branch, alternative root passages.
Temple-like reference buildings may inspire small independently designed additions.

**Essential:** Convincing major branches, readable trunk, and accessible base.

**Avoid:** An ordinary tree with only a widened trunk, a compact spherical crown,
or a mandatory climb to the world-height limit.

## 7. Optional later structures

These do not expand version 0.1. Evaluate them once the first two relics work
visually and technically.

| Idea | Mood and possible discovery | Boundary |
| --- | --- | --- |
| Isolated machine fragment | A hand emerges from a riverbank; a younger shelter sits between fingers | Its own site selection, not a randomly incomplete Colossus |
| The Enclosed Ancient One | A huge ambiguous figure lies inside a greenish crystalline body between dark cliffs | Transparency/glow need a separate prototype; no initial release/boss mechanic |
| The Split Monument | An unusual downward-tapering form has a visible gap between major fragments | Design the apparent suspension and material separately; reference scale is not a fixed requirement |

The fragment is the most direct later experiment because it can reuse Colossus
design language, but it still needs its own composition and exploration sequence.

## 8. Storytelling, names, and rewards

### Visible traces before explanatory text

A small stair on a huge armor plate tells of later inhabitants. A buried entrance
tells of changing ground. These clues should work without a written journal.

If texts are added later, use limited viewpoints—travelers, residents, earlier
researchers—who can be mistaken or disagree. Avoid definitive origins while the
design intentionally leaves them open.

### Names

Working names support discussion. Future display names should be short and
descriptive. Version 0.1 needs no elaborate dynasty or religious history for each
relic. Terms such as “Sentinel” remain interpretations unless explicitly established.
The asset version labels are **Colossus v2**, **Colossus v3**, **Obelisk v2**, and
**Obelisk v3**. The current design pair uses v3 for both relics.

### Rewards

Accessible spaces, viewpoints, and striking material forms carry discovery in
the current playable alpha; its lack of custom rewards remains unchanged.
The later gameplay direction differentiates the relics: technical items from the
Colossus, archaeology and maps from the Obelisk, and exploration with ordinary
mobs in Titan remains without requiring an exclusive item. Containers should suit
the site's history and the modpack's balance.

Structures use normal blocks. Consider mining and player reuse when choosing
materials; artificial indestructibility is not part of this design.

## 9. References and design interpretations

The original lore review on September 13, 2026 inspected **66 frames** spread
across the videos. The three image posts supplied drawing time-lapses; complete
carousels were not checked then. Speech and audio were not evaluated in that
review. The later October Obelisk study additionally inspected both *Painted
Desert* paintings and its process animation.

| Reference | Observed motif | Design use |
| --- | --- | --- |
| [Archaean Colossi](https://www.instagram.com/reel/DaoBxUEiBNa/) | Overgrown machine torso among hills, detached foreground arm | Posture, burial, separate component, scale comparison |
| [Painted Desert](https://www.instagram.com/p/Da0NEq7kUAO/) | Simple flat-topped stele in layered dry terrain | Slender proportions, open surroundings, warm mineral faces |
| [Josh White sci-fi animation](https://www.instagram.com/reel/DbqXYoVx2hR/) | Dark breached tower over a pale plain; large aircraft takes off | Contrast and tower negative space; aircraft is not architecture |
| [D.E.A.D.](https://www.instagram.com/reel/DXM3J4sgqJl/) | Crowned skull in green hills; later enormous body remains | Skull as landscape form; possible later bone fragments |
| [World Tree / Gaia's Nursery](https://www.instagram.com/reel/DaBgsX0C9s4/) | Coastal giant tree, worked stones, waterways, root-side structures | Design crown and accessible base together |
| [Warden-Class Archaean Colossi](https://www.instagram.com/reel/DcwuU3SB5gc/) | Metal giants with round joints, chest openings, architecture | Relationship of machinery and built space |
| [Fragment of the Fallen](https://www.instagram.com/reel/DbD0PB7iD2Q/) | Settlements on and around heads, hands, body remains | Small-scale later reuse; independent fragments |
| [The Ancient One](https://www.instagram.com/p/DcoGiYTkWjH/) | Humanlike figure in green glowing crystalline material between cliffs | Optional enclosed Ancient One |
| [Pilgrimage to the Finger of God](https://www.instagram.com/p/Db8UdK1kXdJ/) | Monumental broken form visibly separated above a lower fragment | Unusual geometry, gap, and wide empty landscape |

The mod draws on atmosphere and design principles. Its designs, names, symbols,
and background are developed independently. Working names here do not claim to
be confirmed lore from the reference authors.

## 10. Visual acceptance and next design work

A structure is visually ready for integration once the actual Minecraft model
answers these questions:

- Is its main form readable from several directions and distances?
- Does it work without shaders?
- Do ground transitions and fractures explain how it sits here?
- Is there a specific close discovery and worthwhile backward view?
- Are required routes accessible without mining?
- Are later additions clearly smaller and distinct from the original relic?
- Do multiple examples show deliberate damage rather than random holes?
- Do important questions remain open while visible details stay coherent?

Silhouettes, palettes, player-scale comparisons, and underground inspection views
now exist for the reference-based assets. The next design step is to review them
in Minecraft, finish the Colossus's intended interior route and terrain clearing,
and tune ground transitions before adding more variants.

Final display names, preferred persistent palettes, and the amount of later reuse
remain collaborative decisions. This guide is a concrete working basis, not settled canon.
