"""Retain 220-block tower height; author ruined storeys, flights and facade courses."""
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *

SOURCE=ROOT/'relics/ruined-tower/design/generated/ruined-tower-v2/ruined-tower-v2-source.blend'


def main():
    checksum=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    meta=json.loads(SOURCE.with_name('ruined-tower-v2.design.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    material('course','515753');material('floor','55554f')
    floors=[];stairs=[]
    # Remaining floor segments attach to the actual inner walls; the center stays
    # broken open. Unequal extents keep the interior from becoming a stack of rings.
    for i,y in enumerate((24,49,77,106,139,170)):
        side=-1 if i%2 else 1
        center=(side*16,y,4 if i%3 else -3)
        floor=box(f'Ruined storey {i+1} / side gallery',center,(11,3,28 if i<3 else 21),'floor',.5)
        damage(floor,(side*12,y,0 if i%2 else 8),(4,3),6)
        floors.append([side*18,y,3])
        box(f'Ruined storey {i+1} / rear fragment',(-side*5,y,13),(26-i*2,3,8),'worn',.4)
        for x in (-18,18):
            box('Storey corbel',(x,y-3,13),(4,5,5),'pier',.4)
        # Fragmentary outer string courses tied to surviving wall, not sky slots.
        if y<140:
            for z in (-24.6,24.6):
                for x,length in [(-20,12),(15,18)]:
                    box('Weathered facade stringcourse',(x,y,z),(length,2.2,2.5),'course',.5)
        for x in (-27.5,27.5):
            box('Side course surviving fragment',(x,y,4),(2.5,2.2,19-i),'course',.4)
    # Three broken stair flights read as architecture, not an empty shaft.
    for flight,base_y in enumerate((4,29,81)):
        side=-1 if flight%2==0 else 1
        for step in range(20):
            if (flight==1 and step in (9,10,11)) or (flight==2 and step>13):continue
            z=-13+step*1.4;y=base_y+step
            box(f'Broken stair flight {flight+1} / tread {step+1}',(side*17,y,z),(7,1.8,2),'floor',.15)
            if step in (3,7,15):stairs.append([side*17,y,z])
        box('Stair landing remnant',(side*16,base_y+20,14),(10,2.5,6),'pier',.4)
    # Vertical ribs with missing sections and narrow window surrounds articulate
    # the broad lower facades while leaving the original breach silhouettes.
    for x in (-20,20):
        for lo,hi in ((6,39),(45,69),(86,120)):
            box('Interrupted facade pilaster',(x,(lo+hi)/2,-25),(2.7,hi-lo,2.6),'pier',.35)
    shell=next(o for o in bpy.context.scene.objects if 'tower shell' in o.name)
    for center,radii in [((-20,196,-23),(6,8)),((15,209,23),(5,9)),((-25,160,-10),(4,10)),((23,181,15),(5,7))]:
        damage(shell,center,radii,12)
    assert len(shell.data.vertices)>100,'Facade damage removed the tower shell'
    # Deliberately uneven missing stones around the low thresholds.
    for i,(x,y,z) in enumerate([(-11,8,-24),(10,20,-24),(-25,43,-18),(24,10,24)]):
        block=box(f'Exposed broken masonry course {i}',(x,y,z),(5,3,4),'course',.4)
        block.rotation_euler.z=.13*(-1 if i%2 else 1)
    features=meta['new_relic_v1'];features['solid_probes_source']+=floors+stairs
    features['features']+=['six partial storeys','three broken stair flights','fragmentary stringcourses and pilasters']
    features['v5_interiors']=False
    save('relics/ruined-tower/design/ruined-tower-v3.json',{
        'name':'Ruined Tower V3 / Broken storeys','reference':'https://www.instagram.com/reel/DbqXYoVx2hR/',
        'visual_acceptance':'October 5 screenshot revision; review pending','new_relic_v1':features,
        'revision_v2':meta['revision_v2'],
        'revision_v3':{'source':str(SOURCE.relative_to(ROOT)).replace('\\','/'),'source_sha256':checksum,
                       'partial_storeys':6,'broken_stair_flights':3,'visible_height_target':220,
                       'feedback':'Screenshots 20–22: uniform wall planes and empty interior shaft',
                       'architectural_interiors_only':True}})
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==checksum


if __name__=='__main__':main()
