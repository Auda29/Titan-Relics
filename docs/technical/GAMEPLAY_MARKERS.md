# Gameplay marker handoff — version 1

Prepared: October 8, 2026. **Marker loader and gameplay injection remain planned.**
Following the user's separate builder implementation request, five
[versioned architectural exports and sidecars](../project/GAMEPLAY_INTERIORS_HANDOFF.md)
are now available as review candidates. This contract does not itself dispatch agents.

User-approved gameplay is in the per-relic `gameplay/` documents. The format and
cardinalities here are integration decisions under the delegated technical work.
Runtime consumers are specified in [Gameplay runtime](GAMEPLAY_RUNTIME.md).

## 1. Deliverables and preservation

For each changed design the builder supplies:

1. A **new versioned source/export**, its editable source, dimensions, ground level,
   facing, SHA-256 and a short change description. Do not overwrite accepted or
   historical exports. The existing [catalog](../../tools/relic_catalog.py) remains
   the visual-alpha baseline until a separately reviewed integration changes it.
2. A sibling **`<export-stem>.gameplay.json`** sidecar beside that export under the
   relic's `design/` area. Do not put marker placeholders into runtime Java sources.
3. Views showing access, required clearance, marker positions and the intended
   exploration, including a player/golem scale reference where relevant.

The existing converter/integrator rejects source entities and block-entity NBT;
raw exports omit air. Therefore the first handoff uses **ordinary placeholder
blocks plus a sidecar**, not command blocks, armor stands, invisible entities or
embedded spawner/vault/loot NBT. The integrator will produce derived templates
and inject the data in a supported step; it must not weaken validation globally.
Do not relabel legacy DataVersion 3105 as a migration. Verify states and formats
against the actual 26.2 runtime.

**Both skulls require no gameplay sidecar and no new edits.** Their interiors,
access, omitted-air behavior, natural spawning and lack of chests remain accepted
as-is. They participate only in the future distribution planner.

## 2. Coordinate and identity contract

The sidecar header contains:

| Field | Contract |
| --- | --- |
| `schema_version` | Integer `1`; reject unknown versions |
| `structure_id` | Existing catalog ID with `relics:` namespace; not a new design |
| `asset_version` | Exact export revision/stem |
| `source_nbt` | Repository-root-relative maintained export path |
| `source_sha256` | SHA-256 of that exact raw NBT, 64 lowercase hexadecimal characters |
| `size` | Three positive integers, identical to raw NBT size |
| `ground_y` | Raw export's ground level, not the padded natural template's level |
| `coordinate_space` | Literal `raw_template` |
| `source_facing` | Literal `north`; document another source orientation before integration |
| `markers` | Array of point markers |
| `regions` | Array of bounded regions; empty when no region is required |

Coordinates are **integer raw-template block positions** relative to its lower
corner `(0,0,0)`, X/Y/Z, before natural-template padding and world rotation. No
world coordinates or guessed terrain height belong in a builder sidecar.

- A point marker has unique `id`, `role`, `pos: [x,y,z]` and optional `facing`.
  Block-injection roles also require `expected_block`, the normalized placeholder
  block state; entity spawn markers denote the **feet block**, not a block to replace.
- A region has unique `id`, `role`, and inclusive integer `min`/`max` corners.
  Clearing regions require an explicit `replaceable_blocks` allow-list; they must
  not mean "erase everything in the model bounds".
- IDs are stable within a design revision and unique across both arrays. Exact
  roles are in the table below; reject unknown roles rather than ignoring them.
- Points and regions must be in the raw bounds. Required clearance can be empty
  in the export: declare it in the sidecar rather than adding an air-filled box.
- `source_nbt` resolves within that relic's maintained design area: no absolute
  paths, parent traversal or URL inputs. IDs use lowercase letters/digits/underscore/
  hyphen; `facing` is a cardinal lowercase direction. Reject unsupported mirroring
  in v1 instead of treating it as a rotation. Validate normalized block-state strings
  against the target registry and exact placeholder state at the point.

Formatting example of **one marker**, not a usable site or guessed coordinate:

```json
{
  "id": "tree-aura",
  "role": "tree_aura_anchor",
  "pos": [10, 1, 10]
}
```

The integrator binds this to the header/hash and builder evidence; copying this
example into a real export is not a valid handoff.

## 3. Transform and chunk contract

1. Verify raw hash, size and ground level before deriving anything.
2. Translate raw coordinates by the **recorded actual derivation offset**. The
   current pipeline uses `(8, padding(contract), 8)`; see
   [terrain foundations](../../tools/terrain_foundations.py). Do not hard-code this
   for future derivatives. Skull 2 clipping is unrelated and must stay unchanged.
3. Apply the **same Minecraft template rotation, pivot and world origin** as the
   natural template. Test NORTH/EAST/SOUTH/WEST, negative coordinates and non-square
   templates; do not rotate around an independently guessed center. Rotate facing
   and every region corner too, then rebuild its axis-aligned bounds.
4. Entity feet become `(x+0.5,y,z+0.5)` after the block transform; aura anchors use
   the transformed block center `(x+0.5,y+0.5,z+0.5)`. Store the resulting aura point.
5. Assign each block/entity action to its owning chunk. A large template is **not**
   permission to write into unloaded neighbors or run entity spawning in worldgen
   worker threads. Repeated chunk placement must not repeat completed actions.

The natural jigsaw surface-query anchor and the gameplay site center are distinct
from the lower template corner. Spacing uses the planner's site center; the Tree
aura uses its builder marker. Detect collisions with the generated jigsaw anchor,
terrain supports, other marker replacements and contradictory clear regions.

## 4. Required roles and builder experience

Counts below are integration starting requirements, not extra rewards.

