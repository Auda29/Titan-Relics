"""Settle the posterior skull into earth by rotating the whole skull/sword assembly."""
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Matrix

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *

SOURCE=ROOT/'relics/titan-skull/design/generated/titan-skull-2-v1/titan-skull-2-v1-source.blend'
ANGLE=math.radians(16)


def settle(p,vector=False):
    x,y,z=p
    if not vector:z+=35
    y,z=y*math.cos(ANGLE)-z*math.sin(ANGLE),y*math.sin(ANGLE)+z*math.cos(ANGLE)
    return [x,y if vector else y-3,z if vector else z-35]


def main():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    meta=json.loads(SOURCE.with_name('titan-skull-2-v1.design.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    for obj in list(bpy.context.scene.objects):
        if obj.type!='MESH':continue
        if any(m and m.name.startswith('terrain_') for m in obj.data.materials):
            bpy.data.objects.remove(obj,do_unlink=True);continue
        # Ground chips stay on their original soil surface. The complete anatomy,
        # attached growth and sword use one rigid rotation, with no neck pedestal.
        if 'Local broken bone chip' in obj.name:continue
        matrix=obj.matrix_world.copy()
        for vertex in obj.data.vertices:
            p=matrix@vertex.co;vertex.co=xyz(settle((p.x,p.z,-p.y)))
        obj.matrix_world=Matrix.Identity(4);obj.data.update()
    features=meta['new_relic_v1']
    for key in ('void_probes_source','solid_probes_source'):features[key]=[settle(p) for p in features[key]]
    for key in ('entry_source','top_source','crossguard_source'):features['sword'][key]=settle(features['sword'][key])
    features['sword']['axis_source']=settle(features['sword']['axis_source'],vector=True)
    deposits([(-27,1,21,27,1.2,-18),(27,8,22,25,1.5,27),(0,35,29,20,1.8,0)],
             18,(-54,56,-58,66))
    meta['revision_v2']={'source':SOURCE.relative_to(ROOT).as_posix(),'source_sha256':digest,
        'rigid_posterior_settlement_degrees':16,'vertical_settlement':3,'pivot_source':[0,0,-35]}
    meta.update(name='Titan Skull 2 V2 / Settled posterior',visual_acceptance='Alpha 4.5 screenshot follow-up; review pending')
    save('relics/titan-skull/design/titan-skull-2-v2.json',meta)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest


if __name__=='__main__':main()
