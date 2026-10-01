"""Titan Skull v1 after the opening D.E.A.D. reference: organic crown and open jaw.

Blender background generator. Source coordinates are Minecraft XYZ, front -Z.
"""
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from create_blender_colossus import xyz, apply, subtract, box, finish

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "relics/titan-skull/design/generated/titan-skull-v1"
COLORS = {"bone": "a99470", "worn": "c5b18c", "mineral": "81755e",
          "earth": "66513d", "moss": "566345", "root": "706044"}


def organic(name, center, radius, mat="bone", rough=1):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=40, location=xyz(center))
    obj = bpy.context.object
    for vertex in obj.data.vertices:
        v = vertex.co.copy()
        ripple = rough*(.55*math.sin(v.x*14+v.y*5)+.3*math.sin(v.z*21-v.x*9))
        vertex.co = Vector((v.x*(radius[0]+ripple), v.y*(radius[2]+ripple), v.z*(radius[1]+ripple)))
    return finish(obj, name, mat)


def tube(name, points, radii, material="bone", sides=12):
    verts, faces = [], []
    coords = [Vector(xyz(p)) for p in points]
    for i, (p, r) in enumerate(zip(coords, radii)):
        tangent = (coords[min(i+1, len(coords)-1)]-coords[max(0, i-1)]).normalized()
        u = tangent.cross(Vector((0, 1, 0))).normalized()
        if u.length < .1:
            u = tangent.cross(Vector((1, 0, 0))).normalized()
        v = tangent.cross(u).normalized()
        for j in range(sides):
            a = math.tau*j/sides
            verts.append(p+r*(math.cos(a)*u+math.sin(a)*v))
    for i in range(len(coords)-1):
        for j in range(sides):
            a, b = i*sides+j, i*sides+(j+1)%sides
            faces.append((a, b, b+sides, a+sides))
    faces.extend([tuple(reversed(range(sides))), tuple((len(coords)-1)*sides+j for j in range(sides))])
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return finish(obj, name, material)


def unite(obj, other):
    mod = obj.modifiers.new("Continuous fossil mass", "BOOLEAN")
    mod.operation, mod.solver, mod.object = "UNION", "EXACT", other
    apply(obj, mod)
    bpy.data.objects.remove(other, do_unlink=True)