| Design | Required point markers | Required regions / experience |
| --- | --- | --- |
| Large Colossus | 1 `colossus_trial_spawner`, 1 `colossus_golem_spawn`, 1 `colossus_vault`, 1 `colossus_hatch`, 1 `colossus_arm_magnet_chest`; any ordinary containers are `colossus_salvage_chest` | Targeted `cockpit_clearance` and `hatch_clearance`; retained body cavity, five near-player-sized crew stations/traces, identifiable hatch reached by player climbing/building. No complete authored ascent. Short independent exploration inside the detached arm to its chest. Golem clearance fits a normal iron golem, not a leash boundary. |
| Small Colossus | 1 `small_magnet_chest`; any other containers are `colossus_salvage_chest` | Accessible but severely decayed interior, cockpit effectively gone. The single magnet roll is per site; ordinary salvage is shared across all its containers. Do not restore two seats or inherit a trial/vault/core. Targeted `small_interior_clearance` only if the builder's new interior needs it. |
| Obelisk | 6 distinct `archaeology_common`, 1 `archaeology_trim`, 1 `archaeology_map` | Eight exterior suspicious sand/gravel positions with readable excavation clues. Keep the monument solid; no underground dungeon, authored guard or special chest requirement. Trim/map positions must be reachable by careful brushing. |
| Ruined Tower | 5 distinct `tower_enderman_spawn`, 1 `tower_ender_chest`, 1 `tower_entry`, 1 `tower_upper_destination` | Lower dungeon with safe Enderman feet/head space and vanilla behavior. Incomplete stairs require player building toward the upper destination. Only targeted `tower_route_clearance` if needed; no complete staircase or repeatable spawner. |
| World Tree | 1 `tree_aura_anchor`, 1 `tree_amethyst_center` | One or more `tree_lighting_scope` regions around trunk/base/roots. Small decorative amethyst sphere inside the bottom of the trunk; no budding amethyst. No loot markers. Aura is a 80-block sphere through walls, independent of remaining blocks. |
| Crowned Skull, all palettes | None | **No change or additional access/clearing review.** |
| Sword-bearing Skull 2 | None | **No change or additional access/clearing review.** |

The marker role supplies gameplay meaning, not an arbitrary loot-table string.
The October 8 builder handoff adds the optional **`arm_clearance`** region role
for the large Colossus's independent broken-elbow passage. It has the same bounded
native-terrain allow-list and authored-solid preservation rules as the other
Colossus clearances. This avoids falsely labeling an arm passage as cockpit space.
The future loader must recognize this explicit role; no runtime loader existed
when the builder added it.
Injection roles are the spawner/vault/chest and `archaeology_*` roles;
`colossus_hatch`, `tower_entry`, `tower_upper_destination`, aura/amethyst review
points and entity feet are references, not runtime block replacements. Required
large clearances each contain at least one bounded region; extra ordinary salvage
containers are optional because the arm/small magnet chest may hold ordinary loot too.
The runtime uses the approved per-site budgets; adding a container never adds a
new special-reward roll. Source placeholders for copper chests, trial spawner,
vault and suspicious blocks must be valid target-version states. The builder
does not need to author their block-entity contents.

For the Tree, `tree_amethyst_center` is a **review marker only**, not an aura switch
or new machine block. Lighting may rise unevenly at most 15 blocks above the
builder-marked local trunk base; no crown/upper-branch lights. Ground coverage
follows the root area and actual shaded spawnable ground, not a perfect 80-block
ring. The integrator must measure real light; firefly visuals are not proof of
spawn suppression. Ordinary natural hostile spawning/arrivals remain unchanged.

## 5. Clearing, injection and one-time initialization

- Clearing is supported only for the explicitly listed Colossus/Tower interior
  regions. Preserve authored solids and other structures; use bounded native
  terrain/vegetation allow-lists, with water rejection at site validation rather
  than silently draining a lake. **No skull clear regions.**
- Clearing and block-entity installation happen in the natural placement pipeline,
  before first player interaction, by owning chunk. Extending late-worldgen
  protection to these injected cells/approved clear cells does not prohibit player
  mining or building. The current protection code is not a gameplay initializer.
- Set loot seeds and block data once; entity actions are queued to a safe server
  context. Record action IDs and deterministic Enderman UUIDs, not just a single
  "whole structure initialized" flag before every chunk has completed.
- Reload never recreates a removed chest, suspicious block, Enderman, amethyst
  sphere or light. Builder-authored decorations do not replenish after mining.
- Raw `/place template`, schematics and player copies do not automatically register
  natural sites or grant the Tree aura. Explicit debug fixture registration belongs
  only in isolated test worlds and is labeled non-natural evidence.

## 6. Handoff acceptance checklist

Before packaging a revised design, verify:

- Header/hash/version binding, canonical path, bounds and exact role cardinalities.
- No duplicate injection positions, ambiguous clearing, negative/reversed bounds,
  accidental source entities or block NBT; no placeholder conflict at the jigsaw anchor.
- Correct derived padding, facing, four rotations, burial and chunk ownership.
- Collision-free initial spawn space and safe feet blocks; ordinary golem/Enderman
  navigation may later change with player building and is not artificially constrained.
- Hatch, independent arm find, finite archaeology and broken Tower ascent match
  the experience, without expanding skull scope or changing preserved Colossus art.
- Lighting/root-only limit and decorative amethyst sphere, with sphere-independent aura.
- Editable export provenance, revision-specific marker views and target-version
  runtime validation. Missing/changed required markers **fail integration closed**;
  do not guess new coordinates or ship a partially initialized reward site.

Actual builder coordinates and asset hashes are deliverables, not missing user
gameplay decisions. The [acceptance plan](../testing/GAMEPLAY_ACCEPTANCE_PLAN.md)
separates future tests from the completed documentation review.
