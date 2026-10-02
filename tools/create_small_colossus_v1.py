"""New small-Colossus asset derived from the preserved archive, never overwriting it."""
import hashlib
from pathlib import Path
import sys

import bpy
from mathutils import Vector,Matrix

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *
from create_colossus_v4 import fingerprint

SOURCE=ROOT/'relics/colossus/archive/first-concept/generated/colossus-source.blend'


def hand():
    for obj in list(bpy.context.scene.objects):
        if obj.name.startswith(('Detached palm','Separate finger','Detached thumb')):
            bpy.data.objects.remove(obj,do_unlink=True)
    # Distal +Z, thumbward -X, palm +Y: a determinant-positive right-hand frame.
    thumbward=Vector((-1,0,0));distal=Vector((0,0,1));palmar=Vector((0,1,0))
    basis=Matrix((thumbward,distal,palmar)).transposed()
    assert abs(basis.determinant()-1)<1e-6
    wrist=Vector((46,5,25))
    def point(u,v,w):return tuple(wrist+basis@Vector((u,v,w)))
    box('V1 small right hand | compact palm',point(0,6,0),(17,7.5,13),'armor',1.5)
    box('V1 small right hand | recessed palm plate',point(0,6,3.9),(11,1,8),'joint',.65)
    cylinder('V1 small right hand | low wrist bearing',point(-7,0,0),point(7,0,0),3.4,'joint',16)
    tips=[]
    for name,u,length,curl in [('little',-6.6,11,5),('ring',-2.2,15,7),('middle',2.2,17,8),('index',6.6,14,6)]:
        points=[point(u,12,0),point(u,12+length*.5,.5),point(u,12+length*.8,curl*.5),point(u,12+length,curl)]
        for j,(a,b) in enumerate(zip(points,points[1:])):
            cylinder(f'V1 small right hand | {name} phalanx {j+1}',a,b,1.5-j*.1,'trim' if j==1 else 'armor',12)
        for p in points[:-1]:ellipsoid('V1 small right hand | knuckle',p,(1.65,1.65,1.65),'joint',12,8)
        tips.append(list(points[-1]))
    thumb=[point(7,3,0),point(12,7,2),point(15,12,5)]
    tapered('V1 small right hand | thumb',thumb,[2.2,1.9,1.5],'trim',12)
    return {'anatomical_side':'right','basis_determinant':basis.determinant(),
            'palmar_normal_source':list(palmar),'wrist_source':list(wrist),'finger_tips_source':tips,
            'palm_up':True,'thumb_tip_source':list(thumb[-1])}


def main():
    source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    originals={o.name:fingerprint(o) for o in bpy.context.scene.objects if o.type=='MESH'}
    # Retain the archive's cool structural identity and avoid bulk valuable metal.
    for name,color in {'armor':'4a5053','trim':'363f40','broken':'5b615c','joint':'424747',
                       'dark':'172123','copper':'527765','moss':'5e743c','earth':'74533b','wood':'91734b'}.items():
        material(name,color)
    pose=hand()
    torso=bpy.data.objects['01 | Hollow armoured torso']
    damage(torso,(-9,31,15),(6,8),14)
    tapered('V1 | Rear exposed support',[(-13,12,9),(-14,24,10),(-10,37,9)],[1.6,1.3,1.3],'joint',10)
    lower=ellipsoid('V1 | Buried lower torso completion',(0,-2,1),(18,8,13),'armor',32,20)
    subtract(lower,ellipsoid('Lower body inner void',(0,-2,1),(13,9,8),'joint',24,16))
    damage(lower,(8,-7,-10),(5,4),10)
    for x,z,h in [(-15,5,8),(13,5,7),(1,10,8)]:
        cylinder('V1 | Buried snapped support',(x,2,z),(x+1,-h,z+1),2.2,'joint',12)
    # Existing archive fragments stay; one small forward chip extends the local deposit composition.
    box('V1 | Forearm-edge chip',(37,1.5,57),(5,3,5),'broken',.6)
    deposits([(-22,6,18,19,2.8,0),(11,9,17,20,3.2,0),(45,17,12,15,2.4,0),
              (46,40,10,15,1.8,0)],7,(-43,59,-26,62))
    changed={'01 | Hollow armoured torso'}
    removed_prefixes=('Detached palm','Separate finger','Detached thumb')
    preserved={}
    bpy.context.view_layer.update()
    for name,digest in originals.items():
        if name in changed or name.startswith(removed_prefixes):continue
        assert fingerprint(bpy.data.objects[name])==digest,f'Unexpected change to archived mesh {name}'
        preserved[name]=digest
    save('relics/colossus/design/small-colossus-v1.json',{
        'name':'Small Colossus V1','reference':'https://www.instagram.com/reel/DaoBxUEiBNa/',
        'archive_source':str(SOURCE.relative_to(ROOT)).replace('\\','/'),'archive_source_sha256':source_hash,
        'preserved_archive_meshes':preserved,
        'new_relic_v1':{'family':'small-colossus','hand':pose,
            'void_probes_source':[[0,27,-17],[-9,31,17]],
            'solid_probes_source':[[0,45,1]],
            'features':['preserved angular helmet','circular chest rupture','palm-up anatomical right hand','buried lower completion','small rear breach'],
            'v5_interiors':False,'rewards_inherited':False}})
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash


if __name__=='__main__':main()
