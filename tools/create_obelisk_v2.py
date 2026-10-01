"""Obelisk v2, a restrained monolith after Josh White's Painted Desert.

blender --background --python-exit-code 1 --python tools/create_obelisk_v2.py
MC XYZ, front -Z; flat crown at Y176, nominal ground Y0, buried foot to Y-32.
"""
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from create_blender_colossus import xyz, box, subtract, finish

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "relics/obelisk/design/generated/obelisk-v2"
COLORS = {"stone": "987344", "sunward": "d1b97d", "worn": "b99b68", "ochre": "a17151",
          "rust": "674b38", "vein": "73744b", "core": "b69c6a"}


def material_for(side, u, y):
    # Broad quiet fields with a few interrupted shallow mineral bands.
    wave = y+.65*math.sin(u*2.4+side)+.25*math.sin(y*.13+u*2)
    if side in (1, 3, 5, 7):
        return "sunward" if side in (5, 7) else "stone"
    base = "sunward" if side == 6 else "stone"
    if y < 0:
        return "core" if side == 6 else "stone"
    if side != 6:
        if any(level < wave < level+1.2 for level in (18, 41, 66, 89, 112, 141, 163)):
            return "ochre"
        if 33 < wave < 33.7 or 119 < wave < 119.7:
            return "vein"
        if 7 < wave < 8.2:
            return "worn"
    elif (16 < wave < 17 or 65 < wave < 66 or 116 < wave < 117) and u < .25:
        return "worn"
    return base


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for name, color in COLORS.items():
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = (*[int(color[i:i+2], 16)/255 for i in (0, 2, 4)], 1)
    levels = list(range(-32, 177))
    # Octagonal cross-section: four primary planes and tiny worn arrises.
    # One source unit is one block; the 209-cell sampling includes both end faces.
    samples = [10, 1, 8, 1, 10, 1, 8, 1]
    vertices, faces, materials = [], [], []
    ring_count = sum(samples)
    for y in levels:
        width, depth, bevel = 22, 18, .65
        outline = [(-width/2+bevel, -depth/2), (width/2-bevel, -depth/2),
                   (width/2, -depth/2+bevel), (width/2, depth/2-bevel),
                   (width/2-bevel, depth/2), (-width/2+bevel, depth/2),
                   (-width/2, depth/2-bevel), (-width/2, -depth/2+bevel)]
        for side, count in enumerate(samples):
            a, b = outline[side], outline[(side+1)%8]
            for j in range(count):
                f = j/count
                vertices.append(xyz((a[0]+(b[0]-a[0])*f, y, a[1]+(b[1]-a[1])*f)))
    for level, y in enumerate(levels[:-1]):
        offset = 0
        for side, count in enumerate(samples):
            for j in range(count):
                a = level*ring_count+offset+j
                b = level*ring_count+(offset+j+1)%ring_count
                faces.append((a, a+ring_count, b+ring_count, b))
                materials.append(material_for(side, 2*(j+.5)/count-1, y+.5))
            offset += count
    # Caps share perimeter vertices: a sealed volume for the optional solid fill.
    faces.append(tuple(range(ring_count)))
    materials.append("core")
    faces.append(tuple(reversed(range((len(levels)-1)*ring_count, len(levels)*ring_count))))
    materials.append("sunward")
    mesh = bpy.data.meshes.new("Continuous parallel-sided stone mass")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("01 | Flat-topped Painted Desert stele", mesh)
    bpy.context.collection.objects.link(obj)
    names = list(COLORS)
    for name in names:
        mesh.materials.append(bpy.data.materials[name])
    for face, name in zip(mesh.polygons, materials):
        face.material_index = names.index(name)
    # Very local losses; the long uninterrupted silhouette remains dominant.
    for name, center, size in [
        ("Low worn corner", (10.8, 9, -8.8), (2.0, 5, 2.0)),
        ("Small upper arris nick", (10.8, 149, -8.8), (1.1, 2.5, 1.1)),
        ("Buried corner fracture", (-10.8, -22, 8.8), (2.2, 9, 2.2)),
    ]:
        subtract(obj, box(name, center, size, "core"))
    bpy.context.view_layer.update()
    corners = [obj.matrix_world @ Vector(v) for v in obj.bound_box]
    low = [min(p[i] for p in corners) for i in range(3)]
    high = [max(p[i] for p in corners) for i in range(3)]
    metadata = {
        "name": "Obelisk v2", "reference": "https://www.instagram.com/p/Da0NEq7kUAO/",
        "reference_credit": "Josh White / Painted Desert", "source_bounds_blender": [low, high],
        "height_target_blocks": 209, "scale_is_estimate": True,
        "ground_level_source": 0, "ground_level_nbt_approx": 32,
        "visible_height_source": 176, "shaft_width_source": [22, 22], "shaft_depth_source": [18, 18],
        "buried_base": {"depth_source": 32, "type": "Continuous stele shaft, not an exposed stepped pedestal"},
        "solid_core": True,
        "basis": "Flat crown, near-parallel tall faces; visible height/projected width about 7:1. No reliable absolute scale in the artwork.",
        "interpretation": "Warm mineral faces and restrained horizontal weathering; sunward face lighter. Hidden sides and buried foot inferred.",
    }
    (OUT / "obelisk-v2.design.json").write_text(json.dumps(metadata, indent=2)+"\n")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.wm.obj_export(filepath=str(OUT / "obelisk-v2.obj"), forward_axis="NEGATIVE_Z", up_axis="Y",
                          export_selected_objects=True, export_triangulated_mesh=True, export_materials=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene["design_name"] = "Obelisk v2"
    scene["reference_url"] = metadata["reference"]
    scene["scale_note"] = "176 source units above ground + 32 below; height is an artistic estimate."
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "obelisk-v2-source.blend"))
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
