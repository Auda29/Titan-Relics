# Colossus v3 — reference design with a buried hip

Updated: October 1, 2026.

## Reference and design decisions

The design follows the **opening 0–5 seconds** of
[Archaean Colossi — The Archive In Between](https://www.instagram.com/reel/DaoBxUEiBNa/).
The video was inspected for this study. Extracted frames are stored locally under
`.work/references/` and are not tracked in Git.

| Reference feature | Colossus v3 interpretation |
| --- | --- |
| Broad, almost hill-shaped bronze armor | Large curved torso and dominant shoulder shells |
| Round helmet with a narrow dark slit | Dome helmet with a cut-out visor |
| Heavy curved pipes below the chin and side filters | Ribbed respirator hose, outlet, and concentric filter housings |
| Aged warm metal, rust, and green deposits | Copper palette, brown terracotta, patina, and moss patches |
| Irregular forehead and lower-shoulder damage | Jagged openings with recessed mechanisms |
| Lower body disappearing into hills | Deep body shell, partly hidden in the landscape presentation |
| Long tubular forearm and hand in the foreground | Detached ringed forearm in the same structure coordinate system |

The back and hidden mechanisms are design additions: the opening scene only shows
a front three-quarter view. The first experiment's large central chest ring was
replaced with a deep, irregular rupture.

## Scale and verified export

The original **[Colossus v2](COLOSSUS_V2.md)** is **160 blocks** tall, compared
with 66 for the first Blender experiment. Adding the buried abdomen and torn hip
increases the overall height to **209 blocks**, while preserving the above-ground
scale with a rounding change of approximately **0.095%**.

This remains a **scale assumption**, not a measured reference dimension. The
foreground person and distant Colossus cannot be compared directly by pixel height.
Helmet/body proportions, arm length, and vegetation provide visual guidance.

In source units, the body is roughly 190 wide, the helmet 60–70 tall, and the
detached arm including its hand about 110 long. These are rounded design measures;
**the exported dimensions in `colossus-v3.manifest.json` are authoritative**.

| Metric | Colossus v3 |
| --- | --- |
| Overall X/Y/Z, including detached arm | **181 × 209 × 227 blocks** |
| Placed blocks | **221,221** |
| Used block types | **11** |
| Nonempty 32-block tiles | **124** |
| Blocks below the nominal surface | **85,432** |
| Nominal surface height in NBT | **Y ≈ 77** |

At that ground plane, approximately **132 block layers** remain above ground.
[Obelisk v3](OBELISK_V3.md) exposes 177 layers, rising about 45 blocks (34%) higher
over terrain despite its shorter total export height of 185 blocks. This relative
scale is a design choice, not a measurement recoverable from the separate references.

All block positions and states match between `.schem` and `.nbt`; tiles reconstruct
the whole template without loss. The original Blender experiment was also checked
against its unchanged checksums.

The footprint includes the gap between body and arm. The size-comparison preview
shows the selected asset beside the first 66-block Blender Colossus at the same
block scale. A two-block figure near the arm provides another comparison.
Landscape, figure, and surface markers are presentation-only.

## Underground continuation

Chest armor continues below the former cut line. A narrowing armored abdomen
reaches a partly preserved hip. Outer and inner armor surfaces and exposed wall
thickness are modeled at the rupture. Internal supports extend from the existing
torso to uneven broken ends, with exposed conduits. There are no legs.

The intended ground plane is approximately NBT Y **77**, about 77 blocks above
the lowest surviving support. This design datum still needs to be translated into
worldgen placement. `colossus-v3-underground-review.png` shows the exposed body,
a turquoise ground plane, and a section of the actual hip NBT.

A comparison against the pre-extension source confirmed the same **47,886 vertices
above source Y 20**. The added lower body is included in `.schem` and `.nbt`, not
just in the landscape view.

## Reproduce

See [Blender workflow](BLENDER_WORKFLOW.md) for setup. From the repository root:

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
& $blender --background --python-exit-code 1 --python tools/create_colossus_v3.py
node tools/obj_to_schem.cjs design/colossus-v3.json
python tools/schem_to_nbt.py design/generated/colossus-v3/colossus-v3.schem design/generated/colossus-v3/colossus-v3.nbt --air omit --tile-size 32
& $blender --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config design/colossus-v3.json
python tools/inspect_ots_result.py --config design/colossus-v3.json
```

Important outputs in `design/generated/colossus-v3/`:

- `colossus-v3-source.blend`: editable model with named components.
- `colossus-v3.obj`, `colossus-v3.schem`, `colossus-v3.nbt`: conversion outputs.
- `colossus-v3.design.json`: reference, scale assumption, and source bounds.
- `colossus-v3.ots.json`, `colossus-v3.manifest.json`, `verification.json`: export and validation metadata, including hashes.
- `colossus-v3-blocks.blend`: actual NBT geometry with a packed texture atlas.
- `colossus-v3-landscape.blend`: NBT plus a separate presentation landscape.
- `colossus-v3-review.png`: source and block-export views.
- `colossus-v3-reference-review.png`: reference crop, landscape, and scale comparison; requires the configured local reference frame.
- `05-blocks-landscape.png`, `06-size-comparison.png`: full-size presentation views.
- `07-buried-body.png`, `08-hip-detail.png`: exposed body and actual underground block detail.
- `colossus-v3-underground.blend`, `colossus-v3-underground-review.png`: inspection scene and labeled overview.

Copy the generated source before manually editing it. Running the generator again
overwrites generated files with matching names.

## Integration status

This is a visual asset prototype. Previews read NBT geometry and render it in
Blender; they are not Minecraft screenshots or proof of natural placement.

The pipeline still uses surface voxelization, omitted air, and legacy DataVersion
3105. Before game integration, review wall thickness, interior air, copper
oxidation states, and material quantities. The larger footprint and deeper burial
also require new site checks, height limits, template references, and build source
selection. The existing alpha build continues to generate its earlier Colossus.
