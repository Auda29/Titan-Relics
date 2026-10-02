"""V4 obelisk: restrained weathering, shallow chips, scattered sand and foundations."""
import copy
import hashlib
import json
import math
from pathlib import Path
import sys

import bmesh
import bpy
from mathutils import Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
from create_blender_colossus import xyz, box, subtract
from create_colossus_v3 import ellipsoid
from create_titan_skull_v2 import bounds
from relic_v4_terrain import build_deposits, obelisk_height

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"relics/obelisk/design"
BASE=DESIGN/"generated/obelisk-v3"
SOURCE=BASE/"obelisk-v3-source.blend"
OUT=DESIGN/"generated/obelisk-v4"
COLORS={"stone":"bba57e","facet":"a08262","sunward":"cdbd99","core":"b69c6a",
        "worn":"ccba92","mineral":"83664c","terrain_top":"d5c595",
        "terrain_patch":"bbab7c","terrain_fill":"b8a77c"}


def volume(obj):
    mesh=bmesh.new()
    mesh.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(mesh,faces=list(mesh.faces))
    assert all(e.is_manifold for e in mesh.edges), "Monolith must stay watertight"
    result=mesh.calc_volume(signed=True)
    mesh.to_mesh(obj.data)
    mesh.free()
    return result


def main():
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    original=json.loads((BASE/"obelisk-v3.design.json").read_text())
    for name,color in COLORS.items():
        mat=bpy.data.materials.get(name) or bpy.data.materials.new(name)
        mat.diffuse_color=(*[int(color[i:i+2],16)/255 for i in (0,2,4)],1)
    obj=bpy.data.objects["Obelisk v3 | tapered square antiprism"]
    obj.name="Obelisk V4 | upright weathered antiprism"
    original_volume=volume(obj)
    original_bounds=bounds([obj])
    # Subdivision changes material resolution, not the eight original planes.
    mesh=bmesh.new()
    mesh.from_mesh(obj.data)
    bmesh.ops.triangulate(mesh,faces=list(mesh.faces))
    bmesh.ops.subdivide_edges(mesh,edges=list(mesh.edges),cuts=47,use_grid_fill=True)
    mesh.to_mesh(obj.data)
    mesh.free()
    chips=[]
    bottom=[(-12,-8,-12),(12,-8,-12),(12,-8,12),(-12,-8,12)]
    top=[(0,176,-24*.67/math.sqrt(2)),(24*.67/math.sqrt(2),176,0),
         (0,176,24*.67/math.sqrt(2)),(-24*.67/math.sqrt(2),176,0)]
    for index,t,rx,ry in [(0,.27,2.2,4.5),(1,.54,2.3,5.0),(2,.78,1.9,4.0),(3,.43,1.8,3.5)]:
        p=Vector(bottom[index]).lerp(Vector(top[index]),t)
        radial=Vector((p.x,0,p.z)).normalized()
        center=p+radial*1.45
        cutter=ellipsoid("Shallow edge abrasion",center,(rx,ry,rx),"worn",16,12)
        subtract(obj,cutter)
        chips.append({"edge":index,"source_center":list(center),"radius_horizontal":rx,"radius_vertical":ry})
    obj.data.materials.clear()
    names=["stone","facet","sunward","worn","mineral","core"]
    for name in names: obj.data.materials.append(bpy.data.materials[name])
    for face in obj.data.polygons:
        p=obj.matrix_world@face.center
        x,y,z=p.x,p.z,-p.y
        if y < -7.5: name="core"
        elif y > 175.5: name="worn"
        else:
            n=math.sin(x*.23+z*.17+y*.047)+.56*math.sin(y*.12-z*.24)+.17*math.sin(x*.55-y*.29)
            name="stone" if n<.75 else "sunward"
            if n < -.65: name="facet"
            if n > 1.05: name="worn"
            # A few narrow, discontinuous mineral seams, not encircling cracks.
            if z < -7 and (43<y<55 or 104<y<112) and abs(x-(1.5+math.sin(y*.4)))<.55:
                name="mineral"
        face.material_index=names.index(name)
    new_volume=volume(obj)
    assert .99 < new_volume/original_volume <= 1, "Excessive damage to the monument"
    assert bounds([obj])==original_bounds, "Height, crown or base silhouette changed"
    # Only low, separated sand drifts; no continuous ring or supporting platform.
    build_deposits(obelisk_height,list(range(-36,37)),list(range(-38,37)),depth=2,spacing=.65)
    for i,(center,size,angle) in enumerate([((-20,.8,-9),(7,3.4,4),-21),
                                           ((-23,.5,1),(5,2.8,5),13),
                                           ((18,.4,-20),(6,2.6,4),32)]):
        fragment=box(f"V4 | Exposed foundation fragment {i+1}",center,size,"worn",.65)
        fragment.rotation_euler.z=math.radians(angle)
    bpy.context.view_layer.update()
    low,high=bounds([o for o in bpy.context.scene.objects if o.type=="MESH"])
    assert low[2]==-8 and high[2]==176
    metadata=copy.deepcopy(original)
    metadata.pop("solid_core")
    metadata["base_antiprism"]=metadata.pop("antiprism")
    metadata.update(name="Obelisk V4",source_bounds_blender=[low,high],blocks_per_source_unit=1,
                    source_v3_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest())
    metadata["obelisk_v4"]={"shallow_chips":chips,"original_volume":original_volume,
        "weathered_volume":new_volume,"volume_removed_percent":100*(1-new_volume/original_volume),
        "monolith_bounds_blender":original_bounds,"core_center_source":[0,0,0],
        "foundation_fragments":3,"upright":True,"solid_core":True,
        "terrain_materials":["minecraft:sand","minecraft:sandstone"]}
    metadata["interpretation"]="Standing square antiprism; coherent surface weathering, four shallow chips, asymmetric sand and three foundation fragments."
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"obelisk-v4.design.json").write_text(json.dumps(metadata,indent=2)+"\n",encoding="utf-8")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.wm.obj_export(filepath=str(OUT/"obelisk-v4.obj"),forward_axis="NEGATIVE_Z",up_axis="Y",
        export_selected_objects=True,export_triangulated_mesh=True,export_materials=True)
    bpy.context.scene["design_name"]="Obelisk V4"
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"obelisk-v4-source.blend"))
    print(json.dumps(metadata,indent=2))


if __name__=="__main__":
    main()
