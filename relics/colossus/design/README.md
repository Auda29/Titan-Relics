# Colossus design assets

- [Small Colossus V1 configuration](small-colossus-v1.json) and [export/review guide](../docs/SMALL_COLOSSUS_V1.md): separate smaller design derived from the preserved archive

- Selected material version: [Study B / salvageable armour](studies/colossus-v4-1-materials-b.json), [acceptance and support checks](../docs/COLOSSUS_MATERIAL_STUDY_B.md); 25,423 copper blocks and 90 raw iron items; visually accepted October 2, 2026

- [Material/salvage study](studies/colossus-v4-1-materials.json) and [exact-shape verification](../docs/COLOSSUS_MATERIAL_STUDY.md): direct V4.1 block remap, no new voxelization

- [V4.1 palm-up frame configuration](colossus-v4-1-frame.json) and [revision guide](../docs/COLOSSUS_V4_1.md)

- Selected V4: [B — open machine frame](colossus-v4-frame.json).
  [A — open chest](colossus-v4-open.json) remains a comparison alternative;
  [comparison and commands](../docs/COLOSSUS_V4_EXPORTS.md).

- [V3 configuration](colossus-v3.json) and [outputs](generated/colossus-v3/)
- [V2 configuration](colossus-v2.json) and [outputs](generated/colossus-v2/)
- [Archived first concept](../archive/first-concept/), reserved as the basis for a
  second, smaller Colossus, with its configuration, model, and exports preserved.

Configurations use repository-root-relative paths. Blender generators and shared
conversion/rendering tools remain in `tools/`; reproduction commands are in the
[design documentation](../docs/COLOSSUS_V3.md).

Generated sources are overwritten by regeneration. Preserve manual edits in a
separate `blender/` source folder before running generators again.
