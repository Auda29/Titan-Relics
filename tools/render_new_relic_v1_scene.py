"""Reference-oriented context for the new V1 assets; actual relic geometry is NBT."""
import json
import math

import bpy
from mathutils import Vector


def render_scene(renderer):
    meta=json.loads((renderer.OUT/f'{renderer.STEM}.design.json').read_text())
    family=meta['new_relic_v1']['family'];preview=renderer.CONFIG['preview']
    low,high=meta['source_bounds_blender'];scale=meta['blocks_per_source_unit'];ground=meta['ground_level_nbt_approx']
    def world(p):
        x,y,z=p
        return ((x-(low[0]+high[0])/2)*scale,(-z-(low[1]+high[1])/2)*scale,(y-low[2])*scale)
    scene=bpy.context.scene
    for obj in scene.objects:
        if 'not exported' in obj.name:obj.hide_render=True
        if obj.type=='LIGHT' and obj.data.type=='AREA':obj.data.energy=25000
    # A shallow irregular surface meets the authored local deposits, without fake block exports.
    vertices=[];faces=[];steps=101;spacing=8
    for j in range(steps):
        z=(j-steps//2)*spacing
        for i in range(steps):
            x=(i-steps//2)*spacing
            distance=math.hypot(x,z)
            height=(math.sin(x*.014+z*.009)*2+math.cos(z*.017)*2)*min(1,max(0,(distance-65)/65))-.45
            vertices.append(world((x,height,z)))
            if i and j:
                a=j*steps+i;faces.append((a-steps-1,a-1,a,a-steps))
    data=bpy.data.meshes.new('Illustrative surrounding terrain');data.from_pydata(vertices,[],faces);data.update()
    obj=bpy.data.objects.new('Surrounding terrain / not exported',data);scene.collection.objects.link(obj)
    for poly in data.polygons:poly.use_smooth=True
    mat=renderer.material('Surrounding terrain',preview['ground_color']);data.materials.append(mat)
    nodes,links=mat.node_tree.nodes,mat.node_tree.links
    noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.13
    coord=nodes.new('ShaderNodeTexCoord');links.new(coord.outputs['Object'],noise.inputs['Vector'])
    ramp=nodes.new('ShaderNodeValToRGB');color=preview['ground_color']
    ramp.color_ramp.elements[0].color=(*[c*.8 for c in color],1)
    ramp.color_ramp.elements[1].color=(*[min(1,c*1.14) for c in color],1)
    links.new(noise.outputs['Fac'],ramp.inputs[0]);links.new(ramp.outputs[0],nodes['Principled BSDF'].inputs['Base Color'])
    sun=bpy.data.lights.new('Soft site daylight','SUN');sun.energy=1.5;sun.angle=.22
    lamp=bpy.data.objects.new(sun.name,sun);scene.collection.objects.link(lamp);lamp.rotation_euler=(.48,-.52,-.4)
    # Human scale figure is explicitly staging, never part of the structure template.
    figure=renderer.material('Two-block visitor',(.62,.28,.09))
    px,pz=(36,-49) if family=='tower' else (-32,-59) if family=='skull-2' else (29,-57) if family=='tree' else (20,-30)
    for p,size in [((px,1,pz),(.65,1.2,.4)),((px,1.8,pz),(.42,.4,.42)),
                   ((px-.18,.3,pz),(.22,.6,.3)),((px+.18,.3,pz),(.22,.6,.3))]:
        bpy.ops.mesh.primitive_cube_add(size=1,location=world(p));person=bpy.context.object
        person.name='Two-block visitor / not exported';person.scale=(size[0],size[2],size[1]);person.data.materials.append(figure)
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.64,.72,.8,1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65
    scene.camera.data.type='PERSP';scene.camera.data.lens=preview.get('lens',44)
    scene.camera.location=world(preview['camera_source']);renderer.point_at(scene.camera,world(preview['target_source']))
    scene.render.resolution_x,scene.render.resolution_y=1400,1700
    scene.cycles.samples=32
    scene.render.filepath=str(renderer.OUT/'05-blocks-landscape.png');bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(renderer.OUT/f'{renderer.STEM}-landscape.blend'))
