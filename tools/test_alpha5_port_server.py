"""Launch/restart isolated production Alpha 5 ports; never open launcher saves."""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import socket
import subprocess
import time
from smoke_server import Console,prepare_classpath

ROOT=Path(__file__).resolve().parents[1]


class PortConsole(Console):
    """Fail immediately on loader/worldgen errors instead of waiting for a chunk timeout."""
    def wait(self,pattern,start=0,timeout=120):
        expression=re.compile(pattern);deadline=time.monotonic()+timeout
        with self.condition:
            while True:
                for line in self.lines[start:]:
                    if '/ERROR]' in line:raise RuntimeError(line+'; see '+str(self.log_path))
                    if expression.search(line):return line
                if self.process.poll() is not None:raise RuntimeError('Server exited; see '+str(self.log_path))
                remaining=deadline-time.monotonic()
                if remaining<=0:raise TimeoutError('No response matching '+repr(pattern)+'; see '+str(self.log_path))
                self.condition.wait(min(.25,remaining))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--loader',default='fabric',choices=('fabric','neoforge'))
    parser.add_argument('--minecraft',default='1.21.1',choices=('1.21.1','26.2'))
    parser.add_argument('--java',type=Path,required=True)
    parser.add_argument('--artifact',type=Path,required=True)
    parser.add_argument('--accept-eula',action='store_true')
    parser.add_argument('--test-mod',type=Path)
    parser.add_argument('--command',action='append',default=[])
    parser.add_argument('--suite',action='store_true',help='Core, recipes, two-player rewards, aura, animals and restart')
    args=parser.parse_args()
    if not args.accept_eula:parser.error('Accept the Minecraft EULA for this isolated server')
    base=ROOT/'build/alpha5-ports-20261028'
    run=base/datetime.now().strftime(f'{args.loader}-{args.minecraft}-%H%M%S-%f')
    (run/'mods').mkdir(parents=True)
    artifact=args.artifact.resolve();shutil.copy2(artifact,run/'mods'/artifact.name)
    if args.test_mod:shutil.copy2(args.test_mod,run/'mods'/args.test_mod.name)
    if args.loader=='fabric':
        deps=ROOT/'build/compat-mc1.21.1/dependencies'
        for name in ('fabric-api-0.116.17+1.21.1.jar','lithostitched-1.8.0-fabric-21.1.jar'):
            shutil.copy2(deps/name,run/'mods'/name)
        cp=prepare_classpath(Path('E:/Roaming/ModrinthApp'),Path.home()/f'.gradle/caches/fabric-loom/{args.minecraft}/minecraft-server.jar',base/f'runtime-fabric-{args.minecraft}',args.minecraft)
        launch=['-cp',os.pathsep.join(map(str,cp)),'net.fabricmc.loader.impl.launch.knot.KnotServer','nogui']
    else:
        from alpha5_neoforge_runtime import installed_arguments,logging_arguments
        native_root=ROOT/f'build/neoforge/runtime-{args.minecraft}'
        native,evidence=installed_arguments(native_root,args.minecraft)
        logger,logging_evidence=logging_arguments(native_root,args.minecraft,run)
        dependency=ROOT/('build/neoforge/dependencies/lithostitched-1.8.0-neoforge-'+('21.1' if args.minecraft=='1.21.1' else '26.2')+'.jar')
        shutil.copy2(dependency,run/'mods'/dependency.name)
        launch=[*logger,*native,'nogui']
        (run/'native-launch.json').write_text(json.dumps({**evidence,**logging_evidence},indent=2),encoding='utf-8')
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    properties={'server-ip':'127.0.0.1','server-port':port,'online-mode':'true','white-list':'true','enforce-whitelist':'true',
                'level-seed':731204,'level-name':'world','view-distance':2,'simulation-distance':2,'max-tick-time':60000,'spawn-protection':0}
    (run/'server.properties').write_text(''.join(f'{k}={v}\n' for k,v in properties.items()),encoding='utf-8')
    (run/'eula.txt').write_text('eula=true\n',encoding='utf-8')
    argfile=run/'args.txt'
    argfile.write_text('\n'.join('"'+v.replace('\\','/')+'"' for v in ['-Xms256M','-Xmx3G','-XX:ActiveProcessorCount=4','-Djava.awt.headless=true',*launch]),encoding='utf-8')
    report={'loader':args.loader,'minecraft':args.minecraft,'artifact':artifact.name,'artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),'passed':False,'iterations':[]}
    print('PORT_SERVER',run,flush=True)
    try:
        for iteration in range(2):
            process=subprocess.Popen([str(args.java.resolve()),'@'+str(argfile)],cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            console=PortConsole(process,run/f'console-{iteration}.log',echo=False)
            try:
                console.wait(r'Done \(',timeout=240)
                results=[]
                commands=list(args.command)
                if args.suite:
                    console.command('gamerule doMobSpawning true',r'Gamerule|Incorrect|Unknown',timeout=30)
                    console.command('forceload add -32 -32 63 63',r'Marked|force.loaded|already|No chunks',timeout=120)
                    commands+=['relicsporttest','relicstreeauratest','relicspresentationtest'+(' reload' if iteration else '')]
                for command in commands:
                    reply=console.command(command,r'PORT_PASS|PORT_FAIL|PRESENTATION_(?:RELOAD_)?PASS|PRESENTATION_FAIL|TREE_AURA_PASS|TREE_AURA_FAIL',timeout=240)
                    assert '_FAIL' not in reply and '_PASS' in reply,reply
                    results.append(reply)
                if args.suite and iteration==0:
                    console.command('gamerule doMobSpawning false',r'Gamerule|Incorrect|Unknown',timeout=30)
                    console.command('time set day',r'Set .*time',timeout=30)
                    console.command('forceload add 4080 4080 4159 4127',r'Marked|force.loaded|already|No chunks',timeout=120)
                    for x in (4096,4112):
                        for z in (4096,4112):
                            deadline=time.monotonic()+120
                            while 'Test passed' not in console.command(f'execute if loaded {x} 159 {z}',r'Test passed|Test failed',timeout=30):
                                assert time.monotonic()<deadline;time.sleep(.25)
                    for command,pattern in [('fill 4096 159 4096 4127 159 4127 minecraft:grass_block',r'Successfully|No blocks'),
                            ('fill 4096 160 4096 4127 163 4127 minecraft:air',r'Successfully|No blocks'),
                            ('fillbiome 4096 144 4096 4127 176 4127 minecraft:plains',r'Successfully|biome')]:console.command(command,pattern,timeout=60)
                    reply=console.command('relicstreeanimalstest',r'TREE_ANIMALS_PASS|TREE_ANIMALS_FAIL',timeout=240)
                    assert 'TREE_ANIMALS_PASS' in reply,reply
                    results.append(reply)
                console.command('save-all flush',r'Saved the game',timeout=120)
                console.command('stop',r'Stopping the server',timeout=60)
                process.wait(timeout=120);console.thread.join(timeout=5)
                errors=[line for line in console.lines if '/ERROR]' in line or 'Mixin apply' in line or 'Couldn\'t parse' in line]
                assert process.returncode==0 and not errors,errors
                report['iterations'].append({'restart':iteration>0,'commands':results,'exit_code':process.returncode})
            finally:
                if process.poll() is None:
                    try:process.stdin.write('stop\n');process.stdin.flush();process.wait(timeout=30)
                    except Exception:process.terminate();process.wait(timeout=15)
        report['passed']=True
        report['proofs']={p.name:p.read_text(encoding='utf-8') for p in run.glob('*proof.txt')}
    finally:(run/'evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True)


if __name__=='__main__':main()
