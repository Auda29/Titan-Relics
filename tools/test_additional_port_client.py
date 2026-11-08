"""Open the additional Fabric/NeoForge clients and exercise the shared menus in an isolated display.

Downloads official hash-checked client libraries/assets; uses a dummy offline QA identity.
No launcher profiles, accounts or existing saves are read or changed.
"""
import argparse,concurrent.futures,json,os,shutil,subprocess,sys,time,zipfile
from datetime import datetime
from pathlib import Path
from additional_port_runtime import ROOT,TARGETS,client_assets,fabric_classpath
from setup_worldgen_build import checked_download,fetch
from prepare_additional_ports import port_java
from release_version import release_version

PROBE='''package de.relics.testmixin;
import de.relics.client.*;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.tabs.TabNavigationBar;
import net.minecraft.client.gui.screens.*;
import net.minecraft.client.gui.screens.worldselection.CreateWorldScreen;
import net.minecraft.network.chat.Component;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
@Mixin(Minecraft.class)
public abstract class PortClientSmoke {
    @Unique private int relics$ticks,relics$phase,relics$last;
    @Unique private void relics$press(Minecraft client,String key){
        String text=Component.translatable(key).getString();
        client.gui.screen().children().stream().filter(Button.class::isInstance).map(Button.class::cast)
            .filter(b->b.getMessage().getString().equals(text)).findFirst().orElseThrow().onPress(null);
    }
    @Inject(method="tick",at=@At("TAIL"))
    private void relics$smoke(CallbackInfo ci) {
        var client=(Minecraft)(Object)this;
        if(++relics$ticks>2400){System.out.println("CLIENT_SMOKE_FAIL timeout phase="+relics$phase);client.stop();return;}
        if(relics$ticks<100 || relics$ticks-relics$last<30 || client.getOverlay()!=null)return;
        var screen=client.gui.screen();
        try {
            if(relics$phase==0){
                if(!(screen instanceof TitleScreen))return;
                client.gui.setScreen(DistributionMenus.defaults(screen));relics$phase++;
            }else if(relics$phase==1){
                if(!(screen instanceof DistributionSettingsScreen))return;
                CreateWorldScreen.openFresh(client,()->client.gui.setScreen(new TitleScreen()));relics$phase++;
            }else if(relics$phase==2){
                if(!(screen instanceof CreateWorldScreen))return;
                screen.children().stream().filter(TabNavigationBar.class::isInstance).map(TabNavigationBar.class::cast)
                    .findFirst().orElseThrow().selectTab(1,false);
                relics$press(client,"relics.settings.world_button");relics$phase++;
            }else if(relics$phase==3){
                if(!(screen instanceof DistributionSettingsScreen))throw new AssertionError("World settings missing");
                for(int i=0;i<5;i++)relics$press(client,"relics.settings.next");
                relics$press(client,"relics.settings.biomes");relics$phase++;
            }else if(relics$phase==4){
                if(!(screen instanceof BiomeSettingsScreen))throw new AssertionError("Biome settings missing");
                java.nio.file.Files.writeString(java.nio.file.Path.of("client-smoke-proof.txt"),
                    "title=true\\ndefaults_render=true\\nworld_tab=true\\nworld_settings_render=true\\nbiome_settings_render=true\\n");
                System.out.println("CLIENT_SMOKE_PASS defaults/world/biome screens rendered");client.stop();relics$phase++;
            }
            relics$last=relics$ticks;
        }catch(Throwable error){error.printStackTrace();System.out.println("CLIENT_SMOKE_FAIL "+error);client.stop();}
    }
}
'''


