"""Serial native-generator audit in an existing isolated Linux modpack fixture.

Never opens a launcher profile. --checks is a remapped Fabric 1.21.1 test JAR
containing DiscoveryBalanceChecks; only that diagnostic class is loaded.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import time
import zipfile

from compile_worldgen import ROOT
from smoke_server import Console
from verify_world import verify_world


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, value):
    temporary = path.with_suffix('.pending')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--fixture', type=Path, required=True)
    ap.add_argument('--artifact', type=Path, required=True)
    ap.add_argument('--checks', type=Path, required=True)
    ap.add_argument('--java', type=Path, required=True)
    ap.add_argument('--seed', type=int, action='append', required=True)
    ap.add_argument('--half-window', type=int, default=12000)
    ap.add_argument('--output', type=Path, default=ROOT/'build/discovery-balance-20261110')
    ap.add_argument('--accept-eula', action='store_true')
    ap.add_argument('--preserve-fixture', action='store_true')
    ap.add_argument('--verify-placement', action='store_true')
    args = ap.parse_args()
    fixture, output, artifact = args.fixture.resolve(), args.output.resolve(), args.artifact.resolve()
    if not args.accept_eula:
        ap.error('Accept the Minecraft EULA for these isolated test worlds')
    if not fixture.is_relative_to(ROOT/'build') or not output.is_relative_to(ROOT/'build'):
        ap.error('Fixture and output must be isolated below this repository build directory')
    if not 2000 <= args.half_window <= 20000:
        ap.error('Half-window must stay within the bounded 2,000–20,000 block audit range')
    output.mkdir(parents=True, exist_ok=True)
    diagnostic = output/'discovery-balance-checks.jar'
    with zipfile.ZipFile(args.checks) as original, zipfile.ZipFile(diagnostic, 'w', zipfile.ZIP_DEFLATED) as target:
        classes = [n for n in original.namelist() if n.startswith('de/relics/DiscoveryBalanceChecks') and n.endswith('.class')]
        if not classes:
            ap.error('Checks JAR does not contain the remapped DiscoveryBalanceChecks class')
        for name in classes:
            target.writestr(name, original.read(name))
        target.writestr('fabric.mod.json', json.dumps({'schemaVersion': 1, 'id': 'relics-discovery-audit',
            'version': '1', 'environment': 'server', 'entrypoints': {'main': ['de.relics.DiscoveryBalanceChecks']},
            'depends': {'relics': '*'}}))
    evidence = {'artifact_sha256': digest(artifact), 'checks_sha256': digest(diagnostic), 'runs': []}
    write(output/'evidence.json', evidence)

    def prepare(label, seed, preserve):
        run = output/label
        run.mkdir(exist_ok=False)
        shutil.copytree(fixture/'mods', run/'mods')
        for path in (run/'mods').glob('*.jar'):
            with zipfile.ZipFile(path) as jar:
                if json.loads(jar.read('fabric.mod.json'))['id'] == 'relics':
                    path.unlink()
        shutil.copy2(artifact, run/'mods'/artifact.name)
        shutil.copytree(fixture/'config', run/'config')
        defaults = run/'config/relics-distribution.json'
        if defaults.exists():
            defaults.rename(defaults.with_suffix('.source.json'))
        if preserve:
            shutil.copytree(fixture/'world', run/'world')
        else:
            shutil.copy2(diagnostic, run/'mods'/diagnostic.name)
        (run/'eula.txt').write_text('eula=true\n')
        (run/'server.properties').write_text('server-ip=127.0.0.1\nserver-port=25596\nonline-mode=true\n'
            'white-list=true\nenforce-whitelist=true\nenable-rcon=false\nenable-query=false\n'
            'level-name=world\nview-distance=2\nsimulation-distance=2\nmax-tick-time=180000\n'
            f'level-seed={seed}\n')
        return run

    cases = [('legacy-preservation', 0, True)] if args.preserve_fixture else []
    cases += [(f'seed-{seed}', seed, False) for seed in args.seed]
    for index, (label, seed, preserve) in enumerate(cases):
        run = prepare(label, seed, preserve)
        unit = f'relics-balance-audit-{os.getpid()}-{index}'
        command = ['systemd-run', '--user', '--scope', '--quiet', '--unit='+unit, '-p', 'MemoryMax=5G',
            '-p', 'CPUQuota=100%', '-p', 'IOWeight=10', 'nice', '-n', '15', 'ionice', '-c', '3',
            str(args.java.resolve()), '-Drelics.balanceHalfWindow='+str(args.half_window), '@'+str(fixture/'args.txt')]
        protected = {n: (run/'world/data'/n).read_bytes() for n in ('relics_distribution_v1.json', 'relics_gameplay_v1.json')} if preserve else {}
        record = {'label': label, 'seed': seed, 'passed': False}
        print('START', label, flush=True)
        p = subprocess.Popen(command, cwd=run, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace', bufsize=1, start_new_session=True)
        console = Console(p, run/'console.log', echo=False)
        try:
            console.wait(r'Done \(', timeout=600)
            if preserve:
                known = fixture/'locate-results.json'
                expected = [q for q in json.loads(known.read_text())['queries'] if q['origin']=='spawn' and q['type'] in ('obelisk','titan_skull')] if known.exists() else []
                snapshot = json.loads(json.loads(protected['relics_distribution_v1.json'])['payload'])
                origin_x, origin_z = snapshot['spawnX'], snapshot['spawnZ']
                for point in expected:
                    line = console.command(f'execute positioned {origin_x} 80 {origin_z} run locate structure #relics:'+point['type'], r'The nearest .* is at|Relikt-Suche angehalten', timeout=360)
                    match = re.search(r'is at \[(-?\d+), ~, (-?\d+)\]', line)
                    assert match and tuple(map(int, match.groups())) == (point['x'], point['z']), line
                record['known_locates_reproduced'] = len(expected)
            else:
                deadline, previous = time.monotonic()+1800, None
                while True:
                    if p.poll() is not None:
                        raise RuntimeError('Server exited before audit completed')
                    if (run/'balance-failure.txt').exists():
                        raise RuntimeError((run/'balance-failure.txt').read_text())
                    progress = (run/'balance-progress.txt').read_text().strip() if (run/'balance-progress.txt').exists() else 'waiting'
                    if progress != previous:
                        print(label, progress, flush=True); previous = progress
                    try:
                        audit = json.loads((run/'balance-audit.json').read_text())
                        if audit.get('complete'):
                            break
                    except (FileNotFoundError, json.JSONDecodeError):
                        pass
                    if time.monotonic() > deadline:
                        raise TimeoutError('Bounded native audit exceeded 30 minutes')
                    time.sleep(2)
                record['cases'] = {name: {k: v for k, v in result.items() if k not in ('sites', 'colossus', 'settings', 'slope_only_sites', 'expanded_crown_sites')} for name, result in audit['cases'].items()}
                if args.verify_placement and seed == args.seed[0]:
                    selected = []
                    for family in ('titan_skull', 'titan_skull_2'):
                        choices = [s for s in audit['cases']['discoveries']['sites'] if s['asset']==family or family=='titan_skull' and s['asset'].startswith('titan_skull_') and s['asset']!='titan_skull_2']
                        if not choices:
                            raise AssertionError('No accepted natural '+family+' in verification window')
                        preferred = audit['cases']['discoveries']['slope_only_sites' if family=='titan_skull_2' else 'expanded_crown_sites']
                        site = preferred[0] if preferred else choices[0]; selected.append(site)
                        x1,z1,x2,z2 = site['minX'],site['minZ'],site['maxX'],site['maxZ']
                        console.command(f'forceload add {x1} {z1} {x2} {z2}', r'Marked|force.loaded|already|No chunks', timeout=60)
                        for x,z in ((x1,z1),(x2,z1),(x1,z2),(x2,z2)):
                            loaded_deadline = time.monotonic()+180
                            while 'Test passed' not in console.command(f'execute if loaded {x} 80 {z}', r'Test passed|Test failed', timeout=30):
                                if time.monotonic()>loaded_deadline:
                                    raise TimeoutError('Natural target chunk did not finish')
                                time.sleep(1)
                    console.command('save-all flush', r'Saved the game', timeout=90)
                    for site in selected:
                        console.command(f'forceload remove {site["minX"]} {site["minZ"]} {site["maxX"]} {site["maxZ"]}', r'Unmarked|not marked|No chunks', timeout=60)
                    record['naturally_generated_assets'] = [s['asset'] for s in selected]
            console.command('stop')
            p.wait(timeout=90)
            assert p.returncode == 0, p.returncode
            for name, raw in protected.items():
                assert (run/'world/data'/name).read_bytes() == raw, 'Frozen plan or reward ledger changed'
            if preserve:
                record['plan_and_reward_ledger_byte_identical'] = True
            if record.get('naturally_generated_assets'):
                verification = verify_world(run/'world', artifact, {'relics:'+name for name in record['naturally_generated_assets']})
                write(run/'natural-block-verification.json', verification)
                if not verification['passed']:
                    raise AssertionError('Natural block/contact verification failed; see '+str(run/'natural-block-verification.json'))
                record['natural_block_verification_passed'] = True
            record['passed'] = True
        except BaseException as error:
            record['error'] = str(error)
            raise
        finally:
            if p.poll() is None:
                try:
                    console.command('stop'); p.wait(timeout=20)
                except Exception:
                    subprocess.run(['systemctl', '--user', 'kill', '--kill-whom=all', '--signal=SIGTERM', unit+'.scope'], capture_output=True)
                    try: p.wait(timeout=15)
                    except subprocess.TimeoutExpired:
                        subprocess.run(['systemctl', '--user', 'kill', '--kill-whom=all', '--signal=SIGKILL', unit+'.scope'], capture_output=True)
                        os.killpg(p.pid, signal.SIGKILL); p.wait(timeout=10)
            console.thread.join(timeout=5)
            record['exit_code'] = p.returncode
            evidence['runs'].append(record); write(output/'evidence.json', evidence)
        print('PASS', label, flush=True)


if __name__ == '__main__':
    main()
