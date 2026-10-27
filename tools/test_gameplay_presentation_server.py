"""Real Fabric reward ejection, personal pickup, restart and magnet motion with two packet-sink players."""
import argparse
from datetime import datetime
import hashlib,json,os,shutil,socket,subprocess,zipfile
from pathlib import Path
from compile_worldgen import ROOT,compile_libraries
from smoke_server import Console

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--accept-eula',action='store_true');p.add_argument('--java-home',type=Path,required=True);p.add_argument('--artifact',type=Path,required=True)
    a=p.parse_args()
    if not a.accept_eula:p.error('Accept Minecraft EULA for this isolated test with --accept-eula')
    artifact=a.artifact.resolve();java=a.java_home.resolve()/'bin';deps=compile_libraries()
    run=ROOT/'build/gameplay-feedback-20261027'/datetime.now().strftime('server-%H%M%S-%f');(run/'mods').mkdir(parents=True)
    classes=run/'test-classes';classes.mkdir()
    subprocess.run([str(java/'javac.exe'),'--release','25','-encoding','UTF-8','-proc:none','-classpath',os.pathsep.join(map(str,[artifact,*deps])),
        '-d',str(classes),str(ROOT/'src/test/java/de/relics/GameplayPresentationChecks.java')],check=True)
    with zipfile.ZipFile(run/'mods/presentation-checks.jar','w') as z:
        for f in classes.rglob('*.class'):z.write(f,f.relative_to(classes).as_posix())
        z.writestr('fabric.mod.json',json.dumps({'schemaVersion':1,'id':'relics-presentation-checks','version':'1','environment':'server','entrypoints':{'main':['de.relics.GameplayPresentationChecks']},'depends':{'relics':'*'}}))
    for f in [artifact,ROOT/'build/worldgen-dependencies/fabric-api-0.161.0+26.2.jar',ROOT/'build/worldgen-dependencies/lithostitched-1.8.0-fabric-26.2.jar']:shutil.copy2(f,run/'mods'/f.name)
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    props={'server-ip':'127.0.0.1','server-port':port,'online-mode':'true','white-list':'true','enforce-whitelist':'true','level-seed':731204,'level-name':'world','view-distance':2,'simulation-distance':2,'pause-when-empty-seconds':0,'max-tick-time':60000}
    (run/'server.properties').write_text(''.join(f'{k}={v}\n' for k,v in props.items()));(run/'eula.txt').write_text('eula=true\n')
    cp=[v for v in deps if v.name=='fabric-loader-0.19.5.jar' or any(s in {'libraries','loader-libraries','versions'} for s in v.parts)]
    argv=['-Xms256M','-Xmx3G','-XX:ActiveProcessorCount=4','-Djava.awt.headless=true','-cp',os.pathsep.join(map(str,cp)),'net.fabricmc.loader.impl.launch.knot.KnotServer','nogui']
    af=run/'args.txt';af.write_text('\n'.join('"'+v.replace('\\','/')+'"' for v in argv))
    report={'artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),'passed':False}
    print('PRESENTATION_SERVER',run,flush=True)
    for iteration in range(2):
        process=subprocess.Popen([str(java/'java.exe'),'@'+str(af)],cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        console=Console(process,run/f'console-{iteration}.log',echo=False)
        try:
            console.wait(r'Done \(',timeout=180)
            if iteration==0:
                console.command('forceload add -32 -32 63 63',r'Marked|force.loaded',timeout=180)
                response=console.command('relicspresentationtest',r'PRESENTATION_PASS|PRESENTATION_FAIL',timeout=180)
                assert 'PRESENTATION_PASS' in response,response
            else:
                response=console.command('relicspresentationtest reload',r'PRESENTATION_RELOAD_PASS|PRESENTATION_FAIL',timeout=180)
                assert 'PRESENTATION_RELOAD_PASS' in response,response
                report['restart_preserved_claims_and_timeline']=True
                report['restart_result']=response
                report['magnet_proof']=(run/'magnet-proof.txt').read_text()
            console.command('save-all flush',r'Saved the game');console.command('stop',r'Stopping the server');process.wait(timeout=120);console.thread.join(timeout=5)
            assert process.returncode==0 and not [l for l in console.lines if '/ERROR]' in l]
            report.update(passed=iteration==1,proof=(run/'presentation-proof.txt').read_text())
        finally:
            if process.poll() is None:
                try:process.stdin.write('stop\n');process.stdin.flush();process.wait(timeout=30)
                except Exception:process.terminate();process.wait(timeout=15)
            report['exit_code']=process.returncode
            (run/'evidence.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)

if __name__=='__main__':main()
