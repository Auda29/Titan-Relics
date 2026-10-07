"""Independent saved-mask audit of bounded supports and former cave-wall regions."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import zipfile

from inspect_ots_result import read_structure
from rooted_embedding import remove_terrain
from terrain_foundations import supported_blocks
from verify_world import AIR_NAMES, AnvilWorld, protected_cell, transform

ROOT=Path(__file__).resolve().parents[1]
NAMES=('titan_skull_2','world_tree')
REGIONS={
    'skull_deep_cave': ('titan_skull_2',[-13146,38,36278,-13131,61,36302]),
    'tree_north_cave': ('world_tree',[23735,40,-45567,23761,62,-45532]),
    'tree_west_cave': ('world_tree',[23660,40,-45480,23692,62,-45460]),
}


def masks(world,bb):
    found={}
    for cx in range(bb[0]//16,bb[3]//16+1):
        for cz in range(bb[2]//16,bb[5]//16+1):
            chunk=world.chunk(cx,cz)
            if chunk is None: raise ValueError('Missing chunk in mask audit')
            for cy,words in chunk.get('fabric:attachments',{}).get('relics:placed_cells',{}).items():
                assert len(words)==64
                for wi,word in enumerate(words):
                    bits=word & ((1<<64)-1)
                    while bits:
                        bit=(bits & -bits).bit_length()-1;idx=wi*64+bit
                        p=(cx*16+idx%16,int(cy)*16+idx//256,cz*16+idx%256//16)
                        if all(bb[k]<=p[k]<=bb[k+3] for k in range(3)):
                            found[p]=world.block(*p)
                        bits &= bits-1
    return found


def support_checks(report,world):
    """Audit actual runtime-mask additions independently of model/gap comparison."""
    checks=[]
    for name in NAMES:
        a=next(a for a in report['asset_selection']['structures'] if a['id']==name)
        instance=next(i for i in report['world_blocks']['instances'] if i['structure']=='relics:'+name)
        source=ROOT/a['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==a['sha256']
        _,raw=read_structure(source);natural,_,policy=supported_blocks(raw,a)
        authored={transform(p,instance['rotation'],instance['origin']) for p in natural}
        bb=instance['bounding_box'].copy();bb[1]=-64
        placed=masks(world,bb);extra={p:s for p,s in placed.items() if p not in authored}
        columns={}
        for x,y,z in extra:columns.setdefault((x,z),[]).append(y)
        failures=[];lengths=[]
        ground=instance['origin'][1]+policy['ground_y']
        for (x,z),ys in columns.items():
            runs=[]
            for y in sorted(ys):
                if not runs or y!=runs[-1][-1]+1:runs.append([])
                runs[-1].append(y)
            for run in runs:
                top=(x,max(run)+1,z);bottom=(x,min(run)-1,z);lengths.append(len(run))
                substrate=world.block(*bottom);start=world.block(*top)
                error=[]
                if top not in authored:error.append('not attached to authored underside')
                if len(run)>a['max_support_depth']:error.append('too deep')
                if not ground-a['surface_contact_depth']<=top[1]<=ground:error.append('outside surface band')
                if substrate is None or substrate['Name'] in AIR_NAMES|{'minecraft:water','minecraft:lava'} or substrate['Name'].endswith('_leaves'):
                    error.append('unsupported short extension')
                if any(extra[x,y,z]!=start for y in run):error.append('material/state differs from attachment')
                if error:failures.append({'top':top,'bottom':bottom,'errors':error})
        checks.append({'id':name,'authored_natural_cells':len(authored),'omitted_deep_raw_cells':len(raw)-len(authored),
                       'runtime_cells':len(extra),'runtime_materials':dict(Counter(s['Name'] for s in extra.values())),
                       'max_runtime_column_length':max(lengths,default=0),'invalid_runs':failures,
                       'ground_y_world':ground,'passed':not failures})
    return checks


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before',type=Path,required=True);parser.add_argument('--after',type=Path,required=True)
    parser.add_argument('--preview-report',type=Path,help='Audit the installed terrain copy after verified reload')
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    paths=(args.before,args.after);reports=[json.loads(p.read_bytes()) for p in paths]
    assert all(r['passed'] and not r['showcase'] for r in reports)
    if reports[0]['seed'] != reports[1]['seed']:
        raise ValueError('Same-seed cave comparison is required')
    worlds=[AnvilWorld(Path(r['run_directory'])/'world') for r in reports]
    preview_evidence={}
    if args.preview_report:
        preview_data=args.preview_report.read_bytes();preview=json.loads(preview_data)
        if (not preview.get('strict_natural_verification_passed') or not preview['verification'].get('passed')
                or preview['source_report_sha256'] != hashlib.sha256(args.after.read_bytes()).hexdigest()):
            raise ValueError('A passing terrain reload from this exact natural run is required')
        reports[1]=dict(reports[1],world_blocks=preview['verification'])
        worlds[1]=AnvilWorld(Path(preview['world_path']))
        preview_evidence={'source_preview_report':args.preview_report.as_posix(),
                          'source_preview_report_sha256':hashlib.sha256(preview_data).hexdigest(),
                          'world_title':preview['world_title']}
    checks=support_checks(reports[1],worlds[1])
    # The accepted source roots must survive. Measure removal of the later
    # extrusion/support wall separately from those immutable anatomical cells.
    accepted_path=ROOT/'relics/world-tree/design/generated/world-tree-v4-1-ground-v3/world-tree-v4-1-ground-v3.nbt'
    assert hashlib.sha256(accepted_path.read_bytes()).hexdigest()=='fee50813242408123f4adcd1a0bacb476799359fce8e80ba5d59a49085823163'
    _,accepted_raw=read_structure(accepted_path)
    config=json.loads((accepted_path.parents[2]/(accepted_path.stem+'.json')).read_bytes())
    accepted_raw,_=remove_terrain(accepted_raw,config['materials'],tree=True,old_ground=8)
    tree_instances=[next(i for i in r['world_blocks']['instances'] if i['structure']=='relics:world_tree') for r in reports]
    assert tree_instances[0]['origin']==tree_instances[1]['origin'] and tree_instances[0]['rotation']==tree_instances[1]['rotation']
    ti=tree_instances[0]
    accepted={transform((x+8,y+12,z+8),ti['rotation'],ti['origin']) for x,y,z in accepted_raw}
    regions=[]
    for label,(name,bb) in REGIONS.items():
        entries=[masks(w,bb) for w in worlds]
        restored=Counter()
        for p in entries[0].keys()-entries[1].keys():restored[worlds[1].block(*p)['Name']]+=1
        retained={p for p in accepted if all(bb[k]<=p[k]<=bb[k+3] for k in range(3))} if name=='world_tree' else set()
        missing=sorted(retained-entries[1].keys())
        extra_counts=[len(e.keys()-retained) for e in entries]
        regions.append({'id':label,'bounds':bb,'before_protected_cells':len(entries[0]),
                        'after_protected_cells':len(entries[1]),'released_positions_now':dict(restored),
                        'remaining_fraction':len(entries[1])/max(1,len(entries[0])),
                        'accepted_art_cells_in_region':len(retained),'missing_accepted_art':missing,
                        'added_geometry_before':extra_counts[0],'added_geometry_after':extra_counts[1],
                        'added_geometry_remaining_fraction':extra_counts[1]/max(1,extra_counts[0])})
    archives=[zipfile.ZipFile(r['world_blocks']['artifact']) for r in reports]
    unchanged=[]
    for a in reports[0]['asset_selection']['structures']:
        if a['id'] in NAMES:continue
        for suffix in ('','_worldgen'):
            path=f'data/relics/structure/{a["id"]}{suffix}.nbt'
            assert archives[0].read(path)==archives[1].read(path),path
        unchanged.append(a['id'])
    for a in archives:a.close()
    face_cavities=[]
    for r,w in zip(reports,worlds):
        a=next(a for a in r['asset_selection']['structures'] if a['id']=='titan_skull_2')
        instance=next(i for i in r['world_blocks']['instances'] if i['structure']=='relics:titan_skull_2')
        probes=json.loads((ROOT/a['source']).with_name('verification.json').read_bytes())['void_probes_local']
        blocked=[]
        for x,y,z in probes:
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    for dz in (-1,0,1):
                        p=transform((x+8+dx,y+dy,z+8+dz),instance['rotation'],instance['origin'])
                        state=w.block(*p)
                        if state is None:raise ValueError('Missing face-cavity cell')
                        if state['Name'] not in AIR_NAMES:blocked.append({'position':p,'state':state})
        face_cavities.append({'checked_cells':len(probes)*27,'blocked':blocked,'strict_air_only':not blocked})
    cavity_contents_preserved=face_cavities[0]==face_cavities[1]
    cavities_ok=(regions[0]['before_protected_cells']>0 and regions[0]['after_protected_cells']==0
                 and all(r['added_geometry_remaining_fraction']<.25 and not r['missing_accepted_art'] for r in regions[1:]))
    result={'scope':'All actual added support runs, exact same cave regions, and eight unchanged templates',
            **preview_evidence,
            'reports':[{'path':p.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
            'supports':checks,'cave_regions':regions,'unchanged_templates':unchanged,
            'face_cavities_before_after':face_cavities,'face_cavity_contents_preserved':cavity_contents_preserved,
            'cave_regression_passed':cavities_ok,'read_errors':[w.read_errors for w in worlds],
            'passed':all(c['passed'] for c in checks) and cavities_ok and cavity_contents_preserved and not any(w.read_errors for w in worlds)}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2))
    return 0 if result['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