def allowed(lib):
    rules=lib.get('rules',[])
    result=not rules
    for rule in rules:
        system=rule.get('os',{})
        if system.get('name','linux')!='linux' or system.get('arch','x86_64') not in ('x86_64','amd64'):continue
        if rule.get('features'):continue
        result=rule['action']=='allow'
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--loader',choices=('fabric','neoforge'),default='fabric')
    ap.add_argument('--minecraft',choices=tuple(TARGETS),required=True)
    ap.add_argument('--java-home',type=Path,required=True)
    ap.add_argument('--java',type=Path,required=True)
    ap.add_argument('--gradle',required=True)
    args=ap.parse_args();mc=args.minecraft;target=TARGETS[mc]
    cache=ROOT/'build/new-version-ports/client-cache';cache.mkdir(parents=True,exist_ok=True)
    meta=cache/f'{mc}.json';checked_download(target['mojang_metadata_url'],meta,'sha1',target['mojang_metadata_sha1'])
    data=json.loads(meta.read_text());libs=[];jobs=[]
    for lib in data['libraries']:
        if not allowed(lib):continue
        entry=lib['downloads']['artifact'];path=cache/'libraries'/entry['path'];libs.append(path)
        jobs.append((entry['url'],path,'sha1',entry['sha1']))
    assets=cache/'assets';index=data['assetIndex'];indexfile=assets/'indexes'/(index['id']+'.json')
    checked_download(index['url'],indexfile,'sha1',index['sha1'])
    for name,obj in json.loads(indexfile.read_text())['objects'].items():
        if name.startswith('minecraft/sounds/'):continue  # This muted UI-only smoke test does not exercise audio.
        sha=obj['hash'];jobs.append((f'https://resources.download.minecraft.net/{sha[:2]}/{sha}',assets/'objects'/sha[:2]/sha,'sha1',sha))
    def download(job):
        for attempt in range(3):
            try:checked_download(*job);return
            except Exception:
                if attempt==2:raise
                time.sleep(1+attempt)
    # Deduplicate shared object hashes before concurrent downloads.
    jobs=list({str(job[1]):job for job in jobs}.values())
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(download,jobs))
    client=client_assets(mc)
    native=None;native_root=ROOT/f'build/new-version-ports/neo-client-install-{mc}'
    if args.loader=='neoforge':
        version=target['neoforge'];native_file=native_root/f'versions/neoforge-{version}/neoforge-{version}.json'
        if not native_file.exists():
            (native_root/'versions'/mc).mkdir(parents=True,exist_ok=True)
            (native_root/'launcher_profiles.json').write_text('{"profiles":{}}')
            shutil.copy2(meta,native_root/'versions'/mc/(mc+'.json'))
            shutil.copy2(client,native_root/'versions'/mc/(mc+'.jar'))
            url=f'https://maven.neoforged.net/releases/net/neoforged/neoforge/{version}/neoforge-{version}-installer.jar'
            installer=ROOT/f'build/new-version-ports/neoforge-{version}-installer.jar'
            checked_download(url,installer,'sha256',fetch(url+'.sha256').decode().strip())
            subprocess.run([str(args.java.resolve()),'-jar',str(installer),'--installClient',str(native_root)],check=True)
        native=json.loads(native_file.read_text())
        def key(lib):
            parts=lib['name'].split(':');return tuple(parts[:2]+parts[3:])
        merged={key(lib):lib for lib in data['libraries'] if allowed(lib)}
        merged.update({key(lib):lib for lib in native['libraries'] if allowed(lib)})
        libs=[]
        for lib in merged.values():
            entry=lib['downloads']['artifact'];path=(native_root/'libraries'/entry['path']) if lib in native['libraries'] else cache/'libraries'/entry['path']
            checked_download(entry['url'],path,'sha1',entry['sha1']);libs.append(path)
    profile=ROOT/f'compat/alpha5-{args.loader}-{mc}'
    source=profile/'build/generated/test/de/relics/testmixin/PortClientSmoke.java';source.parent.mkdir(parents=True,exist_ok=True)
    probe=PROBE.replace('client.getOverlay()', 'client.gui.overlay()') if mc=='26.3' else PROBE
    source.write_text(port_java(source.name,probe,mc,test=True))
    env=os.environ.copy();env['JAVA_HOME']=str(args.java_home.resolve())
    if native:
        boot=source.parent/'NativeClientBoot.java'
        (profile/'build/classes/java/test/de/relics/testmixin/NativeClientBoot.class').unlink(missing_ok=True)
        boot.write_text('package de.relics.clientqa; @net.neoforged.fml.common.Mod(value="relics_port_checks",dist=net.neoforged.api.distmarker.Dist.CLIENT) public final class NativeClientBoot {}')
    task='remapPortTestJar' if mc=='1.21.11' and not native else 'portTestJar'
    subprocess.run([args.gradle,'--no-daemon',task],cwd=profile,env=env,check=True)
    testjar=profile/('build/libs/relics-alpha5-port-checks+mc1.21.11.jar' if mc=='1.21.11' else f'build/libs/relics-{release_version()}-port-tests-dev.jar')
    if native:testjar=profile/f'build/validation/relics-alpha5-port-checks+mc{mc}-neoforge.jar'
    run=ROOT/'build/new-version-ports'/datetime.now().strftime(f'client-{args.loader}-{mc}-%H%M%S-%f');(run/'mods').mkdir(parents=True)
    artifact=ROOT/f"dist/new-version-ports/relics-{release_version()}+mc{mc}{'-neoforge' if native else ''}.jar";shutil.copy2(artifact,run/'mods'/artifact.name)
    from additional_port_runtime import dependency
    for key in (['neoforge:lithostitched'] if native else ['fabric:fabric-api','fabric:lithostitched']):
        p=dependency(mc,key);shutil.copy2(p,run/'mods'/p.name)
    with zipfile.ZipFile(testjar) as original,zipfile.ZipFile(run/'mods/client-smoke.jar','w') as output:
        for n in original.namelist():
            if n.endswith(('PortClientSmoke.class','NativeClientBoot.class')):output.writestr(n,original.read(n))
        if native:
            output.writestr('META-INF/neoforge.mods.toml','modLoader="javafml"\nloaderVersion="[1,)"\nlicense="MIT"\n[[mods]]\nmodId="relics_port_checks"\nversion="1"\n[[mixins]]\nconfig="client-smoke.mixins.json"\n')
        else:output.writestr('fabric.mod.json',json.dumps({'schemaVersion':1,'id':'relics-client-smoke','version':'1','environment':'client','mixins':['client-smoke.mixins.json']}))
        output.writestr('client-smoke.mixins.json',json.dumps({'required':True,'package':'de.relics.testmixin','compatibilityLevel':'JAVA_'+str(target['java']),'client':['PortClientSmoke'],'injectors':{'defaultRequire':1}}))
    cp=[] if native else [p for p in fabric_classpath(mc) if 'loader-libraries' in p.parts or p.name.startswith('fabric-loader-') or p.name=='intermediary.jar']
    cp+=[client,*libs]
    (run/'options.txt').write_text('onboardAccessibility:false\nlang:en_us\nsoundCategory_master:0.0\nrenderDistance:2\n')
    jvm=[];main='net.fabricmc.loader.impl.launch.knot.KnotClient';extra=[]
    if native:
        from alpha5_neoforge_runtime import logging_arguments
        logger,_=logging_arguments(native_root,mc,run)
        jvm=[arg.replace('${library_directory}',str(native_root/'libraries')) for arg in native['arguments']['jvm']]+logger
        main=native['mainClass'];extra=native['arguments']['game']
        (run/'config').mkdir();(run/'config/fml.toml').write_text('earlyWindowControl=false\nversionCheck=false\n')
    cmd=['xvfb-run','-a',str(args.java.resolve()),'-Xmx2G','-XX:ActiveProcessorCount=3',*jvm,'-cp',os.pathsep.join(map(str,cp)),
         main,*extra,'--username','RelicQA','--version',mc,'--gameDir',str(run),
         '--assetsDir',str(assets),'--assetIndex',index['id'],'--uuid','00000000000000000000000000000001','--accessToken','0','--width','960','--height','640']
    print('CLIENT_RUN',run,flush=True)
    with (run/'console.log').open('w') as log:result=subprocess.run(cmd,cwd=run,stdout=log,stderr=subprocess.STDOUT,timeout=600)
    text=(run/'console.log').read_text()
    if result.returncode or 'CLIENT_SMOKE_PASS' not in text or 'CLIENT_SMOKE_FAIL' in text:raise RuntimeError('Client probe failed: '+str(run/'console.log'))
    print('CLIENT_SMOKE_PASS',args.loader,mc,run,flush=True)


if __name__=='__main__':main()
