"""Export ground-only NBT/schematic candidates from pinned, already voxelized art."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from colossus_materials import encode_schematic
from deposit_relief import erode
from inspect_ots_result import read_structure
from relic_catalog import ASSETS
from schem_to_nbt import convert,read_schematic
from terrain_foundations import supported_blocks,TOE_RADIUS

ROOT=Path(__file__).resolve().parents[1]
NAMES=['titan_skull','titan_skull_dry','titan_skull_sand','titan_skull_rock',
       'small_colossus','world_tree','ruined_tower','titan_skull_2']

# Immutable Alpha 4.4 inputs: selecting the derivatives in the mod must not
# turn reproduction into a second erosion pass or replace the before/after art.
BASELINE_EXPORTS = {
    'titan_skull': ('titan-skull-v4-meadow', 136569, 'c4737780cc344b2a3f10743a7155a760df7342f22476308679a9a87545f59e79'),
    'titan_skull_dry': ('titan-skull-v4-dry', 136569, '7c2ea0fde39ba7c9618001dd49e747d2c652e0646c854baf0fadcb6e5ed773a4'),
    'titan_skull_sand': ('titan-skull-v4-sand', 136569, '05ba0c95f74e98eca366c11f4ebe1ceb1b3ce435b82c29d7101f65fd7da7d03e'),
    'titan_skull_rock': ('titan-skull-v4-rock', 136569, '9c41e8bdc5333737ed7c37e6ab8f916aac0f77f32764d20cca4e2fb68e94620b'),
    'small_colossus': ('small-colossus-v7', 235933, 'c48bb70ea3643070e94a44008721cb5c08fda74f80b4efee2e063a44b5436bb4'),
    'world_tree': ('world-tree-v4-1', 293691, 'b8235fd957029d39a534eef2f13924bc850155e46fd5872fc40f51ecce8eea37'),
    'ruined_tower': ('ruined-tower-v5', 307417, '5be62afb4d6a3968e37c61b54e21941273c795921441dc9db8e705ced9f2765f'),
    'titan_skull_2': ('titan-skull-2-v1', 85224, '5a39ac6ef62c1d07eafed69ed8a7cbeb397b4a6d3c4a6f7bf7086fdabdac1b78'),
}


def baseline_contract(name, tower_v6=False):
    contract = dict(ASSETS[name])
    stem, count, checksum = BASELINE_EXPORTS[name]
    if tower_v6 and name == 'ruined_tower':
        stem, count, checksum = ('ruined-tower-v6', 298355,
                                '761d9a257a3339334e2e4f5bc89772330dde75e040fbf9e5e1107ba36a25b779')
    source = (ROOT / contract['source']).parent.parent / stem / f'{stem}.nbt'
    contract.update(version=stem, source=source.relative_to(ROOT).as_posix(),
                    sha256=checksum, blocks=count)
    return contract


def build(name,tower_v6=False):
    contract=baseline_contract(name,tower_v6);source=ROOT/contract['source']
    assert not source.stem.endswith('ground-v2'),'Select the preserved pre-relief baseline, not another relief candidate'
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest==contract['sha256'],'Input checksum differs from its selection/verification'
    config_path=source.parents[2]/f'{source.stem}.json';config=json.loads(config_path.read_text())
    root,blocks=read_structure(source)
    old_natural,_,foundation=supported_blocks(blocks,contract)
    pad=foundation['vertical_padding'];horizontal=foundation['horizontal_padding']
    extra_contacts=set()
    for attempt in range(4):
        result,report=erode(blocks,contract['ground_y'],config['materials'],extra_contacts)
        soil=set(report['terrain_states'])
        natural,_,foundation=supported_blocks(result,contract)
        failures=[];contact_checks=0
        for (x,y,z),s in blocks.items():
            if s in soil:continue
            q=(x+horizontal,y-1+pad,z+horizontal)
            if q in old_natural:
                contact_checks+=1
                if q not in natural:failures.append((x,z))
        if not failures:break
        # A few low root tips sit on the *derived* toe, outside authored earth.
        # Restore the nearby source soil columns which supplied that support,
        # then rerun erosion with those contacts locked.
        for x,z in failures:
            extra_contacts.update((x+dx,z+dz) for dx in range(-TOE_RADIUS,TOE_RADIUS+1)
                                  for dz in range(-TOE_RADIUS,TOE_RADIUS+1))
    else:raise ValueError(f'Cannot preserve {len(failures)} derived art supports')
    report['derived_support_lock_columns']=len(extra_contacts)
    assert all(natural[x+horizontal,y+pad,z+horizontal]==s for (x,y,z),s in result.items())
    stem=source.stem+'-ground-v2';out=source.parent.parent/stem;out.mkdir(parents=True,exist_ok=True)
    schem=out/f'{stem}.schem';schem.write_bytes(encode_schematic(result,root['size'],root['DataVersion'],[0,0,0]))
    convert(schem,schem.with_suffix('.nbt'),'omit',32)
    _,written=read_structure(schem.with_suffix('.nbt'))
    assert written==result==read_schematic(schem.read_bytes())[1]
    manifest=json.loads(schem.with_suffix('.manifest.json').read_text());recovered={}
    for tile in manifest['tiles']:
        _,cells=read_structure(out/tile['path'])
        for p,s in cells.items():
            q=tuple(v+o for v,o in zip(p,tile['origin']));assert q not in recovered;recovered[q]=s
    assert recovered==result
    checksum=hashlib.sha256(schem.with_suffix('.nbt').read_bytes()).hexdigest()
    report.update(size=root['size'],blocks=len(result),tiles=len(manifest['tiles']),data_version=root['DataVersion'],
        source=source.relative_to(ROOT).as_posix(),source_sha256=digest,nbt_sha256=checksum,
        schematic_sha256=hashlib.sha256(schem.read_bytes()).hexdigest(),
        supported_art_cells_checked=contact_checks,foundation=foundation,
        checks=['non-terrain block identity','contact-column identity','no new air under supported art',
                'schematic/NBT equality','lossless tile reconstruction','unchanged declared dimensions'],
        in_game_tested=False,authoring='Explicit block-space terrain derivative; original Blender art preserved')
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    meta=json.loads(source.with_suffix('.design.json').read_text())
    meta.pop('source_blend_sha256',None)
    meta.update(name=stem,visual_acceptance='Alpha 4.4 soil-relief follow-up; review pending',in_game_tested=False,
                terrain_derivative=report)
    schem.with_suffix('.design.json').write_text(json.dumps(meta,indent=2)+'\n')
    config.update(output=schem.relative_to(ROOT).as_posix(),title=stem.upper(),
                  authoring='block-terrain-derivative',
                  subtitle='Eroded soil margins / contact-preserving ground derivative',
                  source_nbt=source.relative_to(ROOT).as_posix())
    config.pop('input',None)
    (source.parents[2]/f'{stem}.json').write_text(json.dumps(config,indent=2)+'\n')
    assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
    print(json.dumps({'asset':name,'candidate':stem,**{k:report[k] for k in ('blocks','modified_columns','removed_soil_cells','protected_contact_columns','supported_art_cells_checked')}},indent=2),flush=True)
    return {'id':name,'candidate':stem,'source':schem.with_suffix('.nbt').relative_to(ROOT).as_posix(),
            'baseline':source.relative_to(ROOT).as_posix(),'ground_y':contract['ground_y'],'verification':report}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets',nargs='+',choices=NAMES,default=NAMES)
    parser.add_argument('--tower-v6',action='store_true');args=parser.parse_args()
    target=ROOT/'build/deposit-relief';target.mkdir(parents=True,exist_ok=True)
    for name in args.assets:
        record=build(name,args.tower_v6)
        (target/(record['id']+'.json')).write_text(json.dumps(record,indent=2)+'\n')
