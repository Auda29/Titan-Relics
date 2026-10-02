# Titan Skull V4 — broken deposits and biome palettes

October 2, 2026. Offline design exports, awaiting visual acceptance and game integration.

[Four-variant review](../design/generated/titan-skull-v4-dry/titan-skull-v4-variants-review.png)
· [V3/V4 comparison](../design/generated/titan-skull-v4-dry/titan-skull-v4-changes-review.png)
· [German revision brief](TITAN_SKULL_V4.md)

## Implemented design

All **62 anatomy meshes** from the checked-in V3 source are preserved, including
the crown, nine vertebrae, two fractures and loose bone fragments. The scale stays
at 0.996998996 blocks/source unit, approximately 76 blocks for the skull itself.
Bone block and calcite now make the skull read as a fossil, with darker mineral
areas and small moss accents.

The continuous hill and stone rim are replaced by separate, asymmetric deposits.
Their tops and foundations taper toward the edges; dense interior slices keep
them solid without globally filling the skull cavities. Open terrain gaps cross
the deposits at source Z54 and Z131. Terrain drops from **244,825 to 116,438
blocks (52.44% less)**. Lower vertebral bodies remain partly buried.

Every variant is **117 × 79 × 179**, **136,569 blocks**, **31 tiles**, nominal
ground **NBT Y8**, DataVersion **3105**. The smaller footprint comes from the
terrain replacement, not rescaling the anatomy.

## Why four variants

The [variant specification](../design/variants/titan-skull-v4.json) splits the
original earth family into two materially different surfaces:

| Export | Surface | Proposed use |
| --- | --- | --- |
| `titan-skull-v4-meadow` | Grass with coarse-earth patches over dirt | Plains, sunflower plains, meadow, blooming valley/plateau, prairie |
| `titan-skull-v4-dry` | Mostly coarse earth, sparse grass over dirt | Savanna, steppe, scrubland |
| `titan-skull-v4-sand` | Sand over sandstone | Future explicitly admitted desert setting |
| `titan-skull-v4-rock` | Stone and gravel | Future explicitly assigned, sufficiently level stony setting |

The first two cover the existing biome tag. Sand and rock fulfill the requested
additional settings; they are not enabled by current worldgen. Snow and red sand
are unnecessary unless snowy biomes or Badlands are added later. Mod-biome mapping
is a design proposal, not verified placement compatibility.

All four have identical occupied coordinates and identical non-terrain block
states. Material proxies isolate terrain from the fossil palette during export.
Covered grass becomes dirt; unsupported sand/gravel becomes sandstone/stone.
The meadow export contains 7,619 grass blocks, versus 1,222 in the dry export.

## Reproduce

Use the existing local Blender and pinned ObjToSchematic setup described in
[Blender workflow](../../../docs/technical/BLENDER_WORKFLOW.md). From repository root:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/create_titan_skull_v4.py
foreach ($variant in @('meadow','dry','sand','rock')) {
    $stem = "titan-skull-v4-$variant"
    $out = "relics/titan-skull/design/generated/$stem"
    $config = "relics/titan-skull/design/$stem.json"
    node tools/obj_to_schem.cjs $config
    python tools/schem_to_nbt.py "$out/$stem.schem" "$out/$stem.nbt" --air omit --tile-size 32
    & 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config $config
    python tools/inspect_ots_result.py --config $config
}
python tools/inspect_relic_v4.py --sheets
```

The final sheet command also requires rendered Obelisk V3/V4 and Skull V3 previews;
omit `--sheets` to run just the cross-variant check. Generating V4 requires the
checked-in V3 `.blend`, not regeneration of earlier designs.

## Validation and limits

Passed source/export hashes, schematic/NBT equality, palette/bounds checks and
lossless tile reconstruction for all variants. All 10,111 terrain columns have
no missing interior cells. Checks cover terrain gaps, partial burial of all nine
vertebrae, bone fractures, rear skull wall, mouth/eye cavities, supported falling
blocks, uncovered grass and cross-variant anatomy equality.

The review images render actual NBT in Blender. Surrounding terrain is illustrative;
the legacy atlas lacks grass, so its preview uses dirt sides and a tinted moss-grain
top. Actual exports contain `grass_block[snowy=false]`, with normal in-game biome tint.

`--air omit` preserves existing terrain in empty positions; cavity checks do not
prove cleared walkable spaces. Biome selection, slope-aware placement and game
validation remain integration work. Alpha 3 still selects V3.
