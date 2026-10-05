"""New compact bronze-machine relative of the large Colossus, authored from primitives."""
import math
from pathlib import Path
import sys

import bpy
from mathutils import Matrix,Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *
import create_colossus_v3 as large


def shell(name,center,radii,thickness=2.5,mat='armor'):
    obj=ellipsoid(name,center,radii,mat,40,26)
    subtract(obj,ellipsoid('Inner armour cavity',center,tuple(r-thickness for r in radii),mat,36,24))
    return obj


def hand():
    wrist=Vector((34,5,-42))
    thumbward,distal,palmar=Vector((1,0,0)),Vector((0,0,-1)),Vector((0,1,0))
    basis=Matrix((thumbward,distal,palmar)).transposed()
    def p(u,v,w):return tuple(wrist+basis@Vector((u,v,w)))
    cylinder('Detached hand | wrist bearing',p(0,-2,0),p(0,2,0),4.2,'joint',24)
    palm=ellipsoid('Detached hand | curved palm',p(0,6,0),(8,3.5,6.5),'plate',28,18)
    large.weather(palm,'plate')
    box('Detached hand | recessed palmar plate',p(0,6,3.3),(8,1.2,7),'joint',.7)
    tips=[]
    for name,u,length,curl in [('little',-6,9,4),('ring',-2,12,6),('middle',2,13,6.5),('index',6,11,5)]:
        points=[p(u,10,0),p(u,10+length*.45,.5),p(u,10+length*.85,curl*.5),p(u,10+length,curl)]
        for j,(a,b) in enumerate(zip(points,points[1:])):
            cylinder('Detached hand | '+name+f' phalanx {j+1}',a,b,1.45-j*.13,'armor',12)
            ellipsoid('Detached hand | articulated knuckle',a,(1.6,1.6,1.6),'joint',12,8)
        tips.append(list(points[-1]))
    tapered('Detached hand | opposing thumb',[p(6,3,0),p(11,6,1),p(12,12,4)],[2,1.7,1.4],'plate',12)
    return {'anatomical_side':'right','basis_determinant':basis.determinant(),
            'palmar_normal_source':list(palmar),'finger_tips_source':tips,'wrist_source':list(wrist)}


