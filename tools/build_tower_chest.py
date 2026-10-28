"""Ruined Tower V10: local chest stand derived from pinned V9."""
import copy,json
from build_gameplay_interiors import Builder,ROOT,ASSETS,STONE,WORN,TRIM,digest
from inspect_ots_result import read_structure
STEM='ruined-tower-v10-chest'
V9='ruined-tower-v9-interiors'
BASE=(ROOT/ASSETS['ruined_tower']['source']).parent.parent
OLD=BASE/V9
OUT=BASE/STEM
PARENT_HASH='4f5fd420eb1461b8e1b3f1c9f8f90ede3e801ea8d1e20972aab3d78d9a9fad8d'
def build():
    path=OLD/(V9+'.nbt');side=json.loads(path.with_suffix('.gameplay.json').read_text())
    assert digest(path)==side['source_sha256']==PARENT_HASH
    design=json.loads(path.with_suffix('.design.json').read_text());assert design['nbt_sha256']==PARENT_HASH
    b=Builder('ruined_tower');b.root,blocks=read_structure(path)
    assert b.root['size']==[111,232,93] and b.root['DataVersion']==3105 and side['ground_y']==12
    b.old=dict(blocks);b.blocks=dict(blocks);b.stem=STEM;b.out=OUT
    b.markers=copy.deepcopy(side['markers']);b.regions=copy.deepcopy(side['regions'])
    b.paths=copy.deepcopy(design['paths']);b.evidence=copy.deepcopy(design['evidence'])
    m=next(m for m in b.markers if m['role']=='tower_ender_chest')
    assert m['pos']==[72,15,55] and m['id']=='tower-ender-chest-1'
    b.group='retired-tower-chest';b.put(m['pos'],None)
    b.group='tower-rear-wall-stand'
    def add(p,state):
        assert p not in b.old,p
        b.put(p,state)
    for x in range(56,61):
        for z in (56,57):
            for y in range(15,18 if x in (56,60) else 19):
                add((x,y,z),WORN if (x+y+z)%3 else STONE)
    for x,top in ((56,19),(60,18)):
        for y in range(15,top+1):add((x,y,55),TRIM if y<top else WORN)
    m['pos']=[58,15,55];m['facing']='north';add(tuple(m['pos']),m['expected_block'])
    b.region('tower_route_clearance',(56,15,52),(60,21,57))
    b.path('tower-entry-to-rear-chest',[(57,15,z) for z in range(20,49)]+[(58,15,48)]+[(58,15,z) for z in range(49,55)],3)
    b.evidence['v10_parent']={'nbt':path.relative_to(ROOT).as_posix(),'sha256':PARENT_HASH,'sidecar_sha256':digest(path.with_suffix('.gameplay.json'))}
    b.evidence['feedback_revision']='V10 rear-wall chest stand; model only, runtime integration and user approval pending'
    b.evidence['terrain_clearance_contract']='Subtract all source solids from each tower_route_clearance volume; retain floor, partitions, stand and ascent. Root handles bounded ore allow-list.'
    return b
if __name__=='__main__':
    build().save()
    for p in OUT.glob('*.json'):
        d=json.loads(p.read_text());p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
