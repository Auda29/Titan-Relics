"""Titan Skull v3: broken articulated spine, partly buried in exported terrain."""
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import create_titan_skull_v2 as base
import create_titan_skull_v1 as bone
from create_blender_colossus import xyz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "relics/titan-skull/design/generated/titan-skull-v3"


def ground(x, z):
    original = base.terrain_height(x, z)
    r2 = ((x-20)/45)**2+((z-94)/77)**2
    if r2 >= 1:
        return original
    f = 1-r2
    extension = -5+18*f**1.2+.6*f*math.sin(x*.17+z*.12)
    return max(original, extension)


def vertebra(number, center, size, yaw, roll, broken=False):
    before = set(bpy.context.scene.objects)
    bone.organic(f"Vertebra {number} | centrum", (0, -1.8*size, 0), (6.3*size, 4.6*size, 3.8*size), rough=.3)
    # A true arch around a visible neural canal; independent transverse processes.
    points = [(5.3*size*math.cos(a), (3.2+4.6*math.sin(a))*size, 0)
              for a in [math.tau*i/20 for i in range(21)]]
    bone.tube(f"Vertebra {number} | neural arch", points, [1.65*size]*len(points), "worn", 8)
    for s in (-1, 1):
        bone.tube(f"Vertebra {number} | transverse process", [(s*4*size, 0, 0), (s*8*size, size, -size),
                  (s*(9.5 if broken and s == 1 else 12)*size, 2.2*size, -2.5*size)],
                  [2.7*size, 2*size, (1.8 if broken else .8)*size], "bone", 8)
    bone.tube(f"Vertebra {number} | dorsal process", [(0, 6.8*size, 0), (0, 10*size, size),
              ((1 if number%2 else -1)*size, (11 if broken else 14)*size, 2.8*size)],
              [2.6*size, 1.8*size, (1.5 if broken else .65)*size], "worn", 8)
    transform = (Matrix.Translation(Vector(xyz(center))) @ Matrix.Rotation(math.radians(yaw), 4, "Z")
                 @ Matrix.Rotation(math.radians(roll), 4, "Y"))
    objects = list(set(bpy.context.scene.objects)-before)
    for obj in objects:
        obj.matrix_world = transform @ obj.matrix_world
        obj["asset_component"] = "spine"
        obj["vertebra_index"] = number
    return objects


def main():
    design = base.main(export=False)
    # Retain the exact v2 skull and replace only its hill with the extended shape.
    for obj in list(bpy.context.scene.objects):
        if obj.get("asset_component") == "exported_terrain":
            bpy.data.objects.remove(obj, do_unlink=True)
    skull_objects = [obj for obj in bpy.context.scene.objects if obj.get("asset_component") == "skull"]
    centers = []
    # Three attached cervical vertebrae, then a real gap and a displaced rear chain.
    specs = [(0, 20, 1.05, 0, -4, False), (1, 31, 1.0, 3, 5, False), (2, 43, 1.05, 5, -7, True),
             (14, 65, 1.12, 17, 24, True), (19, 78, 1.10, 21, 17, False),
             (24, 92, 1.05, 18, 8, False), (30, 106, 1.0, 12, -8, False),
             (34, 120, .95, 8, -19, True), (29, 142, .85, -20, 32, True)]
    for i, (x, z, size, yaw, roll, broken) in enumerate(specs):
        y = ground(x, z)+1.0
        if i == 0:
            y = 23.5
        center = (x, y, z)
        objects = vertebra(i+1, center, size, yaw, roll, broken)
        bpy.context.view_layer.update()
        points = [obj.matrix_world @ vertex.co for obj in objects for vertex in obj.data.vertices]
        below = sum(p.z < ground(p.x, -p.y) for p in points)
        centers.append({"index": i+1, "center_source": list(center), "ground_source_y": ground(x, z),
                        "source_vertices_below_terrain_fraction": below/len(points),
                        "group": "attached" if i < 3 else ("detached_chain" if i < 8 else "loose_tail")})
    # Short fossilized connections on each retained chain, never across a fracture.
    connections = [((-1, 23.5, 10), centers[0]["center_source"])]
    connections += [(centers[a]["center_source"], centers[b]["center_source"])
                    for a, b in [(0, 1), (1, 2), (3, 4), (4, 5), (5, 6), (6, 7)]]
    for a, b in connections:
        obj = bone.tube("Retained intervertebral connection", [a, b], [2.3, 2.0], "mineral", 10)
        obj["asset_component"] = "spine"
    # Broken processes lie on the slope beside the major dislocation.
    for x, z in [(14, 53), (-5, 57), (40, 133)]:
        y = ground(x, z)+.2
        fragment = bone.tube("Detached vertebral process fragment", [(x, y, z), (x+3, y+1.5, z+2), (x+7, y, z+2)],
                             [2.2, 2.4, .8], "worn", 7)
        fragment["asset_component"] = "spine"
    # Dense terrain interiors intentionally cover lower vertebral bodies while
    # leaving arches and spinous processes exposed. No whole-asset solid fill.
    base.mound(ground, range(-58, 73, 2), range(-38, 175, 2))
    bpy.context.view_layer.update()
    low, high = base.bounds([o for o in bpy.context.scene.objects if o.type == "MESH"])
    scale = 79/(high[2]-low[2])
    assert abs(scale-design["blocks_per_source_unit"]) < 1e-6, "Spine changed the accepted skull scale"
    assert base.bounds(skull_objects) == design["skull_bounds_blender"], "Skull geometry was altered"
    design.update(name="Titan Skull v3", source_bounds_blender=[low, high], blocks_per_source_unit=scale)
    design["exported_mound"]["solid_probes_source"] += [[20, 0, 82], [30, -1, 121]]
    design["spine"] = {"vertebrae": centers, "major_fracture_source_z": [49, 57],
                       "secondary_fracture_source_z": [127, 134],
                       "fracture_probe_planes_source_z": [50, 129],
                       "scale_preserved_from": "titan-skull-v2",
                       "bone_materials": ["minecraft:dripstone_block", "minecraft:sandstone", "minecraft:tuff"],
                       "note": "Three attached vertebrae, five displaced connected vertebrae, one isolated terminal vertebra; lower bodies buried."}
    design["interpretation"] = "Colossus-head-scale skull with a broken partly buried spine and extended solid local hill. Spine is an original design addition."
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "titan-skull-v3.design.json").write_text(json.dumps(design, indent=2)+"\n", encoding="utf-8")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.wm.obj_export(filepath=str(OUT / "titan-skull-v3.obj"), forward_axis="NEGATIVE_Z", up_axis="Y",
                          export_selected_objects=True, export_triangulated_mesh=True, export_materials=True)
    bpy.context.scene["design_name"] = "Titan Skull v3"
    bpy.context.scene["scale_note"] = "V2 skull preserved; broken spine and extended terrain are exported."
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "titan-skull-v3-source.blend"))
    print(json.dumps(design, indent=2))


if __name__ == "__main__":
    main()
