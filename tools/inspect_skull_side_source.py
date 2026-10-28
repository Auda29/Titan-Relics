"""Read original editable anatomy to bind the removed export region to its chip."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from build_skull_side_revision import ROOT,OUT,sha,dump
source=ROOT/'relics/titan-skull/design/generated/titan-skull-2-v2/titan-skull-2-v2-source.blend'
design=source.with_name('titan-skull-2-v2.design.json');meta=json.loads(design.read_text());scale=meta['blocks_per_source_unit'];low,high=meta['source_bounds_blender']
bpy.ops.wm.open_mainfile(filepath=str(source));rows=[]
for o in bpy.context.scene.objects:
 if 'Local broken bone chip' not in o.name:continue
 points=[o.matrix_world@v.co for v in o.data.vertices]
 center=[sum(p[i] for p in points)/len(points) for i in range(3)]
 source_center=[center[0],center[2],-center[1]]
 mapped=[((p.x-low[0])*scale,(p.z-low[2])*scale,(-p.y+high[1])*scale) for p in points]
 rows.append({'object':o.name,'source_center':source_center,'materials':[m.name for m in o.data.materials],'export_float_bounds':[[f(p[i] for p in mapped) for i in range(3)] for f in (min,max)],'selected':abs(source_center[0]-40)<.01})
assert len(rows)==3 and sum(r['selected'] for r in rows)==1
dump(OUT/'original-source-binding.json',{'blend':source.relative_to(ROOT).as_posix(),'sha256':sha(source),'design_sha256':sha(design),'blocks_per_source_unit':scale,'chips':rows})
