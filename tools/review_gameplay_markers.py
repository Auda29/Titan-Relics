"""Top-down raw-coordinate marker plans; numerical legend is the sidecar key."""
import json
from PIL import Image,ImageDraw
from review_gameplay_interiors import font
from build_gameplay_interiors import ROOT,ASSETS,STEMS
from inspect_ots_result import read_structure

def main():
    for name,stem in STEMS.items():
        folder=(ROOT/ASSETS[name]['source']).parent.parent/stem
        sidecar=json.loads((folder/(stem+'.gameplay.json')).read_text())
        root,blocks=read_structure(folder/(stem+'.nbt'))
        image=Image.new('RGB',(2200,1600),'#eee9de');draw=ImageDraw.Draw(image)
        draw.text((45,20),stem.upper()+' / MARKER PLAN',font=font(39,True),fill='#293934')
        draw.text((45,90),'Raw-template X/Z projection / north at top / numbers match the legend / all heights are raw Y',font=font(26),fill='#54615a')
        scale=min(1150/root['size'][0],1220/root['size'][2]);ox,oz=60,210
        columns={}
        for (x,y,z),s in blocks.items():
            if (x,z) not in columns or y>columns[x,z][0]:columns[x,z]=(y,s)
        for (x,z),(y,s) in columns.items():
            color='#acb4a2' if any(k in s for k in ('moss','leaves','log')) else '#b6ada0'
            draw.rectangle((ox+x*scale,oz+z*scale,ox+(x+1)*scale,oz+(z+1)*scale),fill=color)
        for x in range(0,root['size'][0],10):
            draw.line((ox+x*scale,oz,ox+x*scale,oz+root['size'][2]*scale),fill='#d0cbbf')
            draw.text((ox+x*scale,oz-27),str(x),font=font(19),fill='#54615a')
        for z in range(0,root['size'][2],10):
            draw.line((ox,oz+z*scale,ox+root['size'][0]*scale,oz+z*scale),fill='#d0cbbf')
            draw.text((ox-40,oz+z*scale),str(z),font=font(19),fill='#54615a')
        for i,m in enumerate(sidecar['markers']):
            x,y,z=m['pos'];cx,cz=ox+(x+.5)*scale,oz+(z+.5)*scale
            color='#27586b' if m['role'].endswith('_spawn') else '#9e542f'
            draw.ellipse((cx-14,cz-14,cx+14,cz+14),fill=color)
            draw.text((cx,cz),str(i+1),font=font(19,True),fill='white',anchor='mm')
            draw.text((1300,220+i*105),f'{i+1:02}  {m["role"]}',font=font(27,True),fill=color)
            draw.text((1350,260+i*105),str(m['pos'])+(' / '+m['facing'] if 'facing' in m else ''),font=font(27),fill='#54615a')
        draw.text((1300,1220),f'Ground: Y{sidecar["ground_y"]}',font=font(30,True),fill='#293934')
        draw.text((1300,1280),f'{len(sidecar["regions"])} bounded sidecar regions',font=font(28),fill='#54615a')
        draw.text((45,1490),'Projection only: markers at different heights may overlap. Use the exact XYZ sidecar and cutaway review for placement.',font=font(27),fill='#54615a')
        image.save(folder/(stem+'-markers-review.png'))

if __name__=='__main__':main()
