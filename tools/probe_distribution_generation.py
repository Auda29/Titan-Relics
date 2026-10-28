"""Reproduce a nominated natural-generation failure with an unchanged artifact.

No diagnostic planner runs. An optional tiny exception logger only preserves
Minecraft's detailed crash report; --vanilla omits Relic for a control run.
"""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import time
import zipfile
from compile_worldgen import ROOT, compile_libraries
from smoke_server import Console


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--java-home',type=Path,required=True)
    p.add_argument('--accept-eula',action='store_true')
    p.add_argument('--vanilla',action='store_true')
    p.add_argument('--audit',type=Path,required=True)
    p.add_argument('--artifact',type=Path,default=ROOT/'build/distribution-artifacts/relics-0.1.0-alpha.5.0+mc26.2.jar')
    p.add_argument('--world-copy',type=Path,help='Copy an earlier isolated build/ test world; never open its source')
    args=p.parse_args()
    if not args.accept_eula:p.error('Read https://aka.ms/MinecraftEULA and accept for this isolated probe')
    audit=json.loads(args.audit.read_text());site=audit['accepted_sites'][0]
    run=ROOT/'build/distribution-audit-20261027'/datetime.now().strftime('probe-%H%M%S-%f')
    (run/'mods').mkdir(parents=True)
    copied_state=None
    if args.world_copy:
        source=args.world_copy.resolve()
        if not source.is_relative_to((ROOT/'build').resolve()) or source.name!='world':
            p.error('Only isolated worlds under this checkout build/ may be copied')
        state=source/'data/relics_distribution_v1.json'
        if state.exists():copied_state=json.loads(json.loads(state.read_text())['payload'])
        shutil.copytree(source,run/'world')
    artifact=args.artifact.resolve()
    deps=compile_libraries()
    cp=[v for v in deps if v.name=='fabric-loader-0.19.5.jar' or any(s in {'libraries','loader-libraries','versions'} for s in v.parts)]
    mods=[ROOT/'build/worldgen-dependencies/fabric-api-0.161.0+26.2.jar',ROOT/'build/worldgen-dependencies/lithostitched-1.8.0-fabric-26.2.jar']
    if not args.vanilla:mods.append(artifact)
    for mod in mods:shutil.copy2(mod,run/'mods'/mod.name)
    classes=run/'test-classes';classes.mkdir()
    subprocess.run([str(args.java_home/'bin/javac.exe'),'--release','25','-proc:none','-classpath',os.pathsep.join(map(str,deps)),
                    '-d',str(classes),str(ROOT/'src/test/java/de/relics/DistributionFailureLogger.java')],check=True)
    with zipfile.ZipFile(run/'mods/failure-logger.jar','w') as z:
        for f in classes.rglob('*.class'):z.write(f,f.relative_to(classes).as_posix())
        z.writestr('fabric.mod.json',json.dumps({'schemaVersion':1,'id':'distribution-failure-logger','version':'1',
                    'environment':'server','entrypoints':{'main':['de.relics.DistributionFailureLogger']}}))
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    props={'server-ip':'127.0.0.1','server-port':port,'online-mode':'true','white-list':'true','enforce-whitelist':'true',
           'level-seed':audit['seed'],'level-name':'world','generate-structures':'true','view-distance':2,'simulation-distance':2,
           'pause-when-empty-seconds':0,'max-tick-time':60000}
    (run/'server.properties').write_text(''.join(f'{k}={v}\n' for k,v in props.items()))
    (run/'eula.txt').write_text('eula=true\n')
    jargs=['-Xms256M','-Xmx3G','-XX:ActiveProcessorCount=4','-Djava.awt.headless=true','-cp',os.pathsep.join(map(str,cp)),
           'net.fabricmc.loader.impl.launch.knot.KnotServer','nogui']
    argfile=run/'java-args.txt';argfile.write_text('\n'.join('"'+v.replace('\\','/')+'"' for v in jargs))
    process=subprocess.Popen([str(args.java_home/'bin/java.exe'),'@'+str(argfile)],cwd=run,stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,
                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    console=Console(process,run/'console.log',echo=False)
    evidence={'seed':audit['seed'],'site':site,'without_relic':args.vanilla,'production_artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),'commands':[]}
    if args.world_copy:evidence['copied_test_world']=str(args.world_copy)
    print('PROBE',run,'without_relic',args.vanilla,flush=True)
    try:
        console.wait(r'Done \(',timeout=180)
        if not args.vanilla and not args.world_copy:console.wait(r'Relic destination ',timeout=300)
        if copied_state:
            loaded=json.loads(json.loads((run/'world/data/relics_distribution_v1.json').read_text())['payload'])
            for key in ['policy','unique','spawnX','spawnZ','fingerprint']:
                assert loaded[key]==copied_state[key],key
            evidence['saved_policy_and_target_preserved']=True
        elif args.world_copy and not args.vanilla:
            assert not (run/'world/data/relics_distribution_v1.json').exists()
            assert any('preserving legacy relic placement' in line for line in console.lines)
            evidence['legacy_without_snapshot_preserved']=True
        for column in range(site['minX']//16,site['maxX']//16+1,8):
            end=min(column+7,site['maxX']//16)
            cmd=f'forceload add {column*16} {site["minZ"]//16*16} {end*16+15} {site["maxZ"]//16*16+15}'
            response=console.command(cmd,r'Marked|force.loaded|No chunks were marked',timeout=100)
            evidence['commands'].append({'command':cmd,'response':response})
        pending=[(x,z) for x in range(site['minX']//16,site['maxX']//16+1)
                 for z in range(site['minZ']//16,site['maxZ']//16+1)]
        deadline=time.monotonic()+180
        while pending:
            pending=[(x,z) for x,z in pending if 'Test passed' not in console.command(
                f'execute if loaded {x*16} 80 {z*16}',r'Test passed|Test failed')]
            if time.monotonic()>deadline:raise TimeoutError(f'{len(pending)} footprint chunks remain incomplete')
            if pending:time.sleep(.5)
        evidence['full_footprint_loaded']=True
        console.command('save-all flush',r'Saved the game')
        console.command('stop',r'Stopping the server');process.wait(timeout=120)
        evidence['completed']=True
    except Exception as error:
        evidence['completed']=False;evidence['failure']=str(error)
        print('PROBE_FAILURE',error,flush=True)
    finally:
        if process.poll() is None:
            try:process.stdin.write('stop\n');process.stdin.flush();process.wait(timeout=30)
            except Exception:process.terminate();process.wait(timeout=15)
        console.thread.join(timeout=5)
        evidence['exit_code']=process.returncode
        evidence['error_lines']=[line for line in console.lines if '/ERROR]' in line]
        (run/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
        print('PROBE_RESULT',json.dumps(evidence),flush=True)
    if not evidence['completed'] or evidence['error_lines'] or evidence['exit_code']!=0:
        raise SystemExit(1)


if __name__=='__main__':main()
