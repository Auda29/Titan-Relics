"""Small Colossus V10: bounded derivative of the pinned V9 export."""
import copy,json
from build_gameplay_interiors import Builder,ROOT,ASSETS,STONE,WORN,TRIM,digest
from inspect_ots_result import read_structure
STEM='small-colossus-v10-landmarks'
V9='small-colossus-v9-interiors'
BASE=(ROOT/ASSETS['small_colossus']['source']).parent.parent
OLD=BASE/V9
OUT=BASE/STEM
PARENT_HASH='565b8461b8aed3d4ab1bdca35859790b280d39167c970a80df96a2dab75d68c0'

def build():
    path=OLD/(V9+'.nbt')
    side=json.loads(path.with_suffix('.gameplay.json').read_text())
    assert digest(path)==side['source_sha256']==PARENT_HASH
    b=Builder('small_colossus'); b.root,blocks=read_structure(path)
    assert b.root['size']==[111,80,113] and b.root['DataVersion']==3105 and side['ground_y']==13
    b.old=dict(blocks);b.blocks=dict(blocks);b.stem=STEM;b.out=OUT
    b.markers=copy.deepcopy(side['markers']);b.regions=copy.deepcopy(side['regions'])
    design=json.loads(path.with_suffix('.design.json').read_text())
    assert design['nbt_sha256']==PARENT_HASH
    b.paths=copy.deepcopy(design['paths']);b.evidence=copy.deepcopy(design['evidence'])
    m=b.markers[0];assert len(b.markers)==1 and m['role']=='small_magnet_chest' and m['pos']==[73,19,80]
    assert b.blocks[tuple(m['pos'])]==m['expected_block']=='minecraft:waxed_cut_copper'
    b.group='retired-lower-find';b.put(m['pos'],None)
    b.group='upper-salvage-frame'
    # All frame cells start empty; the surviving platform and rib stay intact.
    def add(lo,hi,state):
        for x in range(lo[0],hi[0]+1):
            for y in range(lo[1],hi[1]+1):
                for z in range(lo[2],hi[2]+1):
                    assert (x,y,z) not in b.old,(x,y,z)
                    b.put((x,y,z),state)
    add((68,44,51),(68,46,55),WORN)
    add((68,47,51),(68,47,53),STONE)
    for z,top in ((51,48),(55,47)):
        add((67,44,z),(67,top-1,z),TRIM)
        add((67,top,z),(67,top,z),'minecraft:chiseled_deepslate')
    m['pos']=[67,44,53];m['facing']='west';b.put(m['pos'],m['expected_block'])
    # Region volumes are masks: runtime must subtract ALL source solids.
    b.region('small_interior_clearance',(62,43,53),(66,47,58))
    b.region('small_interior_clearance',(64,44,50),(68,50,56))
    b.path('upper-landing-to-salvage',[(61,43,58),(61,43,57),(62,43,57),(63,43,57),(64,44,57),(64,44,56),(65,44,56),(65,44,55),(65,44,54),(65,44,53),(66,44,53)],3)
    b.evidence['v10_parent']={'nbt':path.relative_to(ROOT).as_posix(),'sha256':PARENT_HASH,'sidecar_sha256':digest(path.with_suffix('.gameplay.json'))}
    b.evidence['feedback_revision']='V10 upper salvage frame; not runtime integrated; user visual review pending'
    b.evidence['terrain_clearance_contract']='Clear only source-free cells in small_interior_clearance; retain all source frame, floor and shell blocks. Runtime ore allow-list update remains with root.'
    b.evidence['views']=[{'label':'Second stair end and west-facing salvage frame','lo':[57,35,48],'hi':[71,51,68]}, {'label':'Frame and free lid volume','lo':[63,42,49],'hi':[69,51,57]}]
    return b

if __name__=='__main__':
    build().save()
    p=OUT/(STEM+'.design.json');d=json.loads(p.read_text());d['change_reference']='V9 pinned in evidence.v10_parent; catalog baseline is provenance only'
    p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
