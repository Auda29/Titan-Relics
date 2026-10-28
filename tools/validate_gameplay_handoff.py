"""Independent builder-side validation; does not claim runtime or natural-site tests."""
import argparse
from collections import Counter,deque
import hashlib
import json
from pathlib import Path
import re

from inspect_ots_result import read_structure
from schem_to_nbt import read_schematic
from relic_catalog import ROOT,ASSETS

REQUIRED={
 'colossus':{'colossus_trial_spawner':1,'colossus_golem_spawn':1,'colossus_vault':1,'colossus_hatch':1,'colossus_arm_magnet_chest':1},
 'small_colossus':{'small_magnet_chest':1},
 'obelisk':{'archaeology_common':6,'archaeology_trim':1,'archaeology_map':1},
 'ruined_tower':{'tower_enderman_spawn':5,'tower_ender_chest':1,'tower_entry':1,'tower_upper_destination':1},
 'world_tree':{'tree_aura_anchor':1,'tree_amethyst_center':1}}
REGIONS={'colossus':{'cockpit_clearance','hatch_clearance','arm_clearance'},'small_colossus':{'small_interior_clearance'},
         'obelisk':set(),'ruined_tower':{'tower_route_clearance'},'world_tree':{'tree_lighting_scope'}}
INJECT={'colossus_trial_spawner','colossus_vault','colossus_arm_magnet_chest','colossus_salvage_chest',
        'small_magnet_chest','archaeology_common','archaeology_trim','archaeology_map','tower_ender_chest'}

def require(value,message):
    if not value:raise ValueError(message)

def positions(lo,hi):
    import itertools
    return itertools.product(*(range(a,b+1) for a,b in zip(lo,hi)))

def valid_state(s,registry):
    name,_,tail=s.partition('[');name=name.removeprefix('minecraft:')
    require(name in registry,'Unknown 26.2 block '+name)
    if tail:
        require(tail.endswith(']'),'Invalid state '+s)
        pairs=[p.split('=') for p in tail[:-1].split(',')]
        require(len({p[0] for p in pairs})==len(pairs),'Duplicate properties')
        for key,value in pairs:require(value in registry[name][0].get(key,[]),'Invalid 26.2 state '+s)

def validate(sidecar,blocks,size,registry):
    require(sidecar['schema_version']==1,'Unknown schema')
    name=sidecar['structure_id'].removeprefix('relics:')
    require(name in REQUIRED and sidecar['structure_id']=='relics:'+name,'Unknown structure')
    require(sidecar['coordinate_space']=='raw_template' and sidecar['source_facing']=='north','Invalid coordinate space')
    require(sidecar['size']==list(size),'Size mismatch')
    require(sidecar['ground_y']==ASSETS[name]['ground_y'],'Ground mismatch')
    source=sidecar['source_nbt'];path=Path(source)
    require(not path.is_absolute() and '..' not in path.parts and ':' not in source and '\\' not in source,'Unsafe source path')
    expected_parent=Path(ASSETS[name]['source']).parents[1]
    require(path.parent.parent==expected_parent and path.stem==sidecar['asset_version'],'Wrong asset binding')
    require(re.fullmatch('[a-f0-9]{64}',sidecar['source_sha256']) is not None,'Invalid hash')
    require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sidecar['source_sha256'],'Hash mismatch')
    ids=set();injected=set();roles=Counter()
    def point(p):return len(p)==3 and all(type(v)==int and 0<=v<n for v,n in zip(p,size))
    for marker in sidecar['markers']:
        require(marker['id'] not in ids and re.fullmatch('[a-z0-9_-]+',marker['id']),'Duplicate/invalid id');ids.add(marker['id'])
        role=marker['role'];require(role in REQUIRED[name] or (name in ('colossus','small_colossus') and role=='colossus_salvage_chest'),'Unknown role')
        roles[role]+=1;p=tuple(marker['pos']);require(point(p),'Marker outside bounds')
        require(marker.get('facing','north') in ('north','east','south','west'),'Invalid facing')
        if role in INJECT:
            require(p not in injected,'Duplicate injection');injected.add(p)
            require(marker.get('expected_block')==blocks.get(p),'Placeholder mismatch')
            valid_state(marker['expected_block'],registry)
            require((p[0],p[1]-1,p[2]) in blocks,'Unsupported placeholder')
            require((p[0],p[1]+1,p[2]) not in blocks,'Blocked chest/brush top')
        if role.endswith('_spawn'):
            require(all(q not in blocks for q in positions((p[0]-1,p[1],p[2]-1),(p[0]+1,p[1]+3,p[2]+1))),'Blocked entity clearance')
            require(all((x,p[1]-1,z) in blocks for x in range(p[0]-1,p[0]+2) for z in range(p[2]-1,p[2]+2)),'Unsafe entity floor')
    require(all(roles[role]==count for role,count in REQUIRED[name].items()),'Role cardinality mismatch')
    region_roles=Counter()
    for region in sidecar['regions']:
        require(region['id'] not in ids,'Duplicate id');ids.add(region['id'])
        role=region['role'];region_roles[role]+=1
        require(role in REGIONS[name],'Unknown region role')
        lo,hi=region['min'],region['max']
        require(point(lo) and point(hi) and all(a<=b for a,b in zip(lo,hi)),'Region bounds')
        if role.endswith('_clearance'):
            allowed=region.get('replaceable_blocks',[])
            require(allowed and not any(s in allowed for s in ('minecraft:water','minecraft:lava','*','minecraft:air')),'Unsafe clearing policy')
            for s in allowed:valid_state(s,registry)
    if name=='colossus':require(region_roles['cockpit_clearance'] and region_roles['hatch_clearance'],'Missing required clearance')
    if name=='world_tree':require(region_roles['tree_lighting_scope'],'Missing lighting scope')
    for state in set(blocks.values()):valid_state(state,registry)
    return name

