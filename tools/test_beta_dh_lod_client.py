"""Photograph a server-generated Colossus as DH LOD before the player loads it."""
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
import zipfile

from beta_qa_runtime import compile_sources
from test_beta_performance import SCRATCH, ROOT, JAVA, guard, sha, write


def main():
    guard();source=SCRATCH/'dh/generator-151400';data=json.loads((source/'dh-proof.json').read_text())
    if not data.get('completed') or len(data['INTERNAL_SERVER']['chunks'])!=324:raise ValueError('Expected accepted full-footprint DH fixture')
    fixture=ROOT/'build/beta-client-acceptance-20261104/client-1.21.1-110010-680449'
    profile=Path('E:/Roaming/ModrinthApp/profiles/TerraVista Living World')
    run=SCRATCH/'lod-client'/datetime.now().strftime('render-%H%M%S')
    (run/'mods').mkdir(parents=True);(run/'config').mkdir();(run/'tmp').mkdir()
    for p in (source/'mods').glob('*.jar'):
        if p.name!='dh-probe.jar':shutil.copy2(p,run/'mods'/p.name)
    for p in (profile/'mods').glob('*.jar'):
        if p.name.startswith(('iris-','sodium-')):shutil.copy2(p,run/'mods'/p.name)
    shutil.copytree(source/'world',run/'saves/world');(run/'created-world.txt').write_text('world')
    shutil.copytree(fixture/'natives',run/'natives');write(run/'lod-site.json',data['site'])
    dh=(profile/'config/DistantHorizons.toml').read_text()
    replacements={'generatorPlan':'"CHUNKS_ONLY"','chunkGeneratorMode':'"PRE_EXISTING_ONLY"','lodChunkRenderDistanceRadius':'64',
                  'generationMaxChunkRadius':'32','generationCenterChunkX':str(data['site']['candidate']['x']//16),'generationCenterChunkZ':str(data['site']['candidate']['z']//16)}
    for key,value in replacements.items():dh=re.sub(r'(?m)^(\s*'+key+r'\s*=\s*).+$',lambda m:m.group(1)+value,dh)
    (run/'config/DistantHorizons.toml').write_text(dh)
    shutil.copy2(profile/'config/iris.properties',run/'config/iris.properties');(run/'shaderpacks').mkdir()
    shutil.copy2(profile/'shaderpacks/BSL_v10.1.8.zip',run/'shaderpacks/BSL_v10.1.8.zip')
    text=(ROOT/'src/test/client/de/relics/testmixin/BetaClientBootstrap.java').read_text().replace('BetaClientBootstrap','DistributionMenuChecks')
    old='if(relics$phase==5){net.minecraft.client.Screenshot.grab(client,true);relics$phase=6;return;}'
    new='''if(relics$phase==5){
 var site=com.google.gson.JsonParser.parseString(Files.readString(Path.of("lod-site.json"))).getAsJsonObject();
 double x=site.get("x2").getAsDouble()/2,z=site.get("z2").getAsDouble()/2;int surface=site.get("surface").getAsInt();
 if(relics$joined==0){relics$joined=relics$ticks;client.getSingleplayerServer().execute(()->{var server=client.getSingleplayerServer();for(var command:java.util.List.of("gamemode spectator @a","time set day","weather clear","tp @a "+x+" "+(surface+100)+" "+(z+400)+" facing "+x+" "+(surface+60)+" "+z))server.getCommands().performPrefixedCommand(server.createCommandSourceStack(),command);});return;}
 if(relics$ticks-relics$joined<1800)return;
 int cx=Math.floorDiv(site.getAsJsonObject("candidate").get("x").getAsInt(),16),cz=Math.floorDiv(site.getAsJsonObject("candidate").get("z").getAsInt(),16);
 boolean loaded=client.getSingleplayerServer().submit(()->client.getSingleplayerServer().overworld().hasChunk(cx,cz)).get();
 var proof=new com.google.gson.JsonObject();proof.addProperty("targetNormallyLoaded",loaded);proof.addProperty("distanceToTargetXZ",Math.hypot(client.player.getX()-x,client.player.getZ()-z));proof.addProperty("vanillaRenderDistance",client.options.renderDistance().get());
 Files.writeString(Path.of("dh-lod-proof.json"),proof.toString());net.minecraft.client.Screenshot.grab(client,true);relics$phase=6;return;}
'''
    if old not in text:raise AssertionError('Bootstrap changed')
    text=text.replace(old,new).replace('if(relics$phase==6){','if(relics$phase==6){if(relics$ticks-relics$joined<1860)return;')
    entries=compile_sources('1.21.1',run/'sources',{'DistributionMenuChecks.java':text})
    with zipfile.ZipFile(fixture/'mods/menu-checks.jar') as z:base={n:z.read(n) for n in z.namelist()}
    base.update(entries)
    with zipfile.ZipFile(run/'mods/menu-checks.jar','w',zipfile.ZIP_DEFLATED) as z:
        for n,b in base.items():z.writestr(n,b)
    (run/'options.txt').write_text('lang:en_us\nguiScale:2\nonboardAccessibility:false\nstartedCleanly:true\nrenderDistance:2\nsimulationDistance:2\nsoundCategory_master:0.0\nfullscreen:false\npauseOnLostFocus:false\ntutorialStep:none\n')
    (run/'loopback-hosts.txt').write_text('127.0.0.1 localhost\n::1 localhost\n')
    args=(fixture/'client-args.txt').read_text().replace(fixture.as_posix(),run.as_posix())
    args='\n'.join(l for l in args.splitlines() if not any(s in l for s in ['-Djava.io.tmpdir=','-Djdk.net.hosts.file=']))
    args='"-Djava.io.tmpdir='+(run/'tmp').as_posix()+'"\n"-Djdk.net.hosts.file='+(run/'loopback-hosts.txt').as_posix()+'"\n'+args
    args=args.replace('"-Xmx3G"','"-Xmx4G"').replace('"854"','"1280"').replace('"480"','"720"');(run/'client-args.txt').write_text(args)
    env=os.environ.copy();env.update(TMP=str(run/'tmp'),TEMP=str(run/'tmp'))
    result={'run':str(run),'source_world':str(source/'world'),'source_dh_result':sha(source/'result.json'),'passed':False}
    print('LOD CLIENT '+str(run),flush=True);started=time.monotonic()
    with (run/'console.log').open('wb') as log:
        p=subprocess.Popen([str(JAVA['1.21.1']),'@'+str(run/'client-args.txt')],cwd=run,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW,env=env);result['pid']=p.pid
        try:
            end=time.monotonic()+300
            while p.poll() is None:
                guard()
                if time.monotonic()>end:raise TimeoutError('LOD renderer timeout')
                time.sleep(1)
            if (run/'dh-lod-proof.json').exists():result['proof']=json.loads((run/'dh-lod-proof.json').read_text())
            result['passed']=p.returncode==0 and not result.get('proof',{}).get('targetNormallyLoaded',True)
        finally:
            if p.poll() is None:p.terminate();p.wait(timeout=20)
            result.update(exit=p.returncode,duration=time.monotonic()-started,console_sha256=sha(run/'console.log'))
            write(run/'result.json',result)
            print('LOD END '+json.dumps(result),flush=True)


if __name__=='__main__':main()
