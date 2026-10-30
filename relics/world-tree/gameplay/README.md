# World Tree gameplay planning

> **Current status, October 30, 2026:** The selected gameplay is released; current models, implemented values, evidence and remaining tuning are recorded centrally. See the
> [Alpha 5.0.3 status and roadmap](../../../docs/project/CURRENT_STATUS_AND_ROADMAP.md). Approved design requirements
> remain specifications; dated pending/unimplemented claims below are historical
> where superseded by the released implementation and linked evidence.

Updated: October 8, 2026. V4.3 strands and Alpha 4.9 terrain integration are visually
accepted. No loot or authored encounter system is decided by that acceptance.
The gameplay round is complete; [runtime defaults](../../../docs/technical/GAMEPLAY_RUNTIME.md)
and [builder marker contract](../../../docs/technical/GAMEPLAY_MARKERS.md) specify
technical behavior separately from user approvals. None is implemented yet.

## Approved lore

The Titans **worshipped the World Tree and received their strength and size from
it**. The Colossi's builders tried to destroy it, **but failed**. The conflict is
thousands of years old and no living Titans remain. Current Minecraft mobs and
players now inhabit or otherwise reuse the relics.

The tree's creation and the exact mechanism of its ancient power remain unknown.
This history does not automatically grant players growth/strength effects, a
revival mechanic, a boss, or a quest to destroy the tree. It does not establish
the form of a sanctuary, a battle scar or a settlement beneath its roots.

## Approved gameplay and remaining builder deliverables

### User direction: luminous, restorative refuge

The user wants the tree to represent a **peaceful source of life**, with natural-
looking lighting and a restorative atmosphere. **Animals are welcome and should
occur more frequently; hostile mobs should spawn rarely or not at all.** This
supersedes "all mobs excluded" readings. Species and no-spawner policy are selected
below; exact local density/adjustment still requires tuning.

Lighting can help suppress darkness-dependent spawning but does not exclude all
spawn types or prevent hostile arrivals from outside. Suppression of local spawning
is a direction, not a selected despawn, barrier, repulsion or invulnerability system.
Do not guarantee complete safety against raids, outsiders or player actions.

**Latest animal/spawn clarification:** increase the presence/natural spawning of
**pigs, chickens, sheep and cows**. **No animal spawners or rapid guaranteed
replenishment**: this is a living refuge, not a farm engine. Integration should use
a modest locally scoped natural-spawn adjustment with normal spawn conditions and
population limits, not timer-based entity injection or cap-bypassing replenishment.
The delegated runtime baseline permits at most one extra ordinary selected-species
attempt per eligible local vanilla creature attempt within 64 horizontal blocks
of the saved anchor. The native hook is implemented and cap-tested. Actual
density depends on ordinary habitat and population conditions, not a guaranteed
herd or independent refill timer.
Other ordinary mob behavior remains natural as at the Tower; do not add a hostile
roster, hostile spawn-rate override, barrier or automatic despawn. Planned lighting
is the selected means of reducing darkness-dependent hostile spawning.

**The beneficial effect is reward enough.** No loot chest, exclusive Tree item or
additional reward encounter is selected.

### Approved effect starting values: Regeneration II and Resistance II around the trunk

The user approved these **provisional starting values**. On October 28 the
user increased the radius first to 50 and then to **80 blocks**:

- **Regeneration II and Resistance II**, concentrated around the trunk.
- A **sphere with an 80-block radius** around a **builder-supplied fixed anchor at
  the trunk base**; use three-dimensional distance, not an unlimited-height cylinder.
  The exact template-relative anchor remains to be supplied.
- **No line-of-sight requirement:** the aura works through wood, walls and terrain
  everywhere inside this sphere, including root caves/buildings. Only distance to
  the saved anchor determines spatial inclusion; block obstruction is not a filter.
- The effect **refreshes while the player stays in range** and lasts about
  **five minutes after leaving**. No interaction/payment is selected.

