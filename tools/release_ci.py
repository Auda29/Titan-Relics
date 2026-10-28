"""Validate the four release artifacts and publish verified files without overwriting releases."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib
import zipfile

from release_version import ROOT, release_version, tag_version

TARGETS = (('fabric', '26.2'), ('fabric', '1.21.1'), ('neoforge', '1.21.1'), ('neoforge', '26.2'))


def artifact_name(version, loader, minecraft):
    return f"relics-{version}+mc{minecraft}{'-neoforge' if loader == 'neoforge' else ''}.jar"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_artifact(path, version, loader, minecraft):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError(f'Duplicate ZIP entries in {path.name}')
        if loader == 'fabric':
            metadata = json.loads(archive.read('fabric.mod.json'))
            expected_game = '~26.2' if minecraft == '26.2' else '1.21.1'
            if (metadata['id'], metadata['version'], metadata['depends']['minecraft']) != ('relics', version, expected_game):
                raise ValueError(f'Wrong Fabric version/target: {path.name}')
            if 'META-INF/neoforge.mods.toml' in names:
                raise ValueError('Mixed loader metadata')
        else:
            metadata = tomllib.loads(archive.read('META-INF/neoforge.mods.toml').decode())
            mods = metadata['mods']
            games = [item for item in metadata['dependencies']['relics'] if item['modId'] == 'minecraft']
            if (len(mods) != 1 or mods[0]['modId'] != 'relics' or mods[0]['version'] != version
                    or len(games) != 1 or games[0]['versionRange'] != f'[{minecraft}]'):
                raise ValueError(f'Wrong NeoForge version/target: {path.name}')
            if 'fabric.mod.json' in names:
                raise ValueError('Mixed loader metadata')
        classes = [name for name in names if name.endswith('.class')]
        major = 65 if minecraft == '1.21.1' else 69
        if not classes:
            raise ValueError('Missing runtime classes')
        for name in classes:
            raw = archive.read(name)
            if (not name.startswith('de/relics/') or raw[:4] != bytes.fromhex('cafebabe')
                    or int.from_bytes(raw[6:8], 'big') != major
                    or any(marker in name for marker in ('PlanningFingerprintProbe', 'HiddenFingerprintWindow',
                                                         'FingerprintClientStop', '/testmixin/', '/validation/'))):
                raise ValueError(f'Wrong runtime class/target or diagnostic class: {name}')


def bundle(source, destination, version):
    names = [artifact_name(version, *target) for target in TARGETS]
    allowed = set(names) | {'SHA256SUMS.txt'}
    if destination.exists() and any(p.name not in allowed for p in destination.iterdir()):
        raise ValueError('Release directory contains files from another build/version')
    # Validate every input before copying or publishing any of them.
    for (loader, minecraft), name in zip(TARGETS, names):
        check_artifact(source / name, version, loader, minecraft)
    destination.mkdir(parents=True, exist_ok=True)
    for name in names:
        target = destination / name
        if target.exists() and sha256(target) != sha256(source / name):
            raise ValueError('Existing release bundle differs: ' + name)
        if not target.exists():
            shutil.copy2(source / name, target)
    checksums = ''.join(f'{sha256(destination / name)}  {name}\n' for name in sorted(names))
    checksum_file = destination / 'SHA256SUMS.txt'
    if checksum_file.exists() and checksum_file.read_bytes() != checksums.encode():
        raise ValueError('Existing bundle checksum manifest differs')
    checksum_file.write_bytes(checksums.encode())
    return [destination / name for name in sorted(allowed)]


def gh(*arguments):
    result = subprocess.run(['gh', *map(str, arguments)], capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout


def release_info(tag, repo):
    try:
        return json.loads(gh('release', 'view', tag, '--repo', repo,
                             '--json', 'isDraft,isPrerelease,assets,url'))
    except RuntimeError as error:
        if 'release not found' in str(error).lower():
            return None
        raise


def verify_remote(tag, repo, files):
    if not files:
        return
    with tempfile.TemporaryDirectory(prefix='relics-release-download-') as directory:
        args = ['release', 'download', tag, '--repo', repo, '--dir', directory]
        for file in files:
            args.extend(['--pattern', file.name])
        gh(*args)
        for file in files:
            if sha256(Path(directory) / file.name) != sha256(file):
                raise ValueError('Remote release asset differs; refusing to overwrite: ' + file.name)


def publish(tag, repo, directory):
    version = tag_version(tag)
    if (os.environ.get('GITHUB_EVENT_NAME') != 'push'
            or os.environ.get('GITHUB_REF') != 'refs/tags/' + tag):
        raise ValueError('Publishing is allowed only for the matching tag-push event; manual dispatch is a dry run')
    files = bundle(directory, directory, version)
    prerelease = '-' in version
    info = release_info(tag, repo)
    if info is None:
        curated = ROOT / 'docs/releases' / (version + '.md')
        if curated.is_file():
            notes = curated.read_text(encoding='utf-8')
        else:
            generated = json.loads(gh('api', f'repos/{repo}/releases/generate-notes',
                                      '--method', 'POST', '--field', 'tag_name=' + tag))
            notes = (f'Relic Mod {version}\n\nFabric and NeoForge for Minecraft 26.2 and 1.21.1. '
                     'Install one matching JAR and its dependencies. SHA-256 checksums are included.\n\n'
                     + generated['body'])
        with tempfile.TemporaryDirectory(prefix='relics-release-notes-') as directory_name:
            note_file = Path(directory_name) / 'notes.md'
            note_file.write_text(notes, encoding='utf-8')
            args = ['release', 'create', tag, '--repo', repo, '--verify-tag', '--draft',
                    '--title', 'Relic Mod ' + version, '--notes-file', str(note_file)]
            if prerelease:
                args.append('--prerelease')
            gh(*args)
        info = release_info(tag, repo)
        if info is None:
            raise RuntimeError('Created draft release could not be read')
    existing = {asset['name'] for asset in info['assets']}
    present = [file for file in files if file.name in existing]
    missing = [file for file in files if file.name not in existing]
    if not info['isDraft'] and (missing or info['isPrerelease'] != prerelease):
        raise ValueError('Published release is incomplete or has different metadata; leaving it unchanged')
    verify_remote(tag, repo, present)
    if not info['isDraft']:
        return info['url']  # An exact rerun has no publishing side effects.
    if missing:
        gh('release', 'upload', tag, '--repo', repo, *missing)  # Intentionally no --clobber.
    verify_remote(tag, repo, files)
    args = ['release', 'edit', tag, '--repo', repo, '--verify-tag', '--draft=false',
            '--prerelease=' + str(prerelease).lower()]
    if prerelease:
        args.append('--latest=false')
    gh(*args)
    published = release_info(tag, repo)
    if published is None or published['isDraft']:
        raise RuntimeError('Release did not become published')
    return published['url']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    prepare = commands.add_parser('prepare')
    prepare.add_argument('--tag', required=True)
    prepare.add_argument('--github-output', type=Path)
    pack = commands.add_parser('bundle')
    pack.add_argument('--source', type=Path, default=ROOT / 'dist')
    pack.add_argument('--destination', type=Path, default=ROOT / 'dist/release')
    upload = commands.add_parser('publish')
    upload.add_argument('--tag', required=True)
    upload.add_argument('--repo', required=True)
    upload.add_argument('--directory', type=Path, default=ROOT / 'dist/release')
    args = parser.parse_args()
    if args.command == 'prepare':
        version = tag_version(args.tag)
        values = f'version={version}\nprerelease={str("-" in version).lower()}\n'
        if args.github_output:
            with args.github_output.open('a', encoding='utf-8') as output:
                output.write(values)
        print(values, end='')
    elif args.command == 'bundle':
        files = bundle(args.source, args.destination, release_version())
        print(json.dumps({file.name: sha256(file) for file in files}, indent=2))
    else:
        print(publish(args.tag, args.repo, args.directory))


if __name__ == '__main__':
    main()
