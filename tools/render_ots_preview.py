"""Render the converted NBT with the legacy Minecraft atlas, using Blender Cycles.

blender --background --python tools/render_ots_preview.py
The source view comes from the editable blend; block views come only from the NBT.
"""
import argparse
import json
import math
from pathlib import Path
import random
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from relic_assets import decode_nbt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "relics/colossus/archive/first-concept/generated"
ATLAS = ROOT / ".work/ObjToSchematic/res/atlases"
STEM = "colossus"
CONFIG = {}
FACES = [
    ((1, 0, 0), "east", [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)]),
    ((-1, 0, 0), "west", [(0, 0, 1), (0, 1, 1), (0, 1, 0), (0, 0, 0)]),
    ((0, 1, 0), "up", [(0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)]),
    ((0, -1, 0), "down", [(0, 0, 1), (0, 0, 0), (1, 0, 0), (1, 0, 1)]),
    ((0, 0, -1), "north", [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)]),
    ((0, 0, 1), "south", [(1, 0, 1), (1, 1, 1), (0, 1, 1), (0, 0, 1)]),
]


def material(name, color):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = .88
    return mat


def point_at(obj, target):
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat("-Z", "Y").to_euler()


def stage():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 24
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = 1400, 1050
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "Standard"
    scene.world = bpy.data.worlds.new("Soft daylight")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (.72, .78, .86, 1)
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .65
    subjects = [obj for obj in scene.objects if obj.type == "MESH"]
    corners = [obj.matrix_world @ Vector(v) for obj in subjects for v in obj.bound_box]
    low = Vector(tuple(min(p[i] for p in corners) for i in range(3)))
    high = Vector(tuple(max(p[i] for p in corners) for i in range(3)))
    center = (low+high)/2
    bpy.ops.mesh.primitive_plane_add(size=10000, location=(center.x, center.y, low.z-.15))
    bpy.context.object.name = "Presentation ground (not exported)"
    bpy.context.object.data.materials.append(material("Warm neutral ground", (.31, .30, .27)))
    # Neutral 2-block scale marker, excluded from source and NBT exports.
    bpy.ops.mesh.primitive_cube_add(size=1, location=(low.x-4, high.y+2, low.z+1))
    marker = bpy.context.object
    marker.name = "2-block scale marker (not exported)"
    marker.scale = (.65, .65, 2)
    marker.data.materials.append(material("Scale marker turquoise", (.06, .55, .50)))
    light = bpy.data.lights.new("Large softbox", "AREA")
    light.energy, light.shape, light.size = 180000, "DISK", 80
    lamp = bpy.data.objects.new("Large softbox", light)
    scene.collection.objects.link(lamp)
    lamp.location = center+Vector((-70, 100, 140))
    point_at(lamp, center)
    camera = bpy.data.objects.new("Inspection camera", bpy.data.cameras.new("Inspection camera"))
    scene.collection.objects.link(camera)
    camera.data.type = "ORTHO"
    camera.data.clip_end = 2000
    scene.camera = camera
    return center, corners


def render(name, center, corners, direction):
    scene = bpy.context.scene
    camera = scene.camera
    camera.location = center+Vector(direction)*3
    point_at(camera, center)
    rotation = camera.rotation_euler.to_matrix().transposed()
    projected = [rotation @ (point-center) for point in corners]
    width = max(p.x for p in projected)-min(p.x for p in projected)
    height = max(p.y for p in projected)-min(p.y for p in projected)
    # ortho_scale is the horizontal extent in a landscape render.
    camera.data.ortho_scale = max(width, height*1400/1050)*1.20
    scene.render.filepath = str(OUT / name)
    bpy.ops.render.render(write_still=True)


