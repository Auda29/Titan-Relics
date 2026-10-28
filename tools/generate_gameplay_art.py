"""Original deterministic pixel art for relic items and Monolith armor UV masks.

No structure exports or downloaded textures are modified/copied. Pillow is needed
only to reproduce the committed PNG files, not by the mod or ordinary packaging.
"""
import json
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1] / 'src/main/resources/assets'
ASSETS = ROOT / 'relics'
COLORS = {'.': (0, 0, 0, 0), 'd': '#332d36', 'c': '#a65e37', 'b': '#d68b4f',
          'h': '#f5bf78', 'i': '#b4c0c6', 's': '#626d79', 'v': '#9b61de',
          'l': '#e1b5ff', 'e': '#473756', 'p': '#ddd0b3', 'w': '#f3e9d2'}
SPRITES = {
    'machine_core': [
        '................','.....dddddd.....','...ddbbbbbbdd...','..dbhhbbbbbbc d..'.replace(' ', ''),
        '..dbddddddddcd..','..dbdvvvvvvdcd..','..dh dvllllvdcd..'.replace(' ', ''), '..dbdvlvv lvdcd..'.replace(' ', ''),
        '..dbdvlvv lvdcd..'.replace(' ', ''),'..dbdvllllvdcd..','..dbdvvvvvvdcd..','..dbddddddddcd..',
        '..dcbbbbbbbccd..','...ddccccccdd...','.....dddddd.....','................'],
    'salvage_magnet': [
        '................','................','...ddddddddddd..','..diiibbbbbbbcd.',
        '..dishbbbbbbbcd.','..dishdddddbbcd.','..dishdvvvdbbcd.','..dishdv lvdbbcd.'.replace(' ', ''),
        '..dishdvvvdbbcd.','..dishdddddbbcd.','..dishbbbbbbbcd.','..diiiccccccccd.',
        '...ddddddddddd..','................','................','................'],
    'colossus_key': [
        '................','.....dddddd.....','....dhbbbbcd....','....dbdvvdcd....',
        '....dbdlvdcd....','....dbddddcd....','.....dbbcd......','......dbcd......',
        '......dbcd......','......dbbdd.....','......dbbhcd....','......dbddd.....',
        '......dbbhcd....','......dddddd....','................','................'],
    'monolith_armor_trim_smithing_template': [
        '................','...dddddddddd...','..dwwwwwwwwwpd..','..dwhhhhhhhhpd..',
        '..dwpbbbbbbppd..','..dwppbv bppppd..'.replace(' ', ''),'..dwppbvlbpppd..','..dwppbvvbpppd..',
        '..dwppbvlbpppd..','..dwppbvvbpppd..','..dwppbvlbpppd..','..dwppbbbbpppd..',
        '..dwpppppppppd..','..dppppppppppd..','...dddddddddd...','................']}

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

def generate():
    for name, rows in SPRITES.items():
        # Transparent right padding is explicit; drawing never resizes the sprite.
        if len(rows) != 16 or any(len(row) != 16 for row in rows): raise ValueError(name)
        variants = ['', '_partial', '_empty'] if name in ('machine_core', 'salvage_magnet') else ['']
        for variant in variants:
            image = Image.new('RGBA', (16, 16))
            for y, row in enumerate(rows):
                for x, color in enumerate(row):
                    if variant == '_empty' and color in 'vl': color = 'e'
                    if variant == '_partial' and color in 'vl' and y > 7: color = 'e'
                    image.putpixel((x, y), ImageColor(color))
            target = ASSETS / 'textures/item' / f'{name}{variant}.png'
            target.parent.mkdir(parents=True, exist_ok=True); image.save(target)
            write_json(ASSETS / 'models/item' / f'{name}{variant}.json',
                       {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'relics:item/{name}{variant}'}})
            write_json(ASSETS / 'items' / f'{name}{variant}.json',
                       {'model': {'type': 'minecraft:model', 'model': f'relics:item/{name}{variant}'}})
    generate_trim()

