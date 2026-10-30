# Gameplay planning closure and documentation review

> **Current status, October 30, 2026:** All seven gameplay directions are implemented and released on four game/loader targets. See the
> [Alpha 5.0.3 status and roadmap](CURRENT_STATUS_AND_ROADMAP.md). Approved design requirements
> remain specifications; dated pending/unimplemented claims below are historical
> where superseded by the released implementation and linked evidence.

## Historical planning record

Reviewed: October 8, 2026. **Outcome: all seven gameplay directions, builder handoff
and technical starting contracts are documented consistently.** No further large
user-question round is needed. This closes the planning/documentation gate only;
it is **not gameplay implementation authorization, builder acceptance or a runtime
test report**. The current request includes committing/pushing these planning changes.

## 1. Authority and status vocabulary

**Historical planning milestone:** the user subsequently authorized item/system
implementation on a separate worktree. Its [code status and test boundaries](../testing/GAMEPLAY_IMPLEMENTATION_20261008.md)
do not retroactively turn this planning review into gameplay acceptance.

1. **User-approved design:** current sections of
   [implementation plan](UMSETZUNGSPLAN.md), [lore bible](LORE-BIBLE.md) and each
   relic's gameplay document. Preserve final mechanics/lore/rates when implementing.
2. **Delegated engineering/tuning baseline:**
   [runtime](../technical/GAMEPLAY_RUNTIME.md),
   [builder sidecar v1](../technical/GAMEPLAY_MARKERS.md),
   [distribution resolver](../technical/RELIC_DISTRIBUTION.md). These fill technical
   details without representing their extra numbers as user approvals.
3. **Implemented visual baseline:** repository README, pinned
   [catalog](../../tools/relic_catalog.py) and dated
   [Alpha 4.9 evidence](../testing/ALPHA_4_9_TEST_REPORT.md). Documentation of planned
   gameplay does not add it to the alpha JAR.
4. **Historical evidence/proposals:** versioned design studies, old milestone
   tables, old rates, superseded recipes and optional visual storytelling. Preserve
   provenance/failures; they are not competing current instructions.

“Specified” means a contract exists; “implemented”, “tested” and “accepted” require
their own evidence. Deliberately unknown Titan/crew identities, motive, machine
downfall and exact event sequence are not blockers to invent answers for.

## 2. Seven-design reconciliation

| Design and current visual selection | Selected gameplay / preservation | Remaining deliverables |
| --- | --- | --- |
| Large Colossus V4.1 materials B | Five operators; preserve body cavity, cockpit/hatch and player-built climb; one ordinary-strength attacking defense golem, one key per participant, one fully charged core per player's Vault claim; shared arm magnet | Versioned builder cockpit/hatch/arm sidecar/export; scoped AI/trial lifecycle, durable claims, original item art and survival proof |
| Small Colossus V7 ground-v3 | Two original operators; accessible severe decay/cockpit loss, no palette swap or intact stations; 10% per-site one broken magnet, modest shared salvage, no inherited trial/key/core/Vault | Ruined interior/container markers; finite roll/state/repair integration and tuning |
| Obelisk V4.2 | Solid cleared-territory marker; finite exterior archaeology, six common finds plus reliable Monolith template/map; shared/copyable rewards | Eight builder brushing positions, original trim resources, verified destination/pending-origin/compensation handling |
| Crowned Skull V4, four palettes | Existing interiors/access/natural mobs unchanged; no loot chests or authored encounters; palettes share their design budget | Distribution validation only; **no builder/marker/clearing work** |
| Skull 2 V2 embedded-v1 | Same unchanged gameplay policy; accepted sword/anatomy/terrain integration; sword owner unknown | Distribution validation only; **no builder/marker/clearing work** |
| Ruined Tower V7 ground-v3 | Never-finished base, abandoned, incomplete stairs bridged by player; five one-time ordinary Endermen; one finite site roll: 5% one eye otherwise 4–6 pearls | Lower-area entity/chest and entry/upper destination markers; safe one-time placement and vanilla behavior tests |
| World Tree V4.3 strands | Peaceful refuge; selected natural animals, root/base-only lights up to 15 blocks, small internal decorative amethyst sphere; Regeneration II and Resistance II in 80-block through-wall sphere, five-minute departure tail, saved anchor survives removal | Builder anchor/lights/sphere, natural-spawn/effect integration and actual light/survival tests; no Tree loot |

Visual-alpha geometry/export selection remains unchanged. Material B stays
**25,423 copper blocks + 10 raw iron blocks (90 raw iron items)** with intact V4.1
geometry; its post-salvage simulation is not completed survival-economy testing.
Do not downgrade 26.2 saves; the 1.21.1 visual port remains preserved and a gameplay
backport is a separate later decision.

## 3. Cross-document contracts checked

- **History:** thousands of years, no living Titans; all Colossi crewed, five/two
  operators; defense robot; cleared-territory Obelisks; unfinished campaign Tower;
  Titans' World Tree strength/size and failed destruction. No new boss/revival/motive.
