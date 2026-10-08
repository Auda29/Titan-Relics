"""Local orthographic occupancy sections for precise interior authoring."""
import json
from pathlib import Path
from PIL import Image, ImageDraw
from inspect_ots_result import read_structure
from relic_catalog import ASSETS,ROOT

SLICES={'colossus':[77,90,135,157,165,175,185,195],
        'small_colossus':[13,18,25,35,45,55,65,72],
        'ruined_tower':[12,18,25,35,50,80,130,180],
        'world_tree':[24,26,30,35,40,45,50,65],
        'obelisk':[8,9,10,12,15,20,35,60]}

def main():
    out=ROOT/'.work/interiors';out.mkdir(parents=True,exist_ok=True)
    for name,levels in SLICES.items():
        a=ASSETS[name];root,blocks=read_structure(ROOT/a['source'])
        image=Image.new('RGB',(1600,850),'#eee9de');draw=ImageDraw.Draw(image)
        scale=min(350/root['size'][0],340/root['size'][2])
        for i,y in enumerate(levels):
            ox=40+(i%4)*400;oz=40+(i//4)*420
            draw.text((ox,oz-25),f'{name} / raw Y{y}',fill='black')
            for (x,yy,z),s in blocks.items():
                if yy!=y:continue
                color='#67745b' if any(k in s for k in ('leaves','moss','grass')) else '#977853' if any(k in s for k in ('copper','terracotta','log','wood','dirt')) else '#525b61'
                draw.rectangle((ox+x*scale,oz+z*scale,ox+(x+1)*scale,oz+(z+1)*scale),fill=color)
            for x in range(0,root['size'][0],10):
                draw.line((ox+x*scale,oz,ox+x*scale,oz+root['size'][2]*scale),fill='#bbbbbb',width=1)
                draw.text((ox+x*scale,oz),str(x),fill='red')
            for z in range(0,root['size'][2],20):
                draw.line((ox,oz+z*scale,ox+root['size'][0]*scale,oz+z*scale),fill='#bbbbbb',width=1)
                draw.text((ox,oz+z*scale),str(z),fill='red')
        image.save(out/f'{name}-sections.png')

if __name__=='__main__':main()
