"""Verify closed real-client QA runs, saved NBT and preservation; emit additive evidence."""
import argparse,collections,gzip,hashlib,json,re
from pathlib import Path
from smoke_server import read_nbt

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'build/beta-client-gameplay-20261104'
HOST='00000000-0000-0000-0000-000000000001'
GUEST='b2c6551d-8ddf-3bc0-84e1-962967c209f5'
RUNS={
 'fabric26':dict(long='fabric-26.2-112500',restart='fabric-26.2-115032',late='fabric-26.2-123020',late_end='fabric-26.2-121526',craft='fabric-26.2-122231',craft_restart='fabric-26.2-122752'),
 'neo26':dict(long='neoforge-26.2-112602',restart='neoforge-26.2-115154',late='neoforge-26.2-123030',late_end='neoforge-26.2-121536',craft='neoforge-26.2-122241',craft_restart='neoforge-26.2-122802'),
 'fabric21':dict(long='fabric-1.21.1-112718',restart='fabric-1.21.1-120340',late='fabric-1.21.1-123252',late_end='fabric-1.21.1-122251',craft='fabric-1.21.1-122732',craft_restart='fabric-1.21.1-122941'),
 'neo21':dict(long='neoforge-1.21.1-112652',restart='neoforge-1.21.1-120330',late='neoforge-1.21.1-123302',late_end='neoforge-1.21.1-122301',craft='neoforge-1.21.1-122742',craft_restart='neoforge-1.21.1-122951'),
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
def world(run):return run/'saves'/(run/'created-world.txt').read_text().strip()
def saved(run):
    w=world(run);folder=w/'players/data' if (w/'players/data').exists() else w/'playerdata'
    result={}
    for p in folder.glob('*.dat'):
        nbt=read_nbt(gzip.decompress(p.read_bytes()))
        def receipts(v):
            if isinstance(v,dict):
                if 'relics:delivery_receipts' in v:return sorted(v['relics:delivery_receipts'])
                for child in v.values():
                    found=receipts(child)
                    if found is not None:return found
            return None
        result[p.stem]={'inventory':nbt['Inventory'],'receipts':receipts(nbt) or [],'recipe_book':nbt.get('recipeBook',{}),'file':ref(p)}
    envelope=read(w/'data/relics_gameplay_v1.json')
    assert hashlib.sha256(envelope['payload'].encode()).hexdigest()==envelope['sha256']
    return {'players':result,'ledger':json.loads(envelope['payload']),'ledger_file':ref(w/'data/relics_gameplay_v1.json')}
def count(inv,item):return sum(x.get('count',x.get('Count',0)) for x in inv if x['id']==item)
def process(run):
    p=read(run/'process.json');assert p['exit']==0,(run,p)
    out={k:v for k,v in p.items() if k!='files'}
    out['process_record']=ref(run/'process.json')
    # Bind final closed logs, not the earlier host snapshot of a still-running guest.
    out['evidence']=[ref(f) for f in run.rglob('*') if f.is_file() and (f.suffix in ('.log','.java','.png') or f.name in ('client-args.txt','options.txt','gameplay-proof.txt','long-session-proof.txt','late-event-proof.txt','save-reload-proof.txt','persistence-before.json','persistence-after.json','encounter-final.json','visual-cases.json','visual-proof.txt','menu-checks.jar','load-checks.jar'))]
    out['connections']=[line for line in (run/'console.log').read_text(errors='replace').splitlines() if 'logged in with entity id' in line or 'UUID of player' in line or 'joined the game' in line]
    out['guests']=[]
    for f in run.glob('guest*/process.json'):
        g=read(f);assert g['exit']==0,(f,g);out['guests'].append({k:v for k,v in g.items() if k!='files'})
    return out
def encounter(run,late=False):
    ledger=read(run/'encounter-final.json');events=len(ledger['sites']);ds=list(ledger['deliveries'].values())
    assert len(ds)==events*4 and len(ledger['vaultClaims'])==events*2
    assert all(d['phase']=='DELIVERED' and d['dropUuid'] for d in ds)
    assert len({d['dropUuid'] for d in ds})==len(ds)
    assert all(d['keyPaid'] for d in ds if d['reward']=='CORE')
    assert collections.Counter(d['player'] for d in ds)=={HOST:events*2,GUEST:events*2}
    console=(run/'console.log').read_text(errors='replace')
    drops=set(re.findall(r'QA_PHYSICAL_DROP (\S+) (\S+)',console));assert {d['dropUuid'] for d in ds}<={d[1] for d in drops}
    text=(run/'encounter-actions.log').read_text();states=[]
    for line in text.splitlines():
        _,s=line.split(' ',1)
        if s.startswith('{'):states.append(json.loads(s))
    active=[len(s['sites']['fixture:networkqa0']['participants']) for s in states if s['sites']['fixture:networkqa0']['phase']=='ACTIVE']
    assert 2 in active
    if late:
        assert 1 in active and active.index(1)<active.index(2)
        for uuid in (HOST,GUEST):assert re.search(r'QA_KEY_CONSUMED_BEFORE_CORE '+uuid+r'.*phase=QUEUED keys=0',console)
    proof=(run/('late-event-proof.txt' if late else 'long-session-proof.txt')).read_text()
    duration=int(re.search(r'duration_ms=(\d+)',proof)[1]);assert late or duration>=1200000
    return {'events':events,'duration_ms':duration,'unique_physical_drops':len(drops),'deliveries':len(ds),'claims':len(ledger['vaultClaims']),'active_participant_counts':sorted(set(active)),'host_attacks':text.count('client attack '),'host_key_uses':text.count('client use key'),'guest_attacks':(run/'guest/encounter-actions.log').read_text().count('client attack '),'guest_key_uses':(run/'guest/encounter-actions.log').read_text().count('client use key'),'key_consumed_before_queued_core_direct_inventory_assertion':late}
def collect():
    result={'scope':'Explicit Beta roadmap point 4; operator-prepared fixtures; actual loopback Minecraft clients','targets':{},'runs':{},'helpers':[]}
    for target,names in RUNS.items():
        runs={k:BASE/v for k,v in names.items()};out={'runs':names}
        out['long']=encounter(runs['long']);out['late_active']=encounter(runs['late'],True)
        for kind in ('restart','late_end','craft_restart'):
            r=runs[kind];assert read(r/'persistence-before.json')==read(r/'persistence-after.json');assert (r/'save-reload-proof.txt').exists()
        before,after=saved(runs['long']),saved(runs['restart'])
        assert before['ledger']==after['ledger']
        for uuid in (HOST,GUEST):
            for key in ('inventory','receipts'):assert before['players'][uuid][key]==after['players'][uuid][key],(target,uuid,key)
            inv=after['players'][uuid]['inventory'];assert count(inv,'relics:machine_core')==out['long']['events'];assert count(inv,'relics:colossus_key')==0
        out['full_restart']={'inventory_and_receipts_exact':True,'ledger_exact':True,'before':before,'after':after}
        late=read(runs['late_end']/'persistence-after.json');lateuuid=next(u for u in late['players'] if u!=HOST)
        assert late['ledger']==before['ledger'];assert not late['players'][lateuuid]['receipts'];assert not late['players'][lateuuid]['inventory']
        out['late_after_end']={'uuid':lateuuid,'inventory':[],'receipts':{},'ledger_unchanged':True,'save_reload_unchanged':True}
        craft,restored=saved(runs['craft']),saved(runs['craft_restart']);assert craft['players'][HOST]['inventory']==restored['players'][HOST]['inventory']
        inv=restored['players'][HOST]['inventory']
        expected={'relics:monolith_armor_trim_smithing_template':2,'relics:machine_core':1,'relics:salvage_magnet':1,'minecraft:diamond_chestplate':1}
        assert all(count(inv,k)==v for k,v in expected.items())
        armor=next(x for x in inv if x['id']=='minecraft:diamond_chestplate');assert armor['components']['minecraft:trim']['pattern']=='relics:monolith'
        txt=(runs['craft']/'gameplay-actions.log').read_text();assert all('PASS recipe='+str(i) in txt for i in range(4));assert txt.count('recipe book visible')==3
        snapshot=read(runs['craft_restart']/'persistence-after.json');budgets={x['id']:x['budget'] for x in snapshot['players'][HOST]['inventory'] if 'budget'in x}
        assert budgets=={'relics:machine_core':256,'relics:salvage_magnet':1000}
        out['craft']={'counts':expected,'budgets':budgets,'ingredients_consumed':True,'recipe_book_opened':3,'trim':armor['components']['minecraft:trim'],'full_restart_inventory_exact':True,'save_reload_exact':True,'before':craft,'after':restored}
        for kind,r in runs.items():result['runs'][r.name]=process(r)
        result['targets'][target]=out
    for p in [*ROOT.glob('tools/*beta*gameplay*.py'),ROOT/'tools/prepare_beta_visual_cases.py',*ROOT.glob('src/test/client/de/relics/testmixin/Beta*.java')]:result['helpers'].append(ref(p))
    baseline=read(BASE/'preservation-before.json');authorized=read(BASE/'authorized-root-audio-changes.json')['root_files'];diff=[]
    for name,digest in baseline.items():
        p=ROOT/name;now=sha(p) if p.exists() else None
        if now!=digest:diff.append({'path':name,'before':digest,'after':now,'authorized_root_audio':authorized.get(name)==now})
    assert all(x['authorized_root_audio'] for x in diff),diff
    result['preservation']={'baseline':ref(BASE/'preservation-before.json'),'files_checked':len(baseline),'differences':diff,'root_audio_authorization':ref(BASE/'authorized-root-audio-changes.json'),'identical_jar_storage_deduplication':ref(BASE/'identical-jar-hardlinks.json')}
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=BASE/'verified-evidence.json');a=ap.parse_args();r=collect();a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2));print('Verified',len(r['targets']),'targets;',len(r['runs']),'closed host runs')
