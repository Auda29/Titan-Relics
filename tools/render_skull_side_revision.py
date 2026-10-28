"""Editable per-state voxel points, NBT surface meshes, and fresh reopen proof."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
import render_gameplay_interiors as r
from build_skull_side_revision import OUT,STEM,SOURCE,sha,dump

def mesh_digest(objects):
 payload=[]
 for o in sorted(objects,key=lambda o:o['block_state']):
  payload.append([o['block_state'],[list(v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons],[list(d.uv) for d in o.data.uv_layers.active.data]])
 return hashlib.sha256(json.dumps(payload,separators=(',',':')).encode()).hexdigest()

def recovered_voxels():
 cells={}
 for o in bpy.context.scene.objects:
  if 'voxel_state' not in o:continue
  for v in o.data.vertices:
   q=o.matrix_world@v.co;p=(round(q.x-.5),round(q.z-.5),round(-q.y-.5))
   assert max(abs(q.x-p[0]-.5),abs(q.z-p[1]-.5),abs(-q.y-p[2]-.5))<1e-5
   assert p not in cells;cells[p]=o['voxel_state']
 return cells

def stage():
 s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=True
 s.render.resolution_x=1278;s.render.resolution_y=850;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard'
 w=bpy.data.worlds.new('Inspection daylight');w.use_nodes=True;s.world=w
 next(n for n in w.node_tree.nodes if n.type=='BACKGROUND').inputs['Strength'].default_value=.9
 l=bpy.data.lights.new('Sun','SUN');l.energy=2;o=bpy.data.objects.new('Sun',l);s.collection.objects.link(o);o.rotation_euler=(.5,.5,2.4)
 c=bpy.data.objects.new('Screenshot comparison camera',bpy.data.cameras.new('Camera'));s.collection.objects.link(c);s.camera=c;c.data.lens=30;c.data.clip_end=600
 c.location=(80,35,40);r.renderer.point_at(c,Vector((85,-10,33)))
 s['camera_note']='Approximate screenshot view; neutral daylight; no world terrain recreated. Ground contract remains 28.'
 return s

def main():
 nbt=OUT/(STEM+'.nbt');root,after=r.read_structure(nbt);_,before=r.read_structure(SOURCE)
 for name,blocks in [('before',before),('after',after)]:
  r.clear();objects=r.geometry(blocks,{});s=stage()
  s.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
  if name=='before':continue
  signature=mesh_digest(objects)
  collection=bpy.data.collections.new('Editable voxel points - authoritative export source');s.collection.children.link(collection)
  for state in sorted(set(blocks.values())):
   points=[(x+.5,-z-.5,y+.5) for (x,y,z),v in sorted(blocks.items()) if v==state]
   mesh=bpy.data.meshes.new(state+' voxel points');mesh.from_pydata(points,[],[]);mesh.update()
   obj=bpy.data.objects.new(state+' editable voxels',mesh);collection.objects.link(obj);obj['voxel_state']=state;obj.hide_render=True;obj.hide_set(True)
  s['source_nbt_sha256']=sha(nbt);s['source_nbt']=str(nbt);s['size']=root['size'];s['ground_y']=28;s['source_offset']=[0,0,0]
  s['editing']='Unhide voxel points; edit integer-aligned points by state. recovered_voxels() exports the authoritative cells; surface meshes are rebuildable previews.'
  s['surface_sha256']=signature
  path=OUT/(STEM+'-source.blend');bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True)
  bpy.ops.wm.open_mainfile(filepath=str(path));assert recovered_voxels()==after
  meshes=[o for o in bpy.context.scene.objects if 'block_state' in o]
  assert mesh_digest(meshes)==signature
  assert bpy.context.scene['source_nbt_sha256']==sha(nbt)
  # Independently rebuild all visible topology and UVs from freshly read exported NBT.
  _,fresh=r.read_structure(nbt);r.clear();r.MATS.clear();rebuilt=r.geometry(fresh,{})
  assert mesh_digest(rebuilt)==signature
  dump(OUT/'source-verification.json',{'fresh_reopen':True,'voxel_cells_equal_nbt':len(after),'independent_surface_rebuild_equal':True,'surface_sha256':signature,'blend_sha256':sha(path),'bound_nbt_sha256':sha(nbt)})
if __name__=='__main__':
 if '--verify-only' in sys.argv:
  nbt=OUT/(STEM+'.nbt');path=OUT/(STEM+'-source.blend');_,fresh=r.read_structure(nbt)
  bpy.ops.wm.open_mainfile(filepath=str(path));assert recovered_voxels()==fresh
  signature=mesh_digest([o for o in bpy.context.scene.objects if 'block_state' in o])
  assert bpy.context.scene['source_nbt_sha256']==sha(nbt)
  r.clear();r.MATS.clear();assert mesh_digest(r.geometry(fresh,{}))==signature
  dump(OUT/'source-verification.json',{'fresh_reopen':True,'voxel_cells_equal_nbt':len(fresh),'independent_surface_rebuild_equal':True,'surface_sha256':signature,'blend_sha256':sha(path),'bound_nbt_sha256':sha(nbt)})
 else:main()

