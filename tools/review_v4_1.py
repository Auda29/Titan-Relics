"""Assemble the inspected V4.1 hand and obelisk revisions into publication sheets."""
from pathlib import Path
import json

from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]


def sheet(title,subtitle,panels,footer,path):
    image=Image.new("RGB",(2400,2150),"#eee9de")
    draw=ImageDraw.Draw(image)
    def font(size,bold=False):
        return ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",size)
    draw.text((40,25),title,font=font(43,True),fill="#293934")
    draw.text((40,87),subtitle,font=font(26),fill="#54615a")
    for i,(source,label,note) in enumerate(panels):
        x,y=40+(i%2)*1180,150+(i//2)*900
        pic=Image.open(source).convert("RGB")
        pic.thumbnail((1140,780),Image.Resampling.LANCZOS)
        image.paste(pic,(x+(1140-pic.width)//2,y+(780-pic.height)//2))
        draw.text((x,y+792),label,font=font(29,True),fill="#293934")
        draw.text((x,y+838),note,font=font(23),fill="#54615a")
    draw.text((40,2020),footer,font=font(24),fill="#54615a")
    draw.text((40,2070),"Actual exported NBT rendered in Blender. Inspection crops and surrounding terrain are preview aids.",font=font(24),fill="#54615a")
    image.save(path)
    print(path)


def main():
    colossus=ROOT/"relics/colossus/design/generated/colossus-v4-1-frame"
    sheet("COLOSSUS V4.1 / PALM UP, RELAXED FINGERS",
          "Supinated RIGHT hand / near-horizontal wrist / 434 non-hand V4 meshes preserved",
          [(colossus/"09-hand-before.png","V4 / Previous raised-wrist pose","Original pose for comparison; matching inspection region"),
           (colossus/"10-hand-palm-up.png","V4.1 / Open palm facing upward","Four fingers curl up; separate thumb, no anatomical mirroring"),
           (colossus/"11-hand-profile.png","V4.1 / Lower side view","Palm rests low; fingers rise independently of the wrist"),
           (colossus/"12-hand-higher-terrain.png","V4.1 / Illustrative higher ground","Source Y28 instead of Y20: fingertips remain visible")],
          "Higher-ground panel is a fixed illustration, not a guarantee for arbitrary worldgen slopes.",
          colossus/"colossus-v4-1-hand-review.png")
    obelisk=ROOT/"relics/obelisk/design/generated/obelisk-v4-1"
    old=ROOT/"relics/obelisk/design/generated/obelisk-v4"
    metadata=json.loads((obelisk/"obelisk-v4-1.design.json").read_text())
    removed=metadata["obelisk_v4"]["volume_removed_percent"]
    sheet("OBELISK V4.1 / QUIET FACETS & BRANCHING CRACKS",
          "Consistent sandstone sides / three real surface fissures / four broader edge spalls",
          [(old/"02-blocks-front.png","V4 / Previous contrasting patches","Preserved earlier export"),
           (obelisk/"02-blocks-front.png","V4.1 / Coherent sandstone faces","Local weathering; no alternating high-contrast patches"),
           (obelisk/"10-crack-1.png","V4.1 / Actual crack inspection crop","Open branching fissure with stone backing; cropped above/below"),
           (obelisk/"04-blocks-back.png","V4.1 / Opposite side","Antiprism, crown and solid core retained")],
          f"{removed:.3f}% monolith volume removed. Original V4 sand and foundation geometry retained.",
          obelisk/"obelisk-v4-1-changes-review.png")


if __name__=="__main__": main()
