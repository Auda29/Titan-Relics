# Lore and gameplay review — design follow-up

Recorded: October 2, 2026. Updated: October 8, 2026. This records the user's review and the resulting open
design tasks. Original review suggestions are not approvals in themselves;
subsequent decisions are recorded explicitly below. Material B is selected and
integrated; the cockpit defense-robot history and cleared-territory Obelisk role
are approved. Recipes/reward policies are selected; authored coordinates,
implementation and runtime evidence remain deliverables. The
[planning closure](GAMEPLAY_PLAN_REVIEW.md) and
[runtime defaults](../technical/GAMEPLAY_RUNTIME.md) distinguish those from unanswered gameplay.

## Review baseline and current status

The supplied review examined commit `9a4a87f`: V3 assets existed but were not yet
selected in the playable alpha. Alpha 4.9 now integrates seven designs/ten variants,
including Colossus V4.1 materials B, Obelisk V4.2 and crowned Skull V4.
The [Colossus material study B](../../relics/colossus/docs/COLOSSUS_MATERIAL_STUDY_B.md)
is the selected material version of V4.1, including its simulated post-salvage
appearance. It is packaged and visually integrated in Alpha 4.9; actual recovery
value and balance against future special rewards remain open. This is a separate decision
from the earlier B / open-chest-frame geometry choice.

Custom items, trials, archaeology, and expedition maps are still planning.
The golem's original role is now a **cockpit defense robot in a crewed machine**.
Its present activation/encounter and multiplayer reward rules are selected; the
core's final survival balance and one-large-site implementation remain unproven.

The review's quantities describe **V3**, not measurements of the accepted V4
studies. Its candidate rates are not final discovery balance. The newly approved
unique-large-Colossus rule also supersedes the review's repeatable-large-site
assumption. See [V3 integration](../technical/V3_INTEGRATION.md).

## Approved addition: one large Colossus per world

- The **large Colossus is a unique natural site: one per game world**, not merely
  a structure with very wide spacing. This applies to a whole save/server, not
  separately to each player or region; its intended dimension is the Overworld.
- Planned **smaller Colossi may occur multiple times**. Their frequency and loot
  are separate decisions; they do not automatically inherit the large site's
  Machine Core trial or special items.
- Preserve per-player eligibility at the large site's vault so later multiplayer
  visitors can obtain the core at the same landmark. Verify the actual target-game
  behavior rather than assuming a vanilla vault guarantees unlimited participation.
- Obelisk expedition maps initially lead to this same unique large site. Repeated
  destinations are therefore expected, not evidence of a failed variant search.
- Uniqueness is **not implemented** in Alpha 4.9. Reliable selection of one valid
  site, persistence, searches/maps, and handling existing alpha worlds remain
specified technical implementation and acceptance work. Do not create additional large Colossi
  simply because a map needs a destination or a player has already looted one.

## 1. Material economy: landmark versus mine

**Historical study A — superseded by B:** the user requested limited salvage with complete form
preservation. The [Colossus material study](../../relics/colossus/docs/COLOSSUS_MATERIAL_STUDY.md)
now compares accepted V4.1 against a direct block remap, retaining 197 copper and
10 raw iron blocks. All 223,161 occupied positions are identical. This is an
historical candidate, not the selected material version or final gameplay balance.

**Revised direction:** after reviewing the initial study, the user requested
substantially more copper and visible but plausible mining damage: fewer than
50,000 copper blocks, fewer than 256 raw iron items. [Study B](../../relics/colossus/docs/COLOSSUS_MATERIAL_STUDY_B.md)
retains 25,423 copper blocks and 90 raw iron items. Its intact shape is identical;
after complete metal removal the head remains attached to the buried torso and
no surviving original face-connected component splits. The user visually accepted
study B and its post-salvage appearance on October 2, 2026; it is the selected
material version and is integrated in Alpha 4.9. Offline post-mining connectivity
checks remain distinct from final survival-economy/gameplay acceptance.

