# Relic Mod: lore bible and design guide

Original design draft: September 13, 2026. Updated: October 8, 2026.

The five main motifs and version 0.1 scope come from the original concept.
The October gameplay decisions establish a relative discovery hierarchy and a
shared history clarified by the user on October 8 for all seven relic designs.
Approved lore below is distinct from actual builder coordinates, unimplemented
gameplay and optional visual clues. Gameplay/reward policy is selected; technical
defaults and remaining evidence are in the [planning review](GAMEPLAY_PLAN_REVIEW.md).
The current visual build is Alpha 4.9, including material-B Colossus,
the smaller Colossus, both skull designs, Obelisk, Ruined Tower, and World Tree.
Custom gameplay and unique-large-Colossus generation remain planning.
The [lore/gameplay review](LORE_GAMEPLAY_REVIEW.md) records concerns and follow-up
tasks separately from approved mechanics and historical implementation evidence.

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
  frequencies: **Obelisks and both skull designs are the relatively most frequent
  tier**, followed by **rarer Tower, small Colossi and Tree**, then the **unique
  large Colossus: one natural site per game world**. **All relics must feel genuinely
  rare**, with wide gaps; approved starting rates/distances are documented below. This
  replaces the earlier requirement for Obelisks to be clearly rarer than skulls.
- Alpha 4.9 integrates seven designs/ten visual variants. Interior/reward scope
  and shared density contract are specified; builder exports and gameplay runtime
  implementation/evidence remain outstanding.
- Initial structures use regular Minecraft blocks and original designs.
- Shape, ground contact, and close detail must work without special lighting.
- Selected areas are explorable. The visual alpha has no new combat mechanic;
  planned gameplay adds the selected golem trial, not a mandatory global story.

### Approved history: the Titan conflict — October 8, 2026

The conflict took place **thousands of years ago**. The Titans' exact nature and
the reason for the campaign against them are **lost to time**, not design questions
that must be answered by inventing an origin or choosing a good side and a bad side.

- The **large Colossus was the central machine**; the smaller Colossi were its
  companions. **All Colossi were crewed**, not autonomous giants: **five operators
  in the large machine, two in each smaller one**. They were approximately player-
  sized, possibly a little larger; exact species and height remain unknown.
- Smaller Colossi were built from **weaker materials than the large one**, explaining
  their severely decayed interiors and effectively lost cockpits. This is lore,
  not a new approved palette or runtime durability system.
- The iron golem in the large Colossus's head/cockpit was a **defense robot for
  the cockpit**. The user now prefers **autonomous attacks on players in the trial**,
  superseding retaliation-only behavior. Automatic trial-spawner detection is the
  selected activation, without a console; detection/targeting defaults are in the
  runtime contract and need target-version proof;
  only designated defense golems are affected, not all ordinary golems or the whole wreck.
  The normal trial uses **one defense golem**, not multiple enemies or waves;
  health and damage stay unchanged in multiplayer, while each eligible participant
  still receives a key. There is **no ominous Colossus variant**: Trial Omen leaves
  encounter strength and rewards unchanged; unrelated vanilla trials are unaffected.
  It retains **normal movement, combat and pursuit**, including chasing players
  out of the cockpit under normal AI limits. Only initial player aggression is
  changed; no custom cockpit leash, forced return or teleportation is selected.
- **Obelisks marked territories cleared of Titans by the Colossi.** Titan skulls
  are consequently found across the broad surrounding territories, not necessarily
  directly beside each marker. The original function is territorial marking, not
  the previously undecided wayfinder-versus-single-kill-site alternative.
- The **Ruined Tower was the base from which the Titan-clearing campaign was
  organized**. It was never completed. Its unfinished construction is the reason
  for the intended stronger dilapidation relative to the Colossi, not evidence
  that it must be older or have belonged to an unrelated civilization.
- The Titans **worshipped the World Tree and received their strength and size
  from it**. The Colossi's builders tried to destroy it but failed. The tree's
  original creation, the mechanism of its power and evidence of the failed attack
  are not established.
- **No living Titans remain in the present day.** The ancient past does not
  introduce a surviving Titan, a revival quest or a Titan boss. Current Minecraft
  mobs and players inhabit or otherwise reuse the relics. Their modern presence
  is distinct from original crews or Titans; exact authored inhabitants remain open.

