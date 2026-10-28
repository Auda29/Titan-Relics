"""Create editable V11 source and labelled inspection crops from exported NBT."""
import hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_gameplay_interiors as r
import render_gameplay_interiors_revision  # Blender 5.2 compatible lighting and glass
from build_small_colossus_short_entry import OUT,STEM,OLD,V10,write

side=json.loads((OUT/(STEM+'.gameplay.json')).read_text())
_,blocks=r.read_structure(OUT/(STEM+'.nbt'))
groups={tuple(p):k for k,v in json.loads((OUT/(STEM+'.groups.json')).read_text()).items() for p in v}
if '--verify' in sys.argv:
    path=OUT/(STEM+'-source.blend');bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene
    assert scene['source_nbt_sha256']==side['source_sha256']
    meshes=[o for o in scene.objects if o.type=='MESH' and 'block_state' in o]
    assert meshes and all(len(o.data.polygons)>0 and len(o.data.materials)>0 for o in meshes)
    assert {'shortened-lower-entry'} <= {o['authoring_group'] for o in meshes}
    # Every face in the three edited mesh groups must border an NBT voxel of
    # the same block state and group; no render-only architectural geometry.
    import math
    checked_faces=0
    for o in meshes:
        group=o['authoring_group']
        # Verify every exported surface, including preserved upper geometry.
        for poly in o.data.polygons:
            c=poly.center;n=poly.normal
            candidates=[]
            for sign in (-1,1):
                q=c+sign*.001*n
                candidates.append((math.floor(q.x),math.floor(q.z),math.floor(-q.y)))
            assert any(blocks.get(p)==o['block_state'] and groups.get(p,'Preserved baseline')==group for p in candidates), (group,tuple(c),candidates)
            checked_faces+=1
    assert checked_faces>0
    def signatures(objects):
        return {(o['authoring_group'],o['block_state']): (
            [tuple(round(v,5) for v in vertex.co) for vertex in o.data.vertices],
            [tuple(face.vertices) for face in o.data.polygons]) for o in objects}
    saved=signatures(meshes)
    # Reconstruct all visible faces from NBT in memory, without resaving source.
    rebuilt=r.geometry(blocks,groups)
    assert saved==signatures(rebuilt),'Saved mesh surface differs from NBT reconstruction'
    for o in rebuilt:bpy.data.objects.remove(o,do_unlink=True)
    objs={o.name:o for o in scene.objects if 'gameplay_marker' in o};assert set(objs)=={m['id'] for m in side['markers']}
    for m in side['markers']:
        o=objs[m['id']];x,y,z=m['pos'];assert json.loads(o['gameplay_marker'])==m
        assert all(abs(a-b)<1e-5 for a,b in zip(o.location,(x+.5,-z-.5,y+.5)))
    result={'source_blend_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bound_nbt_sha256':side['source_sha256'],
            'mesh_count':len(meshes),'marker_empties':len(objs),'markers_verified':True,'edited_group_faces_matched_to_export':checked_faces,'fresh_process':True,'all_meshes_equal_fresh_nbt_reconstruction':True}
    write(OUT/'source-verification.json',result)
    print(result);sys.exit(0)

r.clear();objects=r.geometry(blocks,groups)
for m in side['markers']:
    o=bpy.data.objects.new(m['id'],None);bpy.context.scene.collection.objects.link(o)
    x,y,z=m['pos'];o.location=(x+.5,-z-.5,y+.5);o.empty_display_type='SPHERE';o.empty_display_size=.65;o['gameplay_marker']=json.dumps(m)
scene=bpy.context.scene;scene['source_nbt_sha256']=side['source_sha256'];scene['coordinates']='Minecraft X,Y,Z to Blender X,-Z,Y'
scene['pipeline']='NBT surface meshes; export from tools/build_small_colossus_short_entry.py'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(STEM+'-source.blend')),compress=True)
r.stage(objects,OUT/'01-overview.png',(180,280,140),side['ground_y'])

# Full geometry in all views. Fixed camera and scale for both revisions.
def detail(voxels,filename):
    r.clear();r.geometry(voxels,groups)
    scene=bpy.context.scene
    scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
    scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='Standard'
    world=bpy.data.worlds.new('Inspection daylight');world.use_nodes=True;scene.world=world
    bg=next(n for n in world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs['Color'].default_value=(.74,.79,.85,1);bg.inputs['Strength'].default_value=.8
    light=bpy.data.lights.new('Inspection sun','SUN');light.energy=1.7
    lamp=bpy.data.objects.new('Inspection sun',light);scene.collection.objects.link(lamp);lamp.rotation_euler=(.3,-.6,-.2)
    camera=bpy.data.objects.new('Matched entrance camera',bpy.data.cameras.new('Matched entrance camera'));scene.collection.objects.link(camera)
    center=Vector((62,-49,18));camera.location=center+Vector((85,180,85)).normalized()*700;r.renderer.point_at(camera,center)
    camera.data.type='ORTHO';camera.data.ortho_scale=37;camera.data.clip_end=3000;scene.camera=camera
    bpy.ops.mesh.primitive_plane_add(size=2000,location=(62,-49,12.9));bpy.context.object.data.materials.append(r.renderer.material('Presentation ground',(.44,.43,.38)))
    scene.render.filepath=str(OUT/filename);bpy.ops.render.render(write_still=True)
detail(blocks,'02-entry-v11.png')
_,old=r.read_structure(OLD/(V10+'.nbt'))
detail(old,'03-entry-v10.png')
print('Saved V11 source and matched full-geometry entrance views')
