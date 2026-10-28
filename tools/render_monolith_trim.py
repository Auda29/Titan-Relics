"""Blender preview of exported Minecraft 26.2 armor polygons, UVs and palettes.

Read-only native textures and composited review textures live under build/.
Run with Blender --background --python tools/render_monolith_trim.py.
This is an inspection rendering, not a Minecraft client screenshot.
"""
import json
from pathlib import Path
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/'build/monolith-trim-20261028'
OUT=ROOT/'docs/project/reviews/monolith-trim-20261028'
OUT.mkdir(parents=True,exist_ok=True)
evidence=json.loads((CACHE/'native-armor-uv.json').read_text())
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.samples=24
scene.render.resolution_x=560;scene.render.resolution_y=680;scene.render.resolution_percentage=100
scene.world.color=(.24,.24,.24)
scene.view_settings.view_transform='Standard'
scene.render.image_settings.file_format='PNG'
def point(v):return (v[0]/16,v[2]/16,(24-v[1])/16)
objects=[]
for slot in ('head','chest','legs','feet'):
    vertices=[];faces=[];uvs=[]
    for face in evidence['faces']:
        if face['slot']!=slot:continue
        vs=face['vertices'];points=[point(v) for v in vs]
        n=Vector((face['normal'][0],face['normal'][2],-face['normal'][1]))
        if (Vector(points[1])-Vector(points[0])).cross(Vector(points[2])-Vector(points[0])).dot(n)<0:
            points.reverse();vs=list(reversed(vs))
        start=len(vertices);vertices.extend(points);faces.append(tuple(range(start,start+4)))
        uvs.extend([(v[3],1-v[4]) for v in vs])
    mesh=bpy.data.meshes.new(slot);mesh.from_pydata(vertices,[],faces);mesh.update()
    uv=mesh.uv_layers.new()
    for index,coord in enumerate(uvs):uv.data[index].uv=coord
    obj=bpy.data.objects.new(slot,mesh);scene.collection.objects.link(obj);objects.append(obj)
# Neutral mannequin fills openings only; all armor surfaces above are native.
mat=bpy.data.materials.new('Neutral mannequin');mat.diffuse_color=(.27,.28,.3,1)
for center,size in [((0,-4,0),(8,8,8)),((0,6,0),(8,12,4)),((-6,6,0),(4,12,4)),((6,6,0),(4,12,4)),((-2,18,0),(4,12,4)),((2,18,0),(4,12,4))]:
    bpy.ops.mesh.primitive_cube_add(size=1,location=point(center));o=bpy.context.object
    o.dimensions=(size[0]/16,size[2]/16,size[1]/16);o.data.materials.append(mat)
for location,power,size in [((2,-3,4),160,3),((-3,-2,2),100,3),((1,3,3),180,3)]:
    data=bpy.data.lights.new('Inspection light','AREA');data.energy=power;data.size=size
    obj=bpy.data.objects.new('Inspection light',data);scene.collection.objects.link(obj);obj.location=location
    obj.rotation_euler=(Vector((0,0,.9))-obj.location).to_track_quat('-Z','Y').to_euler()
camera=bpy.data.objects.new('Native model camera',bpy.data.cameras.new('Native model camera'));scene.collection.objects.link(camera);scene.camera=camera
camera.data.type='ORTHO';camera.data.ortho_scale=2.35
def texture_material(path):
    material=bpy.data.materials.new(path.stem);material.use_nodes=True
    nodes=material.node_tree.nodes;nodes.clear();output=nodes.new('ShaderNodeOutputMaterial')
    mix=nodes.new('ShaderNodeMixShader');transparent=nodes.new('ShaderNodeBsdfTransparent');diffuse=nodes.new('ShaderNodeBsdfDiffuse')
    texture=nodes.new('ShaderNodeTexImage');texture.image=bpy.data.images.load(str(path),check_existing=True);texture.interpolation='Closest'
    links=material.node_tree.links;links.new(texture.outputs['Color'],diffuse.inputs['Color']);links.new(texture.outputs['Alpha'],mix.inputs[0])
    links.new(transparent.outputs[0],mix.inputs[1]);links.new(diffuse.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],output.inputs['Surface'])
    return material
for variant,material_name in [('before','emerald'),('after','emerald'),('after','amethyst'),('after','copper')]:
    for obj in objects:
        kind='humanoid_leggings' if obj.name=='legs' else 'humanoid'
        obj.data.materials.clear();obj.data.materials.append(texture_material(CACHE/f'{variant}-{material_name}-{kind}.png'))
    for view in ('front','back') if material_name=='emerald' else ('front',):
        camera.location=(2,-6,2.7) if view=='front' else (-2,6,2.7)
        camera.rotation_euler=(Vector((0,0,.95))-camera.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(OUT/f'{variant}-{material_name}-{view}.png');bpy.ops.render.render(write_still=True)