def blocks_from_nbt(path=None, predicate=None):
    root = decode_nbt((path or OUT / f"{STEM}.nbt").read_bytes())
    palette = [entry["Name"] for entry in root["palette"]]
    blocks = {tuple(b["pos"]): palette[b["state"]] for b in root["blocks"]
              if palette[b["state"]] != "minecraft:air" and (predicate is None or predicate(b["pos"]))}
    atlas = json.loads((ATLAS / "vanilla.atlas").read_text())
    atlas_blocks = {entry["name"]: entry for entry in atlas["blocks"]}
    # The legacy atlas lacks grass_block. Use a clearly documented preview-only
    # composite: dirt sides/bottom and moss-grain top, optionally tinted by setting.
    if "minecraft:grass_block" in blocks.values():
        atlas_blocks["minecraft:grass_block"] = {"faces": {
            side: atlas_blocks["minecraft:moss_block" if side == "up" else "minecraft:dirt"]["faces"][side]
            for _, side, _ in FACES}}
    vertices, faces, uvs, grass_faces = [], [], [], []
    sx, _, sz = root["size"]
    for (x, y, z), block in blocks.items():
        for (dx, dy, dz), side, face in FACES:
            if (x+dx, y+dy, z+dz) in blocks:
                continue
            index = len(vertices)
            vertices.extend((x+a-sx/2, -(z+c-sz/2), y+b) for a, b, c in face)
            faces.append(tuple(range(index, index+4)))
            grass_faces.append(block == "minecraft:grass_block" and side == "up")
            tex = atlas["textures"][atlas_blocks[block]["faces"][side]]
            n = atlas["atlasSize"]*3
            u0, u1 = (3*tex["atlasColumn"]+1)/n, (3*tex["atlasColumn"]+2)/n
            v0, v1 = 1-(3*tex["atlasRow"]+2)/n, 1-(3*tex["atlasRow"]+1)/n
            uvs.extend([(u0, v0), (u0, v1), (u1, v1), (u1, v0)])
    mesh = bpy.data.meshes.new("Exposed NBT block faces")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    layer = mesh.uv_layers.new(name="Minecraft atlas")
    layer.data.foreach_set("uv", [v for uv in uvs for v in uv])
    obj = bpy.data.objects.new("Actual converted NBT", mesh)
    bpy.context.collection.objects.link(obj)
    mat = material("Minecraft legacy atlas", (.4, .4, .4))
    texture = mat.node_tree.nodes.new("ShaderNodeTexImage")
    texture.image = bpy.data.images.load(str(ATLAS / "vanilla.png"))
    texture.image.pack()
    texture.interpolation = "Closest"
    mat.node_tree.links.new(texture.outputs["Color"], mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"])
    obj.data.materials.append(mat)
    if any(grass_faces):
        grass = mat.copy()
        grass.name = "Grass preview approximation / biome tint not simulated"
        multiply = grass.node_tree.nodes.new("ShaderNodeMixRGB")
        multiply.blend_type = "MULTIPLY"
        multiply.inputs[0].default_value = 1
        multiply.inputs[2].default_value = (*CONFIG.get("preview", {}).get("grass_tint", [1,1,1]), 1)
        tex = next(n for n in grass.node_tree.nodes if n.type == "TEX_IMAGE")
        grass.node_tree.links.new(tex.outputs["Color"], multiply.inputs[1])
        grass.node_tree.links.new(multiply.outputs[0], grass.node_tree.nodes["Principled BSDF"].inputs["Base Color"])
        obj.data.materials.append(grass)
        for face, is_grass in zip(mesh.polygons, grass_faces):
            face.material_index = int(is_grass)
    bpy.context.view_layer.update()
    print(f"Preview mesh: {len(blocks)} NBT blocks, {len(faces)} visible faces")
    return obj


def scale_comparison(main_model):
    preview = CONFIG.get("preview", {})
    previous = ROOT / preview.get("comparison", "relics/colossus/archive/first-concept/generated/colossus.nbt")
    if not previous.exists():
        return
    small = blocks_from_nbt(previous)
    small.name = "Previous asset / actual block scale"
    small.location = ((main_model.dimensions.x+small.dimensions.x)/2+20, 0, 0) if "comparison" in preview else (162, -47, 0)
    bpy.context.view_layer.update()
    corners = [obj.matrix_world @ Vector(v) for obj in (main_model, small) for v in obj.bound_box]
    low = Vector(tuple(min(p[i] for p in corners) for i in range(3)))
    high = Vector(tuple(max(p[i] for p in corners) for i in range(3)))
    render("06-size-comparison.png", (low+high)/2, corners, (45, 250, 105))
    bpy.data.objects.remove(small, do_unlink=True)


def burial_inspection(main_model, center, corners):
    metadata = json.loads((OUT / f"{STEM}.design.json").read_text())
    ground = metadata["ground_level_nbt_approx"]
    xs, ys = [v.x for v in corners], [v.y for v in corners]
    bounds = (min(xs)-7, max(xs)+7, min(ys)-7, max(ys)+7)
    x0, x1, y0, y1 = bounds
    mesh = bpy.data.meshes.new("Nominal surface datum")
    mesh.from_pydata([(x0, y0, ground), (x1, y0, ground), (x1, y1, ground), (x0, y1, ground)], [], [(0, 1, 2, 3)])
    plane = bpy.data.objects.new("Nominal ground / inspection only", mesh)
    bpy.context.collection.objects.link(plane)
    mat = material("Transparent surface datum", (.12, .62, .58))
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    mix = nodes.new("ShaderNodeMixShader")
    mix.inputs[0].default_value = .10
    links.new(transparent.outputs[0], mix.inputs[1])
    links.new(nodes["Principled BSDF"].outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], nodes["Material Output"].inputs["Surface"])
    mesh.materials.append(mat)
    line_mat = material("Surface datum outline", (.04, .65, .60))
    curve = bpy.data.curves.new("Surface datum outline", "CURVE")
    curve.dimensions, curve.bevel_depth, curve.bevel_resolution = "3D", .35, 1
    spline = curve.splines.new("POLY")
    spline.points.add(3)
    for point, pos in zip(spline.points, [(x0, y0, ground, 1), (x1, y0, ground, 1),
                                         (x1, y1, ground, 1), (x0, y1, ground, 1)]):
        point.co = pos
    spline.use_cyclic_u = True
    outline = bpy.data.objects.new("Surface datum outline", curve)
    bpy.context.collection.objects.link(outline)
    curve.materials.append(line_mat)
    render("07-buried-body.png", center, corners, (120, 250, 90))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / f"{STEM}-underground.blend"))
    bpy.data.objects.remove(plane, do_unlink=True)
    bpy.data.objects.remove(outline, do_unlink=True)
    # Extract an actual block subset for the detail view; no invented interior mesh.
    detail = blocks_from_nbt(predicate=lambda p: p[1] < ground-12 and p[2] > main_model.dimensions.y*.52)
    main_model.hide_render = True
    detail_corners = [detail.matrix_world @ Vector(v) for v in detail.bound_box]
    lo = Vector(tuple(min(p[i] for p in detail_corners) for i in range(3)))
    hi = Vector(tuple(max(p[i] for p in detail_corners) for i in range(3)))
    render("08-hip-detail.png", (lo+hi)/2, detail_corners, (95, 230, 55))
    main_model.hide_render = False
    bpy.data.objects.remove(detail, do_unlink=True)