These are approved internal facts. How much a player can infer from the ruins is
still a storytelling decision. Exact event order, dates, and the cause of each
machine's downfall are not specified; no exact millennial timeline is invented.

Multiple distinct Titan remains should make the scale of this past conflict
visible. A [second independent skull reference](../../relics/titan-skull/docs/TITAN_SKULL_2_CONCEPT.md)
was selected from Instagram reel `Db9KCtWi0eG`, specifically its opening
few seconds; Skull 2 V2 is now integrated and visually accepted in Alpha 4.9. It is a
new design, not another terrain palette or revision of the existing skull.
Further bone-site concepts may follow, but no living Titan system, full skeleton
at every site, or additional specific anatomy is required by this premise.

Later excavation sites and expedition maps reflect subsequent visitors
investigating these territories. A map to the unique large Colossus is not the
Obelisk's original military function, and players may discover relics independently.

**Approved map exception policy:** valid unique natural destinations remain the
target regardless of distance; temporarily unresolved maps are explicitly
unconfirmed and resolve later to that same site; genuinely unavailable destinations
yield three emeralds instead of the finite map reward, while the trim reward
remains. Never generate an extra Colossus, publish rejected/unverified targets,
pay compensation per copied map or replace a known site merely because it is mined
or future generation is disabled. Implementation/retry/claim handling is still pending.

The builders' identities, original crew and the fate of the machines remain
unknown; the campaign's motive is deliberately lost. The approved world-design
rule is **one large Colossus per save/server**, shared by all players, with multiple smaller Colossi
possible. This does not establish that only one machine ever existed historically,
or a single builder for machines, markers, Titans and the tree. Tower and tree
are now explicitly connected to this conflict. Alpha 4.9 does not enforce uniqueness.

The unique large site must be **at least 30,000 blocks horizontally from the shared
world/initial player spawn to its center**. The delegated search prefers a
30,000–60,000-block annulus, then expands outward without an arbitrary distance
cutoff, respecting actual border/terrain limits. Personal beds and respawn positions do not
move or create another site. The user reaffirmed Obelisks/skulls as the relatively
most frequent tier and rejected too many Tower/small-Colossus/Tree sites in the
first illustration. The user now selected **2% candidate chance each for Tower,
small Colossus and World Tree**, replacing the assistant's reduced 2% / 2% / 1%
proposal. These are approved starting weights, not world-wide count caps or
guaranteed successful-site shares.
After comparing travel times with vanilla villages, the user accepted the revised
illustration's broad distance scale, including the roughly 43,000-block journey to
the large site. Keep this expedition scale; exact per-seed distances are not fixed
at 43,000. The subsequent minimum-distance answer selects 30,000 blocks as above.
No worldgen changes are authorized.

The planned large-site vault must preserve per-player eligibility so later multiplayer
visitors can salvage a **fully charged, immediately usable core** at the same
landmark, without initial restoration. The large arm's functional magnet
remains shared finite loot; smaller sites offer a **10% per-site starting chance
for one repair-required magnet**, not guaranteed per-player access. Magnet full
repair uses a crafting table, the existing magnet, **four iron ingots and one
amethyst shard**, replacing the proposed two redstone. The approved repair is shaped:
magnet center, shard above, iron left/right and bottom-left/bottom-right, with all
other slots empty. **Obelisk archaeology is shared and finite**;
later visitors may search another site or copy/share an existing expedition map.
Its exclusive reward is now an **original cosmetic armor-trim template**, not a
separate display-only collectible. Its motif follows the **angular, geometric
Obelisk forms**; duplication uses **one template + seven diamonds + one copper
block -> two templates**, linking its materials to the Colossi. The approved name
is **Monolith-Rüstungsbesatz / Monolith Armor Trim**, with **narrow vertical lines
and angular branches** reflecting the monument. Duplication layout and finite
ordinary-loot baselines are specified; exact artwork/application needs delivery
and runtime evidence. Small sites
do not inherit the core/trial.

The approved core recharge is a shaped crafting-table recipe: **depleted core in
the middle, one coal block left/right and one amethyst shard directly above -> one
fully charged core**, with provisional capacity of 256 completed operations.
Two coal blocks alone supply 160 operations; the 60% gain, reuse and no idle drain
are intended practical benefits, subject to survival balance testing. No recharge
code or alternate charcoal recipe is implemented/selected by this planning.

### Relative discovery hierarchy

