# Gameplay interiors — builder handoff

October 8, 2026. User-authorized implementation of the **structure-builder scope**
in worktree `Relic-Mod-interiors`, branch `feat/gameplay-interiors`, based on
`5925987`. Five new architectural candidates are delivered. The current catalog,
Alpha 4.9 artifacts and all original exports remain unchanged. Gameplay integration
and visual acceptance are separate follow-up gates.

## Deliverables

- [Five-design review](reviews/gameplay-interiors-review.png)
- [Machine-readable handoff index](reviews/gameplay-interiors-handoff.json)
- [26.2 block/property registry excerpt and provenance](reviews/gameplay-registry-26.2.json)

| Design | Revision and files | Geometry review | Exact marker plan |
| --- | --- | --- | --- |
| Large Colossus | [V5 interiors](../../relics/colossus/design/generated/colossus-v5-interiors/) | [Cutaways](../../relics/colossus/design/generated/colossus-v5-interiors/colossus-v5-interiors-review.png) | [Plan](../../relics/colossus/design/generated/colossus-v5-interiors/colossus-v5-interiors-markers-review.png) |
| Small Colossus | [V8 interiors](../../relics/colossus/design/generated/small-colossus-v8-interiors/) | [Cutaways](../../relics/colossus/design/generated/small-colossus-v8-interiors/small-colossus-v8-interiors-review.png) | [Plan](../../relics/colossus/design/generated/small-colossus-v8-interiors/small-colossus-v8-interiors-markers-review.png) |
| Ruined Tower | [V8 interiors](../../relics/ruined-tower/design/generated/ruined-tower-v8-interiors/) | [Cutaways](../../relics/ruined-tower/design/generated/ruined-tower-v8-interiors/ruined-tower-v8-interiors-review.png) | [Plan](../../relics/ruined-tower/design/generated/ruined-tower-v8-interiors/ruined-tower-v8-interiors-markers-review.png) |
| Obelisk | [V5 archaeology](../../relics/obelisk/design/generated/obelisk-v5-archaeology/) | [Excavations](../../relics/obelisk/design/generated/obelisk-v5-archaeology/obelisk-v5-archaeology-review.png) | [Plan](../../relics/obelisk/design/generated/obelisk-v5-archaeology/obelisk-v5-archaeology-markers-review.png) |
| World Tree | [V5 refuge](../../relics/world-tree/design/generated/world-tree-v5-refuge/) | [Roots/heart](../../relics/world-tree/design/generated/world-tree-v5-refuge/world-tree-v5-refuge-review.png) | [Plan](../../relics/world-tree/design/generated/world-tree-v5-refuge/world-tree-v5-refuge-markers-review.png) |

Each folder contains `<stem>.nbt`, `.schem`, `.gameplay.json`, `.design.json`,
`<stem>-source.blend`, review PNGs and `verification.json`. Dimensions, local origin
and ground datum match its Alpha 4.9 raw baseline exactly. Generated tiles,
manifests, individual images and grouping intermediates remain local/reproducible.

### Large Colossus

One cockpit deck at raw Y168 carries **five player-scale station remnants**,
small seats/consoles and short floor conduits within the existing helmet. The
east-facing hatch `[118,169,182]` has a recognizable raised frame and threshold;
players supply their own climb. The normal-golem envelope is `[94,169,183]`, trial
placeholder `[94,169,193]`, and Vault placeholder `[84,169,190]`.

A separate service passage through the broken elbow reaches the arm chest
`[110,78,70]`. Original palm/fingers and body cavity remain exact. Copper/raw-iron
limits are rechecked. This architectural revision changes local geometry; the
original shape-preserving material-B study is preserved separately.

### Small Colossus

The V7 ground-v3 baseline was substantially solid. Bounded internal cuts now expose
a torn breast entry, broken load ribs, salvage recess and stripped upper cockpit
shell reached by maintenance steps. There are **no intact operator stations**,
trial or Vault. The copper-chest placeholder `[73,19,80]` is the single per-site
magnet-role location. Thickened entry treads join the surviving body.

### Ruined Tower

The lower hall contains partition remains, a broad entrance, five distinct
Enderman positions with normal headroom, and one chest marker. The wall-side
ascent rises from raw Y15 to Y174 with five deliberate missing sections. It is
not continuously walkable to the upper marker: players must bridge/build. The
upper landing is a destination, not an extra reward. The unfinished V7 exterior
is the starting form.

### Obelisk

Two exterior excavation areas combine masonry edges, broken low visitor-wall
traces and **eight supported brushing locations**. Six are common finds; the other
two carry trim/map roles. Sand placeholders become suspicious sand at integration;
their tops are accessible. Original terracotta and the monument above Y16 stay exact.

