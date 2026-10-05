"""Shared modeling/export helpers for the four independent new V1 designs."""
import hashlib
import json
import math
from pathlib import Path

import bpy
from mathutils import Vector

from create_blender_colossus import xyz,box,cylinder,subtract,finish,apply
from create_colossus_v3 import ellipsoid,catmull,jagged_cutter
from create_titan_skull_v1 import tube,organic,unite
from create_colossus_v4 import bounds

ROOT=Path(__file__).resolve().parents[1]


def reset(colors):
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    for mat in list(bpy.data.materials):
        if mat.users==0: bpy.data.materials.remove(mat)
    for name,color in colors.items():
        material(name,color)


def material(name,color):
    mat=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color=(*(int(color[i:i+2],16)/255 for i in (0,2,4)),1)
    return mat


def mesh(name,vertices,faces,mat):
    data=bpy.data.meshes.new(name);data.from_pydata([xyz(v) for v in vertices],[],faces);data.update()
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj)
    return finish(obj,name,mat)


def tapered(name,points,radii,mat,sides=14,solid=False):
    obj=tube(name,points,radii,mat,sides)
    if solid:
        vertices=[];faces=[]
        for a,b,ra,rb in zip(points,points[1:],radii,radii[1:]):
            a,b=Vector(a),Vector(b);axis=(b-a).normalized()
            u=axis.cross(Vector((0,1,0)))
            if u.length<.1:u=axis.cross(Vector((1,0,0)))
            u.normalize();v=axis.cross(u)
            steps=max(1,math.ceil((b-a).length/.68))
            for j in range(steps+1):
                t=j/steps;center=a.lerp(b,t);radius=ra+(rb-ra)*t
                start=len(vertices)
                vertices.extend(tuple(center+radius*(math.cos(k*math.tau/sides)*u+math.sin(k*math.tau/sides)*v)) for k in range(sides))
                faces.append(tuple(range(start,start+sides)))
        mesh(name+' | solid interior slices',vertices,faces,mat)
    return obj


def recalculate(obj):
    import bmesh
    bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
    bm.to_mesh(obj.data);bm.free();obj.data.update()


def damage(obj,center,radii,depth):
    cutter=jagged_cutter('Authored missing material',center,radii,depth)
    recalculate(cutter);subtract(obj,cutter)


def deposits(lobes,depth,extent,colors=None):
    from relic_v4_terrain import lobe,build_deposits
    colors=colors or ('596b3c','6a563d','674c37')
    for name,color in zip(('terrain_top','terrain_patch','terrain_fill'),colors):material(name,color)
    def height(x,z):
        return max((lobe(x,z,*p) for p in lobes),default=0)
    xmin,xmax,zmin,zmax=extent
    build_deposits(height,list(range(xmin,xmax+1,2)),list(range(zmin,zmax+1,2)),depth=depth)


def save(config_path,metadata):
    config_path=ROOT/config_path;config=json.loads(config_path.read_text())
    output=ROOT/config['output'];out=output.parent;stem=output.stem;out.mkdir(parents=True,exist_ok=True)
    bpy.context.view_layer.update()
    objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
    low,high=bounds(objects);scale=(config['height']-1)/(high[2]-low[2])
    metadata.update(source_bounds_blender=[low,high],blocks_per_source_unit=scale,
                    height_target_blocks=config['height'],ground_level_source=0,
                    ground_level_nbt_approx=round(-low[2]*scale),mesh_count=len(objects),
                    air_policy='omit; cavities are geometry, not terrain-clearing worldgen',
                    in_game_tested=False,visual_acceptance=metadata.get('visual_acceptance','V1 review pending'),
                    config=str(config_path.relative_to(ROOT)).replace('\\','/'),
                    planned_site_size=config['planned_site_size'])
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.wm.obj_export(filepath=str(ROOT/config['input']),forward_axis='NEGATIVE_Z',up_axis='Y',
                          export_selected_objects=True,export_triangulated_mesh=True,export_materials=True)
    bpy.context.scene['design_name']=metadata['name']
    bpy.context.scene['reference_url']=config.get('reference','')
    bpy.context.scene.unit_settings.system='METRIC'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/f'{stem}-source.blend'))
    metadata['source_blend_sha256']=hashlib.sha256((out/f'{stem}-source.blend').read_bytes()).hexdigest()
    (out/f'{stem}.design.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'name':metadata['name'],'meshes':len(objects),'bounds':[low,high],'scale':scale,'ground':metadata['ground_level_nbt_approx']},indent=2))
