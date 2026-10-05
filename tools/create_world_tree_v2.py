"""Branch-grown World Tree: irregular fine canopy and tapered roots instead of leaf shelves."""
import math
from pathlib import Path
import random
import sys

import bpy
from mathutils import Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *

RNG=random.Random(20261004)


def curved(name,points,radii,mat='wood',sides=14):
    samples=catmull(points,4)
    widths=[]
    for i in range(len(radii)-1):
        widths.extend(radii[i]+(radii[i+1]-radii[i])*j/4 for j in range(4))
    widths.append(radii[-1])
    return tapered(name,samples,widths,mat,sides,True)


def trunk():
    levels=[(-8,0,0,22,18),(0,0,0,21,18),(15,1,1,18,15),(38,4,2,15,13),
            (62,7,3,13,11),(85,8,1,11,9),(108,4,2,9,8),(130,-1,5,6,5),
            (148,-5,7,3,2.7),(166,-8,9,.9,.8)]
    def ring(y):
        a,b=next((a,b) for a,b in zip(levels,levels[1:]) if a[0]<=y<=b[0])
        t=(y-a[0])/(b[0]-a[0]);x,z,rx,rz=[a[k]+(b[k]-a[k])*t for k in range(1,5)]
        result=[]
        for k in range(40):
            angle=k*math.tau/40
            # Broad asymmetric buttresses fade upward; irregular bark, no regular spiral braid.
            lobes=1+(.16*math.exp(-max(y,0)/55)+.045)*math.sin(5*angle+.4)+.045*math.sin(9*angle+y*.013)
            result.append((x+rx*lobes*math.cos(angle),y,z+rz*lobes*math.sin(angle)))
        return result
    ys=[-8+2*i for i in range(88)];vertices=[p for y in ys for p in ring(y)];faces=[]
    for j in range(len(ys)-1):
        for k in range(40):
            a=j*40+k;b=j*40+(k+1)%40;faces.append((a,b,b+40,a+40))
    faces.extend([tuple(reversed(range(40))),tuple(range((len(ys)-1)*40,len(ys)*40))])
    obj=mesh('01 | Asymmetric living trunk',vertices,faces,'wood');recalculate(obj)
    obj.data.materials.append(bpy.data.materials['bark'])
    for poly in obj.data.polygons:
        p=poly.center;angle=math.atan2(-p.y,p.x)
        poly.material_index=int(math.sin(angle*5+.2)>.95 and 12<p.z<92)
    vertices=[];faces=[]
    for i in range(math.ceil(174/.65)+1):
        y=min(166,-8+i*.65);start=len(vertices);vertices.extend(ring(y));faces.append(tuple(range(start,start+40)))
    mesh('Solid trunk internal slices',vertices,faces,'wood')
    return levels


def leaves(name,center,radii):
    # Small overlapping, non-axis-aligned cushions live on actual terminal twigs.
    # Their irregular union forms the crown; there is no parent umbrella/shelf mesh.
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=xyz(center))
    obj=bpy.context.object;phase=RNG.uniform(0,math.tau)
    for vertex in obj.data.vertices:
        p=vertex.co.copy()
        rough=1+.16*math.sin(7*p.x+3*p.y+phase)+.11*math.sin(9*p.z-4*p.x-phase)
        vertex.co=Vector((p.x*radii[0]*rough,p.y*radii[2]*rough,p.z*radii[1]*rough))
    obj.rotation_euler.z=RNG.uniform(-math.pi,math.pi)
    finish(obj,name,'leaf_light' if RNG.random()<.16 else 'leaves')
    inner=obj.copy();inner.data=obj.data.copy();inner.name=name+' | inner leaves'
    bpy.context.collection.objects.link(inner)
    for vertex in inner.data.vertices:vertex.co*=.72


