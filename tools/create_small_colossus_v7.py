"""Reference-led weathering and surface-hugging growth on the preserved V6 body."""
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *

SOURCE=ROOT/'relics/colossus/design/generated/small-colossus-v6/small-colossus-v6-source.blend'


def weather(objects):
    changed=0
    for obj in objects:
        if not any(m and m.name in ('armor','plate','rust','worn') for m in obj.data.materials):continue
        # Subdivide broad shield faces so stains follow smaller patches and runs,
        # rather than painting entire triangular faces of a large forged plate.
        bm=bmesh.new();bm.from_mesh(obj.data)
        edges=[e for e in bm.edges if e.calc_length()>4]
        if edges:bmesh.ops.subdivide_edges(bm,edges=edges,cuts=4,use_grid_fill=True)
        bm.to_mesh(obj.data);bm.free();obj.data.update()
        slots={}
        for key in ('rust','patina','worn','moss','growth'):
            slots[key]=len(obj.data.materials);obj.data.materials.append(bpy.data.materials[key])
        matrix=obj.matrix_world;normal_matrix=matrix.to_3x3().inverted().transposed()
        for face in obj.data.polygons:
            original=obj.data.materials[face.material_index].name
            if original not in ('armor','plate','rust','worn'):continue
            p=matrix@face.center;x,y,z=p.x,p.z,-p.y
            if y<1:continue
            up=(normal_matrix@face.normal).normalized().z
            field=math.sin(x*.19+z*.14)+.65*math.cos(y*.23-z*.17)+.3*math.sin(x*.8-y*.4)
            run=math.sin(x*.48+z*.21+.18*math.sin(y*.2))
            key=None
            if field>1.02:key='patina'
            elif field<-.65 or (run>.87 and up<.3):key='rust'
            elif field>.64:key='worn'
            # Moss favours sheltered ledges, the lower body and rear-facing plates.
            if (up>.3 or z>3 or y<18) and field>.65 and math.sin(x*.21-z*.27)>.15:
                key='moss' if up>.2 else 'growth'
            if key:face.material_index=slots[key];changed+=1
    return changed


def grow(objects):
    vertices=[];faces=[]
    for obj in objects:
        start=len(vertices);vertices.extend(obj.matrix_world@v.co for v in obj.data.vertices)
        faces.extend(tuple(start+i for i in f.vertices) for f in obj.data.polygons)
    surface=BVHTree.FromPolygons(vertices,faces)
    # These patches cling to actual upper surfaces; no free-floating green balls.
    patches=[(-29,-5,13,12),(35,-2,10,11),(-4,27,17,12),
             (12,-10,11,8),(-39,-32,10,10),(35,-22,7,8)]
    probes=[];cells=0
    for index,(cx,cz,rx,rz) in enumerate(patches):
        samples={}
        for x in range(math.floor(cx-rx-2),math.ceil(cx+rx+3)):
            for z in range(math.floor(cz-rz-2),math.ceil(cz+rz+3)):
                radial=((x-cx)/rx)**2+((z-cz)/rz)**2
                edge=1+.16*math.sin(x*.63+z*.4)+.13*math.cos(z*.9-x*.2)
                if radial>edge:continue
                p,n,_,_=surface.ray_cast(Vector((x,-z,90)),Vector((0,0,-1)),100)
                if p is None or p.z<2 or n.z<.32:continue
                # The very highest crown edge stays at the V6 height.
                if p.z>67:continue
                samples[x,z]=p
        verts=[];polys=[]
        for (x,z),p in samples.items():
            corners=[samples.get(k) for k in ((x,z),(x+1,z),(x+1,z+1),(x,z+1))]
            if any(q is None for q in corners):continue
            if max(q.z for q in corners)-min(q.z for q in corners)>2:continue
            height=.7+.25*math.sin(x*.7-z*.5)
            start=len(verts)
            verts.extend((q.x,q.z+dy,-q.y) for dy in (-.3,height) for q in corners)
            polys.extend(tuple(start+i for i in f) for f in ((3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)))
            cells+=1
        if polys:
            obj=mesh(f'Overgrowth {index} / close irregular moss mantle',verts,polys,'moss');recalculate(obj)
            probes.append(list(verts[len(verts)//16*8+4]))
    return cells,probes


def main():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    meta=json.loads(SOURCE.with_name('small-colossus-v6.design.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    material('patina','57715a');material('moss','4f6335');material('growth','485737')
    body=[o for o in bpy.context.scene.objects if o.type=='MESH' and
          not any(m and m.name.startswith('terrain_') for m in o.data.materials)]
    changed=weather(body);cells,probes=grow(body)
    meta.update(name='Small Colossus V7 / Weathered and overgrown',
                visual_acceptance='October 6 weathering revision; user review pending')
    meta['revision_v7']={'source':SOURCE.relative_to(ROOT).as_posix(),'source_sha256':digest,
        'reference_observation':'Debris and irregular growth on the dormant specimen, especially the foreground hand',
        'authored_completion':'Extent of moss and weathering across the unseen back',
        'weathered_faces':changed,'surface_growth_cells':cells,'growth_probes_source':probes,
        'buried_body_preserved':True,'body_shape_preserved':True}
    save('relics/colossus/design/small-colossus-v7.json',meta)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest


if __name__=='__main__':main()
