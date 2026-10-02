"""Publish palette, exact-form and hypothetical salvage comparisons from NBT renders."""
import json
from pathlib import Path

from PIL import Image,ImageDraw,ImageFont
import inspect_ots_result as inspector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"relics/colossus/design/generated/colossus-v4-1-materials"
BASE=ROOT/"relics/colossus/design/generated/colossus-v4-1-frame"


def font(n,bold=False):
    return ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",n)


def panel(image,path,x,y,w,h,title,note):
    pic=Image.open(path).convert("RGB")
    pic.thumbnail((w,h),Image.Resampling.LANCZOS)
    image.paste(pic,(x+(w-pic.width)//2,y+(h-pic.height)//2))
    draw=ImageDraw.Draw(image)
    draw.text((x,y+h+10),title,font=font(30,True),fill="#293934")
    draw.text((x,y+h+55),note,font=font(23),fill="#54615a")


def main():
    report=json.loads((OUT/"verification.json").read_text())
    spec=json.loads((ROOT/"relics/colossus/design/studies/colossus-v4-1-materials.json").read_text())
    inspector.CONFIG=spec;inspector.OUT=OUT;inspector.STEM="colossus-v4-1-materials"
    inspector.contact_sheet(report)
    study=json.loads((OUT/"colossus-v4-1-materials.design.json").read_text())["material_study"]
    image=Image.new("RGB",(2400,2700),"#eee9de");draw=ImageDraw.Draw(image)
    draw.text((45,25),"COLOSSUS / MATERIAL STUDY — EXACT V4.1 FORM",font=font(45,True),fill="#293934")
    draw.text((45,92),"Direct block-state replacement: zero blocks added, removed or moved in the study export",font=font(28),fill="#54615a")
    panel(image,BASE/"05-blocks-landscape.png",40,155,1140,1050,"Accepted V4.1 / Original materials",
          "129,253 copper blocks + 8,821 raw iron blocks")
    panel(image,OUT/"05-blocks-landscape.png",1220,155,1140,1050,"Study / Same shape, less valuable bulk materials",
          "197 copper blocks + 10 raw iron blocks at three salvage sites")
    panel(image,OUT/"10-after-metal-salvage-landscape.png",40,1340,1140,1050,"Hypothetical view / All retained metal removed",
          "Only this preview removes 207 blocks; the export is intact")
    x,y=1260,1400
    lines=[("EXACT SHAPE CHECK",35,True),("181 × 209 × 235 / 223,161 blocks",30,False),
           ("0 added / 0 removed / 0 moved",30,True),("491 source meshes geometrically unchanged",27,False),
           ("",24,False),("RESOURCE REDUCTION",35,True),("Copper: 129,253 → 197  (−99.85%)",29,False),
           ("Raw iron blocks: 8,821 → 10  (−99.89%)",29,False),("Raw iron items: 79,389 → 90",29,False),
           ("",24,False),("BULK PALETTE",35,True),("Copper armour → polished granite",27,False),
           ("Cut plates → light gray terracotta",27,False),("Copper trim → terracotta",27,False),
           ("Iron-colored wear → andesite",27,False),("Patina-colored surfaces → green terracotta",27,False),
           ("",24,False),("AFTER TARGETED SALVAGE",35,True),("99.907% of all blocks remain",30,True),
           ("Helmet, hand, torso and silhouette stay legible",25,False)]
    for text,size,bold in lines:
        draw.text((x,y),text,font=font(size,bold),fill="#293934" if bold else "#54615a")
        y+=size+18
    draw.text((45,2520),"Actual NBT rendered in Blender. Same cameras and terrain. Material study and salvage quantities await approval.",font=font(24),fill="#54615a")
    draw.text((45,2570),"All nonmetal states are unchanged. Post-mining views simulate targeted metal removal, not general demolition.",font=font(24),fill="#54615a")
    draw.text((45,2620),"Editable Blender source preserves all meshes; exact salvage masks are applied reproducibly after the original export.",font=font(24),fill="#54615a")
    path=OUT/"colossus-material-comparison-review.png";image.save(path);print(path)
    image=Image.new("RGB",(2400,2670),"#eee9de");draw=ImageDraw.Draw(image)
    draw.text((45,25),"COLOSSUS / THREE LOCAL SALVAGE SITES",font=font(45,True),fill="#293934")
    draw.text((45,92),"Left: intact material study / Right: hypothetical removal of retained metal only",font=font(28),fill="#54615a")
    for i,zone in enumerate(study["salvage_zones"]):
        for column,stage in enumerate(("before","after")):
            panel(image,OUT/f"11-site-{i+1}-{stage}.png",40+1180*column,150+810*i,1140,670,
                  f"{zone['name'].capitalize()} / {'intact' if column==0 else 'salvaged'}",
                  f"{zone['blocks']} {zone['family']} blocks / actual-NBT inspection crop")
    draw.text((45,2590),"Cropped inspection views. No protection, replenishment or final loot balance is implemented by this material study.",font=font(23),fill="#54615a")
    path=OUT/"colossus-salvage-sites-review.png";image.save(path);print(path)


if __name__=="__main__": main()
