"""Slender sunken sentinel: elongated mask, exposed waist, lamellar shoulders and long arms."""
import math
from pathlib import Path
import sys

import bpy
from mathutils import Matrix,Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *
import create_colossus_v3 as shapes


def lean(p):
    x,y,z=p;shift=max(0,y-8)
    return (x-.19*shift,y,z-.065*shift)


def plate(name,outline,depth,material='armor'):
    """Extrude an authored front outline backward; planar facets rather than domed armour."""
    n=len(outline);vertices=list(outline)+[(x,y,z+depth) for x,y,z in outline]
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    faces.extend((i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n))
    obj=mesh(name,vertices,faces,material);recalculate(obj)
    return obj


def torso():
    # Octagonal tapered cuirass: shoulders substantially wider than waist.
    def volume(name,levels,mat):
        vertices=[];faces=[]
        section=[(-1,-.65),(-.65,-1),(.65,-1),(1,-.65),(1,.65),(.65,1),(-.65,1),(-1,.65)]
        for y,rx,rz in levels:vertices.extend((x*rx,y,z*rz+2) for x,z in section)
        for j in range(len(levels)-1):
            for k in range(8):
                a=j*8+k;b=j*8+(k+1)%8;faces.append((a,b,b+8,a+8))
        faces.extend([tuple(reversed(range(8))),tuple(range((len(levels)-1)*8,len(levels)*8))])
        obj=mesh(name,vertices,faces,mat);recalculate(obj);return obj
    chest=volume('01 | Tapered faceted ribcage',[(25,8,7),(32,12,10),(44,15,10),(49,11,7)],'armor')
    subtract(chest,volume('Open ribcage interior',[(23,5,4),(32,9,7),(44,12,7),(51,8,4)],'joint'))
    damage(chest,(9,33,-7),(6,8),19)
    damage(chest,(-6,39,11),(5,7),12)
    # A diagonal missing edge interrupts the otherwise clearly planar breastplate.
    subtract(chest,box('Lost breastplate corner',(13,45,-6),(9,9,11),'joint',1))
    for x in (-7,7):
        cylinder('Ribcage rear supporting rail',(x,23,6),(x*.8,48,4),1.6,'joint',12)
    cylinder('Upper crossmember',(-10,45,4),(10,45,4),1.8,'joint',12)
    plate('02 | Offset narrow sternum plate',[(-6,46,-9),(-1,48,-9),(3,39,-9),(-1,29,-7),(-5,31,-7)],1.8,'plate')
    plate('Upper left breast bevel',[(-12,43,-7),(-8,46,-8),(-7,35,-8),(-10,32,-6)],1.4,'edge')
    # An exposed narrow articulated abdomen, visibly separate from the chest and pelvis.
    cylinder('03 | Continuous spine',(0,-8,4),(0,53,2),3.4,'joint',16)
    for y in (13,18,23):
        box('Articulated abdominal vertebra',(0,y,2),(12,3.2,10),'joint',.8)
        plate('Overlapping abdominal lamella',[(-5,y+2,-4),(4,y+2,-4),(5,y,-5),(2,y-1,-5),(-5,y,-5)],1.6,'plate')
    for side in (-1,1):
        cylinder('Visible waist tension rod',(side*5,10,3),(side*5,27,4),1.2,'edge',12)
    hip=box('04 | Half-buried angular pelvis',(0,6,6),(24,14,17),'armor',2)
    damage(hip,(8,6,-3),(4,4),9)
    # Kneeling, incomplete upper legs disappear into separate soil contacts.
    for a,b in [((-8,5,6),(-24,-3,-6)),((8,5,6),(19,3,-12))]:
        tapered('Buried folded upper leg',[a,b],[6,5],'plate',8)
    knee=box('Exposed right knee corner',(18,3,-11),(12,9,12),'armor',1.5)
    knee.rotation_euler.z=.25
    cylinder('Visible neck spindle',(0,48,2),(0,58,1),3.2,'joint',16)
    box('Angular neck mounting bracket',(0,51,2),(9,3,8),'plate',1)


