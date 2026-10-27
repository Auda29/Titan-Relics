"""Publish a separate feedback handoff; the original index remains untouched."""
import hashlib
import json
from build_gameplay_interiors import ROOT,ASSETS
from build_gameplay_interiors_revision import STEMS

def main():
    original=json.loads((ROOT/'docs/project/reviews/gameplay-interiors-handoff.json').read_text())
    index={k:v for k,v in original.items() if k!='assets'}
    index['baseline_commit']='cf1d2e56315bcbce11bb37d363b5c34815a5cb33'
    index['status']='feedback revisions; visual review and runtime integration pending'
    index['assets']={}
    for name,stem in STEMS.items():
        folder=(ROOT/ASSETS[name]['source']).parent.parent/stem
        report=json.loads((folder/'verification.json').read_text())
        source=json.loads((folder/'source-verification.json').read_text())
        assert report['nbt_sha256']==source['bound_nbt_sha256']
        report['editable_source']=source
        (folder/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
        files={}
        for suffix in ('.nbt','.schem','.gameplay.json','.design.json','-source.blend','-review.png','-markers-review.png'):
            p=folder/(stem+suffix);data=p.read_bytes()
            files[suffix]={'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
        index['assets'][name]={'files':files,'size':report['size'],'ground_y':ASSETS[name]['ground_y'],
                               'blocks':report['blocks'],'markers':report['markers'],'regions':report['regions']}
    index['assets']['world_tree']=original['assets']['world_tree']
    for entry in index['assets']['world_tree']['files'].values():
        assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256']
    out=ROOT/'docs/project/reviews/gameplay-interiors-feedback-20261027-handoff.json'
    out.write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8',newline='\n');print(out)

if __name__=='__main__':main()
