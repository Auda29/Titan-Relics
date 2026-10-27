"""Resolve the player's relic searches on the same seed in an isolated server and generate two results."""
import argparse
from datetime import datetime
import hashlib,json,os,re,shutil,socket,subprocess,time
from pathlib import Path
from compile_worldgen import ROOT,compile_libraries
from smoke_server import Console
from test_natural_interiors_server import blocks_proof

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--accept-eula',action='store_true');p.add_argument('--java-home',type=Path,required=True);p.add_argument('--artifact',type=Path,required=True)
    args=p.parse_args()
    if not args.accept_eula:p.error('Accept Minecraft EULA for this isolated test with --accept-eula')
    artifact=args.artifact.resolve();deps=compile_libraries();java=args.java_home.resolve()/'bin/java.exe'
    run=ROOT/'build/hand-vault-locate-20261027'/datetime.now().strftime('locate-%H%M%S-%f');(run/'mods').mkdir(parents=True)
    for f in [artifact,ROOT/'build/worldgen-dependencies/fabric-api-0.161.0+26.2.jar',ROOT/'build/worldgen-dependencies/lithostitched-1.8.0-fabric-26.2.jar']:shutil.copy2(f,run/'mods'/f.name)
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    props={'server-ip':'127.0.0.1','server-port':port,'online-mode':'true','white-list':'true','enforce-whitelist':'true','level-name':'world','level-seed':7176494076711744605,'view-distance':2,'simulation-distance':2,'pause-when-empty-seconds':0,'max-tick-time':60000}
    (run/'server.properties').write_text(''.join(f'{k}={v}\n' for k,v in props.items()));(run/'eula.txt').write_text('eula=true\n')
    cp=[v for v in deps if v.name=='fabric-loader-0.19.5.jar' or any(s in {'libraries','loader-libraries','versions'} for s in v.parts)]
    argv=['-Xms256M','-Xmx3G','-XX:ActiveProcessorCount=4','-Djava.awt.headless=true','-cp',os.pathsep.join(map(str,cp)),'net.fabricmc.loader.impl.launch.knot.KnotServer','nogui']
    af=run/'args.txt';af.write_text('\n'.join('"'+v.replace('\\','/')+'"' for v in argv))
    process=subprocess.Popen([str(java),'@'+str(af)],cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    console=Console(process,run/'console.log',echo=False)
    report={'seed':7176494076711744605,'origin':[-68776,-12600],'artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),'search_radius':500000,'results':[],'passed':False}
    print('LOCATE_SERVER',run,flush=True)
    try:
        console.wait(r'Done \(',timeout=180);console.wait(r'Relic destination ',timeout=300)
        status=console.command('relicsdistribution status',r'"snapshot"');snapshot=json.loads(status[status.index('{'):])['snapshot']
        assert snapshot['fingerprint']=='1065c923e12c1ea34e951a9bfee90bdbea46f3d977573aad572b8a75b3969097'
        report['fingerprint_matches_player_world']=True
        for name in ['small_colossus','ruined_tower','world_tree','titan_skull','titan_skull_2']:
            cmd=f'execute positioned -68776 80 -12600 run locate structure #relics:{name}'
            start=time.monotonic();response=console.command(cmd,r'The nearest|Kein gültiges Ziel|Relikt-Suche angehalten',timeout=600)
            found=re.search(r'is at \[(-?\d+), ~, (-?\d+)\]',response)
            assert found,response
            x,z=map(int,found.groups());result=console.command(f'relicsdistribution plan {x} {z}',r'Relic plan Cell')
            site=json.loads(result[result.index('{'):]);assert site and site['x2']//2==x and site['z2']//2==z
            if name=='titan_skull':assert site['asset'].startswith('titan_skull') and site['asset']!='titan_skull_2'
            else:assert site['asset']==name
            record={'type':name,'command':cmd,'response':response,'seconds':round(time.monotonic()-start,3),'site':site};report['results'].append(record)
            print('FOUND',name,x,z,record['seconds'],flush=True)
            (run/'evidence.json').write_text(json.dumps(report,indent=2)+'\n')
        selected=[r['site'] for r in report['results'] if r['type'] in ('small_colossus','world_tree')]
        console.command('gamerule minecraft:random_tick_speed 0',r'Gamerule random_tick_speed is now set to: 0')
        for site in selected:
            for x in range(site['minX']//16,site['maxX']//16+1,8):
                end=min(x+7,site['maxX']//16)
                console.command(f'forceload add {x*16} {site["minZ"]//16*16} {end*16+15} {site["maxZ"]//16*16+15}',r'Marked|force.loaded|No chunks',timeout=180)
            for x in range(site['minX']//16,site['maxX']//16+1):
                for z in range(site['minZ']//16,site['maxZ']//16+1):
                    deadline=time.monotonic()+180
                    while 'Test passed' not in console.command(f'execute if loaded {x*16} 80 {z*16}',r'Test passed|Test failed'):
                        assert time.monotonic()<deadline;time.sleep(.25)
        console.command('save-all flush',r'Saved the game');console.command('stop',r'Stopping the server');process.wait(timeout=120);console.thread.join(timeout=5)
        assert process.returncode==0 and not [l for l in console.lines if '/ERROR]' in l]
        report['block_verification']=blocks_proof(run/'world',artifact,selected);report['passed']=True
    finally:
        if process.poll() is None:
            try:process.stdin.write('stop\n');process.stdin.flush();process.wait(timeout=30)
            except Exception:process.terminate();process.wait(timeout=15)
        (run/'evidence.json').write_text(json.dumps(report,indent=2)+'\n');print('LOCATE_EVIDENCE',run/'evidence.json',flush=True)

if __name__=='__main__':main()
