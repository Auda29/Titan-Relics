"""Editable block-exact Blender sources and actual-NBT architectural cutaways.

Run in Blender with -- <catalog-id>. All spatial coordinates are raw-template
units. Text labels/sheets are composed by host Python, not Blender's Python.
"""
import json
import hashlib
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_ots_result import read_structure
from build_gameplay_interiors import ROOT,ASSETS,STEMS
import render_ots_preview as renderer

ATLAS=ROOT/'.work/foliage-preview-atlas'
DATA=json.loads((ATLAS/'vanilla.atlas').read_text())
ATLAS_BLOCKS={b['name']:b for b in DATA['blocks']}
MATS={}
FACES=renderer.FACES

def partial(state):return any(s in state for s in ('stairs','glow_lichen','cave_vines','firefly_bush'))

def mat(state):
    base=state.split('[')[0]
    if base in MATS:return MATS[base]
    alias={'minecraft:waxed_cut_copper':'minecraft:cut_copper','minecraft:deepslate_tile_stairs':'minecraft:deepslate_tiles',
           'minecraft:glow_lichen':'minecraft:moss_block','minecraft:firefly_bush':'minecraft:moss_block',
           'minecraft:cave_vines':'minecraft:moss_block','minecraft:cave_vines_plant':'minecraft:moss_block',
           'minecraft:grass_block':'minecraft:moss_block'}
    name=alias.get(base,base)
    assert name in ATLAS_BLOCKS,base
    material=renderer.material(base,(.5,.5,.5))
    image=bpy.data.images.get('interior-atlas')
    if image is None:
        image=bpy.data.images.load(str(ATLAS/'vanilla.png'));image.name='interior-atlas';image.pack()
    tex=material.node_tree.nodes.new('ShaderNodeTexImage');tex.image=image;tex.interpolation='Closest'
    bsdf=material.node_tree.nodes['Principled BSDF']
    material.node_tree.links.new(tex.outputs['Color'],bsdf.inputs['Base Color'])
    if 'shroomlight' in base or 'lichen' in base or 'cave_vines' in base:
        bsdf.inputs['Emission Color'].default_value=(.4,.6,.13,1)
        bsdf.inputs['Emission Strength'].default_value=.3
    MATS[base]=(material,name);return MATS[base]

def parts(state):
    if 'stairs' in state:
        upper=((0,.5,0),(1,1,.5))
        if 'facing=south' in state:upper=((0,.5,.5),(1,1,1))
        if 'facing=east' in state:upper=((.5,.5,0),(1,1,1))
        if 'facing=west' in state:upper=((0,.5,0),(.5,1,1))
        return [((0,0,0),(1,.5,1)),upper]
    if 'glow_lichen' in state:
        if 'west=true' in state:return [((0,0,0),(.025,1,1))]
        if 'east=true' in state:return [((.975,0,0),(1,1,1))]
        if 'north=true' in state:return [((0,0,0),(1,1,.025))]
        return [((0,0,.975),(1,1,1))]
    if 'cave_vines' in state:return [((.35,0,.35),(.65,1,.65))]
    if 'firefly_bush' in state:return [((.1,0,.48),(.9,.8,.52)),((.48,0,.1),(.52,.8,.9))]
    return [((0,0,0),(1,1,1))]

def geometry(blocks,groups,predicate=lambda p:True):
    selected={p:s for p,s in blocks.items() if predicate(p)}
    batches={}
    for p,s in selected.items():
        group=groups.get(p,'Preserved baseline')
        key=(group,s);vertices,faces,uvs=batches.setdefault(key,([],[],[]))
        material,name=mat(s)
        for lo,hi in parts(s):
            for delta,side,corners in FACES:
                q=tuple(a+b for a,b in zip(p,delta))
                if not partial(s) and q in selected and not partial(selected[q]):continue
                start=len(vertices)
                for c in corners:
                    x,y,z=[p[i]+lo[i]+c[i]*(hi[i]-lo[i]) for i in range(3)]
                    vertices.append((x,-z,y))
                faces.append(tuple(range(start,start+4)))
                t=DATA['textures'][ATLAS_BLOCKS[name]['faces'][side]];n=DATA['atlasSize']*3
                u0,u1=(t['atlasColumn']*3+1)/n,(t['atlasColumn']*3+2)/n
                v0,v1=1-(t['atlasRow']*3+2)/n,1-(t['atlasRow']*3+1)/n
                uvs.extend([(u0,v0),(u0,v1),(u1,v1),(u1,v0)])
    result=[]
    for (group,state),(vertices,faces,uvs) in batches.items():
        if not faces:continue
        collection=bpy.data.collections.get(group)
        if collection is None:
            collection=bpy.data.collections.new(group);bpy.context.scene.collection.children.link(collection)
        mesh=bpy.data.meshes.new(state);mesh.from_pydata(vertices,[],faces);mesh.update()
        uv=mesh.uv_layers.new(name='Native block atlas');uv.data.foreach_set('uv',[v for u in uvs for v in u])
        obj=bpy.data.objects.new(state,mesh);collection.objects.link(obj)
        obj['block_state']=state;obj['authoring_group']=group;mesh.materials.append(mat(state)[0]);result.append(obj)
    return result

def clear():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    for mesh in list(bpy.data.meshes):
        if not mesh.users:bpy.data.meshes.remove(mesh)