- **Rewards:** guaranteed custom transferable consumed key -> per-player charged
  core, no repeat Vault claims; large-arm full magnet and small-site 10% broken
  magnet/ordinary salvage/archaeology/Tower loot remain shared finite. No refill,
  per-container special rolls or loot at the skulls/Tree.
- **Items/presentation:** 256-operation/no-idle-loss reusable core and 8-block/
  approximately 1,000-collection offhand magnet remain provisional. Both shaped
  recharge/repair layouts preserve one existing item. Final German/English names,
  copper/violet art, exact tooltips/three icons, no inventory bar; Monolith's narrow
  vertical/angular-branch motif and seven-diamond/copper duplication are consistent.
- **Trial behavior:** one golem/no waves/no multiplayer stat scaling/no ominous
  bonus. Scoped initial aggression with otherwise normal movement/pursuit outside
  cockpit, without leash/forced return/teleport; ordinary golems unchanged.
- **Placement:** one shared opportunity per approximately 5,000 × 5,000 blocks,
  2,000 general center floor, 15,000 between Obelisks, 6,000-radius non-touching
  regions. Shares: Obelisk 30%, skull designs 15%/15% inside and 2.5%/2.5% outside,
  Tower/small/Tree 2% each, empty 34%/59%. No rejected-anchor regions or fill/rerolls.
- **Unique/maps:** one valid natural large site per enabled supported save, 30,000
  minimum from frozen shared spawn. No arbitrary map-distance cutoff, extra map
  structure or personal-spawn relocation. Pending means unconfirmed; genuine
  absence substitutes three emeralds once per original reward, not per map copy;
  mined/committed disabled-generation sites stay valid destinations.
- **Tree:** spherical through-wall persisted anchor, no aura from copied blocks;
  lighting footprint independent of aura, no crown lights/budding amethyst,
  ordinary hostiles/arrivals, natural animal caps and no timer/spawner replenishment.

The technical baseline defines item/icon/recipe/progress/pickup accounting,
trial lifecycle/cooldown/participant grants, claim/map persistence, chunk actions,
Tree effect merging and animal attempts. Builder coordinates/artwork are
deliverables, not questions requiring another fundamental design round.

## 4. Superseded active wording and archive boundary

Reconciled the README/shared index, per-relic entry points/gameplay plans, lore
bible, concept catalog, implementation plan and six-point review. Removed stale
active claims that rates, geometry, multiplayer sharing, recharge/repair layouts,
golem activation or aura geometry still require user selection. Linked technical
defaults and separated undelivered builder/artwork from unimplemented mechanics.

Marked original implementation milestones and concept roadmap/acceptance as
historical. Kept dated V1–V4 studies, alternative material A, old retaliation/
restoration/recipe/density proposals and all historical test evidence; these cannot
override the new contracts. Optional visual conflict links do not authorize skull
edits or new settlement/interior scope. README/catalog remains authority on actual
assets; current Alpha 4.9 still uses independent provisional placement sets.

The [browser visualization](visualizations/relic-distribution-plan.html) is a
schematic, not natural Minecraft evidence. All three deterministic examples retain
the approved geometry/one-large-site rules. Seed 137 having seven Trees versus
six Obelisks is explicitly permitted finite-sample variation, not a hierarchy cap
or reason to reroll examples. Aggregate realized rarity under **real biome/terrain
rejection has not been measured**; the new acceptance plan requires it.

## 5. Scope and checks for this documentation revision

Only Markdown planning/index files and the existing schematic HTML are changed.
No Java/worldgen resource/recipe implementation, item/trim assets, builder exports,
JAR, release, dependency update or Minecraft world is changed. No builder session
is dispatched. Local `.openchamber/` screenshots remain outside this push.

Checks run for this documentation revision:

- `python -m unittest discover -s tests -p test_repository_layout.py -v`:
  **4 tests passed**, including local documentation file links and relocated paths.
- `git diff --check`: passed, no whitespace errors. Git's LF/CRLF notice for the
  HTML working copy is a line-ending warning, not a failed check.
- Node executed the HTML's actual script for seeds **42, 137, 812**: passed syntax,
  determinism, one large site, 30,000 spawn floor, all accepted pairs' 2,000 floor,
  Obelisks' 15,000/non-touching regions and the existing schematic counts. No strict
  per-seed tier ordering was imposed. This is not the future production algorithm.

These are not the entire historical Python/JavaScript/Java suite
and do not pass the **future** [gameplay acceptance plan](../testing/GAMEPLAY_ACCEPTANCE_PLAN.md).

## 6. What can start next

After a separate implementation request, proceed with technical API proofs and
item/recipe work while the separate builder produces the marker-bound exports.
Gate natural integration on those deliverables and target-version tests. Unknown
terrain API behavior, durable reward recovery, the one-golem tracking lifecycle
and the safe natural animal hook are explicit prototype/release proof gates;
do not silently replace approved behavior if an adapter fails.
