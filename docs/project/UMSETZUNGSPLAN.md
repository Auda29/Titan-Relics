# Relic Mod: technical implementation plan

## Current planning gate — October 8, 2026

The user selected **Minecraft 26.2 / Fabric first** for the upcoming gameplay
work. The existing 1.21.1 visual-alpha port remains preserved; extending gameplay
to that port is a separate later decision, not part of the first implementation.

**Before gameplay implementation**, document and review the gameplay,
interior/exploration requirements, placement of encounters/rewards, and lore for all
seven relic designs: large Colossus, small Colossus, Obelisk, crowned Titan Skull,
Titan Skull 2, Ruined Tower, and World Tree. Capture the user's answers in their
per-relic documents and shared lore; proposals must remain distinct from approvals.
No new gameplay systems, items, interior exports, or generation changes are
authorized by this planning request.

Run a documentation consistency review before proceeding: reconcile the current
asset/build status, lore connections, reward-sharing rules, item acquisition and
costs, unique-large-site/maps, and the shared Titan-remains density budget. Mark
superseded passages as historical rather than leaving conflicting active rules.
Unanswered lore may deliberately remain mysterious, but record whether it is
internally decided, intentionally unknown, or still awaiting a design decision.

The current visual baseline is **Alpha 4.9**, with seven designs/ten variants;
see [README](../../README.md) and [runtime report](../testing/ALPHA_4_9_TEST_REPORT.md).
It includes Colossus material B and placement-only Java code, **not** the planned
items, trials, archaeology, maps, authored encounters, or large-site uniqueness.
The older milestones and Alpha 2/3 tables below are historical planning context,
not the current implementation inventory. The reconciled status and remaining
evidence gates are recorded in the [planning review](GAMEPLAY_PLAN_REVIEW.md).

### Planning closure and next implementation handoff

The user-level gameplay round is complete. The requested technical/marker work
and documentation reconciliation are now specified in:

- [Gameplay runtime and delegated starting defaults](../technical/GAMEPLAY_RUNTIME.md)
- [Version-1 builder sidecar/marker contract](../technical/GAMEPLAY_MARKERS.md)
- [Deterministic shared budget and unique-site resolver](../technical/RELIC_DISTRIBUTION.md)
- [Future gameplay acceptance matrix](../testing/GAMEPLAY_ACCEPTANCE_PLAN.md)
- [Consistency review, authority and remaining deliverables](GAMEPLAY_PLAN_REVIEW.md)

These documents close the **planning/documentation gate**, not runtime acceptance
or implementation authorization. Actual builder coordinates/revised exports,
original item/trim artwork, API proof gates and Minecraft tests remain deliverables.
The present request is to complete and push documentation only. A subsequent
implementation request can start the technical proof/item work without another
large questionnaire; changed approved behavior still requires approval.

### Responsibility clarification — October 8, 2026

The user assigns **structure construction/interior authoring to another agent**.
This planning/integration work defines gameplay requirements and then implements
them in the mod; it does not author the structures block by block or require the
user to approve every room coordinate. **Custom items, recipes, item models and
textures are within this work's implementation scope.** This clarification does
not itself start implementation or dispatch work to another session; finish the
all-relic gameplay planning/consistency gate first.

For the structure handoff, specify the intended experience, preserved/unchanged
areas and necessary gameplay locations/space. The builder should later supply
template-relative positions/markers for spawners, vaults, loot containers and
archaeology, and references for the Tree's trunk/aura and lighting extent. The
[version-1 sidecar contract](../technical/GAMEPLAY_MARKERS.md) selects raw-template
coordinates/hash binding and records roles/transforms so mod integration
can apply rotation/translation, inject block-entity/loot data and identify natural
sites without guessing coordinates from appearance. The contract is documented,
but its loader and actual builder markers are not implemented/delivered. It grants
no permission to change the accepted skulls.

Encounter/spawn rules, sharing, Tree policy, item presentation and distribution/map
policies are now selected. Delegated ordinary-loot quantities, recipe/icon rules,
state handling and API proof requirements are in the runtime contract. Exact authored
coordinates/artwork are builder/integration deliverables, not another questionnaire.
No additional relic designs or answers to deliberately lost history are required.

