"""Actual planned natural starts, full footprints, native loot and restart/non-refill."""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime
import gzip,hashlib,json,os,re,shutil,socket,subprocess,time,zipfile
from pathlib import Path
from compile_worldgen import ROOT,compile_libraries
from smoke_server import Console,read_nbt
from verify_world import AnvilWorld,verify_piece,transform,protected_cell,AIR_NAMES

def blocks_proof(world,artifact,sites):
    result=[];anvil=AnvilWorld(world)
    with zipfile.ZipFile(artifact) as archive:
        for site in sites:
            found=[]
            for chunk in anvil.chunks():
                start=chunk.get('structures',{}).get('starts',{}).get('relics:'+site['asset'])
                if start and start.get('id')!='INVALID':found.extend(ch for ch in start['Children']
                    if [ch['PosX'],ch['PosY'],ch['PosZ']]==[site['originX'],site['originY'],site['originZ']])
            assert len(found)==1,(site['asset'],len(found))
            child=found[0];location=child['pool_element']['location'].split(':')[1]
            from integrate_gameplay_interiors import MANIFESTS
            if 'relics_natural_site' in child:
                certificate=json.loads(child['relics_natural_site'])
                manifest=json.loads(archive.read(MANIFESTS[certificate['revision']]))
            else:
                assert site['asset']=='titan_skull_2','Missing natural gameplay certificate'
                manifest=json.loads(archive.read('relics.integration.json'))
            contract=next(a for a in manifest['structures'] if a['id']==site['asset'])
            assert location+'.nbt'==contract['worldgen_template']['path']
            expected=read_nbt(gzip.decompress(archive.read('data/relics/structure/'+location+'.nbt')))
            gameplay=contract.get('gameplay',{'offset':[8,contract['worldgen_template']['foundation']['vertical_padding'],8],'markers':[],'clearance_runs':[]})
            offset=gameplay['offset']
            injected={tuple(a+b for a,b in zip(m['pos'],offset)) for m in gameplay['markers'] if 'expected_block' in m}
            restored=[]
            for b in expected['blocks']:
                if tuple(b['pos']) in injected:continue # Verified as native initialized blocks by test mod.
                if expected['palette'][b['state']]['Name']=='minecraft:jigsaw':
                    final=b['nbt']['final_state']
                    if final=='minecraft:structure_void':continue
                    name,_,properties=final.partition('[');state={'Name':name}
                    if properties:state['Properties']=dict(p.split('=') for p in properties.rstrip(']').split(','))
                    expected['palette'].append(state);b={'pos':b['pos'],'state':len(expected['palette'])-1}
                restored.append(b)
            expected['blocks']=restored
            plants=[]
            if site['asset']=='world_tree':
                states={tuple(b['pos']):expected['palette'][b['state']]['Name'] for b in expected['blocks']}
                skip=set()
                for p,name in states.items():
                    below=(p[0],p[1]-1,p[2])
                    if name!='minecraft:firefly_bush' or states.get(below)!='minecraft:rooted_dirt':continue
                    skip.update((p,below));original=transform(p,child['rotation'],[child['PosX'],child['PosY'],child['PosZ']])
                    actual=[]
                    for y in range(original[1]-6,original[1]+7):
                        pos=(original[0],y,original[2]);base=(pos[0],y-1,pos[2])
                        if anvil.block(*pos)['Name']!='minecraft:firefly_bush' or anvil.block(*base)['Name']!='minecraft:rooted_dirt':continue
                        assert protected_cell(anvil.chunk(pos[0]//16,pos[2]//16),pos)
                        assert protected_cell(anvil.chunk(base[0]//16,base[2]//16),base)
                        bed=anvil.block(base[0],base[1]-1,base[2])['Name']
                        assert bed not in AIR_NAMES|{'minecraft:water','minecraft:lava'},('Floating bush socket',base,bed)
                        actual.append(list(pos))
                    assert len(actual)<=1,('Duplicated authored bush',original,actual)
                    plants.append({'source':list(original),'placed':actual[0] if actual else None,'within_vertical_limit':True})
                expected['blocks']=[b for b in expected['blocks'] if tuple(b['pos']) not in skip]
            # The general verifier predates multi-face blocks. Native lichen
            # rotation rotates the face keys as well as facing/axis values.
            turns={'NONE':0,'CLOCKWISE_90':1,'CLOCKWISE_180':2,'COUNTERCLOCKWISE_90':3}[child['rotation']]
            directions=['north','east','south','west']
            for state in expected['palette']:
                props=state.get('Properties',{})
                if state['Name']=='minecraft:glow_lichen':
                    old=dict(props)
                    for i,d in enumerate(directions):props[directions[(i+turns)%4]]=old[d]
            proof=verify_piece(anvil,'relics:'+site['asset'],child,expected)
            assert proof['passed'],proof
            clear=0;blocked=[];unprotected=[]
            for x,y,z0,z1 in gameplay['clearance_runs']:
                for z in range(z0,z1+1):
                    p=transform((x,y,z),child['rotation'],proof['origin']);clear+=1
                    if anvil.block(*p)['Name'] not in AIR_NAMES:blocked.append(list(p))
                    ch=anvil.chunk(p[0]//16,p[2]//16)
                    if not protected_cell(ch,p):unprotected.append(list(p))
            assert not blocked and not unprotected,(site['asset'],blocked[:12],unprotected[:12])
            proof.update(clearance_cells=clear,blocked_clearances=len(blocked),unprotected_clearances=len(unprotected))
            if site['asset']=='world_tree':proof['grounded_plants']=plants
            if site['asset']=='titan_skull_2' and contract['version']=='titan-skull-2-v2-embedded-side-v1':
                side=json.loads((ROOT/contract['source']).with_name('handoff.json').read_text());checked=0
                for cell in side['removed_cells']:
                    if cell['pos'][1]<contract['ground_y']-contract['buried_clip_depth']:continue
                    p=transform(tuple(v+o for v,o in zip(cell['pos'],contract['gameplay']['offset'])),child['rotation'],proof['origin'])
                    assert anvil.block(*p)['Name']!='minecraft:dripstone_block',('Removed chip remains',p)
                    checked+=1
                proof['removed_chip_cells_checked']=checked
            result.append(proof)
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--accept-eula',action='store_true');p.add_argument('--java-home',type=Path,required=True);p.add_argument('--artifact',type=Path,required=True)
    p.add_argument('--unavailable',action='store_true',help='Disable the large Colossus before world creation and verify archaeology compensation')
    p.add_argument('--resume',action='store_true',help='Restart after loading only the central chunks, then complete the saved pieces')
    p.add_argument('--peaceful',action='store_true',help='Verify tower initialization and restart without hostile entities on Peaceful')
    p.add_argument('--tower-only',action='store_true',help='Verify just the tower on Normal, including five initial Endermen')
    args=p.parse_args()
    if not args.accept_eula:p.error('Accept the Minecraft EULA for isolated tests with --accept-eula')
    artifact=args.artifact.resolve();deps=compile_libraries();cp=[p for p in deps if p.name=='fabric-loader-0.19.5.jar' or any(v in {'libraries','loader-libraries','versions'} for v in p.parts)]
    run=ROOT/'build/interior-integration-20261027'/datetime.now().strftime('native-%H%M%S-%f');run.mkdir(parents=True)
    classes=run/'test-classes';classes.mkdir()
    subprocess.run([str(args.java_home/'bin/javac.exe'),'--release','25','-encoding','UTF-8','-proc:none','-classpath',os.pathsep.join(map(str,[artifact,*deps])),
                    '-d',str(classes),str(ROOT/'src/test/java/de/relics/NaturalInteriorChecks.java')],check=True)
    testmod=run/'natural-interior-checks.jar'
    with zipfile.ZipFile(testmod,'w') as z:
        for f in classes.rglob('*.class'):z.write(f,f.relative_to(classes).as_posix())
        z.writestr('fabric.mod.json',json.dumps({'schemaVersion':1,'id':'relics-natural-interior-checks','version':'1','environment':'server',
            'entrypoints':{'main':['de.relics.NaturalInteriorChecks']},'depends':{'relics':'*','fabric-command-api-v2':'*'}}))
    baseline=json.loads((ROOT/'docs/testing/distribution-fix-20261027.json').read_text())
    cases={}
    for seed,asset in [(731204,'obelisk'),(-48291736,'small_colossus'),(20260913,'world_tree'),(4661570585687253657,'ruined_tower')]:
        row=next(r for r in baseline['seed_results'] if r['seed']==seed)
        cases[seed]=[next(s for s in row['sites'] if s['asset']==asset)]
    row=next(r for r in baseline['seed_results'] if r['seed']==731204)
    cases[731204].append(next(s for s in row['sites'] if s['asset']=='obelisk' and s['candidate']['rotation']==2))
    if args.peaceful or args.tower_only:cases={4661570585687253657:cases[4661570585687253657]}
    elif args.unavailable:cases={731204:cases[731204][:1]}
    elif args.resume:cases={731204:cases[731204]}
    report={'artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),'target_unavailable':args.unavailable,'partial_restart':args.resume,'peaceful':args.peaceful,'runs':[],'failures':[]}
    print('NATIVE_INTERIORS',run,flush=True)
    def check(seed,sites):
        root=run/str(seed);(root/'mods').mkdir(parents=True)
        if args.unavailable:
            from configure import settings_resources
            datapack=root/'world/datapacks/interior-unavailable';datapack.mkdir(parents=True)
            for name,content in settings_resources('normal',['colossus']).items():
                target=datapack/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(content)
        for f in [artifact,testmod,ROOT/'build/worldgen-dependencies/fabric-api-0.161.0+26.2.jar',ROOT/'build/worldgen-dependencies/lithostitched-1.8.0-fabric-26.2.jar']:shutil.copy2(f,root/'mods'/f.name)
        (root/'sites.json').write_text(json.dumps(sites))
        with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        props={'server-ip':'127.0.0.1','server-port':port,'online-mode':'true','white-list':'true','enforce-whitelist':'true','level-name':'world','level-seed':seed,
            'generate-structures':'true','view-distance':2,'simulation-distance':2,'pause-when-empty-seconds':0,'max-tick-time':60000,'difficulty':'peaceful'}
        # Normal difficulty retains ordinary naturally initialized Endermen.
        props['difficulty']='peaceful' if args.peaceful else 'normal'
        (root/'server.properties').write_text(''.join(f'{k}={v}\n' for k,v in props.items()));(root/'eula.txt').write_text('eula=true\n')
        argv=['-Xms256M','-Xmx3G','-XX:ActiveProcessorCount=4','-Djava.awt.headless=true','-Drelics.interior.testConfig='+str(root/'sites.json'),
              '-cp',os.pathsep.join(map(str,cp)),'net.fabricmc.loader.impl.launch.knot.KnotServer','nogui']
        af=root/'args.txt';af.write_text('\n'.join('"'+a.replace('\\','/')+'"' for a in argv))
        record={'seed':seed,'sites':sites,'commands':[]}
        for iteration in range(-1 if args.resume else 0,3):
            process=subprocess.Popen([str(args.java_home/'bin/java.exe'),'@'+str(af)],cwd=root,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            console=Console(process,root/f'console-{iteration}.log',echo=False)
            def command(cmd,pattern,timeout=180):
                response=console.command(cmd,pattern,timeout);record['commands'].append({'command':cmd,'response':response});return response
            try:
                console.wait(r'Done \(',timeout=180)
                command('gamerule minecraft:random_tick_speed 0',r'Gamerule random_tick_speed is now set to: 0')
                if iteration<=0:
                    if iteration==-1 or not args.resume:console.wait(r'Relic destination ',timeout=300)
                    if seed==731204 and not args.unavailable and (iteration==-1 or not args.resume):
                        status=command('relicsdistribution status',r'"snapshot"')
                        unique=json.loads(status[status.index('{'):])['snapshot']['unique']
                        assert unique['asset']=='colossus' and unique['candidate']['unique']
                        sites.append(unique)
                        (root/'sites.json').write_text(json.dumps(sites))
                    if iteration==-1:
                        for site in sites:
                            x,z=site['candidate']['x'],site['candidate']['z']
                            command(f'forceload add {x} {z}',r'Marked|force.loaded|No chunks')
                            deadline=time.monotonic()+180
                            while 'Test passed' not in command(f'execute if loaded {x} 80 {z}',r'Test passed|Test failed'):
                                assert time.monotonic()<deadline;time.sleep(.25)
                        command('save-all flush',r'Saved the game');command('stop',r'Stopping the server')
                        process.wait(timeout=120);console.thread.join(timeout=5)
                        assert process.returncode==0 and not [l for l in console.lines if '/ERROR]' in l]
                        partial=[]
                        for chunk in AnvilWorld(root/'world').chunks():
                            for name,start in chunk.get('structures',{}).get('starts',{}).items():
                                if name.startswith('relics:') and start.get('id')!='INVALID':
                                    for child in start['Children']:
                                        assert 'relics_natural_site' in child
                                        partial.append({'structure':name,'template':child['pool_element']['location'],'certificate':child['relics_natural_site']})
                        assert len(partial)==len(sites)
                        record['partial_saved_pieces']=partial
                        continue
                    for site in sites:
                        if site['asset']!='colossus':
                            response=command(f'relicsdistribution plan {site["candidate"]["x"]} {site["candidate"]["z"]}',r'Relic plan Cell')
                            planned=json.loads(response.split(': ',2)[-1]);assert planned==site,(planned,site)
                        for x in range(site['minX']//16,site['maxX']//16+1,8):
                            end=min(x+7,site['maxX']//16)
                            command(f'forceload add {x*16} {site["minZ"]//16*16} {end*16+15} {site["maxZ"]//16*16+15}',r'Marked|force.loaded|No chunks')
                    for site in sites:
                        for x in range(site['minX']//16,site['maxX']//16+1):
                            for z in range(site['minZ']//16,site['maxZ']//16+1):
                                deadline=time.monotonic()+180
                                while 'Test passed' not in command(f'execute if loaded {x*16} 80 {z*16}',r'Test passed|Test failed'):
                                    assert time.monotonic()<deadline;time.sleep(.25)
                deadline=time.monotonic()+60
                while True:
                    response=command('relicsinteriorstest verify',r'INTERIORS_PASS|INTERIORS_FAIL|INTERIORS_PENDING')
                    assert 'FAIL' not in response,response
                    if 'PASS' in response:break
                    assert time.monotonic()<deadline;time.sleep(.25)
                if iteration==1:
                    response=command('relicsinteriorstest mutate',r'INTERIORS_PASS|INTERIORS_FAIL');assert 'PASS' in response
                command('save-all flush',r'Saved the game');command('stop',r'Stopping the server');process.wait(timeout=120);console.thread.join(timeout=5)
                assert process.returncode==0 and not [l for l in console.lines if '/ERROR]' in l]
                if iteration==0:record['block_verification']=blocks_proof(root/'world',artifact,sites)
            finally:
                if process.poll() is None:
                    try:process.stdin.write('stop\n');process.stdin.flush();process.wait(timeout=30)
                    except Exception:process.terminate();process.wait(timeout=15)
        record['passed']=True;(root/'evidence.json').write_text(json.dumps(record,indent=2)+'\n')
        print('PASS native interiors',seed,[s['asset'] for s in sites],flush=True);return record
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures={pool.submit(check,s,sites):s for s,sites in cases.items()}
        for future in as_completed(futures):
            try:report['runs'].append(future.result())
            except Exception as error:report['failures'].append({'seed':futures[future],'error':repr(error)});print('FAIL',futures[future],repr(error),flush=True)
            (run/'evidence.json').write_text(json.dumps(report,indent=2)+'\n')
    print('EVIDENCE',run/'evidence.json',flush=True)
    if report['failures']:raise SystemExit(1)

if __name__=='__main__':main()