def stage(objects,out,direction,ground=None,markers=()):
    scene=bpy.context.scene
    scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
    scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='Standard'
    scene.world=bpy.data.worlds.new('Architectural daylight');scene.world.use_nodes=True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.74,.79,.85,1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
    bpy.context.view_layer.update()
    corners=[o.matrix_world@Vector(v) for o in objects for v in o.bound_box]
    lo=Vector(tuple(min(p[i] for p in corners) for i in range(3)));hi=Vector(tuple(max(p[i] for p in corners) for i in range(3)))
    center=(lo+hi)/2
    light=bpy.data.lights.new('Soft daylight','SUN');light.energy=1.7;light.angle=.3
    lamp=bpy.data.objects.new(light.name,light);scene.collection.objects.link(lamp);lamp.rotation_euler=(.3,-.6,-.2)
    camera=bpy.data.objects.new('Review camera',bpy.data.cameras.new('Review camera'));scene.collection.objects.link(camera)
    camera.data.type='ORTHO';camera.data.clip_end=3000;scene.camera=camera
    camera.location=center+Vector(direction).normalized()*700;renderer.point_at(camera,center)
    rotation=camera.rotation_euler.to_matrix().transposed();points=[rotation@(p-center) for p in corners]
    camera.data.ortho_scale=max(max(p.x for p in points)-min(p.x for p in points),(max(p.y for p in points)-min(p.y for p in points))*4/3)*1.16
    if ground is not None:
        bpy.ops.mesh.primitive_plane_add(size=2000,location=(center.x,center.y,ground-.1))
        bpy.context.object.data.materials.append(renderer.material('Presentation ground',(.44,.43,.38)))
    # Transparent marker envelopes identify reserved entity volumes and a person.
    for m in markers:
        if m['role'].endswith('_spawn'):
            x,y,z=m['pos'];h=2.7 if m['role']=='colossus_golem_spawn' else 2.9
            bpy.ops.mesh.primitive_cube_add(size=1,location=(x+.5,-z-.5,y+h/2))
            o=bpy.context.object;o.scale=(1.4,1.4,h) if h==2.7 else (.6,.6,h)
            wire=o.modifiers.new('Reserved entity envelope','WIREFRAME');wire.thickness=.035
            o.data.materials.append(renderer.material('Entity clearance',(.15,.65,.85)))
    scene.render.filepath=str(out);bpy.ops.render.render(write_still=True)

def main():
    name=sys.argv[sys.argv.index('--')+1]
    if name=='verify':
        for key,stem in STEMS.items():
            folder=(ROOT/ASSETS[key]['source']).parent.parent/stem
            path=folder/(stem+'-source.blend')
            sidecar=json.loads((folder/(stem+'.gameplay.json')).read_text())
            bpy.ops.wm.open_mainfile(filepath=str(path))
            assert bpy.context.scene['source_nbt_sha256']==sidecar['source_sha256'],stem
            mesh_count=sum(o.type=='MESH' for o in bpy.context.scene.objects)
            marker_count=sum('gameplay_marker' in o for o in bpy.context.scene.objects)
            assert marker_count==len(sidecar['markers']) and mesh_count>0
            report={'source_blend_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                    'bound_nbt_sha256':sidecar['source_sha256'],'mesh_count':mesh_count,
                    'marker_empties':marker_count,'opened_and_verified_in_blender':True}
            (folder/'source-verification.json').write_text(json.dumps(report,indent=2)+'\n')
        return
    stem=STEMS[name]
    folder=(ROOT/ASSETS[name]['source']).parent.parent/stem
    root,blocks=read_structure(folder/(stem+'.nbt'))
    design=json.loads((folder/(stem+'.design.json')).read_text());sidecar=json.loads((folder/(stem+'.gameplay.json')).read_text())
    group_data=json.loads((folder/(stem+'.groups.json')).read_text());groups={tuple(p):k for k,points in group_data.items() for p in points}
    clear();objects=geometry(blocks,groups)
    for marker in sidecar['markers']:
        o=bpy.data.objects.new(marker['id'],None);bpy.context.scene.collection.objects.link(o)
        x,y,z=marker['pos'];o.location=(x+.5,-z-.5,y+.5);o.empty_display_type='SPHERE';o.empty_display_size=.65
        o['gameplay_marker']=json.dumps(marker)
    bpy.context.scene['source_nbt_sha256']=sidecar['source_sha256']
    bpy.context.scene['coordinates']='Raw Minecraft X,Y,Z mapped to Blender X,-Z,Y; one unit per block'
    bpy.context.scene['pipeline']='Exact NBT derivative; editable state/group surface meshes. Rebuild/export using build_gameplay_interiors.py.'
    bpy.ops.wm.save_as_mainfile(filepath=str(folder/(stem+'-source.blend')),compress=True)
    stage(objects,folder/'01-overview.png',(180,280,140),sidecar['ground_y'])
    for i,view in enumerate(design['evidence']['views']):
        clear();lo,hi=view['lo'],view['hi']
        objects=geometry(blocks,groups,lambda p:all(a<=v<=c for v,a,c in zip(p,lo,hi)))
        markers=[m for m in sidecar['markers'] if all(a<=v<=c for v,a,c in zip(m['pos'],lo,hi))]
        stage(objects,folder/f'0{i+2}-detail.png',(100,150,190),
              ground=sidecar['ground_y'] if name=='world_tree' and i==0 else None,markers=markers)
    print('Editable source and review renders:',stem)

if __name__=='__main__':main()
