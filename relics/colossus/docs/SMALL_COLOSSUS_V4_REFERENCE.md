# Small Colossus V4 — new primary reference

October 4, 2026. The user rejected V3 as too skeleton-like and explicitly requested
a new smaller Colossus based on this reel:

**[Vigilant-Class Archaean Colossi — The Archive In Between](https://www.instagram.com/reel/Da-s0zqi7OQ/)**

The public caption calls it an educational broadcast from the Pale Lodge about
Vigilant-Class Archaean Colossi. This replaces the archive-based V1, large-machine
likeness V2 and slender exposed-frame V3 as the next small design's primary brief.

## Evidence inspected

The 111.75-second, 768 × 1366 video was retrieved with the existing yt-dlp/FFmpeg
tools. The full clip was sampled every six seconds (0–108 s); additional frames
were extracted at 0, 1.5, 3, 4.5, 16, 18, 80, 84, 105 and 110 seconds. The opening
0/3 s, hangar view at 18 s, active variant at 84 s and closing 110 s were also
inspected at full resolution. Original video, timestamps, contact sheets and
SHA-256 extraction records stay local under `.work/references/small-colossus-v4/`.

### Primary motif: the dormant specimen at 0–4.5 seconds

- A very substantial rounded upper body and large head-like housing rest against
  a rocky slope. Heavy plating covers the body; it is not an exposed framework.
- Two prominent dark oval optical lenses, two smaller upper lenses and smaller
  cheek ports create a multi-optic face. There is no single horizontal visor slit.
- A protruding central housing ends in an arched, vertically ribbed grille.
- The casing has fine incised lines, panel boundaries, rivets and warm aged-metal
  coloration with localized deposits and growth.
- The foreground limb has a broad domed hand/gripper casing with circular ports
  and large curved, blade-like pincers rather than human fingers.
- The rock, perspective, foreground explorer and cropped body obscure full-body
  proportions and limb connections. They do not provide a calibrated block scale.

### Secondary views and limits

The 18 s hangar scene supports the ornate metal/optical/grille language and shows
broad continuous armour, armored abdomen and banded joints. Its multi-arm anatomy
is not proof that the partly hidden opening specimen has the identical arrangement.
The 84 s active creature and the partially logo-covered closing view are separate
variants/context, not orthographic views to combine into one measured body.

## Minecraft translation

V4 uses the dormant opening specimen as its silhouette/face/gripper target:
an enlarged multi-optic head, a thick continuous torso, protected shoulders,
short visible joint sections and grounded pincer assemblies. Keep exposed
machinery local to joints, rather than a skeletal chest and thin waist.

The rear, buried lower completion, second arm attachment, exact pincer tine count
and local soil contacts are authored completions. The whole cliff, explorer and
cosmic scenes are presentation context. Absolute size is a design choice near
the existing smaller-family height, approximately 75 visible blocks.

Warm terracotta/mineral blocks supply the aged-metal impression; real copper is
limited to accents and couplings. Use broad closed forms, lens relief, a real
grille and sparse readable incisions before fine decorative surface detail.
Model in Blender, then check and review actual exported NBT blocks.

## Local reproduction

```powershell
yt-dlp --no-playlist --write-info-json -o '.work/references/small-colossus-v4/%(id)s.%(ext)s' 'https://www.instagram.com/reel/Da-s0zqi7OQ/'
python tools/study_small_colossus_v4.py
python tools/study_small_colossus_v4.py --times 0 1.5 3 4.5 16 18 80 84 105 110 --label details
```

Pillow is needed for contact sheets. Reference media stays excluded from Git;
published reviews should show our modeled/exported geometry.
