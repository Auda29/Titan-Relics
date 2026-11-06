# Project images

## Colossus icon

At the author's request, `titan-relics-icon.png` now shows the large Colossus
from their [river screenshot](../../relics/colossus/demo/colossus-v3-shaders-river.png).
It is a 400 × 400 crop of a real Minecraft shader capture from 1 October 2026.
The image shows **Colossus V3**, an earlier model, rather than the current beta
candidate. It is an interim icon until newer captures are supplied.

Only cropping and resizing were applied. The scene, lighting and blocks are
unchanged; no generative image tool was used. Reproduce with FFmpeg:

```sh
ffmpeg -hide_banner -loglevel error -y \
  -i relics/colossus/demo/colossus-v3-shaders-river.png \
  -vf 'crop=300:300:790:440,scale=400:400:flags=lanczos,format=rgb24' \
  -compression_level 9 -pred mixed \
  -frames:v 1 assets/branding/titan-relics-icon.png
```

Crop coordinates are measured from the original image's top-left corner.
The author's original project work is covered by the root MIT license to the
extent they hold the rights. Minecraft and any shader assets retain their own
rights. The shader pack and settings were not recorded.

## Interim title image and gallery

Use the original PNGs below for Modrinth. The **river view**
is the featured image and the opening image in both platform descriptions and
the repository README. The other two are supporting gallery images. The
[capture notes](../../relics/colossus/demo/README.md) document their provenance.

CurseForge's media uploader rejects images of 2 MB or larger, as confirmed by
the author's upload dialog. Use the smaller PNG copies in
`build/platform-preparation/curseforge-bilder-unter-2mb.zip` for that gallery.
They are 1280 × 702 RGB PNGs, 964,056–1,150,800 bytes each. The full dashboard
package has also been updated to contain these copies under the original
filenames. Repository originals and existing Modrinth images are unchanged.

Reproduce each copy with FFmpeg, replacing `river` with `savanna` or `landscape`
for the other views:

```sh
ffmpeg -hide_banner -loglevel error -y \
  -i relics/colossus/demo/colossus-v3-shaders-river.png \
  -vf 'scale=1280:-2:flags=lanczos,format=rgb24' \
  -compression_level 9 -pred mixed -frames:v 1 \
  build/platform-preparation/curseforge-upload/colossus-v3-shaders-river-curseforge.png
```

| Image | Use | English caption |
| --- | --- | --- |
| [River view](../../relics/colossus/demo/colossus-v3-shaders-river.png) | Featured / title image | Large Colossus across the river. In-game shader capture, 1 October 2026. Earlier Colossus V3 model; interim preview. |
| [Savanna approach](../../relics/colossus/demo/colossus-v3-shaders-savanna.png) | Gallery | Approaching the large Colossus through the savanna. In-game shader capture, 1 October 2026. Earlier Colossus V3 model; interim preview. |
| [Landscape overview](../../relics/colossus/demo/colossus-v3-shaders-landscape.png) | Gallery | Large Colossus in the coastal savanna. In-game shader capture, 1 October 2026. Earlier Colossus V3 model; interim preview. Other visible structures are not identified as Titan Relics assets. |

These images do not establish current world generation, Survival acceptance or
shader compatibility. Replace the icon and these interim images when the author
supplies current captures. The source screenshots remain preserved byte-for-byte.

## Retained former icon source

`obelisk-delapouite.svg` is the **Obelisk** icon by **Delapouite**, downloaded
from [Game-icons.net](https://game-icons.net/1x1/delapouite/obelisk.html).
It is licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/),
not under the project's MIT license.

The SVG is retained as the former temporary icon source. It is no longer the
current PNG icon. Keep its attribution and license link when distributing it.
