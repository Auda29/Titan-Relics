"""Independent rounded skull with a giant diagonal sword; no copied crown or spine."""
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector,Matrix

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *
import create_colossus_v3 as shapes


def nasal_cutter():
    vertices=[(x,y,z) for z in (-62,9) for x,y in [(-6,27),(6,27),(0,42)]]
    obj=mesh('Triangular nasal aperture',vertices,[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],'bone')
    recalculate(obj);return obj


def sword(skull):
    # Front is -Z, so anatomical +X is image-left in a front inspection view.
    origin=Vector((17,62,-4));axis=Vector((.307,.946,.105)).normalized()
    side=Vector((axis.y,-axis.x,0)).normalized();normal=side.cross(axis).normalized()
    def point(t,u=0,v=0):return tuple(origin+axis*t+side*u+normal*v)
    # Cut a real impact collar around the blade before adding the blade itself.
    impact=box('Sword impact cutter',(0,0,0),(17,36,10),'bone',1)
    basis=Matrix((side,axis,normal)).transposed()
    change=Matrix(((1,0,0),(0,0,-1),(0,1,0)))
    transform=Matrix.Translation(Vector(xyz(point(-3))))@(change@basis@change.inverted()).to_4x4()
    impact.matrix_world=transform@impact.matrix_world
    subtract(skull,impact)
    for points in [[(22,61,-7),(28,58,-17),(31,54,-22)],[(13,61,-6),(5,63,-13),(-2,62,-16)]]:
        subtract(skull,tapered('Impact fracture cutter',points,[1.7,1.4,.8],'bone',7))
    # Two crushed cortical lips clamp the blade; a wide air collar alone would
    # leave the enormous weapon touching only a few corner voxels after conversion.
    for sign in (-1,1):
        unite(skull,tapered('Surviving bone lip at sword entry',
                           [point(-8,sign*10.5),point(-5,sign*8),point(-2,sign*5.5)],
                           [3.1,2.8,2.3],'bone',14))
    vertices=[]
    sections=[(-24,2),(-16,8),(-10,10.5),(0,11),(7,11),(14,11.2),(21,11.4),(28,11.5),(35,11.5),(40,11),(44,10)]
    for t,w in sections:
        vertices.extend([point(t,-w/2,0),point(t,0,-2.8),point(t,w/2,0),point(t,0,2.8)])
    faces=[(3,2,1,0)]
    for j in range(len(sections)-1):
        for k in range(4):faces.append((j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k))
    faces.append(tuple(range(len(vertices)-4,len(vertices))))
    blade=mesh('04 | Embedded mineralized sword blade',vertices,faces,'blade');recalculate(blade)
    blade.data.materials.append(bpy.data.materials['edge'])
    blade.data.materials.append(bpy.data.materials['moss'])
    for poly in blade.data.polygons:
        poly.material_index=int(poly.index%4==1)
        level=(poly.index-1)//4
        if 3<=level<=6 and poly.index%4 in (0,1):poly.material_index=2
    # Fine recessed blade ridge, not a glowing stripe or valuable metal core.
    tapered('Sword long weathered ridge',[point(-16,0,-2.8),point(17,0,-2.8),point(41,0,-2.8)],[.7,.9,.7],'edge',8)
    guard=[point(40,-20,0),point(43,-13,0),point(44,0,0),point(43,13,0),point(40,20,0)]
    guard_obj=tapered('05 | Broad curved sword crossguard',guard,[2.8,3.2,3.5,3.2,2.8],'hilt',14)
    guard_obj.data.materials.append(bpy.data.materials['moss'])
    for face in guard_obj.data.polygons:face.material_index=int(face.normal.z>.25)
    cylinder('06 | Wrapped giant sword grip',point(45),point(68),2.6,'band',16)
    for t in range(47,69,4):cylinder('Grip wrapping band',point(t-.65),point(t+.65),2.85,'hilt',16)
    ellipsoid('07 | Sword pommel',point(71),(3.6,4,3.6),'hilt',20,14)
    # Growth hangs from the guard without covering the recognisable cross shape.
    for u,length in [(-17,9),(-10,13),(13,10),(19,7)]:
        p=Vector(point(42,u,0))
        tapered('Moss hanging from crossguard',[p,p+Vector((.8,-length*.5,.2)),p+Vector((.4,-length,0))],[1.2,.8,.25],'growth',8)
    return {'entry_source':list(origin),'axis_source':list(axis),'top_source':list(point(75)),
            'crossguard_source':list(point(44)),'crossguard_width':40,'buried_blade_axis_length':24,
            'surviving_contact_lips':2,
            'valuable_metal_blocks_expected':0}


