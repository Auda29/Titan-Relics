"""Run bounded actual DH FEATURES and INTERNAL_SERVER jobs in a fresh test server."""
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
from smoke_server import Console, inspect_world


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--full-footprint',action='store_true');options=parser.parse_args()
    guard();mc='1.21.1';run=SCRATCH/'dh'/datetime.now().strftime('generator-%H%M%S')
    (run/'mods').mkdir(parents=True);(run/'tmp').mkdir()
    for p in cached_mods(mc,'fabric',None).glob('*.jar'):os.link(p,run/'mods'/p.name)
    dh=Path('E:/Roaming/ModrinthApp/profiles/TerraVista Living World/mods/DistantHorizons-3.3.3-1.21.1-fabric-neoforge.jar')
    shutil.copy2(dh,run/'mods'/dh.name)
    artifact=ARTIFACTS/'relics-0.1.0-alpha.5.0.5+mc1.21.1.jar';shutil.copy2(artifact,run/'mods'/artifact.name)
    source=(ROOT/'src/test/client/de/relics/testmixin/BetaDhGenerationProbe.java').read_text()
    entries=compile_sources(mc,run/'sources',{'BetaDhGenerationProbe.java':source})
    entries['fabric.mod.json']=json.dumps({'schemaVersion':1,'id':'relics_dh_probe','version':'1','environment':'*','mixins':['dh-probe.mixins.json']}).encode()
    entries['dh-probe.mixins.json']=json.dumps({'required':True,'package':'de.relics.testmixin','compatibilityLevel':'JAVA_21','mixins':['BetaDhGenerationProbe'],'injectors':{'defaultRequire':1}}).encode()
    with zipfile.ZipFile(run/'mods/dh-probe.jar','w',zipfile.ZIP_DEFLATED) as z:
        for n,b in entries.items():z.writestr(n,b)
    (run/'eula.txt').write_text('eula=true\n')
    (run/'server.properties').write_text('server-ip=127.0.0.1\nserver-port=0\nonline-mode=false\nlevel-name=world\nlevel-seed=731204\ngenerate-structures=true\nview-distance=2\nsimulation-distance=2\nmax-tick-time=60000\n')
    (run/'dh-request.json').write_text(json.dumps({'fullFootprint':options.full_footprint}))
    (run/'loopback-hosts.txt').write_text('127.0.0.1 localhost\n::1 localhost\n')
    import shlex
    old=shlex.split((ROOT/'build/beta-load-guard/reproduction/args.txt').read_text(),posix=True);cp=old[old.index('-cp')+1]
    args=['-Xms512M','-Xmx4G','-XX:ActiveProcessorCount=4','-Djava.awt.headless=true','-Djava.io.tmpdir='+str(run/'tmp'),
          '-Djdk.net.hosts.file='+str(run/'loopback-hosts.txt'),'-cp',cp,'net.fabricmc.loader.impl.launch.knot.KnotServer','nogui']
    (run/'java-args.txt').write_text('\n'.join('"'+v.replace('\\','/')+'"' for v in args))
    env=os.environ.copy();env.update(TMP=str(run/'tmp'),TEMP=str(run/'tmp'))
    result={'run':str(run),'artifact_sha256':sha(artifact),'dh_sha256':sha(dh),'passed':False}
    print('DH PROBE '+str(run),flush=True)
    p=subprocess.Popen([str(JAVA[mc]),'@'+str(run/'java-args.txt')],cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=subprocess.CREATE_NO_WINDOW,env=env)
    console=Console(p,run/'console.log',echo=False);result['pid']=p.pid;start=time.monotonic()
    try:
        end=time.monotonic()+420
        while not (run/'dh-proof.json').exists():
            if p.poll() is not None:raise RuntimeError('DH probe server stopped before proof')
            if time.monotonic()>end:raise TimeoutError('DH probe did not complete')
            guard();time.sleep(.5)
        time.sleep(.2);result['proof']=json.loads((run/'dh-proof.json').read_text())
        p.stdin.write('save-all flush\nstop\n');p.stdin.flush();p.wait(timeout=90);console.thread.join(timeout=5)
        result['passed']=p.returncode==0 and result['proof'].get('completed') is True
        result['world_inspection']=inspect_world(run/'world')
        print(json.dumps({name: {'seconds':row['seconds'],'chunks':len(row['chunks']),
              'relic_start_chunks':sum(any(s.startswith('relics:') for s in c['validStructureStarts']) for c in row['chunks'])}
              for name,row in result['proof'].items() if name in ['FEATURES','INTERNAL_SERVER']}),flush=True)
    finally:
        if p.poll() is None:
            p.stdin.write('stop\n');p.stdin.flush()
            try:p.wait(timeout=20)
            except subprocess.TimeoutExpired:p.terminate();p.wait(timeout=15)
        result.update(exit=p.returncode,duration=time.monotonic()-start,console_sha256=sha(run/'console.log'))
        write(run/'result.json',result)
        print('DH END exit='+str(p.returncode)+' completed='+str(result['passed']),flush=True)


if __name__=='__main__':main()