def nose_cutter():
    vertices = [xyz((x, y, z)) for z in (-75, 12) for x, y in [(-11, 91), (11, 91), (0, 119)]]
    mesh = bpy.data.meshes.new("Triangular nasal aperture")
    mesh.from_pydata(vertices, [], [(0, 2, 1), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)])
    mesh.update()
    obj = bpy.data.objects.new("Nasal cutter", mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def main(export=True):
    OUT.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for name, color in COLORS.items():
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = (*[int(color[i:i+2], 16)/255 for i in (0, 2, 4)], 1)
    skull = organic("01 | Weathered cranium and open mandible", (0, 102, 6), (53, 54, 40), rough=1.2)
    unite(skull, organic("Maxilla", (0, 83, -18), (39, 22, 30), rough=.8))
    unite(skull, organic("Long open lower jaw", (0, 32, -8), (40, 44, 33), rough=.8))
    # Connected inner cavities; cuts are geometric holes, never black face inserts.
    subtract(skull, organic("Cranial interior", (0, 103, 7), (43, 44, 31), rough=.35))
    subtract(skull, organic("Oral chamber", (0, 39, -6), (31, 49, 26), rough=.2))
    subtract(skull, organic("Tall open mouth", (0, 45, -35), (29, 36, 40), rough=.2))
    for x, y in [(-25, 111), (25, 108)]:
        cutter = organic("Deep eye socket", (x, y, -29), (21, 17, 30), rough=.7)
        cutter.rotation_euler.y = math.radians(-8 if x < 0 else 10)
        subtract(skull, cutter)
    subtract(skull, nose_cutter())
    # Uneven fracture exposing the back of the cranial vault.
    subtract(skull, tube("Rear vault fracture", [(25, 133, 33), (31, 143, 30), (37, 151, 20)], [2.1, 2.8, 1.2], sides=7))
    for x, y, z in [(-17, 143, -22), (13, 136, -31), (-41, 94, -28)]:
        fissure = box("Local erosion incision", (x, y, z), (15, 1.2, 9), "mineral")
        fissure.rotation_euler.y = math.radians(18)
        subtract(skull, fissure)
    # Major cheek arches and long jaw rails follow the reference's open silhouette.
    for s in (-1, 1):
        tube("02 | Sweeping cheekbone", [(s*8, 90, -39), (s*24, 90, -42), (s*43, 86, -30), (s*49, 82, -13)],
             [5, 6, 7, 8])
        tube("03 | Long exposed mandibular rail", [(s*38, 82, -26), (s*32, 61, -34), (s*32, 35, -36), (s*30, 10, -35), (s*25, -5, -20)],
             [5.2, 4, 4.5, 6, 7], "worn")
        # A thin orbital crest; separated from the inner socket opening.
        tube("Supraorbital ridge", [(s*7, 122, -29), (s*20, 129, -31), (s*34, 124, -26), (s*43, 113, -22)],
             [3, 3.5, 3, 2.5])
        for k in range(3):
            tube("Temporal bone strut", [(s*(46+k), 80-k*3, -10+k*6), (s*(41+k), 60-k*3, -5+k*6),
                                          (s*(36+k), 34-k*4, 0+k*6)], [2, 1.4, 3], "mineral", 8)
    # Sparse irregular teeth hang from the upper arch, not a decorative full grin.
    for i, x in enumerate([-22, -15, -7, 2, 10, 18, 24]):
        y = 78-abs(x)*.25
        length = [8, 11, 9, 7, 10, 13, 6][i]
        tube("Worn upper tooth", [(x, y+5, -40), (x*.98, y-length*.5, -43), (x*.96, y-length, -41)],
             [4.3, 3.3, 2.4], "worn", 7)
    for i, x in enumerate([-22, -13, -3, 8, 18]):
        tube("Broken lower tooth", [(x, 8, -30), (x, 15+(i%3)*2, -33)], [4, 2.6], "worn", 7)
    # Crown is made of fossil outgrowths grown into the vault, with unequal tips.
    crown = [(-43, 134, -3, -51, 161), (-31, 145, -9, -36, 175),
             (-12, 152, -8, -9, 190), (11, 151, -4, 18, 185),
             (31, 144, 0, 44, 173), (44, 130, 9, 56, 163),
             (-21, 145, 25, -23, 169)]
    for i, (x, y, z, tx, ty) in enumerate(crown):
        ty -= 10
        tube(f"04 | Organic crown prong {i+1}", [(x, y-6, z), (x, y+8, z), ((x+tx)/2, ty-7, z+2), (tx, ty, z+4)],
             [9, 6, 3.3, .7 if i != 4 else 2.8], "bone", 14)
    # The opening shot has a prominent backward-curving lateral spur.
    tube("05 | Tall lateral occipital spur", [(43, 34, 18), (62, 40, 22), (81, 58, 23), (92, 79, 19), (92, 94, 14)],
         [16, 13, 8, 3, .6], "bone", 18)
    tube("Broken opposite spur", [(-42, 31, 17), (-60, 38, 23), (-72, 49, 24)], [15, 10, 5], "mineral", 14)
    for x, z, rx in [(-48, 12, 33), (45, 21, 35), (-61, -8, 17)]:
        organic("Buried basal bone remnant", (x, 1, z), (rx, 12, 28), "mineral", .8)
    # Fuse adjoining anatomical pieces into one eroded fossil instead of leaving
    # cylinder joints around the crown, cheekbones, and jaw. Preserve open cavities.
    bpy.ops.object.select_all(action="SELECT")
    bpy.context.view_layer.objects.active = skull
    bpy.ops.object.join()
    remesh = skull.modifiers.new("Continuous fossil surface", "REMESH")
    remesh.mode, remesh.voxel_size = "VOXEL", .9
    apply(skull, remesh)
    smooth = skull.modifiers.new("Soft eroded bone transitions", "SMOOTH")
    smooth.factor, smooth.iterations = .8, 4
    apply(skull, smooth)
    decimate = skull.modifiers.new("Retain large fossil planes", "DECIMATE")
    decimate.ratio = .24
    apply(skull, decimate)
    skull.data.materials.clear()
    for name in ("bone", "worn", "mineral", "earth"):
        skull.data.materials.append(bpy.data.materials[name])
    # Limited surface staining, with broad quiet mineral fields retained.
    for obj in list(bpy.context.scene.objects):
        if obj.type != "MESH":
            continue
        for vertex in obj.data.vertices:
            world = obj.matrix_world @ vertex.co
            if world.z < -12:
                world.z = -12
                vertex.co = obj.matrix_world.inverted() @ world
        if obj == skull:
            for face in obj.data.polygons:
                p = obj.matrix_world @ face.center
                value = math.sin(p.x*.13+p.z*.11)+.6*math.sin(p.y*.19-p.z*.07)
                face.material_index = 0
                if value > 1.25:
                    face.material_index = 1
                elif value < -1.25:
                    face.material_index = 2
    for x, y, z, rx, rz in [(-32, 147, 2, 9, 8), (18, 151, 9, 10, 7), (-46, 90, -18, 6, 5),
                              (45, 37, 29, 10, 7), (-54, 11, 2, 12, 10), (52, 11, 28, 11, 12)]:
        organic("Sheltered moss pocket", (x, y, z), (rx, 1.3, rz), "moss", .3)
    bpy.context.view_layer.update()
    objects = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    corners = [o.matrix_world @ Vector(v) for o in objects for v in o.bound_box]
    low = [min(p[i] for p in corners) for i in range(3)]
    high = [max(p[i] for p in corners) for i in range(3)]
    scale = 202/(high[2]-low[2])
    metadata = {"name": "Titan Skull v1", "reference": "https://www.instagram.com/reel/DXM3J4sgqJl/",
                "reference_seconds": [0, 5], "source_bounds_blender": [low, high], "height_target_blocks": 203,
                "ground_level_source": 0, "ground_level_nbt_approx": round(-low[2]*scale),
                "blocks_per_source_unit": scale, "scale_is_estimate": True,
                "interpretation": "Crowned fossil skull, deep real sockets, triangular nose, long open jaw and lateral spur. Back and buried base inferred.",
                "air_policy": "omit; geometric chambers do not yet clear terrain during placement",
                "cavity_probes_source": [[0, 42, -50], [0, 42, -25], [0, 42, 0], [-25, 110, -32], [25, 108, -32], [0, 102, -35]]}
    if not export:
        return metadata
    (OUT / "titan-skull-v1.design.json").write_text(json.dumps(metadata, indent=2)+"\n", encoding="utf-8")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.wm.obj_export(filepath=str(OUT / "titan-skull-v1.obj"), forward_axis="NEGATIVE_Z", up_axis="Y",
                          export_selected_objects=True, export_triangulated_mesh=True, export_materials=True)
    bpy.context.scene["design_name"] = "Titan Skull v1"
    bpy.context.scene["reference_url"] = metadata["reference"]
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "titan-skull-v1-source.blend"))
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
