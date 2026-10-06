"""Break the lower rectangular annex walls into grounded, unequal ruin fragments."""
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *
from create_ruined_tower_v5 import side_cut
import create_colossus_v3 as shapes

SOURCE=ROOT/'relics/ruined-tower/design/generated/ruined-tower-v5/ruined-tower-v5-source.blend'


def main():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    meta=json.loads(SOURCE.with_name('ruined-tower-v5.design.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE));shapes.RNG.seed(610061)
    shell=next(o for o in bpy.context.scene.objects if 'tower shell' in o.name)
    skirts=[o for o in bpy.context.scene.objects if 'Broken tapered buttress' in o.name]
    # The broad lower *main* elevations also need losses. Cut through their
    # thick grounding skirts as well, otherwise the breach is hidden by a second
    # intact wall immediately behind/in front of the shell.
    lower_gaps=[(26,35,-7),(-26,30,-7)]
    for center in lower_gaps:
        side_cut(shell,center,(6.5,11),20)
        for obj in skirts:side_cut(obj,center,(6.5,11),20)
    damage(shell,(7,22,24),(9,11),12)
    for obj in list(bpy.context.scene.objects):
        if obj.type!='MESH' or not any(m and m.name=='course' for m in obj.data.materials):continue
        low,high=bounds([obj])
        if low[0]<17 and high[0]>-3 and low[2]<34 and high[2]>10 and low[1]<-18 and high[1]>-30:
            damage(obj,(7,22,24),(9,11),12)
    for side in (-1,1):
        for j in range(4):
            box('Broken lower bearing course',(side*28.5,11+j*3.1,8+j*.6),
                (2.2,2.5,5.5-j*.6),'worn' if j%2 else 'floor',.3)
    annexes=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'Lower ruin ' in o.name]
    assert len(annexes)==2,'Expected two lower annex shells'
    gaps=[]
    for obj in annexes:
        low,high=bounds([obj]);cx=(low[0]+high[0])/2;side=-1 if cx<0 else 1
        outer=low[0] if side<0 else high[0];z=-(low[1]+high[1])/2
        # Large losses enter from above, so a mostly complete rectangular outer
        # wall becomes several short stubs and an unequal corner pier.
        side_cut(obj,(outer,high[2]-5,z-1),(8,18 if side<0 else 12),16)
        side_cut(obj,(outer,9,z+3),(4.5,9),14)
        damage(obj,(cx,high[2]-4,z+9),(8,14),18)
        damage(obj,(cx-3,12,z+10),(5,9),18)
        gaps.append([outer,high[2]-5,z-1])
        # Ragged stepped fracture at the opposite upper edge instead of another
        # flat horizontal rectangular parapet.
        for j in range(3):
            subtract(obj,box('Unequal lower-wall top loss',
                (cx+(j-1)*6,high[2]-2+(j%2)*3,z-7),(6,8,7),'wall'))
        for j in range(5):
            box('Exposed lower wall masonry',(outer+side*.6,4+j*2.6,z-7),
                (1.7,2.2,3.6),'worn' if j%2 else 'course',.25)
    for j,(x,z,w,h) in enumerate([(-48,32,6,3),(-43,37,4,2),(-35,37,3,1.5),(48,29,4,2.5),(45,35,3,1.5)]):
        obj=box(f'Lower-wall fallen masonry {j}',(x,h/2-.5,z),(w,h,w*.65),'worn',.4)
        obj.rotation_euler.z=math.sin(j+1)*.45
    meta['new_relic_v1']['void_probes_source'].extend(gaps+lower_gaps+[[7,22,24]])
    meta.update(name='Ruined Tower V6 / Broken lower walls',visual_acceptance='Alpha 4.4 screenshot revision; review pending')
    meta['revision_v6']={'source':SOURCE.relative_to(ROOT).as_posix(),'source_sha256':digest,
        'lower_annexes_reworked':2,'lower_main_wall_breaches':3,'visible_height_target':220}
    save('relics/ruined-tower/design/ruined-tower-v6.json',meta)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest


if __name__=='__main__':main()
