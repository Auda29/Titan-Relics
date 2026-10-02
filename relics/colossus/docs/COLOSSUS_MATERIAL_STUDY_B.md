# Colossus material study B — salvageable armour

The user found the initial 197-copper study too restrictive and its salvage
damage almost invisible. The revised requirement is **fewer than 50,000 copper
blocks and fewer than 256 raw iron items**, with visibly changed but plausible
remains after mining. The intact accepted V4.1 form must remain exact.

## Review and files

- [Intact versus fully salvaged comparison](../design/generated/colossus-v4-1-materials-b/colossus-materials-b-comparison-review.png)
- [Metal-location diagram, rear and forearm details](../design/generated/colossus-v4-1-materials-b/colossus-materials-b-salvage-map-review.png)
- [Configuration](../design/studies/colossus-v4-1-materials-b.json)
- [NBT](../design/generated/colossus-v4-1-materials-b/colossus-v4-1-materials-b.nbt)
  / [Schematic](../design/generated/colossus-v4-1-materials-b/colossus-v4-1-materials-b.schem)
  / [Editable Blender source](../design/generated/colossus-v4-1-materials-b/colossus-v4-1-materials-b-source.blend)
- [Verification](../design/generated/colossus-v4-1-materials-b/verification.json)
- [Initial low-metal study A](COLOSSUS_MATERIAL_STUDY.md), preserved for comparison.

**Visually accepted by the user on October 2, 2026:** “ja so sieht das gut aus”.
Study B is the selected material version, including the illustrated post-salvage
appearance: **25,423 copper blocks and 90 raw iron items**, with the complete
intact V4.1 geometry preserved. The original V4.1 and study A remain available.
The packaged mod still uses the V3 assets; this approval records the asset choice.

Review images and generation metadata retain their pre-approval review labels;
this acceptance entry records the subsequent user decision.

## Resource inventory

| Resource | Accepted V4.1 | Study A | Study B | User limit |
| --- | ---: | ---: | ---: | ---: |
| Copper-based placed blocks | 129,253 | 197 | **25,423** | **<50,000** |
| Raw iron blocks | 8,821 | 10 | **10** | At most 28 under the item limit |
| Raw iron items represented | 79,389 | 90 | **90** | **<256** |

Study B includes 10,641 exposed copper, 12,827 exposed cut copper, 1,728 weathered
copper and 227 cut copper blocks. Counts refer to placed blocks, not equivalent
copper ingots. Iron is explicitly budgeted as raw iron **items**: 10 blocks × 9.

## Where copper is retained

| Existing armour region | Copper blocks |
| --- | ---: |
| Front left cuirass panel | 2,885 |
| Front right cuirass panel | 3,254 |
| Rear cuirass panels | 4,502 |
| Near shoulder outer plating | 4,021 |
| Far shoulder outer plating | 4,649 |
| Detached forearm sleeve plating | 1,947 |
| Buried lower front armour | 4,165 |
| **Total** | **25,423** |

The original small rear-breach iron remnant retains ten raw iron blocks.
Large copper areas open the chest/shoulder shell and forearm sleeve when mined;
their permanent ribs, backing, joints and intervening armour remain. The head,
neck, upper chest bridge (source Y75 and above) and hand contain no recoverable
metal. The source-space panel masks are component-scale bounds, not scattered
random ore. Copper keeps its original V4.1 block state and weathering.

Outside these masks, the earlier warm bulk palette remains: polished granite,
light gray terracotta, terracotta, green terracotta and andesite. All original
nonmetal states remain unchanged.

## Shape and post-salvage support

The intact export has **223,161 blocks**, **181 × 209 × 235**, DataVersion 3105,
ground Y77 and **127 tiles**. It is a direct remap of accepted V4.1, with **zero
added, removed or moved positions** and all **491 source meshes** preserved.

The proposed panel volumes initially contain 31,474 copper blocks. Connectivity
analysis makes 6,051 of those positions permanent low-value backing instead of
recoverable metal. Shortest backing paths are widened one face-neighbor layer
within existing geometry. No supporting geometry is added.

After simulated removal of all 25,423 copper and ten raw iron blocks:

- **197,728 blocks remain (88.60%)**.
- The head remains face-connected through the neck and torso to the buried body.
- All **64,313 blocks** at source Y75 and above remain present.
- **No surviving original face-connected component splits**. Existing baseline
  raster fragments may remain or be fully salvaged; none are newly separated.
- The largest component changes from 159,084 to 141,173 blocks. The original
  export already has 8,236 face-connected components; 7,281 survive salvage.
  This is explicitly a relative-connectivity check, not a claim that the original
  export was a single connected solid or a physical structural simulation.

The before/after renders show actual NBT block positions with matching cameras.
The amber/gray map is explicitly false-color to reveal exactly which blocks can
be salvaged. Terrain is illustrative; no Minecraft installation or local in-game
test is involved. The post-salvage views are simulations, not modified exports.

## Reproduction

No new voxelization is performed. The editable source depicts the bulk palette;
non-rendering guides mark regions, while exact copper/iron assignments and
permanent backing are recorded in `.design.json` and the authoritative exports.

```powershell
$config = 'relics/colossus/design/studies/colossus-v4-1-materials-b.json'
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/create_colossus_material_study.py -- --config $config
python tools/inspect_colossus_material_study.py --config $config
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config $config --blocks-only
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/render_colossus_material_details.py -- --config $config
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/render_colossus_panel_details.py
python tools/review_colossus_panels.py
python -m unittest discover -s tests -p test_colossus_materials.py -v
```

The dedicated inspector checks exact occupied/empty positions, baseline hashes,
state mapping, schematic/NBT equality, lossless tile reconstruction, hard resource
caps, original hand/chest/rear probes and independently labeled before/after
face-connectivity. A bridge test checks that salvage retains necessary support
without inventing connections between pre-existing disconnected pieces.
