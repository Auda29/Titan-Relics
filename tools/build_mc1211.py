"""Build/remap the isolated Alpha 4.9 Fabric 1.21.1 JAR and verify its payload."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import zipfile

from prepare_mc1211 import prepare
from relic_catalog import ROOT

PROJECT = ROOT / 'compat/mc1.21.1'


def verify_archive(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError('Duplicate archive entries')
        metadata = json.loads(archive.read('fabric.mod.json'))
        if (metadata.get('id') != 'relics' or metadata['version'] != '0.1.0-alpha.4.9' or metadata['depends']['minecraft'] != '1.21.1'
                or metadata['depends']['java'] != '>=21'):
            raise ValueError('Wrong compatibility target/version')
        manifest = json.loads(archive.read('relics.integration.json'))
        baseline = json.loads((ROOT / 'src/main/resources/relics.integration.json').read_bytes())
        if manifest['structures'] != baseline['structures'] or manifest.get('compatibility_target') != '1.21.1':
            raise ValueError('Changed Alpha 4.9 selection or template contracts')
        templates = set()
        for record in manifest['structures']:
            for field in ('single_template', 'worldgen_template'):
                name = 'data/relics/structure/' + record[field]['path']
                templates.add(name)
                if hashlib.sha256(archive.read(name)).hexdigest() != record[field]['sha256']:
                    raise ValueError('Changed artwork bytes: ' + name)
        if {name for name in names if name.endswith('.nbt')} != templates:
            raise ValueError('Missing or extra template exports')
        classes = [name for name in names if name.endswith('.class')]
        if not classes or any(not name.startswith('de/relics/') for name in classes):
            raise ValueError('Missing runtime classes or bundled third-party code')
        for name in classes:
            data = archive.read(name)
            if data[:4] != bytes.fromhex('cafebabe') or int.from_bytes(data[6:8], 'big') != 65:
                raise ValueError('Runtime class must target Java 21: ' + name)
        if b'method_15172' not in archive.read('de/relics/mixin/StructureTemplateMixin.class'):
            raise ValueError('Missing intermediary-remapped template mixin selector')
        if json.loads(archive.read('pack.mcmeta'))['pack']['pack_format'] != 48:
            raise ValueError('Wrong 1.21.1 data pack format')
    return {'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'minecraft': '1.21.1', 'java_class_major': 65,
            'exact_alpha49_templates': len(templates), 'runtime_classes': len(classes)}


def find_gradle(explicit: str | None) -> str:
    if explicit:
        return explicit
    found = shutil.which('gradle')
    if found:
        return found
    cached = sorted((Path.home() / '.gradle/wrapper/dists/gradle-9.5.1-bin').glob('*/gradle-9.5.1/bin/gradle.bat'))
    if cached:
        return str(cached[0])
    raise ValueError('Install Gradle 9.5+ or provide --gradle; this build does not install it automatically')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gradle', help='Gradle 9.5+ executable')
    parser.add_argument('--java-home', type=Path, help='JDK 21+ used to run Gradle; output always targets Java 21')
    parser.add_argument('--test-java', type=Path, help='Java 21 executable for the shared headless assertions')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    parser.add_argument('--rerun-tasks', action='store_true', help='Recompile/remap to check byte reproducibility')
    args = parser.parse_args()
    prepare()
    environment = os.environ.copy()
    if args.java_home:
        environment['JAVA_HOME'] = str(args.java_home.resolve())
    arguments = [find_gradle(args.gradle), '--no-daemon', 'build']
    if args.test_java:
        arguments.append('-PrelicTestJava=' + str(args.test_java.resolve()))
    if args.rerun_tasks:
        arguments.append('--rerun-tasks')
    subprocess.run(arguments, cwd=PROJECT, env=environment, check=True)
    source = PROJECT / 'build/libs/relics-0.1.0-alpha.4.9+mc1.21.1.jar'
    record = verify_archive(source)
    args.output.mkdir(parents=True, exist_ok=True)
    destination = args.output / source.name
    if destination.resolve() != source.resolve():
        shutil.copy2(source, destination)
    release = PROJECT / 'build/release'
    release.mkdir(parents=True, exist_ok=True)
    (release / 'SHA256SUMS.txt').write_text(record['sha256'] + '  ' + source.name + '\n', encoding='utf-8', newline='\n')
    (release / 'build-verification.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(record, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
