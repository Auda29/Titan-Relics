# Gameplay runtime — implementation starting contract

> **Current status, October 30, 2026:** The released baseline supports Fabric and NeoForge on 26.2 and 1.21.1. See the
> [Alpha 5.0.3 status and roadmap](../project/CURRENT_STATUS_AND_ROADMAP.md). Approved design requirements
> remain specifications; dated pending/unimplemented claims below are historical
> where superseded by the released implementation and linked evidence.

Prepared: October 8, 2026. **Planning only, for Minecraft 26.2 / Fabric first.**
No Java gameplay, resources, item artwork, marker loader or generation changes
are implemented by this document. Existing 1.21.1 visual-alpha artifacts remain
preserved; gameplay backport support is not selected.

**October 27 implementation update:** natural initialization of the approved
interiors, native Trial/Vault presentation and personal world reward drops are
implemented. Successful Vault use consumes its key immediately. A charged magnet
works in either selected hand, with acceleration `0.088` and speed cap `0.385`;
other inventory slots remain inactive. These implemented values supersede the
starting values below. The Tree animal adjustment is implemented and cap-tested
for Alpha 5.0; see section 7.
See [current status and remaining acceptance](../project/ALPHA_5_STATUS_20261027.md).
The original contract below remains as planning history.

## 1. Authority, owners and starting values

**Subsequent implementation status:** the user authorized a separate gameplay
worktree. Standalone item/resource code and opt-in runtime adapters now exist in
`feat/gameplay-items-runtime`, subsequently integrated into `main` alongside the
builder candidates; see [evidence and remaining gates](../testing/GAMEPLAY_IMPLEMENTATION_20261008.md).
This document retains the approved starting contract, not a claim that all its
natural integration/recovery/runtime acceptance gates have passed.

User decisions are authoritative in the [shared implementation plan](../project/UMSETZUNGSPLAN.md)
and per-relic gameplay documents. **Engineering defaults below are delegated
assistant starting choices**, to be validated/tuned rather than misreported as
user-specified numbers. The builder owns structure/interior changes and actual
coordinates; this work owns integration, mechanics, recipes and item artwork.

| System | Starting technical choice |
| --- | --- |
| Item stacks | Core and magnet: maximum stack size 1; key: 64; store item state in versioned persistent components, not names/lore text |
| Core capacity / magnet durability | 256 operations / 1,000 individually collected items; large arm starts with full magnet durability |
| Item icon thresholds | Full at capacity, partly used at `0 < remaining < capacity`, empty/broken at zero; exact values in tooltip; **no inventory bar** |
| Trial player registration | Survival/Adventure only, 14-block spawner detection radius and ordinary vanilla visibility checks; automatic, no console |
| Trial population | One normal iron golem, simultaneous/total count 1, all additional-player count increments zero; no stat scaling or ominous replacement |
| Trial cooldown | Vanilla-style 36,000 server ticks (30 minutes) after completion; adapter must verify 26.2 lifecycle behavior |
| Magnet scan / motion | Scan eligible nearby items every 4 server ticks, with collision/pickup recheck before each pull; acceleration target 0.08 blocks/tick per tick, speed cap 0.35 blocks/tick |
| Tree effect refresh | Every 20 server ticks; Regeneration II and Resistance II for 6,000 ticks (5 minutes); 80-block 3-D sphere, through walls |
| Tree animal area | Surface habitats within 64 horizontal blocks of aura anchor; normal terrain/light/population rules, not the aura's sphere |
| Tree animal adjustment | At most one extra normal selected-species attempt per eligible vanilla local creature attempt; see section 7, not guaranteed twice as many animals |

Do not increase core capacity, enchant away magnet wear, add item light/particles,
new powers, mobs, combat bonuses or a Tree reward chest through these defaults.

Stable resource IDs (registered by the standalone implementation): `relics:machine_core`,
`relics:salvage_magnet`, `relics:colossus_key`,
`relics:monolith_armor_trim_smithing_template`, trim pattern `relics:monolith`,
recipe IDs `relics:machine_core_recharge`, `relics:salvage_magnet_repair` and
`relics:monolith_template_copy`. Component IDs are versioned `relics:core_charge`
and `relics:magnet_wear`; map-origin/delivery components are server-validated,
not player/site binding on the transferable key. Keep existing structure IDs.
Start with original **16 × 16 generated-item sprites**, three core/magnet state
variants and ordinary held-item rendering; no custom 3-D renderer or emissive
light is required. Armor trim texture/atlas registration must match 26.2, with
client and dedicated resource-load tests before accepting artwork as usable.

## 2. World state and existing saves

