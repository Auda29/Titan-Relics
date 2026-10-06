"""Break the broad side walls and blend the foot into meadow soil and dark rubble."""
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *
import create_colossus_v3 as shapes

SOURCE=ROOT/'relics/ruined-tower/design/generated/ruined-tower-v4/ruined-tower-v4-source.blend'


def side_cut(obj,center,radii,depth):
    cutter=jagged_cutter('Side-wall masonry loss',(0,0,0),radii,depth)
    cutter.rotation_euler.z=math.pi/2;cutter.location=xyz(center)
    recalculate(cutter);subtract(obj,cutter)


def main():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    meta=json.loads(SOURCE.with_name('ruined-tower-v4.design.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE));shapes.RNG.seed(61006)
    shell=next(o for o in bpy.context.scene.objects if 'tower shell' in o.name)
    breaches=[((-26,67,-5),(7,12)),((-26,132,2),(9,19)),
              ((26,102,-4),(8,15)),((26,166,-1),(7,14))]
    for center,radii in breaches:side_cut(shell,center,radii,20)
    # Shallow broken recesses and exposed course ends give remaining side walls
    # depth without converting the entire elevation into a regular window grid.
    for side in (-1,1):
        for z,y,h in [(-11,37,24),(6,93,21),(-8,157,29)]:
            subtract(shell,box('Partial recessed side panel',(side*27.8,y,z),(2.4,h,4.5),'wall',.3))
        for i,(y,z,length) in enumerate(((43,-12,13),(88,7,10),(119,-8,16),(151,7,11),(179,-10,9))):
            obj=box(f'Side broken stringcourse {side}.{i}',(side*28.3,y,z),(2.7,2.8,length),'course',.35)
            side_cut(obj,(side*29,y,z+length*.32),(2,2),5)
        for j in range(9):
            y=112+j*3.2;z=-14+(j%3)*1.1
            box(f'Exposed side masonry {side}.{j}',(side*28,y,z),(1.5,2.6,4.3),'worn' if j%3 else 'floor',.2)
    # Chip the plain outer annexes too; their continuous wall mass stays grounded.
    for obj in list(bpy.context.scene.objects):
        if 'Lower ruin ' in obj.name:
            low,high=bounds([obj]);x=(low[0]+high[0])/2
            side_cut(obj,(x+(-10 if x<0 else 9),17,20),(5,10),9)
    for obj in list(bpy.context.scene.objects):
        if obj.type=='MESH' and any(m and m.name.startswith('terrain_') for m in obj.data.materials):
            bpy.data.objects.remove(obj,do_unlink=True)
    deposits([(-34,-12,21,25,.8,-15),(33,17,23,28,1.1,22),(4,33,27,16,.7,0)],
             8,(-56,56,-48,48))
    # Low irregular rubble trails taper into earth, rather than a pale ring.
    for i,(x,z,sx,sz) in enumerate([(-31,-26,4,3),(-34,-31,3,2),(-30,-36,2,2),
                (34,0,4,3),(38,-6,2,3),(39,-11,2,2),(-19,31,4,2),(-12,35,2,2)]):
        obj=box(f'Low rubble trail {i}',(x,.65,z),(sx,1.8,sz),'worn',.3)
        obj.rotation_euler.z=.35*math.sin(i*2)
    meta['new_relic_v1']['void_probes_source'].extend([list(p) for p,_ in breaches])
    meta.update(name='Ruined Tower V5 / Broken side elevations and meadow foot',
                visual_acceptance='October 6 side-wall and terrain revision; user review pending')
    meta['revision_v5']={'source':SOURCE.relative_to(ROOT).as_posix(),'source_sha256':digest,
        'side_wall_breaches':len(breaches),'visible_height_target':220,
        'terrain_revision':'Lower grass/rooted-earth deposits with dark rubble; no sandstone apron'}
    save('relics/ruined-tower/design/ruined-tower-v5.json',meta)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest


if __name__=='__main__':main()
