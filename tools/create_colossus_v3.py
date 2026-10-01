"""Colossus v3: reference-led bronze colossus with a buried, torn hip.

blender --background --python-exit-code 1 --python tools/create_colossus_v3.py
Reference: https://www.instagram.com/reel/DaoBxUEiBNa/
The above-ground scale is calibrated to the initial 160-block v2. The buried
waist adds height below it. Source coordinates: MC XYZ, front -Z.
"""
import json
import math
from pathlib import Path
import random
import sys

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from create_blender_colossus import xyz, box, cylinder, subtract, finish

ROOT = Path(__file__).resolve().parents[1]
VERSION = 3
STEM = "colossus-v3"
OUT = ROOT / "relics/colossus/design/generated" / STEM
RNG = random.Random(20261001)
COLORS = {
    "armor": "9b7953", "plate": "927152", "edge": "b48a58",
    "worn": "b8a187", "rust": "60442f", "patina": "53735a",
    "joint": "343c38", "dark": "10191a", "moss": "4d6034",
    "growth": "394b32", "earth": "68553c",
}


def ellipsoid(name, center, radius, material="armor", segments=48, rings=32):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=xyz(center))
    obj = bpy.context.object
    obj.scale = (radius[0], radius[2], radius[1])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(obj, name, material)


def tube(name, points, radius, material="edge", sides=10):
    points = [Vector(xyz(p)) for p in points]
    vertices, faces = [], []
    for i, p in enumerate(points):
        tangent = (points[min(i+1, len(points)-1)]-points[max(i-1, 0)]).normalized()
        helper = Vector((0, 0, 1)) if abs(tangent.z) < .92 else Vector((1, 0, 0))
        u = tangent.cross(helper).normalized()
        v = tangent.cross(u).normalized()
        for j in range(sides):
            angle = math.tau*j/sides
            vertices.append(p+radius*(u*math.cos(angle)+v*math.sin(angle)))
        if i:
            for j in range(sides):
                a, b = (i-1)*sides+j, (i-1)*sides+(j+1)%sides
                faces.append((a, b, b+sides, a+sides))
    faces.extend([tuple(reversed(range(sides))), tuple((len(points)-1)*sides+j for j in range(sides))])
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return finish(obj, name, material)


def arc(name, center, normal, radius, width, material="edge", start=0, end=360):
    normal = Vector(normal).normalized()
    u = normal.cross(Vector((0, 1, 0))).normalized()
    if u.length < .1:
        u = normal.cross(Vector((1, 0, 0))).normalized()
    v = normal.cross(u).normalized()
    count = max(8, int((end-start)/5))
    points = [Vector(center)+radius*(math.cos(math.radians(start+(end-start)*i/count))*u
                                     +math.sin(math.radians(start+(end-start)*i/count))*v)
              for i in range(count+1)]
    return tube(name, points, width, material)


def catmull(points, steps=7):
    p = [Vector(points[0])]+[Vector(v) for v in points]+[Vector(points[-1])]
    result = []
    for i in range(1, len(p)-2):
        a, b, c, d = p[i-1:i+3]
        for j in range(steps):
            t = j/steps
            result.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
    result.append(Vector(points[-1]))
    return result