| Relic family | Intended relative frequency | Gameplay role |
| --- | --- | --- |
| Titan skulls and future skull/bone variants | Relatively most frequent tier together with Obelisks; still genuinely rare | Explore unchanged interiors with natural mobs; no loot chests or special item |
| Obelisks | Relatively most frequent tier together with skulls; still genuinely rare | Shared finite exterior archaeology: cosmetic armor-trim template, ordinary sherds/common finds and copyable map |
| Large Colossus | One natural site per game world, not a repeatable density target | Technical salvage and head trial; per-player vault grants a fully charged core |
| Smaller Colossi | Rarer repeatable tier with Tower and Tree; 2% per shared opportunity | Enterable decayed interiors; modest copper/iron salvage, possible amethyst/redstone; 10% per-site broken magnet |
| Ruined Tower | Rarer repeatable tier with small Colossi and Tree; 2% per shared opportunity | Natural mobs, delegated Enderman accent; finite Ender reward: 5% eye, otherwise 4–6 pearls |
| World Tree | Rarer repeatable tier with Tower and small Colossi; 2% per shared opportunity | Illuminated peaceful refuge; more pigs/chickens/sheep/cows without spawners; regeneration is reward enough |

Frequency is a **family-level** target: adding more skull or bone variants should
not multiply total encounter density unintentionally. Relatively most frequent
does not mean that every landscape should be crowded with giant remains.

Numeric planning rates are now selected; no runtime worldgen settings are changed. Future
balancing must account for biome eligibility, terrain rejection, and actual
discovery effort, not only candidate spacing. The four crowned-skull palettes
already share a set; Skull 2 still has an independent provisional rate. A combined
budget across both skull designs and future bone sites remains to be implemented.

Detailed gameplay decisions are maintained with each relic:
[Titan Skull](../../relics/titan-skull/gameplay/README.md),
[Obelisk](../../relics/obelisk/gameplay/README.md), and
[Colossus](../../relics/colossus/gameplay/ITEMS.md).

### Review follow-up: evidence and player incentives

- Select visible links between machine and Titan remains: embedded fragments,
  corresponding damage, and later expedition marks are candidate motifs only.
- Derive spatial clues from the selected Obelisk role: cleared territories with
  widely distributed remains. The user approved **30% Obelisk candidate chance**
  and **30% combined skull chance inside / 5% outside**, shared equally by the two
  skull designs: 15% each inside / 2.5% each outside. Crowned-skull palettes share
  that design's budget. Together with the three 2% shares, this leaves **34% empty
  inside / 59% outside**, before additional placement rejection. The user selected
  a **6,000-block radius** and a **2,000-block horizontal center-to-center separation
  floor across all relic types** and **5% combined skull chance outside** within
  the shared budget. The user approved **at most one shared repeatable-relic
  opportunity per approximately 5,000 × 5,000-block area**, with empty/rejected
  attempts retained and the unique large Colossus outside this budget.
  **Obelisk regions must neither overlap
  nor touch**: the user selected **at least 15,000 blocks between their centers**,
  leaving 3,000 blocks between edges with the approved equal 6,000-block radius.
  This replaces the generic floor for this pair. Actual relative density still
  needs validation; no skull at every marker is guaranteed.
- Design the cockpit and trial around the selected historical defense robot.
  Autonomous player attacks are now the selected behavior direction and require
  scoped AI/runtime support. Automatic trial-spawner activation is selected;
  detection/targeting and reset/cooldown defaults are specified in the runtime
  contract and still need target-version testing.
  Maintenance/later-installation and retaliation-only alternatives are superseded.
- Review resource value against the unique landmark's preservation and special
  rewards; ordinary mining remains allowed. Existing worldgen-feature protection
  is not player-mining protection; no indestructible-landmark rule is selected.
- Clarify the core's everyday benefit and later-visitor reward access before final
  loot tuning. See the [six-point review](LORE_GAMEPLAY_REVIEW.md) for priorities,
  historical V3 quantities, and the distinction between proposals and decisions.

### Proposed guiding idea

Three layers of time can be read at a site: the original monument, its damage,
and later reuse by much smaller inhabitants. Nature grows through all three.

Tell this through construction. A small stair might rest on an old armor plate;
a low ring of loose stone near the Obelisk might suggest a much younger camp.
Such traces remain limited in version 0.1.

### Deliberately unanswered questions

