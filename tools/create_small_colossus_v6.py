"""Replace the sphere-built silhouette with overlapping forged armour and a settled pose."""
import hashlib
import math
from pathlib import Path
import sys

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *
import create_small_colossus_v4 as base

SOURCE=ROOT/'relics/colossus/design/generated/small-colossus-v5/small-colossus-v5-source.blend'
PLATES=[]


def casing(name,levels,mat='armor'):
    # Chamfered asymmetric cross-sections form broad planes with a continuous
    # closed core. These are authored shell contours, not low-poly spheres.
    vertices=[]
    for y,cx,cz,rx,rz in levels:
        for x,z in [(-.68,-1),(.62,-1),(1,-.52),(1,.50),(.60,1),(-.68,1),(-1,.48),(-1,-.56)]:
            vertices.append((cx+x*rx,y,cz+z*rz))
    faces=[tuple(reversed(range(8)))]
    for j in range(len(levels)-1):
        for i in range(8):faces.append((j*8+i,j*8+(i+1)%8,(j+1)*8+(i+1)%8,(j+1)*8+i))
    faces.append(tuple(range(len(vertices)-8,len(vertices))))
    obj=mesh(name,vertices,faces,mat);recalculate(obj);return obj


def plate(name,outline,normal,thickness=3,mat='armor',ridge=1.2):
    n=Vector(normal).normalized();points=[Vector(p) for p in outline];count=len(points)
    center=sum(points,Vector())/count+n*ridge
    vertices=[tuple(p) for p in points]+[tuple(p-n*thickness) for p in points]+[tuple(center)]
    faces=[tuple(reversed(range(count,2*count)))]
    for i in range(count):
        j=(i+1)%count;faces.extend([(i,j,2*count),(i,i+count,j+count,j)])
    obj=mesh(name,vertices,faces,mat);recalculate(obj)
    PLATES.append(list(center-n*.6));return obj


def torso():
    casing('01 | Closed chamfered torso',[(-9,0,14,20,16),(8,-1,13,27,22),
            (27,0,10,29,22),(40,2,7,25,19),(49,1,3,19,15)])
    # Chest and abdominal overlaps have unequal edges and widths. The body stays
    # plated and substantial instead of becoming an exposed narrow skeleton.
    for i,(y,width,z) in enumerate(((4,26,-9),(17,28,-13),(31,25,-13))):
        plate(f'Chest shingle {i}',[(-width,y+10,z+2),(-width*.55,y+14,z),
              (width*.68,y+12,z),(width,y+4,z+2),(width*.65,y-2,z-1),(-width*.72,y,z-2)],
              (0,0,-1),4,'plate' if i==1 else 'armor',2)
    for side in (-1,1):
        # One shoulder sits lower and forward; no matching round shoulder balls.
        x=side*30;drop=3 if side<0 else 0;z=4 if side<0 else 9
        casing('02 | Forged shoulder core',[(12-drop,x,z,10,12),(29-drop,x,z,14,17),
                 (44-drop,x-side*3,z,12,13),(49-drop,x-side*5,z,7,9)],'plate')
        for i in range(3):
            y=18+i*10-drop;outer=x+side*(13-i);inner=x-side*11
            plate(f'Shoulder overlapping front plate {side}.{i}',[
                (inner,y+10,z-11),(x,y+13,z-15),(outer,y+6,z-13),
                (outer,y-3,z-11),(x+side*2,y-5,z-15),(inner,y-1,z-12)],
                (0,0,-1),4,'armor' if i!=1 else 'plate',1.8)
            plate(f'Shoulder outer fold {side}.{i}',[
                (outer,y+6,z-13),(outer+side*2,y+5,z+8),
                (outer-side*2,y-5,z+14),(outer,y-3,z-11)],
                (side,0,0),4,'armor',.8)
    casing('Rear buried hip casing',[(-9,0,23,17,11),(8,0,24,23,14),(17,2,23,20,11)],'plate')
    # Broad asymmetric back plates replace the conspicuous posterior orb.
    for i,(y,width,z) in enumerate(((3,23,36),(15,26,34),(28,24,30),(39,19,24))):
        plate(f'Overlapping dorsal shield {i}',[(-width,y+11,z-4),(-width*.4,y+14,z),
              (width*.8,y+12,z-1),(width,y+3,z),(width*.60,y-2,z+2),(-width*.85,y,z+1)],
              (0,0,1),5,'armor' if i%2 else 'plate',1.4)
    for x,y in ((-10,20),(11,25)):
        cylinder('Rear service coupler',(x,y,30),(x,y,36),3.4,'joint',16)
        base.shapes.arc('Rear coupler rim',(x,y,36),(0,0,1),3.7,.6,'edge')


