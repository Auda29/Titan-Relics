"""Illustrate the shape after removing only the study's deliberately retained metal."""
import json
import argparse
from pathlib import Path
import sys

import bpy

sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_ots_preview as renderer
from inspect_ots_result import read_structure

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config",type=Path,default=ROOT/"relics/colossus/design/studies/colossus-v4-1-materials.json")
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    renderer.CONFIG=json.loads(args.config.read_text())
    renderer.ATLAS=ROOT/renderer.CONFIG["repository"]/"res/atlases"
    output=ROOT/renderer.CONFIG["output"]
    renderer.OUT,renderer.STEM=output.parent,output.stem
    meta=json.loads(output.with_suffix(".design.json").read_text())
    zones=meta["material_study"]["salvage_zones"]
    retained={tuple(p) for z in zones for p in z["positions_nbt"]}
    bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
    renderer.blocks_from_nbt(predicate=lambda p:tuple(p) not in retained)
    center,corners=renderer.stage()
    renderer.render("09-after-metal-salvage.png",center,corners,renderer.CONFIG["preview"]["front"])
    if "panel_salvage" in renderer.CONFIG:
        renderer.render("12-after-metal-salvage-back.png",center,corners,renderer.CONFIG["preview"]["back"])
    renderer.CONFIG["preview"]["landscape_image"]="10-after-metal-salvage-landscape.png"
    renderer.CONFIG["preview"]["save_landscape_scene"]=False
    renderer.landscape()
    if "panel_salvage" in renderer.CONFIG:
        return
    low,high=meta["source_bounds_blender"];scale=meta["blocks_per_source_unit"]
    for i,zone in enumerate(zones):
        center=zone["center_source"];r=zone["radius_source"]+3
        def inside(p):
            source=(p[0]/scale+low[0],p[1]/scale+low[2],p[2]/scale-high[1])
            return all(abs(a-b)<r for a,b in zip(source,center))
        for removed in (False,True):
            bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
            renderer.blocks_from_nbt(predicate=lambda p:inside(p) and (not removed or tuple(p) not in retained))
            target,corners=renderer.stage()
            renderer.render(f"11-site-{i+1}-{'after' if removed else 'before'}.png",target,corners,
                            (100,230,120) if i<2 else (50,-230,100))


if __name__=="__main__": main()
