"""Verify and retain the bounded beta compatibility/performance test evidence."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import zlib

from PIL import Image
from smoke_server import read_nbt
from test_beta_performance import SCRATCH, ROOT, sha

EXPECTED_ARTIFACTS = {
    ('fabric','1.21.1'):'a10c4e665798568064ffb8eb37a25c8ded86d193ae5e4e3d785c3091243b9c16',
    ('fabric','26.2'):'9ce11af173ebfd5e2db2ad85a38133c1b1bcc7832154a4dee0c5ee1df01a6508',
    ('neoforge','1.21.1'):'86bb9380a3ed80d9bd2a15d51d1e444f2faba3a0aa53832acce52defce5cf50d',
    ('neoforge','26.2'):'bfd259fe5369e3ad42a00550e11f20f44459b5a748a317d29d8f359233dee486',
}

def bind(path):
    return {'path':str(path),'bytes':path.stat().st_size,'sha256':sha(path)}


def inspect_environment(world):
    data=read_nbt(gzip.decompress((world/'level.dat').read_bytes()))['Data']
    biomes=Counter();starts=Counter();statuses=Counter();templates=set();errors=[]
    region=world/'region'
    if not region.is_dir():region=world/'dimensions/minecraft/overworld/region'
    if not region.is_dir():raise AssertionError('Missing saved overworld region: '+str(world))
    for file in sorted(region.glob('*.mca')):
        raw=file.read_bytes()
        for index in range(1024):
            offset=int.from_bytes(raw[index*4:index*4+3],'big')*4096
            if not offset:continue
            try:
                count=int.from_bytes(raw[offset:offset+4],'big');kind=raw[offset+4];payload=raw[offset+5:offset+4+count]
                if kind==2:payload=zlib.decompress(payload)
                elif kind==1:payload=gzip.decompress(payload)
                elif kind!=3:raise ValueError('Unexpected compression '+str(kind))
                chunk=read_nbt(payload);status=chunk.get('status',chunk.get('Status','unknown'));statuses[status]+=1
                if not status.endswith(':full'):continue
                for section in chunk.get('sections',[]):
                    for biome in section.get('biomes',{}).get('palette',[]):biomes[biome]+=1
                for identifier,start in chunk.get('structures',{}).get('starts',{}).items():
                    if start.get('id') in ['INVALID',None]:continue
                    starts[identifier]+=1
                    for child in start.get('Children',[]):
                        element=child.get('pool_element',{})
                        if isinstance(element,dict) and isinstance(element.get('location'),str):templates.add(element['location'])
            except Exception as exc:errors.append({'file':file.name,'index':index,'error':repr(exc)})
    return {'enabled_datapacks':data['DataPacks']['Enabled'],'disabled_datapacks':data['DataPacks']['Disabled'],
            'saved_chunk_statuses':dict(statuses),'biome_palette_occurrences_in_full_chunks':dict(biomes),
            'valid_structure_starts_in_full_chunks':dict(starts),'piece_template_locations':sorted(templates),'read_errors':errors}


def performance():
    pairs=[]
    selections=[(loader+'-'+mc,mc,loader,731204,'measurement') for mc in ['26.2','1.21.1'] for loader in ['fabric','neoforge']]
    selections += [(profile.replace(' ','-'),mc,'fabric',seed,'validation') for profile,mc in [('TerraVista','26.2'),('TerraVista Living World','1.21.1')] for seed in [731204,731205]]
    for tag,mc,loader,seed,label in selections:
        rows={}
        for kind in ['relic','control']:
            path=SCRATCH/'runs'/f'{tag}-{seed}-{kind}-{label}'/'result.json';row=json.loads(path.read_text())
            if not row['passed'] or row['exit']!=0:raise AssertionError('Unsuccessful selected run: '+str(path))
            if kind=='relic' and row['artifact_sha256']!=EXPECTED_ARTIFACTS[loader,mc]:raise AssertionError('Candidate mismatch')
            if row.get('world_inspection',{}).get('read_errors'):raise AssertionError('Unreadable saved chunks')
            row['result_binding']=bind(path)
            row['capture_files']=[bind(path.parent/n) for n in ['console.log','bench-metrics.json','java-args.txt','server.properties','mods/beta-performance.jar']]
            idle=row['metrics']['phases']['idle']
            row['budget_checks']={'startup':row['startup_seconds']<=180,'idle_sample':idle['ticks']>=200,'idle_mean':idle['meanMs']<25,'idle_p95':idle['p95Ms']<50,'heap':row['metrics']['heapPeakBytes']<=4*2**30,
                                  'phase_timeouts':all(p['seconds']<=(300 if p['name'].startswith('colossus') else 180) for p in row['phases'])}
            if row['profile'] and seed==731204:
                row['saved_environment']=inspect_environment(path.parent/'world')
                if row['saved_environment']['read_errors']:raise AssertionError('Environment inspection failed')
            rows[kind]=row
        a,b=rows['relic'],rows['control']
        if a['route']!=b['route']:raise AssertionError('A/B routes differ')
        ap={p['name']:p for p in a['phases']};bp={p['name']:p for p in b['phases']}
        ordinary_limit=max(bp['ordinary']['seconds']*2,bp['ordinary']['seconds']+15)
        checks={'ordinary_overhead':ap['ordinary']['seconds']<=ordinary_limit,
                'colossus_overhead':all(p['seconds']<=bp[n]['seconds']+60 for n,p in ap.items() if n.startswith('colossus'))}
        if a['profile'] and seed==731204:
            site=a['colossus_site'];starts=a['world_inspection']['natural_structure_starts']
            checks['saved_natural_colossus']=any(s['structure']=='relics:colossus' and s['status'].endswith(':full') and any(box[0]==site['minX'] and box[2]==site['minZ'] and box[3]==site['maxX'] and box[5]==site['maxZ'] for box in s['bounding_boxes']) for s in starts)
            checks['tectonic_active']=all('tectonic:tectonic' in r['saved_environment']['enabled_datapacks'] for r in [a,b])
        passed=all(checks.values()) and all(all(r['budget_checks'].values()) for r in rows.values())
        pairs.append({'name':tag,'minecraft':mc,'loader':loader,'seed':seed,'runs':rows,'pair_checks':checks,'passed':passed})
        print(tag,seed,'budget checks:',passed,flush=True)
    return pairs


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--performance-only',action='store_true');args=ap.parse_args()
    result={'date':'2026-11-04','plan':'docs/testing/BETA_COMPATIBILITY_PLAN_20261104.md','performance_pairs':performance(),
            'performance_limitations':['Bounded cold-start tests on this PC, not a general hardware guarantee','Artificial bulk forceloads can block ticks; idle and load phases are kept separate',
                'TerraVista dedicated reference excludes Voxy World Gen V2, whose client integration requires LWJGL; actual clients retain it']}
    inventories=[]
    for name in ['TerraVista','TerraVista-Living-World']:
        path=SCRATCH/(name+'-inventory.json');inventory=json.loads(path.read_text());profile=Path(inventory['profile']);changed=[]
        for file,hash in inventory['protected_files'].items():
            p=profile/file
            if not p.is_file() or sha(p)!=hash:changed.append(file)
        inventories.append({'inventory':bind(path),'root_jars':len(inventory['mods']),'protected_files':len(inventory['protected_files']),'protected_file_hashes':inventory['protected_files'],'changed_original_files':changed,'mods':inventory['mods']})
    result['profile_inventories']=inventories
    if not args.performance_only:
        graphics=[]
        selected=json.loads((SCRATCH/'graphics-selection.json').read_text())
        for name in selected:
            run=SCRATCH/'clients'/name;row=json.loads((run/'result.json').read_text())
            if not row.get('passed'):raise AssertionError('Unsuccessful selected graphics run '+name)
            retained=[]
            pictures=sorted((run/'screenshots').glob('*.png'))
            for p in pictures:
                with Image.open(p) as image:image.load()
                dest=ROOT/'docs/testing/images/beta-compatibility-20261104'/name/p.name
                dest.parent.mkdir(parents=True,exist_ok=True)
                if dest.exists() and sha(dest)!=sha(p):raise AssertionError('Different retained screenshot exists')
                if not dest.exists():shutil.copy2(p,dest)
                retained.append({'source':bind(p),'retained':bind(dest),'role':'world view' if p==pictures[-1] else 'setup menu','manual_world_view_review':p==pictures[-1]})
            row['retained_screenshots']=retained;row['source_result']=bind(run/'result.json');row['console']=bind(run/'console.log');row['args']=bind(run/'client-args.txt')
            row['runtime_inputs']=[bind(run/'options.txt'),bind(run/'mods/menu-checks.jar')]+[bind(p) for p in (run/'config').rglob('*') if p.is_file()]
            graphics.append(row)
        result['graphics_clients']=graphics
        dh=[]
        for name in ['generator-150234','generator-151400']:
            path=SCRATCH/'dh'/name/'result.json';row=json.loads(path.read_text())
            if not row.get('passed'):raise AssertionError('Selected DH probe did not complete')
            row['result_binding']=bind(path);row['console']=bind(path.parent/'console.log');row['probe_sources']=[bind(p) for p in (path.parent/'sources').glob('*.java')]
            dh.append(row)
        result['dh_generator_tests']=dh
        run=SCRATCH/'lod-client/render-152832';lod=json.loads((run/'result.json').read_text())
        if not lod.get('passed') or lod['proof']['targetNormallyLoaded'] or lod['proof']['distanceToTargetXZ']<=lod['proof']['vanillaRenderDistance']*16:
            raise AssertionError('LOD before-visit invariant failed')
        source=sorted((run/'screenshots').glob('*.png'))[-1]
        with Image.open(source) as picture:picture.load()
        dest=ROOT/'docs/testing/images/beta-compatibility-20261104/dh-colossus-before-visit.png';dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists() and sha(dest)!=sha(source):raise AssertionError('Refusing to replace different LOD evidence')
        if not dest.exists():shutil.copy2(source,dest)
        lod.update(source_result=bind(run/'result.json'),console=bind(run/'console.log'),args=bind(run/'client-args.txt'),screenshot={'source':bind(source),'retained':bind(dest)},
                   review='Root viewed: Colossus silhouette visible in DH LOD; target normally unloaded at 400 blocks, vanilla distance 2. Cut edges bound the prepared chunk dataset.')
        result['dh_lod_before_visit']=lod
    result['all_performance_budgets_pass']=all(p['passed'] for p in result['performance_pairs'])
    result['original_profile_files_unchanged']=all(not i['changed_original_files'] for i in inventories)
    output=SCRATCH/('performance-collected.json' if args.performance_only else 'compatibility-collected.json')
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(output)


if __name__=='__main__':main()
