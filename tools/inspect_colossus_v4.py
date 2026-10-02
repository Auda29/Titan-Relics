"""V4-specific block checks and a visual decision sheet for the two chest variants."""
import argparse
import hashlib
import json
from pathlib import Path

from inspect_ots_result import read_structure, require

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "relics/colossus/design/generated"


def verify(design, blocks):
    low, high = design["source_bounds_blender"]
    scale = design["blocks_per_source_unit"]
    def local(p):
        return (round((p[0]-low[0])*scale), round((p[1]-low[2])*scale), round((p[2]+high[1])*scale))
    def occupied_near(p, radius):
        x, y, z = local(p)
        return sum((x+dx, y+dy, z+dz) in blocks for dx in range(-radius, radius+1)
                   for dy in range(-radius, radius+1) for dz in range(-radius, radius+1))
    hand = design["right_hand"]
    require(hand["side"] == "right" and abs(hand["basis_determinant"]-1) < 1e-5,
            "Hand is mirrored or mislabeled")
    # Independent canonical right-hand cross-product check on stored source axes.
    t, d, p = (hand[key] for key in ("thumbward_source", "distal_source", "palmar_normal_source"))
    cross = [t[1]*d[2]-t[2]*d[1], t[2]*d[0]-t[0]*d[2], t[0]*d[1]-t[1]*d[0]]
    require(sum(a*b for a, b in zip(cross, p)) > .999, "Right-hand anatomical basis changed")
    require(len(hand["digits"]) == 4, "Four fingers plus a separate thumb required")
    tips = [d["tip_source"] for d in hand["digits"]]+[hand["thumb_tip_source"]]
    counts = [occupied_near(p, 3) for p in tips]
    require(all(n > 25 for n in counts), "A finger/thumb disappeared during voxelization")
    require(all(p[1] > design["ground_level_source"]+10 for p in tips), "Fingertips are buried")
    gaps = [occupied_near(p, 0) for p in hand["finger_gap_probes_source"]]
    require(not any(gaps), "Fingers merged at an intended inspection gap")
    rear = [occupied_near(p, 1) for p in design["rear_damage"]["empty_probes_source"]]
    require(not any(rear), f"A designed rear breach was obstructed: {rear}")
    require(occupied_near(design["chest_study"]["empty_center_probe_source"], 2) == 0,
            "Chest mechanism retains a solid center")
    source = OUT / "colossus-v3/colossus-v3-source.blend"
    require(hashlib.sha256(source.read_bytes()).hexdigest() == design["source_v3_sha256"], "V3 source baseline changed")
    return {"anatomical_side": "right", "orientation_determinant": hand["basis_determinant"],
            "finger_and_thumb_samples": counts, "separate_finger_gaps": len(gaps),
            "clear_rear_breach_probes": len(rear), "preserved_v3_source_objects": len(design["preserved_v3_objects"]),
            "chest_variant": design["chest_study"]["variant"], "center_is_open": True}


def compare_variants():
    entries = []
    for variant in ("open", "frame"):
        stem = f"colossus-v4-{variant}"
        folder = OUT / stem
        design = json.loads((folder / f"{stem}.design.json").read_text())
        root, blocks = read_structure(folder / f"{stem}.nbt")
        entries.append((design, root, blocks))
    a, b = entries
    require(a[1]["size"] == b[1]["size"] and a[0]["source_bounds_blender"] == b[0]["source_bounds_blender"],
            "Comparison candidates have different coordinate frames")
    differences = {p for p in a[2].keys() | b[2].keys() if a[2].get(p) != b[2].get(p)}
    low, high = a[0]["source_bounds_blender"]
    s = a[0]["blocks_per_source_unit"]
    require(len(differences) > 100, "Chest candidates are identical")
    require(all(8 <= p[0]/s+low[0] <= 40 and 0 <= p[1]/s+low[2] <= 35
                and -36 <= p[2]/s-high[1] <= -4 for p in differences), "Candidate differences extend beyond chest")
    result = {"different_block_positions": len(differences), "differences_confined_to_chest": True}
    for variant in ("open", "frame"):
        folder = OUT / f"colossus-v4-{variant}"
        verification = json.loads((folder / "verification.json").read_text())
        verification["chest_comparison"] = result
        (folder / "verification.json").write_text(json.dumps(verification, indent=2)+"\n")
    print(json.dumps(result, indent=2))


def sheet():
    from PIL import Image, ImageDraw, ImageFont
    folder = OUT / "colossus-v4-open"
    image = Image.new("RGB", (2400, 2600), "#eee9de")
    draw = ImageDraw.Draw(image)
    def font(size, bold=False):
        return ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf", size)
    def panel(path, x, y, w, h, title, note):
        pic = Image.open(path).convert("RGB")
        pic.thumbnail((w, h), Image.Resampling.LANCZOS)
        image.paste(pic, (x+(w-pic.width)//2, y+(h-pic.height)//2))
        draw.text((x, y+h+8), title, font=font(26, True), fill="#293934")
        draw.text((x, y+h+45), note, font=font(21), fill="#54615a")
    draw.text((45, 25), "COLOSSUS V4 / REAR, RIGHT HAND & CHEST STUDIES", font=font(43, True), fill="#293934")
    draw.text((45, 90), "Original scale, helmet, buried hip and forearm retained / actual exported NBT", font=font(27), fill="#54615a")
    panel(folder / "09-v3-rear-detail.png", 40, 150, 1140, 650, "V3 / Rear before", "Inspection crop: upper torso; head and arm excluded")
    panel(folder / "09-v4-rear-detail.png", 1220, 150, 1140, 650, "V4 / Torn rear armour", "Asymmetric breaches, exposed ribs and torn plate thickness")
    panel(folder / "10-right-hand-palm.png", 40, 910, 1140, 650, "RIGHT hand / Palm side", "Thumb on image right; four fingers rise above nominal ground")
    panel(folder / "12-right-hand-back.png", 1220, 910, 1140, 650, "RIGHT hand / Back side", "Thumb on image left; same hand, opposite camera")
    chest_panels = [(folder / "11-v3-chest-detail.png", "V3 / Original cylinder", "Baseline: plain chest piston"),
                    (folder / "11-v4-chest-detail.png", "A / Removed", "Open chest, existing supports retained"),
                    (OUT / "colossus-v4-frame/11-v4-chest-detail.png", "B / Selected: machine frame", "Broken bearings, supports and conduit")]
    for i, (path, title, note) in enumerate(chest_panels):
        panel(path, 40+i*790, 1680, 750, 650, title, note)
    draw.text((45, 2450), "Chest panels are matching NBT inspection crops with terrain removed, not new exterior openings.", font=font(25), fill="#54615a")
    draw.text((45, 2500), "B selected as the V4 design on October 2, 2026. Blender renders; the playable build still uses V3.", font=font(25), fill="#54615a")
    path = folder / "colossus-v4-changes-review.png"
    image.save(path)
    print(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sheets", action="store_true")
    args = parser.parse_args()
    compare_variants()
    if args.sheets:
        sheet()
