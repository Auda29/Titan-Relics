"""Derive two V4 studies from the checked-in V3 Blender source without rewriting V3.

Blender --background --python-exit-code 1 --python tools/create_colossus_v4.py
MC source coordinates: front -Z, anatomical right +X, up +Y.
"""
import copy
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import create_colossus_v3 as shapes
from create_blender_colossus import xyz, box, cylinder, subtract, apply

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "relics/colossus/design"
BASE = DESIGN / "generated/colossus-v3"
SOURCE = BASE / "colossus-v3-source.blend"


def fingerprint(obj):
    data = {
        "matrix": [list(row) for row in obj.matrix_world],
        "vertices": [list(v.co) for v in obj.data.vertices],
        "faces": [(list(p.vertices), p.material_index) for p in obj.data.polygons],
        "materials": [m.name for m in obj.data.materials],
    }
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def bounds(objects):
    points = [o.matrix_world @ Vector(p) for o in objects for p in o.bound_box]
    return [[min(p[i] for p in points) for i in range(3)],
            [max(p[i] for p in points) for i in range(3)]]


def old_hand(obj):
    return obj.name.startswith(("07 | Half-buried mechanical palm", "Finger ", "Detached hand thumb"))


def raised_right_hand():
    for obj in list(bpy.context.scene.objects):
        if old_hand(obj):
            bpy.data.objects.remove(obj, do_unlink=True)
    a, b = Vector((48, 19, -88)), Vector((-10, 17, -144))
    axis = (b-a).normalized()
    # Orthogonal up, rather than global up, keeps the basis a proper rotation.
    up = (Vector((0, 1, 0))-axis*axis.y).normalized()
    side = axis.cross(up).normalized()
    thumbward = -side  # V3's thumb is on this side of its palm-down right hand.
    theta = math.radians(64)
    distal = axis*math.cos(theta)+up*math.sin(theta)
    palmar = axis*math.sin(theta)-up*math.cos(theta)
    basis = Matrix((thumbward, distal, palmar)).transposed()
    assert abs(basis.determinant()-1) < 1e-5, "Hand must never be mirrored"
    assert thumbward.cross(distal).dot(palmar) > .999, "Right-hand chirality lost"
    wrist = b+axis*8
    before = set(bpy.context.scene.objects)
    # Local u points toward the thumb, v toward fingertips, w out of the palm.
    palm = box("V4 right hand | tapered palm armour", (0, 11, 0), (32, 23, 10), "plate", 3)
    shapes.weather(palm, "plate")
    box("V4 right hand | recessed palm plate", (0, 11, 5.1), (22, 15, 1.4), "joint", 1)
    for u in (-10, 0, 10):
        box("V4 right hand | palm load rib", (u, 10, 6), (1.5, 15, 1.5), "edge", .4)
    cylinder("V4 right hand | wrist hinge", (-15, 1, 0), (15, 1, 0), 4, "joint", 20)
    for u in (-15, 15):
        shapes.ellipsoid("V4 right hand | wrist bearing", (u, 1, 0), (3.3, 4.6, 4.6), "edge", 20, 12)
    digits = []
    # Small finger -> ring -> middle -> index, ending next to the thumb (+u).
    for name, u, length, curl in [("little", -13.5, 20, 8), ("ring", -4.5, 27, 6),
                                  ("middle", 4.5, 30, 5), ("index", 13.5, 25, 9)]:
        points = [(u, 22, 0), (u, 22+length*.48, 0),
                  (u, 22+length*.81, curl*.4), (u, 22+length, curl)]
        for i, (start, end) in enumerate(zip(points, points[1:])):
            cylinder(f"V4 right hand | {name} phalanx {i+1}", start, end, 2.9-i*.2, "plate" if i != 1 else "armor", 12)
        for p in points[:-1]:
            shapes.ellipsoid(f"V4 right hand | {name} knuckle", p, (3.1, 3, 3.1), "joint", 16, 10)
            shapes.arc(f"V4 right hand | {name} knuckle rim", p, (1, 0, 0), 3.2, .6, "edge", 20, 325)
        shapes.ellipsoid(f"V4 right hand | {name} tip", points[-1], (2.5, 2.7, 2.5), "armor", 16, 10)
        shapes.tube(f"V4 right hand | {name} dorsal tendon", [(u, 5, -5.5), (u, 19, -5.5), (u, 28, -3.1)], .75, "joint", 8)
        digits.append({"name": name, "tip_local": points[-1], "root_local": points[0]})
    thumb = [(14, 6, 0), (23, 12, 1), (29, 23, 5)]
    for i, (start, end) in enumerate(zip(thumb, thumb[1:])):
        cylinder(f"V4 right hand | thumb phalanx {i+1}", start, end, 3.6-i*.5, "plate", 14)
    for p in thumb:
        shapes.ellipsoid("V4 right hand | thumb joint", p, (3.6, 3.6, 3.6), "armor", 20, 12)
    # Apply one rigid, determinant-positive transform to all newly modeled parts.
    change = Matrix(((1, 0, 0), (0, 0, -1), (0, 1, 0)))
    transform = Matrix.Translation(Vector(xyz(wrist))) @ (change @ basis @ change.inverted()).to_4x4()
    for obj in set(bpy.context.scene.objects)-before:
        obj.matrix_world = transform @ obj.matrix_world
        obj["asset_component"] = "right_hand"
        obj["anatomical_side"] = "right"
    def world(p):
        return list(wrist+basis @ Vector(p))
    for digit in digits:
        digit["tip_source"] = world(digit.pop("tip_local"))
        digit["root_source"] = world(digit.pop("root_local"))
    return {
        "side": "right", "source_body_right": [1, 0, 0], "source_body_front": [0, 0, -1],
        "pose": "64-degree wrist extension from the original palm-down hand; forearm unchanged",
        "basis_determinant": basis.determinant(), "thumbward_source": list(thumbward),
        "distal_source": list(distal), "palmar_normal_source": list(palmar),
        "wrist_source": list(wrist), "thumb_tip_source": world(thumb[-1]), "digits": digits,
        "finger_gap_probes_source": [world((u, 38, 1)) for u in (-9, 0, 9)],
        "note": "T cross D = P. Same thumb side as V3; no reflection or negative scale.",
    }


