"""Portfolio of four actual-NBT V1 renders; source reference media is not embedded."""
import json
from pathlib import Path

from PIL import Image,ImageDraw,ImageFont
from build_new_relic_v1 import ASSETS,ROOT


def font(size,bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',size)


def main():
    image=Image.new('RGB',(2600,3700),'#eee9de');draw=ImageDraw.Draw(image)
    draw.text((48,24),'FOUR NEW RELICS / V1',font=font(50,True),fill='#293934')
    draw.text((48,94),'Actual exported Minecraft blocks rendered in Blender / first visual review',font=font(30),fill='#54615a')
    titles=['RUINED TOWER','WORLD TREE','SMALL COLOSSUS','TITAN SKULL 2']
    summaries=['Broken vertical shell / authored crown / grounded piers',
               'Living layered crown / twisted trunk / root arches',
               'Preserved archive identity / compact right hand',
               'Rounded skull / embedded sword / open cavities']
    for i,(relic,stem,_) in enumerate(ASSETS.values()):
        out=ROOT/'relics'/relic/'design'/'generated'/stem
        report=json.loads((out/'verification.json').read_text())
        x=40+i%2*1300;y=175+i//2*1730
        draw.text((x,y),f'{i+1:02} / {titles[i]}',font=font(35,True),fill='#293934')
        pic=Image.open(out/'05-blocks-landscape.png').convert('RGB');pic.thumbnail((1220,1460),Image.Resampling.LANCZOS)
        image.paste(pic,(x+(1220-pic.width)//2,y+60))
        size=' × '.join(map(str,report['size']))
        draw.text((x,y+1540),f'{size} / {report["blocks"]:,} blocks',font=font(30,True),fill='#293934')
        draw.text((x,y+1590),summaries[i],font=font(25),fill='#54615a')
        draw.text((x,y+1633),f'{report["palette_entries"]} block types / {report["tiles"]} tiles / checks passed',font=font(25),fill='#54615a')
    draw.text((48,3650),'V1 review candidates. Views framed individually. Surrounding terrain/visitors are illustrative; game integration is pending.',font=font(24),fill='#54615a')
    out=ROOT/'docs/project/reviews/new-relics-v1-review.png';out.parent.mkdir(parents=True,exist_ok=True);image.save(out);print(out)


if __name__=='__main__':main()
