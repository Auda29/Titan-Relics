"""Plan platform uploads by default; execute only an explicitly approved GitHub release.

Upload receipts live on that GitHub release so reruns cannot silently duplicate
files. No project is submitted for moderation or made public by this tool.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import tomllib
from urllib.parse import urlencode
import zipfile

from platform_api import Client, download
from release_ci import TARGETS, artifact_name, check_artifact, gh, release_info, sha256
from release_version import tag_version

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = 'platform-upload-state.json'
PROJECTS = {'modrinth': 'F6QDr5Vr', 'curseforge': '1785231'}


def validate_bundle(directory, version):
    """Validate the complete set and checksums before any network mutation."""
    files = [directory / artifact_name(version, *target) for target in TARGETS]
    names = {file.name for file in files}
    if {p.name for p in directory.iterdir()} != names | {'SHA256SUMS.txt'}:
        raise ValueError('Expected exactly four player JARs and SHA256SUMS.txt')
    rows = (directory / 'SHA256SUMS.txt').read_text().splitlines()
    expected = {sha256(file) + '  ' + file.name for file in files}
    if len(rows) != 4 or set(rows) != expected:
        raise ValueError('Release checksums do not match the complete bundle')
    for file, (loader, game) in zip(files, TARGETS):
        check_artifact(file, version, loader, game)
        with zipfile.ZipFile(file) as archive:
            if archive.read('LICENSE') != (ROOT / 'LICENSE').read_bytes():
                raise ValueError('Missing or different MIT license: ' + file.name)
            if 'CREDITS.md' not in archive.namelist():
                raise ValueError('Missing credits: ' + file.name)
            if loader == 'fabric':
                metadata = json.loads(archive.read('fabric.mod.json'))
                title, license_id = metadata.get('name'), metadata.get('license')
            else:
                metadata = tomllib.loads(archive.read('META-INF/neoforge.mods.toml').decode())
                title, license_id = metadata['mods'][0].get('displayName'), metadata.get('license')
            if title != 'Titan Relics' or license_id != 'MIT':
                raise ValueError('Wrong project name or license: ' + file.name)
    return files


def channel(version):
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-(?:alpha|beta)\.\d+(?:\.\d+)*)?', version):
        raise ValueError('Development/unreviewed version suffix is not a platform release')
    if '-beta.' in version:
        return 'beta'
    if '-alpha.' in version:
        return 'alpha'
    if '-' not in version:
        return 'release'
    raise ValueError('Use a release, alpha or beta version, not an unreviewed development suffix')


def dependency_specs(loader, game):
    result = [('lithostitched', f'1.8.0-{loader}-' + ('21.1' if game == '1.21.1' else game))]
    if loader == 'fabric':
        result.append(('fabric-api', '0.116.17+1.21.1' if game == '1.21.1' else '0.161.0+26.2'))
    return result


def pinned_dependency(client, slug, number, loader, game):
    query = urlencode({'loaders': json.dumps([loader]), 'game_versions': json.dumps([game])})
    versions = client.request('/project/' + slug + '/version?' + query)
    matches = [v for v in versions if v['version_number'] == number
               and loader in v['loaders'] and game in v['game_versions']]
    if len(matches) != 1:
        raise ValueError(f'Expected one pinned {slug} {number} for {loader}/{game}')
    v = matches[0]
    return {'project_id': v['project_id'], 'version_id': v['id'], 'dependency_type': 'required'}


def target_metadata(version, loader, game, notes, dependencies):
    name = f'Titan Relics {version} / {loader.title()} / Minecraft {game}'
    mr = {'name': name, 'version_number': artifact_name(version, loader, game)[7:-4],
          'project_id': PROJECTS['modrinth'], 'changelog': notes, 'version_type': channel(version),
          'game_versions': [game], 'loaders': [loader], 'featured': False,
          'environment': 'client_and_server', 'dependencies': dependencies,
          'file_parts': ['file'], 'primary_file': 'file', 'status': 'listed'}
    cf = {'displayName': name, 'changelog': notes, 'changelogType': 'markdown',
          'releaseType': channel(version), 'isMarkedForManualRelease': False,
          'gameVersionNames': [game, 'Fabric' if loader == 'fabric' else 'NeoForge',
                               'Java 21' if game == '1.21.1' else 'Java 25', 'Client', 'Server'],
          'relations': {'projects': [{'slug': slug, 'type': 'requiredDependency'}
                                    for slug, _ in dependency_specs(loader, game)]}}
    return {'modrinth': mr, 'curseforge': cf}


def make_plan(directory, version, notes, clients):
    files = validate_bundle(directory, version)
    games = {x['version'] for x in clients['modrinth'].request('/tag/game_version')}
    cf_names = {x['name'] for x in clients['curseforge'].request('/game/versions')}
    plan = []
    for file, (loader, game) in zip(files, TARGETS):
        if game not in games:
            raise ValueError('Game version absent from Modrinth catalog: ' + game)
        deps = [pinned_dependency(clients['modrinth'], slug, number, loader, game)
                for slug, number in dependency_specs(loader, game)]
        metadata = target_metadata(version, loader, game, notes, deps)
        if not set(metadata['curseforge']['gameVersionNames']) <= cf_names:
            raise ValueError('A required CurseForge game/loader/Java/environment tag is missing')
        plan.append({'filename': file.name, 'sha256': sha256(file),
                     'sha512': hashlib.sha512(file.read_bytes()).hexdigest(), 'metadata': metadata})
    return plan


class ReleaseJournal:
    """Persist an intent before POST; ambiguous failures require investigation."""
    def __init__(self, repo, tag, plan):
        self.repo, self.tag = repo, tag
        info = release_info(tag, repo)
        if not info or info['isDraft']:
            raise ValueError('Uploads require an existing published GitHub release')
        self.state = {'tag': tag, 'projects': PROJECTS,
                      'files': {p['filename']: p['sha256'] for p in plan}, 'uploads': {}}
        if RECEIPT in {a['name'] for a in info['assets']}:
            with tempfile.TemporaryDirectory() as td:
                gh('release', 'download', tag, '--repo', repo, '--pattern', RECEIPT, '--dir', td)
                previous = json.loads((Path(td) / RECEIPT).read_text())
            if (previous.get('tag') != tag or previous.get('files') != self.state['files']
                    or previous.get('projects') != PROJECTS):
                raise ValueError('Existing upload receipts belong to different files')
            uploads = previous.get('uploads')
            valid_keys = {platform + ':' + item['filename'] for platform in PROJECTS for item in plan}
            if (not isinstance(uploads, dict) or not set(uploads) <= valid_keys
                    or any(entry.get('phase') not in ('uploading', 'uploaded', 'verified')
                           for entry in uploads.values())):
                raise ValueError('Invalid upload receipt schema')
            self.state = previous

    def save(self, key, entry):
        self.state['uploads'][key] = entry
        with tempfile.TemporaryDirectory() as td:
            file = Path(td) / RECEIPT
            file.write_text(json.dumps(self.state, indent=2) + '\n')
            gh('release', 'upload', self.tag, '--repo', self.repo, file, '--clobber')


def matching_version(versions, item):
    metadata = item['metadata']['modrinth']
    candidates = [v for v in versions if v.get('version_number') == metadata['version_number']]
    if not candidates:
        return None
    if len(candidates) != 1:
        raise ValueError('Ambiguous existing Modrinth version')
    version = candidates[0]
    files = version.get('files', [])
    if (version.get('project_id') != PROJECTS['modrinth']
            or version.get('game_versions') != metadata['game_versions']
            or version.get('loaders') != metadata['loaders']
            or version.get('version_type') != metadata['version_type']
            or version.get('environment') != metadata['environment']
            or sorted((d.get('project_id'), d.get('version_id'), d.get('dependency_type'))
                      for d in version.get('dependencies', []))
               != sorted((d['project_id'], d['version_id'], d['dependency_type'])
                         for d in metadata['dependencies'])
            or len(files) != 1 or files[0].get('filename') != item['filename']
            or files[0].get('hashes', {}).get('sha512') != item['sha512']):
        raise ValueError('Existing Modrinth version differs; refusing to overwrite')
    return version


def verify_upload(platform, result, item):
    if platform == 'modrinth':
        version = matching_version([result], item)
        if version is None:
            raise ValueError('Upload response has different version metadata')
        url = version['files'][0]['url']
    else:
        file_id = result['id']
        if not isinstance(file_id, int) or file_id <= 0:
            raise ValueError('Unexpected CurseForge upload ID')
        url = f'https://edge.forgecdn.net/files/{file_id // 1000}/{file_id % 1000}/{item["filename"]}'
    data = download(url)
    if hashlib.sha256(data).hexdigest() != item['sha256']:
        raise ValueError('Downloaded platform file differs from the approved bundle')


def execute(plan, directory, clients, journal):
    versions = clients['modrinth'].request('/project/' + PROJECTS['modrinth'] + '/version')
    # Detect all conflicting Modrinth versions before uploading any target.
    existing = {item['filename']: matching_version(versions, item) for item in plan}
    pending = []
    for platform in ('modrinth', 'curseforge'):
        for item in plan:
            key = platform + ':' + item['filename']
            entry = journal.state['uploads'].get(key)
            result = existing[item['filename']] if platform == 'modrinth' else None
            if entry and entry.get('phase') == 'verified':
                verify_upload(platform, entry['result'], item)
                continue
            if entry and entry.get('phase') == 'uploading' and result is None:
                raise RuntimeError('Uncertain previous upload; inspect receipts before retrying: ' + key)
            if result is None and entry:
                result = entry.get('result')
            if result is None:
                journal.save(key, {'phase': 'uploading'})
                path = '/version' if platform == 'modrinth' else '/projects/' + PROJECTS[platform] + '/upload-file'
                result = clients[platform].upload(path, item['metadata'][platform], directory / item['filename'])
            journal.save(key, {'phase': 'uploaded', 'result': result})
            try:
                verify_upload(platform, result, item)
            except RuntimeError:
                # Moderation can delay download availability. Keep the returned
                # ID and never re-upload merely because a download is pending.
                pending.append(key)
                continue
            journal.save(key, {'phase': 'verified', 'result': result})
    return pending


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tag', required=True)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--notes', type=Path, required=True)
    parser.add_argument('--repo', default='Auda29/Titan-Relics', choices=['Auda29/Titan-Relics'])
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--approved-tag', help='Must exactly match --tag for uploads')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    version = tag_version(args.tag)
    if args.tag != 'v' + version:
        raise ValueError('Platform publication requires one canonical shared release tag')
    for platform, project in PROJECTS.items():
        if os.environ.get(platform.upper() + '_PROJECT_ID', project) != project:
            raise ValueError('Configured project ID differs from the known Titan Relics project')
    if args.execute and (args.approved_tag != args.tag or os.environ.get('PLATFORM_PUBLICATION_APPROVED') != args.tag):
        raise ValueError('Explicit approval for this exact tag is required')
    notes = args.notes.read_text(encoding='utf-8')
    if not notes.strip():
        raise ValueError('Release notes are required')
    if args.execute and any(marker in notes for marker in ('SURVIVAL_ACCEPTANCE: pending', 'SOURCE_SHA', 'DOWNLOAD_URL')):
        raise ValueError('Release notes still contain unresolved acceptance/placeholders')
    clients = {p: Client(p) for p in PROJECTS}
    plan = make_plan(args.directory, version, notes, clients)
    output = {'tag': args.tag, 'mode': 'execute' if args.execute else 'plan', 'files': plan}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(output, indent=2) + '\n')
    if args.execute:
        output['pending_download_verification'] = execute(plan, args.directory, clients, ReleaseJournal(args.repo, args.tag, plan))
    print(json.dumps(output, indent=2))
    return 2 if output.get('pending_download_verification') else 0


if __name__ == '__main__':
    raise SystemExit(main())