def landscape():
    """Reference-style context; all landscape and scale objects are render-only."""
    if CONFIG.get("preview", {}).get("landscape") == "new-relic-v1":
        from render_new_relic_v1_scene import render_scene
        return render_scene(sys.modules[__name__])
    if CONFIG.get("preview", {}).get("landscape") == "v4-deposits":
        from render_relic_v4_scene import render_deposits
        return render_deposits(sys.modules[__name__])
    if CONFIG.get("preview", {}).get("landscape") == "skull-hills":
        from render_skull_scene import render_hills
        return render_hills(sys.modules[__name__])
    if CONFIG.get("preview", {}).get("landscape") == "desert":
        from render_obelisk_scene import render_desert
        return render_desert(sys.modules[__name__])
    metadata = json.loads((OUT / f"{STEM}.design.json").read_text())
    low, high = metadata["source_bounds_blender"]
    scale = (CONFIG["height"]-1)/(high[2]-low[2])
    def world(x, y, z):
        return ((x-(low[0]+high[0])/2)*scale,
                (-z-(low[1]+high[1])/2)*scale, (y-low[2])*scale)
    def ground(x, z):
        return (9+27*math.exp(-((x-105)/75)**2-((z+25)/90)**2)
                +34*math.exp(-((x+114)/64)**2-((z+56)/100)**2)
                +18*math.exp(-((x-50)/130)**2-((z+255)/72)**2)
                +3*math.sin(x*.033+z*.014)*math.cos(z*.023))
    for obj in bpy.context.scene.objects:
        if "not exported" in obj.name:
            obj.hide_render = True
    vertices, faces = [], []
    n, step = 181, 6
    for j in range(n):
        z = -560+j*step
        for i in range(n):
            x = -540+i*step
            vertices.append(world(x, ground(x, z), z))
            if i and j:
                a = j*n+i
                faces.append((a-n-1, a-1, a, a-n))
    mesh = bpy.data.meshes.new("Illustrative rolling hills")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("Landscape context / render only", mesh)
    bpy.context.collection.objects.link(obj)
    for face in mesh.polygons:
        face.use_smooth = True
    mat = material("Muted meadow", (.16, .22, .095))
    noise = mat.node_tree.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = .038
    noise.inputs["Detail"].default_value = 3
    texcoord = mat.node_tree.nodes.new("ShaderNodeTexCoord")
    mat.node_tree.links.new(texcoord.outputs["Object"], noise.inputs["Vector"])
    ramp = mat.node_tree.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (.065, .11, .042, 1)
    ramp.color_ramp.elements[1].color = (.23, .29, .12, 1)
    mat.node_tree.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    mat.node_tree.links.new(ramp.outputs["Color"], mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"])
    mesh.materials.append(mat)
    # A tiny two-block human, deliberately at the arm rather than near the camera.
    human_mat = material("Scale figure ochre", (.7, .30, .055))
    px, pz = 20, -185
    base = ground(px, pz)
    for center, size in [((px, base+1, pz), (.6, 1.2, .35)),
                         ((px, base+1.8, pz), (.4, .4, .4)),
                         ((px-.17, base+.3, pz), (.2, .6, .25)),
                         ((px+.17, base+.3, pz), (.2, .6, .25))]:
        # Height is in final Minecraft blocks, independent of source rescaling.
        location = world(center[0], base+(center[1]-base)/scale, center[2])
        bpy.ops.mesh.primitive_cube_add(size=1, location=location)
        bpy.context.object.name = "Two-block person / render only"
        bpy.context.object.scale = (size[0], size[2], size[1])
        bpy.context.object.data.materials.append(human_mat)
    shrub_mat = material("Low valley scrub", (.055, .11, .06))
    rng = random.Random(2927)
    for _ in range(55):
        x, z = rng.uniform(-125, 120), rng.uniform(-180, 65)
        # Keep the arm valley and silhouette readable.
        if abs(x) < 35:
            continue
        y = ground(x, z)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1, location=world(x, y+.8, z))
        bpy.context.object.name = "Valley scrub / render only"
        bpy.context.object.scale = (rng.uniform(2, 4), rng.uniform(2, 4), rng.uniform(1, 2.5))
        bpy.context.object.data.materials.append(shrub_mat)
    scene = bpy.context.scene
    scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (.32, .48, .72, 1)
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .7
    sun = bpy.data.lights.new("Reference daylight", "SUN")
    sun.energy, sun.angle = 1.6, math.radians(12)
    sun.color = (1.0, .86, .68)
    lamp = bpy.data.objects.new("Reference daylight", sun)
    scene.collection.objects.link(lamp)
    lamp.rotation_euler = (math.radians(28), math.radians(-35), math.radians(-25))
    scene.camera.data.type = "PERSP"
    scene.camera.data.lens = CONFIG.get("preview", {}).get("landscape_lens", 45)
    scene.camera.location = world(175, 126, -390)
    point_at(scene.camera, world(-10, 66, -45))
    scene.render.resolution_x, scene.render.resolution_y = 1400, 1600
    scene.cycles.samples = 32
    scene.render.filepath = str(OUT / CONFIG.get("preview", {}).get("landscape_image", "05-blocks-landscape.png"))
    bpy.ops.render.render(write_still=True)
    if CONFIG.get("preview", {}).get("save_landscape_scene", True):
        bpy.ops.wm.save_as_mainfile(filepath=str(OUT / f"{STEM}-landscape.blend"))


