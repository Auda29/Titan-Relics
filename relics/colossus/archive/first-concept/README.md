# Archived first Colossus concept

Archived: October 1, 2026.

This is the original **99 × 66 × 71-block** Blender concept (26,169 placed blocks),
formerly stored in the Colossus `design/generated/ots/` directory. It is preserved
as the starting point for a **second, smaller Colossus**. The current large
Colossus design remains [V3](../../docs/COLOSSUS_V3.md).

The smaller Colossus is a future design direction. The
[reference/size study](../../docs/SMALL_COLOSSUS_DESIGN_STUDY.md) now proposes a
99 × 76 × 88 site retaining the archive's compact identity and 66-block visible
height, with moderate damage and a buried lower completion. These are working
design values, not a new accepted model. Gameplay remains open. Create a separate
working copy/configuration when modeling begins so this archive is retained.

The subsequent [Small Colossus V1](../../docs/SMALL_COLOSSUS_V1.md) now exists in
its own generated folder and preserves this archive. It retains 40 original
meshes and revises the hand/rear damage while adding buried lower completion.

**Occurrence decision, October 2, 2026:** the large Colossus is intended to be
unique per game world; smaller Colossi may occur multiple times. This archived
baseline is for that separate repeatable design direction. Its rarity and loot
remain open; it does not automatically inherit the large site's core vault or
magnet reward. This is documentation, not an implemented generation change.

## Preserved files

- [Review sheet](generated/colossus-review.png)
- [Editable Blender source](generated/colossus-source.blend)
- [Whole NBT template](generated/colossus.nbt)
- [Sponge schematic](generated/colossus.schem)
- [Converter configuration](colossus-ots.json)
- [Export provenance](generated/colossus.ots.json)
- [Verification record](generated/verification.json)

All local intermediate files, render scenes, backups, and tiles were moved with
the published outputs. They retain the existing Git exclusion policy. No model
geometry or export bytes were changed by archiving.

## Reproduction

Run from the repository root after the shared
[Blender setup](../../../../docs/technical/BLENDER_WORKFLOW.md). These commands
overwrite matching archive outputs; make a working copy before editing manually.

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
& $blender --background --python-exit-code 1 --python tools/create_blender_colossus.py
node tools/obj_to_schem.cjs relics/colossus/archive/first-concept/colossus-ots.json
python tools/schem_to_nbt.py relics/colossus/archive/first-concept/generated/colossus.schem relics/colossus/archive/first-concept/generated/colossus.nbt --air omit --tile-size 32
& $blender --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config relics/colossus/archive/first-concept/colossus-ots.json
python tools/inspect_ots_result.py --config relics/colossus/archive/first-concept/colossus-ots.json
```

`tools/create_blender_colossus.py` remains in the shared tools directory because
later relic generators import its geometry helpers. Default original-concept
rendering/inspection and Colossus size-comparison paths now use this archive.