These values require survival/combat balance testing, not an invented final effect
bundle. The user selected both level-II effects on October 28; other effects are not selected. The technical baseline refreshes
every 20 ticks to 6,000 ticks, with normal effect merging and independent player
checks, without downgrading stronger/longer effects. "Beacon-style" describes
the beneficial effect, not a selected literal beacon block, pyramid, beam, mineral
payment or all beacon powers at once. The historical Titan link does not make
visitors Titans or authorize revival/growth. No permanent/global benefit is chosen.

### Approved lighting palette and placement scope

- Use **glow berries, glow lichen and firefly bushes** (the user's glowing-grass/
  firefly reference), supplemented by **sparse shroomlights** as natural-looking
  luminous fungal growth around the trunk/roots. Exact block positions/amounts
  remain planning. Instead of scattered optional amethyst clusters, the user selected
  **one small amethyst sphere inside the trunk at its bottom/base**. Exact size,
  composition and visibility/access are builder details. The sphere is **decorative
  and normally mineable**, using ordinary amethyst blocks and optionally individual
  crystals, **without budding amethyst or regrowing crystals**. It is not a renewable
  amethyst source and does not control the persistent aura. Sea pickles, brown mushrooms
  and froglights are not selected by default.
- **Illuminate only the trunk/base and root area, not upper branches or the crown.**
  The previously suggested lights in branch forks are superseded by this limit.
- Luminous growth may reach **at most 15 blocks up the trunk from its ground-level
  base**, with varied heights and a natural taper. This is a maximum, not a uniform
  15-block band or a requirement to cover every side to the same height.
- At ground level, the growth/light sources should spread **broadly around the
  trunk and along/between the roots**, paying attention to dark areas beneath the
  canopy. Use irregular clusters/gaps, not equal spacing, a perfect ring or blanket
  coverage. Exact horizontal extent remains open; the effect's 80-block radius is
  not automatically a lighting boundary.
- Light coverage should reduce darkness-dependent hostile spawning beneath the
  canopy. Validate actual in-game light/spawn conditions when this is implemented;
  decorative glow/firefly visuals alone are not reliable coverage or a guarantee
  of total safety. No new repulsion/despawn or universal spawn-blocking system is
  implied by this placement direction. Use the vanilla firefly-bush block/visuals,
  not an invented firefly mob.

**Approved damaged-site policy:** the regeneration aura belongs to the **registered
natural site's original location** and remains there even if players heavily
damage or completely remove the Tree. Normal mining is allowed; no block protection,
automatic rebuilding or new aura from relocated wood/lights is selected. Persist
the original aura anchor independently of remaining Tree blocks. Ordinary player-built
copies do not create additional aura sites. Technical natural-site identification
and save/load behavior still need implementation/validation.

### Remaining implementation and builder evidence

- Existing root-level exploration remains the baseline; no new settlement or
  attack/worship trace is required. Such optional art would need separate review.
- Exact placement/quantity and ground-level spread of glow berries, glow lichen,
  firefly bushes and sparse shroomlights within the trunk/root-only, maximum
  15-block-height scope, plus builder design/anchor for the selected small internal
  amethyst sphere at the trunk base.
- Exact builder-supplied aura anchor and runtime validation of refresh/effect merging
  and multiplayer behavior; tune the approved Regeneration II and Resistance II / 80-block radius /
  five-minute post-departure values without treating them as final balance.
- Validate the specified modest natural-spawn adjustment for the selected pigs, chickens,
  sheep and cows, respecting normal population/terrain limits and no spawners.
  Lighting coverage and outside hostile arrivals remain distinct from animal spawning.
- Validation of the selected repeatable-site frequency and relationships to other relics.

**Approved distribution starting value:** **2% per shared repeatable-relic opportunity**,
inside or outside Obelisk regions, equal to Tower and small Colossi. This replaces
the assistant's 1% proposal; empty opportunities become 34% inside / 59% outside
under the current budget. It is not a per-chunk roll, guaranteed site count or
world-wide cap; the Tree remains repeatable.

First gameplay target is 26.2/Fabric. The documentation gate is closed by the
[planning review](../../../docs/project/GAMEPLAY_PLAN_REVIEW.md); a separate
implementation request and runtime acceptance are still required. Shared history:
[lore bible](../../../docs/project/LORE-BIBLE.md).
