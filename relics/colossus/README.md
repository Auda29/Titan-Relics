# Colossus

The **playable Alpha 3 uses V3**, including the buried abdomen, torn hip, and
detached arm; see [V3 integration](../../docs/technical/V3_INTEGRATION.md).
The **selected offline asset is V4.1 with material study B**. Its palette/inventory
and simulated post-salvage appearance are visually accepted, but build integration
and Minecraft testing are still pending. Material study B is distinct from the
earlier B / open-chest-frame geometry choice.

## Design and assets

- [Accepted material version B / salvageable armour](docs/COLOSSUS_MATERIAL_STUDY_B.md) — same 223,161 positions; 25,423 copper blocks and 90 raw iron items; intact and post-salvage appearance approved

- [V4.1 palm-up hand revision](docs/COLOSSUS_V4_1.md) — visually accepted; selected B chest and revised hand pose

- [In-game shader demo gallery](demo/README.md) — three Colossus V3 Minecraft screenshots
- [V4 revision goals](docs/COLOSSUS_V4.md)
- [V4 exports and reproduction](docs/COLOSSUS_V4_EXPORTS.md) — B / open machine frame selected; A retained for comparison
- [V4 rear / right hand / chest comparison](design/generated/colossus-v4-open/colossus-v4-changes-review.png)
- [V3 design and reproduction commands](docs/COLOSSUS_V3.md)
- [V2 design history](docs/COLOSSUS_V2.md)
- [Design configurations and output layout](design/README.md)
- [V3 Blender model, exports, and review sheets](design/generated/colossus-v3/)
- [Archived first concept](archive/first-concept/): preserved as the basis for a
  future second, smaller Colossus (original export: 99 × 66 × 71 blocks).

## Gameplay

- [Machine Core, Salvage Magnet, Colossus Key, and head trial](gameplay/ITEMS.md)
- [Lore/gameplay review: material economy, trial history, and lasting utility](../../docs/project/LORE_GAMEPLAY_REVIEW.md)

**Approved occurrence rule:** one naturally generated **large Colossus per game
world/save**, shared by all players. Planned **smaller Colossi may occur multiple
times**; their loot and frequency are not yet assigned. Alpha 3 currently uses
repeatable candidate distribution and does **not** enforce large-site uniqueness.
Obelisk maps will initially lead to the same unique large landmark.

The head trial uses an iron golem and a vault with a guaranteed Machine Core
reward. The detached arm offers a short exploration route to a copper chest with
a guaranteed functional Salvage Magnet, without a key or second trial. Detailed
interiors and armor trim design are deferred. These gameplay features are
decisions, not implemented mechanics.

The per-player vault is intended to let later multiplayer visitors obtain a core
at that one site. The magnet's shared copper chest still needs a late-visitor
policy. Review follow-ups are open: bulk metal recovery may overshadow rewards,
the golem needs a historical function, and core capacity/cost must serve an
everyday use case. No palette or gameplay changes are made by these notes.

Shared setup: [Blender workflow](../../docs/technical/BLENDER_WORKFLOW.md).
