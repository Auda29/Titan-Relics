# Four new relics — V1 asset review

October 2, 2026. The user requested V1 models for all four designs following the
[reference/size study](NEXT_FOUR_RELIC_DESIGN_STUDY.md). These are new **visual
review candidates**, separate from the accepted large Colossus, Obelisk and
crowned Titan Skull. The playable Alpha 3 build still selects the three V3 assets.

## Review

### User feedback — October 4, 2026

- **Titan Skull 2:** visually accepted for now; the user likes the current V1.
- **Small Colossus:** revision required. V1 still resembles the original test
  Colossus too closely; the archive-preservation brief needs to be reconsidered.
  The user selected an independent relative of the accepted large Colossus,
  sharing its visual language with different proportions and pose.
- **World Tree:** revision required. The current tree does not look natural enough.
- **Ruined Tower:** the user selected **220 blocks above nominal ground**, at
  approximately the existing width.

These are visual review decisions. The dimensions below describe the existing
V1 exports; game integration is still pending.

See the [October 4 V2 revisions](RELICS_V2_REVIEW.md) for the resulting new candidates.

| Asset | Actual X × Y × Z | Blocks | Ground Y |
| --- | --- | ---: | ---: |
| Ruined Tower | 111 × 192 × 93 | 276,868 | 12 |
| World Tree | 193 × 216 × 169 | 503,048 | 9 |
| Small Colossus | 101 × 76 × 87 | 36,623 | 9 |
| Titan Skull 2 | 105 × 144 × 107 | 85,224 | 12 |

- [Four-relic overview](reviews/new-relics-v1-review.png)
- [All seven current relics at the same scale](reviews/all-current-relics-scale.png)
- [Ruined Tower V1](../../relics/ruined-tower/docs/RUINED_TOWER_V1.md)
- [World Tree V1](../../relics/world-tree/docs/WORLD_TREE_V1.md)
- [Small Colossus V1](../../relics/colossus/docs/SMALL_COLOSSUS_V1.md)
- [Titan Skull 2 V1](../../relics/titan-skull/docs/TITAN_SKULL_2_V1.md)

Each asset has an editable `*-source.blend`, whole `.schem` and `.nbt`,
`.design.json`, `.ots.json`, `verification.json`, a four-view review and a detail
review. Source material names are semantic and map to Minecraft blocks through
the per-asset configuration. OBJ/MTL, tiles, manifests, individual views and
render scenes stay local under the existing publication policy.

The overview uses **actual exported NBT geometry**, individually framed rather
than shown at a common scale. Surrounding terrain and two-block visitors are
illustrations; authored local deposits belong to the exports. These are Blender
renders, not Minecraft screenshots. Original reference frames are not embedded
in the published review.

## Reproduction

The seven-relic scale comparison is reproduced with
`python tools/render_all_relics_scale.py`. It uses the accepted Colossus material
B, Obelisk V4.2 and meadow Skull V4 alongside these four V1s, all at unit block
scale under one orthographic camera. Each asset meets the same nominal ground;
buried portions are hidden. Dimensions include the buried parts. The other three
Skull V4 terrain palettes have identical dimensions and are represented by meadow.

Use the existing Blender 5.2/Python/Node environment and the pinned local
ObjToSchematic checkout. From the repository root:

```powershell
python tools/build_new_relic_v1.py all
python tools/review_new_relic_v1.py
```

The builder also accepts `tower`, `tree`, `small-colossus` or `skull-2`. It runs
the corresponding Blender generator, pinned OBJ conversion, Java NBT conversion
with `--air omit --tile-size 32`, actual-block renders, the dedicated inspector,
and close detail renders. `--skip-model` reuses the generated OBJ; it does not
skip voxelization. The optional `--blender` argument selects an existing executable.
The four independent asset builds can run in parallel with reduced `--threads`.

All exports retain **DataVersion 3105**. The main workflow is unchanged:
Blender → OBJ → ObjToSchematic → Sponge schematic → Java NBT. Source geometry is
not replaced by an unrelated hand-authored NBT generator.

### Geometry and materials

- **Tower:** closed structural wall volumes are explicitly filled with the wall
  block. Real hall/sky openings remain exterior-connected and empty.
- **Tree:** dense internal slices fill the trunk, branches and roots. Foliage
  uses overlapping shelves/edge cushions instead of a solid-filled leaf mountain.
  The exporter uses semantic proxies for unsupported atlas leaf names, then writes
  native `spruce_leaves`/`oak_leaves` with `persistent=true` and log axis states.
- **Small Colossus:** loads the archived editable source into a new destination,
  retains 40 original mesh fingerprints, revises only the old hand/one rear break,
  and adds a buried lower completion plus local deposits.
- **Skull 2:** independently generated rounded cranium, jaw and weapon; it does
  not reuse the first skull's crown, lateral horns or nine-vertebra spine.

The legacy texture atlas lacks oak/spruce leaves. `prepare_foliage_preview.py`
creates a **separate local preview atlas** from the legacy atlas plus two 16px
leaf textures from the public Minecraft asset mirror. No Minecraft installation
is performed, and the pinned converter checkout is unchanged. Fixed preview
tints and opaque leaf rendering approximate in-game foliage; grass tint is also
approximate. Texture URLs/hashes are stored locally in
`.work/foliage-preview-atlas/provenance.json`. Exports contain native blocks.

## Checks and boundaries

`inspect_new_relic_v1.py` checks source/export hashes, exact schematic/NBT state
and coordinate equality, palette inventories, bounds and lossless reconstruction
from tiles. It additionally probes real cavities and structural members, checks
solid trunk samples/persistent leaves, checks archive preservation and right-hand
orientation, and verifies blade sections above and below the skull entry.

The output dimensions are measured from the actual voxel grid. The original
planning table described rounded site envelopes; horizontal extents can differ
slightly due to source bounds, tapering deposits and voxelization. Damage
percentages remain design targets, not falsely reported measured destruction.

This V1 pass establishes exterior form, material language and major geometric
openings. It does not claim finished traversal: `--air omit` leaves existing
terrain untouched at absent cells, so worldgen must later clear designated
entrances/interiors. V5 stairs, halls, rooms and authored routes, encounter/reward
systems, natural placement and in-game review remain subsequent work.