def damage_back():
    shapes.RNG.seed(20261002)
    cuts = [
        ("01 | Broad bronze cuirass", (10, 61, 44), (20, 24), 32),
        ("01 | Broad bronze cuirass", (-25, 37, 47), (9, 16), 25),
        ("02 | Monumental torn pauldron", (-61, 54, 42), (14, 18), 30),
    ]
    for name, center, radii, depth in cuts:
        obj = bpy.data.objects[name]
        cutter = shapes.jagged_cutter("V4 rear-only armour breach", center, radii, depth)
        cutter.data.materials.append(bpy.data.materials["worn"])
        subtract(obj, cutter)
        # Re-cut small trim crossing this region so no unbroken seam spans a hole.
        for trim in list(bpy.context.scene.objects):
            if trim.name.startswith(("Cuirass /", "Pauldron curved plate seam")):
                cutter = shapes.jagged_cutter("V4 interrupted trim", center, (radii[0]*.82, radii[1]*.82), depth)
                cutter.data.materials.append(bpy.data.materials["rust"])
                subtract(trim, cutter)
    # Unequal, bent rear ribs are visible through the armour, not a filled backing.
    for x, end in [(-5, 72), (9, 80), (24, 65)]:
        shapes.tube("V4 rear | exposed bent structural rib", [(x, 30, 33), (x-2, 48, 36), (x+3, end, 30)], 1.9, "joint", 10)
        cylinder("V4 rear | bronze rib sleeve", (x-1, 45, 35), (x, 53, 34), 2.4, "plate", 12)
    shapes.tube("V4 rear | fractured diagonal brace", [(-12, 69, 30), (3, 61, 34), (17, 54, 35)], 1.8, "edge", 10)
    for x, bottom in [(1, 35), (15, 43)]:
        shapes.tube("V4 rear | severed hanging conduit", shapes.catmull([(x, 76, 29), (x+4, 61, 33),
                    (x-2, bottom, 35), (x+2, bottom-3, 38)]), 1.1, "rust", 8)
    for x in (-67, -56):
        cylinder("V4 rear | shoulder lattice", (x, 29, 31), (x+3, 70, 29), 1.6, "joint", 10)
    # Torn outward plate lips emphasize wall thickness without changing the outline.
    for vertices in [[(-9, 78, 32), (1, 85, 29), (9, 82, 32), (1, 76, 41)],
                     [(25, 65, 42), (31, 58, 44), (30, 48, 46), (24, 54, 53)],
                     [(-75, 59, 34), (-69, 69, 33), (-64, 68, 34), (-69, 57, 44)]]:
        mesh = bpy.data.meshes.new("Torn rear plate lip")
        mesh.from_pydata([xyz(p) for p in vertices], [], [(0, 1, 2, 3)])
        mesh.update()
        obj = bpy.data.objects.new("V4 rear | lifted broken plate edge", mesh)
        bpy.context.collection.objects.link(obj)
        mesh.materials.append(bpy.data.materials["plate"])
        mod = obj.modifiers.new("Visible broken metal thickness", "SOLIDIFY")
        mod.thickness = 1.6
        apply(obj, mod)
    return {"breaches": [{"object": n, "center_source": list(c), "radii": list(r), "depth": d}
                         for n, c, r, d in cuts],
            "empty_probes_source": [[18, 69, 45], [-27, 40, 53], [-61, 57, 45]]}