def jagged_cutter(name, center, radii, depth):
    x, y, z = center
    n = 13
    outline = []
    for i in range(n):
        a = math.tau*i/n
        r = RNG.uniform(.72, 1.22)
        outline.append((x+math.cos(a)*r*radii[0], y+math.sin(a)*r*radii[1]))
    vertices = [xyz((px, py, z+dz)) for dz in (-depth/2, depth/2) for px, py in outline]
    faces = [tuple(reversed(range(n))), tuple(range(n, n*2))]
    faces += [(i, (i+1)%n, (i+1)%n+n, i+n) for i in range(n)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def weather(obj, base="armor"):
    names = [base, "plate", "rust", "patina", "worn"]
    obj.data.materials.clear()
    for name in names:
        obj.data.materials.append(bpy.data.materials[name])
    for face in obj.data.polygons:
        p = obj.matrix_world @ face.center
        x, y, z = p.x, p.z, -p.y
        n = math.sin(x*.09+z*.075)+.7*math.cos(y*.13-z*.06)+.35*math.sin(x*.31+y*.19)
        face.material_index = 3 if n > 1.45 else 2 if n < -1.45 else 4 if n > 1.17 else 1 if n < -.45 else 0


def sphere_point(center, radius, latitude, longitude, lift=.0):
    lat, lon = math.radians(latitude), math.radians(longitude)
    return (center[0]+(radius[0]+lift)*math.cos(lat)*math.sin(lon),
            center[1]+(radius[1]+lift)*math.sin(lat),
            center[2]-(radius[2]+lift)*math.cos(lat)*math.cos(lon))


def shell_seams(center, radius, latitudes, longitudes, name, min_latitude=-12):
    for lat in latitudes:
        points = [sphere_point(center, radius, lat, lon, .45) for lon in range(-150, 151, 4)]
        tube(name+" / horizontal panel joint", points, .45, "rust", 6)
    for lon in longitudes:
        points = [sphere_point(center, radius, lat, lon, .5) for lat in range(min_latitude, 79, 3)]
        tube(name+" / meridian panel joint", points, .48, "rust", 6)


def vegetation(center, radius, tracks, name):
    for longitude, low, high in tracks:
        for lat in range(low, high, 2):
            lon = longitude+8*math.sin(lat*.17)+RNG.uniform(-6, 6)
            p = sphere_point(center, radius, lat, lon, .5)
            r = RNG.uniform(3, 5.5)
            ellipsoid(name, p, (r, r*.85, r*.6), "moss" if RNG.random() > .4 else "growth", 12, 8)
            if RNG.random() < .4:
                q = sphere_point(center, radius, lat+1, lon+RNG.choice((-9, 9)), .3)
                ellipsoid(name+" / spreading edge", q, (r*.7, r*.6, r*.45), "growth", 10, 6)


def body():
    # Almost continuous, broad curved cuirass; the small low break replaces v1's
    # central round chest window. Shoulder mass dominates the lower silhouette.
    center, radius = (4, 36, 10), (62, 66, 46)
    chest = ellipsoid("01 | Broad bronze cuirass", center, radius)
    subtract(chest, ellipsoid("Hollow torso cutter", center, (55, 59, 39)))
    if VERSION >= 3:
        subtract(chest, box("Waist connection cutter", (0, -65, 0), (350, 110, 350)))
    else:
        subtract(chest, box("Buried part cutter", (0, -50, 0), (350, 100, 350)))
    subtract(chest, jagged_cutter("Low chest tear", (24, 25, -33), (22, 19), 38))
    weather(chest)
    shell_seams(center, radius, [10, 34, 58], [-105, -70, -35, 0, 35, 70, 105], "Cuirass")
    # Internal machinery is only visible through the torn, overgrown armour.
    for r in (16, 21, 26):
        arc("Rolled lower chest layers", (24, 24, -28), (0, 0, 1), r, 1.6, "joint", 12, 174)
    cylinder("Buried chest piston", (24, 4, -20), (24, 31, -20), 13, "plate", 40)
    box("Interior footing", (6, 11, 2), (57, 4, 43), "joint", 2)
    for x in (-35, -18, 0, 18, 35):
        cylinder("Deep internal rib", (x, 10, 14), (x*.72, 68, 12), 2.2, "joint")
    vegetation(center, radius, [(-30, 3, 65), (32, 10, 62), (65, 12, 62), (5, 58, 76)], "Cuirass ivy")
    # The near shoulder is a massive rounded shell, with a ragged missing lower cap.
    shoulder_center, shoulder_radius = (-57, 35, 9), (43, 56, 48)
    shoulder = ellipsoid("02 | Monumental torn pauldron", shoulder_center, shoulder_radius)
    subtract(shoulder, ellipsoid("Socket cavity", shoulder_center, (37, 49, 41)))
    subtract(shoulder, box("Pauldron buried part", (-57, -50, 0), (180, 100, 200)))
    subtract(shoulder, jagged_cutter("Irregular shoulder breach", (-70, 21, -27), (26, 34), 48))
    weather(shoulder, "plate")
    # Avoid uninterrupted seams across the absent plate by limiting their extent.
    for lon in (-50, -15, 25, 60):
        tube("Pauldron curved plate seam", [sphere_point(shoulder_center, shoulder_radius, lat, lon, .5)
                                           for lat in range(35, 83, 3)], .6, "rust", 6)
    for r in (17, 24, 31):
        arc("Exposed shoulder socket race", (-67, 23, -12), (0, 0, 1), r, 1.9, "joint", -15, 205)
    for i in range(6):
        x = -89+i*6
        cylinder("Torn pauldron interior strut", (x, 5, -12), (x+5, 41, -9), 1.7, "joint")
    vegetation(shoulder_center, shoulder_radius, [(-25, 36, 80), (42, 40, 72)], "Shoulder canopy growth")
    far = ellipsoid("Far buried shoulder", (61, 30, 17), (32, 47, 37), "plate")
    subtract(far, box("Far shoulder buried part", (60, -50, 10), (140, 100, 150)))
    weather(far, "plate")
    # Rolled neck opening is wide and low, like a heavy antique diving suit.
    cylinder("03 | Neck well", (0, 82, 0), (0, 99, 0), 34, "joint", 48)
    arc("Bronze rolled collar", (0, 91, 0), (0, 1, 0), 35, 2.1, "edge")
    arc("Inner neck collar", (0, 96, 0), (0, 1, 0), 31, 1.5, "plate")
    for i in range(32):
        a = i*math.tau/32
        r = RNG.uniform(2.8, 4.8)
        ellipsoid("Neck-well vegetation", (32*math.cos(a), 94+RNG.uniform(-1, 1), 30*math.sin(a)), (r, 1.8, r), "growth", 12, 8)


def helmet():
    before = set(bpy.data.objects)
    center, radius = (0, 124, -1), (29, 34, 29)
    head = ellipsoid("04 | Round diving helmet", center, radius, segments=64, rings=40)
    subtract(head, ellipsoid("Helmet inner shell cutter", center, (26.5, 31.5, 26.5)))
    subtract(head, box("Narrow recessed visor", (0, 127, -29), (47, 5, 23)))
    subtract(head, jagged_cutter("Jagged forehead perforation", (12, 144, -23), (5.2, 4.8), 18))
    subtract(head, jagged_cutter("Small helmet edge loss", (-18, 146, -19), (3.5, 3.5), 16))
    weather(head)
    ellipsoid("Unlit helmet interior", center, (24, 29, 24), "dark", 40, 24)
    shell_seams(center, radius, [37, 61], [-100, -53, 0, 53, 100], "Helmet", min_latitude=18)
    # A curved eyebrow follows the dome rather than forming a rectangular nose.
    tube("Upper visor lip", [sphere_point(center, radius, 10, lon, 1.3) for lon in range(-49, 50, 4)], 1.25, "plate")
    tube("Lower visor lip", [sphere_point(center, radius, -2, lon, .8) for lon in range(-44, 45, 4)], .9, "edge")
    for side in (-1, 1):
        x = side*28
        cylinder("Helmet side filter housing", (x-side*3, 114, -5), (x+side*4, 114, -5), 11.5, "plate", 40)
        cylinder("Recessed side filter", (x+side*4.1, 114, -5), (x+side*4.5, 114, -5), 8.8, "dark", 32)
        arc("Side filter outer rolled rim", (x+side*4.5, 114, -5), (1, 0, 0), 10.4, 1.2, "edge")
        arc("Side filter concentric ring", (x+side*4.8, 114, -5), (1, 0, 0), 7.2, .7, "joint")
        for i in range(-2, 3):
            z = -5+i*2.6
            height = math.sqrt(max(0, 8**2-(i*2.6)**2))
            cylinder("Filter grille rib", (x+side*5, 114-height, z), (x+side*5, 114+height, z), .55, "joint", 6)
    hose = catmull([(-30, 113, -8), (-31, 107, -24), (-20, 104, -35),
                    (0, 104, -39), (20, 108, -34), (30, 115, -13)])
    tube("05 | Heavy curved respirator hose", hose, 4.5, "armor", 14)
    for i in range(3, len(hose)-2, 4):
        a, b = hose[i-1], hose[i+1]
        d = (b-a).normalized()
        cylinder("Hose coupling band", hose[i]-d*.65, hose[i]+d*.65, 4.95, "edge", 16)
    cylinder("Front respirator outlet", (21, 108, -31), (23, 108, -44), 6.1, "plate", 32)
    cylinder("Black respirator aperture", (23, 108, -44.2), (23, 108, -44.8), 4.4, "dark", 24)
    arc("Respirator outlet rim", (23, 108, -44.8), (0, 0, 1), 5.3, 1, "edge")
    vegetation(center, radius, [(40, 27, 69), (-37, 35, 68), (18, -28, -6)], "Helmet ivy")
    # Slight list and turn visible in the original; keep the collar horizontal.
    pivot = Vector(xyz((0, 96, 0)))
    transform = Matrix.Translation(pivot) @ Matrix.Rotation(math.radians(-8), 4, "Z") @ Matrix.Rotation(math.radians(5), 4, "Y") @ Matrix.Translation(-pivot)
    for obj in set(bpy.data.objects)-before:
        obj.matrix_world = transform @ obj.matrix_world


def forearm():
    a, b = Vector((48, 19, -88)), Vector((-10, 17, -144))
    axis = (b-a).normalized()
    side = axis.cross(Vector((0, 1, 0))).normalized()
    start, end = Vector(xyz(a)), Vector(xyz(b))
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=17, radius2=19,
                                    depth=(end-start).length, location=(start+end)/2)
    arm = bpy.context.object
    arm.rotation_euler = (end-start).to_track_quat("Z", "Y").to_euler()
    finish(arm, "06 | Long detached bronze forearm", "armor")
    subtract(arm, cylinder("Forearm hollow", a-axis*2, b+axis*2, 13.5, "joint", 40))
    subtract(arm, jagged_cutter("Broken elbow edge", a+(b-a)*.12+Vector((0, 10, -5)), (7, 8), 34))
    weather(arm)
    for t in (.06, .16, .72, .94):
        center = a+(b-a)*t
        arc("Forearm rolled armour band", center, axis, 17+2*t, 1.3, "edge")
    for t in (.31, .49, .63):
        center = a+(b-a)*t
        arc("Forearm plate seam", center, axis, 17+2*t+.15, .5, "rust")
    cylinder("Dark broken elbow interior", a+axis*3, a+axis*10, 13, "joint", 32)
    arc("Exposed elbow race", a-axis*.5, axis, 15, 1.1, "joint", 20, 320)
    wrist = b+axis*8
    cylinder("Wrist black separation", b, wrist+axis*2, 13, "joint", 40)
    arc("Wrist armour cuff", wrist, axis, 16.5, 2, "plate")
    palm_center = wrist+axis*12
    palm = ellipsoid("07 | Half-buried mechanical palm", palm_center, (18, 11, 17), "plate", 32, 20)
    weather(palm, "plate")
    for i in range(4):
        root = palm_center+axis*12+side*((i-1.5)*7)
        root.y = 10
        knuckle = root+axis*(8-abs(i-1.5))
        tip = knuckle+axis*(9-abs(i-1.5))
        tip.y = 5
        cylinder(f"Finger {i+1} first phalanx", root, knuckle, 3.3, "plate", 12)
        cylinder(f"Finger {i+1} second phalanx", knuckle, tip, 2.8, "armor", 12)
        arc(f"Finger {i+1} knuckle seam", knuckle, axis, 3.4, .6, "joint")
    thumb_root = palm_center-side*17
    thumb_tip = thumb_root+axis*15-side*6
    thumb_root.y, thumb_tip.y = 11, 5
    cylinder("Detached hand thumb", thumb_root, thumb_tip, 4.2, "plate", 16)
    # Sparse trailing growth on the upward-facing, rear half of the sleeve.
    for i in range(14):
        p = a+(b-a)*RNG.uniform(.0, .42)+side*RNG.uniform(-12, 12)
        p.y = 19+math.sqrt(max(0, 17**2-((p-a).dot(side))**2))
        ellipsoid("Arm crest vegetation", p, (RNG.uniform(2, 4), 1.8, RNG.uniform(3, 5)), "moss", 12, 8)