### Approved lore implications — October 8, 2026

All Colossi were crewed, with five operators in the central large machine and
two in each smaller companion, approximately player-sized and perhaps a little
larger. Keep the large body's current cavity and develop mainly its head/cockpit
and identifiable hatch; players find/build their own climb. Smaller machines have
enterable but very decayed interiors with cockpits effectively gone, explained by
weaker original materials. Exact crew species/dimensions and interior blocks remain open.

The existing interiors and current terrain-placement accessibility of both skull
designs are accepted as-is for now. No new room layout, required mouth-to-eye
circuit, additional access review or terrain-clearing work is in the current scope.
Ordinary mobs spawn naturally; no extra spawners, placed enemies, spawn-rate changes
or custom encounter/persistence logic are selected for either skull.
Neither skull gets loot chests or another scripted reward.

The tower is predominantly abandoned, with incomplete stairs requiring player
building to reach an upper level. Ordinary mobs spawn naturally without added
spawners/roster changes. The user delegates whether extra Endermen use local weights
or one-time generation placement; the integration recommendation is a small
one-time group (**five**, as selected by the user), preserving vanilla neutrality/teleportation/
despawning. This still needs safe marker/state/worldgen validation, not both methods
at once. Loot is **shared finite chests, 5% eye otherwise 4–6 pearls**. The documented
starting roll scope is one Ender reward per Tower, with one eye on the rare branch.
The World Tree is a peaceful source of life with natural-looking lights and more
**pigs, chickens, sheep and cows**, using a modest local natural-spawn adjustment
with normal caps/conditions, **no animal spawners or timed replenishment**. Ordinary
hostiles remain natural, reduced through the selected lighting rather than a new
despawn/barrier/spawn-blocking system. No Tree loot is selected; its effect is
reward enough. It has a trunk-focused beacon-
style benefit: approved starting values are **Regeneration I within about 24 blocks
of the trunk**, refreshed during the stay and lasting **about five minutes after
leaving**. The selected aura volume is a **24-block-radius sphere around a fixed
builder-supplied anchor at the trunk base**, using three-dimensional distance.
The aura **works through wood, walls and terrain**, without a line-of-sight or
block-obstruction requirement; spatial inclusion depends only on distance.
The builder supplies the exact anchor. The runtime baseline refreshes every second
to five minutes, with ordinary effect merging and no stronger-effect downgrade;
neutral/hostile behavior stays natural. Additional effects are not selected. The
user selected that the regeneration aura **remains at the original registered
natural site even after damage or complete Tree removal**. Normal mining stays
allowed; no rebuilding/protection or aura creation by copied wood/lights is selected.
The approved light palette is glow berries, glow lichen, firefly bushes and sparse
shroomlights. Restrict lighting to the trunk/base and root area, with irregular
growth at most 15 blocks up the trunk and no upper-branch/crown lights. Spread
ground-level lighting broadly/naturally around the trunk and roots to reduce dark
spawnable canopy-shaded areas. Exact spread/positions/quantities remain open, not
automatically equal to the 24-block aura radius. The user selected **one small
amethyst sphere inside the trunk at its bottom/base**, replacing the optional
scattered-cluster proposal. It is **decorative and normally mineable**, with ordinary
amethyst blocks/optional crystals, **no budding amethyst or regrowth**, and no control
over the persistent aura. Exact builder design remains pending;
this does not add custom firefly mobs or a guaranteed universal safe zone.
Lighting alone does not enforce total safety. These traversal rules supersede historical
blanket expectations of fully walkable/no-building routes.

