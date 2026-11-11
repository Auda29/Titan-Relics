"""Derive one upper-platform treasure niche from the frozen Ruined Tower V10."""
import copy,json
from build_gameplay_interiors import Builder,ROOT,ASSETS,STONE,WORN,TRIM,CHEST,digest
from inspect_ots_result import read_structure

STEM='ruined-tower-v11-upper-chest'
PARENT='ruined-tower-v10-chest'
PARENT_SHA256='d90f64ffe5f2ac273ea2b58852ef275cf2fd0169984baed8de98d5cc714a0c10'
BASE=(ROOT/ASSETS['ruined_tower']['source']).parent.parent
OLD=BASE/PARENT
OUT=BASE/STEM


def build():
    source=OLD/(PARENT+'.nbt');side=json.loads(source.with_suffix('.gameplay.json').read_text())
    assert digest(source)==side['source_sha256']==PARENT_SHA256
    design=json.loads(source.with_suffix('.design.json').read_text())
    assert design['nbt_sha256']==side['source_sha256']
    b=Builder('ruined_tower');b.root,blocks=read_structure(source)
    assert b.root['size']==[111,232,93] and side['ground_y']==12
    b.old=dict(blocks);b.blocks=dict(blocks);b.stem=STEM;b.out=OUT
    b.markers=copy.deepcopy(side['markers']);b.regions=copy.deepcopy(side['regions'])
    b.paths=copy.deepcopy(design['paths']);b.evidence=copy.deepcopy(design['evidence'])
    b.group='upper-platform-treasure-niche'
    def add(p,state):
        if p in b.old:return  # Join the surviving masonry without replacing it.
        assert (p[0],173,p[2]) in b.old,('Outside the existing landing',p)
        b.put(p,state)
    # The landing is reached by the original incomplete wall-side ascent.
    # All additions stand on its existing floor; no wall, stair or gap is cut.
    for x in range(71,76):
        for y in range(174,177 if x!=74 else 176):
            add((x,y,55),WORN if (x+y)%3 else STONE)
    for x,top in ((71,177),(75,176)):
        for y in range(174,top+1):add((x,y,56),TRIM if y<top else WORN)
    b.marker('tower_summit_chest',(73,174,56),facing='south',placeholder=CHEST)
    add((71,178,56),'minecraft:lantern[hanging=false,waterlogged=false]')
    b.region('tower_route_clearance',(72,174,56),(74,178,58))
    b.path('tower-upper-landing-to-treasure',[(72,174,57),(73,174,57)],3)
    b.evidence['v11_parent']={'nbt':source.relative_to(ROOT).as_posix(),'sha256':digest(source),'sidecar_sha256':digest(source.with_suffix('.gameplay.json'))}
    b.evidence['upper_chest']={'position':[73,174,56],'facing':'south','approach':[73,174,57],
        'existing_ascent_destination':[72,174,57],'source_changes':'additions only on existing Y173 platform',
        'loot':'one Feather Falling IV book, 3-6 diamonds, 8-16 iron ingots; once per new tower'}
    b.evidence['feedback_revision']='Upper-platform chest requested by the author on 2026-11-11; native validation pending'
    return b

def write_handoff():
    index=json.loads((ROOT/'docs/project/reviews/tree-skull-feedback-20261028-handoff.json').read_text())
    files={}
    for suffix in ('.nbt','.schem','.gameplay.json','.design.json'):
        path=OUT/(STEM+suffix)
        files[suffix]={'path':path.relative_to(ROOT).as_posix(),'sha256':digest(path),'bytes':path.stat().st_size}
    side=json.loads((OUT/(STEM+'.gameplay.json')).read_text())
    index['assets']['ruined_tower']={'files':files,'size':side['size'],'ground_y':side['ground_y'],
        'blocks':sum(json.loads((OUT/(STEM+'.design.json')).read_text())['palette'].values()),'markers':len(side['markers']),'regions':len(side['regions'])}
    index['status']='Upper platform treasure niche requested 2026-11-11; native validation pending'
    (ROOT/'docs/project/reviews/tower-upper-chest-20261111-handoff.json').write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8',newline='\n')

if __name__=='__main__':
    build().save()
    for path in OUT.rglob('*.json'):
        path.write_text(path.read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
    write_handoff()
