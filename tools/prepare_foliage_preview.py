"""Extend a local preview atlas with leaf textures, without modifying pinned OTS.

No game installation: two 16px texture PNGs only. Preview uses fixed tint and
opaque rendering; actual exported leaves retain their native persistent states.
"""
import hashlib
import json
from pathlib import Path
import urllib.request

from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'.work/ObjToSchematic/res/atlases'
OUT=ROOT/'.work/foliage-preview-atlas'
TEXTURES=ROOT/'.work/preview-textures'


def main():
    OUT.mkdir(parents=True,exist_ok=True);TEXTURES.mkdir(parents=True,exist_ok=True)
    atlas=json.loads((BASE/'vanilla.atlas').read_text());image=Image.open(BASE/'vanilla.png').convert('RGBA')
    size=atlas['atlasSize'];cell=image.width//size;pixel=cell//3
    slot=max(t['atlasRow']*size+t['atlasColumn'] for t in atlas['textures'].values())+1
    provenance=[]
    for name,tint in [('spruce_leaves',(97,153,97)),('oak_leaves',(109,160,79))]:
        url=f'https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/1.19.2/assets/minecraft/textures/block/{name}.png'
        path=TEXTURES/f'{name}.png'
        if not path.exists():path.write_bytes(urllib.request.urlopen(url,timeout=30).read())
        texture=Image.open(path).convert('RGBA').resize((pixel,pixel),Image.Resampling.NEAREST)
        data=[]
        for r,g,b,a in texture.getdata():
            # Opaque fast-style leaf background; no biome tint or alpha simulation claim.
            value=(r+g+b)/3/255 if a else .18
            data.append((*[round(c*value) for c in tint],255))
        texture.putdata(data)
        col,row=slot%size,slot//size
        if row>=size:raise ValueError('Preview atlas has no free texture slots')
        for x in range(3):
            for y in range(3):image.paste(texture,(col*cell+x*pixel,row*cell+y*pixel))
        key='minecraft:block/'+name
        atlas['textures'][key]={'atlasColumn':col,'atlasRow':row}
        atlas['blocks'].append({'name':'minecraft:'+name,'faces':{side:key for side in ('up','down','north','south','east','west')}})
        provenance.append({'texture':name,'url':url,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'fixed_tint':tint})
        slot+=1
    (OUT/'vanilla.atlas').write_text(json.dumps(atlas)+'\n');image.save(OUT/'vanilla.png')
    (OUT/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    print('Local foliage preview atlas:',OUT)


if __name__=='__main__':main()
