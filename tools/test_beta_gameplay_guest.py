"""Launch real offline guests only in a generated build/ QA fixture."""
import argparse,hashlib,json,shutil,subprocess,time,os
from test_beta_gameplay_client import AUTHORIZED_SCRATCH, storage_guard
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('run',type=Path);ap.add_argument('port',type=int,nargs='?',default=25781);ap.add_argument('--scratch-root',type=Path);ap.add_argument('--repeat',action='store_true');ap.add_argument('--name',default='BetaGuest');a=ap.parse_args()
    run=a.run.resolve();root=Path(__file__).resolve().parents[1]
    scratch=a.scratch_root.resolve() if a.scratch_root else root/'build/beta-client-gameplay-20261104'
    if a.scratch_root and scratch != AUTHORIZED_SCRATCH:raise ValueError('Unauthorized scratch root')
    if not run.is_relative_to(scratch):raise ValueError('Run outside QA scratch')
    storage_guard(scratch)
    java='C:/Program Files/Java/jdk-21.0.10/bin/java.exe' if '1.21.1' in str(run) else 'C:/Users/wecke/.gradle/jdks/eclipse_adoptium-25-amd64-windows.2/bin/java.exe'
    records=[]
    for iteration in range(2 if a.repeat else 1):
        guest=run/('guest' if iteration==0 else 'guest-reconnected');guest.mkdir()
        storage_guard(scratch)
        tmp=guest/'tmp';tmp.mkdir()
        env=os.environ.copy();env.update(TMP=str(tmp),TEMP=str(tmp))
        if (run/'natives').exists():shutil.copytree(run/'natives',guest/'natives')
        shutil.copytree(run/'mods',guest/'mods');
        if (run/'config').exists():shutil.copytree(run/'config',guest/'config')
        shutil.copy2(run/'options.txt',guest/'options.txt')
        (guest/'loopback-hosts.txt').write_text('127.0.0.1 localhost\n::1 localhost\n')
        opt=guest/'options.txt';opt.write_text('\n'.join(line for line in opt.read_text().splitlines() if not line.startswith('soundCategory_master:'))+'\nsoundCategory_master:0.0\n')
        for config in run.glob('*log*.xml'):shutil.copy2(config,guest/config.name)
        text=(run/'client-args.txt').read_text().replace(run.as_posix(),guest.as_posix()).replace(str(run),str(guest)).replace('RelicMenuProbe',a.name).replace('RelicLoadProbe',a.name).replace('00000000000000000000000000000001','00000000000000000000000000000002')
        argfile=guest/'client-args.txt';argfile.write_text('"-Drelics.acceptance.join='+str(a.port)+'"\n'+text)
        deadline=time.time()+180
        while not (run/('encounter-ready.txt' if iteration==0 else 'reload-ready.txt')).exists():
            if time.time()>deadline:raise RuntimeError('Host not ready: '+str(run))
            time.sleep(1)
        command=[java,'@'+str(argfile)]
        with (guest/'console.log').open('wb') as log:
            p=subprocess.Popen(command,cwd=guest,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW,env=env)
            r={'pid':p.pid,'started':time.time(),'command':command};records.append(r);print(r,flush=True)
            try:r['exit']=p.wait(timeout=1800)
            finally:
                if p.poll() is None:p.terminate();p.wait(timeout=20);r['terminated']=True
                r['ended']=time.time();r['files']={q.name:hashlib.sha256(q.read_bytes()).hexdigest() for q in guest.glob('*.log')}
                (guest/'process.json').write_text(json.dumps(r,indent=2));(run/'guest-processes.json').write_text(json.dumps(records,indent=2))

if __name__=='__main__':main()
