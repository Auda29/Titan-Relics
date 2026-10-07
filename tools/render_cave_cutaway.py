"""Matched 3D root/cave cutaway, removing native foreground for inspection only."""
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
OUT=ROOT/'build/cave-contacts/20261007/cutaway'
BEFORE=ROOT/'build/smoke/run-20261007-090359-448f2a8bf6a8/report.json'
AFTER=ROOT/'build/smoke/run-20261007-112852-9f207601b88d/report.json'


def extract():
    from verify_world import AnvilWorld,protected_cell,AIR_NAMES
    from extract_rooted_sites import NON_CUBES
    from relic_assets import encode_structure
    OUT.mkdir(parents=True,exist_ok=True)
    low=(23658,40,-45484);high=(23694,74,-45456);records=[]
    for side,path in (('before',BEFORE),('after',AFTER)):
        report=json.loads(path.read_bytes());assert report['passed']
        world=AnvilWorld(Path(report['run_directory'])/'world');blocks={};omitted=0
        for x in range(low[0],high[0]):
            for z in range(low[2],high[2]):
                for y in range(low[1],high[1]):
                    s=world.block(x,y,z);assert s is not None
                    if s['Name'] in AIR_NAMES|NON_CUBES:continue
                    protected=protected_cell(world.chunk(x//16,z//16),(x,y,z))
                    if not protected and z>=-45470:
                        omitted+=1;continue
                    blocks[x-low[0],y-low[1],z-low[2]]=s['Name']
        target=OUT/f'root_cave-{side}.nbt'
        target.write_bytes(encode_structure(blocks,tuple(b-a for a,b in zip(low,high)),4903))
        records.append({'side':side,'source_report':path.relative_to(ROOT).as_posix(),
                        'report_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                        'crop_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
                        'blocks':len(blocks),'omitted_native_foreground_cells':omitted})
    (OUT/'manifest.json').write_text(json.dumps({'scope':'3D cutaway: all protected relic cells retained; native foreground Z >= -45470 hidden in this view only',
        'bounds_min':low,'bounds_max_exclusive':high,'records':records},indent=2)+'\n',encoding='utf-8')


def render():
    import render_rooted_sites as renderer
    renderer.VIEWS=OUT
    renderer.PAIRS=[('root_cave','Root/cave cutaway',160)]
    renderer.render()


def compose():
    from PIL import Image,ImageDraw,ImageFont
    canvas=Image.new('RGB',(1800,1050),'#eeeade');draw=ImageDraw.Draw(canvas)
    font=lambda s:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',s)
    draw.text((25,12),'WURZELN IM HÖHLENRAUM / Links: Alpha 4.8 | Rechts: neue Stränge',font=font(32),fill='#2b3932')
    canvas.paste(Image.open(OUT/'root_cave.png').convert('RGB'),(0,80))
    draw.text((25,990),'3D-Schnitt echter Weltdaten: vorderes natürliches Gestein ausgeblendet; sämtliche Reliktzellen im Ausschnitt sichtbar.',font=font(21),fill='#2b3932')
    path=ROOT/'docs/project/reviews/cave-roots-cutaway-20261007.png';canvas.save(path)
    evidence=json.loads((OUT/'manifest.json').read_bytes());evidence['image_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    path.with_suffix('.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8');print(path)


if __name__=='__main__':
    if '--render' in sys.argv:render()
    else:
        import argparse
        parser=argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--before',type=Path,default=BEFORE);parser.add_argument('--after',type=Path,default=AFTER)
        args=parser.parse_args();BEFORE=args.before.resolve();AFTER=args.after.resolve()
        extract()
        import subprocess
        subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe','--background','--threads','5',
            '--python-exit-code','1','--python',str(Path(__file__).resolve()),'--','--render'],check=True)
        compose()
