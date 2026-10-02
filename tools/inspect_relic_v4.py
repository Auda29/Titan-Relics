"""Offline checks and paired review sheets for Titan Skull V4 and Obelisk V4."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from inspect_ots_result import read_structure, require

ROOT=Path(__file__).resolve().parents[1]
SKULL=ROOT/"relics/titan-skull/design/generated"
OBELISK=ROOT/"relics/obelisk/design/generated"


def source_mapping(design):
    low,high=design["source_bounds_blender"]
    scale=design.get("blocks_per_source_unit",(design["height_target_blocks"]-1)/(high[2]-low[2]))
    def source(p): return (p[0]/scale+low[0],p[1]/scale+low[2],p[2]/scale-high[1])
    def local(p): return (round((p[0]-low[0])*scale),round((p[1]-low[2])*scale),round((p[2]+high[1])*scale))
    return source,local


def check_surface_states(blocks):
    floating=[p for p,s in blocks.items() if s in ("minecraft:sand","minecraft:gravel") and (p[0],p[1]-1,p[2]) not in blocks]
    covered=[p for p,s in blocks.items() if s.startswith("minecraft:grass_block") and (p[0],p[1]+1,p[2]) in blocks]
    require(not floating, f"Unsupported sand/gravel: {len(floating)}")
    require(not covered, f"Buried grass: {len(covered)}")


def skull_check(design,blocks):
    source,local=source_mapping(design)
    terrain=set(design["deposits_v4"]["terrain_materials"])
    terrain_blocks={p:s for p,s in blocks.items() if s in terrain}
    require(0<len(terrain_blocks)<146895,"Deposits must be materially smaller than V3's 244,825 terrain blocks")
    for z in design["deposits_v4"]["gap_source_z"]:
        require(not any(abs(source(p)[2]-z)<.8 for p in terrain_blocks),"A continuous terrain platform bridges a deposit gap")
    columns=defaultdict(list)
    for x,y,z in terrain_blocks: columns[(x,z)].append(y)
    holes=sum((x,y,z) not in blocks for (x,z),ys in columns.items() for y in range(min(ys),max(ys)+1))
    require(holes==0,f"Terrain interior contains {holes} missing column cells")
    check_surface_states(blocks)
    bone=set(design["spine"]["bone_materials"])
    pts=[source(p) for p,state in blocks.items() if state in bone]
    vertebrae=[]
    for v in design["spine"]["vertebrae"]:
        x,_,z=v["center_source"];surface=v["ground_source_y"]
        near=[p for p in pts if abs(p[0]-x)<=16 and abs(p[2]-z)<=5]
        buried=sum(p[1]<surface-1 for p in near)
        exposed=sum(surface+1<p[1]<surface+18 for p in near)
        require(buried>25 and exposed>100,f"Vertebra {v['index']} no longer partly buried")
        vertebrae.append({"index":v["index"],"buried_samples":buried,"exposed_samples":exposed})
    require(all(not any(abs(p[2]-z)<.6 for p in pts) for z in design["spine"]["fracture_probe_planes_source_z"]),
            "Bone bridges an intended spinal fracture")
    rear=local(design["rear_wall_probe_source"])
    require(all(any(blocks.get((rear[0]+dx,rear[1]+dy,rear[2]+dz)) in bone for dz in range(-5,6))
                for dx in (-5,0,5) for dy in (-5,0,5)),"Rear skull wall missing")
    require(hashlib.sha256((SKULL/"titan-skull-v3/titan-skull-v3-source.blend").read_bytes()).hexdigest()==design["source_v3_sha256"],
            "Skull source baseline changed")
    return {"variant":design["deposits_v4"]["variant"],"terrain_blocks":len(terrain_blocks),
            "terrain_reduction_vs_v3_percent":round(100*(1-len(terrain_blocks)/244825),2),
            "solid_columns_checked":len(columns),"missing_column_cells":holes,
            "open_terrain_gap_planes":design["deposits_v4"]["gap_source_z"],
            "anatomy_meshes_preserved":len(design["preserved_anatomy_objects"]),
            "vertebrae":vertebrae,"unsupported_falling_blocks":0,"buried_grass_blocks":0}


def obelisk_check(design,blocks,report):
    source,local=source_mapping(design)
    cx,ground,cz=local((0,0,0))
    require(report.get("filled_voxels",0)>50000,"Solid-core infill was not applied")
    require(all((cx+dx,y,cz+dz) in blocks for dx in range(-3,4) for dz in range(-3,4) for y in range(185)),
            "Monument core is not continuously solid")
    require(all(local((x,0,z)) in blocks for x in (-8,8) for z in (-8,8)),"Square base lost")
    require(all(local((x,175,z)) in blocks for x,z in [(-9,0),(9,0),(0,-9),(0,9)]),"Rotated crown tips missing")
    require(all(local((x,175,z)) not in blocks for x in (-9,9) for z in (-9,9)),"Crown lost antiprism rotation")
    weather=design["obelisk_v4"]
    require(0<weather["volume_removed_percent"]<weather.get("maximum_damage_percent",1) and weather["upright"],"Damage makes the monument unstable")
    # Core-only horizontal slices, excluding the outlying foundation and dunes.
    counts=Counter(p[1] for p in blocks if abs(source(p)[0])<=12 and abs(source(p)[2])<=12)
    require(min(counts[y] for y in range(ground,185))>180,"Monument has a broken or constricted layer")
    check_surface_states(blocks)
    require(hashlib.sha256((OBELISK/"obelisk-v3/obelisk-v3-source.blend").read_bytes()).hexdigest()==design["source_v3_sha256"],
            "Obelisk source baseline changed")
    cracks=[]
    if weather.get("cracks"):
        _,baseline=read_structure(OBELISK/"obelisk-v3/obelisk-v3.nbt")
        base_design=json.loads((OBELISK/"obelisk-v3/obelisk-v3.design.json").read_text())
        _,base_local=source_mapping(base_design)
        for crack in weather["cracks"]:
            removed=0
            backed=0
            n=crack["normal_source"]
            for sample in crack["surface_samples_source"]:
                q=local(sample)
                removed+=sum((q[0]+dx,q[1]+dy,q[2]+dz) not in blocks and
                    base_local(source((q[0]+dx,q[1]+dy,q[2]+dz))) in baseline
                    for dx in range(-1,2) for dy in range(-1,2) for dz in range(-1,2))
                backed+=local([a-4*b for a,b in zip(sample,n)]) in blocks
            require(removed>5,"A designed crack was sealed by voxelization")
            require(backed==len(crack["surface_samples_source"]),"A crack penetrates too deeply")
            cracks.append({"removed_surface_samples":removed,"solid_backing_samples":backed})
        if not weather.get("unpainted_damage"):
            require(not any(s in ("minecraft:terracotta","minecraft:brown_terracotta") for s in blocks.values()),
                    "Large contrasting tiger patches remain")
        require(hashlib.sha256((OBELISK/"obelisk-v4/obelisk-v4-source.blend").read_bytes()).hexdigest()==design["source_v4_sha256"],
                "V4 source baseline changed")
    missing=[]
    if weather.get("unpainted_damage"):
        allowed=set(weather["monolith_materials"])
        require(all(s in allowed for p,s in blocks.items() if source(p)[1]>8),
                "Contrasting fill or pale blocks remain on the monument")
        _,previous=read_structure(OBELISK/"obelisk-v4-1/obelisk-v4-1.nbt")
        for chunk in weather["missing_chunks"]:
            q=local(chunk["center_source"])
            removed=sum((q[0]+dx,q[1]+dy,q[2]+dz) in previous and (q[0]+dx,q[1]+dy,q[2]+dz) not in blocks
                for dx in range(-5,6) for dy in range(-8,9) for dz in range(-5,6))
            require(removed>20,"Missing chunk was filled during export")
            missing.append(removed)
        require(hashlib.sha256((OBELISK/"obelisk-v4-1/obelisk-v4-1-source.blend").read_bytes()).hexdigest()==design["source_v4_1_sha256"],
                "V4.1 source baseline changed")
    return {"continuous_core_prism":[7,185,7],"filled_voxels":report["filled_voxels"],
            "square_base_and_rotated_crown_checked":True,"shallow_chips":len(weather["shallow_chips"]),
            "source_volume_removed_percent":weather["volume_removed_percent"],"foundation_fragments":3,
            "nominal_ground_y":ground,"unsupported_sand_blocks":0,
            **({"open_cracks":cracks,"preserved_v4_scenery_objects":len(design["preserved_v4_objects"])} if cracks else {}),
            **({"missing_chunk_removed_blocks":missing,"unpainted_damage":True} if missing else {})}


def compare_skulls():
    baseline=None
    counts={}
    for variant in ("meadow","dry","sand","rock"):
        stem=f"titan-skull-v4-{variant}";folder=SKULL/stem
        root,blocks=read_structure(folder/f"{stem}.nbt")
        design=json.loads((folder/f"{stem}.design.json").read_text())
        terrain=set(design["deposits_v4"]["terrain_materials"])
        bones={p:s for p,s in blocks.items() if s not in terrain}
        current=(root["size"],set(blocks),bones)
        if baseline is None: baseline=current
        require(current==baseline,"Terrain palettes changed anatomy or occupied positions")
        counts[variant]=Counter(blocks.values())
    require(counts["meadow"]["minecraft:grass_block[snowy=false]"]>3*counts["dry"]["minecraft:grass_block[snowy=false]"],
            "Dry ground does not differ meaningfully from meadow")
    for variant in counts:
        path=SKULL/f"titan-skull-v4-{variant}/verification.json"
        report=json.loads(path.read_text())
        report["variant_comparison"]={"variants":list(counts),"identical_anatomy_and_occupied_positions":True}
        path.write_text(json.dumps(report,indent=2)+"\n")
    print("Four skull variants: identical bone states and coordinates; distinct supported terrain palettes.")


def sheets():
    from PIL import Image,ImageDraw,ImageFont
    def font(n,bold=False):
        return ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",n)
    def panel(sheet,path,box,title,note):
        x,y,w,h=box
        pic=Image.open(path).convert("RGB")
        pic.thumbnail((w,h),Image.Resampling.LANCZOS)
        sheet.paste(pic,(x+(w-pic.width)//2,y+(h-pic.height)//2))
        draw=ImageDraw.Draw(sheet)
        draw.text((x,y+h+8),title,font=font(29,True),fill="#293934")
        draw.text((x,y+h+49),note,font=font(23),fill="#54615a")
    skull=Image.new("RGB",(2400,2700),"#eee9de")
    draw=ImageDraw.Draw(skull)
    draw.text((45,25),"TITAN SKULL V4 / BROKEN DEPOSITS & FOUR GROUND PALETTES",font=font(40,True),fill="#293934")
    draw.text((45,86),"Same skull and nine vertebrae / lighter fossils / native-terrain gaps / no stone rim",font=font(27),fill="#54615a")
    for i,(variant,title,note) in enumerate([
        ("meadow","Meadow / grassy earth","Grass surface with exposed earth patches"),
        ("dry","Dry ground / savanna","Mostly coarse earth with sparse grass"),
        ("sand","Desert / sand","Sand over supported sandstone deposits"),
        ("rock","Stony terrain / stone and gravel","No separate rock border or plinth")]):
        panel(skull,SKULL/f"titan-skull-v4-{variant}/05-blocks-landscape.png",
              (40+i%2*1180,150+i//2*800,1140,680),title,note)
    panel(skull,SKULL/"titan-skull-v4-dry/09-deposits-rear.png",(40,1750,1140,680),
          "Rear / partly buried broken spine","Two open terrain gaps interrupt the old continuous mound")
    panel(skull,SKULL/"titan-skull-v4-dry/10-deposits-overhead.png",(1220,1750,1140,680),
          "Overhead / irregular deposits","Tapered edges and native-ground windows; no enclosing base")
    draw.text((45,2560),"Actual exported NBT in Blender; surrounding ground is illustrative. Grass texture/tint is approximated.",font=font(24),fill="#54615a")
    draw.text((45,2610),"Four material exports, not automatic biome adaptation. In-game terrain placement remains to be tested.",font=font(24),fill="#54615a")
    path=SKULL/"titan-skull-v4-dry/titan-skull-v4-variants-review.png"
    skull.save(path);print(path)
    comparison=Image.new("RGB",(2400,1250),"#eee9de")
    draw=ImageDraw.Draw(comparison)
    draw.text((45,25),"TITAN SKULL / V3 TO V4",font=font(46,True),fill="#293934")
    panel(comparison,SKULL/"titan-skull-v3/05-blocks-landscape.png",(40,120,1140,900),
          "V3 / Continuous grassy hill","Original fossil palette and exported stone-edged mound")
    panel(comparison,SKULL/"titan-skull-v4-dry/05-blocks-landscape.png",(1220,120,1140,900),
          "V4 / Interrupted dry deposits","Same anatomy; lighter fossils; 52.44% fewer terrain blocks")
    draw.text((45,1190),"Actual NBT in illustrative Blender scenery. Different framing; this is a design comparison, not a scale measurement.",font=font(23),fill="#54615a")
    path=SKULL/"titan-skull-v4-dry/titan-skull-v4-changes-review.png"
    comparison.save(path);print(path)
    sheet=Image.new("RGB",(2400,2300),"#eee9de");draw=ImageDraw.Draw(sheet)
    draw.text((45,25),"OBELISK V4 / WEATHERED, UPRIGHT & STABLE",font=font(46,True),fill="#293934")
    draw.text((45,90),"Antiprism and height retained / four shallow chips / asymmetric sand and three foundation fragments",font=font(26),fill="#54615a")
    panel(sheet,OBELISK/"obelisk-v3/02-blocks-front.png",(40,155,1140,925),"V3 / Original monument","Same standing monument, original surface palette")
    panel(sheet,OBELISK/"obelisk-v4/02-blocks-front.png",(1220,155,1140,925),"V4 / Weathered surface","Coherent mineral zones, no deep cracks or leaning")
    panel(sheet,OBELISK/"obelisk-v4/05-blocks-landscape.png",(40,1200,1140,860),"V4 / In illustrative sand terrain","Entire monument; solid core and rotated crown retained")
    panel(sheet,OBELISK/"obelisk-v4/08-foot-detail.png",(1220,1200,1140,860),"V4 / Foundation inspection crop","Scattered remnants and sand; no platform or encircling ring")
    draw.text((45,2200),"Actual NBT rendered in Blender, not in-game. Local sand and fragments exported; surrounding plane is a preview aid.",font=font(23),fill="#54615a")
    path=OBELISK/"obelisk-v4/obelisk-v4-changes-review.png"
    sheet.save(path);print(path)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sheets",action="store_true")
    args=parser.parse_args()
    compare_skulls()
    if args.sheets: sheets()
