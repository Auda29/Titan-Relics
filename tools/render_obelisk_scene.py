"""Painted Desert presentation and solid-foot inspection for Obelisk v2.

Used by render_ots_preview.py with design/obelisk-v2.json. Terrain is render-only.
"""
import json
import math

import bpy
from mathutils import Vector


def render_desert(renderer):
    scene = bpy.context.scene
    out = renderer.OUT
    metadata = json.loads((out / f"{renderer.STEM}.design.json").read_text())
    low, high = metadata["source_bounds_blender"]
    scale = (renderer.CONFIG["height"]-1)/(high[2]-low[2])
    def world(x, y, z):
        return ((x-(low[0]+high[0])/2)*scale,
                (-z-(low[1]+high[1])/2)*scale, (y-low[2])*scale)
    def relief(x, z):
        crest = 24*math.exp(-((x+.34*z+34)/64)**2)*math.exp(-((z+15)/330)**2)
        distant = 47*math.exp(-((z-230)/100)**2)*(1+.33*math.sin(x*.024)+.16*math.sin(x*.055))
        erosion = (9*math.sin(x*.027+z*.012)*math.cos(z*.017)+5*math.sin(x*.062-z*.021)
                   +1.3*math.sin(x*.17+z*.082)*math.cos(x*.095-z*.07))
        return crest+distant+erosion
    origin = relief(0, 0)
    def ground(x, z):
        return relief(x, z)-origin
    for obj in scene.objects:
        if "not exported" in obj.name:
            obj.hide_render = True
    vertices, faces = [], []
    n, step = 201, 6
    for j in range(n):
        z = -700+j*step
        for i in range(n):
            x = -600+i*step
            vertices.append(world(x, ground(x, z), z))
            if i and j:
                a = j*n+i
                faces.append((a-n-1, a-1, a, a-n))
    mesh = bpy.data.meshes.new("Eroded stratified desert")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    terrain = bpy.data.objects.new("Painted Desert landscape / render only", mesh)
    scene.collection.objects.link(terrain)
    for face in mesh.polygons:
        face.use_smooth = True
    mat = renderer.material("Ochre and muted turquoise mineral strata", (.36, .23, .11))
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    coord = nodes.new("ShaderNodeTexCoord")
    separate = nodes.new("ShaderNodeSeparateXYZ")
    links.new(coord.outputs["Object"], separate.inputs[0])
    noise = nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = .013
    noise.inputs["Detail"].default_value = 3
    links.new(coord.outputs["Object"], noise.inputs["Vector"])
    distortion = nodes.new("ShaderNodeMath")
    distortion.operation = "MULTIPLY"
    distortion.inputs[1].default_value = 10
    links.new(noise.outputs["Fac"], distortion.inputs[0])
    add = nodes.new("ShaderNodeMath")
    add.operation = "ADD"
    links.new(separate.outputs["Z"], add.inputs[0])
    links.new(distortion.outputs[0], add.inputs[1])
    frequency = nodes.new("ShaderNodeMath")
    frequency.operation = "MULTIPLY"
    frequency.inputs[1].default_value = .21
    links.new(add.outputs[0], frequency.inputs[0])
    fraction = nodes.new("ShaderNodeMath")
    fraction.operation = "FRACT"
    links.new(frequency.outputs[0], fraction.inputs[0])
    ramp = nodes.new("ShaderNodeValToRGB")
    colors = [(0, (.22, .13, .075, 1)), (.27, (.50, .32, .14, 1)),
              (.43, (.61, .46, .24, 1)), (.52, (.15, .25, .21, 1)),
              (.58, (.12, .21, .18, 1)), (.67, (.37, .16, .095, 1)),
              (.87, (.47, .30, .13, 1)), (1, (.22, .13, .075, 1))]
    ramp.color_ramp.elements.remove(ramp.color_ramp.elements[1])
    ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = colors[0]
    for position, color in colors[1:]:
        ramp.color_ramp.elements.new(position).color = color
    links.new(fraction.outputs[0], ramp.inputs[0])
    links.new(ramp.outputs[0], nodes["Principled BSDF"].inputs["Base Color"])
    grain = nodes.new("ShaderNodeTexNoise")
    grain.inputs["Scale"].default_value = 2.5
    grain.inputs["Detail"].default_value = 3
    links.new(coord.outputs["Object"], grain.inputs["Vector"])
    bump = nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = .12
    bump.inputs["Distance"].default_value = .3
    links.new(grain.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], nodes["Principled BSDF"].inputs["Normal"])
    mesh.materials.append(mat)
    # The 2-block person is in the same world scale as the exported stele.
    person = renderer.material("Scale figure burnt orange", (.47, .115, .04))
    px, pz = 21, -24
    base = ground(px, pz)
    for y, sx, sy, sz in [(1, .55, 1.2, .3), (1.8, .4, .4, .4), (.3, .45, .6, .25)]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=world(px, base+y/scale, pz))
        bpy.context.object.name = "Two-block traveller / render only"
        bpy.context.object.scale = (sx, sz, sy)
        bpy.context.object.data.materials.append(person)
    # Diffuse storm sky plus low warm lateral sun reproduces the large face contrast.
    world_nodes = scene.world.node_tree.nodes
    world_nodes["Background"].inputs["Color"].default_value = (.25, .235, .29, 1)
    world_nodes["Background"].inputs["Strength"].default_value = .42
    for obj in scene.objects:
        if obj.type == "LIGHT" and obj.data.type == "AREA":
            obj.data.energy = 8000
    sun = bpy.data.lights.new("Late desert sun", "SUN")
    sun.energy, sun.angle, sun.color = 3.0, math.radians(8), (1.0, .86, .63)
    lamp = bpy.data.objects.new("Late desert sun", sun)
    scene.collection.objects.link(lamp)
    lamp.location = world(-180, 260, 80)
    renderer.point_at(lamp, world(0, 80, 0))
    scene.camera.data.type, scene.camera.data.lens = "PERSP", 37
    scene.camera.location = world(-140, 65, -335)
    renderer.point_at(scene.camera, world(0, 50, 0))
    scene.render.resolution_x, scene.render.resolution_y = 1400, 1750
    scene.cycles.samples = 32
    scene.render.filepath = str(out / "05-blocks-landscape.png")
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out / f"{renderer.STEM}-landscape.blend"))
    # A second cinematic view makes the underground length and solid cut face legible.
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    root = renderer.decode_nbt((out / f"{renderer.STEM}.nbt").read_bytes())
    cx = root["size"][0]//2
    detail = renderer.blocks_from_nbt(predicate=lambda p: p[1] < 68 and p[0] <= cx)
    center, corners = renderer.stage()
    ground_y = metadata["ground_level_nbt_approx"]
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-.5, 0, ground_y))
    datum = bpy.context.object
    datum.name = "Surface line / inspection only"
    datum.scale = (root["size"][0]+8, root["size"][2]+8, .15)
    datum.data.materials.append(renderer.material("Ground datum turquoise", (.02, .55, .50)))
    renderer.render("07-solid-foot-section.png", center, corners, (135, 230, 90))
    bpy.ops.wm.save_as_mainfile(filepath=str(out / f"{renderer.STEM}-foot-section.blend"))
