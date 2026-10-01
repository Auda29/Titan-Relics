"""Build an editable first Blender concept and triangulated OBJ for ObjToSchematic.

blender --background --python tools/create_blender_colossus.py
Design coordinates are Minecraft XYZ, front -Z; Blender uses (X, -Z, Y).
This is a form/material study, not a finished worldgen structure.
"""
import math
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "relics/colossus/design/generated/ots"
COLORS = {
    "armor": "4b5053", "trim": "33383c", "broken": "575b5e",
    "joint": "606568", "dark": "15191f", "copper": "518c79",
    "moss": "657d35", "earth": "75604a", "wood": "ac8855",
}


def xyz(pos):
    x, y, z = pos
    return x, -z, y


def apply(obj, modifier):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=modifier.name)


def finish(obj, name, material):
    obj.name = name
    obj.data.materials.append(bpy.data.materials[material])
    return obj


def box(name, center, size, material="armor", bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=xyz(center))
    obj = bpy.context.object
    obj.scale = (size[0], size[2], size[1])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new("Broad worn bevel", "BEVEL")
        mod.width, mod.segments = bevel, 1
        apply(obj, mod)
    return finish(obj, name, material)


def ellipsoid(name, center, radius, material="armor"):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, location=xyz(center))
    obj = bpy.context.object
    obj.scale = (radius[0], radius[2], radius[1])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(obj, name, material)


def cylinder(name, a, b, radius, material="joint", vertices=16):
    start, end = Vector(xyz(a)), Vector(xyz(b))
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius,
                                      depth=(end-start).length, location=(start+end)/2)
    obj = bpy.context.object
    obj.rotation_euler = (end-start).to_track_quat("Z", "Y").to_euler()
    return finish(obj, name, material)


def subtract(obj, cutter):
    mod = obj.modifiers.new("Designed opening", "BOOLEAN")
    mod.operation, mod.solver, mod.object = "DIFFERENCE", "EXACT", cutter
    apply(obj, mod)
    bpy.data.objects.remove(cutter, do_unlink=True)