def main():
    reset({'bone':'c7b999','worn':'e0d7bb','mineral':'95826a','moss':'586c35','growth':'454f2c',
           'root':'66513d','blade':'777e73','edge':'a0a393','hilt':'424b47','band':'655e4d'})
    shapes.RNG.seed(403)
    skull=organic('01 | Rounded cranium and open jaw',(0,37,8),(41,27,37),'bone',.6)
    unite(skull,organic('Upper maxilla',(0,29,-24),(28,10,19),'bone',.45))
    unite(skull,organic('Low rounded mandible',(0,-4,-17),(32,8,26),'bone',.4))
    for s in (-1,1):
        unite(skull,tapered('Continuous jaw rail',[(s*31,37,-8),(s*30,23,-18),(s*29,7,-27),(s*24,-5,-32)],
                           [7,5.5,5.5,7],'bone',18))
    subtract(skull,organic('Open cranial interior',(0,38,9),(34,21,30),'bone',.15))
    subtract(skull,organic('Oral chamber',(0,13,-13),(23,22,24),'bone',.1))
    subtract(skull,organic('Deep open mouth',(0,12,-38),(17,15,25),'bone',.15))
    for s in (-1,1):
        cutter=organic('Real deep eye socket',(s*18,43+(1 if s<0 else 0),-24),(12,10,25),'bone',.35)
        subtract(skull,cutter)
    subtract(skull,nasal_cutter())
    for s in (-1,1):
        # Bone arches join the face to the jaw; nothing projects like a horn/crown.
        unite(skull,tapered('02 | Cheek support arch',[(s*9,27,-37),(s*24,26,-38),(s*35,28,-21)],
                           [3.5,4.5,5],'bone',16))
        unite(skull,tapered('Orbital brow',[(s*7,51,-23),(s*18,55,-24),(s*29,51,-18)],
                           [2.6,3,2.6],'bone',14))
    damage(skull,(28,37,37),(4,6),14)
    # Teeth are uneven and intentionally omit two upper and one lower positions.
    teeth=[]
    for i,x in enumerate([-23,-16,-9,-2,5,12,19,25]):
        if i in (2,6):continue
        y=27-abs(x)*.11
        teeth.append(tapered('03 | Worn upper tooth',[(x,y,-38),(x*.98,y-5,-41),(x*.96,y-9-(i%2),-40)],
                            [3.3,2.7,2.1],'worn',9))
    for i,x in enumerate([-22,-14,-6,3,12,21]):
        if i==4:continue
        teeth.append(tapered('03 | Worn lower tooth',[(x,-4,-36),(x,1+i%3,-39)],[3.1,1.9],'worn',9))
    # Fuse anatomical transitions, then perform the weapon impact on that continuous form.
    for tooth in teeth:unite(skull,tooth)
    remesh=skull.modifiers.new('Continuous rounded bone','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.62;apply(skull,remesh)
    smooth=skull.modifiers.new('Worn bone transitions','SMOOTH');smooth.factor=.6;smooth.iterations=2;apply(skull,smooth)
    decimate=skull.modifiers.new('Large fossil planes','DECIMATE');decimate.ratio=.34;apply(skull,decimate)
    weapon=sword(skull)
    skull.data.materials.clear()
    for mat in ('bone','worn','mineral','moss'):skull.data.materials.append(bpy.data.materials[mat])
    for face in skull.data.polygons:
        p=skull.matrix_world@face.center;normal=skull.matrix_world.to_3x3()@face.normal
        x,y,z=p.x,p.z,-p.y
        field=math.sin(x*.085+z*.055)+.6*math.cos(z*.13-y*.045)
        face.material_index=0
        if field<-.95:face.material_index=2
        if y<23 and z<-28:face.material_index=1
        if normal.z>.18 and field>.12 and y>18:face.material_index=3
    for i,(x,y,z) in enumerate([(-31,40,-12),(31,38,-11),(-29,57,8),(23,55,20),(-18,33,38)]):
        # Attached drapes follow the solid outer cheeks/rear, away from aperture centers.
        tapered('08 | Draped old root',[(x,y,z),(x*1.04,y-8,z+1),(x*1.02,y-15,z+2)],[.9,.65,.3],'root',8)
    deposits([(-29,-7,22,31,7,-15),(30,4,23,34,8,20),(0,31,31,24,5,0),
              (-34,-31,16,19,2.5,-15),(35,-28,17,19,3,15)],12,(-54,56,-58,60))
    for x,y,z in [(-43,2,-12),(40,1,-36),(20,.5,48)]:
        ellipsoid('09 | Local broken bone chip',(x,y,z),(4,2.5,5),'mineral',16,10)
    save('relics/titan-skull/design/titan-skull-2-v1.json',{
        'name':'Titan Skull 2 V1','reference':'https://www.instagram.com/reel/Db9KCtWi0eG/',
        'reference_seconds':[0,6],
        'new_relic_v1':{'family':'skull-2','void_probes_source':[[0,11,-44],[-18,44,-28],[18,43,-28],[0,33,-36]],
            'solid_probes_source':[[0,37,44]],'sword':weapon,
            'features':['round uncrowned cranium','open sockets and mouth','diagonal embedded sword','missing teeth','patchy damp deposits'],
            'crown_included':False,'spine_included':False,'v5_interiors':False,
            'placement_setting':'large lush grotto or open sinkhole; cave shell is not exported'}})


if __name__=='__main__':main()