Use a **save-wide server-authoritative ledger**, separate from the existing
worldgen-feature protection data. Namespace/version its persistence. Store:

- Frozen planner inputs, initial shared spawn, resolver cursor and committed unique
  destination from [Distribution](RELIC_DISTRIBUTION.md).
- Stable natural `site_id`, structure start, center/orientation, asset/marker hashes,
  transformed anchors, per-chunk action IDs and initialization state.
- Deterministic finite reward seeds/results, map-origin claim records, per-player
  Vault claim UUIDs, trial encounter IDs/golem UUIDs and pending deliveries.
- Natural Tree aura anchors independently of present block contents.

All mutations go through server-side serialization/atomic logical transitions;
parallel generation tasks do not mutate player inventories or spawn entities.
Cache spatial indices, not copies of authoritative rewards. Persist enough to
resume unfinished **initial** chunk actions without reinitializing completed ones.

**First gameplay acceptance uses fresh worlds.** A visual-alpha save may contain
multiple large starts and no gameplay ledger. Do not delete, shrink, relabel or
automatically fill their interiors/chests. Detect the legacy state and leave
gameplay initialization disabled with a readable migration notice. An explicitly
requested future migration must select an existing canonical natural site and
respect all old structures/player edits; it is outside this first implementation.
No automatic retroactive gameplay or natural insertion in generated old chunks.

Manual templates/player replicas remain ordinary blocks. A debug command may
register a test fixture explicitly, but it must not count as natural-generation
acceptance or establish production uniqueness. In a separate fixture world, use
separate fixture site IDs so test Vaults cannot corrupt the natural unique ledger.

## 3. Marker initialization and finite ordinary loot

Use [Marker handoff v1](GAMEPLAY_MARKERS.md), with raw hash binding and derived
transforms. Author only the selected interior/archaeology/Tree changes; both skulls
have **no gameplay initialization actions**. New source revisions need provenance
and visual review before replacing a catalog pin.

Install block-entity data during natural placement by owning chunk, before first
interaction. Spawn Tower Endermen on the server in a safe post-generation context,
not a worker thread. A removed initialized placeholder stays removed after reload.
Record deterministic action/entity IDs, check matching pending entity UUIDs before
retrying interrupted initialization, and never respawn an already initialized or
naturally despawned Enderman. A single early whole-site "done" bit is insufficient.

**Delegated modest salvage pool, once per natural site:**

| Site | Copper ingots | Iron ingots | Redstone dust | Amethyst shards |
| --- | --- | --- | --- | --- |
| Large Colossus, all ordinary containers including arm combined | 24–40 | 8–16 | 0–4 | 0–2 |
| Small Colossus, all containers combined | 12–20 | 4–8 | 0–2 | 0–1 |

Draw each integer uniformly from its range using the site's independent loot
stream and distribute the result among builder-marked containers. These are
assistant tuning values, not added mineral fields or per-chest budgets. Special
magnet rewards are separate: **one full functional magnet in the large arm**, and
**one broken magnet with 10% per-small-site probability**. Persist the one site
outcome; new containers/players/reloads never add rolls.

Tower loot has **one roll per site**: 5% one Eye of Ender, otherwise uniformly 4–6
pearls; no extra ordinary Tower loot in the initial pool. Place **five ordinary
Endermen once**, each at its builder marker, with normal neutrality, teleportation,
block pickup and despawning. Do not force them to stay or replace natural mob lists.

Obelisk has **eight finite brushable positions**: six common one-item finds with
the existing delegated weights, one guaranteed Monolith template and one map role
or its approved three-emerald substitution. Proper complete brushing of a fresh
site yields its specials; breaking/destroying suspicious blocks does not refill
them or make them indestructible. No loot/encounter additions at either skull or Tree.

## 4. One defense golem, keys and Vault claims

Use a **marked vanilla iron golem** linked to one trial encounter ID. Persist its
marker/UUID and inject only the target-selection behavior needed to attack eligible
players without retaliation. Preserve normal navigation, attack, health, damage and
pursuit, including outside the cockpit; **no custom leash/forced return/teleport**.
Ordinary village/player-created golems must take the unchanged code path.

The target remains a normal eligible player under ordinary AI visibility/range
rules, not a global infinite-range target. Creative/Spectator are not registered
or targeted. Let normal targeting select/switch targets; do not rewrite other mob
AI. The trial's fixed single spawn position must fit the vanilla entity and use
the builder marker. It is not an invisible encounter boundary.

