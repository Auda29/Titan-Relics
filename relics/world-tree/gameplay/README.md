# World Tree gameplay planning

Updated: October 8, 2026. V4.3 strands and Alpha 4.9 terrain integration are visually
accepted. No loot or authored encounter system is decided by that acceptance.

## Approved lore

The Titans **worshipped the World Tree and received their strength and size from
it**. The Colossi's builders tried to destroy it, **but failed**. The conflict is
thousands of years old and no living Titans remain. Current Minecraft mobs and
players now inhabit or otherwise reuse the relics.

The tree's creation and the exact mechanism of its ancient power remain unknown.
This history does not automatically grant players growth/strength effects, a
revival mechanic, a boss, or a quest to destroy the tree. It does not establish
the form of a sanctuary, a battle scar or a settlement beneath its roots.

## Interior and gameplay decisions still needed

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
Exact multiplier, local area and target-version hook remain to be tuned/validated.
Other ordinary mob behavior remains natural as at the Tower; do not add a hostile
roster, hostile spawn-rate override, barrier or automatic despawn. Planned lighting
is the selected means of reducing darkness-dependent hostile spawning.

**The beneficial effect is reward enough.** No loot chest, exclusive Tree item or
additional reward encounter is selected.

### Approved effect starting values: Regeneration I around the trunk

The user approved these **provisional starting values**:

- **Regeneration I**, concentrated around the trunk.
- An approximately **24-block radius** around the trunk; exact reference point
  and horizontal/vertical volume still need specification.
- The effect **refreshes while the player stays in range** and lasts about
  **five minutes after leaving**. No interaction/payment is selected.

These values require survival/combat balance testing, not an invented final effect
bundle. Additional effects are not selected. Decide refresh cadence, stacking with
beacons/other sources and multiplayer behavior. "Beacon-style" describes
the beneficial effect, not a selected literal beacon block, pyramid, beam, mineral
payment or all beacon powers at once. The historical Titan link does not make
visitors Titans or authorize revival/growth. No permanent/global benefit is chosen.

### Approved lighting palette and placement scope

- Use **glow berries, glow lichen and firefly bushes** (the user's glowing-grass/
  firefly reference), supplemented by **sparse shroomlights** as natural-looking
  luminous fungal growth around the trunk/roots. Exact block positions/amounts
  remain planning. Amethyst clusters remain an optional proposal, not a mandatory
  addition; sea pickles, brown mushrooms and froglights are not selected by default.
- **Illuminate only the trunk/base and root area, not upper branches or the crown.**
  The previously suggested lights in branch forks are superseded by this limit.
- Luminous growth may reach **at most 15 blocks up the trunk from its ground-level
  base**, with varied heights and a natural taper. This is a maximum, not a uniform
  15-block band or a requirement to cover every side to the same height.
- At ground level, the growth/light sources should spread **broadly around the
  trunk and along/between the roots**, paying attention to dark areas beneath the
  canopy. Use irregular clusters/gaps, not equal spacing, a perfect ring or blanket
  coverage. Exact horizontal extent remains open; the effect's 24-block radius is
  not automatically a lighting boundary.
- Light coverage should reduce darkness-dependent hostile spawning beneath the
  canopy. Validate actual in-game light/spawn conditions when this is implemented;
  decorative glow/firefly visuals alone are not reliable coverage or a guarantee
  of total safety. No new repulsion/despawn or universal spawn-blocking system is
  implied by this placement direction. Use the vanilla firefly-bush block/visuals,
  not an invented firefly mob.

Specify how the effect identifies
the natural relic and behaves if it is modified/damaged; ordinary copies of its
lights or wood must not be assumed to create new aura sites automatically.

### Remaining decisions

- Whether and how former Titan worship or the failed destruction attempt is visible.
- Root-level exploration, sheltered spaces, access and any later inhabitants.
- Exact placement/quantity and ground-level spread of glow berries, glow lichen,
  firefly bushes and sparse shroomlights within the trunk/root-only, maximum
  15-block-height scope; whether optional amethyst clusters are wanted.
- Exact aura reference point/vertical volume, refresh cadence, effect stacking
  and multiplayer behavior; tune the approved Regeneration I / 24-block radius /
  five-minute post-departure values without treating them as final balance.
- Modest natural-spawn adjustment/density/area for the selected pigs, chickens,
  sheep and cows, respecting normal population/terrain limits and no spawners.
  Lighting coverage and outside hostile arrivals remain distinct from animal spawning.
- Site frequency/uniqueness and relationships to other relics.

First gameplay target is 26.2/Fabric. Finish the all-relic plans and consistency
review before implementation. Shared history: [lore bible](../../../docs/project/LORE-BIBLE.md).