Plan the five-operator cockpit and its historical defense robot before encounter
implementation. **Autonomous attacks are preferred**, requiring targeted AI/runtime
support for designated trial golems, not a global golem behavior change or spawner
data alone. Activation uses automatic trial-spawner player detection, not a console;
the user selected **one defense golem per normal trial**, without a group or
successive waves. Multiplayer leaves its health and damage unchanged, without
player-count scaling; each eligible participant still receives a key. The user
selected **no ominous Colossus variant**: Trial Omen leaves count, strength and
key/core rewards unchanged, without affecting other vanilla trials;
the defense golem retains **normal movement/pathfinding/combat and may pursue
players out of the cockpit**. Only initial player aggression is changed; no
custom cockpit leash, forced return or teleportation is selected.
The runtime baseline uses 14-block player registration with vanilla visibility,
Survival/Adventure only and a 30-minute completed-trial cooldown; these engineering
defaults need target-version validation. Smaller Colossi offer
an approved starting **10% chance per site for one broken magnet**, requiring repair;
the selected sidecar provides one copper-chest marker; its coordinates remain a
builder deliverable. The large
arm's shared guaranteed magnet and per-player core-vault direction are retained.
Vault cores are **fully charged and immediately usable**, with no initial
restoration requirement. The approved crafting-table recharge uses a depleted core
in the middle, one coal block on each side and one amethyst shard directly above,
yielding one fully charged core (provisional 256 operations). Magnet full repair
uses a crafting table and the existing magnet plus four iron ingots and one
amethyst shard in place of the proposed two redstone. Its approved **shaped layout**
has the magnet in the middle, shard above, iron left/right and bottom-left/bottom-right,
with the remaining three slots empty. State handling is specified in the runtime
contract; implementation and balance testing remain.

The earlier 24-coal/four-redstone and three-coal-block proposals are superseded by
the approved **two coal blocks + one amethyst shard + depleted core** shaped recipe.
Two coal blocks alone supply 160 operations, versus the core's provisional 256
(60% more). No charcoal variant is selected. Preserve the existing core's state,
consume recharge ingredients and prevent duplicate items/charge exploits. Recipe
state handling and survival balance still require testing after the planning gate.
The tower was the never-finished campaign base;
the World Tree supplied Titan strength/size and survived attempted destruction.
No living Titans remain; today's inhabitants are ordinary mobs/players, not
surviving ancient crews by default. See [approved lore](LORE-BIBLE.md).

Obelisks marked **cleared territories**, with skulls scattered across broad
surroundings. Plan a regional relationship with explicit distances, counts,
biome/terrain compatibility and interaction with the combined skull-family budget.
This is not a requirement to attach a skull to every foundation or spawn rejected
sites. The current independent structure sets do not enforce this regional lore.
No generation, interior or encounter implementation follows from these answers.

Obelisk exterior archaeology grants an **original cosmetic armor-trim template**
instead of a separate display-only collectible, alongside its expedition map.
Finds are **shared and finite**: late visitors may seek another Obelisk or copy/
share recovered maps. No individual/replenishing archaeology is selected. Trim
motif follows the angular geometric Obelisk forms. Approved duplication is one
template + seven diamonds + one copper block -> two templates, with copper linking
to the Colossi. The runtime selects the normal duplication layout (template top-middle,
copper center, diamonds in the remaining seven slots) and finite eight-block
archaeology baseline. Exact art/coordinates and application tests remain deliverables.

### Latest loot/distribution closure — October 8, 2026

- **Approved machine-item display names (German / English):** Maschinenkern /
  Machine Core, Bergungsmagnet / Salvage Magnet, Colossus-Schlüssel / Colossus Key.
  Artwork, presentation and item registration remain pending. The user selected
  **Monolith-Rüstungsbesatz / Monolith Armor Trim** for the Obelisk's exclusive
  cosmetic trim; its exact artwork/icon remains to be designed.
  The approved pattern direction is **narrow vertical lines with angular branches**,
  reflecting the Obelisk silhouette; exact pixel layout across armor pieces is pending.
- **Approved Machine Core appearance:** compact angular copper housing with a
  visible inset violet energy element. Exact artwork remains pending; state display
  and three-state icon thresholds are specified in the runtime contract;
  this does not change recipes or structure materials.
- **Approved Salvage Magnet appearance:** compact rectangular copper device,
  iron front and violet indicator, rather than a conventional U-shaped magnet.
  Passive offhand mechanics and repair ingredients remain unchanged.
- **Approved Colossus Key appearance:** angular copper key with geometric head,
  toothed shaft and a small violet inset. Vault consumption/eligibility rules are
  unchanged; exact asset creation remains pending.
- **Approved core/magnet status display:** exact remaining values in tooltips and
  changing item icons for full/partly used/empty or broken states, **without an
  inventory status bar**. Full/partial/zero thresholds are specified; exact wording
  and icon artwork are implementation deliverables.
