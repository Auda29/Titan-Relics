"""Replace isolated side holes by continuous collapsed bays and a missing corner."""
import hashlib
import json
from pathlib import Path
import sys

import bpy

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *
from create_ruined_tower_v5 import side_cut
import create_colossus_v3 as shapes

SOURCE=ROOT/'relics/ruined-tower/design/generated/ruined-tower-v6/ruined-tower-v6-source.blend'


def main():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    meta=json.loads(SOURCE.with_name('ruined-tower-v6.design.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE));shapes.RNG.seed(610062)
    cuts=[((-27,55,-10),(12,24)),((-27,82,-10),(14,25)),
          ((-27,108,-5),(13,25)),((-27,129,1),(11,21)),
          ((-27,78,-23),(10,20)),
          ((27,50,-11),(10,21)),((27,74,-13),(11,23)),((27,96,-7),(10,20))]
    # Apply each wound to shell, skirts AND its exposed courses/pier overlays.
    # Otherwise the tiny overlays bridge an opening which should read as collapse.
    objects=[o for o in bpy.context.scene.objects if o.type=='MESH'
             and not any(m and m.name.startswith('terrain_') for m in o.data.materials)]
    for center,radii in cuts:
        x,y,z=center;rz,ry=radii
        for obj in objects:
            low,high=bounds([obj])
            if low[0]>x+9 or high[0]<x-9 or low[2]>y+ry or high[2]<y-ry:continue
            if low[1]>-z+rz or high[1]<-z-rz:continue
            side_cut(obj,center,radii,18)
    for i,(x,z,w,h) in enumerate([(-34,-25,7,4),(-42,-28,5,3),(-35,-36,4,2),
                                  (35,-20,6,3),(43,-24,4,2)]):
        obj=box(f'Collapsed side bay rubble {i}',(x,h/2-.7,z),(w,h,w*.7),'worn',.6)
        obj.rotation_euler.z=(i%3-1)*.3
    meta['new_relic_v1']['void_probes_source'].extend([list(p) for p,_ in cuts])
    meta['revision_v7']={'source':SOURCE.relative_to(ROOT).as_posix(),'source_sha256':digest,
        'connected_side_bays':2,'corner_breaks':1,'visible_height_target':220}
    meta.update(name='Ruined Tower V7 / Collapsed side bays',visual_acceptance='Alpha 4.5 screenshot follow-up; review pending')
    save('relics/ruined-tower/design/ruined-tower-v7.json',meta)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest


if __name__=='__main__':main()