The review reports **141,523 copper-based blocks and 5,609 raw iron blocks** in
the V3 Colossus. These counts were rechecked against its tracked whole NBT export
on October 2, 2026. They are placed-block counts, not a calculation of obtainable
ingots; actual recovery depends on block types and survival mechanics.

Concern: mining the monument could dwarf its carefully limited special rewards
and encourage dismantling a unique shared landmark. Uniqueness limits the number
of deposits but does not remove this incentive or the multiplayer impact.

**Original recommendation, now addressed by selected study B:** concentrate useful
metal in deliberate salvage areas and represent large surface fields with
economically less significant materials. B's palette and stated inventory are
approved as the asset choice; the earlier "no replacement palette selected"
status is superseded. Normal mining remains allowed. Existing worldgen-feature
protection does not prevent player mining; no indestructible-landmark mechanism
has been selected.

**Remaining follow-up:** plan/test playable interior access and actual recovery
value in Minecraft, and compare salvage with special rewards before final
survival/loot tuning. B's material selection and build integration are
settled; its gameplay balance is not. Owner: [Colossus design goals](../../relics/colossus/docs/COLOSSUS_V4.md)
and [gameplay](../../relics/colossus/gameplay/ITEMS.md).

## 2. Give the golem trial a historical function

**Original review concern:** an inactive wreck with an iron-golem trial needed a
legible reason. **October 8 decision:** all Colossi were crewed; the large machine's
head was its cockpit and the golem was its **defense robot**. Maintenance machinery
and later-installation alternatives are superseded, not competing active options.

**Earlier encounter plan — superseded:** the golem only retaliated after a player
struck it. The user now prefers **autonomous attacks** for the designated cockpit
defense golems. Targeted Fabric AI/runtime code can support this; spawner data alone
does not guarantee it. Ordinary golems must retain normal behavior.

**Remaining follow-up:** derive the cockpit layout, present-day activation cues,
key and reward presentation from that selected role. Explain how/why the robot
can still function if needed without inventing a cause yet. Keep the rest of the
Colossus inactive. The golem/key/vault flow remains approved, now including scoped
autonomous aggression as a planned requirement. Automatic trial-spawner activation
is selected, without a console; detection/range/reset/player-mode defaults are
specified in the runtime contract and need testing. The documentation gate is
closed; implementation awaits a separate request and builder deliverables;
no replacement enemy is selected. Owner: [head trial](../../relics/colossus/gameplay/ITEMS.md).

**Interior scope selected October 8:** retain the large body cavity and develop
mainly its five-operator cockpit. Operators were near player scale, perhaps a
little larger; smaller companions had two and now have enterable ruined interiors
with cockpits effectively absent, explained by weaker original materials. The
large hatch is the intended entrance, reached through player-found/built ascent;
an authored ground-to-head stairway is not required. Exact hatch, stations and
encounter positions are still planning.

## 3. Make the shared past visible in discoveries

A damaged machine and a skull alone do not clearly demonstrate the Titan
conflict. Possible connection traces include a machine fragment lodged in bone,
matching damage on the machine, or recurring marks of later expeditions.
These are proposals, not already modeled details or fixed canon.

**Follow-up:** select a small, consistent set of visible links across appropriate
sites. **October 8 decision:** Obelisks marked territories cleared of Titans by
the Colossi; skulls are spread across their broad surroundings. The tower was the
unfinished organizing base; the World Tree was worshipped by Titans, gave them
strength/size, and survived the builders' attempt to destroy it. All now belong
to the same ancient conflict. Regional distances and placement rules are selected;
realized density needs evidence. Visible worship/attack traces are optional later
art, not a required rebuild (especially not at the skulls). Later
researchers' expedition maps remain a plausible explanation without requiring
the ancient builders to have created the maps. Owners: [lore bible](LORE-BIBLE.md),
[Skull gameplay](../../relics/titan-skull/gameplay/README.md), and
[Obelisk gameplay](../../relics/obelisk/gameplay/README.md).

## 4. Define the core's lasting everyday value

The initial **256 completed operations equal the nominal fuel output of 32 coal**.
The distinctive benefits are reuse, retained charge, and no idle drain, not speed
or unlimited energy. A unique expedition, head ascent, trial,
and recurring recharge cost could outweigh that convenience.

