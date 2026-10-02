"""Revise the selected V4 B hand only; keep the published V4 studies intact."""
import hashlib
import json
from pathlib import Path
import sys

import bpy

sys.path.insert(0,str(Path(__file__).resolve().parent))
from create_colossus_v4 import bounds, fingerprint, raised_right_hand

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"relics/colossus/design"
BASE=DESIGN/"generated/colossus-v4-frame"
STEM="colossus-v4-1-frame"
OUT=DESIGN/"generated"/STEM


def main():
    source=BASE/"colossus-v4-frame-source.blend"
    bpy.ops.wm.open_mainfile(filepath=str(source))
    preserved={o.name:fingerprint(o) for o in bpy.context.scene.objects
               if o.type=="MESH" and o.get("asset_component")!="right_hand"}
    for o in list(bpy.context.scene.objects):
        if o.get("asset_component")=="right_hand":
            bpy.data.objects.remove(o,do_unlink=True)
    hand=raised_right_hand(palm_up=True)
    bpy.context.view_layer.update()
    assert all(fingerprint(bpy.data.objects[n])==h for n,h in preserved.items())
    metadata=json.loads((BASE/"colossus-v4-frame.design.json").read_text())
    low,high=bounds([o for o in bpy.context.scene.objects if o.type=="MESH"])
    assert abs(208/(high[2]-low[2])-metadata["blocks_per_source_unit"])<1e-6
    metadata.update(name="Colossus V4.1 / selected machine frame / palm upward",
        right_hand=hand, source_bounds_blender=[low,high],
        source_v4_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),preserved_v4_objects=preserved,
        revision="V4.1: user-requested supinated right hand with upward-curled fingers")
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{STEM}.design.json").write_text(json.dumps(metadata,indent=2)+"\n")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.wm.obj_export(filepath=str(OUT/f"{STEM}.obj"),forward_axis="NEGATIVE_Z",up_axis="Y",
        export_selected_objects=True,export_triangulated_mesh=True,export_materials=True)
    bpy.context.scene["design_name"]=metadata["name"]
    bpy.context.scene["right_hand_note"]=hand["note"]
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/f"{STEM}-source.blend"))
    print(f"Preserved {len(preserved)} non-hand V4 objects; palm normal {hand['palmar_normal_source']}")


if __name__=="__main__": main()
