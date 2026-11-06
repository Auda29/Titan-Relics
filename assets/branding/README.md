# Project icon

`obelisk-delapouite.svg` is the **Obelisk** icon by **Delapouite**, downloaded
from [Game-icons.net](https://game-icons.net/1x1/delapouite/obelisk.html).
It is licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/),
not under the project's MIT license.

`titan-relics-icon.png` is a 400 × 400 raster export of the unchanged white-on-black
SVG, made with CairoSVG 2.8.2. No generative image tool was used. This is a usable
initial project icon and can be replaced by a later dedicated brand design.
Keep the source attribution and license link when distributing either file.

Reproduce the export with CairoSVG installed:

```python
import cairosvg
cairosvg.svg2png(url='assets/branding/obelisk-delapouite.svg',
                write_to='assets/branding/titan-relics-icon.png',
                output_width=400, output_height=400)
```
