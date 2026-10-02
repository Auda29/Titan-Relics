"""Model a twisted rooted tree, solid woody members and persistent-leaf crown."""
import math
from pathlib import Path
import random
import sys

import bpy
from mathutils import Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *


def trunk():
    levels=[(-8,0,0,22,19),(0,0,0,22,19),(18,2,1,19,16),(40,5,3,17,15),
            (62,9,4,16,14),(83,11,2,15,13),(103,7,0,13,11),(124,2,3,10,8),
            (146,-2,7,6,5),(163,0,10,2.5,2)]
    def section(y):
        for a,b in zip(levels,levels[1:]):
            if a[0]<=y<=b[0]:
                t=(y-a[0])/(b[0]-a[0]);return [a[k]+(b[k]-a[k])*t for k in range(1,5)]
        return list(levels[-1][1:])
    count=48
    def ring(y):
        x,z,rx,rz=section(y);twist=y*.016
        return [(x+rx*(1+.13*math.sin(7*a+twist)+.045*math.sin(13*a-twist))*math.cos(a),
                 y,z+rz*(1+.13*math.sin(7*a+twist)+.045*math.sin(13*a-twist))*math.sin(a))
                for a in (k*math.tau/count for k in range(count))]
    vertices=[];faces=[]
    ys=[-8]+list(range(-6,164,2))
    for y in ys:vertices.extend(ring(y))
    for j in range(len(ys)-1):
        for k in range(count):
            a=j*count+k;b=j*count+(k+1)%count;faces.append((a,b,b+count,a+count))
    faces.extend([tuple(reversed(range(count))),tuple(range((len(ys)-1)*count,len(ys)*count))])
    obj=mesh('01 | Twisted fluted living trunk',vertices,faces,'wood');recalculate(obj)
    obj.data.materials.append(bpy.data.materials['bark'])
    for poly in obj.data.polygons:
        p=poly.center;angle=math.atan2(-p.y,p.x)
        poly.material_index=int(math.sin(angle*7+p.z*.016)>.6)
    vertices=[];faces=[]
    for i in range(math.ceil(171/.68)+1):
        y=min(163,-8+i*.68);start=len(vertices);vertices.extend(ring(y));faces.append(tuple(range(start,start+count)))
    mesh('01 | Solid trunk cross-sections',vertices,faces,'wood')
    return levels


def foliage(name,center,radius,phase):
    # Tiered, lobed crown patches, with unequal outlines and a comparatively flat underside.
    x,y,z=center;rx,ry,rz=radius;count=48
    profile=[(-.75,.12),(-.63,.63),(-.35,.91),(0,1),(.42,.86),(.72,.61),(1,.10)]
    vertices=[]
    for j,(height,r) in enumerate(profile):
        for k in range(count):
            a=k*math.tau/count
            ripple=1+.085*math.sin(5*a+phase)+.055*math.sin(11*a-phase)+.025*math.sin(17*a)
            vertices.append((x+rx*r*ripple*math.cos(a),y+ry*height+1.3*math.sin(a*7+phase)*r,
                             z+rz*r*ripple*math.sin(a)))
    faces=[]
    for j in range(len(profile)-1):
        for k in range(count):
            a=j*count+k;b=j*count+(k+1)%count;faces.append((a,b,b+count,a+count))
    faces.extend([tuple(reversed(range(count))),tuple(range((len(profile)-1)*count,len(profile)*count))])
    obj=mesh(name,vertices,faces,'leaves');recalculate(obj)
    obj.data.materials.append(bpy.data.materials['leaf_light'])
    for poly in obj.data.polygons:
        p=poly.center
        poly.material_index=int(poly.normal.z>.2 and math.sin(p.x*.055-p.y*.04+phase)>.78)
    # A second nested skin makes leaf shelves several voxels thick but avoids a solid leaf boulder.
    inner=obj.copy();inner.data=obj.data.copy();inner.name=name+' | inner leaf layer';bpy.context.collection.objects.link(inner)
    for v in inner.data.vertices:
        c=Vector(xyz(center));v.co=c+(v.co-c)*.96
    # Overlapping peripheral leaf cushions break the clean umbrella outline.
    # Their centers stay within the parent shelf, so they are not detached islands.
    for k in range(11):
        a=k*math.tau/11+phase*.3
        edge=.77+.05*math.sin(k*2.3+phase)
        cx=x+rx*edge*math.cos(a);cz=z+rz*edge*math.sin(a)
        cy=y+ry*.10+math.sin(k*1.4+phase)*2.2
        size=7.5+2.5*math.sin(k*.9+phase)**2
        cushion=ellipsoid(name+' | broken leaf edge',(cx,cy,cz),(size,4.5,size*.85),'leaves',20,12)
        for vertex in cushion.data.vertices:
            v=vertex.co;v*=1+.06*math.sin(v.x*1.4+v.y*.8+phase)


