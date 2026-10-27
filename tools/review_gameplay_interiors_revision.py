"""Compose revision review sheets from rendered NBT and preserved V5 cockpit review."""
import json
from PIL import Image,ImageDraw
from build_gameplay_interiors import ROOT,ASSETS,STEMS as OLD
from build_gameplay_interiors_revision import STEMS
from review_gameplay_interiors import font
import review_gameplay_markers as markers

def main():
    markers.STEMS=STEMS;markers.main()
    for name,stem in STEMS.items():
        folder=(ROOT/ASSETS[name]['source']).parent.parent/stem
        d=json.loads((folder/(stem+'.design.json')).read_text())
        panels=[(Image.open(folder/'01-overview.png'),'Aussenansicht')]
        panels += [(Image.open(folder/f'0{i+2}-detail.png'),v['label']) for i,v in enumerate(d['evidence']['views'])]
        if name=='colossus':
            old=(ROOT/ASSETS[name]['source']).parent.parent/OLD[name]/(OLD[name]+'-review.png')
            old_cockpit=Image.open(old).crop((1100,140,2120,940))
            panels.append((old_cockpit,'V5 zum Vergleich: urspruenglich leeres Cockpit'))
            panels += [(Image.open(folder/'visor-inside.png'),'Visier von innen / zusaetzliches Prueflicht'),
                       (Image.open(folder/'visor-outside.png'),'Visier von aussen / zusaetzliches Prueflicht')]
            comparison=Image.new('RGB',(2200,970),'#eee9de');comp=ImageDraw.Draw(comparison)
            for x,pic,label in [(35,old_cockpit,'V5: bisheriges Cockpit'),(1135,Image.open(folder/'02-detail.png'),'V6: erhaltene Stationen und neue Aggregate')]:
                pic=pic.convert('RGB');pic.thumbnail((1030,770));comparison.paste(pic,(x,80))
                comp.text((x,860),label,font=font(27,True),fill='#293934')
            comparison.save(folder/(stem+'-comparison-review.png'))
        columns=2;rows=(len(panels)+1)//2
        image=Image.new('RGB',(2200,110+rows*870+80),'#eee9de');draw=ImageDraw.Draw(image)
        draw.text((35,18),stem.upper(),font=font(42,True),fill='#293934')
        for i,(pic,label) in enumerate(panels):
            x=35+(i%columns)*1080;y=90+(i//columns)*870
            pic=pic.convert('RGB');pic.thumbnail((1030,770));image.paste(pic,(x,y))
            draw.text((x,y+780),label,font=font(24),fill='#293934')
        draw.text((35,image.height-55),'Tatsaechliche NBT-Geometrie; Schnitte sind Ansichtsgrenzen, keine entfernten Daecher.',font=font(24),fill='#54615a')
        image.save(folder/(stem+'-review.png'))

if __name__=='__main__':main()