def buried_waist():
    """Continuous lower cuirass, narrowed waist and ragged partial pelvic shell.

    Both wall surfaces and the exposed broken thickness are explicit geometry.
    The bottom is an open irregular tear, not a flat pedestal or a pair of legs.
    """
    levels = [(8, 56, 41), (-6, 52, 38), (-20, 44, 33),
              (-31, 41, 31), (-40, 46, 33), (-49, 45, 32)]
    count = 96
    vertices, faces = [], []
    for inner in (False, True):
        for level, (y, rx, rz) in enumerate(levels):
            for i in range(count):
                angle = math.tau*i/count
                tear = (5*math.sin(3*angle+.4)+3.5*math.sin(7*angle)+2*math.sin(13*angle)) if level == len(levels)-1 else 0
                thickness = 5.5 if inner else 0
                x = 4+(rx-thickness)*math.cos(angle)
                z = 10+(rz-thickness)*math.sin(angle)
                vertices.append(xyz((x, y+tear, z)))
    wall = len(levels)*count
    for side in (0, 1):
        offset = side*wall
        for level in range(len(levels)-1):
            for i in range(count):
                a, b = offset+level*count+i, offset+level*count+(i+1)%count
                face = (a, b, b+count, a+count)
                faces.append(tuple(reversed(face)) if side else face)
    for level in (0, len(levels)-1):
        for i in range(count):
            a, b = level*count+i, level*count+(i+1)%count
            face = (a, b, b+wall, a+wall)
            faces.append(tuple(reversed(face)) if level == 0 else face)
    mesh = bpy.data.meshes.new("Layered torn waist shell")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("08 | Buried abdomen and torn hip armour", mesh)
    bpy.context.collection.objects.link(obj)
    finish(obj, obj.name, "armor")
    # These openings are wholly below the nominal ground level.
    subtract(obj, jagged_cutter("Buried front armour split", (-15, -24, -23), (10, 15), 22))
    subtract(obj, jagged_cutter("Torn hip plate opening", (28, -43, -15), (11, 12), 22))
    weather(obj)
    # Broken belt segments wrap an elliptical waist rather than forming a plinth.
    for start, end in ((5, 115), (132, 233), (258, 344)):
        points = [(4+42.5*math.cos(math.radians(a)), -32, 10+32.2*math.sin(math.radians(a)))
                  for a in range(start, end+1, 3)]
        tube("Buried articulated waist band", points, 1.35, "plate")
    # Internal longitudinal members tie the new volume into the existing torso.
    for i, angle in enumerate((15, 65, 115, 165, 215, 265, 315)):
        a = math.radians(angle)
        top = (4+37*math.cos(a), 14, 10+26*math.sin(a))
        end_y = (-56, -48, -62, -53, -46, -60, -51)[i]
        bottom = (4+29*math.cos(a)+math.sin(a)*3, end_y, 10+20*math.sin(a))
        cylinder("09 | Exposed snapped pelvic support", top, bottom, 2.6, "joint", 12)
        collar = Vector(top).lerp(Vector(bottom), .72)
        direction = (Vector(bottom)-Vector(top)).normalized()
        cylinder("Broken support sleeve", collar-direction*3, collar+direction*3, 3.6, "plate", 16)
    cylinder("Buried axial mechanism", (4, 7, 10), (5, -38, 11), 12, "joint", 32)
    arc("Broken internal hip bearing", (5, -39, 11), (0, 1, 0), 19, 2, "joint", 18, 287)
    for i in range(4):
        x = -12+i*9
        tube("Dangling severed conduit", catmull([(x, -26, -2), (x-2, -42, -4),
                                                 (x+3, -55-i, -1), (x+6, -52-i, 2)]),
             .9, "rust", 8)


