# Lore and gameplay review — design follow-up

Recorded: October 2, 2026. This records the user's review and the resulting open
design tasks. Suggestions below are **not approved material replacements, recipe
changes, or implemented systems**.

## Review baseline and current status

The supplied review examined commit `9a4a87f`: V3 assets existed but were not yet
selected in the playable alpha. Alpha 3 now integrates Colossus, Obelisk, and
Titan Skull V3. Colossus V4.1, Obelisk V4.2, and the four Skull V4 ground variants
have since been visually accepted offline; their integration remains pending.
Custom items, trials, archaeology, and expedition maps are still planning.

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
- Uniqueness is **not implemented** in Alpha 3. Reliable selection of one valid
  site, persistence, searches/maps, and handling existing alpha worlds remain
  technical design and acceptance work. Do not create additional large Colossi
  simply because a map needs a destination or a player has already looted one.

## 1. Material economy: landmark versus mine

The review reports **141,523 copper-based blocks and 5,609 raw iron blocks** in
the V3 Colossus. These counts were rechecked against its tracked whole NBT export
on October 2, 2026. They are placed-block counts, not a calculation of obtainable
ingots; actual recovery depends on block types and survival mechanics.

Concern: mining the monument could dwarf its carefully limited special rewards
and encourage dismantling a unique shared landmark. Uniqueness limits the number
of deposits but does not remove this incentive or the multiplayer impact.

Suggested direction: concentrate useful metal in deliberate salvage areas and
represent large surface fields with economically less significant materials.
No replacement palette, block protection, or restriction on normal mining has
been selected. The visually accepted warm metal design remains intact for now.

**Follow-up:** inventory the selected export, estimate survival salvage value,
compare it with intended rewards, and decide the material/salvage policy before
final loot tuning. Owner: [Colossus design goals](../../relics/colossus/docs/COLOSSUS_V4.md)
and [gameplay](../../relics/colossus/gameplay/ITEMS.md).

## 2. Give the golem trial a historical function

An inactive wreck with an iron-golem trial needs a legible reason for that local
mechanism. Residual security, maintenance machinery, and a later installation
are alternatives, **not selected explanations**.

The current player-initiated fight makes the golem retaliate; it is not an active
guard preventing entry. Do not present it as such without matching behavior.

**Follow-up:** choose its historical function internally, then derive the room,
activation cues, key, and reward presentation from it. Keep the rest of the
Colossus inactive. Current golem/key/vault flow remains approved; custom aggression
or a replacement enemy is not authorized. Owner: [head trial](../../relics/colossus/gameplay/ITEMS.md).

## 3. Make the shared past visible in discoveries

A damaged machine and a skull alone do not clearly demonstrate the Titan
conflict. Possible connection traces include a machine fragment lodged in bone,
matching damage on the machine, or recurring marks of later expeditions.
These are proposals, not already modeled details or fixed canon.

**Follow-up:** select a small, consistent set of visible links across appropriate
sites. Decide internally whether Obelisks were primarily wayfinders or markers
of destroyed Titans, then derive their spatial clues. Players can remain
uncertain even when the design team has a consistent interpretation. Later
researchers' expedition maps remain a plausible explanation without requiring
the ancient builders to have created the maps. Owners: [lore bible](LORE-BIBLE.md),
[Skull gameplay](../../relics/titan-skull/gameplay/README.md), and
[Obelisk gameplay](../../relics/obelisk/gameplay/README.md).

## 4. Define the core's lasting everyday value

The initial **256 completed operations equal the nominal fuel output of 32 coal**.
The distinctive benefits are reuse, retained charge, and no idle drain, not speed
or unlimited energy. A unique expedition, head ascent, trial, possible restoration,
and recurring recharge cost could outweigh that convenience.

**Follow-up:** define the daily problem the core solves, then tune capacity,
restoration, and charging costs together. Test ordinary use and hopper workflows.
The review does not itself approve a capacity increase, a recipe, a speed boost,
or free fuel. Owner: [Machine Core](../../relics/colossus/gameplay/ITEMS.md).

## 5. Multiplayer rewards have different depletion rules

The planned core vault is per-player; the magnet's copper chest is shared and
finite. Archaeology finds and maps have no finalized distribution rule. At the
unique large site, a later visitor cannot seek another naturally generated large
arm to replace a claimed magnet.

**Follow-up:** define later-visitor access for magnet, ordinary salvage, archaeology,
collectibles, and maps **before final loot distribution**. Consider group discovery
and late arrivals. A per-player chest, replenishment, and smaller-Colossus magnet
loot are possible future decisions, not approved fixes. Owners:
[Colossus gameplay](../../relics/colossus/gameplay/ITEMS.md) and
[Obelisk gameplay](../../relics/obelisk/gameplay/README.md).

## 6. Measure discovery effort, not only spacing

The baseline uses 64-chunk Obelisk and 80-chunk Colossus spacing. Under the same
random-spread assumptions, the latter yields approximately **36% fewer candidates
per area** (`1 - (64 / 80)^2`), not proof of a large difference in actual discovery
time. Biome eligibility and terrain rejection matter substantially.

With the new rule, the large Colossus is no longer a density-tuned repeatable
family. Its challenge is reaching a **single valid destination**, directly or
with a map; repeatable smaller Colossi need their own eventual frequency target.

**Follow-up:** measure search effort across seeds, with/without maps; check target
validity, repeated destinations, distance/fallback behavior, and search cost.
Do not mistake repeated maps to the unique landmark for access to fresh shared
loot. Owner: [technical implementation plan](UMSETZUNGSPLAN.md).

## Preserve these distinctions and priorities

- Skulls do not need an exclusive item.
- Obelisks remain solid, exterior archaeological monuments.
- Maps aid discovery without enforcing a mandatory relic order.

The review recommends **material economy first, historical trial integration
second, and lasting core utility third**. Record these as design-review priorities;
they do not override the agreed next modeling order or authorize changing accepted
models, implementing gameplay, or altering generation now.
