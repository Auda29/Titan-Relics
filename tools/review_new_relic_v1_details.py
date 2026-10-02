"""Compose detail reviews using host Python/Pillow, separate from Blender's Python."""
import argparse
import json
from pathlib import Path

from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('config',type=Path)
    config=json.loads(parser.parse_args().config.read_text());output=ROOT/config['output']
    out,stem=output.parent,output.stem
    views=json.loads((out/'detail-views.json').read_text())
    sheet=Image.new('RGB',(2400,1150),'#eee9de');draw=ImageDraw.Draw(sheet)
    def font(n):return ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
    draw.text((40,24),config['title']+' / DETAIL INSPECTION',font=font(42),fill='#293934')
    for i,view in enumerate(views):
        pic=Image.open(out/view['image']).convert('RGB');pic.thumbnail((1140,855))
        x=40+1180*i;sheet.paste(pic,(x,130));draw.text((x,1000),view['label'],font=font(27),fill='#293934')
    draw.text((40,1080),'Actual-NBT crops. Cut faces are inspection boundaries; the complete export is not cut away.',font=font(26),fill='#54615a')
    path=out/f'{stem}-detail-review.png';sheet.save(path);print(path)


if __name__=='__main__':main()
