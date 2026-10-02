"""Quiet face-consistent V4.1 sandstone with real branching cracks, preserving V4 scenery."""
import hashlib
import json
import math
from pathlib import Path
import sys

import bmesh
import bpy
from mathutils import Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
from create_blender_colossus import xyz, cylinder, subtract
from create_colossus_v3 import ellipsoid
from create_colossus_v4 import fingerprint
from create_obelisk_v4 import volume
from create_titan_skull_v2 import bounds

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"relics/obelisk/design"
BASE=DESIGN/"generated/obelisk-v4"
STEM="obelisk-v4-1"
OUT=DESIGN/"generated"/STEM


def mc(v): return Vector((v.x,v.z,-v.y))


def main():
    source=BASE/"obelisk-v4-source.blend"
    bpy.ops.wm.open_mainfile(filepath=str(source))
    old=bpy.data.objects["Obelisk V4 | upright weathered antiprism"]
    bpy.data.objects.remove(old,do_unlink=True)
    preserved={o.name:fingerprint(o) for o in bpy.context.scene.objects if o.type=="MESH"}
    v3=DESIGN/"generated/obelisk-v3/obelisk-v3-source.blend"
    with bpy.data.libraries.load(str(v3),link=False) as (available,loaded):
        loaded.objects=["Obelisk v3 | tapered square antiprism"]
    obj=loaded.objects[0]
    bpy.context.collection.objects.link(obj)
    obj.name="Obelisk V4.1 | consistent sandstone facets and open cracks"
    # Reuse canonical material names; imported source slots may carry .001 suffixes.
    for slot in obj.material_slots:
        slot.material=bpy.data.materials[slot.material.name.split(".")[0]]
    for name,color in {"stone":"d6c698","facet":"c7b88d","sunward":"dfd3ac",
                       "worn":"c6b58a","mineral":"95806a"}.items():
        bpy.data.materials[name].diffuse_color=(*[int(color[i:i+2],16)/255 for i in (0,2,4)],1)
    original_volume=volume(obj)
    original_bounds=bounds([obj])
    planes=[]
    for f in obj.data.polygons:
        if len(f.vertices)==3:
            planes.append({"normal":mc(f.normal),"center":mc(f.center),
                "vertices":[mc(obj.data.vertices[i].co) for i in f.vertices],
                "material":obj.data.materials[f.material_index].name})
    bm=bmesh.new();bm.from_mesh(obj.data)
    bmesh.ops.triangulate(bm,faces=list(bm.faces))
    bmesh.ops.subdivide_edges(bm,edges=list(bm.edges),cuts=47,use_grid_fill=True)
    bm.to_mesh(obj.data);bm.free()
    # Local tangent paths on three different original planes. No full-height bands.
    cracks=[]
    chosen=[planes[i] for i in (0,3,6)]
    for index,plane in enumerate(chosen):
        normal=plane["normal"]
        up=(Vector((0,1,0))-normal*normal.y).normalized()
        across=up.cross(normal).normalized()
        anchor=plane["center"]+up*(22 if index==2 else 0)
        paths=[
            [[(0,17),(-1.8,10),(.6,3),(-1,-4),(2,-12),(1,-18)],
             [(.6,3),(4,7),(5.5,12)]],
            [[(-2,14),(0,7),(-1,0),(1,-8),(-.5,-15)],
             [(-1,0),(-4,-3),(-5,-7)]],
            [[(-2,12),(-.5,7),(-1,0),(1,-6),(0,-13)],
             [(-.5,7),(2,4),(4,2)]],
        ][index]
        samples=[]
        for branch,path in enumerate(paths):
            points=[anchor+across*u+up*v+normal*.1 for u,v in path]
            radius=1.55 if branch==0 else .95
            for a,b in zip(points,points[1:]):
                subtract(obj,cylinder("V4.1 | Open weathered fissure",a,b,radius,"mineral",12))
                samples.append(list((a+b)/2))
            for p in points[1:-1]:
                subtract(obj,ellipsoid("V4.1 | Crack junction",p,(radius,radius,radius),"mineral",12,8))
        cracks.append({"face":index,"center_source":list(anchor),"normal_source":list(normal),
                       "surface_samples_source":samples,"main_width_source":3.1,
                       "main_height_source":paths[0][0][1]-paths[0][-1][1]})
    chips=[]
    bottom=[(-12,-8,-12),(12,-8,-12),(12,-8,12),(-12,-8,12)]
    top=[(0,176,-24*.67/math.sqrt(2)),(24*.67/math.sqrt(2),176,0),
         (0,176,24*.67/math.sqrt(2)),(-24*.67/math.sqrt(2),176,0)]
    for edge,t,rx,ry in [(0,.27,3.5,6.5),(1,.54,3.2,7),(2,.78,3.0,5.5),(3,.43,2.8,5)]:
        p=Vector(bottom[edge]).lerp(Vector(top[edge]),t)
        center=p+Vector((p.x,0,p.z)).normalized()*.9
        subtract(obj,ellipsoid("V4.1 | Broader edge spall",center,(rx,ry,rx),"worn",16,12))
        chips.append({"edge":edge,"source_center":list(center),"radius_horizontal":rx,"radius_vertical":ry})
    names=["stone","facet","sunward","worn","mineral","core"]
    obj.data.materials.clear()
    for name in names: obj.data.materials.append(bpy.data.materials[name])
    obj.data.update()
    for face in obj.data.polygons:
        p,n=mc(face.center),mc(face.normal)
        nearest=max(planes,key=lambda plane:n.dot(plane["normal"]))
        if p.y< -7.5: name="core"
        elif p.y>175.5: name="sunward"
        elif n.dot(nearest["normal"])<.998:
            # Darker material is confined to genuine cut surfaces.
            name="mineral" if any((p-Vector(c["center_source"])).length<22 for c in cracks) else "worn"
        else:
            name=nearest["material"]
            # Low-contrast local abrasion around fissures; no periodic tiger patches.
            if any((p-Vector(c["center_source"])).length<8 for c in cracks):
                name="worn"
        face.material_index=names.index(name)
    current_volume=volume(obj)
    assert .97<current_volume/original_volume<.999, "Cracks must be visible but retain a massive body"
    assert bounds([obj])==original_bounds
    bpy.context.view_layer.update()
    assert all(fingerprint(bpy.data.objects[n])==h for n,h in preserved.items())
    metadata=json.loads((BASE/"obelisk-v4.design.json").read_text())
    metadata.update(name="Obelisk V4.1 / consistent sandstone sides and branching cracks",
        source_v4_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),preserved_v4_objects=preserved,
        interpretation="Quiet face-consistent sandstone, three branching surface fissures, four broader edge spalls; V4 sand and foundations retained.")
    weather=metadata["obelisk_v4"]
    weather.update(shallow_chips=chips,weathered_volume=current_volume,
        volume_removed_percent=100*(1-current_volume/original_volume),cracks=cracks,
        maximum_damage_percent=3,face_consistent_palette=True)
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{STEM}.design.json").write_text(json.dumps(metadata,indent=2)+"\n")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.wm.obj_export(filepath=str(OUT/f"{STEM}.obj"),forward_axis="NEGATIVE_Z",up_axis="Y",
        export_selected_objects=True,export_triangulated_mesh=True,export_materials=True)
    bpy.context.scene["design_name"]=metadata["name"]
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/f"{STEM}-source.blend"))
    print(f"Preserved {len(preserved)} scenery objects; removed {weather['volume_removed_percent']:.3f}% of monolith volume")


if __name__=="__main__": main()
