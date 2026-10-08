# Standalone gameplay development — October 8, 2026

**Development code, not a gameplay release or Minecraft runtime acceptance.**
The user authorized all items followed by golem behavior, durable Vault rights,
map-state management and Tree aura in a separate worktree. Branch:
`feat/gameplay-items-runtime`; metadata: `0.1.0-alpha.5.0-dev`, Minecraft **26.2 / Fabric / Java 25**.
The user explicitly chose **no server testing**. No server/client, EULA acceptance,
profile installation, new Minecraft world, publication or natural marker hookup
is part of this work. Do not install this development artifact over the accepted
visual release as though the gameplay acceptance gates had passed.

## Code delivered

| Area | Development implementation | Not yet proven |
| --- | --- | --- |
| Machine Core | Versioned bounded 256-operation component, one surviving item, guarded furnace/blast-furnace/smoker path, decrement after output commit, no idle burn, saved appliance mode, removal resets unfinished progress; charged insertion/depleted lower-hopper extraction, GUI fuel acceptance | Actual appliances, GUI/Shift-click, hopper race/switching, reload/break behavior and mod interaction |
| Salvage Magnet | Versioned 1,000-transaction budget, offhand only, 8-block spatial item query every four ticks, nearest/UUID selection, pickup owner/delay/inventory/collision checks before each per-tick impulse, vanilla pickup attribution/debit, broken item retained | Moving/merging items, glass/doors, ownership mutation, last-point and two-player races, actual insertion/storage APIs |
| Recipes/presentation | State-preserving approved shaped recharge/repair; Monolith seven-diamond/copper copy and cosmetic smithing; four registered items, English/German names, original 16×16 sprites, full/partial/zero icons, exact tooltips, no inventory status bar; original 64×32 trim masks with additive palette atlas | Full client resource/atlas load, worn armor and visual approval; full crafting/menu interaction |
| Defense golem/trial | Explicit fixture site -> native trial-player visibility detection, fixed one-golem spawn position, no waves/scaling/ominous path; marked native iron golem gets a normal visible/range-limited eligible-player target goal, with normal stats/navigation/pursuit | Native lifecycle, attack/pursuit outside cockpit, unloaded/dimension-changing entities, Trial Omen, vanilla golem regression and real crash recovery |
| Vault/deliveries | Unlimited save-wide `(site, player UUID)` reservations, transferable custom key only, one fully charged core, fixed key/core loot tables, per-participant repeatable encounter keys, saved queues and player receipts | Actual native interaction/presentation, multiplayer/disconnect/full-inventory behavior, receipt storage, player saves and injected I/O/crash tests |
| Expedition maps | Origin component on ordinary filled maps; pending has no fake map ID/target; immutable resolved target and shared map ID, center/dimension validation, one original three-emerald compensation reservation, compensated copies never revive; vanilla 26.2 cloning preserves components | Actual cartography/crafting menus, inventory/frame/chest presentation refresh, resolver hookup and full recovery tests |
| Tree aura | Saved dimension/block-center anchor, spatial bucket query, feet-position inclusive 24-block sphere through walls, Regeneration I refreshed to 6,000 ticks every 20 ticks, normal effect merging; explicit registration only, no block recognition/chunk loading | Native potion/beacon/milk/death behavior and survival testing |

Core shaped input follows vanilla normalized crafting coordinates: its entirely
empty bottom row is trimmed away. The shape remains shard above center core,
coal blocks left/right, all other occupied slots rejected; a 2×2 grid cannot fit
it. The analogous magnet shape includes both lower iron ingots. Recipes preserve
metadata and return no extra source-item remainder. Artwork is reproduced by
`tools/generate_gameplay_art.py`; no downloaded vanilla PNG was copied.
[Source-art preview](gameplay-items-preview.png) is **not an in-game screenshot**.

## Persistence and recovery boundaries

The journal is `<world>/data/relics_gameplay_v1.json`: schema-versioned,
SHA-256-checked JSON payload, flushed temporary file and atomic replacement.
Corrupt/unknown state or failed commits stop the affected mutation; there is no
empty-ledger reset or stale-backup fallback. Mutations run on the server thread.
It stores fixture anchors, encounters/participants/UUIDs, cooldown deadlines,
terminal golem tombstones, unlimited Vault claims, origins and delivery IDs.

- `QUEUED`: no item or payment mutation yet; offline/full inventories remain queued.
- `IN_FLIGHT`: journal intent exists before key/map debit and complete insertion.
  A persistent, death-copied player attachment records the delivery receipt.
  The adapter requests a vanilla player save and verifies the receipt in `player.dat`
  before acknowledging it; a swallowed native save error is not success.
- `DELIVERED`: matching persisted receipt proves that player's inventory operation
  saved. Normal repeat interactions do not pay again.
- `AMBIGUOUS`: after interruption, dispatch/acknowledgement without a loaded receipt
  is held, logged by delivery ID and reported to the player. Never automatically
  reissue it. A later matching receipt can reconcile the hold.

