"""In-game feedback: slumped, scarred plated sentinel with weathered mineral colours."""
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from new_relic_v1_common import *

SOURCE=ROOT/'relics/colossus/design/generated/small-colossus-v4/small-colossus-v4-source.blend'


def slump(p):
    x,y,z=p
    upper=max(0,y-8)
    # Continuous deformation preserves shoulder/arm contacts while listing the
    # body sideways and pitching the heavy face down toward the foreground hand.
    nod=max(0,min(1,(y-34)/20))
    return (x+.24*upper, y-.09*x*max(0,min(1,(y-3)/24))-.055*upper+.12*(z+1)*nod,
            z-.22*upper)


def main():
    checksum=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    old=json.loads(SOURCE.with_name('small-colossus-v4.design.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    for name,color in {'armor':'88735d','plate':'6f5949','rust':'544737','worn':'8a8875',
                       'edge':'a0795f','claw':'b29c79','growth':'536346'}.items(): material(name,color)
    objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
    body=next(o for o in objects if 'Continuous massive' in o.name)
    head=next(o for o in objects if 'multi-optic head' in o.name)
    shoulder=next(o for o in objects if 'protective shoulder' in o.name and o.location.x<0)
    # Broad dents and torn local plating retain a heavy closed core.
    damage(body,(-15,25,-10),(8,15),9)
    damage(head,(-18,66,-6),(6,7),12)
    damage(shoulder,(-37,41,-4),(8,10),12)
    # Interrupt the symmetric rear domes with staggered overlapping spine plates.
    for i,(x,y,z,w,h) in enumerate([(-4,14,32,24,9),(0,24,32,21,11),(4,34,29,18,10),(6,43,24,15,8)]):
        plate=box(f'Broken overlapping dorsal plate {i}',(x,y,z),(w,h,4),'plate',1.2)
        plate.rotation_euler.y=math.radians((-1 if i%2 else 1)*8)
        if i in (0,2):damage(plate,(x-w*.35,y+3,z),(4,3),8)
    # Long irregular scar incisions on the otherwise broad back; no large cavities.
    for x,y,z in [(-14,34,29),(10,21,33),(-4,44,24)]:
        damage(body,(x,y,z),(2.2,8),8)
    bpy.context.view_layer.update()
    transformed=[]
    for obj in list(bpy.context.scene.objects):
        if obj.type!='MESH':continue
        if any(m and m.name.startswith('terrain_') for m in obj.data.materials):
            bpy.data.objects.remove(obj,do_unlink=True);continue
        matrix=obj.matrix_world.copy()
        for vertex in obj.data.vertices:
            p=matrix@vertex.co
            vertex.co=xyz(slump((p.x,p.z,-p.y)))
        obj.matrix_world=Matrix.Identity(4);obj.data.update();transformed.append(obj)
        if 'casing' in obj.name or 'torso' in obj.name or 'multi-optic head' in obj.name or 'armour' in obj.name:
            # Coherent patches over several source units, not per-block confetti.
            original=len(obj.data.materials)
            for material_name in ('plate','rust','worn','growth'):obj.data.materials.append(bpy.data.materials[material_name])
            for face in obj.data.polygons:
                p=face.center
                field=math.sin(p.x*.19+p.z*.035)+.7*math.sin(p.y*.23-p.z*.11)+.35*math.sin(p.z*.41)
                if field>1.1:face.material_index=original+1
                elif field<-.95:face.material_index=original
                elif p.z<22 and field>.3:face.material_index=original+3
                elif .54<field<.7:face.material_index=original+2
    # Larger asymmetric burial on the listed side, smaller patches around hands.
    deposits([(24,14,29,28,8,20),(6,28,30,21,5,-10),(-30,-21,17,23,3,-20),
              (34,-13,21,22,3,10)],8,(-60,67,-70,50))
    f=old['revision_v4']
    for optic in f['head_optics']+[o for hand in f['pincers'] for o in hand['ports']]:
        for key in ('center_source','dark_probe_source'):optic[key]=list(slump(optic[key]))
    for hand in f['pincers']:
        hand['center_source']=list(slump(hand['center_source']))
        hand['tine_tips_source']=[list(slump(p)) for p in hand['tine_tips_source']]
    for key in ('solid_core_probes_source','grille_rib_probes_source'):f[key]=[list(slump(p)) for p in f[key]]
    for key in ('body_connection_source','head_connection_source'):f[key]=list(slump(f[key]))
    save('relics/colossus/design/small-colossus-v5.json',{
        'name':'Small Colossus V5 / Slumped weathered sentinel','reference':old['reference'],
        'visual_acceptance':'October 5 screenshot revision; review pending','revision_v4':f,
        'revision_v5':{'source':str(SOURCE.relative_to(ROOT)).replace('\\','/'),'source_sha256':checksum,
                       'sideways_shear':.24,'forward_shear':-.22,'asymmetric_burial':True,
                       'feedback':'Screenshots 08/09: toy-like symmetry, bright gold and primitive rear forms'},
        'new_relic_v1':{'family':'small-colossus','v5_interiors':False}})
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==checksum


if __name__=='__main__':main()