- Colossi ordinary loot: modest distributed copper/iron finds, with possible
  amethyst/redstone, in shared finite containers. Exact amounts/anchors are tuning/
  builder details; the runtime now selects modest site-wide starting quantities,
  without changing material B or creating bulk mineral fields.
- The user delegates modest ordinary archaeology loot: the Obelisk plan defines
  six ordinary brushable finds (one item each) from vanilla pottery sherds, clay,
  bricks, bones, string, seeds and small metal finds, alongside reliable map/trim
  roles. These are assistant-defined starting weights/amounts, not user-specified
  values or another exclusive reward.
- Updated relative frequency tiers: **Obelisks + both skulls**, then **Tower +
  small Colossi + Tree**, then the **unique large Colossus**. The selected candidate
  shares below define starting ratios, not guaranteed successful-site ratios.
  **All relics must be genuinely rare and widely
  separated**, avoiding repetitive "another skull" discoveries. This supersedes
  the earlier Obelisks-clearly-rarer-than-skulls rule.
- The distance/region visual review is complete and the starting values below
  are approved. Validate actual density against real-world evidence. A region means
  widely scattered surrounding remains, not a cluster beside every foundation.
- The user has now **approved all three map exceptions** below: distant valid
  target remains the destination; temporarily unresolved maps remain unconfirmed;
  genuinely unavailable destinations yield three emeralds instead of the map.
  Continue requiring one valid natural destination, never a rejected candidate
  or extra Colossus made for a map.

### Distribution proposal and approved map exceptions

The distribution's distances, region radius, opportunity budget and conditional
candidate shares below are **user-approved starting values**, not implemented
generation settings or guaranteed successful-site density. The **map exception
policy is approved**; its code/state handling remains unimplemented.

#### Shared repeatable-relic budget

**User-approved starting budget:** use one combined candidate budget for all repeatable families, **at most
one opportunity per approximately 5,000 × 5,000-block area**, with seed-dependent
positions rather than a visible regular layout. This is not a guaranteed successful
site per cell; rejected/empty opportunities remain empty. The original global 30% skull
proposal is now refined by the user's request for higher skull likelihood only
around Obelisks. **User-approved conditional starting shares** are:

| Relic/outcome | In a valid Obelisk region | Outside such regions |
| --- | --- | --- |
| Obelisk | 30% | 30% |
| Crowned skull, all four palettes combined | 15% | 2.5% |
| Sword-bearing Skull 2 | 15% | 2.5% |
| Ruined Tower | 2% | 2% |
| Small Colossus | 2% | 2% |
| World Tree | 2% | 2% |
| Empty opportunity, rather than reallocating suppressed/rarer shares | 34% | 59% |

The combined skull chance is **30% inside / 5% outside**, not 30% per design,
palette, chunk or an additional roll outside the shared budget. The user approved
the **5% combined outside chance**; the regional radius below is also user-approved.
Do not renormalize the outside weights to fill its deliberate empty share. The unique large
Colossus is **outside this repeatable budget**, still one natural site per save.
The user rejected the first visualization's excessive Towers/small Colossi/Trees
and reaffirmed the hierarchy: **Obelisks/skulls -> rarer Tower/small Colossus/Tree
-> unique large Colossus**. The user now selected **2% each for Tower, small
Colossus and World Tree**, superseding both the first 15% / 15% / 10% illustration
and the reduced assistant 2% / 2% / 1% proposal. The user's "under ten" is interpreted here
as a visual count target per type in the shown 60,000 × 60,000-block example,
**not a world-wide cap**. The three 2% candidate weights are approved starting values,
not guaranteed realized site ratios. Do not impose an artificial nine-site limit or silently
resample examples to hide random variation.
The user approved a **2,000-block minimum horizontal center-to-center distance** between
successful natural relic sites, including different families and the large site,
with additional model-footprint checks as needed. **Obelisk-to-Obelisk separation
has the stronger approved non-overlapping-region constraint below**, not merely
this general floor. These are floors, not target pairing distances or guaranteed
5,000-block travel intervals.

