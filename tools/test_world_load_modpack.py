"""Check a previously isolated modpack/world fixture; refuse launcher/profile directories."""
from __future__ import annotations
import argparse,hashlib,json,shutil,subprocess,time
from pathlib import Path
from smoke_server import Console

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture',type=Path,required=True)
    parser.add_argument('--artifact',type=Path,required=True)
    parser.add_argument('--java',type=Path,required=True)
    parser.add_argument('--remove-mod',action='append',required=True,help='Exact JAR filename in the isolated fixture')
    args=parser.parse_args();run=args.fixture.resolve();artifact=args.artifact.resolve()
    if not run.is_relative_to((ROOT/'build').resolve()):parser.error('Fixture must be inside this repository build directory')
    if any(Path(name).name!=name or not name.endswith('.jar') for name in args.remove_mod):parser.error('Use exact JAR filenames')
    if 'level-name=world' not in (run/'server.properties').read_text():parser.error('Fixture must use its local world directory')
    world=run/'world';journal=world/'data/relics_distribution_v1.json';original=journal.read_bytes()
    state=json.loads(json.loads(original)['payload'])
    if not state.get('frozen') or not state.get('unique'):parser.error('Provide a frozen modpack fixture with a resolved Colossus target')
    evidence=world/'data/relics_planning_environment_v1.json'
    if evidence.exists():
        shutil.copy2(evidence,run/'environment-before-test.json');evidence.unlink()
    shutil.copy2(artifact,run/'mods'/artifact.name)
    mods=[run/'mods'/name for name in args.remove_mod]
    if not all(path.exists() for path in mods):parser.error('Restore all fixture mods before testing')
    def hashes():
        return {p.relative_to(world).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in world.rglob('*') if p.is_file() and p.name!='session.lock'}
    def protected(values):
        return {name:hash for name,hash in values.items() if (('relics' in Path(name).name and name!='data/relics_planning_environment_v1.json')
                or Path(name).name.startswith('map_') or name.startswith(('playerdata/','advancements/')))}
    progress=protected(hashes());report=dict(artifact_sha256=hashlib.sha256(artifact.read_bytes()).hexdigest(),protected_files=len(progress),passed=False,cases=[])
    try:
        for case in ('without-evidence','original','without-seasons','restored'):
            removed=case in ('without-evidence','without-seasons')
            for path in mods:
                disabled=path.with_suffix('.jar.disabled')
                if removed and path.exists():path.rename(disabled)
                if not removed and disabled.exists():disabled.rename(path)
            before=hashes();process=subprocess.Popen([str(args.java.resolve()),'@'+str(run/'args.txt')],cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            console=Console(process,run/f'guard-{case}.log',echo=False);started=False
            try:
                deadline=time.monotonic()+180
                while process.poll() is None:
                    if any('Done (' in line for line in console.lines):started=True;process.stdin.write('stop\n');process.stdin.flush();break
                    if time.monotonic()>deadline:raise TimeoutError(case)
                    time.sleep(.1)
                process.wait(timeout=120);console.thread.join(timeout=5)
            finally:
                if process.poll() is None:process.terminate();process.wait(timeout=15)
            after=hashes();text=''.join(console.lines);rejected='Relic world load rejected before saving' in text
            assert journal.read_bytes()==original,'Relic plan was rewritten'
            assert protected(after)==progress,'Maps, player progress or relic journals changed'
            if case=='without-evidence':assert not started and rejected and before==after,'Rejected modpack load changed world files'
            else:assert started and not rejected and process.returncode==0,'Supported modpack setup did not start'
            report['cases'].append(dict(case=case,started=started,rejected=rejected,exit_code=process.returncode,
                    world_file_count=len(before),all_world_files_unchanged=before==after,journal_byte_identical=True,
                    maps_progress_and_targets_unchanged=True,changed=[name for name in sorted(set(before)|set(after)) if before.get(name)!=after.get(name)]))
            print(json.dumps(report['cases'][-1]),flush=True)
        report['passed']=True
    finally:
        for path in mods:
            disabled=path.with_suffix('.jar.disabled')
            if disabled.exists() and not path.exists():disabled.rename(path)
        (run/'world-load-modpack-evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