### World Tree

The accepted V4.3 strands baseline gains **29 spaced shroomlights, 67 supported
lichen patches, seven short berry strands and three root-adjacent firefly bushes**.
All lie at raw Y24–38, below the maximum 15 blocks above ground Y24. The lighting
scope is `[44,23,55]` through `[138,39,139]`, independent of the gameplay aura.
The entire tree above Y39 remains exact.

One radius-three ordinary amethyst sphere is embedded at `[94,29,93]`, with a
small viewing slit. It has no budding blocks or control logic. The aura marker
`[94,24,93]` is independent of the sphere's survival. There is no Tree clearing
region: the slit is omitted-air source geometry under the existing terrain policy.
Final terrain, block light and vegetation interactions need actual integration tests.

### Skulls

All five current skull exports retain their catalog hashes. There are no skull
revisions, gameplay sidecars or additional clear regions.

## Source workflow and integration

These are **block-exact architectural derivatives** of maintained NBTs using the
existing deterministic schematic/NBT serializer. The Blender-to-voxel art is not
globally revoxelized: interior work must not shift armour, branches or ground joins.
`tools/build_gameplay_interiors.py` maintains the grouped edits. Blender sources
contain editable state/group surface meshes and named marker empties. Coordinates
are `(X,-Z,Y)` from raw-template Minecraft XYZ, one unit per block. Smooth baseline
Blender sources remain preserved. Mesh edits do not automatically update NBT:
change the maintained builder and rebuild to retain block states and sidecar binding.

No source entities, block-entity payloads or explicit air boxes are embedded.
Integration replaces these ordinary placeholders using marker roles:

| Role | Source placeholder | Intended injected block |
| --- | --- | --- |
| Colossus/small/Tower chest | Waxed cut copper | Selected copper chest with finite data |
| Colossus trial | Chiseled deepslate | Scoped trial spawner |
| Colossus Vault | Polished blackstone | Scoped Vault |
| Archaeology | Sand | Suspicious sand with role-specific loot |

The [marker contract](../technical/GAMEPLAY_MARKERS.md) adds optional
**`arm_clearance`** for the independent elbow passage, with the existing bounded
allow-list/preservation rules. The future loader must recognize it explicitly.
Region boxes are work envelopes, **not instructions to erase authored solids**;
skip source occupied cells when clearing native terrain. No water/lava clearing.
Apply actual padding, Minecraft rotation/pivot and owning-chunk actions during
integration. Sidecars contain raw coordinates only.

The original **DataVersion 3105 remains recorded**, not relabeled as migration.
Final block names/properties are checked against a hash-pinned 26.2 registry
summary. Firefly bushes make this a 26.2-first handoff, not a 1.21.1 backport.
Registry checks are not runtime loading evidence.

## Reproduction

Using host Python/Pillow and the existing Blender installation:

```powershell
python tools/build_gameplay_interiors.py all
python tools/prepare_gameplay_registry.py
python tools/validate_gameplay_handoff.py
python -m unittest discover -s tests -p test_gameplay_handoff.py -v

# Repeat for colossus, small_colossus, ruined_tower, obelisk and world_tree:
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --threads 6 --python-exit-code 1 --python tools/render_gameplay_interiors.py -- colossus

python tools/review_gameplay_interiors.py
python tools/review_gameplay_markers.py
python tools/finalize_gameplay_handoff.py
```

Rendering reuses `.work/foliage-preview-atlas` from the existing pipeline. A fresh
machine needs the pinned OTS atlas and `prepare_foliage_preview.py`, as in the V1
workflow. No Minecraft/Modrinth installation or user-world edit was performed here.

## Checks and remaining gates

Completed builder checks cover hashes, bounds, target block/property validity,
marker cardinalities, supported/open placeholders, entity headroom/floors,
path-to-reward reachability, intentional stair interruption, new architecture's
face connection to surviving source, schematic equality and tile reconstruction.
Six focused tests include corrupt sidecars and obstructed spawn fixtures.

Pictures render actual NBT. Cut faces are inspection boundaries, not removed roofs.
Cyan envelopes show mob size. Plant silhouettes and moss-texture proxies for
luminous growth are approximate; Blender emission is **not a block-light test**.

Remaining integration/acceptance: visual approval, target-version loading,
rotation/padding, actual terrain and light tests, chunk-local clearing/injection,
finite loot/entities, trial/Vault, Tree effects and the gameplay acceptance matrix.
Production selection stays on the tested Alpha 4.9 catalog until reviewed integration.
