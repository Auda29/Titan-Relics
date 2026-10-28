"""Create editable V7 source and labelled inspection crops from exported NBT."""
import hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_gameplay_interiors as r
import render_gameplay_interiors_revision  # Blender 5.2 compatible lighting and glass
from build_colossus_landmarks import OUT,STEM

side=json.loads((OUT/(STEM+'.gameplay.json')).read_text())
_,blocks=r.read_structure(OUT/(STEM+'.nbt'))
groups={tuple(p):k for k,v in json.loads((OUT/(STEM+'.groups.json')).read_text()).items() for p in v}
if '--verify' in sys.argv:
    path=OUT/(STEM+'-source.blend');bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene
    assert scene['source_nbt_sha256']==side['source_sha256']
    meshes=[o for o in scene.objects if o.type=='MESH' and 'block_state' in o]
    assert meshes and all(len(o.data.polygons)>0 and len(o.data.materials)>0 for o in meshes)
    assert {'arm-find-frame','central-guard-frame','central-vault-console'} <= {o['authoring_group'] for o in meshes}
    # Every face in the three edited mesh groups must border an NBT voxel of
    # the same block state and group; no render-only architectural geometry.
    import math
    checked_faces=0
    for o in meshes:
        group=o['authoring_group']
        if group not in {'arm-find-frame','central-guard-frame','central-vault-console'}: continue
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

if '--guard-only' in sys.argv:
    r.clear()
    lo,hi=(88,167,176),(101,174,190)
    objects=r.geometry(blocks,groups,lambda p:all(a<=v<=c for v,a,c in zip(p,lo,hi)))
    r.stage(objects,OUT/'03-guard.png',(0,60,300))
    sys.exit(0)

r.clear();objects=r.geometry(blocks,groups)
for m in side['markers']:
    o=bpy.data.objects.new(m['id'],None);bpy.context.scene.collection.objects.link(o)
    x,y,z=m['pos'];o.location=(x+.5,-z-.5,y+.5);o.empty_display_type='SPHERE';o.empty_display_size=.65;o['gameplay_marker']=json.dumps(m)
scene=bpy.context.scene;scene['source_nbt_sha256']=side['source_sha256'];scene['coordinates']='Minecraft X,Y,Z to Blender X,-Z,Y'
scene['pipeline']='NBT surface meshes; export from tools/build_colossus_landmarks.py'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(STEM+'-source.blend')),compress=True)
r.stage(objects,OUT/'01-overview.png',(180,280,140),side['ground_y'])
views=[('02-arm-find.png',(104,74,65),(117,85,78),(95,-140,115)),
       ('03-guard.png',(88,167,176),(101,174,190),(0,60,300)),
       ('04-vault-console.png',(89,167,161),(100,174,172),(20,-140,110))]
for filename,lo,hi,direction in views:
    r.clear();objects=r.geometry(blocks,groups,lambda p:all(a<=v<=c for v,a,c in zip(p,lo,hi)))
    r.stage(objects,OUT/filename,direction)
print('Saved editable source and inspection crops')