Invalid biome/terrain candidates leave gaps; do not force a replacement structure
or fill every area. Weights describe candidate opportunities, not guaranteed shares
of successful placements or player sightings. The current independent structure
sets cannot produce this combined budget by merely copying the spacing to each
family; selecting/rejecting candidates and cross-family separation follow the
new [distribution contract](../technical/RELIC_DISTRIBUTION.md). Validate real seeds/routes against the accepted
illustration rather than treating candidate ratios as guaranteed placement ratios.

**User-approved regional radius: 6,000 blocks horizontally around a valid natural
Obelisk**, while retaining the approved **2,000-block relic separation floor**;
thus nearby skulls would be broadly scattered approximately 2,000–6,000 blocks
away, not at the monument's foot. Neither a fixed skull count nor a skull at every
Obelisk is guaranteed. Other relics remain possible in the region.

**User-approved regional constraint:** natural Obelisk regions must **neither
overlap nor touch**, with **at least 15,000 blocks horizontally between Obelisk
centers**. This replaces the general 2,000-block floor for this pair and supersedes
the earlier 12,000-block touching threshold / proposed 13,000–14,000-block buffer.
With the approved equal **6,000-block radii**, the minimum leaves **3,000 blocks
between region edges**. The 15,000-block minimum is selected, not merely a buffer
proposal; it does not require a regular grid or exactly equal pairwise distances.
The radius is selected; actual density still needs validation. Require **distance > R1 + R2**
as well as the 15,000-block floor if radii later change. Do not solve overlap merely
by unioning regions or capping their stacked spawn weights.

The stronger marker separation rejects more Obelisk attempts, so the 30% candidate
weight is **not a guaranteed share of successful sites**. Review aggregate density,
the intended relative tiers and the regional coverage together; do not compensate
by adding extra opportunities or forcing invalid terrain placements. The existing
5,000-block opportunity grid alone cannot guarantee disjoint regions.

**Schematic visual check:** [interactive distribution illustration](visualizations/relic-distribution-plan.html)
shows three deterministic 60,000 × 60,000-block examples using these approved starting weights,
approved marker/general separation, region radius and large-site spawn floor, without biome/terrain
filtering or actual Minecraft worlds. The first version exposed excessive Towers/
small Colossi/Trees after the stronger Obelisk exclusion; the user's correction is
shown with the user-selected 2% / 2% / 2% weights above, without a count cap. The current
illustration also marks an example world spawn and the unique large site **about
43,012 blocks away** (coordinates chosen solely for illustration). Do not treat
candidate weights as achieved ratios or this example distance as an approved
minimum. The artifact does not modify templates, gameplay or worldgen settings.
With the user-selected 2% Tree share, all three displayed examples still have
fewer than ten Tower/small-Colossus/Tree sites per type. Example 2 has **seven
Trees and six Obelisks**: the hierarchy is a distribution-level goal, not a hard
ordering in every finite sample. Do not hide this by rerolling examples or capping
counts; validate the aggregate hierarchy across many seeds and actual terrain.

**User acceptance after the travel-time comparison:** the distances in the revised
illustration are satisfactory; retain this wide-ranging expedition scale as the
planning baseline rather than reducing it to village-like spacing. This includes
the illustrative large-Colossus journey of about 43,000 blocks from spawn. It is
acceptance of the shown distance scale, not a requirement for those exact site
coordinates, identical distances in every seed or a hard 43,000-block spawn floor.
The user subsequently selected a **30,000-block horizontal minimum from the shared
world spawn to the large site's center**. The delegated resolver searches 30,000–60,000
blocks first, then outward 20,000-block annuli without an arbitrary maximum-distance
cutoff; physical border limits apply. Candidate weights are approved starting values
and worldgen is unchanged.

Region anchors must correspond to valid natural Obelisk sites,
not rejected/nominal candidates or extra markers spawned to satisfy the rule.
Resolve Obelisk anchors before conditional skull selection with deterministic,
order-independent site planning; do not base the rule solely on already visited
chunks, retroactively add skulls, or create circular placement dependencies.
The current independent structure sets do not implement this regional model.

