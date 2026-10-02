"""Matched close views and an explicitly false-color salvage map for study B."""
import json
from pathlib import Path
import sys

import bpy

sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_ots_preview as renderer

ROOT=Path(__file__).resolve().parents[1]


def reset():
    bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)


def main():
    renderer.CONFIG=json.loads((ROOT/"relics/colossus/design/studies/colossus-v4-1-materials-b.json").read_text())
    output=ROOT/renderer.CONFIG["output"]
    renderer.OUT,renderer.STEM=output.parent,output.stem
    renderer.ATLAS=ROOT/renderer.CONFIG["repository"]/"res/atlases"
    meta=json.loads(output.with_suffix(".design.json").read_text())
    retained={tuple(p) for zone in meta["material_study"]["salvage_zones"] for p in zone["positions_nbt"]}
    low,high=meta["source_bounds_blender"];scale=meta["blocks_per_source_unit"]
    views=[("torso",(-104,10,-62),(97,108,63),(80,240,65)),
           ("forearm",(-13,7,-148),(60,44,-72),(70,170,140)),
           ("rear",(-100,5,-60),(97,108,63),(80,-240,70))]
    for name,lo,hi,direction in views:
        def inside(p):
            source=(p[0]/scale+low[0],p[1]/scale+low[2],p[2]/scale-high[1])
            return all(a<=v<=b for v,a,b in zip(source,lo,hi))
        framing=None
        for removed in (False,True):
            reset()
            renderer.blocks_from_nbt(predicate=lambda p:inside(p) and (not removed or tuple(p) not in retained))
            center,corners=renderer.stage()
            if framing is None: framing=(center,corners)
            renderer.render(f"13-{name}-{'after' if removed else 'before'}.png",*framing,direction)
    reset()
    body=renderer.blocks_from_nbt(predicate=lambda p:tuple(p) not in retained)
    body.data.materials.clear();body.data.materials.append(renderer.material("Permanent material / diagram gray",(.22,.26,.29)))
    metal=renderer.blocks_from_nbt(predicate=lambda p:tuple(p) in retained)
    metal.data.materials.clear();metal.data.materials.append(renderer.material("Salvage metal / diagram amber",(1,.32,.035)))
    center,corners=renderer.stage()
    renderer.render("14-salvage-map-front.png",center,corners,(100,230,75))
    renderer.render("14-salvage-map-back.png",center,corners,(100,-250,100))


if __name__=="__main__": main()
