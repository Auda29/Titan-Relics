"""Same-scale before/after NBT comparisons for the October 5 screenshot feedback."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
WORK=ROOT/'.work/screenshot-revisions'
OUTPUT=ROOT/'docs/project/reviews/screenshot-revisions-20261005.png'
TITLE='SCREENSHOT REVISIONS / OCTOBER 5'
PAIRS=[('Small Colossus','colossus','small-colossus',('v4','v5'),
        'Listed posture / weathered armour / asymmetric burial'),
       ('World Tree','world-tree','world-tree',('v2','v3'),
        'Fine branching / smaller sprays / open canopy'),
       ('Ruined Tower','ruined-tower','ruined-tower',('v2','v3'),
        '220 visible layers / broken storeys / stair fragments')]


def render():
    import review_relic_v2 as comparison
    for title,relic,stem,versions,note in PAIRS:
        comparison.WORK=WORK/stem
        comparison.PAIRS=[(title,relic,stem,note)]
        comparison.render(versions)


def compose():
    from PIL import Image,ImageDraw,ImageFont
    def font(n,bold=False):return ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',n)
    canvas=Image.new('RGB',(2400,2530),'#eee9de');draw=ImageDraw.Draw(canvas)
    draw.text((45,25),TITLE,font=font(49,True),fill='#293934')
    draw.text((48,91),'LEFT: before / RIGHT: revised / actual NBT, same block scale within each pair',font=font(28),fill='#54615a')
    for i,(title,relic,stem,versions,note) in enumerate(PAIRS):
        row=json.loads((WORK/stem/'pairs.json').read_text())[0];y=155+i*750
        draw.text((48,y),title.upper(),font=font(34,True),fill='#293934')
        image=Image.open(WORK/stem/(stem+'.png')).convert('RGB')
        if stem=='small-colossus':image=image.crop((0,220,1800,1270))
        image.thumbnail((1370,650),Image.Resampling.LANCZOS);canvas.paste(image,(48+(1370-image.width)//2,y+60))
        x=1460
        draw.text((x,y+110),note.replace(' / ','\n'),font=font(29,True),fill='#293934',spacing=14)
        for j,v in enumerate(row['versions']):
            text=f"{v['version']}   {' x '.join(map(str,v['size']))}\n{v['visible_height']} visible layers / {v['blocks']:,} blocks"
            draw.text((x,y+320+j*110),text,font=font(27),fill='#54615a',spacing=9)
        draw.line((48,y+735,2350,y+735),fill='#c6c6ba',width=2)
    draw.text((48,2460),'Visual candidates. Blender renders of exported blocks; the ground shown here is illustrative.',font=font(27),fill='#54615a')
    output=OUTPUT;output.parent.mkdir(parents=True,exist_ok=True)
    canvas.save(output);print(output)


if __name__=='__main__':
    if '--render' in sys.argv:render()
    elif '--compose-only' in sys.argv:compose()
    else:
        subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe','--background','--threads','8',
                        '--python-exit-code','1','--python',str(Path(__file__).resolve()),'--','--render'],cwd=ROOT,check=True)
        compose()
