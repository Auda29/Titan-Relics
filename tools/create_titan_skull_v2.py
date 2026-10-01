"""Titan Skull v2: Colossus-head scale, intact rear, and exported solid grassy mound.

Internal terrain slices make the mound solid during surface voxelization without
filling the skull cavities. Run with Blender from the repository root.
"""
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import create_titan_skull_v1 as source
from create_blender_colossus import xyz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "design/generated/titan-skull-v2"
BOTTOM = -8


def terrain_height(x, z):
    radius = math.hypot((x-4)/56, (z-19)/51)
    edge = 1+.045*math.sin(math.atan2(z-19, x-4)*5)
    if radius >= edge:
        return BOTTOM
    f = max(0, 1-(radius/edge)**2)
    height = -5+30*f**1.45+1.2*f*math.sin(x*.16+z*.13)
    # Leave the forward oral cavity and approach clear; banks rise at either side.
    corridor = max(0, 1-abs(x)/15)*max(0, min(1, (15-z)/13))
    height = height*(1-corridor)+min(height, 2.5)*corridor
    return height


def mesh_object(name, vertices, faces, materials, indices=None):
    used = sorted({index for face in faces for index in face})
    remap = {old: new for new, old in enumerate(used)}
    vertices = [vertices[i] for i in used]
    faces = [tuple(remap[i] for i in face) for face in faces]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    for material in materials:
        mesh.materials.append(bpy.data.materials[material])
    if indices:
        for p, index in zip(mesh.polygons, indices):
            p.material_index = index
    obj["asset_component"] = "exported_terrain"
    return obj


def clipped_slice(triangle, level):
    """Clip a terrain triangle in XYZ against height >= level; project to plane."""
    result = []
    for a, b in zip(triangle, triangle[1:]+triangle[:1]):
        if a[1] >= level:
            result.append((a[0], level, a[2]))
        if (a[1] >= level) != (b[1] >= level):
            t = (level-a[1])/(b[1]-a[1])
            result.append((a[0]+t*(b[0]-a[0]), level, a[2]+t*(b[2]-a[2])))
    return result


def mound(height_fn=None, grid_x=None, grid_z=None):
    height_fn = height_fn or terrain_height
    for name, color in {"soil": "73513a", "turf": "627541", "rock": "686960"}.items():
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = (*[int(color[i:i+2], 16)/255 for i in (0, 2, 4)], 1)
    vertices, faces, mats, triangles = [], [], [], []
    xs = list(grid_x) if grid_x is not None else list(range(-58, 67, 2))
    zs = list(grid_z) if grid_z is not None else list(range(-38, 77, 2))
    for z in zs:
        for x in xs:
            vertices.append(xyz((x, height_fn(x, z), z)))
    n = len(xs)
    for j in range(len(zs)-1):
        for i in range(n-1):
            a = j*n+i
            for face in [(a, a+n, a+1), (a+1, a+n, a+n+1)]:
                points = [(vertices[k][0], vertices[k][2], -vertices[k][1]) for k in face]
                heights = [p[1] for p in points]
                if max(heights) <= BOTTOM:
                    continue
                faces.append(face)
                triangles.append(points)
                center = tuple(sum(p[k] for p in points)/3 for k in range(3))
                slope = (max(heights)-min(heights))/2
                mats.append(2 if min(heights) < -3 else (1 if slope > 1.5 else 0))
    mesh_object("08 | Exported irregular grass and soil surface", vertices, faces, ["turf", "soil", "rock"], mats)
    # Horizontal slices spaced below one voxel ensure every interior terrain cell
    # is represented. No global fill: oral/cranial air remains open.
    verts, faces, mats = [], [], []
    for step in range(45):
        level = BOTTOM+step*.75
        for triangle in triangles:
            if max(p[1] for p in triangle) <= level+.4:
                continue
            poly = clipped_slice(triangle, level)
            if len(poly) < 3:
                continue
            start = len(verts)
            verts.extend(xyz(p) for p in poly)
            faces.append(tuple(range(start, start+len(poly))))
            mats.append(1 if level < -3 else 0)
    mesh_object("09 | Exported solid mound interior slices", verts, faces, ["soil", "rock"], mats)


