"""Real-client menu checks in an isolated game directory; launcher profiles stay read-only.

Requires a matching local Modrinth asset/library cache. No account tokens or
existing saves are used. Diagnostic classes are kept out of all player JARs.
"""
from __future__ import annotations
import argparse,json,os,shutil,subprocess,zipfile
from datetime import datetime
from pathlib import Path
from compile_worldgen import ROOT,compile_libraries,find_javac
from prepare_alpha5_port import legacy_client
from build_mc1211 import find_gradle


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--minecraft',choices=('1.21.1','26.2'),required=True)
    parser.add_argument('--artifact',type=Path,required=True)
    parser.add_argument('--java-home',type=Path,required=True)
    parser.add_argument('--java',type=Path,required=True)
    parser.add_argument('--cache',type=Path,default=Path('E:/Roaming/ModrinthApp/meta'))
    parser.add_argument('--language',choices=('de_de','en_us'),default='de_de')
    parser.add_argument('--with-modmenu',action='store_true')
    parser.add_argument('--world-load-world',type=Path,help='Copy this isolated test world, reject two altered-journal loads, then restore and load it')
    parser.add_argument('--modpack-dir',type=Path,help='Read-only source of mods/config/defaultconfigs/moonlight datapacks for a copied client fixture')
    args=parser.parse_args();artifact=args.artifact.resolve();meta=args.cache.resolve()
    run=ROOT/'build/distribution-settings-20261030'/datetime.now().strftime('client-'+args.minecraft+'-%H%M%S-%f')
    (run/'mods').mkdir(parents=True);sources=run/'sources';sources.mkdir()
    if args.modpack_dir:
        for path in (args.modpack_dir/'mods').glob('*.jar'):
            if not path.name.startswith('relics-') and path.name!='fingerprint-capture.jar':shutil.copy2(path,run/'mods'/path.name)
        for name in ('config','defaultconfigs','moonlight-global-data-pack'):
            if (args.modpack_dir/name).is_dir():shutil.copytree(args.modpack_dir/name,run/name)
    probe_name='WorldLoadClientChecks' if args.world_load_world else 'DistributionMenuChecks'
    probe=ROOT/f'src/test/client/de/relics/testmixin/{probe_name}.java'
    if args.world_load_world:
        world=run/'saves/guard-world';shutil.copytree(args.world_load_world.resolve(),world)
        journal=world/'data/relics_distribution_v1.json';original=journal.read_bytes();(run/'original-journal.json').write_bytes(original)
        envelope=json.loads(original);state=json.loads(envelope['payload'])
        if not state.get('frozen') or not (state.get('unique') or state.get('unavailable')):raise ValueError('Provide a frozen, resolved isolated test world')
        import hashlib
        state['fingerprint']='0'*64;envelope['payload']=json.dumps(state,separators=(',',':'))
        envelope['sha256']=hashlib.sha256(envelope['payload'].encode()).hexdigest();journal.write_text(json.dumps(envelope),encoding='utf-8')
    hidden=ROOT/'compat/alpha5-fabric-1.21.1/src/test/adapters/de/relics/testmixin/HiddenFingerprintWindow.java'
    if args.minecraft=='1.21.1':
        project=ROOT/'compat/alpha5-fabric-1.21.1'
        target=project/f'build/generated/test/de/relics/testmixin/{probe_name}.java'
        target.parent.mkdir(parents=True,exist_ok=True);target.write_text(legacy_client(probe.read_text()),encoding='utf-8')
        if args.world_load_world:
            extra=ROOT/'src/test/client/de/relics/testmixin/WorldLoadCancelProbe.java'
            (target.parent/extra.name).write_text(legacy_client(extra.read_text()),encoding='utf-8')
        env=os.environ.copy();env['JAVA_HOME']=str(args.java_home.resolve())
        with (run/'probe-build.log').open('wb') as log:
            subprocess.run([find_gradle(None),'--no-daemon','remapPortTestJar'],cwd=project,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
        with zipfile.ZipFile(project/'build/libs/relics-alpha5-port-checks+mc1.21.1.jar') as jar:
            entries={n:jar.read(n) for n in jar.namelist() if n.endswith((probe_name+'.class','HiddenFingerprintWindow.class',*(['WorldLoadCancelProbe.class'] if args.world_load_world else [])))}
        deps=ROOT/'build/compat-mc1.21.1/dependencies'
        dependencies=[deps/'fabric-api-0.116.17+1.21.1.jar',deps/'lithostitched-1.8.0-fabric-21.1.jar']
    else:
        shutil.copy2(probe,sources/probe.name)
        if args.world_load_world:shutil.copy2(ROOT/'src/test/client/de/relics/testmixin/WorldLoadCancelProbe.java',sources/'WorldLoadCancelProbe.java')
        hidden_text=hidden.read_text().replace('import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;', 'import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;')
        hidden_text=hidden_text.replace('@Inject(method="<init>",at=@At(value="INVOKE",target="Lorg/lwjgl/glfw/GLFW;glfwCreateWindow(IILjava/lang/CharSequence;JJ)J"))', '@Inject(method="createGlfwWindow",at=@At("HEAD"))')
        hidden_text=hidden_text.replace('private void relics$hidden(CallbackInfo ci)', 'private static void relics$hidden(CallbackInfoReturnable<Long> ci)')
        (sources/hidden.name).write_text(hidden_text,encoding='utf-8')
        client=Path.home()/'.gradle/caches/fabric-loom/26.2/minecraft-client.jar'
        if not client.exists():client=ROOT/'build/worldgen-dependencies/minecraft-client.jar'
        version=args.minecraft+'-0.19.5';metadata=json.loads((meta/'versions'/version/(version+'.json')).read_text())
        glfw=next(lib for lib in metadata['libraries'] if lib['name'].startswith('org.lwjgl:lwjgl-glfw:') and len(lib['name'].split(':'))==3)
        glfw=meta/'libraries/org/lwjgl/lwjgl-glfw'/glfw['name'].split(':')[2]/('lwjgl-glfw-'+glfw['name'].split(':')[2]+'.jar')
        command=[str(find_javac(args.java_home)),'--release','25','-encoding','UTF-8','-proc:none','-classpath',
                 os.pathsep.join(map(str,[artifact,client,glfw,ROOT/'build/worldgen-dependencies/modmenu-api.jar',*compile_libraries()])),'-d',str(sources),*map(str,sources.glob('*.java'))]
        subprocess.run(command,check=True)
        entries={p.relative_to(sources).as_posix():p.read_bytes() for p in sources.rglob('*.class')}
        deps=ROOT/'build/worldgen-dependencies'
        dependencies=[deps/'fabric-api-0.161.0+26.2.jar',deps/'lithostitched-1.8.0-fabric-26.2.jar']
    entries['fabric.mod.json']=json.dumps({'schemaVersion':1,'id':'relics-menu-checks','version':'1','environment':'client',
                                         'mixins':['menu-checks.mixins.json'],'depends':{'relics':'*'}}).encode()
    entries['menu-checks.mixins.json']=json.dumps({'required':True,'package':'de.relics.testmixin',
        'compatibilityLevel':'JAVA_'+('21' if args.minecraft=='1.21.1' else '25'),
        'client':[probe_name,'HiddenFingerprintWindow',*(['WorldLoadCancelProbe'] if args.world_load_world else [])],'injectors':{'defaultRequire':1}}).encode()
    with zipfile.ZipFile(run/'mods/menu-checks.jar','w',zipfile.ZIP_DEFLATED) as out:
        for name,data in entries.items():out.writestr(name,data)
    for path in [artifact,*dependencies]:shutil.copy2(path,run/'mods'/path.name)
    if args.with_modmenu:
        import urllib.request,hashlib
        version='11.0.3' if args.minecraft=='1.21.1' else '20.0.3'
        menu=json.load(urllib.request.urlopen('https://api.modrinth.com/v2/project/modmenu/version/'+version))
        file=next(f for f in menu['files'] if f['primary']);data=urllib.request.urlopen(file['url']).read()
        assert hashlib.sha512(data).hexdigest()==file['hashes']['sha512'];(run/'mods/modmenu.jar').write_bytes(data)
    (run/'options.txt').write_text(f'lang:{args.language}\nguiScale:2\nonboardAccessibility:false\nstartedCleanly:true\nrenderDistance:2\nsimulationDistance:2\nsoundCategory_master:0.0\n',encoding='utf-8')
    version=args.minecraft+'-0.19.5';metadata=json.loads((meta/'versions'/version/(version+'.json')).read_text())
    cp=[]
    for lib in metadata['libraries']:
        allowed=not lib.get('rules')
        for rule in lib.get('rules',[]):
            osrule=rule.get('os',{});matches=osrule.get('name','windows')=='windows' and osrule.get('arch','amd64') in ('amd64','x86_64')
            if matches:allowed=rule['action']=='allow'
        if not allowed:continue
        download=lib.get('downloads',{}).get('artifact')
        if download:path=meta/'libraries'/download['path']
        else:
            group,name,v,*classifier=lib['name'].split(':')
            path=meta/'libraries'/group.replace('.','/')/name/v/(name+'-'+v+('-'+classifier[0] if classifier else '')+'.jar')
        if not path.is_file():raise FileNotFoundError(path)
        cp.append(path)
    cp.append(meta/'versions'/version/(version+'.jar'))
    natives=run/'natives';natives.mkdir()
    command=['-Xms256M','-Xmx3G','-XX:ActiveProcessorCount=4','-Drelics.menuChecks=true','-Drelics.capturePlanningFingerprint=true',
             '-Djava.library.path='+str(natives),'-Dorg.lwjgl.system.SharedLibraryExtractPath='+str(natives),'-Djna.tmpdir='+str(natives),
             '-Dminecraft.launcher.brand=RelicMenuChecks','-Dminecraft.launcher.version=1','-cp',os.pathsep.join(map(str,cp)),metadata['mainClass'],
             '--username','RelicMenuProbe','--uuid','00000000000000000000000000000001','--accessToken','0','--userType','legacy',
             '--version',version,'--gameDir',str(run),'--assetsDir',str(meta/'assets'),'--assetIndex',metadata['assetIndex']['id'],
             '--width','854','--height','480']
    if args.with_modmenu:command.insert(0,'-Drelics.menuChecks.modmenu=true')
    if args.world_load_world:command.insert(0,'-Drelics.worldLoadChecks=true')
    if args.modpack_dir:command[command.index('-Xmx3G')]='-Xmx5G'
    argfile=run/'client-args.txt';argfile.write_text('\n'.join('"'+v.replace('\\','/')+'"' for v in command),encoding='utf-8')
    print('MENU_CLIENT',run,flush=True)
    with (run/'client-console.log').open('wb') as log:
        process=subprocess.Popen([str(args.java.resolve()),'@'+str(argfile)],cwd=run,stdout=log,stderr=subprocess.STDOUT,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        try:code=process.wait(timeout=300)
        finally:
            if process.poll() is None:process.terminate();process.wait(timeout=20)
    proof=run/('world-load-proof.txt' if args.world_load_world else 'menu-proof.txt')
    if code or not proof.exists():raise AssertionError('Menu check failed; see '+str(run/'client-console.log'))
    print(proof.read_text(),flush=True)


if __name__=='__main__':main()
