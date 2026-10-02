"""V4 skull: preserve anatomy, replace the plinth by broken deposits, four palettes."""
import copy
import hashlib
import json
from pathlib import Path
import sys

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from create_colossus_v4 import fingerprint
from create_titan_skull_v2 import bounds
from relic_v4_terrain import skull_height, build_deposits

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "relics/titan-skull/design"
BASE = DESIGN / "generated/titan-skull-v3"
SOURCE = BASE / "titan-skull-v3-source.blend"
SPEC = DESIGN / "variants/titan-skull-v4.json"


def main():
    spec = json.loads(SPEC.read_text())
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    original = json.loads((BASE / "titan-skull-v3.design.json").read_text())
    for variant, settings in spec["variants"].items():
        bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
        for obj in list(bpy.context.scene.objects):
            if obj.get("asset_component") == "exported_terrain":
                bpy.data.objects.remove(obj, do_unlink=True)
        anatomy = {obj.name: fingerprint(obj) for obj in bpy.context.scene.objects if obj.type == "MESH"}
        for name, color in {"bone":"ded5bc", "worn":"eeeae1", "mineral":"978371",
                            "earth":"76513d", "moss":"73734a", "root":"736043"}.items():
            mat=bpy.data.materials.get(name)
            if mat:
                mat.diffuse_color=(*[int(color[i:i+2],16)/255 for i in (0,2,4)],1)
        for name, color in zip(("terrain_top","terrain_patch","terrain_fill"),settings["colors"]):
            mat=bpy.data.materials.new(name)
            mat.diffuse_color=(*[int(color[i:i+2],16)/255 for i in (0,2,4)],1)
        build_deposits(skull_height,list(range(-64,77,2)),list(range(-30,165,2)))
        bpy.context.view_layer.update()
        require_preserved = {name:fingerprint(bpy.data.objects[name]) for name in anatomy}
        assert require_preserved == anatomy, "Skull/spine geometry changed"
        low, high = bounds([o for o in bpy.context.scene.objects if o.type == "MESH"])
        scale = 79/(high[2]-low[2])
        assert abs(scale-original["blocks_per_source_unit"]) < 1e-6
        stem=f"titan-skull-v4-{variant}"
        out=DESIGN/"generated"/stem
        out.mkdir(parents=True,exist_ok=True)
        metadata=copy.deepcopy(original)
        metadata.pop("exported_mound",None)
        metadata.update(name=f"Titan Skull V4 / {settings['label']}", source_bounds_blender=[low,high],
                        source_v3_sha256=source_hash,preserved_anatomy_objects=anatomy)
        for vertebra in metadata["spine"]["vertebrae"]:
            x,_,z=vertebra["center_source"]
            vertebra["ground_source_y"]=skull_height(x,z)
            vertebra.pop("source_vertices_below_terrain_fraction",None)
        metadata["spine"]["bone_materials"]=["minecraft:bone_block","minecraft:calcite","minecraft:dripstone_block"]
        metadata["deposits_v4"]={"variant":variant,"bottom_source_y":-8,"slice_spacing":.7,
            "terrain_materials":list(set(settings["materials"].values())),
            "gap_source_z":[54,131],"no_continuous_base":True,
            "solid_probes_source":[[1,3,25],[22,3,90],[29,0,142]],
            "suggested_biomes":settings["suggested_biomes"],"runtime_selection_implemented":False}
        metadata["interpretation"]="Preserved skull and broken spine; light fossil palette; separate tapered deposits with native-terrain gaps and no stone rim."
        (out/f"{stem}.design.json").write_text(json.dumps(metadata,indent=2)+"\n",encoding="utf-8")
        config={"repository":".work/ObjToSchematic","commit":"b611b52c7a87cad99127908598bab019fe9e7c3f",
            "input":f"relics/titan-skull/design/generated/{stem}/{stem}.obj",
            "output":f"relics/titan-skull/design/generated/{stem}/{stem}.schem","height":80,
            "title":f"TITAN SKULL V4 / {variant.upper()}",
            "subtitle":"Broken deposits / no stone rim / same skull and spine / biome-specific ground",
            "reference":original["reference"],"materials":{**spec["bone_materials"],**settings["materials"]},
            "material_proxies":spec["material_proxies"],
            "view_labels":["01 / Editable source", "02 / Actual NBT / front", "03 / Actual NBT / side", "04 / Actual NBT / rear"],
            "review_footer":"NBT rendered in Blender. Local deposits are exported; staging plane is illustrative. Grass texture/tint is approximated.",
            "preview":{"front":[-180,250,175],"other":[260,-70,170],"back":[110,-250,200],
                       "landscape":"v4-deposits","ground_color":settings["ground_color"],
                       "grass_tint":[1.18,1.08,.6] if variant=="dry" else [1,1,1],
                       "camera_source":[-150,102,-155],"target_source":[6,24,48]}}
        if variant in ("meadow","dry"):
            config["covered_replacements"]={"minecraft:grass_block[snowy=false]":"minecraft:dirt"}
        if variant == "sand": config["unsupported_replacements"]={"minecraft:sand":"minecraft:sandstone"}
        if variant == "rock": config["unsupported_replacements"]={"minecraft:gravel":"minecraft:stone"}
        (DESIGN/f"{stem}.json").write_text(json.dumps(config,indent=2)+"\n",encoding="utf-8")
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.wm.obj_export(filepath=str(out/f"{stem}.obj"),forward_axis="NEGATIVE_Z",up_axis="Y",
            export_selected_objects=True,export_triangulated_mesh=True,export_materials=True)
        bpy.context.scene["design_name"]=metadata["name"]
        bpy.ops.wm.save_as_mainfile(filepath=str(out/f"{stem}-source.blend"))
        print(f"{stem}: {len(anatomy)} anatomy meshes preserved; {low} / {high}")


if __name__ == "__main__":
    main()
