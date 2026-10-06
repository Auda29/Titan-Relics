"""Build the Alpha 4.5 follow-up with low cores and explicit deeper burial contracts."""
import argparse
import hashlib
import json
from pathlib import Path

from colossus_materials import encode_schematic
from embedding_relief import sculpt
from inspect_ots_result import read_structure
from relic_catalog import ASSETS
from schem_to_nbt import convert,read_schematic
from terrain_foundations import supported_blocks,TOE_RADIUS,padding

ROOT=Path(__file__).resolve().parents[1]
# Fixed Alpha 4.5 sources plus the new Tower V7; integration must not move inputs.
BASELINES={
 'titan_skull':('titan-skull','titan-skull-v4-meadow-ground-v2',8,16,4,'fcfef99961773832f54b24ff585d5e96a64bf9e3ed2ac7b0888158e8804c7f6b'),
 'titan_skull_dry':('titan-skull','titan-skull-v4-dry-ground-v2',8,16,4,'3cd8249a3401c39f162bf62217d68ad00fcd385a507aeb9d794e54e3351fdc20'),
 'titan_skull_sand':('titan-skull','titan-skull-v4-sand-ground-v2',8,16,4,'358bd8f318ef5ad0ea1c6b27292fb5b30f94ebb0afa937bf778f16d9ff47a829'),
 'titan_skull_rock':('titan-skull','titan-skull-v4-rock-ground-v2',8,16,6,'fd6ce1c124b0d5ac51777644e0b7214f053a32bf8460b1e30b9e3fe1f0aaeacf'),
 'small_colossus':('colossus','small-colossus-v7-ground-v2',9,13,4,'5a1afb7dc0b8cb30bba6428cc612aa26dcfe6f63d4cfca7a5aaca41edb5a5843'),
 'world_tree':('world-tree','world-tree-v4-1-ground-v2',8,8,6,'5ba0b4f73f0e1fd5087f2ecdb28849a78f3297caffbbb2d6b5b58b98ce2ebaf6'),
 'ruined_tower':('ruined-tower','ruined-tower-v7',12,12,6,'60a3ad133353a61cb1a71641074e646f460d5be8f8ddc5c5e967427212b29ef3'),
}


def baseline(name):
    folder,stem,ground,new_ground,slope,digest=BASELINES[name]
    source=ROOT/f'relics/{folder}/design/generated/{stem}/{stem}.nbt'
    return source,ground,new_ground,slope,digest