def chest_variant(variant):
    # The plain piston exposed in V3's low front chest tear. Neck well is retained.
    bpy.data.objects.remove(bpy.data.objects["Buried chest piston"], do_unlink=True)
    if variant == "frame":
        for y, r, start, end in [(6, 12, 10, 285), (19, 11, 35, 247), (30, 10, 125, 337)]:
            shapes.arc("V4 chest | broken open bearing", (24, y, -20), (0, 1, 0), r, 1.3, "plate", start, end)
        for angle, height in [(35, 31), (155, 25), (272, 29)]:
            a = math.radians(angle)
            x, z = 24+10*math.cos(a), -20+10*math.sin(a)
            shapes.tube("V4 chest | snapped machine support", [(x, 4, z), (x, 18, z), (x-2, height, z+1)], 1.4, "joint", 10)
        shapes.tube("V4 chest | disconnected copper line", [(17, 28, -15), (14, 21, -17), (17, 9, -17)], .9, "edge", 8)
    return {"variant": variant, "removed_object": "Buried chest piston",
            "original_center_source": [24, 17.5, -20], "original_radius_source": 13,
            "neck_well_retained": True, "empty_center_probe_source": [24, 25, -20],
            "selected_design": variant == "frame", "selection_date": "2026-10-02",
            "decision": "B / frame selected by the user for V4; A retained for comparison. Game build still selects V3."}


def build(variant):
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    baseline = {o.name: fingerprint(o) for o in bpy.context.scene.objects if o.type == "MESH"}
    hand = raised_right_hand()
    rear = damage_back()
    chest = chest_variant(variant)
    bpy.context.view_layer.update()
    changed = {"01 | Broad bronze cuirass", "02 | Monumental torn pauldron", "Buried chest piston"}
    preserved = {}
    for name, digest in baseline.items():
        if name in changed or name.startswith(("07 |", "Finger ", "Detached hand thumb", "Cuirass /", "Pauldron curved plate seam")):
            continue
        assert name in bpy.data.objects and fingerprint(bpy.data.objects[name]) == digest, f"Unexpected modification: {name}"
        preserved[name] = digest
    stem = f"colossus-v4-{variant}"
    out = DESIGN / "generated" / stem
    out.mkdir(parents=True, exist_ok=True)
    metadata = copy.deepcopy(json.loads((BASE / "colossus-v3.design.json").read_text()))
    low, high = bounds([o for o in bpy.context.scene.objects if o.type == "MESH"])
    scale = 208/(high[2]-low[2])
    assert abs(scale-metadata["blocks_per_source_unit"]) < 1e-6, "Accepted body scale must stay fixed"
    metadata.update(name=f"Colossus V4 / {variant}", source_bounds_blender=[low, high],
                    right_hand=hand, rear_damage=rear, chest_study=chest,
                    source_v3_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                    preserved_v3_objects=preserved, in_game_tested=False)
    (out / f"{stem}.design.json").write_text(json.dumps(metadata, indent=2)+"\n", encoding="utf-8")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.wm.obj_export(filepath=str(out / f"{stem}.obj"), forward_axis="NEGATIVE_Z", up_axis="Y",
                          export_selected_objects=True, export_triangulated_mesh=True, export_materials=True)
    bpy.context.scene["design_name"] = metadata["name"]
    bpy.context.scene["right_hand_note"] = hand["note"]
    bpy.ops.wm.save_as_mainfile(filepath=str(out / f"{stem}-source.blend"))
    print(f"{stem}: {len(preserved)} V3 meshes preserved, hand determinant {hand['basis_determinant']:.6f}, bounds {low}, {high}")


if __name__ == "__main__":
    for candidate in ("open", "frame"):
        build(candidate)
