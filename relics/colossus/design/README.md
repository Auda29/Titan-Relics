# Colossus design assets

- [V3 configuration](colossus-v3.json) and [outputs](generated/colossus-v3/)
- [V2 configuration](colossus-v2.json) and [outputs](generated/colossus-v2/)
- [Original experiment configuration](colossus-ots.json) and [outputs](generated/ots/)

Configurations use repository-root-relative paths. Blender generators and shared
conversion/rendering tools remain in `tools/`; reproduction commands are in the
[design documentation](../docs/COLOSSUS_V3.md).

Generated sources are overwritten by regeneration. Preserve manual edits in a
separate `blender/` source folder before running generators again.
