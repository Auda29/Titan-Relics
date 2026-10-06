"""Pin the eight art candidates and their required placement contracts for integration."""
import hashlib
import json
from pathlib import Path

from build_embedding_relief import BASELINES
from inspect_ots_result import read_structure
from relic_catalog import ASSETS
from terrain_foundations import supported_blocks

ROOT=Path(__file__).resolve().parents[1]
MODELS={
 'titan_skull_2':('titan-skull','titan-skull-2-v2','titan-skull-2-v1-ground-v2',12,4,
                  '1d4b8da9d888355da29d7d3caa1b419f00d1ef3ed051fa018ac0ad0efa5565b6'),
}


def main():
    target=ROOT/'build/embedding-relief';target.mkdir(parents=True,exist_ok=True);records=[]
    for name,(folder,stem,baseline,old_ground,slope,digest) in MODELS.items():
        source=ROOT/f'relics/{folder}/design/generated/{stem}/{stem}.nbt'
        old=source.parent.parent/baseline/(baseline+'.nbt')
        assert hashlib.sha256(old.read_bytes()).hexdigest()==digest
        report=json.loads((source.parent/'verification.json').read_text());meta=json.loads(source.with_suffix('.design.json').read_text())
        root,blocks=read_structure(source);checksum=hashlib.sha256(source.read_bytes()).hexdigest()
        assert report['nbt_sha256']==checksum and report['blocks']==len(blocks)
        features=report['new_relic_v1']
        assert features['ground_level']==meta['ground_level_nbt_approx']
        contract=dict(ASSETS[name]);contract.update(source=source.relative_to(ROOT).as_posix(),version=stem,
            size=root['size'],blocks=len(blocks),sha256=checksum,ground_y=meta['ground_level_nbt_approx'],slope=slope,visually_accepted=False)
        natural,_,foundation=supported_blocks(blocks,contract)
        pad=foundation['vertical_padding'];h=foundation['horizontal_padding']
        assert all(natural[x+h,y+pad,z+h]==s for (x,y,z),s in blocks.items())
        report={**report,'placement_contract':contract,'foundation':foundation}
        record={'id':name,'baseline':old.relative_to(ROOT).as_posix(),'baseline_ground_y':old_ground,
                'candidate':stem,'source':contract['source'],'ground_y':contract['ground_y'],'verification':report}
        (target/(name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
    for name in (*BASELINES,*MODELS):
        record=json.loads((target/(name+'.json')).read_text());contract=record['verification']['placement_contract']
        assert hashlib.sha256((ROOT/contract['source']).read_bytes()).hexdigest()==contract['sha256']
        records.append({'id':name,**contract})
    output=ROOT/'docs/project/embedding-candidates-20261006.json'
    output.write_text(json.dumps({'status':'visual candidates; new runtime validation pending',
        'basis':'Alpha 4.5 screenshots; current installed artifact is not changed by this index',
        'placement_note':'Use these ground_y AND slope values together with these exact NBT hashes. Do not reuse Alpha 4.5 burial.',
        'structures':records},indent=2)+'\n')
    print(output)


if __name__=='__main__':main()
