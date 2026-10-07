"""Same-world-coordinate slices and overview renders for the two cave candidates."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
OUT=ROOT/'build/cave-contacts/20261007/views'
SLICES=[('skull-cave', 'SCHÄDEL 2 / tiefer Höhlenanschnitt', 'x', -13139, 36278, 36301, 38, 65),
        ('tree-cave-north', 'BAUM / nördliche Höhlenwand', 'x', 23744, -45565, -45535, 40, 73),
        ('tree-cave-west', 'BAUM / westlicher Wurzeldurchtritt', 'z', -45470, 23660, 23692, 40, 72)]
COLORS={'minecraft:stone':'#777a7c', 'minecraft:dirt':'#725239', 'minecraft:grass_block':'#638441',
        'minecraft:bone_block':'#e5debc', 'minecraft:calcite':'#dadad4', 'minecraft:dripstone_block':'#94756d',
        'minecraft:spruce_log':'#866238', 'minecraft:stripped_spruce_log':'#ac8259',
        'minecraft:moss_block':'#587432', 'minecraft:water':'#406896', 'minecraft:oak_leaves':'#3a6538'}


def slices(before_path, after_path):
    from PIL import Image,ImageDraw,ImageFont
    from verify_world import AnvilWorld,AIR_NAMES,protected_cell
    reports=[json.loads(p.read_bytes()) for p in (before_path,after_path)]
    assert all(r['passed'] and not r['showcase'] for r in reports)
    worlds=[AnvilWorld(Path(r['run_directory'])/'world') for r in reports]
    image=Image.new('RGB',(1500,1580),'#18212d');draw=ImageDraw.Draw(image)
    font=lambda s:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',s)
    draw.text((20,14),'HÖHLENKONTAKTE / GLEICHE WELTKOORDINATEN',font=font(29),fill='white')
    draw.text((20,58),'Links: Alpha 4.8  |  Rechts: neuer Kandidat  |  Orange Umrandung: gespeicherte Reliktzellen',font=font(21),fill='#bfcddd')
    records=[]
    for row,(name,title,axis,fixed,u0,u1,y0,y1) in enumerate(SLICES):
        top=105+row*475;draw.text((20,top),title,font=font(25),fill='white')
        cell=min(20,410//(y1-y0),680//(u1-u0));saved=[]
        for col,w in enumerate(worlds):
            cells=[];left=25+col*750
            for u in range(u0,u1):
                for y in range(y0,y1):
                    p=(fixed,y,u) if axis=='x' else (u,y,fixed)
                    state=w.block(*p)
                    assert state is not None
                    protected=protected_cell(w.chunk(p[0]//16,p[2]//16),p)
                    cells.append({'position':p,'state':state,'relic_protected':protected})
                    block=state['Name'];color='#0c1118' if block in AIR_NAMES else COLORS.get(block,'#888474')
                    xx=left+(u-u0)*cell;yy=top+45+(y1-1-y)*cell
                    draw.rectangle((xx,yy,xx+cell-1,yy+cell-1),fill=color,
                                   outline='#dd9d50' if protected else '#25313b')
            saved.append(cells)
            draw.text((left,top+450),f'{axis.upper()}={fixed}, Y {y0}–{y1-1}',font=font(17),fill='#bfcddd')
        records.append({'id':name,'cells_before_after':saved})
    draw.text((20,1540),'Echte gespeicherte Blöcke, schematische Materialfarben; schwarze Zellen sind Luft. Keine Clientaufnahme.',font=font(19),fill='#bfcddd')
    image_path=ROOT/'docs/project/reviews/cave-contacts-20261007.png';image.save(image_path)
    evidence={'scope':'Exact saved-world slices; natural cavities and saved protection masks',
              'reports':[{'path':p.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (before_path,after_path)],
              'slices':records,'image_sha256':hashlib.sha256(image_path.read_bytes()).hexdigest()}
    (OUT/'slices.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
    print(image_path)


def render():
    import render_rooted_sites as renderer
    renderer.VIEWS=OUT
    renderer.PAIRS=[('titan_skull_2','SCHÄDEL 2 / kurzer Materialkontakt, flacher unterirdischer Fußabdruck',75),
                    ('world_tree','BAUM / einzelne Wurzelstränge, kurze Oberflächenkontakte',25)]
    renderer.render()


def compose():
    from PIL import Image,ImageDraw,ImageFont
    image=Image.new('RGB',(1800,1700),'#eeeade');draw=ImageDraw.Draw(image)
    font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
    draw.text((25,14),'Links: Alpha 4.8  |  Rechts: Höhlenkontakt-Kandidat',font=font(32),fill='#2b3932')
    for row,(name,title) in enumerate((('titan_skull_2','SCHÄDEL 2 / Erdsaum durch kurze anatomische Kontakte ersetzt'),('world_tree','BAUM / Wurzelbereich mit sparsamen, verzweigten Fortsätzen'))):
        y=75+row*785;draw.text((25,y),title,font=font(28),fill='#2b3932')
        picture=Image.open(OUT/(name+'.png')).convert('RGB');picture.thumbnail((1740,715),Image.Resampling.LANCZOS)
        image.paste(picture,((1800-picture.width)//2,y+45))
    draw.text((25,1655),'Gerenderte gespeicherte Weltdaten, identische Ausschnitte; vereinfachte Texturen und kleine Pflanzen ausgelassen.',font=font(20),fill='#2b3932')
    path=ROOT/'docs/project/reviews/cave-contacts-surface-20261007.png';image.save(path);print(path)
    provenance=json.loads((OUT/'manifest.json').read_bytes())
    provenance['texture_fallbacks']=json.loads((OUT/'texture-fallbacks.json').read_bytes())
    provenance['slice_planes']=SLICES
    provenance['slice_data_sha256']=hashlib.sha256((OUT/'slices.json').read_bytes()).hexdigest()
    provenance['images']=[{'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
                         for p in (path,ROOT/'docs/project/reviews/cave-contacts-20261007.png')]
    (ROOT/'docs/project/reviews/cave-contacts-20261007.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    if '--render' in sys.argv:
        render()
    else:
        parser=argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--before',type=Path,required=True);parser.add_argument('--after',type=Path,required=True)
        args=parser.parse_args()
        OUT.mkdir(parents=True,exist_ok=True)
        slices(args.before,args.after)
        import subprocess
        subprocess.run([sys.executable,str(ROOT/'tools/extract_rooted_sites.py'),'--before',str(args.before),
            '--after',str(args.after),'--output',str(OUT),'--structures','titan_skull_2','world_tree'],check=True)
        subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe','--background','--threads','5',
            '--python-exit-code','1','--python',str(Path(__file__).resolve()),'--','--render'],check=True)
        compose()