def ring(name, center, radius, tube, material, start=0, end=360):
    # Faceted tube around a ring in the Minecraft XY plane; front faces -Z.
    vertices, faces = [], []
    segments = max(4, round((end-start)/8))
    for i in range(segments+1):
        angle = math.radians(start+(end-start)*i/segments)
        for j in range(8):
            t = math.tau*j/8
            r = radius+tube*math.cos(t)
            vertices.append(xyz((center[0]+r*math.cos(angle),
                                 center[1]+r*math.sin(angle), center[2]+tube*math.sin(t))))
    for i in range(segments):
        for j in range(8):
            a, b = i*8+j, i*8+(j+1)%8
            faces.append((a, b, b+8, a+8))
    faces.extend([tuple(reversed(range(8))), tuple(segments*8+j for j in range(8))])
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return finish(obj, name, material)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for name, color in COLORS.items():
        mat = bpy.data.materials.new(name)
        rgb = [int(color[i:i+2], 16)/255 for i in (0, 2, 4)]
        mat.diffuse_color = (*rgb, 1)
    # A broad sunken chest, deliberately hollow, with a torn circular aperture.
    chest = ellipsoid("01 | Hollow armoured torso", (0, 26, 0), (23, 23, 17))
    subtract(chest, ellipsoid("Room cutter", (0, 26, 0), (18, 18, 12)))
    subtract(chest, cylinder("Chest aperture", (0, 27, -24), (0, 27, 0), 11))
    subtract(chest, box("Accessible doorway", (0, 13, -14), (9, 12, 24)))
    subtract(chest, box("Upper daylight fracture", (12, 41, -9), (6, 18, 13)))
    box("02 | Chamber floor", (0, 8.5, 0), (31, 3, 24), "broken", 1)
    box("03 | Entrance apron", (0, 8, -20), (7, 2, 16), "broken", .6)
    for x in (-15, 15):
        cylinder("Internal structural rib", (x, 10, 5), (x, 34, 5), 1.5)
    ring("Dormant inner mechanism", (0, 22, 10), 8, 1.2, "joint", 10, 345)
    ring("Broken chest lip", (0, 27, -15), 12, 1.3, "trim", 32, 306)
    ring("Restrained oxidised inlay", (0, 27, -16.2), 12, .55, "copper", 45, 165)
    ring("Oxidised lower fragment", (0, 27, -16.2), 12, .55, "copper", 198, 262)
    # Shoulders have different states; the attached arm carries weight into earth.
    ellipsoid("Left layered pauldron", (-25, 37, 0), (13, 10, 14), "trim")
    ellipsoid("Left shoulder armour", (-27, 39, -1), (11, 8, 12))
    cylinder("Weight bearing upper arm", (-30, 31, 1), (-33, 15, -1), 7)
    ellipsoid("Grounded left forearm", (-33, 10, -5), (9, 10, 12))
    box("Left resting knuckles", (-32, 4, -14), (16, 7, 12), "trim", 2)
    ellipsoid("Broken right socket", (25, 36, 0), (9, 9, 11), "broken")
    cylinder("Exposed right shoulder axle", (26, 36, 0), (33, 35, 0), 5, "joint")
    # Low neck and an angular helmet with a recessed, unlit visor.
    cylinder("Neck collar", (0, 43, 1), (0, 49, 1), 9, "joint")
    head = box("04 | Bevelled helmet", (-1, 56, 1), (24, 20, 22), "armor", 4)
    subtract(head, box("Visor cut", (-1, 55, -10), (20, 4, 8)))
    subtract(head, box("Missing helmet corner", (9, 64, -8), (8, 8, 12)))
    box("Deep unlit visor", (-1, 55, -6.7), (19, 3, 1), "dark")
    box("Heavy brow", (-2, 58, -10), (25, 3, 5), "trim", .8)
    box("Central face guard", (-1, 51.5, -10), (5, 7, 5), "trim", 1)
    box("Left cheek plate", (-8, 50.5, -8), (5, 6, 5), "trim", 1)
    # The detached right arm is a single designed assembly, in the same frame.
    cylinder("05 | Severed elbow ring", (46, 10, -4), (46, 10, 2), 7, "joint")
    ellipsoid("Detached forearm", (46, 8, 13), (8, 7, 16))
    box("Detached forearm inset", (46, 13, 13), (8, 2, 20), "trim", .5)
    box("Detached palm", (46, 5, 29), (17, 8, 12), "armor", 2)
    for i in range(4):
        x = 39.5+i*4.3
        box(f"Separate finger {i+1}", (x, 3, 38-(i%2)), (2.8, 5, 12-(i%2)*2), "trim", .7)
    thumb = box("Detached thumb", (36, 4, 28), (5, 5, 10), "trim", 1)
    thumb.rotation_euler.z = math.radians(-28)
    # Vegetation follows upper surfaces, leaving broad armour fields readable.
    ellipsoid("Moss on sheltered shoulder", (-29, 45, 0), (8, 2, 8), "moss")
    ellipsoid("Moss in elbow hollow", (-36, 18, -2), (4, 2, 5), "moss")
    ellipsoid("Moss on fallen wrist", (48, 13, 24), (5, 1.5, 4), "moss")
    for i in range(3):
        cylinder("Trailing shoulder growth", (-33+i*3, 44-i, -9),
                 (-34+i*3, 35-i*3, -11), .7, "moss", 6)
    # Small human-scale intervention in one protected corner of the room.
    box("Later wooden shelter roof", (-10, 15, 3), (7, 1, 7), "wood")
    for x in (-13, -7):
        cylinder("Later shelter post", (x, 10, 0), (x, 15, 0), .45, "wood", 6)
    for i, (x, z, r) in enumerate([(-20, -17, 4), (21, -12, 3), (30, 15, 4), (36, -9, 2)]):
        rock = box(f"Fallen armour fragment {i}", (x, r/2, z), (r*2, r, r*1.6), "broken", .8)
        rock.rotation_euler.z = i*.6
    # Thin ground drifts join the heavy body to the future terrain.
    for x, z, rx, rz in [(-20, 6, 19, 15), (13, 6, 16, 15), (47, 15, 11, 20)]:
        mound = ellipsoid("Accumulated earth", (x, 0, z), (rx, 5, rz), "earth")
        subtract(mound, box("Below ground cutter", (x, -10, z), (rx*3, 20, rz*3)))
    bpy.ops.object.select_all(action="SELECT")
    # Export before adding presentation objects. OBJ and blend contain identical meshes.
    bpy.ops.wm.obj_export(filepath=str(OUT / "colossus.obj"),
                          forward_axis="NEGATIVE_Z", up_axis="Y",
                          export_selected_objects=True, export_triangulated_mesh=True,
                          export_materials=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1
    scene["design_note"] = "ObjToSchematic form study; 1 Blender unit approximately 1 Minecraft block. Front Blender +Y."
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "colossus-source.blend"))
    print(f"Editable source and OBJ written to {OUT}")


if __name__ == "__main__":
    main()
