"""Read-only saved-site sections: authored soil, derived supports and native terrain."""
import hashlib
import json
from collections import Counter
from pathlib import Path

from inspect_ots_result import read_structure
from terrain_foundations import TOE_RADIUS,padding
from verify_world import AnvilWorld,transform,protected_cell

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'build/smoke/run-20261006-104446-781ff9011d44'
OUT=ROOT/'build/screenshot-review/20261006-alpha4-5/embedding-audit'
NAMES=('small_colossus','titan_skull_dry','titan_skull_rock','titan_skull_2','world_tree')


def main():
    from PIL import Image,ImageDraw,ImageFont
    report=json.loads((RUN/'report.json').read_text());world=AnvilWorld(RUN/'world')
    OUT.mkdir(parents=True,exist_ok=True);records=[]
    canvas=Image.new('RGB',(1440,1250),'#efeade');draw=ImageDraw.Draw(canvas)
    font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
    draw.text((20,12),'ALPHA 4.5 / SAVED WORLD / VERTICAL SECTIONS',font=font(26),fill='#293934')
    draw.text((20,50),'Brown: authored soil | orange: added support | dark: art | green: unmasked terrain | blue: water',font=font(18),fill='#293934')
    for row,name in enumerate(NAMES):
        contract=next(c for c in report['asset_selection']['structures'] if c['id']==name)
        instance=next(i for i in report['world_blocks']['instances'] if i['structure']=='relics:'+name)
        path=ROOT/contract['source'];assert hashlib.sha256(path.read_bytes()).hexdigest()==contract['sha256']
        _,blocks=read_structure(path);ground=contract['ground_y'];pad=padding(contract)
        config=json.loads((path.parents[2]/(path.stem+'.json')).read_text())
        soil={s for k,s in config['materials'].items() if k.startswith('terrain_')}
        soil-=set(s for k,s in config['materials'].items() if not k.startswith('terrain_'))
        def pos(x,y,z):return transform((x+TOE_RADIUS,y+pad,z+TOE_RADIUS),instance['rotation'],instance['origin'])
        # Longitudinal central section shows posterior overhang and spinal deposits.
        x=contract['size'][0]//2;bottom=ground-28;top=ground+28;counts=Counter()
        y0=90+row*224;draw.text((20,y0),f'{name} / raw X={x} / nominal ground Y={ground}',font=font(19),fill='#293934')
        length=contract['size'][2];sx=1320/(length+24);sy=3.2
        for z in range(-12,length+12):
            for y in range(bottom,top+1):
                p=pos(x,y,z);actual=world.block(*p)
                if actual is None:raise ValueError(f'Missing chunk at {p}')
                state=actual['Name'];color='#dce6e8'
                if state not in ('minecraft:air','minecraft:cave_air','minecraft:void_air'):
                    if state=='minecraft:water':color='#719fbd';kind='water'
                    elif (x,y,z) in blocks:
                        kind='authored_soil' if blocks[x,y,z] in soil else 'art'
                        color='#987551' if kind=='authored_soil' else '#363d36'
                    elif protected_cell(world.chunk(p[0]//16,p[2]//16),p):kind='derived_support';color='#d69245'
                    else:kind='unmasked_terrain';color='#71865c'
                    counts[kind]+=1
                px=25+(z+12)*sx;py=y0+30+(top-y)*sy
                draw.rectangle((px,py,px+sx,py+sy),fill=color)
        line=y0+30+(top-ground)*sy;draw.line((25,line,1345,line),fill='#d75146',width=1)
        above=[y-ground for (x,y,z),s in blocks.items() if s in soil and y>=ground]
        records.append({'id':name,'source':contract['source'],'source_sha256':contract['sha256'],
            'origin':instance['origin'],'rotation':instance['rotation'],'ground_y':ground,
            'max_authored_soil_above_ground':max(above,default=0),'authored_soil_cells_at_or_above_ground':len(above),
            'section_raw_x':x,'section_counts':dict(counts)})
    canvas.save(OUT/'saved-sections.png')
    result={'run':RUN.relative_to(ROOT).as_posix(),'report_sha256':hashlib.sha256((RUN/'report.json').read_bytes()).hexdigest(),
        'scope':'Saved post-placement sections; unmasked blocks are surviving terrain, not a reconstruction of overwritten native surfaces.',
        'records':records}
    (OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
