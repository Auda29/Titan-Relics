"""V11 derivative of exported V10; six-block shorter lower entry only."""
import copy,json
from build_gameplay_interiors import Builder,ROOT,ASSETS,WORN,digest
from inspect_ots_result import read_structure
STEM='small-colossus-v11-short-entry'
V10='small-colossus-v10-landmarks'
BASE=(ROOT/ASSETS['small_colossus']['source']).parent.parent
OLD=BASE/V10
OUT=BASE/STEM
PARENT_HASH='7d88093eece8e8de1d8b8ca3e316ae516e8b5c6dcdfc20b50b8fc35586133db8'
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def build():
    path=OLD/(V10+'.nbt');assert digest(path)==PARENT_HASH
    side=json.loads(path.with_suffix('.gameplay.json').read_text());design=json.loads(path.with_suffix('.design.json').read_text())
    assert side['source_sha256']==design['nbt_sha256']==PARENT_HASH
    b=Builder('small_colossus');catalog=dict(b.old)
    b.root,blocks=read_structure(path);b.old=dict(blocks);b.blocks=dict(blocks);b.stem=STEM;b.out=OUT
    b.markers=copy.deepcopy(side['markers']);b.regions=copy.deepcopy(side['regions']);b.paths=copy.deepcopy(design['paths']);b.evidence=copy.deepcopy(design['evidence'])
    b.group='shortened-lower-entry'
    for z in range(40,47):
        y=13 if z<46 else 14
        for x in range(59,66):
            p=(x,y,z);assert p not in catalog and b.blocks[p]==WORN
            b.put(p,None)
    removed=[]
    kept=[]
    for reg in b.regions:
        if reg['min'][0]==59 and reg['max'][0]==65 and reg['min'][2]==reg['max'][2] and 40<=reg['min'][2]<=45:
            removed.append(reg['id']);continue
        if reg['min']==[59,15,46] and reg['max']==[65,19,46]:reg['min'][1]=14
        kept.append(reg)
    assert len(removed)==6;b.regions=kept
    route=next(p for p in b.paths if p['name']=='breast-rupture-entry')
    route['feet']=[p for p in route['feet'] if p[2]>=46];route['feet'][0]=[62,14,46]
    b.evidence['v11_parent']={'nbt':path.relative_to(ROOT).as_posix(),'sha256':PARENT_HASH,'sidecar_sha256':digest(path.with_suffix('.gameplay.json'))}
    b.evidence['feedback_revision']='V11 six-block shorter lower entry; model only; runtime integration and user acceptance pending'
    b.evidence['short_entry']={'shortening_blocks':6,'start':[62,14,46],'removed_regions':removed,'lowered_region':'small-interior-clearance-9','catalog_solids_changed':0}
    b.evidence['views']=[{'label':'Short lower entrance, full export geometry','lo':[0,0,0],'hi':[110,79,112]}]
    return b
if __name__=='__main__':
    b=build();b.save()
    p=OUT/(STEM+'.design.json');d=json.loads(p.read_text());d['change_reference']='V10 pinned in evidence.v11_parent; catalog provenance retained';write(p,d)
    # Retained threshold is editable as a separate group even though its floor is unchanged.
    groups=json.loads((OUT/(STEM+'.groups.json')).read_text());groups['shortened-lower-entry']=[[x,13,46] for x in range(59,66)];write(OUT/(STEM+'.groups.json'),groups)
    for p in OUT.rglob('*.json'):write(p,json.loads(p.read_text()))
