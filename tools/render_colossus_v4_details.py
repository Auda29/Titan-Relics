"""Render actual-NBT V3/V4 rear, right-hand, and chest comparison crops in Blender."""
import argparse
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_ots_preview as renderer

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "relics/colossus/design"


def view(stem, name, region, direction, ground=False):
    renderer.OUT = DESIGN / "generated" / stem
    renderer.STEM = stem
    metadata = json.loads((renderer.OUT / f"{stem}.design.json").read_text())
    data = renderer.decode_nbt((renderer.OUT / f"{stem}.nbt").read_bytes())
    low, high = metadata["source_bounds_blender"]
    scale = metadata["blocks_per_source_unit"]
    def source(p):
        return (p[0]/scale+low[0], p[1]/scale+low[2], p[2]/scale-high[1])
    def inside(p):
        return all(a <= v <= b for a, v, b in zip(region[0], source(p), region[1]))
    def world(p):
        x, y, z = p
        return Vector(((x-low[0])*scale-data["size"][0]/2,
                       -((z+high[1])*scale-data["size"][2]/2), (y-low[2])*scale))
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    renderer.blocks_from_nbt(predicate=inside)
    renderer.stage()
    corners = [world((x, y, z)) for x in (region[0][0], region[1][0])
               for y in (region[0][1], region[1][1]) for z in (region[0][2], region[1][2])]
    center = sum(corners, Vector())/8
    if ground:
        plane = bpy.data.objects["Presentation ground (not exported)"]
        plane.location.z = metadata["ground_level_nbt_approx"]-.2
        plane.data.materials[0].diffuse_color = (.18, .22, .11, 1)
        plane.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (.18, .22, .11, 1)
    renderer.render(name, center, corners, direction)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hands-only", action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    for stem in (() if args.hands_only else ("colossus-v3", "colossus-v4-open", "colossus-v4-frame")):
        # V3 comparison images are written to V4-open; source V3 stays untouched.
        if stem == "colossus-v3":
            original_render = renderer.render
            def baseline_render(name, center, corners, direction):
                renderer.OUT = DESIGN / "generated/colossus-v4-open"
                original_render(name, center, corners, direction)
            renderer.render = baseline_render
        label = "v3" if stem == "colossus-v3" else "v4"
        view(stem, f"11-{label}-chest-detail.png", ((-8, 0, -46), (55, 57, 13)), (50, 230, 90))
        if stem != "colossus-v4-frame":
            view(stem, f"09-{label}-rear-detail.png", ((-99, 18, -3), (82, 103, 57)), (50, -270, 80))
        if stem == "colossus-v3":
            renderer.render = original_render
    for name, direction in [("10-right-hand-palm.png", (-180, 170, 80)),
                            ("12-right-hand-back.png", (180, -170, 110))]:
        view("colossus-v4-open", name, ((-63, 9, -185), (13, 70, -132)), direction, ground=True)


if __name__ == "__main__":
    main()
