"""Independent shape/state invariants for the post-export Colossus material study."""
from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path

from colossus_materials import metal_family,NEIGHBORS
from inspect_colossus_v4 import verify
from inspect_ots_result import read_structure,require
from schem_to_nbt import read_schematic

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/"relics/colossus/design/studies/colossus-v4-1-materials.json"


def support_check(old,blocks,removed,design):
    def labels(positions):
        unseen=set(positions);label={};sizes=[]
        while unseen:
            seed=next(iter(unseen));unseen.remove(seed);pending=[seed];count=0
            while pending:
                p=pending.pop();label[p]=len(sizes);count+=1
                x,y,z=p
                for q in ((x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)):
                    if q in unseen: unseen.remove(q);pending.append(q)
            sizes.append(count)
        return label,sizes
    before,before_sizes=labels(old)
    after,after_sizes=labels(blocks.keys()-removed)
    descendants={}
    for p,label in after.items(): descendants.setdefault(before[p],set()).add(label)
    require(all(len(ids)==1 for ids in descendants.values()),"Mining splits an existing connected component")
    low,high=design["source_bounds_blender"];scale=design["blocks_per_source_unit"]
    protected={p for p in old if p[1]/scale+low[2]>=75}
    require(not protected & removed,"Mining cuts the protected upper chest, neck or head")
    main=max(range(len(before_sizes)),key=lambda i:before_sizes[i])
    main_after=next(iter(descendants[main]))
    head={p for p in protected if p[1]/scale+low[2]>105 and before[p]==main}
    require(len(head)>1000 and all(after[p]==main_after for p in head),"Head support missing")
    require(any(label==main_after and p[1]<design["ground_level_nbt_approx"] for p,label in after.items()),
            "Head does not connect to buried body")
    return {"original_face_components":len(before_sizes),"remaining_face_components":len(after_sizes),
            "new_component_splits":0,"head_connected_to_buried_body":True,
            "protected_head_neck_upper_bridge_blocks":len(protected),
            "main_component_before":before_sizes[main],"main_component_after":after_sizes[main_after],
            "note":"Strict 6-neighbor conservation relative to baseline; original disconnected raster fragments are retained or wholly salvaged, never newly split. This is not a load simulation."}


def check(config=CONFIG):
    global CONFIG
    CONFIG=config.resolve()
    spec=json.loads(CONFIG.read_text())
    output=ROOT/spec["output"];out=output.parent;stem=output.stem
    design=json.loads((out/f"{stem}.design.json").read_text())
    study=design["material_study"]
    require(hashlib.sha256(CONFIG.read_text(encoding="utf-8").encode("utf-8")).hexdigest()==study["config_sha256"],
            "Study config changed since generation")
    for path,sha in study["sources"].items():
        require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,f"Source changed: {path}")
    original,old=read_structure(ROOT/spec["source_nbt"])
    root,blocks=read_structure(out/f"{stem}.nbt")
    size,schematic,version,offset=read_schematic(output.read_bytes(),"omit")
    require(list(size)==root["size"]==original["size"],"Dimensions changed")
    require(blocks.keys()==old.keys(),"Occupied block positions changed")
    require(blocks==schematic,"Schematic and NBT states differ")
    require(version==root["DataVersion"]==original["DataVersion"],"DataVersion changed")
    require(offset==read_schematic((ROOT/spec["source_schematic"]).read_bytes(),"omit")[3],"Schematic offset changed")
    require(root["entities"]==original["entities"],"Entities changed")
    retained=set()
    for zone in study["salvage_zones"]:
        positions=set(map(tuple,zone["positions_nbt"]))
        require(not retained & positions,"Salvage regions overlap")
        require(0<len(positions)==zone["blocks"]<=zone.get("max_blocks",zone["blocks"]),"Invalid salvage quantity")
        if "panel_salvage" not in spec:
            visited=set();pending=[next(iter(positions))]
            while pending:
                p=pending.pop()
                if p in visited: continue
                visited.add(p)
                pending.extend(q for d in NEIGHBORS if (q:=tuple(a+b for a,b in zip(p,d))) in positions and q not in visited)
            require(visited==positions,"Salvage is dispersed instead of face-connected")
        require(all(blocks[p]==old[p] and metal_family(blocks[p])==zone["family"] for p in positions),"Retained metal changed")
        retained|=positions
    for p,old_state in old.items():
        expected=old_state if p in retained else spec["replacements"].get(old_state,old_state)
        require(blocks[p]==expected,f"Unexpected material edit at {p}")
    require({p for p,s in blocks.items() if metal_family(s)}==retained,"Valuable metal outside salvage sites")
    require(dict(Counter(blocks.values()))==study["after_counts"],"Inventory stale")
    require(dict(Counter(old.values()))==study["before_counts"],"Baseline inventory stale")
    support=None
    if "panel_salvage" in spec:
        copper=sum(metal_family(s)=="copper" for s in blocks.values())
        raw_iron=9*sum(metal_family(s)=="iron" for s in blocks.values())
        require(copper<spec["resource_limits_exclusive"]["copper_blocks"],"Copper budget exceeded")
        require(raw_iron<spec["resource_limits_exclusive"]["raw_iron_items"],"Raw iron budget exceeded")
        support=support_check(old,blocks,retained,design)
    manifest=json.loads((out/f"{stem}.manifest.json").read_text())
    recovered={}
    for tile in manifest["tiles"]:
        tile_root,tile_blocks=read_structure(out/tile["path"])
        require(tile_root["size"]==tile["size"],"Tile dimensions differ")
        for p,state in tile_blocks.items():
            q=tuple(a+b for a,b in zip(p,tile["origin"]))
            require(q not in recovered,"Overlapping tiles")
            recovered[q]=state
    require(recovered==blocks,"Tile reconstruction differs")
    shapes=verify(design,blocks)
    report={"size":list(size),"blocks":len(blocks),"palette_entries":len(set(blocks.values())),
        "tiles":len(manifest["tiles"]),"data_version":version,"in_game_tested":False,
        "geometry":{"identical_occupied_positions":True,"added_positions":0,"removed_positions":0,
            "moved_positions":0,"identical_empty_space":True,"preserved_blender_meshes":len(study["source_mesh_fingerprints"]),
            "unchanged_nonmetal_states":sum(metal_family(s) is None for s in old.values())},
        "changed_states":sum(s!=old[p] for p,s in blocks.items()),
        "salvage":{"zones":len(study["salvage_zones"]),"retained_metal_blocks":len(retained),
            "blocks_remaining_after_metal_removal":len(blocks)-len(retained),
            "remaining_percent":100*(1-len(retained)/len(blocks)),
            "before":study["before_economy"],"after":study["after_economy"]},
        "colossus_v4":shapes,
        "checks":["baseline hashes","identical position set, bounds and voids","exact schematic/NBT equality",
            "only metal states changed","no metal outside designated salvage masks","lossless tile reconstruction"],
        "schematic_sha256":hashlib.sha256(output.read_bytes()).hexdigest(),
        "nbt_sha256":hashlib.sha256((out/f"{stem}.nbt").read_bytes()).hexdigest(),
        "source_blend_sha256":hashlib.sha256((out/f"{stem}-source.blend").read_bytes()).hexdigest()}
    if support: report["post_salvage_support"]=support
    (out/"verification.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    return report


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config",type=Path,default=CONFIG)
    check(parser.parse_args().config)
