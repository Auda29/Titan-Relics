"""Chipped stair remnants, exposed masonry and staggered fractured upper walls."""
import hashlib
import json
import math
from pathlib import Path
import random
import sys

import bpy

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *

SOURCE=ROOT/'relics/ruined-tower/design/generated/ruined-tower-v3/ruined-tower-v3-source.blend'


def skyline_cutter(rear=False):
    profile=[(-35,174),(-27,182),(-22,174),(-17,190),(-12,180),(-8,203),
             (-3,193),(2,205),(8,195),(13,212),(18,202),(22,220),(26,208),(35,197)]
    if rear:profile=[(x,y-7-3*math.sin(x*.31)) for x,y in profile]
    outline=profile+[(35,250),(-35,250)];count=len(outline)
    zs=(0,40) if rear else (-40,0)
    vertices=[(x,y,z) for z in zs for x,y in outline]
    faces=[tuple(reversed(range(count))),tuple(range(count,2*count))]
    faces += [(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)]
    obj=mesh('Unequal fracture silhouette cutter',vertices,faces,'wall');recalculate(obj);return obj


def main():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    meta=json.loads(SOURCE.with_name('ruined-tower-v3.design.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE));rng=random.Random(41005)
    bpy.context.view_layer.update()
    for obj in list(bpy.context.scene.objects):
        if obj.type!='MESH':continue
        _,high=bounds([obj])
        if high[2]>172:
            subtract(obj,skyline_cutter());subtract(obj,skyline_cutter(True))
    shell=next(o for o in bpy.context.scene.objects if 'tower shell' in o.name)
    # Local losses at the edges of the tall sky slots, not only paint on the wall.
    for center,radii in [((-11,159,-24),(4,9)),((12,186,-24),(4,11)),
                          ((-5,176,24),(5,10)),((17,140,24),(4,8))]:
        damage(shell,center,radii,12)
    # The lowest flight looked complete in-game. Break it in the middle, chip
    # remaining noses, and leave rubble on the existing lower floor.
    removed=[]
    for obj in list(bpy.context.scene.objects):
        if 'Broken stair flight 1 / tread ' not in obj.name:continue
        step=int(obj.name.rsplit(' ',1)[-1])-1
        if step in (9,10,11,12,13,14):
            removed.append(step);bpy.data.objects.remove(obj,do_unlink=True)
        elif step in (4,8,16,18):
            damage(obj,(-13.5,4+step,-13+step*1.4),(2.0,.8),3.5)
    for i,(x,z,w) in enumerate([(-15,0,3),(-10,5,2.3),(-19,9,2.2),(-14,13,2.7)]):
        obj=box(f'Fallen stair masonry {i}',(x,6,z),(w,1.4,w*.8),'worn',.3)
        obj.rotation_euler.z=rng.uniform(-.6,.6)
    # Reveal unequal remnants of an inner masonry facing. Small coherent patches
    # of protruding courses carry relief; broad intact sections stay readable.
    patches=[(-20,33,-8),(-20,88,6),(20,61,-1),(20,126,7),(-20,151,10)]
    for patch,(x,y,z) in enumerate(patches):
        for row in range(6):
            for col in range(4):
                if rng.random()<.24:continue
                depth=.8+rng.random()*.7
                box(f'Exposed inner stone course {patch}.{row}.{col}',
                    (x,y+row*2.6,z+(col-1.5)*3.5+(row%2)*1.6),
                    (depth,2.3,3.2),'course' if rng.random()<.65 else 'worn',.18)
    for obj in list(bpy.context.scene.objects):
        if 'rear fragment' in obj.name:
            low,high=bounds([obj]);x=(low[0]+high[0])/2;y=(low[2]+high[2])/2;z=-(low[1]+high[1])/2
            damage(obj,(x+3,y,z-3.5),(3.5,2),6)
    # Slender irregular repair/exposure bands, rather than a uniform tile wall.
    for x,y,z in [(-21,32,-10),(21,96,4),(-21,122,9)]:
        for j in range(4):
            box('Interrupted interior repair seam',(x,y+j*3,z+j*.4),(1.1,2.5,1.3),'accent',.15)
    assert len(shell.data.vertices)>100,'Crown cutting removed the shell'
    feature=meta['new_relic_v1']
    feature['void_probes_source'].append([-17,16,3.8])
    save('relics/ruined-tower/design/ruined-tower-v4.json',{
        'name':'Ruined Tower V4 / Fractured skyline','reference':meta['reference'],
        'visual_acceptance':'Alpha 4.2 screenshot follow-up; review pending',
        'new_relic_v1':feature,'revision_v2':meta['revision_v2'],'revision_v3':meta['revision_v3'],
        'revision_v4':{'source':str(SOURCE.relative_to(ROOT)).replace('\\','/'),'source_sha256':digest,
                       'feedback':'Alpha 4.2: parallel top sheets, complete first stair and uniform interior walls',
                       'lowest_stair_removed_steps_zero_based':removed,'inner_masonry_patches':len(patches),
                       'front_and_rear_skyline_staggered':True,'visible_height_target':220}})
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest


if __name__=='__main__':main()
