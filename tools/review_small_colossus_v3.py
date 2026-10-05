"""Same-scale actual-NBT comparison of the rejected V2 and new slender V3 sentinel."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
WORK=ROOT/'.work/small-colossus-v3-review'
OUT=ROOT/'relics/colossus/design/generated/small-colossus-v3/small-colossus-v3-comparison-review.png'


def render():
    import review_relic_v2 as comparison
    comparison.WORK=WORK
    comparison.PAIRS=[('Small Colossus','colossus','small-colossus','Slender sunken sentinel')]
    comparison.render(('v2','v3'))


def compose():
    from PIL import Image,ImageDraw,ImageFont
    data=json.loads((WORK/'pairs.json').read_text())[0]['versions']
    sheet=Image.new('RGB',(2400,1530),'#eee9de');draw=ImageDraw.Draw(sheet)
    def font(n,bold=False):return ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',n)
    draw.text((48,30),'SMALL COLOSSUS / V2 -> V3',font=font(55,True),fill='#293934')
    draw.text((50,105),'Actual exported blocks / same scale, camera and nominal ground',font=font(31),fill='#54615a')
    image=Image.open(WORK/'small-colossus.png').convert('RGB')
    # Remove empty staging space without changing either subject's relative scale.
    image=image.crop((0,300,1800,1200)).resize((2300,1150),Image.Resampling.LANCZOS)
    sheet.paste(image,(50,160))
    for x,row,label in [(70,data[0],'V2 / TOO SIMILAR TO THE LARGE COLOSSUS'),
                        (1250,data[1],'V3 / SLENDER SUNKEN SENTINEL')]:
        draw.text((x,1330),label,font=font(28,True),fill='#293934')
        dimensions=' x '.join(map(str,row['size']))
        draw.text((x,1377),f'{dimensions} blocks / {row["visible_height"]} visible layers',font=font(27),fill='#54615a')
    draw.text((50,1450),'V3: long mask, narrow waist, stepped plates and two long arms. Visual candidate; game integration pending.',
              font=font(26),fill='#54615a')
    sheet.save(OUT);print(OUT)


if __name__=='__main__':
    if '--render' in sys.argv:render()
    elif '--compose-only' in sys.argv:compose()
    else:
        subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe','--background','--threads','8',
                        '--python-exit-code','1','--python',str(Path(__file__).resolve()),'--','--render'],cwd=ROOT,check=True)
        compose()
