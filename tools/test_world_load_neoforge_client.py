"""Run the real NeoForge client load guard in a copied test world, without launcher accounts."""
from __future__ import annotations
import argparse,hashlib,json,os,re,shutil,subprocess,zipfile
from datetime import datetime
from pathlib import Path
from compile_worldgen import ROOT,find_javac
from prepare_alpha5_port import legacy_client
from prepare_alpha5_neoforge import TARGETS


def allowed(item):
    if not isinstance(item,dict) or not item.get('rules'):return True
    result=False
    for rule in item['rules']:
        osrule=rule.get('os',{});features=rule.get('features',{})
        matches=osrule.get('name','windows')=='windows' and osrule.get('arch','amd64') in ('amd64','x86_64')
        matches=matches and all(bool(value)==(key=='has_custom_resolution') for key,value in features.items())
        if matches:result=rule['action']=='allow'
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--minecraft',choices=TARGETS,required=True)
    parser.add_argument('--artifact',type=Path,required=True)
    parser.add_argument('--world',type=Path,required=True,help='An isolated NeoForge world with a frozen, resolved plan')
    parser.add_argument('--java-home',type=Path,required=True)
    parser.add_argument('--client-install',type=Path,help='Isolated NeoForge client installation, required for 26.2')
    parser.add_argument('--cache',type=Path,default=Path('E:/Roaming/ModrinthApp/meta'))
    args=parser.parse_args();mc=args.minecraft;meta=args.cache.resolve();target=TARGETS[mc]
    run=ROOT/'build/beta-load-guard'/datetime.now().strftime('neo-client-'+mc+'-%H%M%S-%f')
    (run/'mods').mkdir(parents=True);sources=run/'sources';sources.mkdir()
    world=run/'saves/guard-world';shutil.copytree(args.world.resolve(),world)
    journal=world/'data/relics_distribution_v1.json';original=journal.read_bytes();(run/'original-journal.json').write_bytes(original)
    envelope=json.loads(original);state=json.loads(envelope['payload'])
    if not state.get('frozen') or not (state.get('unique') or state.get('unavailable')):raise ValueError('World must have a resolved frozen plan')
    state['fingerprint']='0'*64;envelope['payload']=json.dumps(state,separators=(',',':'))
    envelope['sha256']=hashlib.sha256(envelope['payload'].encode()).hexdigest();journal.write_text(json.dumps(envelope),encoding='utf-8')
    text=(ROOT/'src/test/client/de/relics/testmixin/WorldLoadClientChecks.java').read_text()
    if mc=='1.21.1':text=legacy_client(text)
    (sources/'WorldLoadClientChecks.java').write_text(text,encoding='utf-8')
    shutil.copy2(ROOT/'src/test/client/de/relics/testmixin/WorldLoadCancelProbe.java',sources/'WorldLoadCancelProbe.java')
    hidden=(ROOT/'compat/alpha5-fabric-1.21.1/src/test/adapters/de/relics/testmixin/HiddenFingerprintWindow.java').read_text()
    if mc=='1.21.1':
        hidden=hidden.replace('Lorg/lwjgl/glfw/GLFW;glfwCreateWindow(IILjava/lang/CharSequence;JJ)J','Lnet/neoforged/fml/loading/ImmediateWindowHandler;setupMinecraftWindow(Ljava/util/function/IntSupplier;Ljava/util/function/IntSupplier;Ljava/util/function/Supplier;Ljava/util/function/LongSupplier;)J')
    if mc=='26.2':
        hidden=hidden.replace('import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;', 'import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;')
        hidden=hidden.replace('@Inject(method="<init>",at=@At(value="INVOKE",target="Lorg/lwjgl/glfw/GLFW;glfwCreateWindow(IILjava/lang/CharSequence;JJ)J"))','@Inject(method="createGlfwWindow",at=@At("HEAD"))')
        hidden=hidden.replace('private void relics$hidden(CallbackInfo ci)','private static void relics$hidden(CallbackInfoReturnable<Long> ci)')
    (sources/'HiddenFingerprintWindow.java').write_text(hidden,encoding='utf-8')
    (sources/'LoadTestBootstrap.java').write_text('package de.relics.loadprobe; @net.neoforged.fml.common.Mod("relics_load_checks") public final class LoadTestBootstrap { public LoadTestBootstrap() {} }',encoding='utf-8')
    cp=(ROOT/f'compat/alpha5-neoforge-{mc}/build/runtime-classpath.txt').read_text().strip()
    with (run/'compile.log').open('wb') as log:
        subprocess.run([str(find_javac(args.java_home)),'--release',str(target['java']),'-encoding','UTF-8','-proc:none','-classpath',os.pathsep.join([str(args.artifact.resolve()),cp]),'-d',str(sources),*map(str,sources.glob('*.java'))],stdout=log,stderr=subprocess.STDOUT,check=True)
    with zipfile.ZipFile(run/'mods/load-checks.jar','w',zipfile.ZIP_DEFLATED) as archive:
        for p in sources.rglob('*.class'):archive.write(p,p.relative_to(sources).as_posix())
        archive.writestr('META-INF/neoforge.mods.toml','''modLoader="javafml"
loaderVersion="[1,)"
license="MIT"
[[mods]]
modId="relics_load_checks"
version="1"
displayName="Isolated load checks"
[[mixins]]
config="load-checks.mixins.json"
''')
        archive.writestr('load-checks.mixins.json',json.dumps({'required':True,'package':'de.relics.testmixin','compatibilityLevel':'JAVA_'+str(target['java']),'client':['WorldLoadClientChecks','HiddenFingerprintWindow','WorldLoadCancelProbe'],'injectors':dict(defaultRequire=1)}))
    artifact=args.artifact.resolve();shutil.copy2(artifact,run/'mods'/artifact.name)
    dependency=ROOT/f'build/neoforge/dependencies/lithostitched-1.8.0-neoforge-{target["litho"]}.jar'
    shutil.copy2(dependency,run/'mods'/dependency.name)
    (run/'options.txt').write_text('lang:de_de\nguiScale:2\nonboardAccessibility:false\nstartedCleanly:true\nrenderDistance:2\nsimulationDistance:2\n',encoding='utf-8')
    (run/'config').mkdir();(run/'config/fml.toml').write_text('earlyWindowControl = false\nversionCheck = false\n',encoding='utf-8')
    if mc=='1.21.1':
        version=mc+'-'+target['neo'];metadata=json.loads((meta/'versions'/version/(version+'.json')).read_text());libraries=meta/'libraries'
        clientjar=meta/'versions'/version/(version+'.jar')
    else:
        if not args.client_install:parser.error('--client-install is required for 26.2')
        install=args.client_install.resolve();version='neoforge-'+target['neo'];libraries=install/'libraries'
        metadata=json.loads((install/'versions'/mc/(mc+'.json')).read_text());child=json.loads((install/'versions'/version/(version+'.json')).read_text())
        for kind in ('jvm','game'):metadata['arguments'][kind]+=child['arguments'][kind]
        combined={}
        for lib in metadata['libraries']+child['libraries']:
            group,name,v,*classifier=lib['name'].split(':');combined[(group,name,tuple(classifier))]=lib
        metadata['libraries']=list(combined.values());metadata['mainClass']=child['mainClass'];clientjar=install/'versions'/mc/(mc+'.jar')
    classpath=[]
    for lib in metadata['libraries']:
        if not allowed(lib):continue
        download=lib.get('downloads',{}).get('artifact')
        if download:path=libraries/download['path']
        else:
            group,name,v,*classifier=lib['name'].split(':');path=libraries/group.replace('.','/')/name/v/(name+'-'+v+('-'+classifier[0] if classifier else '')+'.jar')
        if not path.exists() and libraries!=meta/'libraries':
            cached=meta/'libraries'/path.relative_to(libraries)
            if cached.exists():path=cached
        if not path.exists():raise FileNotFoundError(path)
        if download and download.get('sha1') and hashlib.sha1(path.read_bytes()).hexdigest()!=download['sha1']:raise ValueError('Client library checksum mismatch: '+str(path))
        classpath.append(path)
    classpath=list(dict.fromkeys([*classpath,clientjar]));natives=run/'natives';natives.mkdir()
    values=dict(natives_directory=str(natives),launcher_name='RelicLoadChecks',launcher_version='1',classpath=os.pathsep.join(map(str,classpath)),classpath_separator=os.pathsep,
                library_directory=str(libraries),auth_player_name='RelicLoadProbe',version_name=version,game_directory=str(run),assets_root=str(meta/'assets'),assets_index_name=metadata['assetIndex']['id'],
                auth_uuid='00000000000000000000000000000001',auth_access_token='0',clientid='0',auth_xuid='0',user_type='legacy',version_type='release',resolution_width='854',resolution_height='480')
    def expand(items):
        result=[]
        for item in items:
            if not allowed(item):continue
            value=item.get('value') if isinstance(item,dict) else item
            for raw in value if isinstance(value,list) else [value]:
                def substitute(match):
                    if match[1] not in values:raise ValueError('Unreviewed launcher placeholder: '+match[1])
                    return values[match[1]]
                result.append(re.sub(r'\$\{([^}]+)\}',substitute,raw))
        return result
    from alpha5_neoforge_runtime import logging_arguments
    logger,_=logging_arguments(ROOT/f'build/neoforge/runtime-{mc}',mc,run)
    command=['-Xms256M','-Xmx3G','-XX:ActiveProcessorCount=4','-Drelics.worldLoadChecks=true','-Drelics.capturePlanningFingerprint=true',*logger,*expand(metadata['arguments']['jvm']),metadata['mainClass'],*expand(metadata['arguments']['game'])]
    argfile=run/'client-args.txt';argfile.write_text('\n'.join('"'+v.replace('\\','/')+'"' for v in command),encoding='utf-8')
    print('NEO_LOAD_CLIENT',run,flush=True)
    with (run/'console.log').open('wb') as log:
        process=subprocess.Popen([str(find_javac(args.java_home).with_name('java.exe')),'@'+str(argfile)],cwd=run,stdout=log,stderr=subprocess.STDOUT,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        try:code=process.wait(timeout=300)
        finally:
            if process.poll() is None:process.terminate();process.wait(timeout=20)
    proof=run/'world-load-proof.txt'
    if code or not proof.exists():raise AssertionError('NeoForge client load check failed; see '+str(run/'console.log'))
    evidence=dict(loader='neoforge',minecraft=mc,neoforge=target['neo'],artifact_sha256=hashlib.sha256(artifact.read_bytes()).hexdigest(),passed=True,proof=proof.read_text())
    (run/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8');print(json.dumps(evidence),flush=True)


if __name__=='__main__':main()
