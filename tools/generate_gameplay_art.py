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
    for leggings in (False, True):
        image = Image.new('RGBA', (64, 32)); draw = ImageDraw.Draw(image)
        # Vanilla humanoid UV faces, independently drawn upright/angular branches.
        faces = [(4,20,7,31),(20,20,23,31)] if leggings else [(8,8,15,15),(20,20,27,31),(44,20,47,31),(4,20,7,31),(20,20,23,31)]
        for x0,y0,x1,y1 in faces:
            x = (x0+x1)//2
            draw.line([(x,y0+1),(x,y1-1)], fill=(224,224,224,255))
            draw.line([(x,y0+3),(x0,y0+1)], fill=(160,160,160,255))
            draw.line([(x,y1-4),(x1,y1-2)], fill=(160,160,160,255))
        if leggings:
            draw.line([(22,20),(22,29)],fill=(224,224,224,255))
            draw.line([(22,24),(26,21)],fill=(160,160,160,255))
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
