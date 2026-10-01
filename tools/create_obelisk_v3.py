"""Build Obelisk v3: a tapered square antiprism with a shallow buried foot.

Minecraft XYZ, front -Z. Ground Y0, bottom Y-8, flat crown Y176.
The top square is rotated 45 degrees and has 67% of the base edge length.
"""
import json
import math
from pathlib import Path
import sys

import bmesh
import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from create_blender_colossus import xyz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "design/generated/obelisk-v3"
COLORS = {"stone": "987344", "facet": "805b40", "sunward": "c3a570", "core": "b69c6a"}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    vertices = []
    for y, side, twist in [(-8, 24, 0), (176, 24*.67, 45)]:
        radius = side/math.sqrt(2)
        for i in range(4):
            angle = math.radians(-135+90*i+twist)
            vertices.append(xyz((radius*math.cos(angle), y, radius*math.sin(angle))))
    faces, materials = [], []
    for i in range(4):
        j = (i+1)%4
        # Every lateral face is one real plane, not a diagonal on a box wall.
        faces.extend([(i, j, 4+i), (j, 4+j, 4+i)])
        materials.extend(["stone", "sunward" if i == 3 else "facet"])
    faces.extend([(3, 2, 1, 0), (4, 5, 6, 7)])
    materials.extend(["core", "sunward"])
    mesh = bpy.data.meshes.new("Eight planar antiprism facets and two square caps")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("Obelisk v3 | tapered square antiprism", mesh)
    bpy.context.collection.objects.link(obj)
    for name, color in COLORS.items():
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = (*[int(color[i:i+2], 16)/255 for i in (0, 2, 4)], 1)
        mesh.materials.append(mat)
    for polygon, name in zip(mesh.polygons, materials):
        polygon.material_index = list(COLORS).index(name)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    assert all(edge.is_manifold for edge in bm.edges), "Antiprism must be closed"
    volume = bm.calc_volume(signed=True)
    assert volume > 0, "Normals must face outwards"
    assert len(bm.verts) == 8 and len(bm.faces) == 10
    assert sum(len(face.verts) == 3 for face in bm.faces) == 8
    bm.to_mesh(mesh)
    bm.free()
    bpy.context.view_layer.update()
    corners = [obj.matrix_world @ Vector(v) for v in obj.bound_box]
    low = [min(p[i] for p in corners) for i in range(3)]
    high = [max(p[i] for p in corners) for i in range(3)]
    metadata = {
        "name": "Obelisk v3", "reference": "https://www.instagram.com/p/Da0NEq7kUAO/",
        "reference_credit": "Josh White / Painted Desert; user-provided antiprism diagrams",
        "source_bounds_blender": [low, high], "height_target_blocks": 185,
        "ground_level_source": 0, "ground_level_nbt_approx": 8,
        "visible_height_source": 176, "scale_is_estimate": True, "solid_core": True,
        "buried_base": {"depth_source": 8, "type": "Short continuation of the antiprism"},
        "antiprism": {"sides": 4, "twist_degrees": 45, "base_edge_source": 24,
                      "top_edge_source": 24*.67, "top_edge_ratio": .67,
                      "lateral_triangles": 8, "closed_manifold": True, "source_volume": volume},
        "interpretation": "Eight long planar triangles between rotated square caps; shallow burial; no rectangular shaft.",
    }
    (OUT / "obelisk-v3.design.json").write_text(json.dumps(metadata, indent=2)+"\n", encoding="utf-8")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.wm.obj_export(filepath=str(OUT / "obelisk-v3.obj"), forward_axis="NEGATIVE_Z", up_axis="Y",
                          export_selected_objects=True, export_triangulated_mesh=True, export_materials=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene["design_name"] = "Obelisk v3"
    scene["reference_url"] = metadata["reference"]
    scene["scale_note"] = "176 units above ground, only 8 below. Square top rotated 45 degrees; edge ratio 0.67."
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "obelisk-v3-source.blend"))
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