- Who built and crewed the Colossi. The motive for killing the Titans and their
  exact nature remain deliberately lost to time.
- Details of the conflict, including why the campaign and tower construction ended.
- Whether world trees grew, were planted, or were altered.
- Who physically built the Obelisks; their cleared-territory role is established.
- Whether individual relics fell in one event or over many ages within this ancient
  history; no exact dates are fixed beyond thousands of years having passed.

There is no official map of an old empire, fixed list of gods, or global disaster
explaining every discovery. A structure may offer clues without resolving these questions.

## 3. Internal design background

These are working concepts, not necessarily in-game names.

| Layer | Building assumption | Visible evidence |
| --- | --- | --- |
| The old grandeur | Some structures served purposes and scales alien to present inhabitants | Huge material fields, unusual openings, components far beyond human scale |
| The fractures | Places suffered different forms of damage, abandonment, or burial | Sheared connections, collapsed rooms, exposed inner layers |
| Later reuse | Visitors used reachable parts as paths, shelter, or landmarks | Small steps, walls, repaired crossings, abandoned work areas |
| The present | Later inhabitants reuse ancient places; their knowledge of the original purpose can be incomplete | Grass on metal, roots in masonry, open routes, quiet interiors |

Not every relic needs every layer. A nearly untouched Obelisk needs no ruined
city at its base. Some relics may be unoccupied while others are reused. Their
shared ancient conflict does not imply that the Titans, machines, and living tree
were created by the same builders or that every site needs a present-day settlement.

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
route must have a recognizable intended entrance rather than require blind mining.
This is **not a universal no-building traversal rule**: players find/build their
own ascent to the large cockpit's hatch and bridge incomplete Tower stairs.
Other sites' exact traversal requirements remain per-relic decisions.

Reference figures and aircraft do not supply reliable absolute dimensions when
their distance or size is unknown. Current Blender heights are artistic estimates;
two-block figures and same-block-scale previews make our chosen dimensions explicit.

### 4.4 A quiet world with local tension

Most exterior views are calm. Tension comes from entering a darker room, an
ambiguous opening, or imagining how large the complete body once was.
Version 0.1 adds no custom jump scares, bosses, or soundscapes. Sites are not
promised to be mob-free shelters by default. The World Tree is intended as a
peaceful source of life: more selected animals through modest natural spawning,
lighting that reduces darkness-dependent hostile spawning, and Regeneration I in
a 24-block sphere through walls around a fixed trunk-base anchor, lasting about
five minutes after leaving. Ordinary hostiles/arrivals stay natural; there is no
barrier or immunity. Technical refresh/spawn rules are specified, not tested;
lighting alone does not guarantee complete safety.

### 4.5 Light and color

Daylight, shadows, and surroundings carry the main effect. The Tree's approved
root/base-only lighting is an upcoming builder addition, not in the current alpha;
other custom light accents and the glowing Ancient One remain optional later work.

| Material family | Design role | Initial vanilla palette options |
| --- | --- | --- |
| Dark supporting mass | Torso, tower, exposed technical layers | Deepslate, basalt, dark stone |
| Aged metal skin | Selected armor, rings, joints | Copper aging stages; test persistent states |
| Pale mineral mass | Skull, light erosion, monument faces | Calcite, bone blocks, sandstone, pale stone |
| Later small-scale interventions | Paths, supports, shelters | Wood, cobblestone, sparse ordinary lighting |
| Returning nature | Ground joins, seams, sheltered tops | Dirt, moss, grass, roots, suitable leaves |

This is a palette to try, not a requirement to use every material. Assess large
quantities of economically valuable blocks as part of exploration/resource balance.
The review flags the V3 Colossus's 141,523 copper-based and 5,609 raw iron blocks
as a potential incentive to dismantle the landmark. Recount the selected export
and evaluate recovery value. The original suggestion of concentrated salvage and
less valuable broad fields has since led to the approved
[material study B](../../relics/colossus/docs/COLOSSUS_MATERIAL_STUDY_B.md): 25,423
copper blocks and 90 raw iron items, with intact V4.1 geometry preserved. This is
the selected asset palette/inventory, not a pending material choice. Alpha 4.9
includes B; recovery value and balance against future special rewards remain open.
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

**Narrative core:** An ancient territorial marker declared an area cleared of
Titans by the Colossi. Weathered skulls scattered over the surrounding territory
are its spatial counterpart. Later inhabitants may use it as a landmark and
investigate its foot; that reuse is not its original purpose.

