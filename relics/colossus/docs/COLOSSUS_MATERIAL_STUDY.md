# Colossus — shape-locked material and salvage study

**Historical study A.** The user requested more visible copper salvage after
reviewing this version. [Study B](COLOSSUS_MATERIAL_STUDY_B.md) is now visually
accepted: 25,423 copper blocks, 90 raw iron items, and checked post-mining support.

October 2, 2026. The user approved studying lower-value materials with the
**complete accepted V4.1 form preserved**. This candidate's palette and salvage
quantities await review; it does not replace the accepted original automatically.

[Material comparison and post-salvage view](../design/generated/colossus-v4-1-materials/colossus-material-comparison-review.png)
· [Three salvage sites](../design/generated/colossus-v4-1-materials/colossus-salvage-sites-review.png)
· [Study configuration](../design/studies/colossus-v4-1-materials.json)

## Exact geometry preservation

This is a **direct block-state remap of the accepted V4.1 NBT/schematic**, not a
new voxelization. Independent checks compare complete occupied position sets:

- **181 × 209 × 235**, exactly **223,161 occupied blocks**, ground Y77, DataVersion 3105.
- **Zero added, removed or moved positions.** All empty spaces remain identical.
- All **491 original Blender meshes** retain their vertices, faces, transforms
  and material-slot assignments. Only the source material colors change; salvage
  guides are non-rendering empties.
- All **85,087 original nonmetal block states** are unchanged.
- The palm-up hand, fingers, thumb, rear breaches, helmet, abdomen and selected
  chest frame retain their accepted geometry.

The editable source depicts the bulk palette. Exact retained-metal positions
are a reproducible post-export mask stored in the design metadata; the source
render is labeled accordingly. The actual-NBT views show the final assignments.

## Candidate bulk materials

| Original block | Replacement outside salvage clusters | Intended visual role |
| --- | --- | --- |
| Exposed copper | Polished granite | Warm weathered armour mass |
| Exposed cut copper | Light gray terracotta | Muted brown plate surfaces |
| Cut copper | Terracotta | Warmer rims and trim |
| Weathered copper | Green terracotta | Darker olive patina-colored surfaces |
| Raw iron block | Andesite | Cool worn edges and exposed damage |

This changes the visual material treatment and survival resource value, not
the underlying shape. Source material names still identify the old component
roles. No new lore about the original machine's literal construction is implied.

## Resource inventory and salvage proposal

| Resource | Original V4.1 | Study | Reduction |
| --- | ---: | ---: | ---: |
| Copper-based placed blocks | 129,253 | **197** | **99.85%** |
| Raw iron blocks | 8,821 | **10** | **99.89%** |
| Raw iron items represented by those blocks | 79,389 | **90** | **99.89%** |

Copper counts are placed-block totals, not ingot-equivalent claims. Oxidized and
cut copper types have different crafting/recovery implications. These quantities
are a concrete study proposal, not approved final survival balance.

Three existing component regions retain original metal states:

| Region | Retained metal | Source-space center |
| --- | ---: | --- |
| Detached forearm fitting | **128 copper blocks** | (48, 26, −88) |
| Open chest machinery | **69 copper blocks** | (17, 24, −17) |
| Rear breach remnants | **10 raw iron blocks** | (10, 37, 44) |

Each site uses one face-connected group seeded at the nearest eligible original
metal block within its configured sphere. Caps are 128 / 96 / 24; smaller existing
connected groups stay smaller rather than introducing scattered ore to fill the
quota. No extra blocks, containers or routes are created.

The hypothetical salvage previews remove only those **207** retained metal
blocks. **222,954 blocks (99.907%) remain**. These previews demonstrate the effect
of targeted metal recovery; the published study export itself retains every
original position. Ordinary mining of the replacement materials is still possible.
This study does not implement protection, replenishment or multiplayer rewards.

## Reproduce and verify

Use the existing Blender/Python environment and local legacy texture atlas.
ObjToSchematic is **not rerun** for this palette-only derivative.

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/create_colossus_material_study.py
python tools/inspect_colossus_material_study.py
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config relics/colossus/design/studies/colossus-v4-1-materials.json
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/render_colossus_material_details.py
python tools/review_colossus_materials.py
python -m unittest discover -s tests -p test_colossus_materials.py -v
```

The dedicated inspector checks baseline hashes, exact grid/void conservation,
schematic/NBT equality including origin/DataVersion, unchanged nonmetal states,
salvage connectivity, absence of metal outside the three masks, resource counts,
hand/rear/chest probes and lossless reconstruction from **127 tiles**. Unit tests
cover disconnected salvage candidates and independent schematic round trips with
nontrivial axes, offsets, air and multi-byte palette indices.

The study exports **14 block types** and records provenance in `.design.json`
and `verification.json`; it deliberately has no fabricated `.ots.json` report.
The config lives under `design/studies/` because this is not an OBJ conversion.
Editable source, whole NBT/schematic and review images follow the existing Git
publication policy. Tiles, render scenes and individual renders stay local.

Actual Minecraft appearance, survival salvage balance and access remain to be
reviewed. Alpha 3 still uses V3. The unique-large-site and gameplay systems are
separate pending integration work.