def mask():
    # Long, tapered mask with a pointed chin. Two small eye recesses replace the
    # diving helmet's wide visor, side filters, hoses and round rolled collar.
    outline=[(-5.5,74,-6),(-7,69,-7),(-5,59,-8),(0,55,-8),
             (5,59,-8),(7,69,-7),(5.5,74,-6),(0,77,-5)]
    head=plate('05 | Long hollow sentinel mask',outline,12,'armor')
    inner=[(-3.5,73,-3),(-4.5,68,-4),(-3,60,-4),(0,58,-4),
           (3,60,-4),(4.5,68,-4),(3.5,73,-3),(0,74,-2)]
    subtract(head,plate('Mask internal cavity',inner,8,'joint'))
    for side in (-1,1):
        cutter=box('Deep individual eye recess',(side*3.4,68,-7),(3.7,2.7,8),'dark')
        cutter.rotation_euler.y=math.radians(-side*12)
        subtract(head,cutter)
        box('Recessed unlit eye',(side*3.4,68,-3.7),(3.4,2.2,.8),'dark')
    plate('Raised vertical mask keel',[(-.8,73,-7.3),(.8,73,-7.3),(1.2,64,-9.5),(0,59,-10),(-1.2,64,-9.5)],1.4,'plate')
    plate('Left tapered cheek',[(-6,65,-8),(-2,64,-9),(-1.5,58,-9),(-4,60,-8)],1.3,'plate')
    plate('Right tapered cheek',[(6,65,-8),(2,64,-9),(1.5,58,-9),(4,60,-8)],1.3,'plate')
    damage(head,(-4,73,-5),(2.5,3),11)
    # Recessed rear spine detail; no spherical ear housings.
    box('Mask rear vertical service panel',(0,67,5),(4,13,2),'joint',.4)
    for y in (63,67,71):box('Rear mask fastener',(0,y,6.1),(2,1,1),'edge',.15)


def arm_member(name,a,b,width_a,width_b):
    a,b=Vector(a),Vector(b);axis=(b-a).normalized()
    side=axis.cross(Vector((0,0,1))).normalized();front=side.cross(axis).normalized()
    if front.z>0:front=-front
    cylinder(name+' | internal actuator',a,b,min(width_a,width_b)*.52,'joint',16)
    # Three long faceted shields leave one service-side slot open along the limb.
    for turn,material in [(-.88,'armor'),(0,'plate'),(.88,'armor')]:
        radial=(front*math.cos(turn)+side*math.sin(turn)).normalized()
        tangent=axis.cross(radial).normalized();points=[]
        for t,w in ((.09,width_a),(.83,width_b)):
            c=a.lerp(b,t)+radial*w*.82
            points.extend((c-tangent*w*.42,c+tangent*w*.42))
        # Four outer corners and a radial inner layer form a thick longitudinal plate.
        p0,p1,p2,p3=points
        outer=[p0,p1,p3,p2];vertices=[tuple(p) for p in outer]+[tuple(p-radial*1.6) for p in outer]
        obj=mesh(name+' | longitudinal armour',vertices,[(0,3,2,1),(4,5,6,7),(0,1,5,4),
                     (1,2,6,5),(2,3,7,6),(3,0,4,7)],material);recalculate(obj)
    for t,w in ((.08,width_a),(.87,width_b)):
        p=a.lerp(b,t);cylinder(name+' | joint coupling',p-axis*.8,p+axis*.8,w*.87,'edge',12)


def right_hand(wrist):
    wrist=Vector(wrist);basis=Matrix((Vector((1,0,0)),Vector((0,0,-1)),Vector((0,1,0)))).transposed()
    def p(u,v,w):return tuple(wrist+basis@Vector((u,v,w)))
    box('Right hand | long flat palm',p(0,4.5,0),(11,4,10),'armor',1)
    box('Right hand | recessed palm joint',p(0,4.5,2.2),(6,1,6),'joint',.5)
    tips=[]
    for name,u,length,curl in [('little',-4.6,7,2),('ring',-1.5,9,3),('middle',1.5,10,3.5),('index',4.6,8,2.5)]:
        points=[p(u,9,0),p(u,9+length*.55,0),p(u,9+length,curl)]
        for i,(a,b) in enumerate(zip(points,points[1:])):
            cylinder(f'Right hand | {name} finger {i+1}',a,b,1.2-i*.1,'plate',10)
            ellipsoid('Right hand | knuckle',a,(1.3,1.3,1.3),'joint',12,8)
        tips.append(list(points[-1]))
    tapered('Right hand | opposing thumb',[p(4,2,0),p(8,6,1),p(9,10,2)],[1.6,1.3,1.1],'armor',10)
    return {'anatomical_side':'right','basis_determinant':basis.determinant(),
            'palmar_normal_source':[0,1,0],'finger_tips_source':tips,'wrist_source':list(wrist)}