**Planned gameplay:** Shared finite archaeology at its foot yields an original
cosmetic armor-trim template and a map to the unique large Colossus. Multiple maps
may lead to the same site and can be copied/shared. The trim uses geometric Obelisk
forms and can be duplicated with seven diamonds and a copper block plus the existing
template. Regional placement is specified; exact trim art/application needs delivery
and tests. No replenishing per-player finds are
selected. See the
[gameplay decisions](../../relics/obelisk/gameplay/README.md).

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

**Historical design:** [Obelisk v3](../../relics/obelisk/docs/OBELISK_V3.md) refines this using the supplied antiprism diagrams:
eight long triangular faces, a smaller square crown rotated 45 degrees, and only
eight blocks of burial. Broad quiet facets now carry the shape instead of a
rectangular shaft.
The current build selects V4.2; versioned asset documents retain their historical
geometry and review evidence.

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

**Exploration:** The nearer arm makes the machine readable and offers its separate
short magnet exploration. The existing main body cavity remains largely as-is.
Players climb or build their own route to the head's identifiable hatch; a ready-
made ground-to-cockpit stairway is not selected. Normal building/mining remains allowed.

**Approved interior scope:** Keep the existing large hollow body; develop mainly
the **head/cockpit for five near-player-sized operators**, its defense robot and
trial/vault. Provide a hatch and targeted clear cockpit/entry volumes. Exact
stations, retained machinery and hatch position remain open. Do not invent a
multi-room body rebuild or completed ascent. Smaller companions had two operators
but now have enterable, very decayed interiors with cockpits effectively absent.

**Narrative core:** Something overwhelming to humans has itself become ground,
roof, and path. It was the central crewed Colossus in the ancient Titan-clearing
campaign, accompanied by smaller crewed machines. The original motive and Titan
nature are lost to time; the builders' identities and its own fall are unknown.

**Occurrence and variants:** One large Colossus is intended per world. Its model
revisions and possible appearance variants do not authorize more large sites.
The planned smaller Colossi are separate, repeatable relic designs; new poses
and their loot require separate decisions and acceptance work.

**Essential:** Readable posture, extensive ground contact, a detached component,
and an accessible main room.

**Avoid:** Randomly assembled limbs, floating parts, uniform greenery, and a fully
equipped cockpit that immediately explains every function. The machine does not
activate in version 0.1.

**Historical designs:** [Colossus v2](../../relics/colossus/docs/COLOSSUS_V2.md) has the reference's bronze
dome helmet, narrow visor, respirator hoses, and broad armor. [Colossus v3](../../relics/colossus/docs/COLOSSUS_V3.md)
continues below ground through the abdomen to an irregular torn hip, exposed
supports, and conduits, without legs. The surface silhouette is preserved at
almost the same block scale. An accessible in-terrain route for these new assets
still needs to be completed and tested.
Alpha 4.9 selects V4.1 with material study B. Both large and smaller Colossi need
targeted interior/access plans. Small sites have an approved starting **10% chance
per site for one broken magnet**, requiring the selected shaped four-iron/shard
repair; exact builder placement remains undelivered.
They do not inherit the large site's trial, core or vault.

### 6.3 Ruined tower

**Working name:** The Open Tower. **Status:** V7 ground-v3 visually integrated;
gameplay and interior layout remain planning.

**Mood and silhouette:** A dark angular mass with major vertical openings stands
over a pale plain. Missing walls expose deep rooms and isolated surviving connections.

**Setting:** Dry open basins and suitable desert edges. A few independently
designed lower parts may emphasize the main tower's height.

**Exploration:** The tower is predominantly abandoned. Incomplete stairs allow
players to work upward to an upper level, **requiring them to build across gaps**.
Exact entrance/levels remain open. The proposed lower dungeon now has an Ender-
themed direction, with less common mobs such as Endermen. Chest loot should be
**shared finite Ender loot: 5% eye, otherwise 4–6 pearls**. Ordinary mobs keep
natural spawning and vanilla behavior. The user delegates the Enderman accent's
method; the integration recommendation is a few one-time Endermen at generation
(**five**, replacing the earlier two-Enderman proposal), without recurring spawners
or altered hostility. Vanilla
despawning/teleportation still applies, not guaranteed persistent guards. The
starting loot interpretation is one roll per Tower, one eye on the 5% branch;
exact positions/technical validation remain. No custom boss or mandatory combat
gate is selected.