Obelisk/skull regional lore must **not** add bonus skulls outside this budget.
The radius, general separation and shares are approved; deterministic selection
is specified in the distribution contract. Biome/terrain API equivalence and
realized density still need implementation/validation.
**Approved large-site direction:** the unique large Colossus must be **far from
the shared world/player spawn**, with an approved **30,000-block horizontal minimum
to its center**, not a near-spawn reward. Its delegated search preference and
resumable validation are specified in [Distribution](../technical/RELIC_DISTRIBUTION.md);
the illustrated travel-distance scale is accepted as above. Do not reinterpret this
as moving it relative to every player's bed or personal respawn point. Approved
maps still have no maximum travel-distance cutoff.

#### Approved map policy

1. **Valid natural unique destination:** every expedition map points to it even
   from far-away Obelisks. Do not substitute a small Colossus or generate another
   large one. No maximum travel-distance cutoff or teleportation; distance/direction feedback
   is useful optional presentation to specify later.
2. **Destination not yet resolved / transient search or loading problem:** retain
   an explicitly **unconfirmed expedition-map state** and retry target resolution;
   publish coordinates only after validity is established. All such maps resolve
   to the same saved destination. This requires custom item/state handling,
   not a fabricated marker, generic empty vanilla map or permanent fallback due
   solely to one failed/bounded search. Never reroll other archaeological loot.
3. **Destination genuinely unavailable**, for example large-Colossus natural
   generation disabled before any site exists: replace that site's map reward
   with **three emeralds**, shared finite like its archaeology. The trim reward
   remains. This compensation is not a new structure or repeatable payout. Already
   valid existing destinations stay valid even if future generation is disabled.

All three cases are **approved by the user**. Resolution/retry feedback, per-origin
claim state and re-enable behavior are specified in the runtime/distribution contracts
and remain to be implemented/tested.
Compensation belongs to the original finite archaeological reward, not separately
to every copied pending map; prevent map-plus-compensation double claims or copy/
reload payouts. A mined/damaged known site is not automatically a missing
destination or permission to create a replacement.

## Historical milestones and original implementation baseline

**Archive boundary:** everything in the following original sections 1–11 describes
the pre-Alpha-4 milestone plan and evidence at its recorded dates. Statements such
as "current Alpha 3", the two-structure scope, old dependency versions, obsolete
candidate spacings and no-building access criteria are **not current instructions**.
Use the current planning/closure sections above, README/catalog and dated Alpha 4.9
reports for present status. Preserve the historical failures and inventory; do not
reinterpret them as gameplay test results or re-run old modeling tasks.

**Design priority update, October 2, 2026:** the user has visually accepted
Colossus V4.1, Obelisk V4.2 and all four Titan Skull V4 ground variants. Create
the other planned relics before V5 interior architecture. The remaining original
motifs are the Ruined Tower and World Tree; the smaller Colossus is a separate
direction based on the archived first concept. Following the reference studies,
the user requested [V1s for all four new designs](NEW_RELICS_V1.md), including
sword-bearing Titan Skull 2. These exports now await visual review.
This does not close worldgen or in-game checks.

**Occurrence and review update, October 2, 2026:** one naturally generated large
Colossus per game world/save, shared by all players; smaller Colossi may occur
multiple times. Alpha 3 does not yet enforce this rule. The
[lore/gameplay review](LORE_GAMEPLAY_REVIEW.md) records material economy, trial
history, visible lore links, lasting core value, multiplayer reward access, and
discovery effort as open design tasks, not implemented fixes.

**Alpha 3 update:** the three V3 exports are now selected for the visual test
build. See [V3 integration](../technical/V3_INTEGRATION.md). The Alpha 2 evidence
and planning baseline below remain historical; final gameplay/interiors and
broader acceptance are still pending.

Updated: October 2, 2026.

This is the implementation and acceptance plan for version 0.1. **The current
visual test build was 0.1.0-alpha.3 for Minecraft 26.2 / Fabric 0.19.5**, selecting
the three V3 exports with natural worldgen. The procedural Alpha 2 architecture,
dimensions, phases, and evidence below remain a historical planning baseline
where not explicitly superseded by the updates and linked V3 integration report.
Accepted V4 studies, unique-site generation, and custom gameplay are not yet
integrated. Completing individual checks does not satisfy every acceptance
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
| Reproducible build | Python resource packaging; Alpha 4.2 adds JDK 25 placement-only compilation |
| Full personal modpack and custom configs | Not fully accepted; integration tests used a selected default-config subset |
| World preset, extra datapacks, graphics, shaders/LOD | Must be recorded for broader acceptance |
| Test hardware, JVM memory, storage, performance baseline | Must be fixed before comparative measurements |

