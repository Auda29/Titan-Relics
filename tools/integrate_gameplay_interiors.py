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

PREVIOUS_REVISION='interiors-20261027-v1'
LANDMARK_REVISION='interiors-20261028-v2'
SMALL_LANDMARK_REVISION='interiors-20261028-v3'
SHORT_ENTRY_REVISION='interiors-20261028-v4'
TREE_SKULL_REVISION='interiors-20261028-v5'
REVISION='interiors-20261111-v6'
PREVIOUS_INDEX=ROOT/'docs/project/reviews/gameplay-interiors-feedback-20261027-handoff.json'
LANDMARK_INDEX=ROOT/'docs/project/reviews/colossus-landmarks-20261028-handoff.json'
SMALL_LANDMARK_INDEX=ROOT/'docs/project/reviews/small-colossus-landmarks-20261028-handoff.json'
SHORT_ENTRY_INDEX=ROOT/'docs/project/reviews/interiors-short-entry-tower-20261028-handoff.json'
TREE_SKULL_INDEX=ROOT/'docs/project/reviews/tree-skull-feedback-20261028-handoff.json'
INDEX=ROOT/'docs/project/reviews/tower-upper-chest-20261111-handoff.json'
MANIFESTS={PREVIOUS_REVISION:'relics.gameplay.integration.json',LANDMARK_REVISION:'relics.gameplay.landmarks.integration.json',SMALL_LANDMARK_REVISION:'relics.gameplay.small_landmarks.integration.json',SHORT_ENTRY_REVISION:'relics.gameplay.short_entry_tower.integration.json',TREE_SKULL_REVISION:'relics.gameplay.tree_skull.integration.json',REVISION:'relics.gameplay.tower_summit.integration.json'}
# Neighbouring chunk decoration can already have grown a tree before this piece
# places. Restrict removal to omitted cells in the approved clearance regions.
RUNTIME_NATIVE=sorted(set(NATIVE)|{'minecraft:'+wood+'_log' for wood in
    ('oak','spruce','birch','jungle','acacia','dark_oak','mangrove','cherry','pale_oak')}|
    {'minecraft:'+wood+'_leaves' for wood in
    ('oak','spruce','birch','jungle','acacia','dark_oak','mangrove','cherry','pale_oak','azalea','flowering_azalea')})
# Surface veins can occupy the same bounded omitted cells as their stone host.
# Preserve the old revision's exact allow-list/fingerprint and protect authored solids.
LANDMARK_NATIVE=sorted(set(RUNTIME_NATIVE)|{
    'minecraft:'+prefix+ore+'_ore' for prefix in ('','deepslate_')
    for ore in ('coal','iron','copper','gold','redstone','lapis','diamond','emerald')
}|{'minecraft:'+name for name in ('clay','mud','packed_mud','podzol','mycelium','red_sand',
    'sandstone','red_sandstone','calcite','dripstone_block','moss_block','snow','snow_block')})
V4_NATIVE=sorted(set(LANDMARK_NATIVE)|{'minecraft:bush'})

def source_path(relative):
    # Preserve frozen provenance strings while accepting Windows-authored
    # handoffs on POSIX build hosts as well.
    return ROOT/relative.replace('\\','/')

def bound_files(asset):
    # Handoffs may key records by suffix or full filename. Bind exactly one
    # whole-template source and sidecar, never the separate tile collection.
    selected={}
    for suffix in ('.nbt','.gameplay.json'):
        candidates=[e for e in asset['files'].values() if e['path'].endswith(suffix)]
        if len(candidates)!=1:raise ValueError('Ambiguous handoff source: '+suffix)
        selected[suffix]=candidates[0]
    return selected

