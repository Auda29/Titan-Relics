"""Audit the supplied production artifact in isolated, real Fabric worlds.

Records every top-level opportunity and explains native terrain rejections.
No tuning, profile installation or edits to existing worlds. The separate audit
mod reads frozen runtime inputs; it is never bundled in the player artifact.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import threading
import time
import zipfile

from compile_worldgen import ROOT, compile_libraries
from smoke_server import Console, inspect_world
from verify_world import verify_world


def mix(value):
    mask = (1 << 64) - 1
    value = ((value ^ (value >> 30)) * 0xbf58476d1ce4e5b9) & mask
    value = ((value ^ (value >> 27)) * 0x94d049bb133111eb) & mask
    value ^= value >> 31
    return value if value < 1 << 63 else value - (1 << 64)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--accept-eula', action='store_true')
    parser.add_argument('--java-home', type=Path, required=True)
    parser.add_argument('--artifact', type=Path, default=ROOT / 'dist/relics-0.1.0-alpha.5.0.2+mc26.2.jar')
    parser.add_argument('--seeds', nargs='+', type=int)
    parser.add_argument('--jobs', type=int, choices=(1, 2), default=2)
    parser.add_argument('--no-natural-checks', action='store_true')
    args = parser.parse_args()
    if not args.accept_eula:
        parser.error('Read https://aka.ms/MinecraftEULA and pass --accept-eula for the isolated test worlds')
    seeds = args.seeds or [731204, -48291736, 20260913] + [mix(20261027 + i) for i in range(27)]
    assert len(seeds) == len(set(seeds))
    destination = ROOT / 'build/distribution-audit-20261027' / datetime.now().strftime('run-%H%M%S')
    destination.mkdir(parents=True)
    artifact = args.artifact.resolve()
    dependencies = compile_libraries()
    classpath = [p for p in dependencies if p.name == 'fabric-loader-0.19.5.jar'
                 or any(part in {'libraries', 'loader-libraries', 'versions'} for part in p.parts)]
    classes = destination / 'audit-classes'
    classes.mkdir()
    subprocess.run([str(args.java_home / 'bin/javac.exe'), '--release', '25', '-encoding', 'UTF-8', '-proc:none',
                    '-classpath', os.pathsep.join(map(str, [artifact, *dependencies])), '-d', str(classes),
                    str(ROOT / 'src/test/java/de/relics/DistributionAuditMod.java')], check=True)
    audit_jar = destination / 'distribution-audit.jar'
    with zipfile.ZipFile(audit_jar, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in classes.rglob('*.class'):
            archive.write(path, path.relative_to(classes).as_posix())
        archive.writestr('fabric.mod.json', json.dumps({'schemaVersion': 1, 'id': 'relics-distribution-audit',
                        'version': '1', 'environment': 'server', 'entrypoints': {'main': ['de.relics.DistributionAuditMod']},
                        'depends': {'relics': '*', 'fabric-lifecycle-events-v1': '*'}}))
    metadata = {'seeds': seeds, 'artifact_sha256': hashlib.sha256(artifact.read_bytes()).hexdigest(),
                'audit_source_sha256': hashlib.sha256((ROOT / 'src/test/java/de/relics/DistributionAuditMod.java').read_bytes()).hexdigest(),
                'audit_jar_sha256': hashlib.sha256(audit_jar.read_bytes()).hexdigest(), 'jobs': args.jobs,
                'window_blocks': [120000, 120000], 'window_center': 'actual frozen initial world spawn',
                'audit_changes_production_rules': False, 'completed': [], 'failures': []}
    (destination / 'manifest.json').write_text(json.dumps(metadata, indent=2) + '\n')
    chosen_assets = set()
    chosen_lock = threading.Lock()

    def run_seed(seed):
        run = destination / str(seed)
        (run / 'mods').mkdir(parents=True)
        for path in [artifact, audit_jar, ROOT / 'build/worldgen-dependencies/fabric-api-0.161.0+26.2.jar',
                     ROOT / 'build/worldgen-dependencies/lithostitched-1.8.0-fabric-26.2.jar']:
            shutil.copy2(path, run / 'mods' / path.name)
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        properties = {'server-ip': '127.0.0.1', 'server-port': port, 'online-mode': 'true', 'white-list': 'true',
                      'enforce-whitelist': 'true', 'max-players': 1, 'enable-rcon': 'false', 'enable-query': 'false',
                      'level-name': 'world', 'level-seed': seed, 'generate-structures': 'true', 'gamemode': 'creative',
                      'difficulty': 'peaceful', 'view-distance': 2, 'simulation-distance': 2,
                      'pause-when-empty-seconds': 0, 'max-tick-time': 60000}
        (run / 'server.properties').write_text(''.join(f'{k}={v}\n' for k, v in properties.items()))
        (run / 'eula.txt').write_text('eula=true\n')
        arguments = ['-Xms256M', '-Xmx3G', '-XX:ActiveProcessorCount=4', '-Djava.awt.headless=true',
                     '-cp', os.pathsep.join(map(str, classpath)), 'net.fabricmc.loader.impl.launch.knot.KnotServer', 'nogui']
        argfile = run / 'java-args.txt'
        argfile.write_text('\n'.join('"' + arg.replace('\\', '/') + '"' for arg in arguments))
        print(f'START seed={seed}', flush=True)
        process = subprocess.Popen([str(args.java_home / 'bin/java.exe'), '@' + str(argfile)], cwd=run,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, encoding='utf-8', errors='replace', bufsize=1,
                                   creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        console = Console(process, run / 'console.log', echo=False)
        commands = []
        def command(text, pattern, timeout=120):
            response = console.command(text, pattern, timeout)
            commands.append({'command': text, 'response': response})
            return response
        try:
            console.wait(r'Done \(', timeout=180)
            ready = console.wait(r'RELIC_AUDIT_READY|RELIC_AUDIT_FAILED', timeout=600)
            if 'FAILED' in ready:
                raise RuntimeError(ready)
            audit = json.loads((run / 'audit.json').read_text())
            selected = []
            if not args.no_natural_checks:
                with chosen_lock:
                    for site in audit['accepted_sites']:
                        if site['asset'] not in chosen_assets:
                            chosen_assets.add(site['asset'])
                            selected.append(site)
                            if len(selected) == 2:
                                break
            for site in selected:
                min_cx, max_cx = site['minX'] // 16, site['maxX'] // 16
                min_cz, max_cz = site['minZ'] // 16, site['maxZ'] // 16
                for column in range(min_cx, max_cx + 1, 8):
                    end = min(column + 7, max_cx)
                    command(f'forceload add {column * 16} {min_cz * 16} {end * 16 + 15} {max_cz * 16 + 15}', r'Marked|force.loaded')
                # Await every footprint chunk, not only its start/corners.
                pending = [(x, z) for x in range(min_cx, max_cx + 1) for z in range(min_cz, max_cz + 1)]
                deadline = time.monotonic() + 180
                while pending:
                    pending = [(x, z) for x, z in pending if 'Test passed' not in
                               command(f'execute if loaded {x * 16} 80 {z * 16}', r'Test passed|Test failed')]
                    if time.monotonic() >= deadline:
                        raise TimeoutError(f'Natural footprint incomplete: {site["asset"]}, {len(pending)} chunks')
                    if pending:
                        time.sleep(.5)
                command('save-all flush', r'Saved the game')
                command('forceload remove all', r'Unmarked|Removed|No chunks|force.loaded')
            command('save-all flush', r'Saved the game')
            command('stop', r'Stopping the server')
            process.wait(timeout=120)
            console.thread.join(timeout=5)
            assert process.returncode == 0
            assert not [line for line in console.lines if '/ERROR]' in line], console.lines[-30:]
            inspection = inspect_world(run / 'world')
            assert not inspection['read_errors'], inspection
            for site in selected:
                matching = [s for s in inspection['natural_structure_starts']
                            if s['structure'] == 'relics:' + site['asset']
                            and s['chunk'] == [site['candidate']['x'] // 16, site['candidate']['z'] // 16]]
                assert len(matching) == 1, (site, inspection)
                box = matching[0]['bounding_boxes'][0]
                assert [box[0], box[2], box[3], box[5]] == [site['minX'], site['minZ'], site['maxX'], site['maxZ']]
            proof = {'seed': seed, 'selected_sites': selected, 'saved_world': inspection, 'commands': commands}
            if selected:
                verification = verify_world(run / 'world', artifact, {'relics:' + site['asset'] for site in selected})
                proof['block_verification'] = verification
                # Keep actual failures as evidence; never label incomplete or
                # mismatching geometry a successful block-level verification.
                if not verification['passed']:
                    proof['block_verification_failed'] = True
            (run / 'natural-proof.json').write_text(json.dumps(proof, indent=2) + '\n')
            print(f'PASS seed={seed} cells={audit["cell_count"]} accepted={len(audit["accepted_sites"])} outcomes={audit["outcomes"]}', flush=True)
            return {'seed': seed, 'path': run.relative_to(ROOT).as_posix(), 'cell_count': audit['cell_count'],
                    'outcomes': audit['outcomes'], 'accepted_by_family': audit['accepted_by_family'],
                    'accepted_sites': audit['accepted_sites'], 'natural_checked': [site['asset'] for site in selected],
                    'natural_passed': proof.get('block_verification', {}).get('passed'),
                    'audit_sha256': hashlib.sha256((run / 'audit.json').read_bytes()).hexdigest(),
                    'natural_proof_sha256': hashlib.sha256((run / 'natural-proof.json').read_bytes()).hexdigest(),
                    'console_sha256': hashlib.sha256((run / 'console.log').read_bytes()).hexdigest()}
        finally:
            if process.poll() is None:
                try:
                    process.stdin.write('stop\n');process.stdin.flush();process.wait(timeout=30)
                except Exception:
                    process.terminate();process.wait(timeout=15)

    print(f'AUDIT {destination}', flush=True)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(run_seed, seed): seed for seed in seeds}
        for future in as_completed(futures):
            seed = futures[future]
            try:
                metadata['completed'].append(future.result())
            except Exception as error:
                metadata['failures'].append({'seed': seed, 'error': str(error)})
                print(f'FAIL seed={seed}: {error}', flush=True)
            (destination / 'manifest.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(f'FINISHED {len(metadata["completed"])}/{len(seeds)}; manifest {destination / "manifest.json"}', flush=True)
    if metadata['failures']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
