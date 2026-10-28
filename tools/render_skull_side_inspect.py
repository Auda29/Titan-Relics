import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
import render_gameplay_interiors as r
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'relics/titan-skull/design/generated/titan-skull-2-v2-embedded-side-v1'
OUT.mkdir(exist_ok=True)
src=ROOT/'relics/titan-skull/design/generated/titan-skull-2-v2-embedded-v1/titan-skull-2-v2-embedded-v1.nbt'
_,blocks=r.read_structure(src)
r.clear();r.geometry(blocks,{})
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=12;s.cycles.use_denoising=True
s.render.resolution_x=1100;s.render.resolution_y=800;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard'
w=bpy.data.worlds.new('Inspection daylight');w.use_nodes=True;s.world=w
next(n for n in w.node_tree.nodes if n.type=='BACKGROUND').inputs['Strength'].default_value=.8
l=bpy.data.lights.new('Sun','SUN');l.energy=2;o=bpy.data.objects.new('Sun',l);s.collection.objects.link(o);o.rotation_euler=(.3,-.5,-.3)
c=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));s.collection.objects.link(c);s.camera=c;c.data.lens=30;c.data.clip_end=600
for name,pos,target in [('left-candidate',(-25,10,48),(16,-30,34)),('right-candidate',(120,40,49),(81,-8,34)),('overview',(150,180,140),(49,-45,48))]:
 c.location=pos;r.renderer.point_at(c,Vector(target));s.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