def integrate_visual(entry,binding,resources,verify,revision):
    """Select a marker-free visual revision without changing legacy templates."""
    handoff=source_path(binding['path']);content=handoff.read_bytes()
    assert hashlib.sha256(content).hexdigest()==binding['sha256']
    side=json.loads(content);source=ROOT/side['source']
    assert hashlib.sha256(source.read_bytes()).hexdigest()==side['sha256']
    root,raw=read_structure(source)
    assert root['size']==side['size']==entry['size'] and len(raw)==side['blocks']
    assert side['ground_y']==entry['ground_y'] and side['buried_clip_depth']==entry['buried_clip_depth']
    contract={**ASSETS[entry['id']],**{k:side[k] for k in ('source','version','sha256','blocks')},'visually_accepted':False}
    blocks,size,foundation=supported_blocks(raw,contract)
    offset=[TOE_RADIUS,foundation['vertical_padding'],TOE_RADIUS]
    anchor=(size[0]//2,foundation['ground_y']-1,size[2]//2)
    final=blocks.get(anchor,'minecraft:structure_void');blocks[anchor]='minecraft:jigsaw[orientation=north_up]'
    nbt={k:(8,v) for k,v in {'id':'minecraft:jigsaw','name':'relics:center','target':'minecraft:empty',
        'pool':'minecraft:empty','joint':'rollable','final_state':final}.items()}
    nbt.update(selection_priority=(3,0),placement_priority=(3,0))
    natural=encode_structure(blocks,tuple(size),root['DataVersion'],{anchor:nbt})
    stem=entry['id']+'_side_v1';destination=resources/'data/relics/structure';destination.mkdir(parents=True,exist_ok=True)
    for filename,data in ((stem+'.nbt',source.read_bytes()),(stem+'_worldgen.nbt',natural)):
        target=destination/filename
        if verify:
            if not target.is_file() or target.read_bytes()!=data:raise ValueError('Stale visual template: '+str(target))
        else:target.write_bytes(data)
    entry.update(contract)
    entry['single_template']={'path':stem+'.nbt','sha256':side['sha256']}
    entry['worldgen_template']={'path':stem+'_worldgen.nbt','sha256':hashlib.sha256(natural).hexdigest(),
        'size':size,'anchor':list(anchor),'final_state':final,'foundation':foundation}
    # A frozen selection certificate with no gameplay actions or rewards.
    entry['gameplay']={'version':revision,'selection_handoff_sha256':binding['sha256'],
        'asset_version':side['version'],'offset':offset,'markers':[],'clearance_runs':[],'replaceable_blocks':[]}

def integrate(resources=ROOT/'src/main/resources',verify=False,revision=REVISION):
    if revision not in MANIFESTS:raise ValueError('Unknown interior revision: '+revision)
    index=json.loads({PREVIOUS_REVISION:PREVIOUS_INDEX,LANDMARK_REVISION:LANDMARK_INDEX,SMALL_LANDMARK_REVISION:SMALL_LANDMARK_INDEX,SHORT_ENTRY_REVISION:SHORT_ENTRY_INDEX,TREE_SKULL_REVISION:TREE_SKULL_INDEX,REVISION:INDEX}[revision].read_text(encoding='utf-8'))
    old=json.loads((resources/'relics.integration.json').read_text())
    manifest=copy.deepcopy(old)
    manifest.update(selection='alpha5-gameplay',revision=revision,air_policy='bounded native clearance; preserve authored solids')
    registry=json.loads((ROOT/'docs/project/reviews/gameplay-registry-26.2.json').read_text())['blocks']
    registry.update(json.loads((ROOT/'docs/project/reviews/gameplay-interiors-feedback-20261027-registry.json').read_text())['blocks'])
    if revision==REVISION:
        registry.update(json.loads((ROOT/'docs/project/reviews/tower-upper-chest-20261111-registry.json').read_text())['blocks'])
    for entry in manifest['structures']:
        name=entry['id']
        if name in index.get('visual_assets',{}):
            integrate_visual(entry,index['visual_assets'][name],resources,verify,revision);continue
        if name not in index['assets']:continue
        files=bound_files(index['assets'][name]);source=source_path(files['.nbt']['path'])
        for ext in ('.nbt','.gameplay.json'):
            assert hashlib.sha256(source_path(files[ext]['path']).read_bytes()).hexdigest()==files[ext]['sha256']
        root,raw=read_structure(source)
        side=json.loads(source_path(files['.gameplay.json']['path']).read_text())
        validate(side,raw,root['size'],registry)
        if name in ('colossus','small_colossus','ruined_tower'):
            expected_chests=2 if name=='ruined_tower' and side['asset_version']=='ruined-tower-v11-upper-chest' else 1
            assert sum(m['role'].endswith('_chest') for m in side['markers'])==expected_chests,'Unexpected per-site chest budget'
        contract={**ASSETS[name],'source':files['.nbt']['path'],'sha256':files['.nbt']['sha256'],
                  'version':side['asset_version'],'blocks':len(raw),
                  'visually_accepted':name not in ('small_colossus','ruined_tower') if revision in (SHORT_ENTRY_REVISION,TREE_SKULL_REVISION,REVISION) else
                    not ((revision!=PREVIOUS_REVISION and name=='colossus') or (revision==SMALL_LANDMARK_REVISION and name=='small_colossus'))}
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
        suffix=('_v11' if revision==REVISION and name=='ruined_tower' else
                '_v7' if revision!=PREVIOUS_REVISION and name=='colossus' else
                '_v11' if revision in (SHORT_ENTRY_REVISION,TREE_SKULL_REVISION,REVISION) and name=='small_colossus' else
                '_v10' if (revision==SMALL_LANDMARK_REVISION and name=='small_colossus') or (revision in (SHORT_ENTRY_REVISION,TREE_SKULL_REVISION,REVISION) and name=='ruined_tower') else '')
        stem=f'{name}_gameplay'+suffix
        raw_name=f'{stem}.nbt';natural_name=f'{stem}_worldgen.nbt'
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
        entry['gameplay']={'version':revision,'sidecar_sha256':files['.gameplay.json']['sha256'],
            'asset_version':side['asset_version'],'offset':offset,'markers':side['markers'],
            'clearance_runs':runs,'replaceable_blocks':V4_NATIVE if revision in (SHORT_ENTRY_REVISION,TREE_SKULL_REVISION,REVISION) and name in ('small_colossus','ruined_tower') else LANDMARK_NATIVE if (revision!=PREVIOUS_REVISION and name=='colossus') or (revision==SMALL_LANDMARK_REVISION and name=='small_colossus') else RUNTIME_NATIVE}
    target=resources/MANIFESTS[revision]
    if verify:
        if not target.is_file() or json.loads(target.read_text())!=manifest:raise ValueError('Stale approved gameplay manifest')
    else:target.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    return manifest

if __name__=='__main__':
    for revision in MANIFESTS:integrate(revision=revision)
