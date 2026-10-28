"""Verify native Alpha 5 port placement, exact footprints, actions, maps and non-refill."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime
import hashlib,json,os,re,shutil,socket,subprocess,time,uuid
from pathlib import Path
from smoke_server import prepare_classpath
from test_alpha5_port_server import PortConsole as Console
from test_natural_interiors_server import blocks_proof

ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--accept-eula',action='store_true');p.add_argument('--java',type=Path,required=True)
    p.add_argument('--artifact',type=Path,required=True);p.add_argument('--test-mod',type=Path,required=True)
    p.add_argument('--loader',default='fabric');p.add_argument('--minecraft',default='1.21.1')
    p.add_argument('--case',choices=('all','obelisk','small_colossus','world_tree','ruined_tower','titan_skull_2'),default='all')
    a=p.parse_args()
    if not a.accept_eula:p.error('Accept EULA for the isolated Minecraft tests')
    source=a.artifact.resolve();source_test=a.test_mod.resolve();base=ROOT/'build/alpha5-ports-20261028'
    run=base/(datetime.now().strftime(f'natural-{a.loader}-{a.minecraft}-%H%M%S-%f')+'-'+uuid.uuid4().hex[:8]);run.mkdir(parents=True)
    inputs=run/'inputs';inputs.mkdir()
    artifact=inputs/source.name;artifact.write_bytes(source.read_bytes())
    testmod=inputs/source_test.name;testmod.write_bytes(source_test.read_bytes())
    # Later worlds and the independent verifier always read these immutable copies.
    assert hashlib.sha256(artifact.read_bytes()).hexdigest()==hashlib.sha256(source.read_bytes()).hexdigest()
    assert hashlib.sha256(testmod.read_bytes()).hexdigest()==hashlib.sha256(source_test.read_bytes()).hexdigest()
    cp=prepare_classpath(Path('E:/Roaming/ModrinthApp'),Path.home()/f'.gradle/caches/fabric-loom/{a.minecraft}/minecraft-server.jar',base/f'runtime-fabric-{a.minecraft}',a.minecraft)
    baseline=json.loads((ROOT/'docs/testing/distribution-fix-20261027.json').read_bytes())
    cases=[(731204,'obelisk'),(-48291736,'small_colossus'),(20260913,'world_tree'),(4661570585687253657,'ruined_tower'),(731204,'titan_skull_2')]
    if a.case!='all':cases=[c for c in cases if c[1]==a.case]
    report={'loader':a.loader,'minecraft':a.minecraft,'artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),'runs':[],'failures':[]}
    print('NATURAL_PORT',run,flush=True)
    def check(seed,asset):
        root=run/str(seed);(root/'mods').mkdir(parents=True)
        for file in (artifact,testmod,*[(ROOT/'build/compat-mc1.21.1/dependencies'/name) for name in ('fabric-api-0.116.17+1.21.1.jar','lithostitched-1.8.0-fabric-21.1.jar')]):shutil.copy2(file,root/'mods'/file.name)
        with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        props={'server-ip':'127.0.0.1','server-port':port,'online-mode':'true','white-list':'true','enforce-whitelist':'true','level-name':'world','level-seed':seed,'generate-structures':'true','view-distance':2,'simulation-distance':2,'max-tick-time':60000,'difficulty':'normal'}
        (root/'server.properties').write_text(''.join(f'{k}={v}\n' for k,v in props.items()),encoding='utf-8');(root/'eula.txt').write_text('eula=true\n',encoding='utf-8')
        argv=['-Xms256M','-Xmx3G','-XX:ActiveProcessorCount=4','-Djava.awt.headless=true','-Drelics.interior.testConfig='+str(root/'sites.json'),'-cp',os.pathsep.join(map(str,cp)),'net.fabricmc.loader.impl.launch.knot.KnotServer','nogui']
        argfile=root/'args.txt';argfile.write_text('\n'.join('"'+v.replace('\\','/')+'"' for v in argv),encoding='utf-8')
        record={'seed':seed,'asset':asset,'sites':[],'iterations':[]};sites=[]
        candidates=[s for row in baseline['seed_results'] if row['seed']==seed for s in row['sites'] if s['asset']==asset]
        for iteration in range(3):
            process=subprocess.Popen([str(a.java.resolve()),'@'+str(argfile)],cwd=root,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            console=Console(process,root/f'console-{iteration}.log',echo=False)
            def command(cmd,pattern,timeout=180):return console.command(cmd,pattern,timeout)
            try:
                console.wait(r'Done \(',timeout=240)
                command('gamerule randomTickSpeed 0',r'Gamerule|Unknown|Incorrect')
                if iteration==0:
                    console.wait(r'Relic destination ',timeout=300)
                    status=command('relicsdistribution status',r'"snapshot"')
                    unique=json.loads(status[status.index('{'):])['snapshot']['unique']
                    if asset=='obelisk':
                        assert unique and unique['asset']=='colossus';sites.append(unique)
                    for old in candidates[:2]:
                        candidate=old['candidate']
                        response=command(f'relicsdistribution plan {candidate["x"]} {candidate["z"]}',r'Relic plan Cell',timeout=300)
                        planned=json.loads(re.search(r'Relic plan Cell\[.*?\]: (.*)',response).group(1))
                        if planned is not None and planned['asset']==asset and planned not in sites:sites.append(planned)
                    assert any(s['asset']==asset for s in sites),('No valid target at candidate nominations',seed,asset)
                    (root/'sites.json').write_text(json.dumps(sites),encoding='utf-8');record['sites']=sites
                    for site in sites:
                        for x in range(site['minX']//16,site['maxX']//16+1,8):
                            end=min(x+7,site['maxX']//16)
                            command(f'forceload add {x*16} {site["minZ"]//16*16} {end*16+15} {site["maxZ"]//16*16+15}',r'Marked|force.loaded|No chunks')
                # 1.21.1 publishes Done before all persisted forced chunks are FULL.
                for site in sites:
                    for x in range(site['minX']//16,site['maxX']//16+1):
                        for z in range(site['minZ']//16,site['maxZ']//16+1):
                            deadline=time.monotonic()+180
                            while 'Test passed' not in command(f'execute if loaded {x*16} 80 {z*16}',r'Test passed|Test failed'):
                                assert time.monotonic()<deadline;time.sleep(.25)
                deadline=time.monotonic()+120
                while True:
                    reply=command('relicsinteriorstest verify',r'INTERIORS_PASS|INTERIORS_FAIL|INTERIORS_PENDING')
                    assert 'FAIL' not in reply,reply
                    if 'PASS' in reply:break
                    assert time.monotonic()<deadline;time.sleep(.25)
                console.wait(r'Relic distribution map checks passed:',timeout=180)
                if iteration==1:assert 'PASS' in command('relicsinteriorstest mutate',r'INTERIORS_PASS|INTERIORS_FAIL')
                command('save-all flush',r'Saved the game');command('stop',r'Stopping the server');process.wait(timeout=120);console.thread.join(timeout=5)
                errors=[line for line in console.lines if '/ERROR]' in line or 'Couldn\'t parse' in line]
                assert process.returncode==0 and not errors,errors[:5]
                if iteration==0:record['blocks']=blocks_proof(root/'world',artifact,sites,plant='minecraft:fern')
                record['iterations'].append({'iteration':iteration,'exit_code':process.returncode,'verification':reply})
            finally:
                if process.poll() is None:
                    try:process.stdin.write('stop\n');process.stdin.flush();process.wait(timeout=30)
                    except Exception:process.terminate();process.wait(timeout=15)
        record['passed']=True;(root/'evidence.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
        print('PASS natural',seed,asset,flush=True);return record
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures={pool.submit(check,*case):case for case in cases}
        for future in as_completed(futures):
            try:report['runs'].append(future.result())
            except Exception as error:
                report['failures'].append({'case':futures[future],'error':repr(error)});print('FAIL',futures[future],repr(error),flush=True)
            (run/'evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('EVIDENCE',run/'evidence.json',flush=True)
    return int(bool(report['failures']))


if __name__=='__main__':raise SystemExit(main())
