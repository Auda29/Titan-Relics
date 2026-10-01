"""Skull asset presentation, optional cavity section, and head-scale comparison."""
import json
import math

import bpy


def render_hills(renderer):
    scene, out = bpy.context.scene, renderer.OUT
    metadata = json.loads((out / f"{renderer.STEM}.design.json").read_text(encoding="utf-8"))
    low, high = metadata["source_bounds_blender"]
    scale = (renderer.CONFIG["height"]-1)/(high[2]-low[2])
    preview = renderer.CONFIG.get("preview", {})
    scene_scale = preview.get("scene_scale", 1)
    def world(x, y, z):
        return ((x-(low[0]+high[0])/2)*scale, (-z-(low[1]+high[1])/2)*scale, (y-low[2])*scale)
    def ground(x, z):
        if metadata.get("exported_mound"):
            # Ground stays under the exported hill, so the actual block terrain
            # remains visible rather than being replaced by an illustrative prop.
            distance = math.hypot(x, z)
            fade = min(1, max(0, (distance-85)/100))
            return -1+fade*(5*math.sin(x*.021)+4*math.sin(z*.017))
        # Keep the mouth approach low, with gently rising banks on both sides.
        weight = min(1, max(0, (abs(x)-28)/65))
        banks = weight*(15+12*math.sin(z*.015+x*.01))
        distant = 38*math.exp(-((z-190)/130)**2)*(1+.32*math.sin(x*.014))
        foreground = 9*math.sin(x*.017+z*.012)*min(1, max(0, (-z-60)/160))
        return banks+distant+foreground-4
    for obj in scene.objects:
        if "not exported" in obj.name:
            obj.hide_render = True
    n, step = 181, 6
    vertices, faces = [], []
    for j in range(n):
        z = -650+j*step
        for i in range(n):
            x = -540+i*step
            vertices.append(world(x, ground(x, z), z))
            if i and j:
                a = j*n+i
                faces.append((a-n-1, a-1, a, a-n))
    mesh = bpy.data.meshes.new("Broad green valley")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    terrain = bpy.data.objects.new("Illustrative hills / not exported", mesh)
    scene.collection.objects.link(terrain)
    mat = renderer.material("Muted upland grass", (.12, .18, .06))
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    tex = nodes.new("ShaderNodeTexNoise")
    tex.inputs["Scale"].default_value = .035
    tex.inputs["Detail"].default_value = 4
    coords = nodes.new("ShaderNodeTexCoord")
    links.new(coords.outputs["Object"], tex.inputs["Vector"])
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (.045, .075, .025, 1)
    ramp.color_ramp.elements[1].color = (.24, .29, .12, 1)
    links.new(tex.outputs["Fac"], ramp.inputs[0])
    links.new(ramp.outputs[0], nodes["Principled BSDF"].inputs["Base Color"])
    bump = nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = .15
    bump.inputs["Distance"].default_value = .7
    links.new(tex.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs[0], nodes["Principled BSDF"].inputs["Normal"])
    mesh.materials.append(mat)
    for p in mesh.polygons:
        p.use_smooth = True
    # Human-scale traveller near the approach, kept at actual two-block height.
    person = renderer.material("Traveller ochre cloak", (.45, .21, .07))
    px, pz = -15*scene_scale, -115*scene_scale
    base = ground(px, pz)
    for y, size in [(1, (.6, .35, 1.25)), (1.8, (.4, .4, .4)), (.3, (.45, .3, .6))]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=world(px, base+y/scale, pz))
        obj = bpy.context.object
        obj.name = "Two-block traveller / preview only"
        obj.scale = size
        obj.data.materials.append(person)
    scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (.34, .48, .65, 1)
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .5
    for obj in scene.objects:
        if obj.type == "LIGHT" and obj.data.type == "AREA":
            obj.data.energy = 16000
    sun = bpy.data.lights.new("Soft valley daylight", "SUN")
    sun.energy, sun.angle = 2, math.radians(18)
    sun.color = (1, .91, .75)
    lamp = bpy.data.objects.new("Soft valley daylight", sun)
    scene.collection.objects.link(lamp)
    lamp.location = world(-180, 280, -120)
    renderer.point_at(lamp, world(0, 70, 0))
    scene.camera.data.type, scene.camera.data.lens = "PERSP", 43
    scene.camera.location = world(*preview.get("camera_source", [-133, 64, -390]))
    renderer.point_at(scene.camera, world(*preview.get("target_source", [0, 73, 0])))
    scene.render.resolution_x, scene.render.resolution_y = 1400, 1600
    scene.cycles.samples = 32
    scene.render.filepath = str(out / "05-blocks-landscape.png")
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out / f"{renderer.STEM}-landscape.blend"))
    if preview.get("head_comparison"):
        head_comparison(renderer, metadata)
    if preview.get("spine_inspection"):
        spine_inspection(renderer, metadata)
    if not preview.get("section", True):
        return
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    # Source X0 is not necessarily the center of a footprint containing a side spur.
    mid = round(-low[0]*scale)
    renderer.blocks_from_nbt(predicate=lambda p: p[0] <= mid)
    center, corners = renderer.stage()
    renderer.render("07-skull-section.png", center, corners, (190, 240, 95))
    bpy.ops.wm.save_as_mainfile(filepath=str(out / f"{renderer.STEM}-section.blend"))