def main():
    reset({'wood':'564430','bark':'756044','cut':'604a34','leaves':'30482d','leaf_light':'46603b',
           'moss':'566c3b','stone':'64705a'})
    rng=random.Random(402);levels=trunk()
    # Five primary limbs carry distinct foliage shelves, all starting inside the trunk.
    branches=[([(6,79,2),(-12,105,4),(-35,131,7),(-61,147,6)],[13,11,8,3.8]),
              ([(8,89,2),(26,103,-6),(48,130,-14),(64,140,-16)],[12,9,6,2.8]),
              ([(6,103,4),(-7,129,24),(-22,155,45),(-26,169,57)],[11,8,5,2.3]),
              ([(4,115,0),(24,139,14),(43,163,30),(56,175,35)],[10,8,5,2]),
              ([(9,79,0),(16,97,-22),(22,113,-43),(30,121,-59)],[10,8,5,2])]
    for i,(points,radii) in enumerate(branches):
        tapered(f'02 | Primary branch {i+1}',points,radii,'wood',18,True)
        start=Vector(points[-2]);end=Vector(points[-1])
        for j,side in enumerate((-1,1)):
            tip=end+Vector((side*(14+i),3+j*3,(j-.5)*18))
            tapered(f'03 | Supported secondary bough {i+1}.{j+1}',[start,end,tip],[radii[-2]*.7,radii[-1],1.1],'bark',12,True)
            ellipsoid(f'Branch-tip foliage {i+1}.{j+1}',tuple(tip),(10,6,9),'leaves',20,12)
    # Central high forks visibly carry the upper canopy rather than stopping below it.
    for i,end in enumerate([(-28,183,-5),(20,188,12),(1,181,-36)]):
        tapered(f'03 | Crown fork {i+1}',[(1,134,5),(end[0]*.5,159,end[2]*.6),end],[8,5,1.5],'wood',14,True)
    # Six uneven roots; two front arches keep broad walk-through spaces.
    roots=[([(3,30,2),(19,24,-15),(39,15,-33),(50,0,-43),(54,-7,-48)],[15,12,8,6,3]),
           ([(-4,25,0),(-22,23,-13),(-39,13,-29),(-48,0,-41),(-53,-7,-45)],[14,11,7,5,2]),
           ([(5,23,5),(28,15,16),(46,5,35),(51,-7,48)],[14,10,7,2.8]),
           ([(-8,22,7),(-26,17,24),(-42,4,42),(-47,-7,49)],[13,10,6,2]),
           ([(0,18,8),(0,12,31),(12,3,47),(18,-7,54)],[13,9,6,2.5]),
           ([(4,16,-5),(7,8,-27),(2,0,-42),(-4,-7,-50)],[11,7,5,2])]
    for i,(points,radii) in enumerate(roots):tapered(f'04 | Grounded root arch {i+1}',points,radii,'wood',18,True)
    # One old branch scar below the main crown, visibly rooted in the trunk.
    tapered('05 | Old broken branch',[(12,57,2),(29,64,6),(37,68,7)],[8,6,4.8],'wood',14,True)
    cylinder('Exposed healed branch end',(35.8,67,6.8),(37.4,68.3,7.1),4.5,'cut',14)
    for i,(center,radius) in enumerate([((-48,148,7),(44,15,42)),((51,140,-12),(42,14,38)),
                                       ((0,184,1),(61,24,47)),((-20,177,34),(61,21,50)),
                                       ((47,171,26),(40,17,38)),((-48,121,27),(36,12,32)),
                                       ((25,118,-41),(48,12,34)),((-7,160,-46),(53,16,39))]):
        foliage(f'06 | Layered crown mass {i+1}',center,radius,i*.79)
    # Lower shelf is explicitly borne by an offshoot rather than a floating leaf island.
    tapered('Secondary lower spreading limb',[(-3,60,9),(-21,89,16),(-46,114,29)],[9,6,2.7],'wood',14,True)
    for i,(x,z,h) in enumerate([(-42,-15,6),(28,-29,4.5),(-23,28,7)]):
        obj=box(f'07 | Worked stone caught in roots {i+1}',(x,h/2,z),(6,h,4),'stone',.7)
        obj.rotation_euler.z=rng.uniform(-.3,.3)
    for x,y,z,rx,rz in [(-15,6,-8,6,9),(20,6,9,7,8),(-24,12,20,4,7),(37,5,-31,6,4)]:
        ellipsoid('Sheltered root moss',(x,y,z),(rx,1.5,rz),'moss',20,12)
    deposits([(-35,-31,19,22,2.8,-20),(36,-32,20,23,3.1,20),(-32,33,23,23,3.1,0),
              (35,33,24,24,3,0),(0,8,23,28,2,0)],8,(-60,62,-62,64))
    save('relics/world-tree/design/world-tree-v1.json',{
        'name':'World Tree V1','reference':'https://www.instagram.com/reel/DaBgsX0C9s4/',
        'new_relic_v1':{'family':'tree','void_probes_source':[[-30,4,-20],[29,4,-20]],
            'solid_probes_source':[[0,20,0],[5,43,3],[9,65,4]],
            'features':['five primary crown limbs','eight unequal foliage masses','six grounded roots','one broken branch','three worked stones'],
            'trunk_source_levels':levels,'solid_wood_slice_spacing':.68,'persistent_leaves':True,
            'foliage_note':'Nested leaf shelves, not solid filled foliage boulders; major wood is densely sliced solid.',
            'v5_interiors':False}})


if __name__=='__main__':main()
