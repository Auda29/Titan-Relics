"""Label the native armor inspection images produced by render_monolith_trim.py."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

OUT=Path(__file__).resolve().parents[1]/'docs/project/reviews/monolith-trim-20261028'

def main():
    font=ImageFont.load_default(size=23);small=ImageFont.load_default(size=17)
    canvas=Image.new('RGB',(1680,1460),'#1b2026');draw=ImageDraw.Draw(canvas)
    draw.text((24,12),'Monolith - native Minecraft 26.2 armor / UV inspection',font=font,fill='white')
    draw.text((24,44),'Blender inspection light, neutral mannequin; not a Minecraft client screenshot.',font=small,fill='#b9c4cf')
    rows=[('before-emerald-front','Before / Emerald'),('after-emerald-front','After / Emerald'),
          ('after-amethyst-front','After / Amethyst'),('before-emerald-back','Before / back'),
          ('after-emerald-back','After / back'),('after-copper-front','After / Copper')]
    for i,(name,label) in enumerate(rows):
        x=(i%3)*560;y=80+(i//3)*690
        canvas.paste(Image.open(OUT/(name+'.png')).convert('RGB'),(x,y))
        draw.text((x+20,y+645),label,font=font,fill='white')
    canvas.save(OUT/'comparison-review.png')

if __name__=='__main__':main()