def head_comparison(renderer, metadata):
    """Show actual NBT skull and Colossus head, with independent rest heights."""
    from mathutils import Vector
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    # Keep the exported mound. Removing terrain by palette would expose holes at
    # skull/soil intersections and misrepresent the actual complete structure.
    skull = renderer.blocks_from_nbt()
    cdir = renderer.ROOT / "relics/colossus/design/generated/colossus-v3"
    design = json.loads((cdir / "colossus-v3.design.json").read_text())
    cscale = design["blocks_per_source_unit"]
    low, high = design["source_bounds_blender"]
    def is_head(p):
        x, y, z = p[0]/cscale+low[0], p[1]/cscale+low[2], p[2]/cscale-high[1]
        # The top of the shoulders is below Y96. This spatial crop includes dome,
        # filters and respirator; it is an NBT head-region crop, not a new export.
        return y >= 96 and -42 <= x <= 42 and -50 <= z <= 36
    head = renderer.blocks_from_nbt(cdir / "colossus-v3.nbt", predicate=is_head)
    bpy.context.view_layer.update()
    for obj in (skull, head):
        points = [obj.matrix_world @ Vector(v) for v in obj.bound_box]
        lo = Vector(tuple(min(v[i] for v in points) for i in range(3)))
        hi = Vector(tuple(max(v[i] for v in points) for i in range(3)))
        obj.location -= Vector(((lo.x+hi.x)/2, (lo.y+hi.y)/2, lo.z))
    head.location.x -= (head.dimensions.x+skull.dimensions.x)/2+12
    bpy.context.view_layer.update()
    center, corners = renderer.stage()
    renderer.render("08-head-comparison.png", center, corners, (0, 270, 55))
    bpy.ops.wm.save_as_mainfile(filepath=str(renderer.OUT / f"{renderer.STEM}-head-comparison.blend"))


def spine_inspection(renderer, metadata):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    renderer.blocks_from_nbt()
    center, corners = renderer.stage()
    renderer.render("09-spine-overview.png", center, corners, (120, -240, 240))
    bpy.ops.wm.save_as_mainfile(filepath=str(renderer.OUT / f"{renderer.STEM}-spine-overview.blend"))
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    low, high = metadata["source_bounds_blender"]
    scale = metadata["blocks_per_source_unit"]
    def detail(p):
        x, y, z = p[0]/scale+low[0], p[1]/scale+low[2], p[2]/scale-high[1]
        return -17 <= x <= 53 and y >= 0 and 25 <= z <= 155
    renderer.blocks_from_nbt(predicate=detail)
    center, corners = renderer.stage()
    renderer.render("10-spine-detail.png", center, corners, (190, -110, 220))
    bpy.ops.wm.save_as_mainfile(filepath=str(renderer.OUT / f"{renderer.STEM}-spine-detail.blend"))
