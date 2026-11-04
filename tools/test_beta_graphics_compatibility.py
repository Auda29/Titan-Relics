"""Fresh, muted modpack clients in E: scratch, with explicit graphics variants."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import zipfile

from beta_qa_runtime import compile_sources
from test_beta_performance import SCRATCH, ROOT, ARTIFACTS, JAVA, cached_mods, sha, guard, write


def run_client(profile, variant, restart_from=None):
    guard();mc='26.2' if profile=='TerraVista' else '1.21.1'
    source_profile=Path('E:/Roaming/ModrinthApp/profiles')/profile
    fixture=ROOT/'build/beta-client-acceptance-20261104'/('client-26.2-105935-270526' if mc=='26.2' else 'client-1.21.1-110010-680449')
    run=SCRATCH/'clients'/datetime.now().strftime(profile.replace(' ','-')+'-'+variant+'-%H%M%S')
    (run/'mods').mkdir(parents=True);(run/'tmp').mkdir()
    excluded=[]
    for p in cached_mods(mc,'fabric',profile).glob('*.jar'):
        if (variant=='no-voxy' and p.name.startswith(('voxy-','Voxy World Gen V2-')) or
            variant in ['no-bridge','no-shader-no-bridge','no-seasons'] and p.name.startswith('ssdh-') or
            variant=='no-seasons' and p.name.startswith('SereneSeasons-')):
            excluded.append(p.name);continue
        os.link(p,run/'mods'/p.name)
    for n in ['config','defaultconfigs','moonlight-global-data-pack']:
        if (source_profile/n).is_dir():shutil.copytree(source_profile/n,run/n)
    if restart_from:
        previous=Path(restart_from).resolve()
        if not previous.is_relative_to((SCRATCH/'clients').resolve()):raise ValueError('Only an owned graphics fixture may be restarted')
        prior=json.loads((previous/'result.json').read_text())
        if prior['profile']!=profile or prior['variant']!=variant or not prior.get('passed'):raise ValueError('Restart fixture does not match the accepted case')
        shutil.copytree(previous/'saves',run/'saves');shutil.copy2(previous/'created-world.txt',run/'created-world.txt')
    iris=run/'config/iris.properties'
    if iris.exists():
        text=iris.read_text();text='\n'.join(l for l in text.splitlines() if not l.startswith('enableShaders='))+'\nenableShaders='+('false' if 'no-shader' in variant else 'true')+'\n';iris.write_text(text)
        pack=next((l.split('=',1)[1] for l in text.splitlines() if l.startswith('shaderPack=')),None)
        if pack and (source_profile/'shaderpacks'/pack).is_file():
            (run/'shaderpacks').mkdir();shutil.copy2(source_profile/'shaderpacks'/pack,run/'shaderpacks'/pack)
    dh=run/'config/DistantHorizons.toml'
    if dh.exists():
        import re
        dh.write_text(re.sub(r'generatorPlan\s*=\s*"[^"]+"','generatorPlan = "DISABLED"',dh.read_text()))
    voxygen=run/'config/voxyworldgenv2.json'
    if voxygen.exists():
        settings=json.loads(voxygen.read_text());settings.update(generationRadius=8,maxActiveTasks=2,maxQueueSize=512)
        write(voxygen,settings)
    artifact=ARTIFACTS/f'relics-0.1.0-alpha.5.0.5+mc{mc}.jar';shutil.copy2(artifact,run/'mods'/artifact.name)
    shutil.copytree(fixture/'natives',run/'natives')
    text=(ROOT/'src/test/client/de/relics/testmixin/BetaClientBootstrap.java').read_text().replace('BetaClientBootstrap','DistributionMenuChecks')
    # Existing installation defaults are valid; factory-default coverage belongs to point 4.
    text=text.replace('if(Files.exists(DistributionConfig.file()))throw new AssertionError("Unexpected installation defaults");','')
    text=text.replace('if(!DistributionConfig.load().equals(DistributionSettings.DISCOVERY))throw new AssertionError("Factory default differs");','')
    text=text.replace('if(!((de.relics.client.WorldDistributionDraft)creation).relics$draft().equals(DistributionSettings.DISCOVERY))throw new AssertionError("New world draft differs");','')
    text=text.replace('if(!state.settings.equals(DistributionSettings.DISCOVERY))throw new AssertionError("Frozen settings differ from DISCOVERY");','')
    text=text.replace('if(Files.exists(DistributionConfig.file()))throw new AssertionError("Factory check wrote installation defaults");','')
    text=text.replace('frozen DISCOVERY','frozen world settings')
    old='if(relics$phase==5){net.minecraft.client.Screenshot.grab(client,true);relics$phase=6;return;}'
    replacement='''if(relics$phase==5){
 if(relics$joined==0){relics$joined=relics$ticks;client.getSingleplayerServer().execute(()->{var server=client.getSingleplayerServer();for(var command:java.util.List.of("gamemode spectator @a","time set day","weather clear","execute as @a at @s run tp @s ~ ~70 ~ 160 25"))server.getCommands().performPrefixedCommand(server.createCommandSourceStack(),command);});return;}
 if(relics$ticks-relics$joined<600)return;
 boolean shaders=false;try{var api=Class.forName("net.irisshaders.iris.api.v0.IrisApi");var instance=api.getMethod("getInstance").invoke(null);shaders=(boolean)api.getMethod("isShaderPackInUse").invoke(instance);}catch(ClassNotFoundException ignored){}
 Files.writeString(Path.of("graphics-proof.json"),"{\\"renderedTicks\\":600,\\"shadersInUse\\":"+shaders+"}");
 net.minecraft.client.Screenshot.grab(client,true);relics$phase=6;return;}
'''
    replacement=replacement.replace(' if(relics$ticks-relics$joined<600)return;', '''
 if(Boolean.getBoolean("relics.compat.seasons") && relics$maxPlayers==0 && relics$ticks-relics$joined>=200){
 relics$maxPlayers=1;client.getSingleplayerServer().execute(()->{var server=client.getSingleplayerServer();server.getCommands().performPrefixedCommand(server.createCommandSourceStack(),"season set mid_winter");try{var helper=Class.forName("sereneseasons.api.season.SeasonHelper");var state=helper.getMethod("getSeasonState",net.minecraft.world.level.Level.class).invoke(null,server.overworld());var season=Class.forName("sereneseasons.api.season.ISeasonState").getMethod("getSubSeason").invoke(state);Files.writeString(Path.of("season-command-result.txt"),season.toString());}catch(Exception ex){throw new RuntimeException(ex);}});}
 if(relics$ticks-relics$joined<600)return;''')
    if old not in text:raise ValueError('Client bootstrap changed; review patch')
    text=text.replace(old,replacement)
    text=text.replace('if(relics$phase==6){','if(relics$phase==6){if(relics$ticks-relics$joined<660)return;')
    entries=compile_sources(mc,run/'sources',{'DistributionMenuChecks.java':text})
    with zipfile.ZipFile(fixture/'mods/menu-checks.jar') as z:base={n:z.read(n) for n in z.namelist()}
    base.update(entries)
    with zipfile.ZipFile(run/'mods/menu-checks.jar','w',zipfile.ZIP_DEFLATED) as z:
        for n,b in base.items():z.writestr(n,b)
    (run/'options.txt').write_text('lang:en_us\nguiScale:2\nonboardAccessibility:false\nstartedCleanly:true\nrenderDistance:8\nsimulationDistance:2\nsoundCategory_master:0.0\nfullscreen:false\npauseOnLostFocus:false\ntutorialStep:none\n')
    (run/'loopback-hosts.txt').write_text('127.0.0.1 localhost\n::1 localhost\n')
    args=(fixture/'client-args.txt').read_text().replace(fixture.as_posix(),run.as_posix()).replace(str(fixture),str(run))
    args='\n'.join(l for l in args.splitlines() if not any(t in l for t in ['-Djava.io.tmpdir=','-Djdk.net.hosts.file=']))
    args='"-Djava.io.tmpdir='+(run/'tmp').as_posix()+'"\n"-Djdk.net.hosts.file='+(run/'loopback-hosts.txt').as_posix()+'"\n'+args
    args=args.replace('"-Xmx3G"','"-Xmx4G"').replace('"854"','"1280"').replace('"480"','"720"')
    seasons=mc=='1.21.1' and variant!='no-seasons'
    if seasons:args='"-Drelics.compat.seasons=true"\n'+args
    (run/'client-args.txt').write_text(args)
    for f in fixture.glob('*log*.xml'):shutil.copy2(f,run/f.name)
    env=os.environ.copy();env.update(TMP=str(run/'tmp'),TEMP=str(run/'tmp'))
    result={'profile':profile,'minecraft':mc,'variant':variant,'run':str(run),'excluded':excluded,'artifact_sha256':sha(artifact),'distant_generator_disabled_for_graphics_isolation':dh.exists(),
            'voxy_generator_test_bounds':{'radiusChunks':8,'maxActiveTasks':2,'maxQueueSize':512} if voxygen.exists() else None,'restart_of':str(restart_from) if restart_from else None}
    print('CLIENT '+str(run),flush=True);started=time.monotonic()
    with (run/'console.log').open('wb') as log:
        p=subprocess.Popen([str(JAVA[mc]),'@'+str(run/'client-args.txt')],cwd=run,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW,env=env)
        result['pid']=p.pid
        try:
            end=time.monotonic()+300
            while p.poll() is None:
                guard()
                if time.monotonic()>end:raise TimeoutError('Graphics client timeout')
                time.sleep(1)
            result['exit']=p.returncode
            result['proof']=json.loads((run/'graphics-proof.json').read_text()) if (run/'graphics-proof.json').exists() else None
            if seasons:result['season_command_result']=(run/'season-command-result.txt').read_text().strip() if (run/'season-command-result.txt').exists() else None
            result['passed']=p.returncode==0 and result['proof'] is not None and result['proof']['shadersInUse']==('no-shader' not in variant)
            if seasons:result['passed']=result['passed'] and result.get('season_command_result')=='MID_WINTER'
            return result
        finally:
            if p.poll() is None:p.terminate();p.wait(timeout=20)
            result.update(exit=p.returncode,duration=time.monotonic()-started,files={str(f.relative_to(run)):sha(f) for f in run.rglob('*') if f.is_file() and f.suffix in ['.java','.log','.png','.json'] and 'saves' not in f.parts})
            write(run/'result.json',result)
            print('CLIENT END '+profile+' '+variant+' exit='+str(p.returncode),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--profile',choices=['TerraVista','TerraVista Living World'],required=True)
    ap.add_argument('--variant',choices=['as-installed','no-voxy','no-shader','no-bridge','no-shader-no-bridge','no-seasons'],default='as-installed')
    ap.add_argument('--restart-from',type=Path)
    a=ap.parse_args()
    if not run_client(a.profile,a.variant,a.restart_from)['passed']:raise SystemExit(1)
