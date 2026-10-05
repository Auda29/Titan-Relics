# Next four relics — reference, scale and damage study

October 2, 2026. Scope requested by the user: evaluate the references and establish
size, proportions and destruction level for all four designs **before Blender**.
This page and the linked briefs establish recommended working dimensions, not
user-approved models or exported bounds. No model or structure was generated.

**Subsequent step:** the user then requested V1s for all four. See the
[new V1 assets and measured exports](NEW_RELICS_V1.md). This page retains the
original planning dimensions as the comparison baseline.

**October 4 small-Colossus update:** the user later rejected the slender V3 as too
skeletal and selected a new [Vigilant-Class primary reference](../../relics/colossus/docs/SMALL_COLOSSUS_V4_REFERENCE.md).
The archive-based proportions below remain historical V1 planning.

## Recommended working sizes

All dimensions are **X width × Y height × Z depth, in Minecraft blocks**. The
site envelope includes the relic, local debris/root spread and planned burial;
it does not include a whole landscape, coastline or cavern. Heights are rounded
design extents, not measurements of the fictional world shown in the videos.

| Relic | Planned site envelope | Above nominal ground | Main proportions | Damage target |
| --- | --- | ---: | --- | --- |
| [Ruined Tower](../../relics/ruined-tower/docs/REFERENCE_DESIGN_STUDY.md) | **112 × 192 × 96** | **180** | Main tower 56 wide × 48 deep; height/width ≈3.2 | Heavy; 30–35% of reconstructed exterior wall area missing |
| [World Tree](../../relics/world-tree/docs/REFERENCE_DESIGN_STUDY.md) | **192 × 216 × 176** | **208** | Crown 192 × 176; trunk foot 44 × 38; root spread 112 × 104 | Living and mostly intact; one lost major side branch, <5% major woody volume missing |
| [Smaller Colossus](../../relics/colossus/docs/SMALL_COLOSSUS_DESIGN_STUDY.md) | **99 × 76 × 88** | **66** | Main shoulder span ≈76; helmet 24 × 20 × 22 | Moderate; 20–25% reconstructed outer armour area missing; one detached right forearm |
| [Titan Skull 2](../../relics/titan-skull/docs/TITAN_SKULL_2_CONCEPT.md) | **104 × 144 × 116** | **132**, including sword | Skull 82 wide × 76 tall × 90 deep, 64 visible; sword rises another ≈68 | Local impact + erosion; 12–18% reconstructed bone volume missing |

The damage percentages are **authoring targets with different denominators**,
not measured reference damage, fill fractions or mutually comparable scores.
Natural cavities, detached-but-present limbs, foliage gaps and burial are not
counted as missing material. Actual inventories follow only after modeling.

### Scale hierarchy

- The smaller Colossus stays at the archive's approximately 66-block height above
  ground, about half the large Colossus's ≈132 visible blocks; it is a different
  compact design rather than a miniature of the accepted diving-helmet Colossus.
- Skull 2's **bone alone** is about the large Colossus's helmet scale. The sword,
  not a larger head, gives the complete site its 132-block visible height.
- The tower is a slender architectural landmark; the World Tree is the broadest
  and tallest above-ground proposal. Crown mass, not only a fat trunk, establishes
  its scale.
- Future placement must check build height. With a highest allowed block Y319
  and a 16-block design margin, conservative nominal-ground ceilings are about
  Y123 for the tower and Y95 for the tree. These are placement requirements, not
  changes to the current world's height or terrain generator.

## What was actually inspected

| Reference | Inspected frames / evidence | Main limitation |
| --- | --- | --- |
| [Tower / Josh White](https://www.instagram.com/reel/DbqXYoVx2hR/) | 0–28 s, sampled every 2 s; 0 s enlarged | Roof/top stays cropped throughout the useful shot; depth and original height cannot be measured |
| [World Tree / The Archive In Between](https://www.instagram.com/reel/DaBgsX0C9s4/) | 0–48 s every 3 s, then 51–105 s every 6 s; 6, 21, 48, 57 s enlarged | Montage shows changing tree/branch arrangements; no consistent multi-view reconstruction |
| Smaller Colossus | Archived source and actual-NBT review, original Colossus reference stills 01/04, archived generator dimensions | Archive is the primary shape reference; the original reel is family/style context, not a new small-body measurement |
| [Skull 2 / The Archive In Between](https://www.instagram.com/reel/Db9KCtWi0eG/) | 0, 0.5, 1, 2, 3, 4, 5, 6, 8, 10, 15, 20 s; 1 and 5 s enlarged | Selected motif is the opening ≈0–6 s; sword pommel and skull rear are not fully visible |

Important findings:

1. **Tower:** the large object to the right departs during the clip. It is an
   aircraft, not a permanent tower annex. The broken upper termination must be
   designed because the source never reveals it.
2. **Tree:** use an irregular, layered cypress-like crown and a twisted fluted
   trunk. Buildings, carved stones and water passages provide context rather than
   a requirement to reproduce the entire montage as one continuous site.
3. **Smaller Colossus:** keep the archive's angular helmet, circular chest rupture
   and compact supported body. Do not replace that identity with the large
   Colossus's round helmet and longer sleeve proportions.
4. **Skull 2:** the identifying feature is a **huge sword embedded diagonally in
   the overgrown cranium**, within a damp cavern/grotto. It is not another crowned
   skull. The reference's cavern is a setting requirement to interpret, not a
   reason to copy an entire enclosed cave into the relic export.

## Evidence and publication

Original videos, downloaded metadata, timestamped PNGs, contact sheets and the
local four-relic comparison board are under `.work/references/` and stay local.
The public repo stores these observations, source URLs and design decisions.
The local board uses actual reference frames and the **existing** archived
Colossus render; it is not a preview of new models.

Local video SHA-256 values and extraction timestamps are recorded in
`.work/references/four-studies-manifest.json`. Extraction used existing `yt-dlp`
and FFmpeg installations, without Blender or new Minecraft installations.

## Handoff boundary

The four linked briefs give one concrete starting design each, including what is
observed, what is inferred, and what is newly authored. Hidden-side geometry,
actual block quantities and later playable routes cannot be validated from a
reference sheet. All accepted Colossus/Obelisk/Skull exports remain the baseline.
V5 rooms, stairs, encounters, rewards and worldgen remain later work. The next
modeling session should use these dimensions as its starting specification after
the user has reviewed them; this task itself ends at reference/design evaluation.
