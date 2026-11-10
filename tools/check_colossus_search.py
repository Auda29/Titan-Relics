"""Serial destination-search checks using an existing isolated Fabric modpack fixture.

Reads the fixture's absolute-classpath args.txt, mods and config. Creates fresh
worlds below build only; never opens a launcher save or generates distant chunks.
Use revision 2 with a released artifact for an explicit historical control.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import socket
import subprocess
import time
import zipfile

from compile_worldgen import ROOT
from smoke_server import Console


def snapshot(run):
    envelope = json.loads((run/'world/data/relics_distribution_v1.json').read_text())
    assert envelope['version'] == 1
    assert hashlib.sha256(envelope['payload'].encode()).hexdigest() == envelope['sha256']
    return json.loads(envelope['payload'])


def shutdown(process):
    if process.poll() is not None:
        return
    try:
        process.stdin.write('stop\n')
        process.stdin.flush()
        process.wait(timeout=30)
    except (BrokenPipeError, OSError, subprocess.TimeoutExpired):
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=10)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture', type=Path, required=True)
    parser.add_argument('--artifact', type=Path, required=True)
    parser.add_argument('--java', type=Path, required=True)
    parser.add_argument('--checks', type=Path, help='Remapped 1.21.1 test JAR containing ColossusSearchBootChecks, to disable spawn-area pregeneration only')
    parser.add_argument('--seed', type=int, action='append', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--revision', type=int, choices=(2, 3), default=3)
    parser.add_argument('--restart', action='store_true')
    parser.add_argument('--resume', action='store_true', help='Resume recorded launches in this output directory without replacing worlds or evidence')
    parser.add_argument('--timeout', type=int, default=600)
    parser.add_argument('--accept-eula', action='store_true')
    args = parser.parse_args()
    fixture, output, artifact = args.fixture.resolve(), args.output.resolve(), args.artifact.resolve()
    if not args.accept_eula:
        parser.error('Accept the Minecraft EULA for these isolated test worlds')
    if not fixture.is_relative_to(ROOT/'build') or not output.is_relative_to(ROOT/'build'):
        parser.error('Fixture and output must remain below this repository build directory')
    if not 60 <= args.timeout <= 900:
        parser.error('Timeout must be between 60 and 900 seconds per server launch')
    if len(set(args.seed)) != len(args.seed):
        parser.error('Each seed may occur only once per output directory')
    output.mkdir(parents=True, exist_ok=True)
    baseline = fixture/'console.log'
    baseline_messages = set()
    if baseline.exists():
        for line in baseline.read_text(errors='replace').splitlines():
            match = re.search(r"\[main/ERROR\]: (No data fixer registered for.*|Registry 'moonlight:(?:world_saved_data_type|custom_map_data_types)' was empty after loading)$", line)
            if match:
                baseline_messages.add(match.group(1).strip())

    def classify_errors(lines):
        known, unexpected = [], []
        for line in lines:
            if '/ERROR]' not in line:
                continue
            message = line.split('[main/ERROR]: ', 1)[-1].strip()
            if message in baseline_messages:
                known.append(message)
            elif '[Yggdrasil Key Fetcher/ERROR]' in line and 'Failed to request yggdrasil public key' in line:
                known.append(line)
            else:
                unexpected.append(line)
        return known, unexpected

    diagnostic = None
    if args.checks:
        diagnostic = output/'colossus-search-boot-checks.jar'
        with zipfile.ZipFile(args.checks) as source:
            name = 'de/relics/ColossusSearchBootChecks.class'
            bytecode = source.read(name)
        metadata = {'schemaVersion': 1, 'id': 'relics-colossus-search-boot-checks',
                'version': '1', 'environment': 'server', 'entrypoints': {'main': ['de.relics.ColossusSearchBootChecks']},
                'depends': {'minecraft': '1.21.1', 'relics': '*', 'fabric-lifecycle-events-v1': '*'}}
        if diagnostic.exists():
            with zipfile.ZipFile(diagnostic) as previous:
                assert previous.read(name) == bytecode and json.loads(previous.read('fabric.mod.json')) == metadata
        else:
            with zipfile.ZipFile(diagnostic, 'w', zipfile.ZIP_DEFLATED) as target:
                for path,content in ((name, bytecode), ('fabric.mod.json', json.dumps(metadata).encode())):
                    entry = zipfile.ZipInfo(path, (2026, 1, 1, 0, 0, 0))
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    target.writestr(entry, content)
    report = {'artifact_sha256': hashlib.sha256(artifact.read_bytes()).hexdigest(),
              'revision': args.revision, 'spawn_area_pregeneration_disabled': diagnostic is not None,
              'checks_sha256': hashlib.sha256(diagnostic.read_bytes()).hexdigest() if diagnostic else None,
              'complete': False, 'runs': []}
    if args.resume:
        evidence = output/'evidence.json'
        previous = json.loads(evidence.read_text())
        for key in ('artifact_sha256', 'revision', 'checks_sha256', 'spawn_area_pregeneration_disabled'):
            assert previous[key] == report[key], f'Cannot resume different audit inputs: {key}'
        assert [item['seed'] for item in previous['runs']] == args.seed[:len(previous['runs'])]
        backup = output/f'evidence.before-resume-{time.time_ns()}.json'
        shutil.copy2(evidence, backup)
        report = previous
        report['complete'] = False
        report.pop('failure', None)
    report['baseline_log_sha256'] = hashlib.sha256(baseline.read_bytes()).hexdigest() if baseline.exists() else None
    report['known_fixture_error_messages'] = sorted(baseline_messages)
    try:
        for seed in args.seed:
            run = output/f'seed-{seed}'
            item = next((item for item in report['runs'] if item['seed'] == seed), None)
            if item is None:
                run.mkdir(exist_ok=False)
                (run/'mods').mkdir()
                for source in sorted((fixture/'mods').glob('*.jar')):
                    with zipfile.ZipFile(source) as archive:
                        metadata = json.loads(archive.read('fabric.mod.json'))
                    if metadata['id'] == 'relics' or metadata['id'].startswith('relics-'):
                        continue
                    shutil.copy2(source, run/'mods'/source.name)
                shutil.copy2(artifact, run/'mods'/artifact.name)
                if diagnostic:
                    shutil.copy2(diagnostic, run/'mods'/diagnostic.name)
                shutil.copytree(fixture/'config', run/'config')
                defaults = run/'config/relics-distribution.json'
                if defaults.exists():
                    defaults.rename(defaults.with_suffix('.fixture.json'))
                families = {name: dict(mode='LANDSCAPES', selected=[]) for name in
                            ('colossus', 'obelisk', 'titan_skull', 'titan_skull_2', 'ruined_tower', 'small_colossus', 'world_tree')}
                defaults.write_text(json.dumps({'format': 1, 'settings': dict(cellSize=2000, minDistance=800,
                    obeliskDistance=6000, regionRadius=2400, colossusMinDistance=4000, generationRevision=args.revision,
                    outside=[3000,1500,1500,200,200,200], inside=[3000,2500,2500,200,200,200], biomes={'families': families})}))
                with socket.socket() as sock:
                    sock.bind(('127.0.0.1', 0))
                    port = sock.getsockname()[1]
                properties = {'server-ip': '127.0.0.1', 'server-port': port, 'online-mode': 'true',
                    'white-list': 'true', 'enforce-whitelist': 'true', 'level-seed': seed, 'level-name': 'world',
                    'view-distance': 2, 'simulation-distance': 2, 'max-tick-time': 180000, 'spawn-protection': 0}
                (run/'server.properties').write_text(''.join(f'{key}={value}\n' for key,value in properties.items()))
                (run/'eula.txt').write_text('eula=true\n')
                item = {'seed': seed, 'launches': []}
                report['runs'].append(item)
            original = item['launches'][0]['snapshot'] if item['launches'] else None
            if original is not None:
                assert snapshot(run) == original and item['last_exit_code'] == 0
                for iteration in range(len(item['launches'])):
                    known, errors = classify_errors((run/f'console-{iteration}.log').read_text().splitlines())
                    assert not errors, errors
                    item['launches'][iteration]['known_fixture_errors'] = known
            for iteration in range(len(item['launches']), 2 if args.restart else 1):
                started = time.monotonic()
                process = subprocess.Popen([str(args.java.resolve()), '@'+str(fixture/'args.txt')], cwd=run,
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding='utf-8', errors='replace', bufsize=1, start_new_session=True)
                console = Console(process, run/f'console-{iteration}.log', echo=False)
                try:
                    console.wait(r'Done \(', timeout=args.timeout)
                    while True:
                        current = snapshot(run)
                        if current.get('unique') or current.get('unavailable'):
                            break
                        if process.poll() is not None:
                            raise RuntimeError('Server exited during destination search')
                        if time.monotonic()-started > args.timeout:
                            raise TimeoutError('Destination search exceeded the bounded audit timeout')
                        time.sleep(.25)
                    assert current['seed'] == seed and current['settings']['generationRevision'] == args.revision
                    assert current['unique'] and not current['unavailable'], current
                    policy = 'relics-distribution-v5-colossus-search' if args.revision == 3 else 'relics-distribution-v4-discoveries'
                    assert current['policy'] == policy
                    destination = current['unique']
                    distance = math.hypot(destination['x2']/2-current['spawnX'], destination['z2']/2-current['spawnZ'])
                    assert distance >= 4000
                    if args.revision == 3:
                        progress = current['colossusSearch']
                        checked = progress['coarseChecked']+progress['refinementChecked']
                        assert checked == current['candidatesChecked'] == sum(progress['rejected'].values())+1
                    if original is None:
                        original = current
                    else:
                        assert current == original, 'Completed destination or diagnostic state changed after restart'
                    item['launches'].append({'restart': bool(iteration), 'seconds': round(time.monotonic()-started, 3),
                                             'distance': distance, 'snapshot': current})
                    print(f'PASS seed={seed} restart={bool(iteration)} distance={distance:.1f} checked={current["candidatesChecked"]}', flush=True)
                finally:
                    shutdown(process)
                    console.thread.join(timeout=5)
                    item['last_exit_code'] = process.returncode
                known, errors = classify_errors(console.lines)
                item['launches'][-1]['known_fixture_errors'] = known
                assert process.returncode == 0 and not errors, errors
        report['complete'] = True
    except Exception as error:
        report['failure'] = str(error)
        raise
    finally:
        (output/'evidence.json').write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
