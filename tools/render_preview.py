#!/usr/bin/env python3
"""Render the actual generated blocks as inspectable PNG design previews.

Pillow is optional and only required for these previews, not the asset/build tool.
These are geometry renders, not Minecraft screenshots or proof of runtime loading.
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from relic_assets import AIR, colossus, obelisk

COLORS={"deepslate_tiles":"#4b5556","cracked_deepslate_tiles":"#434e4e","polished_deepslate":"#313d42","polished_basalt":"#6d7070",
        "cobbled_deepslate":"#586366","sandstone":"#bd9c65","cut_sandstone":"#a38450","smooth_sandstone":"#d6bc84",
        "waxed_weathered_cut_copper":"#559185","moss_block":"#687e45","azalea_leaves":"#547342","grass_block":"#698250","dirt":"#75604a",
        "black_concrete":"#141f25","oak_log":"#796149","oak_planks":"#a88a5c","crafting_table":"#a67f50"}


def rgb(block):
    h=COLORS.get(block.removeprefix("minecraft:").split("[")[0],"#a7a096")
    return tuple(int(h[i:i+2],16) for i in (1,3,5))


def render(model,out: Path,cutaway=False):
    image=Image.new("RGB",(1600,1200),"#e8e3d8")
    draw=ImageDraw.Draw(image)
    try:
        title=ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf",34)
        label=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf",20)
    except OSError:
        title=label=ImageFont.load_default()
    draw.text((60,35),"RELIC / "+model.id.upper()+(" / SECTION" if cutaway else ""),font=title,fill="#263936")
    draw.text((60,88),f"{model.size[0]} x {model.size[1]} x {model.size[2]} blocks | seed {model.seed} | actual generated geometry",font=label,fill="#52655e")
    blocks={p:b for p,b in model.blocks.items() if b!=AIR and (not cutaway or p[2]>=35)}
    sx,sy,sz=model.size
    scale=min(1250/(sx+sz),850/(sy+(sx+sz)*.5))
    def project(x,y,z): return (800+(x+z-(sx+sz)/2)*scale,190+(sy+sz*.5+(x-z)*.5-y)*scale)
    # Ground plate establishes model scale, but is not exported structure geometry.
    draw.polygon([project(-5,0,-5),project(sx+5,0,-5),project(sx+5,0,sz+5),project(-5,0,sz+5)],fill="#d0caba")
    for (x,y,z),b in sorted(blocks.items(),key=lambda item:(item[0][0]+item[0][1]-item[0][2],item[0])):
        base=rgb(b)
        if (x,y,z-1) not in blocks:
            draw.polygon([project(x,y,z),project(x+1,y,z),project(x+1,y+1,z),project(x,y+1,z)],fill=tuple(int(c*.78) for c in base))
        if (x+1,y,z) not in blocks:
            draw.polygon([project(x+1,y,z),project(x+1,y,z+1),project(x+1,y+1,z+1),project(x+1,y+1,z)],fill=tuple(int(c*.60) for c in base))
        if (x,y+1,z) not in blocks:
            draw.polygon([project(x,y+1,z),project(x+1,y+1,z),project(x+1,y+1,z+1),project(x,y+1,z+1)],fill=base)
    # Cyan two-block person gives a neutral reference independent of player skins.
    px,py=project(5,model.ground_y,5)
    draw.rectangle((px,py-2*scale,px+.6*scale,py),fill="#38b7b0")
    draw.text((60,1125),"Alpha design preview. Flat block colors; no shaders. Cyan marker = 2-block player height.",font=label,fill="#52655e")
    out.parent.mkdir(parents=True,exist_ok=True)
    image.save(out,optimize=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("design/generated"))
    parser.add_argument("--seed",type=int,default=2913)
    args=parser.parse_args()
    for model in (obelisk(args.seed),colossus(args.seed)):
        render(model,args.output/f"{model.id}.png")
        if model.id=="colossus": render(model,args.output/"colossus-section.png",True)
    print(f"Geometry previews written to {args.output}")


if __name__=="__main__": main()