def main():
    reset({**large.COLORS,'terrain_top':'586d3b','terrain_patch':'6a563d','terrain_fill':'674c37'})
    large.RNG.seed(20261004)
    chest=shell('01 | Slumped broad curved cuirass',(0,22,4),(25,28,18),3)
    damage(chest,(10,17,-12),(11,13),23)
    damage(chest,(-11,27,20),(6,10),14)
    subtract(chest,box('Broken lower waist',(12,-7,0),(20,10,38),'joint'))
    large.weather(chest)
    # Off-center lower tear with actual visible structure instead of a circular chest window.
    for x in (-16,-5,7,16):
        tapered('02 | Internal load-bearing frame',[(x,-8,8),(x,13,10),(x*.7,35,9),(-5,46,2)],
                [2,1.7,1.6,1.5],'joint',12)
    cylinder('Internal cross brace',(-15,12,10),(14,32,9),1.4,'joint',12)
    cylinder('Fractured lower drive member',(7,-6,4),(8,14,3),3.2,'joint',20)
    large.shell_seams((0,22,4),(25,28,18),[22,51],[-63,-25,30,65],'Cuirass',min_latitude=25)
    # Shoulder mass and a low bent supporting arm produce a different compact stance.
    left=shell('03 | Grounded left shoulder armour',(-24,31,5),(15,18,17),2.7,'plate')
    damage(left,(-33,23,-8),(5,7),15);large.weather(left,'plate')
    cylinder('Left upper-arm bearing',(-28,27,4),(-33,14,-2),6,'joint',24)
    arm=ellipsoid('Left supporting forearm',(-33,10,-9),(8,12,11),'armor',32,20);large.weather(arm)
    cylinder('Left wrist pressed into earth',(-33,5,-15),(-33,4,-20),5,'joint',20)
    ellipsoid('Grounded left hand',(-33,3,-22),(7.5,4,6),'plate',24,16)
    for x in (-38,-34.5,-31,-27.5):
        tapered('Left grounded curled finger',[(x,4,-24),(x,2,-29),(x,0,-29)],[1.5,1.4,1.2],'armor',10)
    right=shell('04 | Higher torn right shoulder',(25,32,5),(13,15,16),2.5)
    damage(right,(29,22,-7),(7,9),23);large.weather(right)
    cylinder('Exposed right shoulder axle',(23,31,4),(31,26,-2),5,'joint',24)
    cylinder('Severed right upper-arm stump',(30,26,-2),(34,20,-5),5.7,'plate',24)
    large.arc('Broken elbow bearing',(34,20,-5),(0,-1,-.4),5.8,.9,'joint',20,320)
    cylinder('05 | Rolled low neck collar',(-5,42,2),(-5,48,2),12,'joint',36)
    large.arc('Collar bronze lip',(-5,46,2),(0,1,0),12.8,1.2,'edge')
    # Family likeness: domed helmet, narrow recessed visor, filters and a ribbed hose.
    before=set(bpy.data.objects)
    center=(-5,57,2);radii=(14,16,14)
    head=shell('06 | Listed compact diving dome',center,radii,2)
    subtract(head,box('Visor opening',(-5,59,-11),(23,3.5,10),'dark'))
    damage(head,(2,68,-7),(3,4),10)
    large.weather(head)
    ellipsoid('Unlit recessed helmet interior',center,(11.5,13.5,11.5),'dark',28,18)
    large.shell_seams(center,radii,[42],[-50,10,65],'Dome',min_latitude=25)
    for y,lat in [('brow',12),('lower lip',-3)]:
        large.tube('Curved visor '+y,[large.sphere_point(center,radii,lat,lon,.5) for lon in range(-53,54,5)],.7,'plate')
    for side in (-1,1):
        x=-5+side*13
        cylinder('Helmet side filter',(x-side*2,53,2),(x+side*3,53,2),5,'plate',24)
        cylinder('Recessed filter grill',(x+side*3,53,2),(x+side*3.3,53,2),3.6,'dark',24)
        large.arc('Filter rolled rim',(x+side*3.4,53,2),(1,0,0),4.4,.7,'edge')
        for z in (0,2,4):cylinder('Filter grille',(x+side*3.6,50,z),(x+side*3.6,56,z),.45,'joint',8)
    hose=large.catmull([(-18,52,-1),(-18,48,-10),(-8,47,-16),(4,49,-14),(9,53,0)],4)
    large.tube('Ribbed helmet respirator',hose,2.2,'plate',12)
    for i in range(2,len(hose)-2,3):
        direction=(hose[i+1]-hose[i-1]).normalized()
        cylinder('Hose coupling',hose[i]-direction*.45,hose[i]+direction*.45,2.6,'edge',12)
    cylinder('Offset respirator outlet',(3,49,-13),(3,49,-18),3.4,'plate',24)
    cylinder('Outlet recess',(3,49,-18),(3,49,-18.4),2.2,'dark',20)
    large.vegetation(center,radii,[(40,37,68)],'Sheltered dome growth')
    pivot=Vector(xyz((-5,46,2)))
    transform=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(-9),4,'Y')@Matrix.Rotation(math.radians(7),4,'Z')@Matrix.Translation(-pivot)
    for obj in set(bpy.data.objects)-before:obj.matrix_world=transform@obj.matrix_world
    # A broken short sleeve lies forward of the matching shoulder, rather than behind the body.
    a,b=Vector((37,6,-14)),Vector((34,5,-40));axis=(b-a).normalized()
    sleeve=cylinder('07 | Detached tapered forearm shell',a,b,7.4,'armor',32)
    subtract(sleeve,cylinder('Open sleeve cavity',a-axis*2,b+axis*2,5,'joint',28))
    damage(sleeve,(40,10,-17),(4,4),13);large.weather(sleeve)
    for t in (.13,.78,.96):large.arc('Forearm rolled band',a.lerp(b,t),axis,7.5,.8,'edge')
    cylinder('Forearm inner mechanism',a+axis*3,b-axis*2,2,'joint',16)
    pose=hand()
    for x,y,z,rx,ry,rz in [(-26,46,1,7,2,7),(-35,19,-7,4,2,5),(-9,42,-8,5,2,4),
                          (19,35,-7,4,3,3),(39,12,-24,3,1.5,5),(-19,17,18,4,4,2)]:
        ellipsoid('Localized overgrowth',(x,y,z),(rx,ry,rz),'moss',20,12)
    for x,z,s in [(20,-24,5),(-19,-20,4),(39,-5,4)]:
        piece=box('Fallen armour fragment',(x,1.2,z),(s,2.5,s*.7),'plate',.6);piece.rotation_euler.z=.4
    deposits([(-25,-10,20,20,2.7,-15),(9,8,24,19,3,0),(36,-26,12,23,1.8,0),
              (33,-51,12,14,1.2,0)],8,(-48,52,-69,35))
    save('relics/colossus/design/small-colossus-v2.json',{
        'name':'Small Colossus V2','visual_acceptance':'V2 review pending',
        'revision_v2':{'direction':'Independent relative of accepted large Colossus',
                       'archive_meshes_reused':0,'large_asset_meshes_reused':0,
                       'features':['listed dome helmet','curved visor and ribbed respirator','broad bronze-coloured armour',
                                   'asymmetric supporting arm','lower irregular chest tear','connected internal frame']},
        'new_relic_v1':{'family':'small-colossus','hand':pose,
                        'void_probes_source':[[10,17,-13],[-11,27,20]],
                        'solid_probes_source':[[-5,45,2],[-16,12,9]],'v5_interiors':False,'rewards_inherited':False}})


if __name__=='__main__':main()