This is **not a claim of crash-safe exactly-once delivery across every Minecraft
save path**. Dedicated/integrated-owner save ordering, death cloning, attachment
NBT layout, disk failures and power-loss durability still require runtime evidence.
No automatic administrator “retry” command is provided: investigate the journal,
player file/receipt and logs together, keep consistent backups, and resolve a held
legitimate grant only with evidence. Do not delete a claim or roll back one file
independently to manufacture fresh entitlement. A missing receipt is uncertainty,
not proof that a player received nothing.

`SPAWN_PENDING` reserves a golem UUID before insertion. Missing tracked entities
become `ENTITY_UNKNOWN`; absence/unload is neither death nor permission to replace.
Confirmed death queues one key per registered participant. Confirmed destructive
non-death removal grants none; both enter a 36,000-tick cooldown. Terminal UUIDs
are tombstoned so a stale saved entity cannot revive a completed encounter when
loaded. A crash between reserved spawn and first entity save can leave a fixture
held as unknown; no duplicate is spawned to “fix” it. Entity-load/removal event
ordering and tombstone behavior remain a runtime proof gate.

## Tests actually performed

- Compile all production sources with checksum-verified Minecraft 26.2,
  Fabric Loader 0.19.5, Fabric API 0.161.0+26.2 and Lithostitched 1.8.0 against JDK 25.
- Headless Java tests use actual item/component, recipe/loot and Monolith codecs,
  shaped assembly/remainders, vanilla map-cloning recipe, native map-center math,
  production ledger reservation/completion/reconciliation and aura boundary code.
  More than 512 Vault UUIDs are retained across journal reload.
  **648 gameplay assertions passed.** The separate existing headless placement
  Java suite also passed **755 assertions**.
- The unit bootstrap deliberately supplies only selected actual item initializers,
  four vanilla trim materials and fixture armor/material tags. **It is not a full
  datapack load and does not apply Fabric mixins or instantiate a Minecraft server.**
- Static ASM checks validate the new mixins' declared target methods, shadow
  fields/methods, accessor/invoker descriptors and wrapped pickup invocation against
  26.2 bytecode. **Target existence is not successful mixin application/execution.**
  **34 static target contracts passed.**
- The pre-existing full Python suite passed **105 tests**, including exact accepted
  raw/natural exports, terrain/density preservation and isolated visual 1.21.1
  preparation. All **six** new artwork/resource tests also passed, as did the
  **four** documentation/layout tests rerun after the status documentation edits.
  New resource checks are in `tests/test_gameplay_resources.py`.
- `git diff --check` passed. Two final development builds were byte-identical:
  `dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar`, SHA-256
  `5dd5163cfd95bb7a624ca77e4f735b0491a37b3e8051118c80af245575a3c9fa`.

Reproduce without a server (JDK 25 and the verified cache required):

```powershell
python tools/setup_worldgen_build.py --accept-downloads
python tools/test_gameplay.py --java-home "$env:JAVA_HOME"
python -m unittest discover -s tests -v
python tools/build.py --java-home "$env:JAVA_HOME"
```

Dependency preparation downloads build inputs only; it does not launch Minecraft.
The local development JAR is under `dist/`, not a published release.
JDK deprecation notices from vanilla/JOML and deprecated compatible tooltip APIs
are recorded as warnings, not runtime evidence.

## Optional future isolated fixture setup

Only after separately choosing a new test world and authorizing runtime tests,
start its JVM with `-Drelics.gameplayFixtures=true`. No command is registered on
ordinary launches. Operator commands:

```text
/relicsfixture site <name> <spawner x y z> <golem x y z> <vault x y z>
/relicsfixture tree <name> <anchor x y z>
/relicsfixture map <origin>
/relicsfixture target <target x y z>
/relicsfixture unavailable
/relicsfixture status
```

Place a real trial spawner and Vault first; registration does not construct or
clear terrain. Give enough free space/support for an ordinary golem. Fixture IDs
are prefixed `fixture:`; registration refuses duplicate IDs/anchors instead of
overwriting claims. A target command explicitly simulates a committed fixture
destination; it does **not** prove the natural unique-site resolver found one.
No force-complete, free-reward, natural registration or retroactive migration
command is implemented.

## Still outside this implementation

Actual builder sidecars/exports/coordinates and natural gameplay initialization,
shared rarity/unique-site resolver, finite archaeology/chest/animal/Enderman hooks
remain pending. In particular **no extra natural animal attempts** or substitute
forced spawning were added; the user requested the aura, not an unproven spawning
shortcut. Pending-map retries currently resolve against explicitly committed
ledger state on holder checks, not a fabricated natural target or unbounded search.
The complete [gameplay acceptance matrix](GAMEPLAY_ACCEPTANCE_PLAN.md) remains
future work, especially multiplayer, crash injection, client rendering, actual
biome/terrain rarity, performance and survival tuning.

Both skulls, accepted visual models/worldgen resources and existing worlds are
unchanged. The separate 1.21.1 preparation now reads a pinned visual Alpha 4.9
metadata snapshot, copies only the original visual Java/mixins and strips the two
26.2 gameplay initialization calls; it does not silently backport the new items.
No preserved release JAR or Minecraft profile was overwritten.