def bounds(objects):
    points = [obj.matrix_world @ Vector(v) for obj in objects for v in obj.bound_box]
    return [[min(p[i] for p in points) for i in range(3)], [max(p[i] for p in points) for i in range(3)]]


def main(export=True):
    original = source.main(export=False)
    skull_objects = list(bpy.context.scene.objects)
    factor = 76/(original["source_bounds_blender"][1][2]-original["source_bounds_blender"][0][2])
    for obj in skull_objects:
        # Bake transforms into source units; origin and cavities stay consistent.
        for vertex in obj.data.vertices:
            vertex.co = (obj.matrix_world @ vertex.co)*factor
        obj.matrix_world.identity()
        obj["asset_component"] = "skull"
    bpy.context.view_layer.update()
    skull_bounds = bounds(skull_objects)
    mound()
    bpy.context.view_layer.update()
    all_bounds = bounds([o for o in bpy.context.scene.objects if o.type == "MESH"])
    low, high = all_bounds
    scale = 79/(high[2]-low[2])
    colossus = json.loads((ROOT / "design/generated/colossus-v3/colossus-v3.design.json").read_text())
    # Measure the actual dome shell from the saved Colossus model, after its tilt.
    blend = ROOT / "design/generated/colossus-v3/colossus-v3-source.blend"
    with bpy.data.libraries.load(str(blend), link=False) as (available, loaded):
        loaded.objects = [n for n in available.objects if n.startswith("04 | Round diving helmet")]
    assert len(loaded.objects) == 1, "Expected the Colossus dome shell"
    helmet = loaded.objects[0]
    bpy.context.collection.objects.link(helmet)
    bpy.context.view_layer.update()
    points = [helmet.matrix_world @ vertex.co for vertex in helmet.data.vertices]
    head_bounds = [[min(p[i] for p in points) for i in range(3)], [max(p[i] for p in points) for i in range(3)]]
    head_dims = [(head_bounds[1][i]-head_bounds[0][i])*colossus["blocks_per_source_unit"] for i in (0, 2, 1)]
    bpy.data.objects.remove(helmet, do_unlink=True)
    metadata = {
        "name": "Titan Skull v2", "reference": original["reference"], "reference_seconds": [0, 5],
        "source_bounds_blender": all_bounds, "height_target_blocks": 80,
        "ground_level_source": 0, "ground_level_nbt_approx": round(-low[2]*scale),
        "blocks_per_source_unit": scale, "scale_is_estimate": True,
        "skull_bounds_blender": skull_bounds,
        "skull_height_blocks_approx": (skull_bounds[1][2]-skull_bounds[0][2])*scale,
        "colossus_head_reference": {"asset": "colossus-v3", "part": "Round diving helmet dome shell",
                                    "dimensions_xyz_blocks": head_dims,
                                    "skull_to_helmet_height_ratio": 76*scale/head_dims[1]},
        "skull_scale_from_v1_source": factor,
        "exported_mound": {"bottom_source_y": BOTTOM, "slice_spacing": .75,
                            "solid_probes_source": [[-20, 0, 20], [20, 4, 24], [0, 5, 38]],
                            "terrain_materials": ["minecraft:moss_block", "minecraft:dirt", "minecraft:stone"]},
        "rear_wall_probe_source": [0, 103*factor, 45*factor],
        "cavity_probes_source": [[v*factor for v in p] for p in original["cavity_probes_source"]],
        "interpretation": "Skull modestly larger than Colossus dome; complete rear; actual exported grassy mound, not just a render prop.",
        "air_policy": "omit; local generated mound leaves mouth clear; existing world terrain still requires an explicit clearing policy",
    }
    if not export:
        return metadata
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "titan-skull-v2.design.json").write_text(json.dumps(metadata, indent=2)+"\n", encoding="utf-8")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.wm.obj_export(filepath=str(OUT / "titan-skull-v2.obj"), forward_axis="NEGATIVE_Z", up_axis="Y",
                          export_selected_objects=True, export_triangulated_mesh=True, export_materials=True)
    bpy.context.scene["design_name"] = "Titan Skull v2"
    bpy.context.scene["scale_note"] = "76-block skull at Colossus-head scale, with exported terrain; rear is complete."
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "titan-skull-v2-source.blend"))
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