**Narrative core:** This was the campaign's organizing base, but it was **never
finished**. Unfinished construction and millennia of decay account for its stronger
dilapidation relative to the Colossi. Modern inhabitants may reuse parts of it;
room functions, the reason construction stopped, and exact reuse remain open.

**Variants:** Missing side sections, buried lower floors, limited height changes.
Do not create dead ends on required routes through free recombination.

**Essential:** Large negative spaces, dark mass against light terrain, and at least
one meaningful reachable viewpoint.

**Avoid:** A uniform skyscraper with copied floors and purely decorative doors.
The aircraft taking off in the reference is not a fixed annex.

### 6.4 Titan skull

**Working name:** The Face in the Valley. **Status:** crowned Skull V4 and separate
Skull 2 V2 visually integrated; existing interiors and current accessibility
accepted as-is for now. Mob spawning stays natural and unchanged, without authored
encounters; **neither skull gets loot chests**.

**Historical asset study:** [Titan Skull v3](../../relics/titan-skull/docs/TITAN_SKULL_V3.md) retains the fused
organic crown, hollow cranium, triangular nose, open jaw, and lateral spurs of v1,
but reduces the skull to approximately Colossus-head scale. The user's premise is
that the living titan could have fought the Colossus. This guides relative size
and the working Titan-conflict history without adding a fight mechanic. V3 includes
a complete posterior wall and a broken nine-vertebra spine, partly buried in an
extended solid local mound. Two dislocations and loose fragments suggest an
incomplete fallen skeleton. The earlier route idea below is not a new required
layout: the current interiors and terrain-placement accessibility of both skull
designs are accepted as-is for now. No additional access review or terrain-clearing
work is selected; leave the current state unchanged.

**Mood and silhouette:** An eroded mineral form becomes recognizable as a skull.
Eye sockets, nose, and mouth determine its shape. A few broken projections suggest
a crown without explaining its origin.

**Setting:** Broad green valleys and grasslands. The lower jaw/face partly merges
with terrain. Pale bone or stone alternates with soil and growth.

**Exploration:** At first it resembles unusual geology. A side view reveals the
eye and jaw. Existing hollows are the approved exploration basis for both designs.
The earlier mouth-to-eye-socket route is optional inspiration, not a required new
circuit or authorization to rebuild the accepted interiors.

**Narrative core:** The size of the fallen Titan is unsettling. Both skull designs
belong to Titans that worshipped the World Tree and received strength and size
from it. No living Titans remain; ordinary current inhabitants occupy their remains.
Skulls occur across the territories marked as cleared by Obelisks. Their exact
ancient nature, the campaign's motive and Skull 2's sword owner remain unknown.

**Gameplay direction:** Ordinary mobs may naturally spawn in the decaying remains;
the user selected **no additional spawners, placed enemies or spawning changes**
for either design. A special item, boss, or trial is not required; see the
[gameplay decisions](../../relics/titan-skull/gameplay/README.md).

**Variants:** A missing tooth, broken projection, partly collapsed socket, or
different burial. Ribs and a full skeleton remain later possibilities.

**Essential:** A face readable from several angles, irregular erosion, accessible hollow.

**Avoid:** Perfect symmetry, a decorative grin, overly fine tooth rows, or a label
identifying the corpse of a named god.

### 6.5 World tree

**Working name:** The Old Root Refuge. **Status:** V4.3 strands and terrain
integration visually accepted; gameplay and exploration layout remain planning.

**Mood and silhouette:** A solitary giant tree has a broad irregular trunk and a
crown divided into major masses. Roots open into paths and rooms at its base.

**Setting:** Suitable green coasts or broad river valleys. It stands within the
landscape rather than automatically replacing an entire biome. Waterways are an
optional site variant, not mandatory for every tree.

**Exploration:** The crown appears first. Ordinary trees vanish against the trunk
as the player approaches. A root arch enters a sheltered area containing worked
stones held by roots. A short path or stream leads out to a second view of the base.

