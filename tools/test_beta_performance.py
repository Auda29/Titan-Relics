"""Serial isolated A/B chunk-generation measurements; never launches a user profile."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
import zipfile

import ctypes
from ctypes import wintypes

from compile_worldgen import ROOT, compile_libraries
from smoke_server import Console, inspect_world
from neoforge_runtime import installed_arguments, logging_arguments

SCRATCH = Path('E:/Relic_Mod_QA/compatibility-20261104')
ARTIFACTS = ROOT / 'build/beta-client-acceptance-20261104/artifacts'
JAVA = {'1.21.1': Path('C:/Program Files/Java/jdk-21.0.10/bin/java.exe'),
        '26.2': Path('C:/Users/wecke/.gradle/jdks/eclipse_adoptium-25-amd64-windows.2/bin/java.exe')}


def resident_bytes(pid):
    class Counters(ctypes.Structure):
        _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in
            ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage',
             'QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
    kernel=ctypes.WinDLL('kernel32',use_last_error=True);api=ctypes.WinDLL('psapi',use_last_error=True)
    kernel.OpenProcess.restype=wintypes.HANDLE
    kernel.CloseHandle.argtypes=[wintypes.HANDLE]
    api.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(Counters),wintypes.DWORD]
    handle=kernel.OpenProcess(0x410,False,pid)
    if not handle:raise ctypes.WinError(ctypes.get_last_error())
    try:
        counters=Counters();counters.cb=ctypes.sizeof(counters)
        if not api.GetProcessMemoryInfo(handle,ctypes.byref(counters),counters.cb):raise ctypes.WinError(ctypes.get_last_error())
        return counters.WorkingSetSize
    finally:kernel.CloseHandle(handle)


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def write(path, data):
    temporary=path.with_suffix(path.suffix+'.pending')
    temporary.write_text(json.dumps(data, indent=2), encoding='utf-8')
    for attempt in range(30):
        try:temporary.replace(path);return
        except PermissionError:
            if attempt==29:raise
            time.sleep(.01)


def guard():
    if shutil.disk_usage(ROOT).free < 4*2**30 or shutil.disk_usage(SCRATCH).free < 20*2**30:
        raise RuntimeError('Storage reserve reached; no more test starts')
    # Count unique files across every test kind and both dimension layouts.
    seen=set();size=0
    for path in SCRATCH.rglob('*'):
        if not path.is_file():continue
        stat=path.stat();identity=(stat.st_dev,stat.st_ino)
        if identity not in seen:
            seen.add(identity);size+=stat.st_size
    if size > 12*2**30:
        raise RuntimeError('Scratch budget reached')


def compile_probe(mc, loader):
    out = SCRATCH/'probes'/(loader+'-'+mc)
    out.mkdir(parents=True, exist_ok=True)
    source = (ROOT/'src/test/client/de/relics/testmixin/BetaPerformanceProbe.java').read_text()
    if mc == '1.21.1' and loader == 'fabric':
        source = source.replace('method="tickServer"', 'method="method_3748"')
    java = out/'BetaPerformanceProbe.java'; java.write_text(source, encoding='utf-8')
    classes = out/'classes';classes.mkdir(exist_ok=True)
    cp = os.pathsep.join(map(str, compile_libraries()))
    if mc == '1.21.1':
        cp = (ROOT/'compat/alpha5-fabric-1.21.1/build/runtime-classpath.txt').read_text().strip()
    with (out/'compile.log').open('wb') as log:
        subprocess.run([str(JAVA[mc].with_name('javac.exe')), '-J-Djava.io.tmpdir='+str(out),
                        '--release', '21' if mc=='1.21.1' else '25','-proc:none','-encoding','UTF-8',
                        '-cp',cp,'-d',str(classes),str(java)], stdout=log,stderr=subprocess.STDOUT,check=True)
    raw = out/'probe-named.jar'
    with zipfile.ZipFile(raw,'w') as z:
        for p in classes.rglob('*.class'):z.write(p,p.relative_to(classes).as_posix())
    jar = raw
    if mc == '1.21.1' and loader == 'fabric':
        modules=Path.home()/'.gradle/caches/modules-2/files-2.1'
        remapper_cp=[*modules.glob('net.fabricmc/tiny-remapper/0.14.0/*/*.jar'),*modules.glob('net.fabricmc/mapping-io/*/*/*.jar'),*modules.glob('org.ow2.asm/*/9.10.1/*/*.jar')]
        mappings=Path.home()/'.gradle/caches/fabric-loom/1.21.1/loom.mappings.1_21_1.layered+hash.2198-v2/mappings.tiny'
        jar=out/'probe-intermediary.jar'
        with (out/'remap.log').open('wb') as log:
            subprocess.run([str(JAVA[mc]),'-Djava.io.tmpdir='+str(out),'-cp',os.pathsep.join(map(str,remapper_cp)),
                            'net.fabricmc.tinyremapper.Main',str(raw),str(jar),str(mappings),'named','intermediary',*cp.split(os.pathsep)],stdout=log,stderr=subprocess.STDOUT,check=True)
    with zipfile.ZipFile(jar) as z:entries={n:z.read(n) for n in z.namelist()}
    entries['beta-performance.mixins.json']=json.dumps({'required':True,'package':'de.relics.testmixin','compatibilityLevel':'JAVA_'+('21' if mc=='1.21.1' else '25'),'mixins':['BetaPerformanceProbe'],'injectors':{'defaultRequire':1}}).encode()
    if loader=='fabric':
        entries['fabric.mod.json']=json.dumps({'schemaVersion':1,'id':'relics_performance_checks','version':'1','environment':'*','mixins':['beta-performance.mixins.json']}).encode()
    else:
        entries['META-INF/neoforge.mods.toml']=b'modLoader="javafml"\nloaderVersion="[1,)"\nlicense="MIT"\n[[mods]]\nmodId="relics_performance_checks"\nversion="1"\ndisplayName="Isolated performance checks"\n[[mixins]]\nconfig="beta-performance.mixins.json"\n'
    final=out/'beta-performance.jar'
    with zipfile.ZipFile(final,'w',zipfile.ZIP_DEFLATED) as z:
        for n,b in entries.items():z.writestr(n,b)
    return final


def cached_mods(mc, loader, profile):
    tag=profile or loader+'-'+mc
    dest=SCRATCH/'modsets'/tag;dest.mkdir(parents=True,exist_ok=True)
    if profile:
        sources=list((Path('E:/Roaming/ModrinthApp/profiles')/profile/'mods').glob('*.jar'))
        sources=[p for p in sources if not p.name.startswith('relics-')]
    else:
        fixture={'fabric-1.21.1':'client-1.21.1-110010-680449','fabric-26.2':'client-26.2-105935-270526',
                 'neoforge-1.21.1':'neo-client-1.21.1-110000-535487','neoforge-26.2':'neo-client-26.2-110020-943280'}[loader+'-'+mc]
        sources=list((ROOT/'build/beta-client-acceptance-20261104'/fixture/'mods').glob('*.jar'))
        sources=[p for p in sources if not p.name.startswith('relics-') and not p.name.endswith('checks.jar')]
    for p in sources:
        q=dest/p.name
        if not q.exists():shutil.copy2(p,q)
        if sha(p)!=sha(q):raise RuntimeError('Cached mod source changed: '+str(p))
    return dest


def run_case(mc,loader,seed,with_relic,profile=None,regions=None,label=''):
    guard()
    key=(profile or loader+'-'+mc).replace(' ','-')+'-'+str(seed)+('-relic' if with_relic else '-control')
    if label:key+='-'+label
    run=SCRATCH/'runs'/key
    if run.exists():raise ValueError('Refusing to overwrite run '+str(run))
    (run/'mods').mkdir(parents=True);(run/'tmp').mkdir()
    excluded=[]
    for p in cached_mods(mc,loader,profile).glob('*.jar'):
        if profile=='TerraVista' and p.name=='Voxy World Gen V2-fabric-26.2-2.4.3.jar':
            excluded.append({'file':p.name,'reason':'Client graphics integration references LWJGL on a dedicated server; retained in real-client tests'})
            continue
        os.link(p,run/'mods'/p.name)
    probe=compile_probe(mc,loader);shutil.copy2(probe,run/'mods'/probe.name)
    artifact=ARTIFACTS/('relics-0.1.0-alpha.5.0.5+mc'+mc+('-neoforge' if loader=='neoforge' else '')+'.jar')
    if with_relic:shutil.copy2(artifact,run/'mods'/artifact.name)
    if profile:
        original=Path('E:/Roaming/ModrinthApp/profiles')/profile
        for n in ['config','defaultconfigs','moonlight-global-data-pack']:
            if (original/n).is_dir():shutil.copytree(original/n,run/n)
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    props={'server-ip':'127.0.0.1','server-port':port,'online-mode':'false','level-name':'world','level-seed':seed,
           'generate-structures':'true','view-distance':2,'simulation-distance':2,'max-players':1,'max-tick-time':60000,
           'pause-when-empty-seconds':0,'enable-rcon':'false','enable-query':'false','difficulty':'peaceful'}
    (run/'server.properties').write_text(''.join(f'{k}={v}\n' for k,v in props.items()))
    (run/'eula.txt').write_text('eula=true\n')
    (run/'loopback-hosts.txt').write_text('127.0.0.1 localhost\n::1 localhost\n')
    args=['-Xms512M','-Xmx4G','-XX:ActiveProcessorCount=4','-Djava.awt.headless=true',
          '-Djava.io.tmpdir='+str(run/'tmp'),'-Djdk.net.hosts.file='+str(run/'loopback-hosts.txt')]
    if loader=='neoforge':
        server=ROOT/('build/neoforge/runtime-'+mc)
        base,evidence=installed_arguments(server,mc);logging,_=logging_arguments(server,mc,run);args+=logging+base+['nogui']
    else:
        if mc=='1.21.1':
            import shlex
            old=shlex.split((ROOT/'build/beta-load-guard/reproduction/args.txt').read_text(),posix=True)
            cp=old[old.index('-cp')+1]
        else:
            cp=os.pathsep.join(str(p) for p in compile_libraries() if p.name=='fabric-loader-0.19.5.jar' or any(t in {'libraries','loader-libraries','versions'} for t in p.parts))
        args+=['-cp',cp,'net.fabricmc.loader.impl.launch.knot.KnotServer','nogui']
    argfile=run/'java-args.txt';argfile.write_text('\n'.join('"'+a.replace('\\','/')+'"' for a in args))
    env=os.environ.copy();env.update(TMP=str(run/'tmp'),TEMP=str(run/'tmp'))
    result={'run':str(run),'minecraft':mc,'loader':loader,'profile':profile,'seed':seed,'with_relic':with_relic,
            'excluded_server_mods':excluded,
            'probe_source_sha256':sha(ROOT/'src/test/client/de/relics/testmixin/BetaPerformanceProbe.java'),
            'artifact_sha256':sha(artifact) if with_relic else None,'mod_hashes':{p.name:sha(p) for p in (run/'mods').glob('*.jar')},'phases':[],'passed':False}
    print('START '+key,flush=True)
    started=time.monotonic();p=subprocess.Popen([str(JAVA[mc]),'@'+str(argfile)],cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=subprocess.CREATE_NO_WINDOW,env=env)
    console=Console(p,run/'console.log',echo=False);peak=0
    def wait_for(predicate,timeout):
        nonlocal peak
        end=time.monotonic()+timeout
        while not predicate():
            if p.poll() is not None:raise RuntimeError('Server exited: '+str(p.returncode))
            peak=max(peak,resident_bytes(p.pid))
            if time.monotonic()>end:raise TimeoutError(key)
            guard();time.sleep(.2)
    def command(cmd):p.stdin.write(cmd+'\n');p.stdin.flush()
    def metrics():
        try:return json.loads((run/'bench-metrics.json').read_text())
        except (FileNotFoundError,json.JSONDecodeError,PermissionError):return {}
    try:
        wait_for(lambda:any('Done (' in line for line in console.lines),180)
        result['startup_seconds']=time.monotonic()-started
        if with_relic:
            def journal():
                try:return json.loads(json.loads((run/'world/data/relics_distribution_v1.json').read_text())['payload'])
                except (FileNotFoundError,json.JSONDecodeError,PermissionError,KeyError):return {}
            wait_for(lambda:journal().get('unique') is not None or journal().get('unavailable'),180)
            result['colossus_site']=journal().get('unique')
        plan=regions or [('warmup',512,512,7),('ordinary',1024,1024,15)]
        if regions=='extended':
            if not with_relic or not result.get('colossus_site'):raise ValueError('Extended route requires a resolved natural destination first')
            plan=[('warmup',512,512,7),('ordinary',1024,1024,15)]
            site=result['colossus_site'];index=0
            for x in range(site['minX']//16,site['maxX']//16+1,8):
                for z in range(site['minZ']//16,site['maxZ']//16+1,8):
                    plan.append(('colossus-'+str(index),x,z,7));index+=1
            plan += [('pregeneration-0',1536,1536,15),('pregeneration-1',1552,1536,15)]
        result['route']=plan
        for name,x,z,width in plan:
            command('forceload remove all')
            (run/'bench-phase.txt').write_text(name)
            wait_for(lambda:metrics().get('phase')==name,15)
            write(run/'bench-chunks-request.json',{'id':name,'minX':x,'maxX':x+width,'minZ':z,'maxZ':z+width})
            begin=time.monotonic();command(f'forceload add {x*16} {z*16} {(x+width)*16+15} {(z+width)*16+15}')
            def complete():
                row=metrics().get('chunks',{})
                return row.get('id')==name and row.get('loaded')==row.get('total')==(width+1)**2
            wait_for(complete,300 if name.startswith('colossus') else 180)
            phase={'name':name,'seconds':time.monotonic()-begin,'chunks':(width+1)**2};result['phases'].append(phase)
            print(key+' '+json.dumps(phase),flush=True)
        command('forceload remove all');(run/'bench-phase.txt').write_text('idle')
        wait_for(lambda:metrics().get('phase')=='idle',15)
        wait_for(lambda:metrics().get('phases',{}).get('idle',{}).get('ticks',0)>=200,45)
        result['metrics']=metrics();command('save-all flush');time.sleep(2);command('stop')
        p.wait(timeout=120);console.thread.join(timeout=5)
        result['exit']=p.returncode;result['passed']=p.returncode==0
        if with_relic:result['world_inspection']=inspect_world(run/'world')
        return result
    finally:
        if p.poll() is None:
            command('stop')
            try:p.wait(timeout=30)
            except subprocess.TimeoutExpired:p.terminate();p.wait(timeout=20)
        result.update(exit=p.returncode,peak_rss_bytes=peak,duration_seconds=time.monotonic()-started,
                      world_bytes=sum(q.stat().st_size for q in (run/'world').rglob('*') if q.is_file()),console_sha256=sha(run/'console.log'))
        write(run/'result.json',result)
        print('END '+key+' passed='+str(result['passed']),flush=True)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--minecraft',choices=['1.21.1','26.2'],required=True)
    ap.add_argument('--loader',choices=['fabric','neoforge'],default='fabric')
    ap.add_argument('--seed',type=int,default=731204)
    ap.add_argument('--profile',choices=['TerraVista','TerraVista Living World'])
    ap.add_argument('--control',action='store_true')
    ap.add_argument('--route',type=Path)
    ap.add_argument('--label',default='')
    a=ap.parse_args();run_case(a.minecraft,a.loader,a.seed,not a.control,a.profile,json.loads(a.route.read_text()) if a.route else None,a.label)


if __name__=='__main__':main()
