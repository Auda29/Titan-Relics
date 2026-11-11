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


def external_key_fetch_error(line):
    """Retain this unrelated network failure without disabling online authentication."""
    return '[Yggdrasil Key Fetcher/ERROR]' in line and 'Failed to request yggdrasil public key' in line


def game_error(line):
    return '/ERROR]' in line and not external_key_fetch_error(line)


class PortConsole(Console):
    """Fail immediately on loader/worldgen errors instead of waiting for a chunk timeout."""
    def wait(self,pattern,start=0,timeout=120):
        expression=re.compile(pattern);deadline=time.monotonic()+timeout
        with self.condition:
            while True:
                for line in self.lines[start:]:
                    if game_error(line):raise RuntimeError(line+'; see '+str(self.log_path))
                    if expression.search(line):return line
                if self.process.poll() is not None:raise RuntimeError('Server exited; see '+str(self.log_path))
                remaining=deadline-time.monotonic()
                if remaining<=0:raise TimeoutError('No response matching '+repr(pattern)+'; see '+str(self.log_path))
                self.condition.wait(min(.25,remaining))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--loader',default='fabric',choices=('fabric','neoforge'))
    parser.add_argument('--minecraft',default='1.21.1',choices=('1.21.1','1.21.11','26.2','26.3'))
    parser.add_argument('--java',type=Path,required=True)
    parser.add_argument('--artifact',type=Path,required=True)
    parser.add_argument('--accept-eula',action='store_true')
    parser.add_argument('--test-mod',type=Path)
    parser.add_argument('--command',action='append',default=[])
    parser.add_argument('--suite',action='store_true',help='Core, recipes, two-player rewards, aura, animals and restart')
    parser.add_argument('--distribution-preset',choices=('expedition','balanced','discovery','tower-only'),help='Exercise frozen new-world settings in an isolated server')
    parser.add_argument('--biome-mode',choices=('standard','landscapes','empty-colossus'),default='landscapes')
    parser.add_argument('--reload-preset',choices=('expedition','balanced','discovery','invalid'),help='Change installation defaults before reopening the same world')
    parser.add_argument('--historical-journal',action='store_true',help='Reopen an Expedition fixture as a pre-menu v2 world')
    parser.add_argument('--world-load-checks',action='store_true',help='Reject isolated invalid planning fixtures before any world file changes')
    args=parser.parse_args()
    if args.historical_journal and args.distribution_preset!='expedition':parser.error('Historical journal fixture requires Expedition')
    if not args.accept_eula:parser.error('Accept the Minecraft EULA for this isolated server')
    base=ROOT/'build/alpha5-ports-20261028'
    run=base/datetime.now().strftime(f'{args.loader}-{args.minecraft}-%H%M%S-%f')
    (run/'mods').mkdir(parents=True)
    artifact=args.artifact.resolve();shutil.copy2(artifact,run/'mods'/artifact.name)
    if args.test_mod:shutil.copy2(args.test_mod,run/'mods'/args.test_mod.name)
    if args.loader=='fabric':
        if args.minecraft in ('1.21.11','26.3'):
            from additional_port_runtime import fabric_classpath,dependency
            cp=fabric_classpath(args.minecraft)
            for key in ('fabric:fabric-api','fabric:lithostitched'):
                dep=dependency(args.minecraft,key);shutil.copy2(dep,run/'mods'/dep.name)
        elif args.minecraft=='26.2':
            from compile_worldgen import compile_libraries
            libraries=compile_libraries()
            for name in ('fabric-api-0.161.0+26.2.jar','lithostitched-1.8.0-fabric-26.2.jar'):
                shutil.copy2(ROOT/'build/worldgen-dependencies'/name,run/'mods'/name)
            cp=[p for p in libraries if p.name=='fabric-loader-0.19.5.jar' or any(v in {'libraries','loader-libraries','versions'} for v in p.parts)]
        else:
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
        if args.minecraft in ('1.21.11','26.3'):
            from additional_port_runtime import dependency as pinned_dependency
            dependency=pinned_dependency(args.minecraft,'neoforge:lithostitched')
        shutil.copy2(dependency,run/'mods'/dependency.name)
        launch=[*logger,*native,'nogui']
        (run/'native-launch.json').write_text(json.dumps({**evidence,**logging_evidence},indent=2),encoding='utf-8')
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    properties={'server-ip':'127.0.0.1','server-port':port,'online-mode':'true','white-list':'true','enforce-whitelist':'true',
                'level-seed':731204,'level-name':'world','view-distance':2,'simulation-distance':2,'max-tick-time':60000,'spawn-protection':0}
    if args.minecraft!='1.21.1':properties['pause-when-empty-seconds']=0
    (run/'server.properties').write_text(''.join(f'{k}={v}\n' for k,v in properties.items()),encoding='utf-8')
    (run/'eula.txt').write_text('eula=true\n',encoding='utf-8')
    def settings(preset):
        cell,distance,obelisks,region={'expedition':(5000,2000,15000,6000),'balanced':(3000,1200,9000,3600),
            'discovery':(2000,800,6000,2400),'tower-only':(2000,800,6000,2400)}[preset]
        families={} if args.biome_mode=='standard' or args.historical_journal else {name:dict(mode='LANDSCAPES',selected=[]) for name in ('colossus','obelisk','titan_skull','titan_skull_2','ruined_tower','small_colossus','world_tree')}
        if args.biome_mode=='empty-colossus':families={'colossus':dict(mode='CUSTOM',selected=[])}
        colossus=({'expedition':30000,'balanced':15000,'discovery':8000,'tower-only':8000} if args.historical_journal else {'expedition':15000,'balanced':8000,'discovery':4000,'tower-only':4000})[preset]
        return dict(cellSize=cell,minDistance=distance,obeliskDistance=obelisks,regionRadius=region,colossusMinDistance=colossus,generationRevision=1 if args.historical_journal else 3,biomes={'families':families},
                    outside=[0,0,0,10000,0,0] if preset=='tower-only' else ([3000,250,250,200,200,200] if args.historical_journal else [3000,1500,1500,200,200,200]),
                    inside=[0,0,0,10000,0,0] if preset=='tower-only' else ([3000,1500,1500,200,200,200] if args.historical_journal else [3000,2500,2500,200,200,200]))
    def defaults(preset):
        config=run/'config/relics-distribution.json';config.parent.mkdir(exist_ok=True)
        config.write_text('invalid-for-new-worlds' if preset=='invalid' else json.dumps({'format':1,'settings':settings(preset)}),encoding='utf-8')
    if args.distribution_preset:defaults(args.distribution_preset)
    frozen=None
    custom_site=None
    argfile=run/'args.txt'
    argfile.write_text('\n'.join('"'+v.replace('\\','/')+'"' for v in ['-Xms256M','-Xmx3G','-XX:ActiveProcessorCount=4','-Djava.awt.headless=true',*launch]),encoding='utf-8')
    report={'loader':args.loader,'minecraft':args.minecraft,'artifact':artifact.name,'artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),'passed':False,'iterations':[]}
    print('PORT_SERVER',run,flush=True)
    try:
        for iteration in range(2):
            if iteration and args.reload_preset:defaults(args.reload_preset)
            process=subprocess.Popen([str(args.java.resolve()),'@'+str(argfile)],cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            console=PortConsole(process,run/f'console-{iteration}.log',echo=False)
            try:
                console.wait(r'Done \(',timeout=600 if args.minecraft in ('1.21.11','26.3') else 240)
                if args.distribution_preset=='tower-only':
                    if custom_site is None:
                        for x,z in ((-4000,-4000),(-2000,0),(0,-2000),(0,0),(2000,0),(0,2000)):
                            reply=console.command(f'relicsdistribution plan {x} {z}',r'Relic plan .*:',timeout=180)
                            custom_site=json.loads(re.search(r'Relic plan .*?: (null|\{.*\})',reply).group(1))
                            if custom_site is not None:break
                        assert custom_site is not None and custom_site['asset']=='ruined_tower','Custom family ticket yielded no test site'
                    candidate=custom_site['candidate'];x,z=candidate['x'],candidate['z']
                    console.command(f'forceload add {x} {z}',r'Marked|force.loaded|already|No chunks',timeout=120)
                    deadline=time.monotonic()+120
                    while 'Test passed' not in console.command(f'execute if loaded {x} 70 {z}',r'Test passed|Test failed',timeout=30):
                        assert time.monotonic()<deadline;time.sleep(.25)
                results=[]
                commands=list(args.command)
                if args.suite:
                    console.command('gamerule '+('doMobSpawning' if args.minecraft=='1.21.1' else 'minecraft:spawn_mobs')+' true',r'Gamerule|Game rule|Incorrect|Unknown',timeout=30)
                    console.command('forceload add -32 -32 63 63',r'Marked|force.loaded|already|No chunks',timeout=120)
                    commands+=['relicsporttest','relicstreeauratest','relicspresentationtest'+(' reload' if iteration else '')]
                for command in commands:
                    reply=console.command(command,r'PORT_PASS|PORT_FAIL|PRESENTATION_(?:RELOAD_)?PASS|PRESENTATION_FAIL|TREE_AURA_PASS|TREE_AURA_FAIL',timeout=240)
                    assert '_FAIL' not in reply and '_PASS' in reply,reply
                    results.append(reply)
                if args.suite and iteration==0:
                    console.command('gamerule '+('doMobSpawning' if args.minecraft=='1.21.1' else 'minecraft:spawn_mobs')+' false',r'Gamerule|Game rule|Incorrect|Unknown',timeout=30)
                    console.command('time set day',r'Set .*time|time marker',timeout=30)
                    console.command('forceload add 4080 4080 4159 4127',r'Marked|force.loaded|already|No chunks',timeout=120)
                    for x in (4096,4112):
                        for z in (4096,4112):
                            deadline=time.monotonic()+120
                            while 'Test passed' not in console.command(f'execute if loaded {x} 159 {z}',r'Test passed|Test failed',timeout=30):
                                assert time.monotonic()<deadline;time.sleep(.25)
                    for command,pattern in [('fill 4096 159 4096 4127 159 4127 minecraft:grass_block',r'Successfully|No blocks'),
                            ('fill 4096 160 4096 4127 163 4127 minecraft:air',r'Successfully|No blocks'),
                            ('fillbiome 4096 144 4096 4127 176 4127 minecraft:plains',r'Successfully|[Bb]iome')]:console.command(command,pattern,timeout=60)
                    reply=console.command('relicstreeanimalstest',r'TREE_ANIMALS_PASS|TREE_ANIMALS_FAIL',timeout=240)
                    assert 'TREE_ANIMALS_PASS' in reply,reply
                    results.append(reply)
                if args.distribution_preset and iteration==0:
                    # The destination is selected asynchronously. Freeze a resolved
                    # baseline before testing that a restart preserves that choice.
                    deadline=time.monotonic()+600
                    while True:
                        path=run/'world/data/relics_distribution_v1.json'
                        if path.exists():
                            state=json.loads(json.loads(path.read_text())['payload'])
                            if state.get('unique') is not None or state.get('unavailable'):break
                        if process.poll() is not None:raise RuntimeError('Server exited before planning completed')
                        if time.monotonic()>deadline:raise TimeoutError('Initial relic destination did not resolve')
                        time.sleep(.25)
                console.command('save-all flush',r'Saved the game',timeout=120)
                console.command('stop',r'Stopping the server',timeout=60)
                process.wait(timeout=300 if args.minecraft in ('1.21.11','26.3') else 120);console.thread.join(timeout=5)
                errors=[line for line in console.lines if game_error(line) or 'Mixin apply' in line or 'Couldn\'t parse' in line]
                assert process.returncode==0 and not errors,errors
                report['iterations'].append({'restart':iteration>0,'commands':results,'exit_code':process.returncode,
                    'external_service_errors':[line for line in console.lines if external_key_fetch_error(line)]})
                if custom_site is not None:
                    from verify_world import AnvilWorld
                    candidate=custom_site['candidate'];chunk=AnvilWorld(run/'world').chunk(candidate['x']//16,candidate['z']//16)
                    start=chunk['structures']['starts'].get('relics:ruined_tower')
                    assert start and start.get('id')!='INVALID' and start.get('Children'),'Custom planned chunk has no natural structure start'
                    report['iterations'][-1]['custom_natural_start']={'site':custom_site,'start_id':start['id'],'pieces':len(start['Children'])}
                if args.distribution_preset:
                    envelope=json.loads((run/'world/data/relics_distribution_v1.json').read_text())
                    assert hashlib.sha256(envelope['payload'].encode()).hexdigest()==envelope['sha256']
                    snapshot=json.loads(envelope['payload'])
                    if args.biome_mode=='empty-colossus':assert snapshot['unavailable'] and snapshot.get('unique') is None,'Empty Colossus selection must resolve unavailable, never search forever'
                    historical=iteration and args.historical_journal
                    assert snapshot['policy']==('relics-distribution-v2-local64-r3072' if historical else 'relics-distribution-v3-settings' if args.historical_journal else 'relics-distribution-v5-colossus-search')
                    expected_settings=None if historical else settings(args.distribution_preset)
                    assert snapshot.get('settings')==expected_settings,('Saved settings differ',snapshot.get('settings'),expected_settings)
                    invariant={key:snapshot.get(key) for key in ('policy','settings','unique','fingerprint','spawnX','spawnZ')}
                    if iteration:assert invariant==frozen,'Reopen changed world settings or the unique destination'
                    frozen=invariant;report['iterations'][-1]['frozen_distribution']=invariant
                    if not iteration and args.historical_journal:
                        snapshot['policy']='relics-distribution-v2-local64-r3072';snapshot.pop('settings')
                        payload=json.dumps(snapshot,separators=(',',':'))
                        (run/'world/data/relics_distribution_v1.json').write_text(json.dumps(dict(version=1,payload=payload,sha256=hashlib.sha256(payload.encode()).hexdigest())),encoding='utf-8')
                        frozen={**invariant,'policy':snapshot['policy'],'settings':None}
            finally:
                if process.poll() is None:
                    diagnostic=args.java.resolve().with_name('jcmd')
                    if diagnostic.exists():
                        with (run/f'threads-{iteration}.log').open('w') as output:
                            try:subprocess.run([str(diagnostic),str(process.pid),'Thread.print'],stdout=output,stderr=subprocess.STDOUT,timeout=15)
                            except subprocess.TimeoutExpired:pass
                    try:process.stdin.write('stop\n');process.stdin.flush();process.wait(timeout=30)
                    except Exception:
                        process.terminate()
                        try:process.wait(timeout=15)
                        except subprocess.TimeoutExpired:process.kill();process.wait(timeout=15)
        if args.world_load_checks:
            import copy
            world=run/'world';journal=world/'data/relics_distribution_v1.json';original=journal.read_bytes()
            original_envelope=json.loads(original);original_state=json.loads(original_envelope['payload'])
            def hashes():
                return {p.relative_to(world).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in world.rglob('*') if p.is_file() and p.name!='session.lock'}
            report['world_load_checks']=[]
            border_file=world/('data/world_border.dat' if args.minecraft=='1.21.11' else 'dimensions/minecraft/overworld/data/minecraft/world_border.dat')
            border_original=border_file.read_bytes() if args.minecraft in ('1.21.11','26.3') else None
            try:
                for name,reason in [('fingerprint','unknown'),('seed','seed'),('border','border'),('enabled','structures'),('unfinished','unfinished'),('checksum','unknown')]+([('saved-border','border')] if border_original is not None else []):
                    state=copy.deepcopy(original_state)
                    if name=='fingerprint':state['fingerprint']='0'*64
                    elif name=='seed':state['seed']+=1
                    elif name=='border':state['minX']+=1
                    elif name=='enabled':state['enabled']=state['enabled'][1:]
                    elif name=='unfinished':state['frozen']=False;state['unique']=None
                    payload=json.dumps(state,separators=(',',':'))
                    envelope=dict(version=1,payload=payload,sha256='0'*64 if name=='checksum' else hashlib.sha256(payload.encode()).hexdigest())
                    if name=='saved-border':
                        import gzip,struct
                        raw=gzip.decompress(border_original);key=b'\x06\x00\x08center_x'
                        if raw.count(key)!=1:raise ValueError('Unexpected saved border codec')
                        offset=raw.index(key)+len(key)
                        raw=raw[:offset]+struct.pack('>d',1024.0)+raw[offset+8:]
                        border_file.write_bytes(gzip.compress(raw,mtime=0))
                    journal.write_text(json.dumps(envelope),encoding='utf-8');before=hashes()
                    process=subprocess.Popen([str(args.java.resolve()),'@'+str(argfile)],cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
                    console=Console(process,run/f'reject-{name}.log',echo=False)
                    try:
                        deadline=time.monotonic()+(300 if args.minecraft in ('1.21.11','26.3') else 180)
                        while process.poll() is None:
                            assert not any('Done (' in line for line in console.lines),'Rejected fixture started the server'
                            if time.monotonic()>deadline:raise TimeoutError('Rejected load did not return: '+name)
                            time.sleep(.1)
                        console.thread.join(timeout=5);text=''.join(console.lines)
                        assert 'Relic world load rejected before saving' in text and 'Reason='+reason in text,text[-3000:]
                        after=hashes();assert before==after,('Rejected load changed world files',name,[p for p in set(before)|set(after) if before.get(p)!=after.get(p)])
                        report['world_load_checks'].append(dict(case=name,reason=reason,world_file_count=len(before),all_world_files_unchanged=True,exit_code=process.returncode))
                    finally:
                        if process.poll() is None:process.terminate();process.wait(timeout=15)
                    journal.write_bytes(original)
                    if border_original is not None:border_file.write_bytes(border_original)
            finally:
                journal.write_bytes(original)
                if border_original is not None:border_file.write_bytes(border_original)
            process=subprocess.Popen([str(args.java.resolve()),'@'+str(argfile)],cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            console=PortConsole(process,run/'restored-world.log',echo=False)
            try:
                console.wait(r'Done \(',timeout=600 if args.minecraft in ('1.21.11','26.3') else 180);console.command('stop',r'Stopping the server',timeout=60)
                process.wait(timeout=300 if args.minecraft in ('1.21.11','26.3') else 120);console.thread.join(timeout=5)
                assert process.returncode==0 and journal.read_bytes()==original,'Restored world changed the frozen plan'
                report['world_load_restored']=dict(started=True,journal_byte_identical=True,exit_code=process.returncode)
            finally:
                if process.poll() is None:process.terminate();process.wait(timeout=15)
        report['passed']=True
        report['proofs']={p.name:p.read_text(encoding='utf-8') for p in run.glob('*proof.txt')}
    finally:(run/'evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True)


if __name__=='__main__':main()
