"""Native selected-animal spawn hook and shared-cap proof on an isolated server."""
import argparse,hashlib,json,os,shutil,socket,subprocess,zipfile,time
from pathlib import Path
from datetime import datetime
from compile_worldgen import ROOT,compile_libraries
from smoke_server import Console

def main():
    p=argparse.ArgumentParser();p.add_argument('--accept-eula',action='store_true');p.add_argument('--java-home',type=Path,required=True);p.add_argument('--artifact',type=Path,required=True);a=p.parse_args()
    if not a.accept_eula:p.error('Accept EULA for the isolated Minecraft test')
    run=ROOT/'build/alpha5-release-20261028'/datetime.now().strftime('animals-%H%M%S-%f');(run/'mods').mkdir(parents=True)
    java=a.java_home.resolve()/'bin';artifact=a.artifact.resolve();deps=compile_libraries();classes=run/'classes';classes.mkdir()
    subprocess.run([str(java/('javac.exe' if os.name=='nt' else 'javac')),'--release','25','-encoding','UTF-8','-proc:none','-classpath',os.pathsep.join(map(str,[artifact,*deps])),'-d',str(classes),
        *[str(ROOT/'src/test/java/de/relics'/s) for s in ('TreeAnimalChecks.java','TreeAnimalProbeMixin.java')]],check=True)
    with zipfile.ZipFile(run/'mods/animal-checks.jar','w') as z:
        for f in classes.rglob('*.class'):z.write(f,f.relative_to(classes).as_posix())
        z.writestr('fabric.mod.json',json.dumps({'schemaVersion':1,'id':'tree-animal-checks','version':'1','environment':'server','mixins':['animal-probe.mixins.json'],'entrypoints':{'main':['de.relics.TreeAnimalChecks']},'depends':{'relics':'*'}}))
        z.writestr('animal-probe.mixins.json',json.dumps({'required':True,'package':'de.relics.testmixin','compatibilityLevel':'JAVA_25','mixins':['TreeAnimalProbeMixin'],'injectors':{'defaultRequire':1}}))
    for f in [artifact,ROOT/'build/worldgen-dependencies/fabric-api-0.161.0+26.2.jar',ROOT/'build/worldgen-dependencies/lithostitched-1.8.0-fabric-26.2.jar']:shutil.copy2(f,run/'mods'/f.name)
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    properties={'server-ip':'127.0.0.1','server-port':port,'online-mode':'true','white-list':'true','enforce-whitelist':'true','level-seed':731204,'level-name':'world','view-distance':2,'simulation-distance':2,'pause-when-empty-seconds':0,'max-tick-time':60000}
    (run/'server.properties').write_text(''.join(f'{k}={v}\n' for k,v in properties.items()));(run/'eula.txt').write_text('eula=true\n')
    cp=[d for d in deps if d.name=='fabric-loader-0.19.5.jar' or any(v in {'libraries','loader-libraries','versions'} for v in d.parts)]
    args=['-Xms256M','-Xmx3G','-XX:ActiveProcessorCount=4','-Djava.awt.headless=true','-cp',os.pathsep.join(map(str,cp)),'net.fabricmc.loader.impl.launch.knot.KnotServer','nogui']
    argfile=run/'args.txt';argfile.write_text('\n'.join('"'+v.replace('\\','/')+'"' for v in args))
    process=subprocess.Popen([str(java/('java.exe' if os.name=='nt' else 'java')),'@'+str(argfile)],cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0));console=Console(process,run/'console.log',echo=False)
    report={'artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),'passed':False};print('ANIMAL_SERVER',run,flush=True)
    try:
        console.wait(r'Done \(',timeout=180)
        for command,pattern in [('gamerule minecraft:spawn_mobs false',r'Gamerule|Incorrect|Unknown'),('time set day',r'Set .*time|time marker'),
                ('forceload add 4080 4080 4159 4127',r'Marked|force.loaded')]:
            console.command(command,pattern,timeout=180)
        for x in (4096,4112):
            for z in (4096,4112):
                deadline=time.monotonic()+120
                while 'Test passed' not in console.command(f'execute if loaded {x} 159 {z}',r'Test passed|Test failed',timeout=30):
                    assert time.monotonic()<deadline;time.sleep(.25)
        for command,pattern in [('fill 4096 159 4096 4127 159 4127 minecraft:grass_block',r'Successfully|No blocks'),
                ('fill 4096 160 4096 4127 163 4127 minecraft:air',r'Successfully|No blocks'),('fillbiome 4096 144 4096 4127 176 4127 minecraft:plains',r'Successfully|biome')]:
            console.command(command,pattern,timeout=60)
        reply=console.command('relicstreeanimalstest',r'TREE_ANIMALS_PASS|TREE_ANIMALS_FAIL',timeout=180);assert 'TREE_ANIMALS_PASS' in reply,reply
        report['proof']=(run/'tree-animal-proof.txt').read_text();report['passed']=True
        console.command('save-all flush',r'Saved the game');console.command('stop',r'Stopping the server');process.wait(timeout=120);console.thread.join(timeout=5)
        assert process.returncode==0 and not [line for line in console.lines if '/ERROR]' in line]
    finally:
        if process.poll() is None:
            try:process.stdin.write('stop\n');process.stdin.flush();process.wait(timeout=30)
            except Exception:process.terminate();process.wait(timeout=15)
        report['exit_code']=process.returncode;(run/'evidence.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)

if __name__=='__main__':main()
