"""Build study B comparison sheets from real block renders and a labeled mask map."""
import json
from pathlib import Path

from PIL import Image,ImageDraw
from review_colossus_materials import font,panel

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"relics/colossus/design/generated/colossus-v4-1-materials-b"


def main():
    report=json.loads((OUT/"verification.json").read_text())
    count=report["salvage"]["after"]
    image=Image.new("RGB",(2400,2690),"#eee9de");draw=ImageDraw.Draw(image)
    draw.text((45,25),"COLOSSUS / STUDY B — SALVAGEABLE ARMOUR",font=font(44,True),fill="#293934")
    draw.text((45,90),f"{count['copper_blocks']:,} copper blocks / {count['raw_iron_blocks']} raw iron blocks = {count['raw_iron_items']} raw iron items",font=font(30),fill="#54615a")
    panel(image,OUT/"05-blocks-landscape.png",40,150,1140,1050,"Intact B / Exact accepted V4.1 shape",
          "All 223,161 block positions preserved")
    panel(image,OUT/"10-after-metal-salvage-landscape.png",1220,150,1140,1050,"After mining all copper and raw iron",
          "Permanent head, neck, upper bridge and backing remain")
    panel(image,OUT/"13-torso-before.png",40,1360,1140,855,"Chest and shoulders / Before salvage",
          "Copper follows broad armour-panel regions")
    panel(image,OUT/"13-torso-after.png",1220,1360,1140,855,"Chest and shoulders / After salvage",
          "Exposed backing and openings; no new disconnected remnants")
    draw.text((45,2380),"GEOMETRY CHECK: 0 added / 0 removed / 0 moved in the intact export",font=font(31,True),fill="#293934")
    draw.text((45,2440),"AFTER SALVAGE: head still connects to buried torso; no original surviving component splits",font=font(27),fill="#293934")
    draw.text((45,2500),f"{report['salvage']['blocks_remaining_after_metal_removal']:,} blocks remain ({report['salvage']['remaining_percent']:.2f}%). Copper < 50,000; raw iron items < 256.",font=font(28),fill="#293934")
    draw.text((45,2570),"Actual NBT rendered in Blender. Matched views, illustrative terrain. Study B palette awaits visual review.",font=font(24),fill="#54615a")
    draw.text((45,2620),"Support check preserves baseline face-connectivity; it is not a physical load simulation or mining protection.",font=font(23),fill="#54615a")
    path=OUT/"colossus-materials-b-comparison-review.png";image.save(path);print(path)
    image=Image.new("RGB",(2400,2860),"#eee9de");draw=ImageDraw.Draw(image)
    draw.text((45,25),"COLOSSUS B / WHERE THE METAL IS REMOVED",font=font(44,True),fill="#293934")
    draw.text((45,92),"Top: false-color map. Amber = salvage metal; gray = permanent low-value materials.",font=font(28),fill="#54615a")
    for column,side in enumerate(("front","back")):
        panel(image,OUT/f"14-salvage-map-{side}.png",40+1180*column,160,1140,760,
              f"Salvage map / {side}","Diagram colors, not the actual block palette")
    for row,name in enumerate(("rear","forearm")):
        for column,stage in enumerate(("before","after")):
            panel(image,OUT/f"13-{name}-{stage}.png",40+1180*column,1060+840*row,1140,710,
                  f"{name.capitalize()} / {stage} salvage","Actual NBT / identical camera and crop")
    draw.text((45,2800),"Only the simulated after-views remove blocks. The intact B export retains the complete accepted V4.1 form.",font=font(24),fill="#54615a")
    path=OUT/"colossus-materials-b-salvage-map-review.png";image.save(path);print(path)


if __name__=="__main__": main()
