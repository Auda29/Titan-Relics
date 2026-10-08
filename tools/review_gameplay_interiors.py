"""Compose actual-NBT builder reviews and the five-asset handoff overview."""
import json
from PIL import Image,ImageDraw,ImageFont
from build_gameplay_interiors import ROOT,ASSETS,STEMS

def font(n,bold=False):return ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',n)

def main():
    gallery=Image.new('RGB',(3200,2700),'#eee9de');g=ImageDraw.Draw(gallery)
    g.text((45,18),'GAMEPLAY INTERIORS / BUILDER HANDOFF',font=font(48,True),fill='#293934')
    g.text((45,80),'Versioned architectural candidates / actual NBT / runtime initialization remains with integration',font=font(28),fill='#54615a')
    for i,(name,stem) in enumerate(STEMS.items()):
        folder=(ROOT/ASSETS[name]['source']).parent.parent/stem
        d=json.loads((folder/(stem+'.design.json')).read_text());s=json.loads((folder/(stem+'.gameplay.json')).read_text())
        image=Image.new('RGB',(3200,1450),'#eee9de');draw=ImageDraw.Draw(image)
        draw.text((40,20),stem.upper(),font=font(46,True),fill='#293934')
        panels=[('01-overview.png','Exterior / current ground datum')]+[(f'0{j+2}-detail.png',v['label']) for j,v in enumerate(d['evidence']['views'])]
        for j,(file,label) in enumerate(panels):
            pic=Image.open(folder/file).convert('RGB');pic.thumbnail((1020,800));image.paste(pic,(40+j*1060,140))
            draw.text((40+j*1060,965),label,font=font(25),fill='#293934')
        text='  |  '.join(f'{m["role"]}: {m["pos"]}' for m in s['markers'])
        import textwrap
        for j,line in enumerate(textwrap.wrap(text,155)):
            draw.text((40,1040+j*36),line,font=font(27),fill='#54615a')
        draw.text((40,1370),'Detail views are cutaways. Cyan boxes show reserved mob size. Solid marker blocks are placeholders, not initialized gameplay.',font=font(28),fill='#54615a')
        image.save(folder/(stem+'-review.png'))
        pic=Image.open(folder/'02-detail.png').convert('RGB');pic.thumbnail((1000,750))
        x=45+(i%3)*1060;y=170+(i//3)*1170;gallery.paste(pic,(x,y))
        g.text((x,y+780),stem,font=font(28,True),fill='#293934')
        g.text((x,y+830),d['evidence']['views'][0]['label'],font=font(25),fill='#54615a')
        g.text((x,y+880),f'{len(s["markers"])} markers / {len(s["regions"])} bounded regions',font=font(27),fill='#54615a')
    g.text((2170,1610),'BOTH SKULLS',font=font(44,True),fill='#293934')
    g.text((2170,1690),'Preserved without changes',font=font(31),fill='#54615a')
    g.text((2170,1740),'No new markers or clear regions',font=font(28),fill='#54615a')
    g.text((45,2610),'Review candidates / native 26.2 states checked against registry report / in-game light and integration tests pending',font=font(30),fill='#54615a')
    path=ROOT/'docs/project/reviews/gameplay-interiors-review.png';gallery.save(path);print(path)

if __name__=='__main__':main()