Do not commit credentials, account data, personal saves, or third-party mod JARs.
Additional loaders and game versions should follow a working first release.

## 3. Architecture

| Layer | Current responsibility |
| --- | --- |
| Mod packaging | Fabric metadata/resources and Alpha 4.2 placement-only Java components |
| Structure sources | Procedural alpha geometry and separate Blender source generators |
| Worldgen data | Biomes, rigid template pools, distribution, and placement conditions |
| Lithostitched | Delegating structure type, grid/height/biome conditions, and jigsaw placement |
| Development tools | Conversion, manifests, export checks, previews, settings packs, and server/world verification |
| Custom runtime code | Alpha 4.2 terrain supports and non-overlap reservations address demonstrated data-only placement gaps; no gameplay code |

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

These areas already exist. Alpha 4.2 adds `src/main/java/` for small placement-only
components and `src/test/java/` for their headless tests; see
[the terrain correction](../technical/ALPHA_4_2_TERRAIN.md). Local worlds and
runtime data remain outside tracked sources. Reference media is not shipped with the mod.

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

The first Blender experiment remains separately reproducible at 99 × 66 × 71 in
[`relics/colossus/archive/first-concept/`](../../relics/colossus/archive/first-concept/).
It is preserved as the basis for a future second, smaller Colossus.
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

### Future contract: unique large site and repeatable smaller sites

The large Colossus must have **one natural site per save/server in the Overworld**,
not one per player, region, or density preset. Smaller Colossi may have several
natural sites; their distribution and loot remain separate decisions. Existing
Alpha 3 structure sets do not enforce uniqueness, and increasing spacing alone
does not meet this contract.

Before implementation, choose and validate how to resolve a single suitable site
consistently from the seed/generator, preserve its identity across save/load and
exploration, and expose it to `/locate` and expedition maps. Maps initially share
that destination, including when its chunks have not been explored; a rejected
candidate or an extra structure created for a map is not acceptable.

Define search distance/cost limits and behavior for no valid site, disabled
generation, or existing alpha saves containing multiple large starts. Decide
compatibility/configuration semantics explicitly; do not delete existing relics
or silently generate a replacement after shared loot is taken or the landmark is
mined. This records requirements and open edge cases, not a chosen runtime design.

Future acceptance must cover multiple seeds, chunk exploration orders, integrated
and dedicated servers, simultaneous discovery, reloads, configuration changes,
and maps from different Obelisks. Confirm at most one natural large start and a
valid destination in supported enabled worlds; also verify that smaller Colossi
can repeat without inheriting the large site's loot by accident.

### Discovery and multiplayer follow-up

Candidate spacing is not actual search time. The review's 64/80-chunk baseline
means about 36% fewer Colossus candidates per area under equal assumptions, not
proof of the desired discovery hierarchy. Measure repeatable-family candidates,
rejections, placements, and travel/search effort. For the unique large site,
measure reachability and map-assisted discovery separately from density.

Before final loot distribution, test later arrivals at the same landmark, vault
eligibility persistence and player-history limits, shared magnet depletion, and
archaeology/map availability. Per-player core eligibility is intended; infinite
vanilla-vault memory or per-player chest/archaeology behavior is not assumed.
These checks are future gates, not claims made by the Alpha 3 test report.

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

## Current next work — supersedes the historical section 11

1. Await a separate gameplay implementation request; no code/assets/generation
   changes are included in this documentation push.
2. Prove safe deterministic terrain planning, one-golem lifecycle, durable Vault
   claims and the natural animal-spawn hook in isolated 26.2 tests.
3. Implement item components/furnace/magnet/recipes and original artwork following
   the runtime contract, without another major gameplay design round.
4. Receive builder sidecars/revised versioned exports, validate hashes/transforms
   and integrate only the selected Colossus/Obelisk/Tower/Tree changes. Leave skulls alone.
5. Implement shared natural-site/claim/map state and run the gameplay acceptance
   plan. Survival tuning and target-version evidence are release gates, not completed work.
