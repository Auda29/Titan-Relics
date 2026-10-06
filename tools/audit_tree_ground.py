"""Read-only root/terrain cross sections from the saved Alpha 4.3 natural test."""
import json
import hashlib
from collections import Counter
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from inspect_ots_result import read_structure
from verify_world import AnvilWorld,transform
from terrain_foundations import TOE_RADIUS,padding

RUN=ROOT/'build/smoke/run-20261005-124958-97f7626d565d'
OUT=ROOT/'build/screenshot-review/20261006-alpha4-3/ground-audit'


def main():
    from PIL import Image,ImageDraw,ImageFont
    report=json.loads((RUN/'report.json').read_text())
    instance=next(i for i in report['world_blocks']['instances'] if i['structure']=='relics:world_tree')
    contract=next(c for c in report['asset_selection']['structures'] if c['id']=='world_tree')
    source=ROOT/contract['source']
    if hashlib.sha256(source.read_bytes()).hexdigest()!=contract['sha256']:
        raise ValueError('Saved-run source hash changed')
    _,blocks=read_structure(source)
    world=AnvilWorld(RUN/'world');ground=contract['ground_y'];pad=padding(contract)
    def pos(p):return transform((p[0]+TOE_RADIUS,p[1]+pad,p[2]+TOE_RADIUS),instance['rotation'],instance['origin'])
    def state(p):
        value=world.block(*pos(p))
        if value is None:raise ValueError(f'Missing world chunk at {pos(p)}')
        return value['Name']
    lowest={}
    for (x,y,z),s in blocks.items():
        if 'log' in s:lowest[x,z]=min(y,lowest.get((x,z),y))
    gaps=[];contacts=0;missing=0
    for (x,z),y in lowest.items():
        if y>ground+2:continue
        if 'log' not in state((x,y,z)):missing+=1
        below=state((x,y-1,z))
        if below not in ('minecraft:air','minecraft:cave_air','minecraft:water','minecraft:void_air'):
            contacts+=1;continue
        depth=0
        while depth<32 and state((x,y-1-depth,z)) in ('minecraft:air','minecraft:cave_air','minecraft:water','minecraft:void_air'):
            depth+=1
        gaps.append({'raw_position':[x,y,z],'world_position':list(pos((x,y,z))),'gap':depth,'below':below})
    OUT.mkdir(parents=True,exist_ok=True)
    result={'world':str(RUN/'world'),'tree_instance':instance,'low_root_columns':contacts+len(gaps),
            'baseline_nbt_sha256':contract['sha256'],
            'runtime_report_sha256':hashlib.sha256((RUN/'report.json').read_bytes()).hexdigest(),
            'direct_contacts':contacts,'missing_expected_wood':missing,'low_root_gap_columns':len(gaps),
            'gaps_by_root_height_above_nominal_ground':dict(sorted(Counter(p['raw_position'][1]-ground for p in gaps).items())),
            'gap_examples':sorted(gaps,key=lambda p:p['gap'],reverse=True),
            'scope':'Lowest log per X/Z column at or below nominal ground +2; arched roots above that band excluded'}
    if '--candidate' in sys.argv:
        from terrain_foundations import supported_blocks
        candidate=ROOT/'relics/world-tree/design/generated/world-tree-v4-1/world-tree-v4-1.nbt'
        candidate_root,candidate_blocks=read_structure(candidate)
        assert list(candidate_root['size'])==contract['size'],'Projection requires identical placement bounds'
        overlay,_,_=supported_blocks(candidate_blocks,contract)
        remaining=[]
        for item in gaps:
            x,y,z=item['raw_position'];q=(x+TOE_RADIUS,y-1+pad,z+TOE_RADIUS)
            s=overlay.get(q,state((x,y-1,z))).split('[')[0]
            if s in ('minecraft:air','minecraft:cave_air','minecraft:water','minecraft:void_air'):remaining.append(item)
        result['candidate_projection']={'candidate':str(candidate.relative_to(ROOT)),
            'kind':'Read-only overlay of candidate derived foundation onto saved terrain; not a new runtime test',
            'remaining_low_root_gap_columns':len(remaining),
            'remaining_at_or_below_ground':sum(p['raw_position'][1]<=ground for p in remaining),
            'remaining_ground_edge_examples':[p for p in remaining if p['raw_position'][1]<=ground],
            'closed_low_root_gap_columns':len(gaps)-len(remaining)}
    (OUT/'tree-ground.json').write_text(json.dumps(result,indent=2)+'\n')
    font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
    canvas=Image.new('RGB',(1200,650),'#eee9de');draw=ImageDraw.Draw(canvas)
    draw.text((25,15),'WORLD TREE / SAVED ALPHA 4.3 TERRAIN / ROOT CROSS SECTIONS',font=font(23),fill='#293934')
    colors={'minecraft:grass_block':'#6b8547','minecraft:dirt':'#806448','minecraft:rooted_dirt':'#927553',
            'minecraft:moss_block':'#687843','minecraft:water':'#568aa5'}
    for row,z in enumerate((65,95,125)):
        top=70+row*165
        draw.text((25,top),f'Raw Z={z}; nominal ground = Y{ground}',font=font(17),fill='#293934')
        for x in range(20,177):
            for y in range(-14,20):
                s=state((x,y,z));color=colors.get(s)
                if color is None:
                    color='#a68152' if 'log' in s else '#376147' if 'leaves' in s else '#c6d5db' if s.endswith(('air','grass','fern')) else '#73797c'
                px=30+(x-20)*7;py=top+28+(19-y)*3
                draw.rectangle((px,py,px+6,py+2),fill=color)
        line=top+28+(19-ground)*3
        draw.line((30,line,1128,line),fill='#e5b15d',width=1)
    draw.text((25,592),f'Low root columns: {contacts} direct contacts / {len(gaps)} air or water gaps; soil supports: {instance["foundation_contact"]["unsupported_columns"]} unsupported.',font=font(18),fill='#293934')
    canvas.save(OUT/'tree-ground-sections.png')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