Adapt trial-spawner configuration/runtime so **one encounter has exactly one
golem**, even with multiple players or Trial Omen. Keep ordinary spawners' ominous
behavior. Preserve ordinary damage when players flee; leaving registration range
does not heal, teleport or replace the living golem. While its tracked golem is
alive, or its status is unknown in an unloaded chunk, do not spawn another. If it
dies outside the cockpit, completion still resolves once. Disappearance/removal
without a confirmed defeat is not success: issue no keys, reconcile the encounter
and restart only under the verified cooldown/reset lifecycle, never duplicate a
possibly living unloaded golem. Verify native 26.2 tracking before relying on it.

Persist the adapter's explicit lifecycle (names are implementation-neutral):

| State | Allowed transition |
| --- | --- |
| `READY` | Eligible native registration/windup -> `ACTIVE`; create one encounter ID and one tracked golem, not one per player |
| `ACTIVE` | Confirmed tracked death -> `REWARD_PENDING`; last player leaving does not reset it |
| `ENTITY_UNKNOWN` | Resolve saved entity status -> same `ACTIVE` encounter or confirmed completion/abort; never spawn a replacement while unknown |
| `REWARD_PENDING` | Reserve each participant's one delivery -> `COOLDOWN`; disconnected/full-inventory grants remain separately pending |
| `ABORTED` | Confirmed non-defeat removal only -> `COOLDOWN`, no keys; reconcile removal reason before entering this state |
| `COOLDOWN` | After 36,000 server ticks -> `READY`; do not wait for every disconnected participant to collect its queued key |

Use saved world game time for cooldown deadlines, including unloaded site chunks;
server-offline wall time does not advance it. The native spawner animation/windup
may be retained, but its tracked-entity distance bookkeeping must not override
this no-duplicate/no-leash contract. Repeatable encounter keys and one lifetime
core claim per player/site remain different records.

Registered Survival/Adventure participants get **one key each per completed
encounter**, including valid late joiners registered before completion. Save the
participant set and completion/grant state. A full inventory or disconnected
participant gets a saved pending delivery, not a shared unowned item another
player can take. Do not reroll on login. Repeating a later trial can yield a key,
but does not restore that player's already claimed core eligibility.
Reward loot tables supply the fixed key/core result; the scoped server adapter
owns per-participant delivery and durable eligibility. Spawner/Vault loot-table
configuration alone does not satisfy those guarantees.

Vault access requires the custom key, consumes **one** key on successful claim,
and grants **one fully charged core**. It is not proof of that player's adjacent
golem kill, and the key remains transferable/not bound to player/site. Reject
both vanilla key types. Use a save-wide **`(site_id, player_uuid)` claim record**;
the finite remembered-player list of a vanilla Vault is not sufficient authority.
Retain its presentation where supported, but never evict old claims to admit new
players. A picked-up core belongs to an ordinary transferable item, not a bound player.

Claim transitions reserve a unique delivery ID, consume the key and produce the
recorded result as one logical server operation. Preserve pending deliveries
across normal save/load and prevent repeated interactions/concurrent requests
from paying twice. **Crash recovery is an explicit implementation proof gate**:
player files and world/block data are not inherently one disk transaction. Use
delivery IDs/reconciliation, and fail closed on an ambiguous delivery instead of
blindly reissuing a core/key. Do not claim vanilla data alone provides crash-safe
exactly-once rewards or silently drop a pending legitimate grant.

## 5. Machine Core and crafting state

Store versioned `remaining_operations` in `0..256` (starting capacity). The core
stays in the appliance's fuel slot as the same single item; **do not translate it
into ordinary burn ticks or consume it as conventional fuel**. In furnaces, blast
furnaces and smokers, a custom guarded processing path supplies heat only when a
recipe can progress and the core is charged, at that appliance's normal speed.

- Decrement by **one only after one recipe operation actually commits its output**,
  even if the recipe outputs multiple items. Blocked outputs, invalid inputs,
  idle time and abandoned partial progress cost zero.
- Keep core-backed progress in the appliance. Save/load or unloaded chunks preserve
  item charge/progress normally, without an offline processing catch-up.
- Removing/replacing the active core or switching its funding mode resets unfinished
  core-backed progress. It does not refund a completed operation, export progress
  with the item, or leave free heat that completes the same job without paying.
- Honor already paid ordinary-fuel burn time before starting the core-specific
  mode; do not double-charge both fuels. Normalize the mode/progress boundary and
  test mixed-fuel switching rather than inheriting an accidental free final job.
- After the last completed operation, the empty core remains inactive in the fuel
  slot. Hopper insertion accepts one charged core; ordinary output extraction is
  unchanged, and a lower hopper may extract an empty core after normal outputs.
  Do not automatically extract charged cores or duplicate the item on appliance break.

