"""Serial Fabric 26.2 tower summit generation, loot and restart/non-refill proof.

Requires cached dependencies and explicit EULA acceptance. Never opens a player save.
"""
import argparse,json,hashlib,os,re,shutil,socket,subprocess,sys,time,zipfile
from datetime import datetime
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'tools'))
from compile_worldgen import compile_libraries
from smoke_server import Console
from test_surface_structure_server import stop,journal
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--accept-eula',action='store_true');parser.add_argument('--artifact',type=Path,required=True);parser.add_argument('--java-home',type=Path,required=True);parser.add_argument('--output',type=Path,default=root/'build/tower-summit-native'/datetime.now().strftime('%Y%m%d-%H%M%S'));parser.add_argument('--seed',type=int,default=-4443928181842649648)
args=parser.parse_args()
if not args.accept_eula:parser.error('Explicitly accept https://aka.ms/MinecraftEULA with --accept-eula for this isolated test')
run=args.output.resolve()
if run.exists() and any(run.iterdir()):parser.error('Use an empty output directory; existing files and worlds are never reused')
(run/'mods').mkdir(parents=True,exist_ok=True)
jar=args.artifact.resolve();java=args.java_home.resolve()/'bin/java'
with zipfile.ZipFile(jar) as archive:assert json.loads(archive.read('fabric.mod.json'))['depends']['minecraft']=='26.2','This native test requires Fabric 26.2'
deps=compile_libraries();classes=run/'test-classes';classes.mkdir(exist_ok=True)
subprocess.run([str(java.with_name('javac')),'--release','25','-encoding','UTF-8','-proc:none','-cp',os.pathsep.join(map(str,[jar,*deps])),'-d',str(classes),str(root/'src/test/java/de/relics/NaturalInteriorChecks.java')],check=True)
with zipfile.ZipFile(run/'mods/natural-checks.jar','w') as out:
 for p in classes.rglob('*.class'):out.write(p,p.relative_to(classes).as_posix())
 out.writestr('fabric.mod.json',json.dumps({'schemaVersion':1,'id':'relics_tower_checks','version':'1','environment':'server','entrypoints':{'main':['de.relics.NaturalInteriorChecks']},'depends':{'relics':'*'}}))
shutil.copy2(jar,run/'mods'/jar.name)
for name in ['fabric-api-0.161.0+26.2.jar','lithostitched-1.8.0-fabric-26.2.jar']:shutil.copy2(root/'build/worldgen-dependencies'/name,run/'mods'/name)
cp=[p for p in deps if p.name=='fabric-loader-0.19.5.jar' or any(v in {'libraries','loader-libraries','versions'} for v in p.parts)]
world=run/'world';(world/'data').mkdir(parents=True,exist_ok=True)
families={name:{'mode':'LANDSCAPES','selected':[]} for name in ['colossus','obelisk','titan_skull','titan_skull_2','ruined_tower','small_colossus','world_tree']}
settings={'format':1,'settings':{'cellSize':2000,'minDistance':800,'obeliskDistance':6000,'regionRadius':2400,'colossusMinDistance':4000,'generationRevision':3,'outside':[3000,1500,1500,200,200,200],'inside':[3000,2500,2500,200,200,200],'biomes':{'families':families}}}
(world/'data/relics_creation_settings.json').write_text(json.dumps(settings))
(run/'eula.txt').write_text('eula=true\n');config=run/'sites.json';config.write_text('[]\n')
evidence={'minecraft':'26.2','seed':args.seed,'artifact_sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'passes':[]};site=None
for iteration in range(3):
 with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
 props={'server-ip':'127.0.0.1','server-port':port,'online-mode':'true','white-list':'true','enforce-whitelist':'true','max-players':1,'level-name':'world','level-seed':evidence['seed'],'generate-structures':'true','gamemode':'creative','difficulty':'peaceful','view-distance':2,'simulation-distance':2,'max-tick-time':120000,'pause-when-empty-seconds':0}
 (run/'server.properties').write_text(''.join(f'{k}={v}\n' for k,v in props.items()))
 before=journal(world)[0] if (world/'data/relics_distribution_v1.json').exists() else None
 args=[str(java),'-Xms256M','-Xmx2300M','-XX:ActiveProcessorCount=1','-Djava.awt.headless=true','-Drelics.interior.testConfig='+str(config),'-cp',os.pathsep.join(map(str,cp)),'net.fabricmc.loader.impl.launch.knot.KnotServer','nogui']
 print('START',iteration,flush=True);start=time.monotonic();proc=subprocess.Popen(args,cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1,start_new_session=True);console=Console(proc,run/f'console-{iteration}.log',echo=False)
 try:
  console.wait(r'Done \(',timeout=240)
  console.command('gamerule minecraft:random_tick_speed 0',r'Gamerule.*0')
  if iteration==0:
   line=console.command('locate structure relics:ruined_tower',r'\[-?\d+, ~, -?\d+\]',timeout=420);m=re.search(r'\[(-?\d+), ~, (-?\d+)\]',line);assert m,line
   plan=console.command(f'relicsdistribution plan {m[1]} {m[2]}',r'Relic plan .*: \{',timeout=180);site=json.loads(plan[plan.index(': {')+2:]);assert site['asset']=='ruined_tower';config.write_text(json.dumps([site]));evidence['site']=site
   print('LOCATED',site['candidate']['x'],site['candidate']['z'],'rotation',site['candidate']['rotation'],flush=True)
  console.command(f"forceload add {site['minX']} {site['minZ']} {site['maxX']} {site['maxZ']}",r'Marked|force.loaded|No chunks')
  deadline=time.monotonic()+300
  while True:
   line=console.command('relicsinteriorstest verify',r'INTERIORS_PASS|INTERIORS_PENDING|INTERIORS_FAIL',timeout=180)
   assert 'FAIL' not in line,line
   if 'PASS' in line:break
   if time.monotonic()>deadline:raise TimeoutError('Natural actions did not initialize')
   time.sleep(.5)
  proof=run/('native-after-restart.json' if iteration==2 else 'native-initial.json');shutil.copy2(proof,run/f'proof-{iteration}.json')
  if iteration==1:
   line=console.command('relicsinteriorstest mutate',r'INTERIORS_PASS|INTERIORS_FAIL',timeout=120);assert 'PASS' in line,line
  console.command('save-all flush',r'Saved the game',timeout=90)
 finally:stop(proc,console)
 assert proc.returncode==0,(iteration,proc.returncode)
 errors=[x for x in console.lines if '/ERROR]' in x];assert not errors,errors[:3]
 raw,state=journal(world);assert state['interiors']=='interiors-20261111-v6'
 if before is not None:assert before==raw,'Frozen journal changed on reload'
 evidence['passes'].append({'iteration':iteration,'seconds':round(time.monotonic()-start,2),'java_exit_code':proc.returncode,'journal_sha256':hashlib.sha256(raw).hexdigest(),'proof':json.loads((run/f'proof-{iteration}.json').read_text())});(run/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print('PASS',iteration,flush=True)
assert evidence['passes'][0]['proof']==evidence['passes'][1]['proof'],'Untouched loot changed after reload'
evidence['assertions']=['natural planned tower','two native chests with correct marker facing and free lids','guaranteed Feather Falling IV, 3-6 diamonds, 8-16 iron','lower Ender reward retained','untouched loot stable on reload','removed chests not recreated on second reload','frozen journal byte-identical','all Java exits zero without ERROR log entries']
(run/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print('TOWER_SUMMIT_NATIVE_PASS',flush=True)