**Follow-up:** define the daily problem the core solves, then tune capacity,
and charging costs together. The user now selects a **fully charged, immediately
usable Vault core**; initial restoration/cost is superseded. Test ordinary use and
hopper workflows.
The user has also selected a **shaped crafting-table recharge**: depleted core in
the middle, coal blocks left/right, one amethyst shard above, yielding one fully
charged core. The two coal blocks alone supply 160 operations; the provisional
256-operation core adds 96 (60%) in exchange for the shard and acquisition effort.
The review does not itself approve a capacity increase, speed boost or free fuel.
Recipe state handling/balance still need testing. Owner:
[Machine Core](../../relics/colossus/gameplay/ITEMS.md).

## 5. Multiplayer rewards have different depletion rules

The planned core vault is per-player; the magnet's copper chest is shared and
finite. **Obelisk archaeology is now shared and finite**, including its selected
cosmetic armor-trim template and expedition map. Later players may seek another
Obelisk or copy/share recovered maps. Template duplication now follows the vanilla
principle: one template + seven diamonds + one copper block yields two templates.
The motif uses angular geometric Obelisk forms, with exact artwork open. At the
unique large site, a later visitor cannot seek another naturally generated large
arm to replace a claimed magnet.

**Follow-up:** finalize loot layouts/quantities, exact trim artwork/application and remaining
ordinary-salvage access **before final loot distribution**. Consider group discovery
and late arrivals. **Rare percentage-based magnet loot in repeatable smaller
Colossi is now selected** as an additional acquisition path, not a guaranteed
per-player reward. The approved starting target is **10% per site for one broken
magnet requiring repair**, with exact position/container open. Magnet full repair
at a crafting table uses the existing magnet, four iron ingots and one amethyst
shard instead of the proposed two redstone. Crafting/state handling and balance
still need validation.
Per-player chests and replenishment are not selected. Owners:
[Colossus gameplay](../../relics/colossus/gameplay/ITEMS.md) and
[Obelisk gameplay](../../relics/obelisk/gameplay/README.md).

## 6. Measure discovery effort, not only spacing

The historical review baseline used 64-chunk Obelisk and 80-chunk Colossus spacing. Under the same
random-spread assumptions, the latter yields approximately **36% fewer candidates
per area** (`1 - (64 / 80)^2`), not proof of a large difference in actual discovery
time. Biome eligibility and terrain rejection matter substantially.

With the new rule, the large Colossus is no longer a density-tuned repeatable
family. Its challenge is reaching a **single valid destination**, directly or
with a map; repeatable smaller Colossi now have a 2% shared-opportunity starting target.

**Follow-up:** measure search effort across seeds, with/without maps; check target
validity, repeated destinations, distance/fallback behavior, and search cost.
The user has selected keeping distant valid targets, an explicitly unconfirmed
map state for transient unresolved targets, and three emeralds instead of the map
for genuinely unavailable targets, with the trim reward retained. Implement/test
retry/claim handling without compensation per copied map or substitute structures.
Do not mistake repeated maps to the unique landmark for access to fresh shared
loot. Owner: [technical implementation plan](UMSETZUNGSPLAN.md).

## Preserve these distinctions and priorities

- Skulls do not need an exclusive item.
- Obelisks remain solid, exterior archaeological monuments.
- Maps aid discovery without enforcing a mandatory relic order.

The review recommends **material economy first, historical trial integration
second, and lasting core utility third**. Record these as design-review priorities;
they do not override the agreed next modeling order or authorize changing accepted
models, implementing gameplay, or altering generation now. The later selection
of material study B addresses the asset-choice portion of the first priority,
not its outstanding survival-balance checks. The October 8 lore addresses the
historical-function portion of the second priority, not the cockpit/activation
layout or implementation. The all-relic documentation/consistency review is complete;
gameplay/interior implementation on 26.2/Fabric still needs a separate request,
builder exports and the new acceptance matrix. Historical review suggestions do
not override the resulting decisions or authorize optional conflict-trace rebuilds.
