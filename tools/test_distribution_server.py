"""Isolated production-loader proof for distribution, asynchronous locate and saved natural starts.

Uses local checksum-verified dependencies. Never installs into a launcher profile.
Requires explicit --accept-eula, creates new worlds and reloads only those worlds.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import time
import uuid
from compile_worldgen import ROOT, compile_libraries
from smoke_server import Console, inspect_world
import tempfile
import zipfile


def snapshot(run):
    envelope = json.loads((run / 'world/data/relics_distribution_v1.json').read_text())
    assert hashlib.sha256(envelope['payload'].encode()).hexdigest() == envelope['sha256']
    return json.loads(envelope['payload'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--accept-eula', action='store_true')
    parser.add_argument('--java', type=Path, required=True)
    parser.add_argument('--artifact', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=731204)
    parser.add_argument('--interrupt', action='store_true', help='Stop during a pending search, then resume and reload')
    parser.add_argument('--max-world-size', type=int, default=29999984)
    parser.add_argument('--preset', choices=('expedition', 'balanced', 'discovery'), default='expedition')
    args = parser.parse_args()
    if not args.accept_eula:
        parser.error('Read https://aka.ms/MinecraftEULA and pass --accept-eula for this isolated server')
    run = ROOT / 'build/distribution-runtime' / f'{args.seed}-{uuid.uuid4().hex[:8]}'
    (run / 'mods').mkdir(parents=True)
    if args.preset != 'expedition':
        cell, distance, obelisks, region, colossus = {'balanced': (3000, 1200, 9000, 3600, 15000),
                                                   'discovery': (2000, 800, 6000, 2400, 8000)}[args.preset]
        creation = run / 'world/data/relics_creation_settings.json'
        creation.parent.mkdir(parents=True)
        creation.write_text(json.dumps({'format': 1, 'settings': {'cellSize': cell, 'minDistance': distance,
                            'obeliskDistance': obelisks, 'regionRadius': region, 'colossusMinDistance': colossus,
                            'outside': [3000, 250, 250, 200, 200, 200], 'inside': [3000, 1500, 1500, 200, 200, 200]}}), encoding='utf-8')
    libraries = compile_libraries()
    cp = [p for p in libraries if p.name == 'fabric-loader-0.19.5.jar'
          or any(part in {'libraries', 'loader-libraries', 'versions'} for part in p.parts)]
    for artifact in [args.artifact.resolve(), ROOT / 'build/worldgen-dependencies/fabric-api-0.161.0+26.2.jar',
                     ROOT / 'build/worldgen-dependencies/lithostitched-1.8.0-fabric-26.2.jar']:
        shutil.copy2(artifact, run / 'mods' / artifact.name)
    # Test-only lifecycle checks never enter the player artifact.
    compiler = args.java.resolve().with_name('javac.exe' if os.name == 'nt' else 'javac')
    with tempfile.TemporaryDirectory(dir=ROOT / 'build', prefix='distribution-runtime-checks-') as directory:
        subprocess.run([str(compiler), '--release', '25', '-proc:none', '-encoding', 'UTF-8',
                        '-classpath', os.pathsep.join(map(str, [args.artifact.resolve(), *libraries])),
                        '-d', directory, str(ROOT / 'src/test/java/de/relics/DistributionRuntimeChecks.java')], check=True)
        with zipfile.ZipFile(run / 'mods/distribution-runtime-checks.jar', 'w') as archive:
            for path in Path(directory).rglob('*.class'):
                archive.write(path, path.relative_to(directory).as_posix())
            archive.writestr('fabric.mod.json', json.dumps({'schemaVersion': 1, 'id': 'relics-distribution-runtime-checks',
                            'version': '1', 'environment': 'server', 'entrypoints': {'main': ['de.relics.DistributionRuntimeChecks']},
                            'depends': {'relics': '*', 'fabric-lifecycle-events-v1': '*'}}))
            with zipfile.ZipFile(args.artifact) as production:
                manifest = json.loads(production.read('relics.integration.json'))
            archive.writestr('data/relics/tags/worldgen/structure/distribution_runtime_repeatables.json',
                            json.dumps({'values': ['relics:' + a['id'] for a in manifest['structures'] if a['family'] != 'colossus']}))
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    properties = {'server-ip': '127.0.0.1', 'server-port': port, 'online-mode': 'true',
                  'white-list': 'true', 'enforce-whitelist': 'true', 'max-players': 1,
                  'enable-query': 'false', 'enable-rcon': 'false', 'level-name': 'world',
                  'level-seed': args.seed, 'generate-structures': 'true', 'gamemode': 'creative',
                  'difficulty': 'peaceful', 'view-distance': 2, 'simulation-distance': 2,
                  'pause-when-empty-seconds': 0, 'max-tick-time': 60000, 'max-world-size': args.max_world_size}
    (run / 'server.properties').write_text(''.join(f'{k}={v}\n' for k, v in properties.items()))
    (run / 'eula.txt').write_text('eula=true\n')
    arguments = ['-Xms512M', '-Xmx4G', '-Djava.awt.headless=true', '-cp', os.pathsep.join(map(str, cp)),
                 'net.fabricmc.loader.impl.launch.knot.KnotServer', 'nogui']
    argfile = run / 'java-args.txt'
    argfile.write_text('\n'.join('"' + a.replace('\\', '/') + '"' for a in arguments))
    evidence = {'seed': args.seed, 'preset': args.preset, 'artifact_sha256': hashlib.sha256(args.artifact.read_bytes()).hexdigest(),
                'run': str(run.relative_to(ROOT)), 'passes': [], 'commands': []}
    print(f'Isolated distribution server: {run}', flush=True)
    first = None
    for iteration in range(3 if args.interrupt else 2):
        process = subprocess.Popen([str(args.java.resolve()), '@' + str(argfile)], cwd=run,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, encoding='utf-8', errors='replace', bufsize=1,
                                   creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        console = Console(process, run / f'console-{iteration}.log', echo=False)
        def command(text, pattern, timeout=120):
            started = time.monotonic()
            response = console.command(text, pattern, timeout)
            evidence['commands'].append({'command': text, 'response': response,
                                         'seconds': round(time.monotonic() - started, 4)})
            return response
        try:
            console.wait(r'Done \(', timeout=180)
            command('relicsdistribution status', r'\{"policy"')
            if args.interrupt and iteration == 0:
                current = snapshot(run)
                assert current['frozen'] and not current.get('unique') and current['candidatesChecked'] > 0, current
                command('stop', r'Stopping the server')
                process.wait(timeout=120)
                console.thread.join(timeout=5)
                assert not [line for line in console.lines if '/ERROR]' in line], console.lines[-30:]
                evidence['interrupted_snapshot'] = snapshot(run)
                evidence['passes'].append('stopped while unique search remained pending; persisted cursor retained')
                print('PASS controlled interruption during pending search', flush=True)
                continue
            console.wait(r'Relic distribution (map|unavailable) checks passed', timeout=180)
            current = snapshot(run)
            if current['unavailable']:
                assert args.max_world_size < 20000 and not current.get('unique'), current
                assert current['unavailableReason'] == 'finite frozen world border exhausted'
                command('locate structure relics:colossus', r'Kein.*Ziel')
                command('save-all flush', r'Saved the game')
                command('stop', r'Stopping the server')
                process.wait(timeout=120); console.thread.join(timeout=5)
                assert not [line for line in console.lines if '/ERROR]' in line]
                inspection = inspect_world(run / 'world')
                assert not inspection['read_errors'] and not inspection['natural_structure_starts']
                evidence['unavailable_snapshot'] = current
                evidence['passes'].append(f'iteration {iteration}: finite border exhaustion persisted; no fake target/map/start')
                print(f'PASS unavailable destination iteration {iteration}', flush=True)
                continue
            assert current['frozen'] and current.get('unique') and not current['unavailable'], current
            configured_minimum = {'expedition': 30000, 'balanced': 15000, 'discovery': 8000}[args.preset]
            assert current['settings']['colossusMinDistance'] == configured_minimum, current
            unique = current['unique']
            assert ((unique['x2'] / 2 - current['spawnX']) ** 2
                    + (unique['z2'] / 2 - current['spawnZ']) ** 2) >= current.get('settings', {}).get('colossusMinDistance', 30000) ** 2
            if first is None:
                first = current
            else:
                for field in ('unique', 'seed', 'spawnX', 'spawnZ', 'fingerprint'):
                    assert current[field] == first[field], field
                evidence['passes'].append('target and original spawn unchanged after restart and setworldspawn')
            for prefix in ('', 'execute positioned 50000 80 -50000 run '):
                response = command(prefix + 'locate structure relics:colossus', r'nearest.*relics:colossus.*is at')
                assert f"[{unique['x2'] // 2}, ~, {unique['z2'] // 2}]" in response, response
            evidence['passes'].append(f'iteration {iteration}: global locate from two origins agrees with journal')
            if first is current:
                response = command('locate structure #relics:distribution_runtime_repeatables',
                                   r'nearest.*repeatables.*is at|Kein.*Ziel', timeout=180)
                match = re.search(r'\[(-?\d+), ~, (-?\d+)\]', response)
                if match:
                    rx, rz = map(int, match.groups())
                    response = command(f'relicsdistribution plan {rx} {rz}', r'Relic plan Cell', timeout=180)
                    planned = json.loads(response.split(': ', 2)[-1])
                    assert planned and planned['asset'] != 'colossus', response
                    evidence['ordinary_site'] = planned
                    response2 = command(f'relicsdistribution plan {rx} {rz}', r'Relic plan Cell')
                    assert json.loads(response2.split(': ', 2)[-1]) == planned
                    command(f'forceload add {rx} {rz}', r'Marked|force.loaded')
                else:
                    evidence['passes'].append('bounded repeatable search returned no confirmed site; no replacement roll')
                x = unique['candidate']['x']
                z = unique['candidate']['z']
                command(f'forceload add {x} {z}', r'Marked|force.loaded')
                deadline = time.monotonic() + 120
                while True:
                    response = command(f'execute if loaded {x} 80 {z}', r'Test passed|Test failed')
                    if 'Test passed' in response:
                        break
                    if time.monotonic() > deadline:
                        raise TimeoutError('Natural destination chunk did not finish')
                    time.sleep(.5)
                command('setworldspawn 8000 80 -8000', r'Set the world spawn')
                reload_start = len(console.lines)
                command('reload', r'Reloading')
                console.wait(r'Relic distribution settings unchanged after datapack reload', start=reload_start, timeout=120)
                evidence['passes'].append('unchanged datapack reload retains planning snapshot')
                command('save-all flush', r'Saved the game')
            command('relicsdistribution status', r'\{"policy"')
            command('stop', r'Stopping the server')
            process.wait(timeout=120)
            console.thread.join(timeout=5)
            assert process.returncode == 0, process.returncode
            errors = [line for line in console.lines if '/ERROR]' in line or 'Exception in thread' in line]
            assert not errors, errors
            inspection = inspect_world(run / 'world')
            assert not inspection['read_errors'], inspection['read_errors']
            starts = [s for s in inspection['natural_structure_starts'] if s['structure'] == 'relics:colossus']
            assert len(starts) == 1, starts
            start = starts[0]
            assert start['chunk'] == [unique['candidate']['x'] // 16, unique['candidate']['z'] // 16]
            box = start['bounding_boxes'][0]
            assert box[0] + box[3] == unique['x2'] and box[2] + box[5] == unique['z2'], (box, unique)
            assert [box[0], box[1], box[2], box[3], box[5]] == [unique['minX'], unique['originY'], unique['minZ'], unique['maxX'], unique['maxZ']], (box, unique)
            ordinary = evidence.get('ordinary_site')
            if ordinary:
                found = [s for s in inspection['natural_structure_starts'] if s['structure'] == 'relics:' + ordinary['asset']]
                assert len(found) == 1, inspection
                bounds = found[0]['bounding_boxes'][0]
                assert bounds[0] + bounds[3] == ordinary['x2'] and bounds[2] + bounds[5] == ordinary['z2'], found
                evidence['passes'].append(f'iteration {iteration}: repeatable plan agrees with saved natural geometry')
            evidence['passes'].append(f'iteration {iteration}: exactly one saved natural Colossus start; exact transformed center')
            evidence[f'world_{iteration}'] = inspection
            print(f'PASS production server iteration {iteration}, target {unique["x2"] // 2}, {unique["z2"] // 2}', flush=True)
        finally:
            if process.poll() is None:
                try:
                    process.stdin.write('stop\n'); process.stdin.flush(); process.wait(timeout=30)
                except Exception:
                    process.terminate(); process.wait(timeout=15)
            (run / 'evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')
    print(f'Evidence: {run / "evidence.json"}', flush=True)


if __name__ == '__main__':
    main()
