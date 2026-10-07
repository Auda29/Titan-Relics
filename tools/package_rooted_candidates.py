"""Build an isolated review JAR with three candidate overrides, preserving default selection."""
import copy
import hashlib
import json
from pathlib import Path
import shutil

from build import check_resources, write_archive
from compile_worldgen import compile_worldgen
from integrate_relics import integrate
from relic_catalog import ASSETS, ROOT


def main():
    index = ROOT / 'docs/project/rooted-candidates-20261007.json'
    selection = json.loads(index.read_text())
    original = copy.deepcopy(ASSETS)
    out = ROOT / 'build/rooted-embedding/20261007'
    resources = out / 'resources'
    resources.mkdir(parents=True, exist_ok=True)
    # Only runtime scaffolding; templates/resources are generated from the override selection.
    for name in ('fabric.mod.json', 'pack.mcmeta', 'relics.mixins.json'):
        shutil.copy2(ROOT / 'src/main/resources' / name, resources / name)
    assets = ROOT / 'src/main/resources/assets'
    if assets.is_dir():
        shutil.copytree(assets, resources / 'assets', dirs_exist_ok=True)
    metadata = json.loads((resources / 'fabric.mod.json').read_text())
    metadata['version'] = '0.1.0-alpha.4.8-candidate'
    (resources / 'fabric.mod.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    try:
        for a in selection['structures']:
            ASSETS[a['id']] = {k: v for k, v in a.items() if k != 'id'}
        manifest = integrate(resources)
        manifest['revision'] = '2026-10-07-native-ground-rooted-candidates'
        manifest['candidate_index_sha256'] = hashlib.sha256(index.read_bytes()).hexdigest()
        (resources / 'relics.integration.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        check_resources(resources)
        artifact = out / 'relics-0.1.0-alpha.4.8-candidate+mc26.2.jar'
        digest = write_archive(artifact, resources, compile_worldgen())
        (out / 'artifact.json').write_text(json.dumps({'path': artifact.relative_to(ROOT).as_posix(),
            'sha256': digest, 'overrides': [a['id'] for a in selection['structures']],
            'default_selection_modified': False}, indent=2) + '\n', encoding='utf-8')
        print(artifact)
        print(digest)
    finally:
        ASSETS.clear()
        ASSETS.update(original)


if __name__ == '__main__':
    main()
