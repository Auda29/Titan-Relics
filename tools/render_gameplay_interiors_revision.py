"""Render revised NBTs and reopen the resulting editable sources in Blender."""
import hashlib
import json
import sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_gameplay_interiors as r
from build_gameplay_interiors_revision import STEMS

r.STEMS=STEMS
original_mat=r.mat
original_partial=r.partial
def mat(state):
    material,name=original_mat(state)
    if state=='minecraft:black_stained_glass' and not material.get('revision_glass'):
        nodes=material.node_tree.nodes;links=material.node_tree.links
        bsdf=nodes['Principled BSDF'];out=next(n for n in nodes if n.type=='OUTPUT_MATERIAL')
        transparent=nodes.new('ShaderNodeBsdfTransparent')
        mix=nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=.45
        links.new(transparent.outputs[0],mix.inputs[1]);links.new(bsdf.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],out.inputs['Surface'])
        material['revision_glass']=True
    return material,name
r.mat=mat
r.partial=lambda state: 'stained_glass' in state or original_partial(state)

def stage(objects,out,direction,ground=None,markers=()):
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
    scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='Standard'
    world=bpy.data.worlds.new('Architectural daylight');world.use_nodes=True;scene.world=world
    bg=next(n for n in world.node_tree.nodes if n.type=='BACKGROUND')
    bg.inputs['Color'].default_value=(.74,.79,.85,1);bg.inputs['Strength'].default_value=.8
    bpy.context.view_layer.update();corners=[o.matrix_world@Vector(v) for o in objects for v in o.bound_box]
    lo=Vector(tuple(min(p[i] for p in corners) for i in range(3)));hi=Vector(tuple(max(p[i] for p in corners) for i in range(3)));center=(lo+hi)/2
    light=bpy.data.lights.new('Soft daylight','SUN');light.energy=1.7;light.angle=.3
    lamp=bpy.data.objects.new(light.name,light);scene.collection.objects.link(lamp);lamp.rotation_euler=(.3,-.6,-.2)
    camera=bpy.data.objects.new('Review camera',bpy.data.cameras.new('Review camera'));scene.collection.objects.link(camera)
    camera.data.type='ORTHO';camera.data.clip_end=3000;scene.camera=camera
    camera.location=center+Vector(direction).normalized()*700;r.renderer.point_at(camera,center)
    rotation=camera.rotation_euler.to_matrix().transposed();points=[rotation@(p-center) for p in corners]
    camera.data.ortho_scale=max(max(p.x for p in points)-min(p.x for p in points),(max(p.y for p in points)-min(p.y for p in points))*4/3)*1.16
    if ground is not None:
        bpy.ops.mesh.primitive_plane_add(size=2000,location=(center.x,center.y,ground-.1));bpy.context.object.data.materials.append(r.renderer.material('Presentation ground',(.44,.43,.38)))
    for m in markers:
        if m['role'].endswith('_spawn'):
            x,y,z=m['pos'];h=2.7 if m['role']=='colossus_golem_spawn' else 2.9
            bpy.ops.mesh.primitive_cube_add(size=1,location=(x+.5,-z-.5,y+h/2));o=bpy.context.object
            o.scale=(1.4,1.4,h) if h==2.7 else (.6,.6,h);o.modifiers.new('Reserved entity envelope','WIREFRAME').thickness=.035
            o.data.materials.append(r.renderer.material('Entity clearance',(.15,.65,.85)))
    scene.render.filepath=str(out);bpy.ops.render.render(write_still=True)
r.stage=stage

def visor_views():
    name='colossus';stem=STEMS[name];folder=(r.ROOT/r.ASSETS[name]['source']).parent.parent/stem
    _,blocks=r.read_structure(folder/(stem+'.nbt'))
    group_data=json.loads((folder/(stem+'.groups.json')).read_text());groups={tuple(p):k for k,v in group_data.items() for p in v}
    r.clear()
    objects=r.geometry(blocks,groups,lambda p: 64<=p[0]<=124 and 165<=p[1]<=199 and 130<=p[2]<=212)
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
    scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='Standard'
    world=bpy.data.worlds.new('Visor daylight');world.use_nodes=True
    bg=next(n for n in world.node_tree.nodes if n.type=='BACKGROUND')
    bg.inputs['Color'].default_value=(.74,.79,.85,1)
    bg.inputs['Strength'].default_value=1.2;scene.world=world
    light=bpy.data.lights.new('Sun','SUN');light.energy=2;ob=bpy.data.objects.new('Sun',light);scene.collection.objects.link(ob);ob.rotation_euler=(.3,-.6,-.2)
    light=bpy.data.lights.new('Inspection fill, not in-game lighting','POINT');light.energy=2500;light.shadow_soft_size=8
    ob=bpy.data.objects.new(light.name,light);scene.collection.objects.link(ob);ob.location=(94,-179,181)
    camera=bpy.data.objects.new('Visor camera',bpy.data.cameras.new('Visor camera'));scene.collection.objects.link(camera);scene.camera=camera
    camera.data.type='PERSP';camera.data.lens=24;camera.data.clip_start=.05;camera.data.clip_end=500
    for filename,pos,target in [('visor-inside.png',(94,-177,172),(94,-150,173)),('visor-outside.png',(94,-137,174),(94,-160,173))]:
        camera.location=Vector(pos);r.renderer.point_at(camera,Vector(target));scene.render.filepath=str(folder/filename);bpy.ops.render.render(write_still=True)

def verify_sources():
    for name,stem in STEMS.items():
        folder=(r.ROOT/r.ASSETS[name]['source']).parent.parent/stem;path=folder/(stem+'-source.blend')
        side=json.loads((folder/(stem+'.gameplay.json')).read_text())
        bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene
        scene['pipeline']='Exact NBT derivative; editable state/group surface meshes. Rebuild/export using tools/build_gameplay_interiors_revision.py.'
        bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True)
        bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene
        assert scene['source_nbt_sha256']==side['source_sha256']
        meshes=[o for o in scene.objects if o.type=='MESH' and 'block_state' in o]
        assert meshes and all(len(o.data.polygons)>0 and len(o.data.materials)>0 for o in meshes)
        objects={o.name:o for o in scene.objects if 'gameplay_marker' in o}
        assert set(objects)=={m['id'] for m in side['markers']}
        for m in side['markers']:
            obj=objects[m['id']];x,y,z=m['pos']
            assert obj.type=='EMPTY' and json.loads(obj['gameplay_marker'])==m
            assert all(abs(a-b)<1e-5 for a,b in zip(obj.location,(x+.5,-z-.5,y+.5)))
        record={'source_blend_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'bound_nbt_sha256':side['source_sha256'],'mesh_count':len(meshes),
                'marker_empties':len(objects),'marker_contents_and_positions_verified':True,
                'opened_and_verified_in_blender':True}
        (folder/'source-verification.json').write_text(json.dumps(record,indent=2)+'\n')

if __name__=='__main__':
    name=sys.argv[sys.argv.index('--')+1]
    if name=='verify':verify_sources()
    else:
        r.main()
        if name=='colossus':visor_views()
