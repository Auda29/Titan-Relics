"""Actual-NBT V4 deposits in restrained preview terrain, including rear/foot views."""
import json

import bpy
from mathutils import Vector


def render_deposits(renderer):
    metadata=json.loads((renderer.OUT/f"{renderer.STEM}.design.json").read_text())
    preview=renderer.CONFIG["preview"]
    scene=bpy.context.scene
    ground=metadata["ground_level_nbt_approx"]
    root=renderer.decode_nbt((renderer.OUT/f"{renderer.STEM}.nbt").read_bytes())
    # Local terrain is exported. This flat surrounding plane only illustrates its
    # nominal landing surface; it is not evidence of terrain-adaptive placement.
    for obj in scene.objects:
        if "not exported" in obj.name: obj.hide_render=True
        if obj.type=="LIGHT" and obj.data.type=="AREA": obj.data.energy=12000
    bpy.ops.mesh.primitive_plane_add(size=1800,location=(0,0,ground-.35))
    obj=bpy.context.object
    obj.name="Surrounding biome illustration / not exported"
    color=preview["ground_color"]
    mat=renderer.material("Surrounding ground preview",color)
    nodes,links=mat.node_tree.nodes,mat.node_tree.links
    noise=nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value=.15
    noise.inputs["Detail"].default_value=3
    coord=nodes.new("ShaderNodeTexCoord")
    links.new(coord.outputs["Object"],noise.inputs["Vector"])
    ramp=nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color=(*[c*.87 for c in color],1)
    ramp.color_ramp.elements[1].color=(*[min(1,c*1.08) for c in color],1)
    links.new(noise.outputs["Fac"],ramp.inputs[0])
    links.new(ramp.outputs[0],nodes["Principled BSDF"].inputs["Base Color"])
    obj.data.materials.append(mat)
    sun=bpy.data.lights.new("Neutral soft sunlight","SUN")
    sun.energy,sun.angle=1.6,.25
    lamp=bpy.data.objects.new(sun.name,sun)
    scene.collection.objects.link(lamp)
    lamp.rotation_euler=(.5,-.6,-.4)
    main=bpy.data.objects["Actual converted NBT"]
    corners=[main.matrix_world@Vector(v) for v in main.bound_box]
    center=sum(corners,Vector())/8
    renderer.render("05-blocks-landscape.png",center,corners,preview.get("front",[-180,250,175]))
    bpy.ops.wm.save_as_mainfile(filepath=str(renderer.OUT/f"{renderer.STEM}-landscape.blend"))
    renderer.render("09-deposits-rear.png",center,corners,preview.get("back",[110,-250,200]))
    if "deposits_v4" in metadata:
        renderer.render("10-deposits-overhead.png",center,corners,(0,-25,400))
    else:
        # Explicit crop of the lower monument, foundation fragments and sand.
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=False)
        renderer.blocks_from_nbt(predicate=lambda p:p[1]<ground+19)
        center,corners=renderer.stage()
        plane=bpy.data.objects["Presentation ground (not exported)"]
        plane.location.z=ground-.35
        plane.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(*color,1)
        renderer.render("08-foot-detail.png",center,corners,(-130,200,145))