def head():
    optics,grille,_=base.head()
    for obj in list(bpy.context.scene.objects):
        if any(name in obj.name for name in ('Broad integrated multi-optic head','Head plate fastener')):
            bpy.data.objects.remove(obj,do_unlink=True)
    helmet=casing('03 | Broad forged helmet core',[(33,0,-1,15,13),(43,0,-1,24,20),
                   (61,0,-1,24,21),(71,-2,1,18,16),(75,-4,2,10,10)])
    plate('Crown forward overlapping brow',[(-23,62,-14),(-18,72,-12),(-6,76,-9),
          (12,73,-10),(23,62,-14),(12,64,-17),(-10,64,-17)],(0,0,-1),3,'plate',1)
    for side in (-1,1):
        plate('Helmet temple lamella',[(side*20,39,-10),(side*26,44,-4),
              (side*26,61,0),(side*18,72,3),(side*16,60,13),(side*22,43,10)],
              (side,0,0),3.5,'armor',.8)
    plate('Sloping rear helmet guard',[(-21,43,16),(-18,65,19),(-8,75,12),
          (13,70,15),(22,52,17),(14,38,17)],(0,0,1),4,'plate',1.2)
    damage(helmet,(-20,65,-9),(4.5,5),8)
    import bmesh
    bm=bmesh.new();bm.from_mesh(helmet.data);volume=bm.calc_volume()
    assert all(e.is_manifold for e in bm.edges) and volume>30000,'Helmet core lost its closed mass'
    bm.free();return optics,grille,volume


def settle(p):
    x,y,z=p;upper=max(0,y-7);weight=max(0,min(1,(y-8)/29))
    # Lower hands remain on the ground while the whole upper mass pitches and
    # lists over them. The vertical compression makes the helmet sit into the chest.
    return (x+.23*upper,y-.12*upper-.10*x*weight+.09*(z+2)*weight,z-.31*upper)


def main():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest();PLATES.clear()
    reset({'armor':'88735d','plate':'6f5949','edge':'a0795f','worn':'8a8875','rust':'544737',
           'patina':'587560','joint':'45463b','dark':'102126','claw':'8b7461','moss':'56683b','growth':'536346'})
    base.shapes.RNG.seed(61005)
    torso();optics,grille,volume=head()
    base.limb('Left',(-32,23,4),(-38,9,-19));base.limb('Right',(32,23,8),(36,8,-9))
    pincers=[base.pincer('Foreground left pincer',(-38,7,-31)),base.pincer('Right grounded pincer',(36,6,-21),.85)]
    for hand in pincers:
        x,y,z=hand['center_source'];s=hand['scale']
        # A continuous metal heel visually connects each pincer root to its casing.
        plate('Gripper heel armour',[(x-11*s,y+3,z-5*s),(x+10*s,y+3,z-5*s),
              (x+10*s,y-3,z-16*s),(x-10*s,y-3,z-16*s)],(0,1,0),3,'plate',1)
    for x,y,z in ((-28,43,9),(25,39,18),(7,15,32)):
        ellipsoid('Embedded sparse growth',(x,y,z),(4,1.1,3),'moss',16,8)
    bpy.context.view_layer.update()
    for obj in list(bpy.context.scene.objects):
        if obj.type!='MESH':continue
        matrix=obj.matrix_world.copy()
        for vertex in obj.data.vertices:
            p=matrix@vertex.co;vertex.co=xyz(settle((p.x,p.z,-p.y)))
        obj.matrix_world=Matrix.Identity(4);obj.data.update()
        if any(key in obj.name for key in ('shield','shingle','shoulder','helmet','lamella','plate')):
            original=len(obj.data.materials)
            for key in ('rust','worn'):obj.data.materials.append(bpy.data.materials[key])
            for face in obj.data.polygons:
                p=face.center;field=math.sin(p.x*.23+p.z*.11)+.65*math.sin(p.y*.21-p.z*.12)
                if field>1.22:face.material_index=original
                elif field< -1.45:face.material_index=original+1
    deposits([(20,16,30,25,7,25),(1,27,25,19,4,-15),(-37,-27,19,23,1.8,-18),
              (34,-17,19,21,1.6,16)],8,(-62,65,-70,49))
    for optic in optics+[port for hand in pincers for port in hand['ports']]:
        for key in ('center_source','dark_probe_source'):optic[key]=list(settle(optic[key]))
    for hand in pincers:
        hand['center_source']=list(settle(hand['center_source']))
        hand['tine_tips_source']=[list(settle(p)) for p in hand['tine_tips_source']]
    save('relics/colossus/design/small-colossus-v6.json',{
        'name':'Small Colossus V6 / Overlapping forged armour','reference':base.REFERENCE,
        'visual_acceptance':'Alpha 4.2 screenshot follow-up; review pending',
        'revision_v6':{'source':str(SOURCE.relative_to(ROOT)).replace('\\','/'),'source_sha256':digest,
                       'feedback':'Alpha 4.2: spherical shoulders/back/head and disconnected-looking pale pincers',
                       'overlapping_plate_count':len(PLATES),'plate_probes_source':[list(settle(p)) for p in PLATES],
                       'sphere_based_body_and_shoulders':False,'forward_shear':-.31},
        'revision_v4':{'closed_source_head_volume':volume,'head_optics':optics,'pincers':pincers,
                       'grille_rib_probes_source':[list(settle(p)) for p in grille],
                       'solid_core_probes_source':[list(settle(p)) for p in [(0,20,10),(0,53,0)]],
                       'body_connection_source':list(settle((0,20,10))),
                       'head_connection_source':list(settle((0,60,-5))),
                       'continuous_body_source_y':[13,23,34],
                       'hidden_completion_authored':['back','second arm attachment','buried body','pincer anatomy']},
        'new_relic_v1':{'family':'small-colossus','v5_interiors':False}})
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest


if __name__=='__main__':main()
