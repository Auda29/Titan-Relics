# Small Colossus V1

Status: **first exported candidate for the independent smaller design**.

- [Four-view review](../design/generated/small-colossus-v1/small-colossus-v1-review.png)
- [Hand/rear details](../design/generated/small-colossus-v1/small-colossus-v1-detail-review.png)
- [Blender source](../design/generated/small-colossus-v1/small-colossus-v1-source.blend)
- [NBT](../design/generated/small-colossus-v1/small-colossus-v1.nbt) / [Schematic](../design/generated/small-colossus-v1/small-colossus-v1.schem)
- [Configuration](../design/small-colossus-v1.json) / [Verification](../design/generated/small-colossus-v1/verification.json)

**Actual export: 101 × 76 × 87, 36,623 blocks, ten block types, 20 tiles.**
Nominal ground is NBT Y9, leaving approximately 67 visible blocks. Planning
envelope: 99 × 76 × 88; added deposits/voxel rounding explain the slight difference.

## Archive relationship

This loads the [archived first concept](../archive/first-concept/README.md) and
writes a new destination. **40 original meshes** retain their geometry,
transforms and material-slot fingerprints, including the angular helmet and
compact supported body. The archive file hash is checked and preserved.

Changes are a modest rear torso breach, a proper palm-up right hand with four
curled fingers and thumb, a buried lower torso continuation, snapped lower
supports and local deposits. The old right palm/fingers/thumb are replaced.
The hand frame has determinant +1 and an upward palmar normal. Fingertip probes
and chest/rear void probes are checked against the exported blocks.

Dark structural material keeps this distinct from the large bronze Colossus.
The limited weathered-cut-copper chest accents come from the archive; there is
no bulk raw iron. Existing small wooden archive shelter elements remain as visual
reuse, without assigning a reward or gameplay system.

Review priorities: compact silhouette versus the archive, hand readability after
burial, and the new rear opening. This repeated-family design does not inherit
the large site's Core/Magnet/unique-world policy. It is not yet visually accepted.

Reproduce with `python tools/build_new_relic_v1.py small-colossus`. See the
[brief](SMALL_COLOSSUS_DESIGN_STUDY.md) and [shared V1 workflow](../../../docs/project/NEW_RELICS_V1.md).