def main():
    global CONFIG, OUT, STEM, ATLAS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "relics/colossus/archive/first-concept/colossus-ots.json")
    parser.add_argument("--source-only", action="store_true")
    parser.add_argument("--blocks-only", action="store_true")
    parser.add_argument("--landscape-only", action="store_true")
    parser.add_argument("--presentation-only", action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    CONFIG = json.loads(args.config.read_text(encoding="utf-8"))
    output = ROOT / CONFIG["output"]
    OUT, STEM = output.parent, output.stem
    ATLAS = ROOT / CONFIG.get("preview_atlas", str(Path(CONFIG["repository"]) / "res/atlases"))
    preview = CONFIG.get("preview", {})
    bpy.ops.wm.open_mainfile(filepath=str(OUT / f"{STEM}-source.blend"))
    # Source materials are intentionally simple, not a texture bake.
    for mat in bpy.data.materials:
        rgb = mat.diffuse_color[:]
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = rgb
        mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = .85
    if not args.blocks_only and not args.landscape_only and not args.presentation_only:
        center, corners = stage()
        render("01-blender-source.png", center, corners, preview.get("front", (100, 180, 95)))
    if args.source_only:
        return
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    main_model = blocks_from_nbt()
    center, corners = stage()
    if args.landscape_only or args.presentation_only:
        if args.presentation_only:
            scale_comparison(main_model)
        landscape()
        return
    render("02-blocks-front.png", center, corners, preview.get("front", (100, 180, 95)))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / f"{STEM}-blocks.blend"))
    render("03-blocks-other-side.png", center, corners, preview.get("other", (-140, 160, 85)))
    render("04-blocks-back.png", center, corners, preview.get("back", (130, -170, 115)))
    if preview.get("buried_hip"):
        burial_inspection(main_model, center, corners)
    if preview.get("landscape"):
        scale_comparison(main_model)
        landscape()


if __name__ == "__main__":
    main()
