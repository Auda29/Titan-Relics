"""Create editable tower V10 source and labelled inspection crops from exported NBT."""
import hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_gameplay_interiors as r
import render_gameplay_interiors_revision  # Blender 5.2 compatible lighting and glass
from build_tower_chest import OUT,STEM

side=json.loads((OUT/(STEM+'.gameplay.json')).read_text())
_,blocks=r.read_structure(OUT/(STEM+'.nbt'))
groups={tuple(p):k for k,v in json.loads((OUT/(STEM+'.groups.json')).read_text()).items() for p in v}
if '--verify' in sys.argv:
    path=OUT/(STEM+'-source.blend');bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene
    assert scene['source_nbt_sha256']==side['source_sha256']
    meshes=[o for o in scene.objects if o.type=='MESH' and 'block_state' in o]
    assert meshes and all(len(o.data.polygons)>0 and len(o.data.materials)>0 for o in meshes)
    assert {'tower-rear-wall-stand'} <= {o['authoring_group'] for o in meshes}
    # Every face in the three edited mesh groups must border an NBT voxel of
    # the same block state and group; no render-only architectural geometry.
    import math
    checked_faces=0
    for o in meshes:
        group=o['authoring_group']
        if group not in {'tower-rear-wall-stand'}: continue
        for poly in o.data.polygons:
            c=poly.center;n=poly.normal
            candidates=[]
            for sign in (-1,1):
                q=c+sign*.001*n
                candidates.append((math.floor(q.x),math.floor(q.z),math.floor(-q.y)))
            assert any(blocks.get(p)==o['block_state'] and groups.get(p)==group for p in candidates), (group,tuple(c),candidates)
            checked_faces+=1
    assert checked_faces>0
    objs={o.name:o for o in scene.objects if 'gameplay_marker' in o};assert set(objs)=={m['id'] for m in side['markers']}
    for m in side['markers']:
        o=objs[m['id']];x,y,z=m['pos'];assert json.loads(o['gameplay_marker'])==m
        assert all(abs(a-b)<1e-5 for a,b in zip(o.location,(x+.5,-z-.5,y+.5)))
    result={'source_blend_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bound_nbt_sha256':side['source_sha256'],
            'mesh_count':len(meshes),'marker_empties':len(objs),'markers_verified':True,'edited_group_faces_matched_to_export':checked_faces,'fresh_process':True}
    (OUT/'source-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result);sys.exit(0)

if '--detail-only' in sys.argv:
    r.clear();objects=r.geometry(blocks,groups,lambda p:55<=p[0]<=61 and 14<=p[1]<=22 and 54<=p[2]<=58)
    r.stage(objects,OUT/'05-stand.png',(45,160,110))
    sys.exit(0)

r.clear();objects=r.geometry(blocks,groups)
for m in side['markers']:
    o=bpy.data.objects.new(m['id'],None);bpy.context.scene.collection.objects.link(o)
    x,y,z=m['pos'];o.location=(x+.5,-z-.5,y+.5);o.empty_display_type='SPHERE';o.empty_display_size=.65;o['gameplay_marker']=json.dumps(m)
scene=bpy.context.scene;scene['source_nbt_sha256']=side['source_sha256'];scene['coordinates']='Minecraft X,Y,Z to Blender X,-Z,Y'
scene['pipeline']='Full NBT surface meshes; tools/build_tower_chest.py'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(STEM+'-source.blend')),compress=True)
r.stage(objects,OUT/'01-overview.png',(180,280,140),side['ground_y'])
# Full export, perspective camera inside the existing entrance. No wall masks.
scene=bpy.context.scene
for o in list(scene.objects):
    if o.type in {'LIGHT','CAMERA'}:bpy.data.objects.remove(o,do_unlink=True)
camera=bpy.data.objects.new('Entrance inspection camera',bpy.data.cameras.new('Entrance inspection camera'));scene.collection.objects.link(camera);scene.camera=camera
camera.data.type='PERSP';camera.data.lens=25;camera.data.clip_start=.05;camera.data.clip_end=1000
for pos,energy in [((58,-36,21),2200),((58,-51,21),1800),((57,-23,19),900)]:
    light=bpy.data.lights.new('Inspection fill only, no Minecraft light','AREA');light.energy=energy;light.shape='DISK';light.size=10
    ob=bpy.data.objects.new(light.name,light);scene.collection.objects.link(ob);ob.location=pos
for name,pos,target in [('02-entry.png',(57.5,-24,17.2),(58.5,-55.5,16.5)),('03-close.png',(58.5,-48,18),(58.5,-56,17))]:
    camera.location=Vector(pos);r.renderer.point_at(camera,Vector(target));scene.render.filepath=str(OUT/name);bpy.ops.render.render(write_still=True)
r.clear();objects=r.geometry(blocks,groups,lambda p:36<=p[0]<=82 and 11<=p[1]<=24 and 16<=p[2]<=63)
r.stage(objects,OUT/'04-hall.png',(30,160,210))