**Narrative core:** The Titans worshipped this tree and received their strength
and size from it. The Colossi's builders tried and failed to destroy it. It endures
after the Titans' disappearance and may now be reused by ordinary inhabitants.
The tree's origin, age relative to worked stones and visible attack/worship traces
remain open. The selected present-day direction is a **peaceful source of life**:
natural-looking lights using **glow berries, glow lichen, firefly bushes and sparse
shroomlights**, more pigs/chickens/sheep/cows through a modest local natural-spawn
adjustment, without animal spawners or farm-like rapid replenishment. Other mobs
remain natural; lighting should reduce darkness-dependent hostile spawning. Lighting
is confined to the **trunk/base and roots**, with irregular growth reaching **at
most 15 blocks up the trunk**; no upper-branch/crown lights are selected. At ground
level it spreads broadly and asymmetrically around the trunk/roots to reduce dark
spawnable areas beneath the canopy. Exact spread/positions remain open, independent
of the aura radius; firefly bushes add vanilla visuals, not a new firefly mob.
The user selected **one small amethyst sphere inside the trunk at its bottom/base**,
instead of optional scattered clusters. It is **decorative and normally mineable**,
with ordinary amethyst blocks/optional crystals, **no budding amethyst or crystal
regrowth**. Exact builder design remains pending; it does not relocate or disable
the registered aura when removed.
The beneficial effect is reward enough; no additional Tree loot/chest or exclusive
item is selected.
Approved starting values are **Regeneration I within about 24 blocks of the trunk**,
refreshed during the stay and lasting **about five minutes after leaving**. A fixed
builder-supplied trunk-base anchor and a **24-block-radius sphere** are selected;
the aura **works through wood, walls and terrain**, without requiring free sight.
The exact anchor coordinate remains a builder deliverable. Technical refresh is
every 20 ticks to 6,000 ticks with ordinary effect merging; neutral/hostile arrivals
remain natural. These require runtime tests; further effects are not selected. This
does not require a literal beacon or guarantee total safety from lighting alone.
The regeneration aura **remains at its registered natural-site location even after
heavy damage or complete removal of the Tree**. Mining stays allowed; no automatic
restoration, indestructibility or new aura from player-built copies is selected.
No Titan revival, player gigantism, boss or destruction quest is introduced.

**Variants:** Crown shape, a broken major branch, alternative root passages.
Temple-like reference buildings may inspire small independently designed additions.

**Essential:** Convincing major branches, readable trunk, and accessible base.

**Avoid:** An ordinary tree with only a widened trunk, a compact spherical crown,
or a mandatory climb to the world-height limit.

## 7. Optional later structures

The [four-relic pre-modeling study](NEXT_FOUR_RELIC_DESIGN_STUDY.md) records the
new working dimensions and damage targets for the tower, tree, smaller Colossus
and second skull. It separates observed reference features from authored choices;
it does not establish a sword owner, new rewards or a shared builder for all relics.

The user subsequently requested [four V1 models and exports](NEW_RELICS_V1.md).
These V1 exports are historical; all four designs have successors in Alpha 4.9.
Their lore now follows the October 8 decisions above, not the original undecided
connection to the conflict. Gameplay remains unimplemented.

The optional ideas in the table below are not part of the seven-design planning
scope and are not authorized by the new lore.

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
Versioned asset labels identify geometry/reproduction history, not separate
historical machines. Consult the current README/catalog for selected build assets.

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
| [Second Titan Skull reference](https://www.instagram.com/reel/Db9KCtWi0eG/) | Opening 0–6 s verified: overgrown skull with diagonal embedded sword in a damp cavern | Separate second skull/sword composition; no crown or copied spine |
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
- Are intended entrances identifiable, and are any required player-built climbs/
  stair bridges deliberate rather than accidental placement failures?
- Are later additions clearly smaller and distinct from the original relic?
- Do multiple examples show deliberate damage rather than random holes?
- Do important questions remain open while visible details stay coherent?

Silhouettes, palettes, player-scale comparisons, and underground inspection views
exist and Alpha 4.9 has integrated the seven designs. The October 8 all-relic
documentation/consistency gate is closed by the planning review; gameplay, revised
interiors and original item/trim artwork still need a separate implementation
request and the runtime acceptance matrix.
Interior access and gameplay acceptance are not implied by visual-model acceptance.

Item/key/Monolith German and English display names are final. Structure working
names and optional later reuse remain illustrative, not required new decisions.
Selected palettes stay preserved; changing them needs separate review.
The October 8 history is approved internal lore;
unresolved details and illustrative exploration motifs are not additional canon.