def crown():
    scaffold=[([(7,70,3),(-11,92,1),(-36,114,1),(-65,131,3)],[10,8,5,2.5]),
              ([(7,82,2),(24,103,-5),(45,123,-16),(66,138,-23)],[9.5,7,4.5,2.2]),
              ([(5,96,4),(-7,120,22),(-26,146,39),(-41,162,56)],[8.5,6.5,4,1.9]),
              ([(3,110,3),(21,134,13),(41,156,28),(56,171,33)],[8,6,3.5,1.7]),
              ([(8,77,0),(18,96,-21),(29,111,-43),(40,123,-59)],[8.5,6.5,4,1.8]),
              ([(0,125,5),(-17,149,0),(-35,171,-11),(-44,182,-19)],[6,4.5,2.8,1.4]),
              ([(-3,135,7),(4,157,9),(12,177,4),(17,190,0)],[5,3.7,2.3,1.1]),
              ([(2,119,4),(-5,143,-17),(-9,165,-34),(-15,179,-49)],[6.5,4.7,3,1.5]),
              ([(-2,132,6),(-10,157,20),(-12,179,30),(-8,187,39)],[5.5,4,2.4,1.1])]
    terminals=0;tip_probes=[]
    for i,(points,radii) in enumerate(scaffold):
        curved(f'02 | Primary living bough {i+1}',points,radii)
        direction=(Vector(points[-1])-Vector(points[-2])).normalized()
        lateral=Vector((-direction.z,0,direction.x)).normalized()
        for j in range(5):
            t=.25+j*.17;start=Vector(points[-2]).lerp(Vector(points[-1]),t)
            side=(-1 if j%2 else 1)*RNG.uniform(10,20)
            end=start+direction*RNG.uniform(8,15)+lateral*side+Vector((0,RNG.uniform(5,12),0))
            mid=start.lerp(end,.52)+Vector((0,-2,0))
            curved(f'03 | Secondary fork {i+1}.{j+1}',[start,mid,end],[2.5,1.6,.8],sides=10)
            for k in range(3):
                origin=mid.lerp(end,.30+k*.30)
                tip=end+direction*RNG.uniform(1,7)+lateral*((k-1)*RNG.uniform(6,12))+Vector((0,RNG.uniform(2,8),0))
                curved(f'04 | Terminal spray {terminals+1}',[origin,origin.lerp(tip,.55),tip],[1.3,1,.8],sides=8)
                # Distinct irregular clusters at staggered heights, all overlapping the twig.
                for n,tleaf in enumerate((.42,.75,1)):
                    center=origin.lerp(tip,tleaf)+Vector((RNG.uniform(-1,1),RNG.uniform(0,2),RNG.uniform(-1,1)))
                    radius=RNG.uniform(5.3,8.8)
                    leaves(f'05 | Twig foliage {terminals+1}.{n+1}',center,(radius,RNG.uniform(4.5,7.8),radius*RNG.uniform(.7,1.1)))
                terminals+=1
                tip_probes.append(list(tip))
        # Mid-bough growth joins the terminal crowns into a living canopy. Without
        # these older lateral forks the tree reads as a pollarded candelabra.
        for j in range(3):
            origin=Vector(points[1]).lerp(Vector(points[2]),.15+j*.35)
            side=(-1 if j%2 else 1)*RNG.uniform(12,22)
            tip=origin+direction*RNG.uniform(12,20)+lateral*side+Vector((0,RNG.uniform(12,22),0))
            mid=origin.lerp(tip,.55)
            curved(f'Inner crown lateral {i+1}.{j+1}',[origin,mid,tip],[2.4,1.5,.9],sides=10)
            for k in (-1,1):
                end=tip+lateral*k*RNG.uniform(5,10)+Vector((0,RNG.uniform(2,7),0))
                curved(f'Inner crown terminal {terminals+1}',[mid,tip,end],[1.4,1,.8],sides=8)
                for n,tleaf in enumerate((.3,.65,1)):
                    center=mid.lerp(end,tleaf)+Vector((0,2,0));radius=RNG.uniform(6.5,9.5)
                    leaves(f'05 | Inner crown foliage {terminals+1}.{n+1}',center,(radius,radius*.8,radius*.85))
                terminals+=1;tip_probes.append(list(end))
    return terminals,tip_probes