Implement custom **state-preserving shaped recipes** with the exact approved
layouts. Core recharge accepts **only depleted cores** plus two coal blocks/shard,
returns one existing core fully charged, and consumes ingredients once. Magnet
repair accepts damaged/broken magnets, returns one existing fully repaired magnet,
and uses four iron/shard in its selected layout. Full inputs or extra occupied
slots fail; Shift-click, recipe previews and repeated craft actions must not create
an extra input remainder. Preserve applicable metadata; no implicit enchantment
bypass, renamed-item substitute, loose-coal/charcoal or alternate repair recipe.

Display final German/English names and the approved copper/violet artwork
directions. Implement **three icon states and exact tooltip values**, no durability/
charge bar. Zero explicitly says depleted/inactive or broken/inactive. Key/Monolith
icons are distinct, not renamed vanilla assets; create artwork during implementation.

## 6. Magnet motion, eligibility and wear

Keep provisional radius **8 blocks** and capacity **1,000**. Only a functional
offhand magnet participates. Query nearby dropped item entities, not inventories,
blocks, mobs, XP, players or global dimensions. Before pulling, check:

1. Normal item pickup delay and ownership rules permit this player.
2. Simulated insertion can accept at least some of the stack with its components.
3. An unobstructed collision-shape path connects item and player's pickup vicinity;
   closed doors/trapdoors, glass and solid walls obstruct even if visually transparent.

Apply bounded velocity, not teleportation/inventory extraction. Recheck collision
and pickup eligibility before impulses; use ordinary movement collision and normal
pickup to finish. Stop when the inventory fills, ownership changes, the magnet
leaves the selected hand, durability reaches zero or the item leaves range. Do not keep
tugging uncollectable items or charge failed attempts. Vanilla pickup delays still
apply to a player dropping their own items.

For overlapping magnets, select the nearest eligible player, UUID tie-break, with
a short-lived server-side attraction claim. It does not override actual item owner
or prevent normal nonmagnetic pickup. Clear it when eligibility changes; do not
persist fake owners onto ordinary items.

**October 28 user decision:** wear is one point per individual item successfully
inserted through magnet assistance. A 64-item stack costs 64 points; partial
pickup costs the actual inserted count. Limit assisted insertion to the remaining
budget. Failed pickups and attempted pulls cost nothing. This supersedes the
earlier per-transaction baseline. Attribute only recent assisted pulls
to that magnet, and debit after actual positive inventory insertion. At zero retain
the broken item and cease assistance; do not destroy it. Test two-player races,
full inventories and mutation/merge between query and pickup.
Serialize the last-point debit with pickup attribution; stale attraction claims
cannot count as fresh assistance after depletion. Ordinary nearby vanilla pickup
may still occur without a functioning magnet and must not create negative wear.

## 7. World Tree effect, animals and lighting

Every second, check living Survival/Adventure players against persisted natural Tree anchors
using squared 3-D distance **`<= 80²`** from the saved builder block-center anchor.
Use the player's feet position as the delegated distance point; Creative/Spectator
skip the gameplay effect but remain usable for separate visual test fixtures.
No sight ray, remaining-tree test, beacon pyramid or payment. Refresh Regeneration II
and Resistance II to five minutes; do not multiply strength/duration across sources or replace a
stronger/longer existing effect with a weaker/shorter one. Use normal effect merging
including hidden lower effects, and test potion/beacon interactions and milk.
Milk removes the current effect normally; remaining in range refreshes it again.
Death does not copy the effect to a distant respawn; each player gets an independent
check. Leaving the sphere stops refreshing, not the already granted timer. The
saved point does not require its own anchor chunk to be loaded for this distance
check; it is queried near players without force-loading remote chunks.

The anchor survives Tree/amethyst removal, but does not move with copied materials.
It does not force remote chunks to stay loaded. Natural dimension and saved
registration, not block-pattern recognition, identify the aura. Hostiles and neutral
mobs retain ordinary behavior; lighting only reduces dark spawning, not outside
arrivals, raids or special spawning.

**Animal integration choice:** within a 64-block horizontal surface habitat,
allow up to **one additional ordinary natural attempt** for pigs/chickens/sheep/
cows when an existing eligible vanilla local creature spawn attempt is processed.
Use the same caps, habitat, player-distance, collision and biome eligibility checks
before every extra attempt; unrelated creatures keep their original behavior.
Do not just double all species weights and claim this doubles animal abundance.
No separate refill clock, placed animal dispenser, mob spawner or direct cap bypass.
This is a maximum attempt budget, not a guaranteed herd or a timer farm; a full
creature cap can yield no increase. The native 26.2 hook observes successful
selected-species spawns inside the ordinary chunk pass. It permits one extra
candidate in the same loaded chunk within 64 horizontal blocks and eight
vertical blocks of a saved anchor. It reruns native biome selection,
player/spawn distance, habitat, obstruction and density checks and charges the
same SpawnState. Breeding, commands, spawners, chunk-generation herds and
unrelated species are unaffected. Actual abundance depends on ordinary caps and habitat.

