"""Warm ochre V4.2 with unpainted fractures and actual missing edge chunks."""
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
from create_blender_colossus import xyz, subtract
from create_colossus_v4 import fingerprint
from create_obelisk_v4 import volume
from create_obelisk_v4_1 import mc
from create_titan_skull_v2 import bounds

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"relics/obelisk/design"
BASE=DESIGN/"generated/obelisk-v4-1"
STEM="obelisk-v4-2"
OUT=DESIGN/"generated"/STEM


def main():
    source=BASE/"obelisk-v4-1-source.blend"
    bpy.ops.wm.open_mainfile(filepath=str(source))
    obj=bpy.data.objects["Obelisk V4.1 | consistent sandstone facets and open cracks"]
    obj.name="Obelisk V4.2 | ochre monolith with missing edge chunks"
    original_bounds=bounds([obj])
    preserved={o.name:fingerprint(o) for o in bpy.context.scene.objects if o.type=="MESH" and o!=obj}
    # Original planes define both the broad sides and the exposed fracture stone.
    v3=DESIGN/"generated/obelisk-v3/obelisk-v3-source.blend"
    with bpy.data.libraries.load(str(v3),link=False) as (_,loaded):
        loaded.objects=["Obelisk v3 | tapered square antiprism"]
    reference=loaded.objects[0]
    planes=[(mc(f.center),mc(f.normal),reference.data.materials[f.material_index].name.split(".")[0])
            for f in reference.data.polygons if len(f.vertices)==3]
    bpy.data.objects.remove(reference,do_unlink=True)
    for name,color in {"ochre":"a87730","clay":"956b4a"}.items():
        mat=bpy.data.materials.new(name)
        mat.diffuse_color=(*[int(color[i:i+2],16)/255 for i in (0,2,4)],1)
    bottom=[(-12,-8,-12),(12,-8,-12),(12,-8,12),(-12,-8,12)]
    top=[(0,176,-24*.67/math.sqrt(2)),(24*.67/math.sqrt(2),176,0),
         (0,176,24*.67/math.sqrt(2)),(-24*.67/math.sqrt(2),176,0)]
    missing=[]
    for i,(edge,t,r,h) in enumerate([(0,.48,4.2,6.2),(1,.82,4.5,7.4)]):
        p=Vector(bottom[edge]).lerp(Vector(top[edge]),t)
        center=p+Vector((p.x,0,p.z)).normalized()*.35
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=xyz(center))
        cutter=bpy.context.object
        cutter.name="V4.2 | Irregular missing edge chunk"
        cutter.scale=(r,r,h)
        cutter.rotation_euler=(.18,-.15,.37+i*.44)
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        cutter.data.materials.append(bpy.data.materials["ochre"])
        subtract(obj,cutter)
        missing.append({"edge":edge,"center_source":list(center),"radius_horizontal":r,"radius_vertical":h})
    obj.data.materials.clear()
    for name in ("ochre","clay"): obj.data.materials.append(bpy.data.materials[name])
    obj.data.update()
    for face in obj.data.polygons:
        p=mc(face.center)
        # Distance to the original face, not cut normal, preserves that side's
        # material across intact surface, fissures and missing-piece interiors.
        nearest=min(planes,key=lambda plane:abs((p-plane[0]).dot(plane[1])))
        face.material_index=int(nearest[2]=="facet") if -7.5<p.y<175.5 else 0
    current_volume=volume(obj)
    bpy.context.view_layer.update()
    assert bounds([obj])==original_bounds
    assert all(fingerprint(bpy.data.objects[n])==digest for n,digest in preserved.items())
    metadata=json.loads((BASE/"obelisk-v4-1.design.json").read_text())
    metadata.update(name="Obelisk V4.2 / warm ochre and unpainted missing pieces",
        source_v4_1_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        preserved_v4_1_scenery_objects=preserved,
        interpretation="Ochre/clay facets with same-material cut faces; three open cracks and two additional missing angular edge chunks.")
    weather=metadata["obelisk_v4"]
    weather.update(weathered_volume=current_volume,
        volume_removed_percent=100*(1-current_volume/weather["original_volume"]),
        missing_chunks=missing,unpainted_damage=True,
        monolith_materials=["minecraft:yellow_terracotta","minecraft:terracotta"])
    assert 0<weather["volume_removed_percent"]<3
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{STEM}.design.json").write_text(json.dumps(metadata,indent=2)+"\n")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.wm.obj_export(filepath=str(OUT/f"{STEM}.obj"),forward_axis="NEGATIVE_Z",up_axis="Y",
        export_selected_objects=True,export_triangulated_mesh=True,export_materials=True)
    bpy.context.scene["design_name"]=metadata["name"]
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/f"{STEM}-source.blend"))
    print(f"Two unfilled missing pieces; monolith volume removed {weather['volume_removed_percent']:.3f}%")


if __name__=="__main__": main()
