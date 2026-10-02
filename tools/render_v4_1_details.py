"""NBT-only hand-pose and open-crack inspection views for the V4.1 revision."""
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_ots_preview as renderer
from render_colossus_v4_details import view

ROOT=Path(__file__).resolve().parents[1]


def main():
    out=ROOT/"relics/colossus/design/generated/colossus-v4-1-frame"
    region=((-78,4,-208),(17,85,-123))
    if "--obelisk-only" not in sys.argv:
        view("colossus-v4-frame","09-hand-before.png",region,(-140,180,220),True,output=out)
        view("colossus-v4-1-frame","10-hand-palm-up.png",region,(-140,180,220),True)
        view("colossus-v4-1-frame","11-hand-profile.png",region,(170,190,50),True)
        view("colossus-v4-1-frame","12-hand-higher-terrain.png",region,(-140,180,160),True,terrain_y=28)
    stem="obelisk-v4-1"
    renderer.OUT=ROOT/"relics/obelisk/design/generated"/stem
    renderer.STEM=stem
    renderer.CONFIG=json.loads((ROOT/f"relics/obelisk/design/{stem}.json").read_text())
    meta=json.loads((renderer.OUT/f"{stem}.design.json").read_text())
    from inspect_relic_v4 import source_mapping
    source,_=source_mapping(meta)
    for i,crack in enumerate(meta["obelisk_v4"]["cracks"]):
        center=crack["center_source"]
        bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
        renderer.blocks_from_nbt(predicate=lambda p:abs(source(p)[1]-center[1])<23)
        target,corners=renderer.stage()
        normal=crack["normal_source"]
        renderer.render(f"10-crack-{i+1}.png",target,corners,(normal[0]*230,-normal[2]*230,65))


if __name__=="__main__": main()