def main(version=3):
    global VERSION, STEM, OUT
    VERSION = version
    STEM = f"colossus-v{version}"
    OUT = ROOT / "relics/colossus/design/generated" / STEM
    RNG.seed(20261001)
    OUT.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for name, color in COLORS.items():
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = (*[int(color[i:i+2], 16)/255 for i in (0, 2, 4)], 1)
    body()
    helmet()
    forearm()
    # No integral plinth or projecting walkway: the armour continues into the soil.
    for x, z in [(-77, -16), (45, -28), (-24, 39)]:
        mound = ellipsoid("Soil in buried armour junction", (x, 1, z), (19, 8, 15), "earth", 24, 12)
        subtract(mound, box("Soil below baseline", (x, -20, z), (60, 40, 60)))
    if VERSION >= 3:
        buried_waist()
    bpy.context.view_layer.update()
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    corners = [obj.matrix_world @ Vector(v) for obj in meshes for v in obj.bound_box]
    low = [min(p[i] for p in corners) for i in range(3)]
    high = [max(p[i] for p in corners) for i in range(3)]
    # Keep the accepted above-ground body at the previous block scale. Fixing
    # total height to 160 again would shrink the helmet and shoulders.
    original_height = 170.94763278961182
    blocks_per_unit = 159/original_height
    target_height = round((high[2]-low[2])*blocks_per_unit)+1
    export_scale = (target_height-1)/(high[2]-low[2])
    metadata = {
        "name": f"Colossus v{VERSION}", "reference": "https://www.instagram.com/reel/DaoBxUEiBNa/",
        "reference_seconds": [0, 5], "source_bounds_blender": [low, high],
        "height_target_blocks": target_height, "scale_is_estimate": True,
        "scale_reference": {"original_source_height": original_height, "original_export_height": 160},
        "blocks_per_source_unit": export_scale,
        "basis": "Dome head/body width about 0.3–0.4; helmet/visible-body height about 0.35; detached sleeve in foreground. Perspective prevents absolute measurement.",
        "ground_level_source": 20, "seed": 20261001,
        "ground_level_nbt_approx": round((20-low[2])*export_scale),
        "hidden_geometry": "Rear and inner structure inferred; reference shows one frontal three-quarter view.",
    }
    if VERSION >= 3:
        metadata["buried_hip"] = {"shell_ends_source_y": [-60, -38], "lowest_support_source_y": low[2],
                                  "note": "Open irregular pelvic tear with continuous double-sided armour, snapped supports and conduits; no legs."}
    (OUT / f"{STEM}.design.json").write_text(json.dumps(metadata, indent=2)+"\n")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.wm.obj_export(filepath=str(OUT / f"{STEM}.obj"), forward_axis="NEGATIVE_Z", up_axis="Y",
                          export_selected_objects=True, export_triangulated_mesh=True, export_materials=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene["design_name"] = f"Colossus v{VERSION}"
    scene["reference_url"] = metadata["reference"]
    scene["scale_note"] = ("Above-ground scale calibrated to Colossus v2; additional buried abdomen and torn hip increase total export height."
                           if VERSION >= 3 else "160-block height is an artistic estimate from the reference perspective.")
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / f"{STEM}-source.blend"))
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
