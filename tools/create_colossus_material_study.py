"""Blender source palette and direct V4.1 block remap: absolutely no re-voxelization."""
from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
import sys

import bpy

sys.path.insert(0,str(Path(__file__).resolve().parent))
from create_colossus_v4 import fingerprint
from create_blender_colossus import xyz
from colossus_materials import encode_schematic,remap,metal_family
from inspect_ots_result import read_structure
from schem_to_nbt import read_schematic,convert

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/"relics/colossus/design/studies/colossus-v4-1-materials.json"


def main():
    global CONFIG
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config",type=Path,default=CONFIG)
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    CONFIG=args.config.resolve()
    spec=json.loads(CONFIG.read_text())
    nbt=ROOT/spec["source_nbt"];blend=ROOT/spec["source_blend"];schem=ROOT/spec["source_schematic"]
    out=(ROOT/spec["output"]).parent;stem=Path(spec["output"]).stem
    out.mkdir(parents=True,exist_ok=True)
    baseline=json.loads(nbt.with_suffix(".design.json").read_text())
    root,blocks=read_structure(nbt)
    size,schematic,version,offset=read_schematic(schem.read_bytes(),"omit")
    assert blocks==schematic and list(size)==root["size"] and version==root["DataVersion"]
    result,zones=remap(blocks,baseline,spec)
    (out/f"{stem}.schem").write_bytes(encode_schematic(result,size,version,offset))
    manifest=convert(out/f"{stem}.schem",out/f"{stem}.nbt","omit",32)
    bpy.ops.wm.open_mainfile(filepath=str(blend))
    meshes={o.name:fingerprint(o) for o in bpy.context.scene.objects if o.type=="MESH"}
    atlas=json.loads((ROOT/spec["repository"]/"res/atlases/vanilla.atlas").read_text())
    colors={b["name"]:b["colour"] for b in atlas["blocks"]}
    old_config=json.loads((ROOT/"relics/colossus/design/colossus-v4-1-frame.json").read_text())
    for name,state in old_config["materials"].items():
        target=spec["replacements"].get(state,state)
        color=colors[target]
        mat=bpy.data.materials.get(name)
        if mat: mat.diffuse_color=(*(color[c] for c in ("r","g","b")),1)
    for zone in zones:
        empty=bpy.data.objects.new(f"Salvage mask | {zone['name']}",None)
        bpy.context.collection.objects.link(empty)
        empty.location=xyz(zone["center_source"])
        empty.empty_display_type="SPHERE";empty.empty_display_size=zone["radius_source"]
        empty["note"]="Guide only. Exact retained block mask is recorded in the design JSON and applied after export."
        empty["retained_blocks"]=zone["blocks"]
    bpy.context.view_layer.update()
    assert all(fingerprint(bpy.data.objects[n])==digest for n,digest in meshes.items())
    bpy.context.scene["design_name"]="Colossus V4.1 / shape-locked material study"
    bpy.context.scene["palette_note"]="Bulk-palette source view; authoritative localized metal masks are applied directly to the accepted V4.1 NBT grid. Do not re-voxelize."
    bpy.ops.wm.save_as_mainfile(filepath=str(out/f"{stem}-source.blend"))
    before,after=Counter(blocks.values()),Counter(result.values())
    def economy(counts):
        return {"copper_blocks":sum(n for state,n in counts.items() if metal_family(state)=="copper"),
                "raw_iron_blocks":counts["minecraft:raw_iron_block"],
                "raw_iron_items":counts["minecraft:raw_iron_block"]*9}
    baseline.pop("visual_acceptance",None)
    baseline.update(name="Colossus V4.1 / material and salvage study",revision="Palette-only derivative; pending visual and balance review")
    baseline["material_study"]={"config":str(CONFIG.relative_to(ROOT)).replace("\\","/"),
        "config_sha256":hashlib.sha256(CONFIG.read_text(encoding="utf-8").encode("utf-8")).hexdigest(),
        "sources":{str(p.relative_to(ROOT)).replace("\\","/"):hashlib.sha256(p.read_bytes()).hexdigest() for p in (nbt,blend,schem)},
        "method":"Direct block-state remap of accepted V4.1. No geometry regeneration or voxelization.",
        "source_mesh_fingerprints":meshes,"salvage_zones":zones,"replacements":spec["replacements"],
        "before_counts":dict(before),"after_counts":dict(after),"before_economy":economy(before),"after_economy":economy(after),
        "changed_states":sum(blocks[p]!=result[p] for p in blocks),"occupied_positions_unchanged":True,
        "source_preview_note":"Editable source shows the bulk palette. Non-rendering empties mark salvage areas; exact voxel masks are post-export.",
        "source_offset":offset,"tiles":len(manifest["tiles"])}
    (out/f"{stem}.design.json").write_text(json.dumps(baseline,indent=2)+"\n")
    print(json.dumps({"before":economy(before),"after":economy(after),"zones":[(z['name'],z['blocks']) for z in zones]},indent=2))


if __name__=="__main__": main()