def roots():
    for i,(angle,length,width,arch) in enumerate([(-157,54,12,False),(-102,48,10,True),
                                               (-39,63,13,True),(24,49,10,False),
                                               (71,57,11,False),(131,45,9,False),(173,39,8,False)]):
        a=math.radians(angle);d=Vector((math.cos(a),0,math.sin(a)));side=Vector((-d.z,0,d.x))
        points=[d*5+Vector((0,22,0)),d*(length*.38)+Vector((0,13 if arch else 8,0)),
                d*(length*.73)+side*3+Vector((0,5 if arch else 1,0)),d*length+side*6+Vector((0,-3,0))]
        curved(f'06 | Tapered root buttress {i+1}',points,[width,width*.68,3.7,1.2],sides=16)
        for sign in (-1,1):
            start=points[2];end=d*(length+RNG.uniform(5,13))+side*(sign*RNG.uniform(7,14))+Vector((0,-4,0))
            curved(f'Root ground fork {i+1}.{sign}',[start,start.lerp(end,.55)+Vector((0,-1,0)),end],[3.2,1.8,.65],sides=10)
    curved('Old weathered branch scar',[(13,51,3),(25,57,6),(30,59,7)],[6.5,4,2.7])
    cylinder('Healed branch end',(29,58.6,6.8),(30.5,59.3,7.1),2.7,'cut',14)
    for i,(x,z,h) in enumerate([(-36,-15,6),(25,-27,4.5),(-20,26,7)]):
        obj=box(f'Worked stone among roots {i+1}',(x,h/2,z),(5,h,3.5),'stone',.6)
        obj.rotation_euler.z=RNG.uniform(-.4,.4)
    for x,z,r in [(-27,7,6),(14,-21,5),(29,23,7),(-20,-20,4)]:
        ellipsoid('Root contact moss',(x,1.8,z),(r,2,r*.7),'moss',16,10)
    deposits([(-32,-16,22,19,2.2,-15),(36,-23,22,23,2.2,25),(-24,31,25,20,2.4,0),
              (24,32,23,21,2.1,0),(0,4,22,26,1.7,0)],8,(-68,70,-66,68))


def main():
    RNG.seed(20261004)
    reset({'wood':'574531','bark':'756044','cut':'604a34','leaves':'30482d','leaf_light':'46603b',
           'moss':'566c3b','stone':'64705a'})
    levels=trunk();terminals,tip_probes=crown();roots()
    bpy.context.view_layer.update()
    objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
    low,high=bounds(objects);vertical_factor=207/high[2]
    # Keep the accepted working height while retaining natural horizontal branch spread.
    from mathutils import Matrix
    for obj in objects:
        matrix=obj.matrix_world.copy()
        for vertex in obj.data.vertices:
            p=matrix@vertex.co
            if p.z>0:p.z*=vertical_factor
            vertex.co=p
        obj.matrix_world=Matrix.Identity(4);obj.data.update()
    save('relics/world-tree/design/world-tree-v2.json',{
        'name':'World Tree V2','visual_acceptance':'V2 review pending',
        'revision_v2':{'primary_boughs':9,'secondary_boughs':72,'terminal_boughs':terminals,
                       'leaf_clusters':terminals*3,'foliage_parent_shelves':0,'vertical_factor':vertical_factor,
                       'direction':'Asymmetric branch-grown canopy and tapered irregular root forks'},
        'new_relic_v1':{'family':'tree','void_probes_source':[],
                        'solid_probes_source':[[0,20*vertical_factor,0],[4,43*vertical_factor,2],[7,65*vertical_factor,3]],
                        'branch_tip_probes_source':[[x,y*vertical_factor,z] for x,y,z in tip_probes],
                        'trunk_source_levels_before_height_fit':levels,'solid_wood_slice_spacing':.68,
                        'persistent_leaves':True,'v5_interiors':False}})


if __name__=='__main__':main()
