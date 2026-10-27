"""Derive approved gameplay templates alongside the frozen visual-alpha resources."""
import copy
import hashlib
import json
from pathlib import Path
from inspect_ots_result import read_structure
from relic_assets import encode_structure
from relic_catalog import ROOT, ASSETS
from terrain_foundations import supported_blocks, TOE_RADIUS
from build_gameplay_interiors import NATIVE
from validate_gameplay_handoff import validate

REVISION='interiors-20261027-v1'
INDEX=ROOT/'docs/project/reviews/gameplay-interiors-feedback-20261027-handoff.json'
# Neighbouring chunk decoration can already have grown a tree before this piece
# places. Restrict removal to omitted cells in the approved clearance regions.
RUNTIME_NATIVE=sorted(set(NATIVE)|{'minecraft:'+wood+'_log' for wood in
    ('oak','spruce','birch','jungle','acacia','dark_oak','mangrove','cherry','pale_oak')}|
    {'minecraft:'+wood+'_leaves' for wood in
    ('oak','spruce','birch','jungle','acacia','dark_oak','mangrove','cherry','pale_oak','azalea','flowering_azalea')})

def integrate(resources=ROOT/'src/main/resources',verify=False):
    index=json.loads(INDEX.read_text(encoding='utf-8'))
    old=json.loads((resources/'relics.integration.json').read_text())
    manifest=copy.deepcopy(old)
    manifest.update(selection='alpha5-gameplay',revision=REVISION,air_policy='bounded native clearance; preserve authored solids')
    registry=json.loads((ROOT/'docs/project/reviews/gameplay-registry-26.2.json').read_text())['blocks']
    registry.update(json.loads((ROOT/'docs/project/reviews/gameplay-interiors-feedback-20261027-registry.json').read_text())['blocks'])
    for entry in manifest['structures']:
        name=entry['id']
        if name not in index['assets']:continue
        files=index['assets'][name]['files'];source=ROOT/files['.nbt']['path']
        for ext in ('.nbt','.gameplay.json'):
            assert hashlib.sha256((ROOT/files[ext]['path']).read_bytes()).hexdigest()==files[ext]['sha256']
        root,raw=read_structure(source)
        side=json.loads((ROOT/files['.gameplay.json']['path']).read_text())
        validate(side,raw,root['size'],registry)
        if name in ('colossus','small_colossus','ruined_tower'):
            assert sum(m['role'].endswith('_chest') for m in side['markers'])==1,'Loot budget requires exactly one chest per site'
        contract={**ASSETS[name],'source':files['.nbt']['path'],'sha256':files['.nbt']['sha256'],
                  'version':side['asset_version'],'blocks':len(raw),'visually_accepted':True}
        blocks,size,foundation=supported_blocks(raw,contract)
        offset=[TOE_RADIUS,foundation['vertical_padding'],TOE_RADIUS]
        clear=set()
        for region in side['regions']:
            if not region['role'].endswith('_clearance'):continue
            assert set(region['replaceable_blocks'])==set(NATIVE)
            lo,hi=region['min'],region['max']
            for x in range(lo[0],hi[0]+1):
                for y in range(lo[1],hi[1]+1):
                    for z in range(lo[2],hi[2]+1):
                        if (x,y,z) not in raw:clear.add((x,y,z))
        if name=='colossus':
            # The approved new visor removes shell cells outside the old cockpit
            # region. Reserve only those removed cells, never the glass remnants.
            prior=ROOT/'relics/colossus/design/generated/colossus-v5-interiors/colossus-v5-interiors.nbt'
            _,previous=read_structure(prior)
            clear.update(p for p in previous if p not in raw and 86<=p[0]<=102 and 169<=p[1]<=177 and 145<=p[2]<=163)
        padded={tuple(a+b for a,b in zip(p,offset)) for p in clear}
        for p in padded:blocks.pop(p,None) # Foundation derivation may not close an authored passage.
        runs=[]
        for x,y,z in sorted(padded):
            if runs and runs[-1][0:2]==[x,y] and runs[-1][3]+1==z:runs[-1][3]=z
            else:runs.append([x,y,z,z])
        anchor=(size[0]//2,foundation['ground_y']-1,size[2]//2)
        assert anchor not in padded,'Clearance conflicts with surface anchor'
        final=blocks.get(anchor,'minecraft:structure_void');blocks[anchor]='minecraft:jigsaw[orientation=north_up]'
        nbt={k:(8,v) for k,v in {'id':'minecraft:jigsaw','name':'relics:center','target':'minecraft:empty',
              'pool':'minecraft:empty','joint':'rollable','final_state':final}.items()}
        nbt.update(selection_priority=(3,0),placement_priority=(3,0))
        natural=encode_structure(blocks,tuple(size),root['DataVersion'],{anchor:nbt})
        raw_name=f'{name}_gameplay.nbt';natural_name=f'{name}_gameplay_worldgen.nbt'
        destination=resources/'data/relics/structure';destination.mkdir(parents=True,exist_ok=True)
        for filename,content in ((raw_name,source.read_bytes()),(natural_name,natural)):
            target=destination/filename
            if verify:
                if not target.is_file() or target.read_bytes()!=content:raise ValueError('Stale approved gameplay template: '+str(target))
            else:target.write_bytes(content)
        entry.update(contract)
        entry['single_template']={'path':raw_name,'sha256':files['.nbt']['sha256']}
        entry['worldgen_template']={'path':natural_name,'sha256':hashlib.sha256(natural).hexdigest(),
            'size':size,'anchor':list(anchor),'final_state':final,'foundation':foundation}
        entry['gameplay']={'version':REVISION,'sidecar_sha256':files['.gameplay.json']['sha256'],
            'asset_version':side['asset_version'],'offset':offset,'markers':side['markers'],
            'clearance_runs':runs,'replaceable_blocks':RUNTIME_NATIVE}
    target=resources/'relics.gameplay.integration.json'
    if verify:
        if not target.is_file() or json.loads(target.read_text())!=manifest:raise ValueError('Stale approved gameplay manifest')
    else:target.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    return manifest

if __name__=='__main__':integrate()
