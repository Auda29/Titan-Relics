"""Check the real ObjToSchematic round trip and assemble the rendered review sheet.

Requires Pillow for the contact sheet, not for --check-only.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from relic_assets import decode_nbt
from schem_to_nbt import read_schematic

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "relics/colossus/design/generated/ots"
STEM = "colossus"
CONFIG = {}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_structure(path):
    root = decode_nbt(path.read_bytes())
    palette = []
    for state in root["palette"]:
        properties = state.get("Properties", {})
        suffix = "["+",".join(f"{k}={v}" for k, v in sorted(properties.items()))+"]" if properties else ""
        palette.append(state["Name"]+suffix)
    blocks = {}
    for entry in root["blocks"]:
        pos = tuple(entry["pos"])
        require(pos not in blocks, f"Duplicate position in {path}: {pos}")
        require(all(0 <= v < n for v, n in zip(pos, root["size"])), f"Out of bounds: {pos}")
        blocks[pos] = palette[entry["state"]]
    return root, blocks


def check():
    size, schematic, version, _ = read_schematic((OUT / f"{STEM}.schem").read_bytes(), "omit")
    root, blocks = read_structure(OUT / f"{STEM}.nbt")
    require(tuple(root["size"]) == size, "Dimensions changed during conversion")
    require(root["DataVersion"] == version, "DataVersion changed during conversion")
    require(blocks == schematic, "Schematic/NBT blocks differ")
    report = json.loads((OUT / f"{STEM}.ots.json").read_text())
    for filename, expected in [(ROOT / report["input"], report["source_sha256"]),
                               (OUT / f"{STEM}.schem", report["schematic_sha256"])]:
        require(hashlib.sha256(filename.read_bytes()).hexdigest() == expected, f"Stale report for {filename}")
    require(dict(Counter(blocks.values())) == report["blocks"], "Reported palette counts differ")
    require(set(blocks.values()) <= set(report["materials"].values()), "Unexpected block outside chosen palette")
    manifest = json.loads((OUT / f"{STEM}.manifest.json").read_text())
    recovered = {}
    for tile in manifest["tiles"]:
        tile_root, entries = read_structure(OUT / tile["path"])
        require(tile_root["size"] == tile["size"], "Tile dimensions differ")
        for pos, state in entries.items():
            absolute = tuple(v+o for v, o in zip(pos, tile["origin"]))
            require(absolute not in recovered, "Overlapping tile blocks")
            recovered[absolute] = state
    require(recovered == blocks, "Tiles do not reconstruct the complete NBT")
    summary = {
        "size": list(size), "blocks": len(blocks), "palette_entries": len(set(blocks.values())),
        "tiles": len(manifest["tiles"]), "data_version": version,
        "schematic_sha256": report["schematic_sha256"],
        "nbt_sha256": hashlib.sha256((OUT / f"{STEM}.nbt").read_bytes()).hexdigest(),
        "checks": ["source/export hashes", "all block coordinates and states preserved",
                   "palette counts", "bounds", "lossless tile reconstruction"],
        "in_game_tested": False,
    }
    design_path = OUT / f"{STEM}.design.json"
    if design_path.exists():
        design = json.loads(design_path.read_text())
        if "buried_hip" in design:
            ground = design["ground_level_nbt_approx"]
            below = {pos: state for pos, state in blocks.items() if pos[1] < ground}
            require(design["height_target_blocks"] == size[1], "Export height would change the calibrated body scale")
            require(ground > 50 and len(below) > 10000, "Buried waist is missing or too shallow")
            reference = design["scale_reference"]
            original_scale = (reference["original_export_height"]-1)/reference["original_source_height"]
            scale_change = design["blocks_per_source_unit"]/original_scale-1
            require(abs(scale_change) < .005, "Above-ground body was rescaled instead of extended downward")
            summary["buried_hip"] = {"nominal_surface_y": ground, "blocks_below_surface": len(below),
                                     "depth_below_surface": ground-min(p[1] for p in below),
                                     "scale_change_percent": round(scale_change*100, 4)}
        if design.get("solid_core"):
            cx, cz = size[0]//2, size[2]//2
            require(report.get("filled_voxels", 0) > 0, "Solid infill was not applied")
            require(all((x, y, z) in blocks for x in range(cx-3, cx+4)
                        for y in range(size[1]) for z in range(cz-3, cz+4)), "Solid core contains voids")
            ground = design["ground_level_nbt_approx"]
            summary["solid_core"] = {"filled_voxels": report["filled_voxels"],
                                     "continuous_checked_prism": [7, size[1], 7],
                                     "ground_level": ground,
                                     "blocks_below_ground": sum(p[1] < ground for p in blocks)}
        if "antiprism" in design:
            ground = design["ground_level_nbt_approx"]
            cx, cz = size[0]//2, size[2]//2
            top = size[1]-2
            # At the base the four corners exist; the rotated crown loses those
            # corners but retains its four axis tips. Inspect the actual blocks.
            require(all((cx+dx, ground, cz+dz) in blocks for dx in (-8, 8) for dz in (-8, 8)),
                    "Square antiprism base is missing")
            require(all((cx+dx, top, cz+dz) not in blocks for dx in (-8, 8) for dz in (-8, 8)),
                    "Crown retained rectangular corners instead of rotated facets")
            require(all((cx+dx, top, cz+dz) in blocks for dx, dz in [(-9, 0), (9, 0), (0, -9), (0, 9)]),
                    "Rotated crown tips are missing")
            below = sum(p[1] < ground for p in blocks)
            require(ground == 8 and below/len(blocks) < .08, "Foot is not shallow")
            require(size[1] == design["height_target_blocks"], "Antiprism height changed")
            summary["antiprism"] = {"base_and_rotated_crown_checked": True,
                                     "buried_layers": ground, "blocks_below_ground": below,
                                     "buried_block_percent": round(100*below/len(blocks), 2)}
        if "cavity_probes_source" in design:
            low, high = design["source_bounds_blender"]
            scale = design["blocks_per_source_unit"]
            def local(point):
                x, y, z = point
                return (round((x-low[0])*scale), round((y-low[2])*scale), round((z+high[1])*scale))
            probes = [local(p) for p in design["cavity_probes_source"]]
            require(all((p[0]+dx, p[1]+dy, p[2]+dz) not in blocks for p in probes
                        for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1)),
                    "An eye, nose, or mouth cavity is obstructed")
            start, end = probes[0], probes[2]
            require(start[:2] == end[:2], "Mouth probes must define a straight inspection channel")
            require(all((start[0]+dx, start[1]+dy, z) not in blocks
                        for dx in range(-2, 3) for dy in range(-2, 3)
                        for z in range(max(0, start[2]), end[2]+1)), "Mouth inspection channel is blocked")
            ground = design["ground_level_nbt_approx"]
            summary["skull_cavities"] = {"empty_3x3x3_probes": probes,
                                        "mouth_channel_cross_section": [5, 5],
                                        "ground_level": ground,
                                        "blocks_below_ground": sum(p[1] < ground for p in blocks),
                                        "terrain_clearing_defined": False}
            if "exported_mound" in design:
                terrain = set(design["exported_mound"]["terrain_materials"])
                solid_probes = [local(p) for p in design["exported_mound"]["solid_probes_source"]]
                require(all((p[0]+dx, y, p[2]+dz) in blocks for p in solid_probes
                            for dx in range(-2, 3) for dz in range(-2, 3)
                            for y in range(2, p[1]+2)), "Exported mound contains an empty interior column")
                terrain_count = sum(state in terrain for state in blocks.values())
                require(terrain_count > 50000 and terrain <= set(blocks.values()), "Exported terrain materials are missing")
                rear = local(design["rear_wall_probe_source"])
                require(all(any(blocks.get((rear[0]+dx, rear[1]+dy, rear[2]+dz)) in
                                    {"minecraft:dripstone_block", "minecraft:sandstone", "minecraft:tuff"}
                                for dz in range(-5, 6)) for dx in (-5, 0, 5) for dy in (-5, 0, 5)),
                        "Rounded posterior skull wall is missing")
                ratio = design["colossus_head_reference"]["skull_to_helmet_height_ratio"]
                require(1 <= ratio <= 1.3, "Skull is no longer close to Colossus-head scale")
                summary["exported_mound"] = {"terrain_blocks": terrain_count,
                                              "solid_column_groups_checked": len(solid_probes),
                                              "rear_wall_rays_checked": 9,
                                              "skull_height_blocks_approx": design["skull_height_blocks_approx"],
                                              "skull_to_helmet_height_ratio": ratio}
                if "spine" in design:
                    spine = design["spine"]
                    bone_materials = set(spine["bone_materials"])
                    bone_points = [(p[0]/scale+low[0], p[1]/scale+low[2], p[2]/scale-high[1])
                                   for p, state in blocks.items() if state in bone_materials]
                    vertebra_checks = []
                    for vertebra in spine["vertebrae"]:
                        x, _, z = vertebra["center_source"]
                        surface = vertebra["ground_source_y"]
                        nearby = [p for p in bone_points if abs(p[0]-x) <= 16 and abs(p[2]-z) <= 5]
                        below = sum(p[1] < surface-1 for p in nearby)
                        above = sum(surface+1 < p[1] < surface+18 for p in nearby)
                        require(below > 30 and above > 100, f"Vertebra {vertebra['index']} is missing or not partly buried")
                        vertebra_checks.append({"index": vertebra["index"], "buried_bone_samples": below, "exposed_bone_samples": above})
                    planes = spine["fracture_probe_planes_source_z"]
                    require(all(not any(abs(p[2]-z) < .6 for p in bone_points) for z in planes),
                            "A bony bridge crosses an intended spinal fracture")
                    require(len(vertebra_checks) == 9, "Expected nine vertebral remnants")
                    summary["spine"] = {"vertebrae_checked": vertebra_checks,
                                         "bone_free_fracture_planes_source_z": planes,
                                         "skull_height_blocks_approx": design["skull_height_blocks_approx"]}
    (OUT / "verification.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary, indent=2))
    return summary


def contact_sheet(summary):
    from PIL import Image, ImageDraw, ImageFont
    sheet = Image.new("RGB", (2400, 2030), "#eee9de")
    draw = ImageDraw.Draw(sheet)
    def font(size, bold=False):
        try:
            return ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf", size)
        except OSError:
            return ImageFont.load_default(size=size)
    draw.text((48, 25), CONFIG.get("title", "DER GESUNKENE WÄCHTER"), fill="#293934", font=font(46, True))
    draw.text((48, 86), CONFIG.get("subtitle", "Blender → ObjToSchematic 1.0 → Java-NBT  /  Erster Form- und Materialtest"), fill="#54615a", font=font(28))
    views = [("01-blender-source.png", "01 / Blender-Quelle · einfache Materialfarben"),
             ("02-blocks-front.png", "02 / Exportierte Blöcke · Minecraft-Texturen"),
             ("03-blocks-other-side.png", "03 / Gegenansicht · Innenlagen und Schulter"),
             ("04-blocks-back.png", "04 / Rückseite · abgetrennter Arm")]
    for index, (filename, label) in enumerate(views):
        label = CONFIG.get("view_labels", [v[1] for v in views])[index]
        x, y = 40+(index%2)*1180, 155+(index//2)*875
        image = Image.open(OUT / filename).convert("RGB")
        image.thumbnail((1140, 815), Image.Resampling.LANCZOS)
        sheet.paste(image, (x, y))
        draw.text((x+10, y+822), label, fill="#293934", font=font(25, True))
    size = " × ".join(map(str, summary["size"]))
    draw.text((48, 1917), f"{size} Blöcke  ·  {summary['blocks']:,} gesetzte Blöcke  ·  {summary['palette_entries']} Blocktypen  ·  Türkis = 2 Blöcke Höhe".replace(",", "."),
              fill="#293934", font=font(27, True))
    draw.text((48, 1966), CONFIG.get("review_footer", "NBT-Geometrie in Blender gerendert; kein Ingame-Nachweis. Geländeplatte und Maßstabsmarker gehören nur zur Vorschau."),
              fill="#54615a", font=font(24))
    output = OUT / f"{STEM}-review.png"
    sheet.save(output)
    print(f"Review sheet: {output}")


def reference_sheet(summary):
    from PIL import Image, ImageDraw, ImageFont
    sheet = Image.new("RGB", (2400, 2250), "#eee9de")
    draw = ImageDraw.Draw(sheet)
    def font(size, bold=False):
        try:
            return ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf", size)
        except OSError:
            return ImageFont.load_default(size=size)
    def panel(path, box, crop=None):
        image = Image.open(path).convert("RGB")
        if crop:
            image = image.crop(crop)
        x, y, width, height = box
        image.thumbnail((width, height), Image.Resampling.LANCZOS)
        sheet.paste(image, (x+(width-image.width)//2, y+(height-image.height)//2))
    title = CONFIG.get("title", STEM.upper())
    draw.text((48, 24), title, fill="#293934", font=font(50, True))
    draw.text((48, 91), CONFIG.get("reference_title", "Archaean Colossi · Referenzstudie mit Blender und ObjToSchematic"), fill="#54615a", font=font(30))
    panel(ROOT / CONFIG["reference_frame"], (40, 155, 1140, 1120), CONFIG.get("reference_crop", (0, 80, 1080, 1490)))
    panel(OUT / "05-blocks-landscape.png", (1220, 155, 1140, 1120))
    credit = CONFIG.get("reference_credit", "The Archive In Between · Ausschnitt")
    draw.text((60, 1290), f"01 / Original · {credit}", fill="#293934", font=font(25, True))
    label = CONFIG.get("landscape_label", "echte NBT-Blöcke, illustrative Hügel")
    draw.text((1240, 1290), f"02 / {title} · {label}", fill="#293934", font=font(23, True))
    panel(OUT / CONFIG.get("detail_image", "02-blocks-front.png"), (40, 1350, 1140, 750))
    comparison = OUT / CONFIG.get("comparison_image", "06-size-comparison.png")
    panel(comparison if comparison.exists() else OUT / "04-blocks-back.png", (1220, 1350, 1140, 750))
    draw.text((60, 2108), CONFIG.get("detail_label", "03 / Gesamte exportierte Struktur ohne Landschaft"), fill="#293934", font=font(25, True))
    version = title.split()[-1].lower()
    label = f"04 / Gleicher Maßstab: {version} ({summary['size'][1]} gesamt) und erster Colossus (66)" if comparison.exists() else "04 / Rückseite"
    label = CONFIG.get("comparison_label", label)
    draw.text((1240, 2108), label, fill="#293934", font=font(25, True))
    size = " × ".join(map(str, summary["size"]))
    count = f"{summary['blocks']:,}".replace(",", ".")
    dimensions = CONFIG.get("dimensions_label", "X/Y/Z, inklusive Arm")
    draw.text((48, 2160), f"{size} Blöcke ({dimensions})  ·  {count} gesetzte Blöcke", fill="#293934", font=font(26, True))
    url = CONFIG.get("reference", "https://www.instagram.com/reel/DaoBxUEiBNa/").removeprefix("https://www.")
    draw.text((48, 2206), CONFIG.get("reference_footer", f"Blender-Render der NBT, kein Ingame-Bild. Gelände und Figuren sind Vorschauhilfen. Referenz: {url}"), fill="#54615a", font=font(21))
    output = OUT / f"{STEM}-reference-review.png"
    sheet.save(output)
    print(f"Reference comparison: {output}")


def burial_sheet(summary):
    from PIL import Image, ImageDraw, ImageFont
    sheet = Image.new("RGB", (2400, 2170), "#eee9de")
    draw = ImageDraw.Draw(sheet)
    def font(size, bold=False):
        try:
            return ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf", size)
        except OSError:
            return ImageFont.load_default(size=size)
    draw.text((48, 25), f"{CONFIG.get('title', STEM.upper())} / VERSUNKENER UNTERKÖRPER", fill="#293934", font=font(44, True))
    draw.text((48, 87), "Fortgesetzter Rumpf · verjüngte Taille · unregelmäßig abgerissene Hüfte", fill="#54615a", font=font(29))
    panels = [("05-blocks-landscape.png", "01 / Einbettung in die illustrative Hügellandschaft"),
              ("07-buried-body.png", "02 / Freigelegt · Türkis markiert das gedachte Bodenniveau"),
              ("08-hip-detail.png", "03 / Untergrund-Detail · Panzerung und abgerissene Träger"),
              ("03-blocks-other-side.png", "04 / Gegenansicht des gesamten Strukturverbunds")]
    for index, (name, label) in enumerate(panels):
        x, y = 40+(index%2)*1180, 155+(index//2)*920
        image = Image.open(OUT / name).convert("RGB")
        image.thumbnail((1140, 850), Image.Resampling.LANCZOS)
        sheet.paste(image, (x+(1140-image.width)//2, y+(850-image.height)//2))
        draw.text((x+10, y+865), label, fill="#293934", font=font(23, True))
    burial = summary["buried_hip"]
    size = " × ".join(map(str, summary["size"]))
    draw.text((48, 2025), f"{size} Blöcke gesamt · bis {burial['depth_below_surface']} Blöcke unter dem gedachten Bodenniveau", fill="#293934", font=font(28, True))
    draw.text((48, 2080), "Der zusätzliche Unterkörper ist in der NBT enthalten. Die türkise Ebene und die Landschaft dienen nur der Vorschau.", fill="#54615a", font=font(24))
    draw.text((48, 2118), "Oberirdischer Maßstab an den bisherigen Entwurf angepasst; gerenderte NBT-Geometrie, kein Ingame-Nachweis.", fill="#54615a", font=font(24))
    output = OUT / f"{STEM}-underground-review.png"
    sheet.save(output)
    print(f"Burial review: {output}")


def main():
    global OUT, STEM, CONFIG
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--config", type=Path, default=ROOT / "relics/colossus/design/colossus-ots.json")
    args = parser.parse_args()
    CONFIG = json.loads(args.config.read_text(encoding="utf-8"))
    output = ROOT / CONFIG["output"]
    OUT, STEM = output.parent, output.stem
    summary = check()
    if not args.check_only:
        contact_sheet(summary)
        if CONFIG.get("reference_frame") and (ROOT / CONFIG["reference_frame"]).exists():
            reference_sheet(summary)
        if "buried_hip" in summary:
            burial_sheet(summary)


if __name__ == "__main__":
    main()