def arms():
    # Shoulders overlap in flat steps; neither shoulder is a round shell.
    for side in (-1,1):
        cylinder('Shoulder load-bearing axle',(side*9,45,3),(side*23,43,3),3,'joint',16)
        for j in range(3):
            x=side*(15+j*4);y=48-j*2.6
            outline=[(x-side*5,y+1,-5),(x+side*4,y,-4),(x+side*6,y-6,-3),(x-side*4,y-7,-4)]
            shoulder=plate('06 | Stepped shoulder lamella',outline,13,'armor' if j!=1 else 'plate')
            if side==1 and j==2:damage(shoulder,(x+side*2,y-4,-2),(2.5,3),10)
    left=[(-24,41,3),(-39,23,-1),(-45,5,-19)]
    right=[(24,41,3),(29,24,0),(22,5,-24)]
    for name,points in [('Left',left),('Right',right)]:
        for i,(a,b) in enumerate(zip(points,points[1:])):
            arm_member(name+f' arm segment {i+1}',a,b,4.8-i*.6,3.8-i*.4)
        elbow=Vector(points[1]);cylinder(name+' exposed elbow bearing',elbow+Vector((-3,0,0)),elbow+Vector((3,0,0)),4,'joint',16)
    box('Left hand | grounded supporting palm',(-45,3,-23),(11,5,10),'armor',.8)
    for i,x in enumerate((-49,-46,-43,-40)):
        tapered('Left hand | spread grounded digit',[(x,3,-27),(x-1,1,-33-i%2),(x-1,-1,-34-i%2)],
                [1.35,1.2,1.1],'plate',10)
    tapered('Left hand | grounded thumb',[(-50,3,-22),(-54,2,-26),(-54,0,-30)],[1.8,1.5,1.2],'armor',10)
    return right_hand(right[-1])


def main():
    reset({'armor':'666158','plate':'705b49','edge':'567563','worn':'777767','rust':'654937',
           'patina':'567563','joint':'303b3a','dark':'172020','moss':'536739','growth':'425333'})
    shapes.RNG.seed(202610041)
    torso();mask();pose=arms()
    # Weathering is concentrated at joints and ledges rather than covering the mask.
    for p,r in [((-16,48,5),(4,1.4,4)),((13,42,7),(3,2,3)),((-7,9,11),(5,2,4)),
                ((-43,8,-15),(3,1.3,4)),((0,75,1),(3,1.4,3)),((-11,32,7),(2,5,2))]:
        ellipsoid('Sheltered ledge growth',p,r,'moss',16,10)
    # Apply one continuous sideways/forward list to the machine, leaving soil in world space.
    bpy.context.view_layer.update()
    for obj in [o for o in bpy.context.scene.objects if o.type=='MESH']:
        transform=obj.matrix_world.copy()
        for vertex in obj.data.vertices:
            p=transform@vertex.co
            vertex.co=xyz(lean((p.x,p.z,-p.y)))
        obj.matrix_world=Matrix.Identity(4);obj.data.update()
    pose['finger_tips_source']=[list(lean(p)) for p in pose['finger_tips_source']]
    pose['wrist_source']=list(lean(pose['wrist_source']))
    for x,z,w in [(-23,-13,5),(12,20,4),(-32,7,4)]:
        obj=box('Fallen flat armour fragment',(x,.6,z),(w,1.6,w*1.4),'plate',.3);obj.rotation_euler.z=.45
    deposits([(-9,7,24,23,2.3,0),(-43,-23,16,19,1.6,-15),(23,-28,14,22,1.5,15),
              (18,-8,18,18,2.1,0)],8,(-62,46,-53,36))
    save('relics/colossus/design/small-colossus-v3.json',{
        'name':'Small Colossus V3 / Sunken Sentinel','visual_acceptance':'V3 review pending',
        'revision_v3':{'direction':'User-selected slender sentinel with a clearly distinct silhouette',
                       'archive_meshes_reused':0,'large_asset_meshes_reused':0,
                       'features':['elongated tapered mask','two individual recessed eyes','narrow articulated waist',
                                   'flat stepped shoulder armour','two long attached arms','sideways sunken kneeling pose'],
                       'sideways_shear':-.19,'forward_shear':-.065,
                       'collar_probe_source':list(lean((0,52,2))),
                       'head_connection_probe_source':list(lean((0,73,-6))),
                       'waist_band_source_y':[15,22],'chest_band_source_y':[38,44]},
        'new_relic_v1':{'family':'small-colossus','hand':pose,
                        'void_probes_source':[list(lean((9,33,-7))),list(lean((-6,39,11)))],
                        'solid_probes_source':[list(lean((0,52,2))),list(lean((0,18,2)))],
                        'v5_interiors':False,'rewards_inherited':False}})


if __name__=='__main__':main()
