"""Natural large/small landmark generation in all rotations and old-save upgrade.

Uses isolated local worlds only. The old player JAR bootstraps one V6 save;
the current JAR must keep its fingerprint, templates, markers and non-refill state.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime
import gzip,hashlib,json,os,shutil,socket,subprocess,time,zipfile
from pathlib import Path
from compile_worldgen import ROOT,compile_libraries
from smoke_server import Console
from test_natural_interiors_server import blocks_proof

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--accept-eula',action='store_true')
    parser.add_argument('--java-home',type=Path,required=True)
    parser.add_argument('--artifact',type=Path,required=True)
    parser.add_argument('--previous-artifact',type=Path,required=True)
    parser.add_argument('--upgrade-only',action='store_true')
    parser.add_argument('--partial-upgrade',action='store_true',help='Bootstrap V6 with only its central chunk, then finish the piece on the new JAR')
    parser.add_argument('--small-only',action='store_true',help='Use four known naturally accepted Small Colossus sites and their old-save upgrade')
    parser.add_argument('--tower-only',action='store_true',help='Use naturally accepted Tower sites in all four rotations and an old-save upgrade')
    parser.add_argument('--rotation',type=int,choices=range(4),help='Run only one rotation, including its upgrade case if selected')
    parser.add_argument('--asset',choices=('world_tree','titan_skull_2'),help='Check the tree or revised skull on accepted natural sites')
    parser.add_argument('--no-upgrade',action='store_true')
    args=parser.parse_args()
    if not args.accept_eula:parser.error('Accept Minecraft EULA for isolated server tests with --accept-eula')
    current=args.artifact.resolve();previous=args.previous_artifact.resolve();java=args.java_home.resolve()/'bin'
    run=ROOT/'build/colossus-landmarks-20261028'/datetime.now().strftime('native-%H%M%S-%f');run.mkdir(parents=True)
    deps=compile_libraries();cp=[p for p in deps if p.name=='fabric-loader-0.19.5.jar' or any(v in {'libraries','loader-libraries','versions'} for v in p.parts)]
    def test_mod(artifact,old):
        src=run/('old-src' if old else 'src');src.mkdir();classes=src/'classes';classes.mkdir()
        source=ROOT/'src/test/java/de/relics/NaturalInteriorChecks.java'
        if old:
            target=src/'NaturalInteriorChecks.java'
            # Compile the same checks against the previous public API; no Git history required.
            data=source.read_text(encoding='utf-8')
            for before,after in [('NaturalInteriors.certificate(level.getSeed(),site,revision)','NaturalInteriors.certificate(level.getSeed(),site)'),
                                 ('NaturalInteriors.manifest(revision)','NaturalInteriors.manifest()')]:
                assert before in data;data=data.replace(before,after)
            target.write_text(data,encoding='utf-8');sources=[target]
        else:sources=[source,ROOT/'src/test/java/de/relics/NaturalEncounterChecks.java']
        subprocess.run([str(java/'javac.exe'),'--release','25','-encoding','UTF-8','-proc:none','-classpath',os.pathsep.join(map(str,[artifact,*deps])),'-d',str(classes),*map(str,sources)],check=True)
        mod=src/'checks.jar'
        with zipfile.ZipFile(mod,'w') as z:
            for p in classes.rglob('*.class'):z.write(p,p.relative_to(classes).as_posix())
            z.writestr('fabric.mod.json',json.dumps({'schemaVersion':1,'id':'colossus-landmark-checks','version':'1','environment':'server',
                'entrypoints':{'main':['de.relics.NaturalInteriorChecks']+([] if old else ['de.relics.NaturalEncounterChecks'])},'depends':{'relics':'*'}}))
        return mod
    mods={False:test_mod(current,False),True:test_mod(previous,True)}
    report={'artifact_sha256':hashlib.sha256(current.read_bytes()).hexdigest(),'runs':[],'failures':[]}
    def snapshot(world):
        e=json.loads((world/'data/relics_distribution_v1.json').read_text());assert hashlib.sha256(e['payload'].encode()).hexdigest()==e['sha256']
        s=json.loads(e['payload']);return {k:s[k] for k in ('fingerprint','interiors','unique')}
    def check(seed,rotation,upgrade=False,planned_site=None):
        root=run/(str(seed)+'-r'+str(rotation)+('-upgrade' if upgrade else ''));(root/'mods').mkdir(parents=True)
        for f in [ROOT/'build/worldgen-dependencies/fabric-api-0.161.0+26.2.jar',ROOT/'build/worldgen-dependencies/lithostitched-1.8.0-fabric-26.2.jar']:shutil.copy2(f,root/'mods'/f.name)
        with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        props={'server-ip':'127.0.0.1','server-port':port,'online-mode':'true','white-list':'true','enforce-whitelist':'true','level-name':'world','level-seed':seed,
            'generate-structures':'true','view-distance':2,'simulation-distance':2,'pause-when-empty-seconds':0,'max-tick-time':60000,'difficulty':'normal'}
        (root/'server.properties').write_text(''.join(f'{k}={v}\n' for k,v in props.items()));(root/'eula.txt').write_text('eula=true\n')
        argv=['-Xms256M','-Xmx3G','-XX:ActiveProcessorCount=4','-Djava.awt.headless=true','-Drelics.interior.testConfig='+str(root/'sites.json'),'-cp',os.pathsep.join(map(str,cp)),'net.fabricmc.loader.impl.launch.knot.KnotServer','nogui']
        af=root/'args.txt';af.write_text('\n'.join('"'+v.replace('\\','/')+'"' for v in argv))
        rec={'seed':seed,'rotation':rotation,'upgrade_from_v6':upgrade,'partial_upgrade':upgrade and args.partial_upgrade,'passed':False};sites=[];frozen=None
        for iteration in range(3 if upgrade else 2):
            old=upgrade and iteration==0
            shutil.copy2(previous if old else current,root/'mods/relics.jar');shutil.copy2(mods[old],root/'mods/checks.jar')
            process=subprocess.Popen([str(java/'java.exe'),'@'+str(af)],cwd=root,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            console=Console(process,root/f'console-{iteration}.log',echo=False)
            def command(cmd,pattern,timeout=180):return console.command(cmd,pattern,timeout)
            try:
                console.wait(r'Done \(',timeout=180)
                command('gamerule minecraft:random_tick_speed 0',r'Gamerule random_tick_speed is now set to: 0')
                if iteration==0:
                    console.wait(r'Relic destination ',timeout=300)
                    if planned_site is None:
                        status=command('relicsdistribution status',r'"snapshot"');unique=json.loads(status[status.index('{'):])['snapshot']['unique']
                    else:
                        reply=command(f'relicsdistribution plan {planned_site["candidate"]["x"]} {planned_site["candidate"]["z"]}',r'Relic plan Cell')
                        unique=json.loads(reply.split(': ',2)[-1]);assert unique==planned_site,(unique,planned_site)
                    assert unique['candidate']['rotation']==rotation,unique
                    sites=[unique];(root/'sites.json').write_text(json.dumps(sites));rec['site']=unique
                    if upgrade and args.partial_upgrade:
                        x,z=unique['candidate']['x'],unique['candidate']['z']
                        command(f'forceload add {x} {z}',r'Marked|force.loaded|No chunks')
                        deadline=time.monotonic()+180
                        while 'Test passed' not in command(f'execute if loaded {x} 80 {z}',r'Test passed|Test failed'):
                            assert time.monotonic()<deadline;time.sleep(.25)
                        command('save-all flush',r'Saved the game');command('stop',r'Stopping the server');process.wait(timeout=120);console.thread.join(timeout=5)
                        assert process.returncode==0
                        frozen=snapshot(root/'world');rec['frozen']=frozen
                        from verify_world import AnvilWorld
                        pieces=[child for chunk in AnvilWorld(root/'world').chunks()
                                for name,start in chunk.get('structures',{}).get('starts',{}).items()
                                if name=='relics:'+unique['asset'] and start.get('id')!='INVALID' for child in start['Children']]
                        assert len(pieces)==1 and json.loads(pieces[0]['relics_natural_site'])['revision']==frozen['interiors']
                        rec['partial_saved_certificate']=pieces[0]['relics_natural_site'];continue
                if iteration==0 or upgrade and args.partial_upgrade and iteration==1:
                    unique=sites[0]
                    for x in range(unique['minX']//16,unique['maxX']//16+1,8):
                        end=min(x+7,unique['maxX']//16)
                        command(f'forceload add {x*16} {unique["minZ"]//16*16} {end*16+15} {unique["maxZ"]//16*16+15}',r'Marked|force.loaded|No chunks')
                    for x in range(unique['minX']//16,unique['maxX']//16+1):
                        for z in range(unique['minZ']//16,unique['maxZ']//16+1):
                            deadline=time.monotonic()+180
                            while 'Test passed' not in command(f'execute if loaded {x*16} 80 {z*16}',r'Test passed|Test failed'):
                                assert time.monotonic()<deadline;time.sleep(.25)
                deadline=time.monotonic()+60
                while True:
                    response=command('relicsinteriorstest verify',r'INTERIORS_PASS|INTERIORS_FAIL|INTERIORS_PENDING')
                    assert 'FAIL' not in response,response
                    if 'PASS' in response:break
                    assert time.monotonic()<deadline;time.sleep(.25)
                if not upgrade and iteration==0 and sites[0]['asset']=='colossus':
                    command('relicsnaturalencountertest',r'NATURAL_ENCOUNTER_STARTED|NATURAL_ENCOUNTER_FAIL')
                    response=console.wait(r'NATURAL_ENCOUNTER_PASS|NATURAL_ENCOUNTER_FAIL',timeout=120)
                    assert 'PASS' in response,response
                    rec['encounter']=(root/'natural-encounter-proof.txt').read_text()
                if iteration==(1 if upgrade else 0):
                    response=command('relicsinteriorstest mutate',r'INTERIORS_PASS|INTERIORS_FAIL');assert 'PASS' in response,response
                command('save-all flush',r'Saved the game');command('stop',r'Stopping the server');process.wait(timeout=120);console.thread.join(timeout=5)
                assert process.returncode==0 and not [l for l in console.lines if '/ERROR]' in l]
                now=snapshot(root/'world')
                if frozen is None:
                    frozen=now;rec['frozen']=frozen
                else:assert frozen==now,'World fingerprint/revision/target changed on upgrade/restart'
                if 'blocks' not in rec:
                    rec['blocks']=blocks_proof(root/'world',current,sites)
                    rec['initial_markers']=json.loads((root/'native-initial.json').read_text())
            finally:
                if process.poll() is None:
                    try:process.stdin.write('stop\n');process.stdin.flush();process.wait(timeout=30)
                    except Exception:process.terminate();process.wait(timeout=15)
        rec['passed']=True;(root/'evidence.json').write_text(json.dumps(rec,indent=2)+'\n');print('PASS',seed,'rotation',rotation,'upgrade',upgrade,flush=True);return rec
    cases=[(3528628362682006658,0,False),(-4685435945225202909,1,False),(7176494076711744605,2,False),(731204,3,False),(-4685435945225202909,1,True)]
    if args.small_only or args.tower_only or args.asset:
        baseline=json.loads((ROOT/'docs/testing/distribution-fix-20261027.json').read_text())
        chosen={}
        for row in baseline['seed_results']:
            for site in row['sites']:
                if site['asset']==(args.asset or ('ruined_tower' if args.tower_only else 'small_colossus')):chosen.setdefault(site['candidate']['rotation'],(row['seed'],site))
        assert chosen
        if not args.asset:assert set(chosen)=={0,1,2,3}
        cases=[(seed,rotation,False,site) for rotation,(seed,site) in chosen.items()]
        seed,site=chosen[1];cases.append((seed,1,True,site))
    if args.upgrade_only:cases=[c for c in cases if c[2]]
    if args.no_upgrade:cases=[c for c in cases if not c[2]]
    if args.rotation is not None:cases=[c for c in cases if c[1]==args.rotation]
    print('LANDMARK_SERVERS',run,flush=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures={pool.submit(check,*c):c for c in cases}
        for future in as_completed(futures):
            try:report['runs'].append(future.result())
            except Exception as e:report['failures'].append({'case':futures[future],'error':repr(e)});print('FAIL',futures[future],repr(e),flush=True)
            (run/'evidence.json').write_text(json.dumps(report,indent=2)+'\n')
    print('EVIDENCE',run/'evidence.json',flush=True)
    if report['failures']:raise SystemExit(1)

if __name__=='__main__':main()
