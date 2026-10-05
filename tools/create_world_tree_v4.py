"""Spreading, repeatedly forked tree; foliage grows across fans, not along sausages."""
import hashlib
import math
from pathlib import Path
import random
import sys

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
import create_world_tree_v2 as base
from new_relic_v1_common import *

RNG=random.Random(461005)
SOURCE=ROOT/'relics/world-tree/design/generated/world-tree-v3/world-tree-v3-source.blend'


def direction(angle):
    return Vector((math.cos(angle),0,math.sin(angle)))


def branch(name,points,radii):
    base.curved(name,points,radii,sides=10)
    return [Vector(p) for p in catmull(points,4)]


def crown():
    tips=[];forks=[];sprays=0;secondary=0
    # Broad bent limbs turn outward. Their descendants divide in different
    # directions instead of repeating the primary's rising cylindrical silhouette.
    scaffold=[(72,205,53,32,8.8),(82,12,59,36,8.1),(94,115,53,32,7.5),
              (105,282,57,34,6.9),(117,48,45,31,6.0),(130,188,42,28,5.0),
              (141,91,30,28,4.0),(150,314,29,28,3.4),(121,247,42,26,5.2)]
    for i,(y,degrees,length,rise,width) in enumerate(scaffold):
        angle=math.radians(degrees);d=direction(angle);side=direction(angle+math.pi/2)
        origin=Vector((7 if y<110 else 2 if y<130 else -4,y,4))
        path=branch(f'02 | Outward bending primary {i}',[
            origin,origin+d*(length*.26)+Vector((0,rise*.68,0)),
            origin+d*(length*.64)+side*RNG.uniform(-5,5)+Vector((0,rise,0)),
            origin+d*length+side*RNG.uniform(-7,7)+Vector((0,rise*.88,0))],
            [width,width*.65,width*.38,2.0])
        for j,index in enumerate((5,7,9,11,12)):
            start=path[index];forks.append(list(start));secondary+=1
            a=angle+math.radians((-1 if j%2 else 1)*RNG.uniform(27,70))
            lateral=direction(a);length2=RNG.uniform(19,29)*(1 if y<125 else .85)
            end=start+lateral*length2+Vector((0,RNG.uniform(-4,29),0))
            middle=start.lerp(end,.50)+Vector((0,RNG.uniform(3,7),0))
            second=branch(f'03 | Spreading fork {i}.{j}',[start,middle,end],[2.9,1.9,1.25])
            for k in range(3):
                root=second[(3,5,8)[k]]
                a3=a+math.radians((k-1)*RNG.uniform(36,58)+RNG.uniform(-12,12))
                d3=direction(a3);tip=root+d3*RNG.uniform(12,21)+Vector((0,RNG.uniform(-7,17),0))
                third=branch(f'04 | Visible tapering twig {i}.{j}.{k}',
                             [root,root.lerp(tip,.52)+Vector((0,3,0)),tip],[1.45,1.15,.95])
                # Each terminal is a fan with separate lateral leaf-bearing ends.
                # The proximal half stays exposed; no sleeve of overlapping leaves.
                for n,idx in enumerate((4,6,8)):
                    root4=third[idx]
                    a4=a3+math.radians((-1 if n%2 else 1)*RNG.uniform(40,82))
                    tip4=root4+direction(a4)*RNG.uniform(5,10)+Vector((0,RNG.uniform(-5,8),0))
                    branch(f'05 | Leaf-bearing twig {len(tips)}',[root4,root4.lerp(tip4,.55),tip4],[1.05,.95,.85])
                    tips.append(list(tip4))
                    radius=RNG.uniform(3.6,5.5)
                    base.leaves(f'06 | Offset foliage fan {sprays}',tip4+Vector((0,1.2,0)),
                                (radius,RNG.uniform(2.1,3.5),radius*RNG.uniform(.8,1.25)))
                    sprays+=1
                    # Smaller pendant spray gives ragged lower edges, not a
                    # repeated ellipsoid wrapped around the full twig length.
                    offset=direction(a4+1.1)*2.8+Vector((0,-1.1,0))
                    base.leaves(f'06 | Pendant foliage fringe {sprays}',tip4+offset,
                                (radius*.62,2.3,radius*.70));sprays+=1
    return tips,forks,secondary,sprays


def main():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    RNG.seed(461005);base.RNG.seed(461005)
    reset({'wood':'574531','bark':'756044','cut':'604a34','leaves':'30482d',
           'leaf_light':'46603b','moss':'566c3b','stone':'64705a'})
    levels=base.trunk();tips,forks,secondary,sprays=crown();base.roots()
    for obj in list(bpy.context.scene.objects):
        if obj.type=='MESH' and any(m and m.name.startswith('terrain_') for m in obj.data.materials):
            bpy.data.objects.remove(obj,do_unlink=True)
    # Narrow low deposits follow the buttresses, leaving native ground between
    # roots instead of several conspicuous round grass hummocks.
    deposits([(-26,-13,31,9,1.0,28),(27,-20,34,8,1.1,-36),
              (-18,29,28,8,.9,-56),(15,32,29,10,.85,62),(0,0,20,18,1.2,0)],
             8,(-70,72,-68,70))
    bpy.context.view_layer.update()
    objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
    low,high=bounds(objects)
    # Horizontal spread is explicit and capped for future padded integration.
    horizontal=min(1,222/max(high[0]-low[0],high[1]-low[1]));vertical=207/high[2]
    def fit(p):return [p[0]*horizontal,p[1]*vertical if p[1]>0 else p[1],p[2]*horizontal]
    for obj in objects:
        matrix=obj.matrix_world.copy()
        for vertex in obj.data.vertices:
            p=matrix@vertex.co;vertex.co=xyz(fit((p.x,p.z,-p.y)))
        obj.matrix_world=Matrix.Identity(4);obj.data.update()
    save('relics/world-tree/design/world-tree-v4.json',{
        'name':'World Tree V4 / Spreading ramified crown','visual_acceptance':'Alpha 4.2 screenshot follow-up; review pending',
        'revision_v2':{'primary_boughs':9,'secondary_boughs':secondary,'terminal_boughs':len(tips),
                       'leaf_clusters':sprays,'vertical_factor':vertical,'foliage_parent_shelves':0},
        'revision_v4':{'source':str(SOURCE.relative_to(ROOT)).replace('\\','/'),'source_sha256':digest,
                       'feedback':'Alpha 4.2: cactus-like upright leaf sleeves; round root hummocks',
                       'horizontal_factor':horizontal,'branch_orders':4,'proximal_twigs_uncovered':True,
                       'fork_probes_source':[fit(p) for p in forks]},
        'new_relic_v1':{'family':'tree','void_probes_source':[],
                       'solid_probes_source':[fit(p) for p in [(0,20,0),(4,43,2),(7,65,3)]],
                       'branch_tip_probes_source':[fit(p) for p in tips],
                       'trunk_source_levels_before_height_fit':levels,'persistent_leaves':True,'v5_interiors':False}})
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest


if __name__=='__main__':main()
