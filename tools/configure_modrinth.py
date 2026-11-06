"""Review or apply the prepared project text without changing release status."""
import argparse
import json
from pathlib import Path

from platform_api import Client

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'F6QDr5Vr'


def project_fields():
    document = (ROOT / 'docs/releases/MODRINTH_DRAFT.md').read_text(encoding='utf-8')
    body = document.split('## Description draft\n', 1)[1].split('\n## Version settings at release', 1)[0].strip()
    body = body.replace('This is a beta-page draft; a public beta has not been released.',
                        'Public beta preparation is in progress; no public beta has been released.')
    body += ('\n\n### Development disclosure\n\n'
             'Generative AI tools assisted development of the code and this project description. '
             'Visual inspiration and source references are identified in the credits. '
             'This project is still a draft and has not been submitted for public beta approval.\n')
    return {'title': 'Titan Relics', 'description': 'Explore colossal ruins, uncover archaeology and follow expedition maps to recover ancient machinery.',
            'body': body, 'categories': ['adventure', 'worldgen'],
            'additional_categories': ['game-mechanics'], 'license_id': 'MIT',
            'license_url': 'https://github.com/Auda29/Titan-Relics/blob/main/LICENSE',
            'source_url': 'https://github.com/Auda29/Titan-Relics',
            'issues_url': 'https://github.com/Auda29/Titan-Relics/issues',
            'wiki_url': 'https://github.com/Auda29/Titan-Relics/blob/main/docs/players/PLAYER_GUIDE.md'}


def apply(client, icon=False):
    before = client.request('/project/' + PROJECT)
    if before['id'] != PROJECT or before['status'] != 'draft':
        raise ValueError('Expected the known draft project; refusing to alter a published/reviewed project')
    backup = ROOT / 'build/platform-preparation/modrinth-before.json'
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        backup.write_text(json.dumps(before, indent=2) + '\n', encoding='utf-8')
    fields = project_fields()
    client.request('/project/' + PROJECT, 'PATCH', fields)
    if icon:
        image = (ROOT / 'assets/branding/titan-relics-icon.png').read_bytes()
        if len(image) > 256 * 1024:
            raise ValueError('Icon exceeds the API size limit')
        client.request('/project/' + PROJECT + '/icon?ext=png', 'PATCH', image, 'image/png')
    after = client.request('/project/' + PROJECT)
    expected = {k: v for k, v in fields.items() if k not in ('license_id', 'license_url')}
    if any(after.get(k) != v for k, v in expected.items()) or after.get('license', {}).get('id') != 'MIT':
        raise RuntimeError('Project update could not be fully verified')
    if after['status'] != 'draft' or after['versions'] != before['versions']:
        raise RuntimeError('Unexpected project status/version change')
    result = {'id': PROJECT, 'status': after['status'], 'license': after['license']['id'],
              'categories': after['categories'], 'versions': len(after['versions']),
              'icon_present': bool(after.get('icon_url')), 'body_verified': True}
    (backup.parent / 'modrinth-configured.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Apply to the known draft only; never submits for review')
    parser.add_argument('--icon', action='store_true', help='Also apply the prepared Colossus screenshot icon')
    args = parser.parse_args()
    print(json.dumps(apply(Client('modrinth'), args.icon) if args.apply else project_fields(), indent=2))
