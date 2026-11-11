"""Serial Fabric 1.21.1 Living-World regression: baseline, filter, reload, old-save preservation.

Uses an existing isolated server fixture; never opens the supplied player saves.
Requires --accept-eula. All Java children are stopped, terminated, then killed on timeout.
"""
from __future__ import annotations
import argparse,hashlib,json,os,shutil,signal,socket,subprocess,time,zipfile
from pathlib import Path
from smoke_server import Console
ROOT=Path(__file__).resolve().parents[1]

def stop(process,console):
    if process.poll() is None:
        try:process.stdin.write('stop\n');process.stdin.flush();process.wait(timeout=45)
        except (OSError,subprocess.TimeoutExpired):
            os.killpg(process.pid,signal.SIGTERM)
            try:process.wait(timeout=10)
            except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait(timeout=10)
    console.thread.join(timeout=5)

def journal(world):
    raw=(world/'data/relics_distribution_v1.json').read_bytes();e=json.loads(raw)
    assert hashlib.sha256(e['payload'].encode()).hexdigest()==e['sha256']
    return raw,json.loads(e['payload'])

def selected(seed,dimension,id,x,z):
    mask=(1<<64)-1
    def mix(v):
        v &= mask;v=((v^(v>>30))*0xbf58476d1ce4e5b9)&mask;v=((v^(v>>27))*0x94d049bb133111eb)&mask;return v^(v>>31)
    key=0x4bcd350f92e76a81^mix(seed)^mix(((x&0xffffffff)<<32)^(z&0xffffffff))
    for b in (dimension+'\0'+id).encode():key=mix(key^b)
    return mix(key)&1==0

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--accept-eula',action='store_true')
    for arg in ['artifact','baseline','probe','fixture','java','output','input']:p.add_argument('--'+arg,type=Path,required=True)
    p.add_argument('--seed',type=int,default=-4443928181842649648)
    p.add_argument('--extra-cases',action='store_true',help='After the four saved passes, test reverse visitation and dense-village bootstrap')
    args=p.parse_args()
    if not args.accept_eula:p.error('Pass --accept-eula only after accepting https://aka.ms/MinecraftEULA for isolated tests')
    run=args.output.resolve();run.mkdir(parents=True,exist_ok=True);mods=run/'mods';mods.mkdir(exist_ok=True)
    for file in (args.fixture/'mods').glob('*.jar'):
        with zipfile.ZipFile(file) as z:
            try:mid=json.loads(z.read('fabric.mod.json'))['id']
            except KeyError:continue
        if mid=='relics' or 'checks' in mid or 'probe' in mid:continue
        dest=mods/file.name
        if not dest.exists():os.link(file,dest)
    for name in ['config','defaultconfigs','moonlight-global-datapacks']:
        src=args.fixture/name
        if src.is_dir() and not (run/name).exists():shutil.copytree(src,run/name)
    with zipfile.ZipFile(args.probe) as z,zipfile.ZipFile(mods/'surface-checks.jar','w') as out:
        for n in z.namelist():
            if n.endswith('.class'):out.writestr(n,z.read(n))
        out.writestr('fabric.mod.json',json.dumps({'schemaVersion':1,'id':'relics_surface_checks','version':'1','environment':'server','entrypoints':{'main':['de.relics.SurfaceStructureBootChecks']},'depends':{'relics':'*'}}))
    runtime=args.fixture/'runtime';cp=[runtime/'versions/1.21.1/server-1.21.1.jar',*sorted((runtime/'libraries').rglob('*.jar')),*sorted((runtime/'loader').rglob('*.jar'))]
    assert all(x.is_file() for x in cp)
    (run/'eula.txt').write_text('eula=true\n');shutil.copy2(args.input,run/'surface-audit-input.json')
    families={name:{'mode':'LANDSCAPES','selected':[]} for name in ['colossus','obelisk','titan_skull','titan_skull_2','ruined_tower','small_colossus','world_tree']}
    settings={'format':1,'settings':{'cellSize':2000,'minDistance':800,'obeliskDistance':6000,'regionRadius':2400,'colossusMinDistance':4000,'generationRevision':3,'outside':[3000,1500,1500,200,200,200],'inside':[3000,2500,2500,200,200,200],'biomes':{'families':families}}}
    passes=[('baseline',args.baseline,'world-baseline'),('filtered',args.artifact,'world-filtered'),('filtered-reload',args.artifact,'world-filtered'),('legacy-reload',args.artifact,'world-baseline')]
    evidence={'seed':args.seed,'artifact_sha256':hashlib.sha256(args.artifact.read_bytes()).hexdigest(),'baseline_sha256':hashlib.sha256(args.baseline.read_bytes()).hexdigest(),'passes':[]}
    if args.extra_cases:
        previous=json.loads((run/'evidence.json').read_text())
        assert all(previous[k]==evidence[k] for k in ['seed','artifact_sha256','baseline_sha256']), 'Previous native evidence is for different inputs'
        assert [x['name'] for x in previous['passes']]==[x[0] for x in passes], 'Four successful baseline/reload passes required first'
        evidence=previous
        passes=[('reverse',args.artifact,'world-reverse'),('bootstrap',args.artifact,'world-bootstrap')]
    for name,artifact,worldname in passes:
        world=run/worldname
        if not world.exists():
            (world/'data').mkdir(parents=True);(world/'data/relics_creation_settings.json').write_text(json.dumps(settings))
        test_input=json.loads(args.input.read_text())
        if name=='reverse':test_input['starts'].reverse()
        if name=='bootstrap':
            test_input={'cells':[],'starts':[],'blocks':[]}
            pack=world/'datapacks/surface-bootstrap';(pack/'data/minecraft/worldgen/structure').mkdir(parents=True,exist_ok=True)
            (pack/'data/minecraft/worldgen/structure_set').mkdir(parents=True,exist_ok=True)
            (pack/'pack.mcmeta').write_text(json.dumps({'pack':{'pack_format':48,'description':'Isolated dense-village bootstrap test'}}))
            with zipfile.ZipFile(runtime/'versions/1.21.1/server-1.21.1.jar') as vanilla:
                village=json.loads(vanilla.read('data/minecraft/worldgen/structure/village_plains.json'))
            env=json.loads((run/'world-baseline/data/relics_planning_environment_v1.json').read_text())
            village['biomes']=[b['id'] for b in env['signature']['biomes']];village['size']=0
            (pack/'data/minecraft/worldgen/structure/village_plains.json').write_text(json.dumps(village))
            (pack/'data/minecraft/worldgen/structure_set/villages.json').write_text(json.dumps({'placement':{'type':'minecraft:random_spread','spacing':2,'separation':1,'salt':10387312},'structures':[{'structure':'minecraft:village_plains','weight':1}]}))
        (run/'surface-audit-input.json').write_text(json.dumps(test_input))
        before=journal(world)[0] if (world/'data/relics_distribution_v1.json').exists() else None
        shutil.copy2(artifact,mods/'relics-current.jar')
        with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        properties={'server-ip':'127.0.0.1','server-port':port,'online-mode':'true','white-list':'true','enforce-whitelist':'true','max-players':1,'enable-query':'false','enable-rcon':'false','level-name':worldname,'level-seed':args.seed,'generate-structures':'true','gamemode':'creative','difficulty':'peaceful','view-distance':2,'simulation-distance':2,'max-tick-time':120000,'pause-when-empty-seconds':0}
        (run/'server.properties').write_text(''.join(f'{k}={v}\n' for k,v in properties.items()))
        cmd=[str(args.java.resolve()),'-Xms256M','-Xmx2500M','-XX:ActiveProcessorCount=1','-Djava.awt.headless=true','-cp',os.pathsep.join(str(x.resolve()) for x in cp),'net.fabricmc.loader.impl.launch.knot.KnotServer','nogui']
        print('START',name,flush=True);start=time.monotonic()
        process=subprocess.Popen(cmd,cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,start_new_session=True)
        console=Console(process,run/(name+'.log'),echo=False)
        try:
            console.wait(r'Done \(',timeout=240)
            # The persisted unique site, rather than a log line absent on reload, establishes readiness.
            deadline=time.monotonic()+240
            while True:
                _,state=journal(world)
                if state.get('unique') or state.get('unavailable'):break
                if time.monotonic()>deadline:raise TimeoutError('Unique search did not settle')
                time.sleep(.25)
            console.command('surfaceaudit',r'SURFACE_AUDIT_OK',timeout=360)
            console.command('save-all flush',r'Saved the game',timeout=90)
            result=json.loads((run/'surface-audit-result.json').read_text());shutil.copy2(run/'surface-audit-result.json',run/(name+'-result.json'))
        finally:stop(process,console)
        assert process.returncode==0,(name,process.returncode)
        raw,state=journal(world)
        if before is not None:assert before==raw,(name,'persisted plan changed during reload')
        evidence['passes'].append({'name':name,'seconds':round(time.monotonic()-start,2),'state':state,'result':result})
        (run/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print('PASS',name,round(time.monotonic()-start,1),'s',flush=True)
    base,new,reloaded,legacy=[x['result'] for x in evidence['passes'][:4]]
    assert base['plans']==new['plans']==reloaded['plans']==legacy['plans'],'Relic sites changed'
    assert base['runtime']['snapshot']['unique']==new['runtime']['snapshot']['unique'],'Unique Colossus changed'
    assert base['runtime']['snapshot'].get('surfaceStructures') is None and legacy['runtime']['snapshot'].get('surfaceStructures') is None
    assert new['runtime']['snapshot']['surfaceStructures']==reloaded['runtime']['snapshot']['surfaceStructures']
    assert new['starts']==reloaded['starts'] and base['starts']==legacy['starts'],'Persisted structure decisions changed'
    changed=[]
    for old,current in zip(base['starts'],new['starts']):
        if old['valid'] and not current['valid']:
            assert selected(args.seed,'minecraft:overworld',old['id'],old['x'],old['z']);changed.append(old['id'])
    assert changed,'No colliding whole structure was suppressed in native test'
    assert base['blocks']==new['blocks'],'Selected relic model blocks changed'
    if args.extra_cases:
        reverse,bootstrap=[x['result'] for x in evidence['passes'][4:]]
        canonical=lambda rows:sorted(rows,key=lambda r:(r['id'],r['x'],r['z']))
        assert canonical(reverse['starts'])==canonical(new['starts']), 'First-visit order changed foreign decisions'
        assert reverse['plans']==new['plans'] and reverse['blocks']==new['blocks'], 'First-visit order changed relics'
        assert bootstrap['runtime']['surfaceFilter']['bootstrapPreserved']>0, 'Native initial-area exception was not exercised'
    evidence['assertions']=['same six ordinary relic plans','same unique Colossus','whole foreign-start suppression observed','filtered restart stable','legacy snapshot bytes and structures preserved','sampled model blocks unchanged'];evidence['suppressed_types']=changed
    if args.extra_cases:evidence['assertions']+=['reverse first-visit order stable','native dense-village initial-spawn exception exercised']
    (run/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print('ALL NATIVE SURFACE CHECKS PASSED',changed,flush=True)
if __name__=='__main__':main()
