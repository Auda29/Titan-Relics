"""Public V3/V4 NBT review and a local-only reference/model comparison."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
WORK=ROOT/'.work/small-colossus-v4-review'
ASSET=ROOT/'relics/colossus/design/generated/small-colossus-v4'
REFERENCES=ROOT/'.work/references/small-colossus-v4'


def render():
    import review_relic_v2 as comparison
    comparison.WORK=WORK
    comparison.PAIRS=[('Small Colossus','colossus','small-colossus','Reference-led dormant plated specimen')]
    comparison.render(('v3','v4'))


def compose():
    from PIL import Image,ImageDraw,ImageFont
    def font(n,bold=False):return ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',n)
    rows=json.loads((WORK/'pairs.json').read_text())[0]['versions']
    canvas=Image.new('RGB',(2400,1530),'#eee9de');draw=ImageDraw.Draw(canvas)
    draw.text((48,28),'SMALL COLOSSUS / V3 -> V4',font=font(55,True),fill='#293934')
    draw.text((50,106),'Actual NBT / same scale and ground / V4 based on the new Vigilant-Class reference',font=font(29),fill='#54615a')
    image=Image.open(WORK/'small-colossus.png').convert('RGB').crop((0,300,1800,1200))
    canvas.paste(image.resize((2300,1150),Image.Resampling.LANCZOS),(50,160))
    for x,row,label in [(70,rows[0],'V3 / REJECTED AS TOO SKELETAL'),(1250,rows[1],'V4 / DORMANT PLATED SPECIMEN')]:
        draw.text((x,1330),label,font=font(30,True),fill='#293934')
        dims=' x '.join(map(str,row['size']))
        draw.text((x,1377),f'{dims} blocks / {row["visible_height"]} visible layers',font=font(27),fill='#54615a')
    draw.text((50,1450),'New primary reference: instagram.com/reel/Da-s0zqi7OQ/ / V4 visual candidate; game integration pending.',
              font=font(26),fill='#54615a')
    output=ASSET/'small-colossus-v4-comparison-review.png';canvas.save(output);print(output)
    # Original third-party frames remain local; only our model review is published.
    reference=REFERENCES/'frame-000.00.png'
    if reference.exists():
        local=Image.new('RGB',(2400,2100),'#eee9de');draw=ImageDraw.Draw(local)
        draw.text((48,25),'PRIMARY REFERENCE -> SMALL COLOSSUS V4',font=font(49,True),fill='#293934')
        draw.text((50,97),'Opening dormant specimen / individually framed / reference frame stays local',font=font(29),fill='#54615a')
        for path,x,width,label in [(reference,35,1070,'The Archive In Between / 0 seconds'),
                                  (ASSET/'05-blocks-landscape.png',1140,1220,'Our actual exported NBT / Blender preview')]:
            image=Image.open(path).convert('RGB');image.thumbnail((width,1790),Image.Resampling.LANCZOS)
            local.paste(image,(x+(width-image.width)//2,160+(1790-image.height)//2))
            draw.text((x+10,1980),label,font=font(27,True),fill='#293934')
        draw.text((48,2035),'Observed: plated mass, multi-optic face, arched grille and pincer. Rear, burial and limb completion are authored.',font=font(25),fill='#54615a')
        target=REFERENCES/'reference-and-v4.png';local.save(target);print(target)


if __name__=='__main__':
    if '--render' in sys.argv:render()
    elif '--compose-only' in sys.argv:compose()
    else:
        subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe','--background','--threads','8',
                        '--python-exit-code','1','--python',str(Path(__file__).resolve()),'--','--render'],cwd=ROOT,check=True)
        compose()
