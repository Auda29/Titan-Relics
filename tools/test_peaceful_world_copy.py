"""Reproduce a Peaceful tower crash on a copy, then verify the fixed JAR twice.

Original save/profile stay read-only. Only the explicitly provided output copy
is launched, first with the old JAR, then fixed on Peaceful and on Normal reload.
"""
import argparse
from datetime import datetime
import hashlib,json,os,shutil,socket,subprocess,zipfile
from pathlib import Path
from compile_worldgen import ROOT,compile_libraries
from smoke_server import Console

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--accept-eula',action='store_true');p.add_argument('--world',type=Path,required=True)
    p.add_argument('--artifact',type=Path,required=True);p.add_argument('--previous-artifact',type=Path,required=True)
    p.add_argument('--tower-records',type=Path,required=True);p.add_argument('--java-home',type=Path,required=True)
    a=p.parse_args()
    if not a.accept_eula:p.error('Accept Minecraft EULA for the isolated world copy with --accept-eula')
    source=a.world.resolve();run=ROOT/'build/magnet-small-landmarks-20261028/crash-fix'/datetime.now().strftime('copy-%H%M%S-%f')
    run.mkdir(parents=True);world=run/'world';assert not world.exists() and source!=world.resolve()
    files={f.relative_to(source).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in source.rglob('*') if f.is_file()}
    shutil.copytree(source,world)
    assert all(hashlib.sha256((world/f).read_bytes()).hexdigest()==h for f,h in files.items())
    (run/'source-hashes.json').write_text(json.dumps(files,indent=2)+'\n')
    rows=json.loads(a.tower_records.read_text());assert len(rows)==1;target=rows[0];bounds=target['bounds']
    (run/'target-certificate.json').write_text(json.dumps(target['certificate']))
    deps=compile_libraries();java=a.java_home.resolve()/'bin';classes=run/'classes';classes.mkdir();(run/'mods').mkdir()
    subprocess.run([str(java/'javac.exe'),'--release','25','-encoding','UTF-8','-proc:none','-classpath',os.pathsep.join(map(str,[a.artifact.resolve(),*deps])),
        '-d',str(classes),str(ROOT/'src/test/java/de/relics/PeacefulLoadChecks.java')],check=True)
    with zipfile.ZipFile(run/'mods/peaceful-checks.jar','w') as z:
        for f in classes.rglob('*.class'):z.write(f,f.relative_to(classes).as_posix())
        z.writestr('fabric.mod.json',json.dumps({'schemaVersion':1,'id':'relics-peaceful-checks','version':'1','environment':'server','entrypoints':{'main':['de.relics.PeacefulLoadChecks']},'depends':{'relics':'*'}}))
    for f in [ROOT/'build/worldgen-dependencies/fabric-api-0.161.0+26.2.jar',ROOT/'build/worldgen-dependencies/lithostitched-1.8.0-fabric-26.2.jar']:shutil.copy2(f,run/'mods'/f.name)
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    props={'server-ip':'127.0.0.1','server-port':port,'online-mode':'true','white-list':'true','enforce-whitelist':'true','level-name':'world',
        'view-distance':2,'simulation-distance':2,'pause-when-empty-seconds':0,'max-tick-time':60000,'difficulty':'peaceful'}
    (run/'server.properties').write_text(''.join(f'{k}={v}\n' for k,v in props.items()));(run/'eula.txt').write_text('eula=true\n')
    cp=[v for v in deps if v.name=='fabric-loader-0.19.5.jar' or any(s in {'libraries','loader-libraries','versions'} for s in v.parts)]
    argv=['-Xms256M','-Xmx3G','-XX:ActiveProcessorCount=4','-Djava.awt.headless=true','-cp',os.pathsep.join(map(str,cp)),'net.fabricmc.loader.impl.launch.knot.KnotServer','nogui']
    af=run/'args.txt';af.write_text('\n'.join('"'+v.replace('\\','/')+'"' for v in argv))
    report={'artifact_sha256':hashlib.sha256(a.artifact.read_bytes()).hexdigest(),'source_save':str(source),'source_files':len(files),'passed':False,'boots':[]}
    print('WORLD_COPY',run,flush=True)
    try:
        for iteration in range(3):
            shutil.copy2(a.previous_artifact if iteration==0 else a.artifact,run/'mods/relics.jar')
            process=subprocess.Popen([str(java/'java.exe'),'@'+str(af)],cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            console=Console(process,run/f'console-{iteration}.log',echo=False)
            try:
                console.wait(r'Done \(',timeout=180)
                if iteration==0:
                    try:console.command(f'forceload add {bounds[0]} {bounds[2]} {bounds[3]} {bounds[5]}',r'Marked|force.loaded|No chunks',timeout=180)
                    except RuntimeError:pass
                    response=console.wait(r'Cannot create natural Enderman',timeout=180)
                    process.wait(timeout=120);console.thread.join(timeout=5)
                    report['boots'].append({'old_crash_reproduced':True,'message':response})
                else:
                    if iteration==2:console.command('difficulty normal',r'The difficulty has been set to|The difficulty did not change')
                    response=console.command('relicspeacefulcheck'+(' reload' if iteration==2 else ''),r'PEACEFUL_LOAD_PASS|PEACEFUL_RELOAD_PASS|PEACEFUL_LOAD_FAIL',timeout=180)
                    assert 'FAIL' not in response,response
                    console.command('save-all flush',r'Saved the game');console.command('stop',r'Stopping the server');process.wait(timeout=120);console.thread.join(timeout=5)
                    assert process.returncode==0 and not [line for line in console.lines if '/ERROR]' in line]
                    report['boots'].append({'fixed':True,'reloaded':iteration==2,'response':response})
            finally:
                if process.poll() is None:
                    try:process.stdin.write('stop\n');process.stdin.flush();process.wait(timeout=30)
                    except Exception:process.terminate();process.wait(timeout=15)
            (run/'evidence.json').write_text(json.dumps(report,indent=2)+'\n')
        report['passed']=True
    finally:
        unchanged=all((source/f).exists() and hashlib.sha256((source/f).read_bytes()).hexdigest()==h for f,h in files.items())
        report['source_files_unchanged']=unchanged
        (run/'evidence.json').write_text(json.dumps(report,indent=2)+'\n')
        assert unchanged,'Original save changed while testing its copy'
    print(json.dumps(report),flush=True)

if __name__=='__main__':main()
