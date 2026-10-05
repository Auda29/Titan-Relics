"""Extend the tower above its lower ruins to 220 visible blocks, preserving its footprint."""
import hashlib
import json
from pathlib import Path
import sys

import bpy
from mathutils import Matrix

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import ROOT, save

SOURCE=ROOT/'relics/ruined-tower/design/generated/ruined-tower-v1/ruined-tower-v1-source.blend'


def height(y):
    return y if y<=48 else 48+(y-48)*172/132


def main():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    metadata=json.loads(SOURCE.with_name('ruined-tower-v1.design.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    # Apply the piecewise map in world space, including vertices crossing Y48.
    for obj in bpy.context.scene.objects:
        if obj.type!='MESH':continue
        matrix=obj.matrix_world.copy()
        for vertex in obj.data.vertices:
            p=matrix@vertex.co;p.z=height(p.z);vertex.co=p
        obj.matrix_world=Matrix.Identity(4)
        obj.data.update()
    features=metadata['new_relic_v1']
    for key in ('void_probes_source','solid_probes_source'):
        features[key]=[[x,height(y),z] for x,y,z in features[key]]
    save('relics/ruined-tower/design/ruined-tower-v2.json',{
        'name':'Ruined Tower V2','visual_acceptance':'V2 review pending',
        'new_relic_v1':features,
        'revision_v2':{'source':str(SOURCE.relative_to(ROOT)).replace('\\','/'),
                       'source_sha256':digest,'visible_height_target':220,
                       'unchanged_below_source_y':48,'upper_height_factor':172/132,
                       'horizontal_scale':1,'nominal_ground_ceiling_with_16_block_margin':83}})
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest


if __name__=='__main__':main()