def build(name):
    source,old_ground,ground,slope,digest=baseline(name)
    assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
    config=json.loads((source.parents[2]/(source.stem+'.json')).read_text())
    root,blocks=read_structure(source)
    result,art,report=sculpt(blocks,ground,config['materials'],moss_pads=name=='world_tree')
    old_contract={'ground_y':old_ground,'slope':10 if name=='ruined_tower' else 12,'size':root['size']}
    contract={'ground_y':ground,'slope':slope,'size':root['size']}
    old_natural,_,_=supported_blocks(blocks,old_contract)
    # Only low art contacts are retained. High soil buttressing inside the cranium
    # is deliberately removed, while the near-ground anatomy still has support.
    old_pad=padding(old_contract);pad=padding(contract);checked=0;restored=0
    for attempt in range(3):
        natural,_,foundation=supported_blocks(result,contract);missing=[]
        for x,y,z in art:
            if y>ground+2:continue
            # A raw Y0 underside is outside the authored grid. It is deeply
            # buried at the new ground line and belongs to the runtime substrate
            # check, not a fabricated out-of-bounds authored soil cell.
            if y==0:continue
            if (x+TOE_RADIUS,y-1+old_pad,z+TOE_RADIUS) not in old_natural:continue
            if (x+TOE_RADIUS,y-1+pad,z+TOE_RADIUS) not in natural:missing.append((x,y-1,z))
        if not missing:break
        for p in missing:
            assert p not in art
            # Buried tips formerly resting on a derived toe get a local earth toe.
            # This is limited to ground+1, never a new high pedestal.
            x,y,z=p
            for yy in range(max(0,y-3),y+1):
                if (x,yy,z) not in result:result[x,yy,z]=config['materials']['terrain_fill'];restored+=1
    else:raise ValueError(f'Unresolved low art supports: {missing[:10]}')
    checked=sum(0<y<=ground+2
                and (x+TOE_RADIUS,y-1+old_pad,z+TOE_RADIUS) in old_natural for x,y,z in art)
    below_bounds=sum(y==0 for x,y,z in art)
    assert all(result.get(p)==s for p,s in art.items())
    assert max((p[1]-ground for p in result if p not in art),default=0)<=1
    stem=source.stem.replace('-ground-v2','')+'-ground-v3';out=source.parent.parent/stem;out.mkdir(parents=True,exist_ok=True)
    path=out/(stem+'.schem');path.write_bytes(encode_schematic(result,root['size'],root['DataVersion'],[0,0,0]))
    convert(path,path.with_suffix('.nbt'),'omit',32)
    _,written=read_structure(path.with_suffix('.nbt'));assert written==result==read_schematic(path.read_bytes())[1]
    manifest=json.loads(path.with_suffix('.manifest.json').read_text());recovered={}
    for tile in manifest['tiles']:
        _,cells=read_structure(out/tile['path'])
        for p,s in cells.items():
            q=tuple(v+o for v,o in zip(p,tile['origin']));assert q not in recovered;recovered[q]=s
    assert recovered==result
    checksum=hashlib.sha256(path.with_suffix('.nbt').read_bytes()).hexdigest()
    contract.update(source=path.with_suffix('.nbt').relative_to(ROOT).as_posix(),version=stem,blocks=len(result),sha256=checksum,
                    family=ASSETS[name]['family'],biomes=ASSETS[name]['biomes'],visually_accepted=False)
    report.update(source=source.relative_to(ROOT).as_posix(),source_sha256=digest,
        nbt_sha256=checksum,schematic_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        size=root['size'],blocks=len(result),tiles=len(manifest['tiles']),data_version=root['DataVersion'],
        original_ground_y=old_ground,ground_y=ground,additional_burial=ground-old_ground,
        placement_contract=contract,foundation=foundation,low_art_undersides_checked=checked,
        restored_low_toe_cells=restored,buried_boundary_undersides_requiring_runtime_check=below_bounds,
        non_terrain_scope='All art except explicitly declared low Tree moss pads',
        checks=['immutable art exact identity','ground cap <= nominal+1','low art support preservation',
                'schematic/NBT equality','lossless tile reconstruction','bounds','source hash'],in_game_tested=False)
    if name=='world_tree':
        accepted=source.parent.parent/'world-tree-v4/world-tree-v4.nbt';_,old=read_structure(accepted)
        woody_leaves=lambda s:'log' in s or 'leaves' in s
        assert {p:s for p,s in old.items() if woody_leaves(s)}=={p:s for p,s in result.items() if woody_leaves(s)}
        report['accepted_wood_and_foliage_identical']=True
        report['accepted_tree_sha256']=hashlib.sha256(accepted.read_bytes()).hexdigest()
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    config.update(output=path.relative_to(ROOT).as_posix(),source_nbt=source.relative_to(ROOT).as_posix(),
                  authoring='block-embedding-derivative',ground_y=ground,title=stem.upper(),
                  subtitle='Low central deposits / deeper embedding / flatter placement sites')
    config.pop('input',None)
    (source.parents[2]/(stem+'.json')).write_text(json.dumps(config,indent=2)+'\n')
    meta=json.loads(source.with_suffix('.design.json').read_text());meta.pop('source_blend_sha256',None)
    meta.update(name=stem,ground_level_nbt_approx=ground,embedding_derivative=report,
                visual_acceptance='Alpha 4.5 embedding follow-up; review pending',in_game_tested=False)
    path.with_suffix('.design.json').write_text(json.dumps(meta,indent=2)+'\n')
    target=ROOT/'build/embedding-relief';target.mkdir(parents=True,exist_ok=True)
    comparison=report['source']
    if name=='ruined_tower':
        comparison=(source.parent.parent/'ruined-tower-v6-ground-v2/ruined-tower-v6-ground-v2.nbt').relative_to(ROOT).as_posix()
        assert hashlib.sha256((ROOT/comparison).read_bytes()).hexdigest()=='88a7f0d218b1f5343cbbf3ebef1bd46e70df060d866cf36d3473107a03dbe4bd'
    (target/(name+'.json')).write_text(json.dumps({'id':name,'baseline':comparison,'baseline_ground_y':old_ground,
       'candidate':stem,'source':contract['source'],'ground_y':ground,'verification':report},indent=2)+'\n')
    assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
    print(json.dumps({k:report[k] for k in ('source','blocks','ground_y','removed_cells','changed_surface_states','low_art_undersides_checked','restored_low_toe_cells')},indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--assets',nargs='+',choices=BASELINES,default=list(BASELINES))
    for name in parser.parse_args().assets:build(name)