Builder lights remain root/base-only, unevenly up to 15 blocks high. Measure
shaded spawnable surfaces within the authored root lighting scope separately
from the aura and animal area. The internal **decorative amethyst sphere** uses
no budding blocks/regrowth and is not an aura switch or new loot container.

## 8. Monolith trim and expedition-map state

Create original **Monolith-Rüstungsbesatz / Monolith Armor Trim** assets: narrow
vertical lines with angular branches across the armor pieces. Use normal smithing
trim application/material rules; no armor statistics. Technical duplication layout
follows the vanilla pattern: template top-middle, copper block center, diamonds
in the other seven cells -> two templates. No extra template-input remainder.

Each natural Obelisk map reward gets a saved **origin claim ID**. Pending and resolved
copies retain it and use normal map-copying ingredients/behavior through a component-
preserving recipe adapter. An explicitly unconfirmed map has no invented target
coordinates. Maps share the [unique resolver](RELIC_DISTRIBUTION.md), never spawn
their own destination, and cannot reveal a rejected/unverified candidate.

| Origin state | Result |
| --- | --- |
| `PENDING` | Persist an unconfirmed expedition map and retry in bounded server work, on availability/reload/holder checks; no new loot roll |
| `MAP_RESOLVED` | All copies reference the same committed natural destination; no maximum travel-distance cutoff |
| `COMPENSATED` | One finite payout of three emeralds instead of this original map reward; all copies lose payout/target entitlement |

If truly unavailable at initial brushing, produce three emeralds directly for
the map role and mark that origin compensated. If a pending map later becomes
definitively unavailable, allow **one redemption for its origin** by a holder
using the pending map; consume that copy on successful redemption and mark all
other copies explicitly unavailable/no-payout rather than silently blank;
invalidate all pending copies using the shared ledger. Use the same pending-delivery
protection as other grants. A copied map is not an additional compensation claim.
Once compensated, later re-enabling cannot convert old copies into a map as well.
Once resolved, generation deactivation or player mining does not invalidate the
destination or grant compensation. The independent trim reward stays finite and
unaffected. No marker refresh/reload can recreate consumed archaeology.

## 9. Implementation sequence and evidence

After a separate implementation request:

1. Prove the planner/terrain API equivalence, trial single-golem lifecycle, Vault
   durable eligibility and safe natural-spawn hook in isolated 26.2 fixtures.
2. Implement versioned item state, furnace path, recipes and pickup accounting.
3. Add marker validation/derivation and per-chunk idempotent initialization; consume
   actual builder exports, not coordinates inferred from screenshots.
4. Implement natural-site state, distribution/resolver, finite loot/claims/maps,
   golem aggression and Tree effects/animal adjustment without changing ordinary mobs.
5. Create the original item/trim assets, then run the
   [acceptance matrix](../testing/GAMEPLAY_ACCEPTANCE_PLAN.md) and survival tuning.

API inability, ambiguous reward recovery, unacceptable stalls or false anchors
block the affected feature/release. Technical defaults can be tuned with evidence;
changing approved mechanics, distances or reward policies requires renewed approval.


## October 28 interior revision V4

Fresh worlds select `interiors-20261028-v4`: accepted Large Colossus V7,
Small Colossus V11, Tower V10, accepted Obelisk V6 and retained World Tree V5.
The new Small entrance is six blocks shorter; its upper chest remains unchanged.
The Tower chest is centered on the rear wall opposite the entrance, at raw
[58,15,55], facing north. The new stand and existing source solids are excluded
from native terrain clearance. V1, V2 and V3 remain available with their exact
previous manifests, coordinates and template bytes; existing worlds do not move
loot or structures. See [integration and review](../project/INTERIORS_V4_20261028.md).

Monolith now uses isolated one-pixel angular marks on the native 26.2 equipment
UVs. The native netherite alpha mask constrains the pattern, so helmet openings,
lower bare arms and upper boot transparency remain clear. Existing smithing
material palettes still determine the color. IDs, recipes, item art and armor
statistics are unchanged. The texture updates existing trimmed armor after
resource reload or game restart, independently of world interior revision.