def trim_mask(leggings=False):
    """One-pixel fractured vertical details on verified 26.2 equipment UV faces."""
    image=Image.new('RGBA',(64,32));draw=ImageDraw.Draw(image)
    main=(192,192,192,255);branch=(128,128,128,255)
    def stem(x,y,height,side=1):
        draw.line([(x,y),(x,y+height-1)],fill=main)
        draw.point((x+side,y+1),fill=branch)
    if leggings:
        # Waist fragments and upper-leg marks stop before the native boot area.
        for x,side in ((21,1),(26,-1),(33,1),(38,-1)):stem(x,28,2,side)
        for x in (18,29):draw.point((x,29),fill=branch)
        for x in (1,5,9,13):stem(x,21,4,1)
    else:
        # Helmet face opening stays clear; each side/back receives a short mark.
        stem(10,9,2,-1);stem(13,9,2,1)
        for x,side in ((3,-1),(20,1),(26,1),(29,-1)):stem(x,10,3,side)
        # Separate chest columns, with no neck, belt or shared leg-UV overpaint.
        stem(21,24,5,1);stem(26,24,5,-1)
        stem(34,23,5,-1);stem(37,23,5,1)
        stem(18,24,4,-1);stem(29,24,4,1)
        # Pauldrons occupy the upper arm only; boot marks start at the ankle.
        for x in (41,45,49,53):stem(x,21,3,1)
        for x in (1,5,9,13):stem(x,27,3,1)
    return image

def generate_trim():
    for leggings in (False, True):
        image=trim_mask(leggings)
        target = ASSETS / 'textures/trims/entity' / ('humanoid_leggings' if leggings else 'humanoid') / 'monolith.png'
        target.parent.mkdir(parents=True, exist_ok=True); image.save(target)
    materials = ['amethyst','copper','copper_darker','diamond','diamond_darker','emerald','gold','gold_darker','iron','iron_darker','lapis','netherite','netherite_darker','quartz','redstone','resin']
    write_json(ROOT / 'minecraft/atlases/armor_trims.json', {'sources': [{
        'type':'minecraft:paletted_permutations', 'palette_key':'minecraft:trims/color_palettes/trim_palette',
        'permutations':{m:f'minecraft:trims/color_palettes/{m}' for m in materials},
        'textures':['relics:trims/entity/humanoid/monolith','relics:trims/entity/humanoid_leggings/monolith']}]})

def ImageColor(color):
    if isinstance(COLORS[color], tuple): return COLORS[color]
    value = COLORS[color].lstrip('#'); return tuple(int(value[i:i+2],16) for i in (0,2,4))+(255,)

def preview(destination):
    image = Image.new('RGB', (900, 700), '#161b22')
    draw = ImageDraw.Draw(image)
    title = ImageFont.load_default(size=24)
    label = ImageFont.load_default(size=16)
    draw.text((28, 20), 'Relic gameplay - original pixel art', fill='#f0e7d9', font=title)
    draw.text((28, 52), 'Source-art preview only; not a Minecraft rendering test.', fill='#aeb8c7', font=label)
    rows = [('machine_core', 'Machine Core'), ('salvage_magnet', 'Salvage Magnet')]
    for row, (name, caption) in enumerate(rows):
        draw.text((28, 101+row*167), caption, fill='#f0e7d9', font=label)
        for column, (suffix, state) in enumerate([('', 'Full'), ('_partial', 'Partial'), ('_empty', 'Depleted / broken')]):
            x, y = 260+column*180, 95+row*167
            sprite = Image.open(ASSETS / 'textures/item' / f'{name}{suffix}.png').resize((112,112),Image.Resampling.NEAREST)
            image.paste(sprite,(x,y),sprite)
            draw.text((x,y+120),state,fill='#aeb8c7',font=label)
    for column, (name, caption) in enumerate([('colossus_key','Colossus Key'),('monolith_armor_trim_smithing_template','Monolith Template')]):
        x, y = 50+column*215, 433
        sprite=Image.open(ASSETS/'textures/item'/f'{name}.png').resize((112,112),Image.Resampling.NEAREST)
        image.paste(sprite,(x,y),sprite);draw.text((x,y+120),caption,fill='#f0e7d9',font=label)
    for row, kind in enumerate(['humanoid','humanoid_leggings']):
        mask=Image.open(ASSETS/'textures/trims/entity'/kind/'monolith.png').resize((256,128),Image.Resampling.NEAREST)
        image.paste(mask,(565,390+row*130),mask)
    draw.text((545, 670), 'Monolith UV masks (not worn armor)',fill='#aeb8c7',font=label)
    destination.parent.mkdir(parents=True,exist_ok=True); image.save(destination)

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview',type=Path)
    args=parser.parse_args()
    generate()
    if args.preview: preview(args.preview)
