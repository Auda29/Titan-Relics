# World Tree

> **Current status, October 30, 2026:** World Tree V5, grounded plants, Regeneration II/Resistance II in an 80-block sphere and bounded natural animal attempts are integrated. See the
> [Alpha 5.0.3 status and roadmap](../../docs/project/CURRENT_STATUS_AND_ROADMAP.md). Approved design requirements
> remain specifications; dated pending/unimplemented claims below are historical
> where superseded by the released implementation and linked evidence.

## Historical planning record

**Lore approved October 8:** the Titans worshipped this tree and received strength
and size from it. The Colossi's builders tried and failed to destroy it. Thousands
of years later no living Titans remain; current inhabitants reuse the relics.
Present-day gameplay is selected in the [gameplay plan](gameplay/README.md);
worship/attack traces remain optional art rather than required new edits.
The current gameplay direction is a peaceful
source of life, with more pigs/chickens/sheep/cows through modest local natural
spawning, **no animal spawners or farm-like refill**, natural-looking lights to
reduce darkness-dependent hostile spawning, and a trunk-focused benefit. Ordinary
hostiles keep natural rules; no barrier/despawn system is selected. The effect is
reward enough, with no Tree chest/item. Approved starting values are
Regeneration II and Resistance II within 80 blocks, refreshed during the stay and lasting five
minutes after leaving. The selected 80-block sphere works through walls and
persists at its saved original anchor even after complete Tree removal; copies
create no aura. Technical refresh/effect merging and natural spawn defaults are
in the [runtime contract](../../docs/technical/GAMEPLAY_RUNTIME.md), awaiting tests;
additional effects are not selected. No code or
new geometry has been implemented by this planning.

**Lighting direction:** glow berries, glow lichen, firefly bushes and sparse
shroomlights, restricted to the trunk/base and root area. Growth reaches at most
15 blocks up the trunk, unevenly and naturally; no upper-branch/crown lights.
At ground level it spreads broadly and irregularly around the trunk and roots
to reduce dark spawnable areas beneath the canopy. Exact spread/positions remain
open and are not automatically the aura's 80-block radius. The user selected
**one small amethyst sphere inside the trunk at its bottom/base**, rather than
scattered optional clusters. It is decorative and mineable, without budding amethyst
or regrowth, and does not control the persistent aura. Exact builder design remains pending.

**World Tree V4.3 strands and its current Alpha 4.9 terrain integration were
visually accepted by the user on October 7, 2026.** Five new Tree screenshots
show the base, crown, roots and cave opening; see the
[acceptance record](../../docs/project/reviews/alpha4-9-user-acceptance-20261007.json).
The existing model and bounded-contact policy remain unchanged; gameplay is
outside this visual acceptance.

**Alpha 4.9 selects V4.3 strands.** Accepted art and world pose remain unchanged
under the same +12 Y export translation and ground Y24. Replace the later broad
37,005-cell extrusion with 1,883 face-connected wood cells along 50 tapering
strand/fork paths. Only short contacts of up to two cells within the three-block
surface band are bridged; deep roots and longer cave openings remain open. See
[candidate provenance](../../docs/testing/CAVE_CONTACTS_20261007.md) and
[current runtime evidence](../../docs/testing/ALPHA_4_9_TEST_REPORT.md).

**Alpha 4.8 selects V4.2 rooted.** Accepted wood and foliage are retained under
a uniform +12 Y export translation, with 37,005 face-connected low wood additions.
Ground Y24 places the accepted art four blocks deeper; exposed low roots continue
using their own wood state, not dirt pillars. Authored soil/moss platforms are
removed without closing higher intentional root arches. See
[candidate provenance](../../docs/testing/ROOTED_EMBEDDING_20261007.md) and
[current runtime status](../../docs/testing/ALPHA_4_8_TEST_REPORT.md).

Historical candidate: [V4.1 ground-v3](../../docs/project/EMBEDDING_20261006.md)
lowers the regular moss pads into broken ground patches. Accepted wood and
foliage remain exact exported-block matches.

**V4's form and foliage were accepted on October 6.** V4.1 adds only narrow
earth transitions at root contacts; its validator requires identical non-terrain
blocks. See the [ground audit and follow-up](../../docs/project/GROUND_WEATHERING_20261006.md).
Packaged Alpha 4.6 uses V4.1 ground-v3; its
[runtime status](../../docs/testing/ALPHA_4_6_TEST_REPORT.md) separately checks low
moss edits, root contacts and buried undersides. Accepted wood and foliage remain
identical, not every moss cell. Alpha 4.5's ground-v2, Alpha 4.4's V4.1 and
Alpha 4.3's V4 evidence remain historical.

- [V2 natural-growth revision](docs/WORLD_TREE_V2.md)
- [V1 exports, review and reproduction](docs/WORLD_TREE_V1.md)

The [reference/size study](docs/REFERENCE_DESIGN_STUDY.md) establishes a working
192 × 216 × 176 envelope, including a 208-block-tall living tree above ground.

- [Design documentation status](docs/README.md)
- [Design asset status](design/README.md)
- [Gameplay planning status](gameplay/README.md)

Its original motif remains in the shared
[concept catalog](../../docs/project/Minecraft-Relikte-Modplan.md).
