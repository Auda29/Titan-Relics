"""Compile a separate gameplay probe and run a copied, isolated accepted client fixture."""
import argparse, hashlib, json, os, shutil, subprocess, time, zipfile
from pathlib import Path
from datetime import datetime
from compile_worldgen import ROOT, compile_libraries

AUTHORIZED_SCRATCH = Path('E:/Relic_Mod_QA/renderer-20261104').resolve()
FIXTURES = {'fabric-1.21.1':'client-1.21.1-110010-680449', 'fabric-26.2':'client-26.2-105935-270526', 'neoforge-1.21.1':'neo-client-1.21.1-110000-535487', 'neoforge-26.2':'neo-client-26.2-110020-943280'}

def storage_guard(scratch):
    if shutil.disk_usage(ROOT).free < 64*1024**2:
        raise RuntimeError('System drive below 64 MiB reserve')
    if shutil.disk_usage(scratch).free < 2*1024**3:
        raise RuntimeError('Scratch drive below 2 GiB reserve')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--scratch-root', type=Path)
    ap.add_argument('--reuse-probe', type=Path)
    ap.add_argument('--fixture',type=Path,required=True)
    ap.add_argument('--loader',choices=['fabric','neoforge'],default='fabric')
    ap.add_argument('--port',type=int,default=25781)
    ap.add_argument('--visual-cases',type=Path)
    ap.add_argument('--late',action='store_true')
    ap.add_argument('--compile-only',action='store_true')
    ap.add_argument('--late-end',action='store_true')
    ap.add_argument('--solo',action='store_true')
    ap.add_argument('--verify',action='store_true')
    ap.add_argument('--encounter',action='store_true')
    ap.add_argument('--minecraft',choices=['26.2','1.21.1'],default='26.2')
    args=ap.parse_args(); fixture=args.fixture.resolve()
    mc=args.minecraft
    scratch=args.scratch_root.resolve() if args.scratch_root else ROOT/'build/beta-client-gameplay-20261104'
    if args.scratch_root and scratch != AUTHORIZED_SCRATCH:
        raise ValueError('Only the explicitly authorized E: scratch root is permitted')
    storage_guard(scratch if scratch.exists() else scratch.parent)
    allowed=ROOT/'build/beta-client-acceptance-20261104'/FIXTURES[args.loader+'-'+mc]
    if fixture != allowed.resolve():
        raise ValueError('Only the four accepted fresh source fixtures are permitted')
    java=Path('C:/Users/wecke/.gradle/jdks/eclipse_adoptium-25-amd64-windows.2/bin/java.exe')
    if mc=='1.21.1':java=Path('C:/Program Files/Java/jdk-21.0.10/bin/java.exe')
    run=scratch/datetime.now().strftime(args.loader+'-'+mc+'-%H%M%S-%f')
    run.mkdir(parents=True); sources=run/'sources';sources.mkdir()
    tmp=run/'tmp';tmp.mkdir()
    env=os.environ.copy();env.update(TMP=str(tmp),TEMP=str(tmp))
    for name in ['mods','saves','config','natives']:
        if (fixture/name).exists():shutil.copytree(fixture/name,run/name)
    if args.loader=='neoforge':
        config=run/'config';config.mkdir(exist_ok=True);fml=config/'fml.toml'
        previous=fml.read_text() if fml.exists() else ''
        fml.write_text('\n'.join(line for line in previous.splitlines() if not line.strip().startswith(('earlyWindowControl','versionCheck')))+'\nearlyWindowControl = false\nversionCheck = false\n')
    for name in ['options.txt','created-world.txt']:shutil.copy2(fixture/name,run/name)
    (run/'options.txt').write_text((run/'options.txt').read_text().replace('simulationDistance:2','simulationDistance:5')+'\npauseOnLostFocus:false\nsoundCategory_master:0.0\n')
    original=(ROOT/'src/test/client/de/relics/testmixin/BetaClientBootstrap.java').read_text().replace('BetaClientBootstrap','DistributionMenuChecks')
    if args.encounter:
        original=original.replace('if(relics$phase==21 &&', 'if(relics$phase==21){if(client.level==null && relics$ticks-relics$joined>100){client.stop();return;}de.relics.clientqa.BetaEncounterDriver.client(client);return;}\n if(relics$phase==210 &&')
    original=original.replace('relics$ticks%30','relics$ticks%5')
    original=original.replace('if(relics$phase==5 && Boolean.getBoolean', 'if(relics$phase==5){de.relics.clientqa.BetaGameplayDriver.tick(client);return;}\n if(relics$phase==50 && Boolean.getBoolean',1)
    probe_name='DistributionMenuChecks' if args.loader=='fabric' else 'WorldLoadClientChecks'
    original=original.replace('DistributionMenuChecks',probe_name)
    (sources/(probe_name+'.java')).write_text(original,encoding='utf-8')
    shutil.copy2(ROOT/'src/test/client/de/relics/testmixin/BetaGameplayDriver.java',sources/'BetaGameplayDriver.java')
    if mc=='1.21.1':
        from prepare_alpha5_port import legacy_client
        for source in sources.glob('*.java'):
            text=legacy_client(source.read_text()).replace('ContainerInput','ClickType').replace('handleClickType','handleInventoryMouseClick').replace('net.minecraft.resources.Identifier','net.minecraft.resources.ResourceLocation').replace('.ITEM.getValue(','.ITEM.get(').replace('Screenshot.grab(c,true)','Screenshot.grab(c.gameDirectory,c.getMainRenderTarget(),message->{})')
            source.write_text(text,encoding='utf-8')
    if args.encounter:
        shutil.copy2(ROOT/'src/test/client/de/relics/testmixin/BetaEncounterDriver.java',sources/'BetaEncounterDriver.java')
        if mc=='1.21.1':
            extra=sources/'BetaEncounterDriver.java';extra.write_text(legacy_client(extra.read_text()).replace('ContainerInput','ClickType').replace('handleClickType','handleInventoryMouseClick').replace('net.minecraft.world.entity.animal.golem.','net.minecraft.world.entity.animal.').replace('.setSelectedSlot(0)','.selected=0').replace('Screenshot.grab(c,true)','Screenshot.grab(c.gameDirectory,c.getMainRenderTarget(),message->{})'))
        if args.late:
            extra=sources/'BetaEncounterDriver.java';extra.write_text(extra.read_text().replace('if(s.getPlayerList().getPlayerCount()<2)return;','').replace('            client(c);','            if(s.getPlayerList().getPlayerCount()>=2)client(c);').replace('>=1200000','>=0').replace('long-session-proof.txt','late-event-proof.txt'))
        driver=sources/'BetaGameplayDriver.java';driver.write_text(driver.read_text().replace('c.stop();step++;','de.relics.clientqa.BetaEncounterDriver.tick(c);'))
    if args.verify:
        shutil.copy2(ROOT/'src/test/client/de/relics/testmixin/BetaPersistenceDriver.java',sources/'BetaPersistenceDriver.java')
        if mc=='1.21.1':
            extra=sources/'BetaPersistenceDriver.java';extra.write_text(extra.read_text().replace('c.level.disconnect(net.minecraft.network.chat.Component.literal("QA save/reload"))','c.level.disconnect()'))
        extra=sources/'BetaPersistenceDriver.java'
        if args.late_end:extra.write_text(extra.read_text().replace('BlockPos(x,239,z)','BlockPos(x,119,z)').replace('tp @a 0.5 240 0.5','tp @a 0.5 120 -2.5'))
        if args.solo:extra.write_text(extra.read_text().replace('getPlayerCount()<2','getPlayerCount()<1'))
        bootstrap=sources/(probe_name+'.java');bootstrap.write_text(bootstrap.read_text().replace('de.relics.clientqa.BetaGameplayDriver.tick(client)','de.relics.clientqa.BetaPersistenceDriver.tick(client)'))
    if args.visual_cases:
        shutil.copy2(args.visual_cases,run/'visual-cases.json')
        shutil.copy2(ROOT/'src/test/client/de/relics/testmixin/BetaVisualDriver.java',sources/'BetaVisualDriver.java')
        extra=sources/'BetaVisualDriver.java'
        if mc=='1.21.1':extra.write_text(legacy_client(extra.read_text()).replace('Screenshot.grab(c,true)','Screenshot.grab(c.gameDirectory,c.getMainRenderTarget(),message->{})'))
        bootstrap=sources/(probe_name+'.java');bootstrap.write_text(bootstrap.read_text().replace('de.relics.clientqa.BetaGameplayDriver.tick(client)','de.relics.clientqa.BetaVisualDriver.tick(client)'))
        opt=run/'options.txt';opt.write_text('\n'.join(line for line in opt.read_text().splitlines() if not line.startswith(('renderDistance:','fov:','renderClouds:','tutorialStep:','soundCategory_master:')))+'\nrenderDistance:32\nfov:0.0\ntutorialStep:none\nsoundCategory_master:0.0\nrenderClouds:'+('false' if mc=='1.21.1' else '"false"')+'\n')
    artifact=next(p for p in (run/'mods').glob('relics-*.jar') if 'menu' not in p.name)
    client=Path.home()/'.gradle/caches/fabric-loom/26.2/minecraft-client.jar'
    glfw=next(p for p in Path('E:/Roaming/ModrinthApp/meta/libraries/org/lwjgl/lwjgl-glfw').glob('*/lwjgl-glfw-*.jar') if 'natives' not in p.name)
    cp=os.pathsep.join(map(str,[artifact,client,glfw,*compile_libraries()]))
    if args.loader=='neoforge':cp=str(artifact)+os.pathsep+(ROOT/f'compat/alpha5-neoforge-{mc}/build/runtime-classpath.txt').read_text().strip()
    remapped=None
    if args.reuse_probe:
        reuse=args.reuse_probe.resolve()
        if not reuse.is_relative_to(ROOT/'build/beta-client-gameplay-20261104') and not reuse.is_relative_to(AUTHORIZED_SCRATCH):
            raise ValueError('Probe outside authorized QA sources')
        with zipfile.ZipFile(reuse) as z:
            if z.testzip() is not None:raise ValueError('Corrupt probe')
            remapped={n:z.read(n) for n in z.namelist() if n.endswith('.class')}
        if not any(n.endswith('BetaVisualDriver.class') for n in remapped):raise ValueError('Visual probe missing')
        # Reuse only when all generated Java sources match the prior compilation inputs.
        for source in sources.glob('*.java'):
            if source.read_bytes() != (reuse.parent.parent/'sources'/source.name).read_bytes():
                raise ValueError('Reused probe source mismatch: '+source.name)
    elif args.loader=='fabric' and mc=='1.21.1':
        # Compile only the probe against the existing named runtime; remap entirely on E:.
        bootstrap=sources/(probe_name+'.java')
        bootstrap.write_text(bootstrap.read_text().replace('@Inject(method="tick"','@Inject(method="method_1574"'))
        named_cp=(ROOT/'compat/alpha5-fabric-1.21.1/build/runtime-classpath.txt').read_text().strip()
        with (run/'compile.log').open('wb') as log:
            subprocess.run([str(java.with_name('javac.exe')),'-J-Djava.io.tmpdir='+str(tmp),'--release','21','-proc:none','-encoding','UTF-8','-cp',named_cp,'-d',str(sources),*map(str,sources.glob('*.java'))],stdout=log,stderr=subprocess.STDOUT,check=True,env=env)
        raw=run/'probe-named.jar';mapped=run/'probe-intermediary.jar'
        with zipfile.ZipFile(raw,'w') as z:
            for p in sources.rglob('*.class'):z.write(p,p.relative_to(sources).as_posix())
        modules=Path.home()/'.gradle/caches/modules-2/files-2.1'
        remapper_cp=[*modules.glob('net.fabricmc/tiny-remapper/0.14.0/*/*.jar'),*modules.glob('net.fabricmc/mapping-io/*/*/*.jar'),*modules.glob('org.ow2.asm/*/9.10.1/*/*.jar')]
        mappings=Path.home()/'.gradle/caches/fabric-loom/1.21.1/loom.mappings.1_21_1.layered+hash.2198-v2/mappings.tiny'
        with (run/'remap.log').open('wb') as log:
            subprocess.run([str(java),'-Djava.io.tmpdir='+str(tmp),'-cp',os.pathsep.join(map(str,remapper_cp)),'net.fabricmc.tinyremapper.Main',str(raw),str(mapped),str(mappings),'named','intermediary',*named_cp.split(os.pathsep)],stdout=log,stderr=subprocess.STDOUT,check=True,env=env)
        with zipfile.ZipFile(mapped) as z:remapped={n:z.read(n) for n in z.namelist() if n.endswith('.class')}
    else:
        with (run/'compile.log').open('wb') as log:
            subprocess.run([str(java.with_name('javac.exe')),'-J-Djava.io.tmpdir='+str(tmp),'--release','21' if mc=='1.21.1' else '25','-proc:none','-encoding','UTF-8','-cp',cp,'-d',str(sources),*map(str,sources.glob('*.java'))],stdout=log,stderr=subprocess.STDOUT,check=True,env=env)
    probe=run/('mods/menu-checks.jar' if args.loader=='fabric' else 'mods/load-checks.jar')
    with zipfile.ZipFile(probe) as z:entries={n:z.read(n) for n in z.namelist()}
    entries.update(remapped if remapped is not None else {p.relative_to(sources).as_posix():p.read_bytes() for p in sources.rglob('*.class')})
    with zipfile.ZipFile(probe,'w',zipfile.ZIP_DEFLATED) as z:
        for n,data in entries.items():z.writestr(n,data)
    launch=(fixture/'client-args.txt').read_text().replace(fixture.as_posix(),run.as_posix())
    for config in fixture.glob('*log*.xml'):shutil.copy2(config,run/config.name)
    if args.visual_cases:launch=launch.replace('"854"','"1280"').replace('"480"','"720"')
    launch='\n'.join(line for line in launch.splitlines() if '-Drelics.qa.port=' not in line and '-Djdk.net.hosts.file=' not in line)
    launch='\n'.join(line for line in launch.splitlines() if not line.startswith(chr(34)+'-Djava.io.tmpdir='))
    launch=chr(34)+'-Djava.io.tmpdir='+tmp.as_posix()+chr(34)+'\n'+launch
    # JVM-only hosts service: unknown service names cannot fall back to external DNS.
    # No operating-system hosts file, firewall or user profile is changed.
    (run/'loopback-hosts.txt').write_text('127.0.0.1 localhost\n::1 localhost\n')
    (run/'client-args.txt').write_text('"-Djdk.net.hosts.file='+str(run/'loopback-hosts.txt')+'"\n"-Drelics.qa.port='+str(args.port)+'"\n'+launch)
    if args.compile_only:
        print('COMPILED',run,flush=True);return
    record={'run':str(run),'started':time.time(),'artifact':str(artifact),'sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),'probe_sha256':hashlib.sha256(probe.read_bytes()).hexdigest(),'java_args':(run/'client-args.txt').read_text(),'command':[str(java),'@'+str(run/'client-args.txt')]}
    storage_guard(scratch)
    print(run,flush=True)
    with (run/'console.log').open('wb') as log:
        p=subprocess.Popen(record['command'],cwd=run,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW,env=env)
        record['pid']=p.pid
        try:
            deadline=time.time()+(1800 if args.encounter or args.visual_cases else 600)
            while p.poll() is None:
                storage_guard(scratch)
                if time.time()>deadline:raise TimeoutError('Client timeout')
                time.sleep(2)
            record['exit']=p.returncode
        finally:
            if p.poll() is None:p.terminate();p.wait(timeout=20)
            record['ended']=time.time();record['duration']=record['ended']-record['started']
            record['files']={str(q.relative_to(run)):hashlib.sha256(q.read_bytes()).hexdigest() for q in run.rglob('*') if q.is_file() and q.suffix in ('.log','.java','.jar','.png','.txt')}
            (run/'process.json').write_text(json.dumps(record,indent=2))
    assert record['exit']==0 and (run/('visual-proof.txt' if args.visual_cases else 'save-reload-proof.txt' if args.verify else 'late-event-proof.txt' if args.encounter and args.late else 'long-session-proof.txt' if args.encounter else 'gameplay-proof.txt')).exists(),run

if __name__=='__main__':main()