def reachable(blocks,start,target,max_y=None):
    """One-block-wide/two-block-high player envelope, <=1 block steps, no mining.

    Conservative full-cube stair treatment; not a physics/pathfinder simulation.
    """
    def clear(p):
        x,y,z=p
        return (max_y is None or y<=max_y) and p not in blocks and (x,y+1,z) not in blocks and (x,y-1,z) in blocks
    start=tuple(start);target=tuple(target)
    require(clear(start),'Blocked route start '+str(start))
    queue=deque([start]);seen={start}
    while queue:
        x,y,z=queue.popleft()
        if abs(x-target[0])+abs(y-target[1])+abs(z-target[2])<=1:return True
        for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
            for dy in (0,1,-1):
                p=x+dx,y+dy,z+dz
                if p not in seen and clear(p):seen.add(p);queue.append(p)
    return False

def inspect(path,registry):
    sidecar=json.loads(path.read_text());nbt=ROOT/sidecar['source_nbt']
    root,blocks=read_structure(nbt)
    require(not root.get('entities') and not any('nbt' in b for b in root['blocks']),'Source entities/block NBT')
    name=validate(sidecar,blocks,root['size'],registry)
    require(read_schematic(nbt.with_suffix('.schem').read_bytes())[1]==blocks,'Schematic mismatch')
    manifest=json.loads(nbt.with_suffix('.manifest.json').read_text());assembled={}
    for tile in manifest['tiles']:
        _,part=read_structure(nbt.parent/tile['path'])
        for p,s in part.items():
            q=tuple(a+c for a,c in zip(p,tile['origin']));require(q not in assembled,'Overlapping tiles');assembled[q]=s
    require(assembled==blocks,'Tile mismatch')
    a=ASSETS[name];base=ROOT/a['source'];require(hashlib.sha256(base.read_bytes()).hexdigest()==a['sha256'],'Baseline mutated')
    _,old=read_structure(base);design=json.loads(nbt.with_suffix('.design.json').read_text())
    checks=['source hash and revision binding','26.2 block/property report','roles/bounds/placeholder supports',
            'entity footprints/headroom','schematic equality','lossless tile reconstruction','unchanged baseline hash']
    if name in ('colossus','small_colossus','ruined_tower'):
        unseen=blocks.keys()-old.keys()
        while unseen:
            seed=unseen.pop();queue=[seed];anchored=False
            while queue:
                x,y,z=queue.pop()
                for q in ((x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)):
                    if q in old and q in blocks:anchored=True
                    if q in unseen:unseen.remove(q);queue.append(q)
            require(anchored,'New floating architectural component at '+str(seed))
        checks.append('new architecture face-connected to surviving baseline')
    for route in design['paths']:
        for x,y,z in route['feet']:
            require(all((x,y+dy,z) not in blocks for dy in range(route['height'])),'Blocked path '+route['name']+str((x,y,z)))
            require((x,y-1,z) in blocks,'Path without floor '+str((x,y,z)))
        require(reachable(blocks,route['feet'][0],route['feet'][-1]),'Disconnected route '+route['name'])
    if design['paths']:checks.append('two-block player routes / continuous support')
    if name=='colossus':
        require(all(blocks.get(p)==s for p,s in old.items() if (p[2]>135 and p[1]<135) or p[2]<60),'Body cavity or hand changed')
        require(sum('copper' in s for s in blocks.values())<50000,'Copper budget')
        require(9*sum('raw_iron_block' in s for s in blocks.values())<256,'Raw iron budget')
        checks.append('body cavity / original hand / resource limits preserved')
    if name=='obelisk':
        require(all(blocks.get(p)==s for p,s in old.items() if 'terracotta' in s or p[1]>=16),'Monument altered')
        checks.append('solid monument and damage preserved')
    if name=='world_tree':
        require(all(blocks.get(p)==s for p,s in old.items() if p[1]>39),'Upper tree changed')
        require(not any('budding_amethyst' in s for s in blocks.values()),'Renewable amethyst')
        for p,s in blocks.items():
            x,y,z=p
            if any(k in s for k in ('shroomlight','glow_lichen','cave_vines','firefly_bush')):
                require(y<=sidecar['ground_y']+15,'Light above root/base height limit')
                require(any(all(a<=v<=c for v,a,c in zip(p,r['min'],r['max'])) for r in sidecar['regions'] if r['role']=='tree_lighting_scope'),'Light outside declared scope')
            if s.startswith('minecraft:firefly_bush'):require(blocks.get((x,y-1,z))=='minecraft:rooted_dirt','Bush substrate')
            if 'cave_vines' in s:require((x,y+1,z) in blocks,'Unsupported berries')
            if 'glow_lichen' in s:
                offsets={'west':(-1,0,0),'east':(1,0,0),'north':(0,0,-1),'south':(0,0,1)}
                require(any(f'{face}=true' in s and tuple(a+d for a,d in zip(p,delta)) in blocks for face,delta in offsets.items()),'Unsupported lichen')
        checks.append('upper tree exact / nonrenewable sphere / attached lighting')
    report={'size':root['size'],'blocks':len(blocks),'tiles':len(manifest['tiles']),
            'markers':len(sidecar['markers']),'regions':len(sidecar['regions']),
            'checks':checks,'nbt_sha256':sidecar['source_sha256'],
            'in_game_tested':False,'natural_rotation_and_chunk_injection_tested':False,
            'actual_block_light_tested':False,'visual_acceptance':'pending'}
    target=nbt.parent/'verification.json'
    # Published reports are hash-bound. Rechecking on Windows must preserve the
    # existing line endings rather than silently replacing LF with CRLF.
    newline='\r\n' if target.is_file() and b'\r\n' in target.read_bytes() else '\n'
    target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline=newline)
    print(name,': PASS',len(checks),'checks');return report

def main():
    parser=argparse.ArgumentParser();parser.add_argument('asset',nargs='?',default='all');args=parser.parse_args()
    from build_gameplay_interiors import STEMS
    registry=json.loads((ROOT/'docs/project/reviews/gameplay-registry-26.2.json').read_text())['blocks']
    for name,stem in STEMS.items():
        if args.asset not in ('all',name):continue
        path=(ROOT/ASSETS[name]['source']).parent.parent/stem/(stem+'.gameplay.json')
        inspect(path,registry)

if __name__=='__main__':main()
