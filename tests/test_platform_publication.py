"""Publication safety with synthetic JARs and mocked APIs; never uploads files."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import publish_platforms as publish
from configure_modrinth import project_fields, apply, PROJECT
from platform_api import Client

VERSION = '1.0.0-beta.1'


class API:
    def __init__(self, platform):
        self.platform, self.uploads = platform, []
        self.versions = []

    def request(self, path):
        if path == '/tag/game_version':
            return [{'version': '1.21.1'}, {'version': '26.2'}]
        if path == '/game/versions':
            return [{'name': name} for name in ['1.21.1', '26.2', 'Fabric', 'NeoForge', 'Java 21', 'Java 25', 'Client', 'Server']]
        if path == '/project/F6QDr5Vr/version':
            return self.versions
        if path.startswith('/project/'):
            from urllib.parse import urlparse, parse_qs
            query = parse_qs(urlparse(path).query)
            game = json.loads(query['game_versions'][0])[0]
            loader = json.loads(query['loaders'][0])[0]
            slug = path.split('/')[2]
            number = dict(publish.dependency_specs(loader, game))[slug]
            return [{'id': slug + loader + game, 'project_id': slug, 'version_number': number,
                     'loaders': [loader], 'game_versions': [game]}]
        raise AssertionError(path)

    def upload(self, path, metadata, file):
        self.uploads.append(file.name)
        if self.platform == 'curseforge':
            return {'id': 1000 + len(self.uploads)}
        result = copy.deepcopy(metadata)
        result['id'] = 'uploaded-' + str(len(self.uploads))
        result['files'] = [{'filename': file.name, 'url': 'https://files.example/' + file.name,
                            'hashes': {'sha512': hashlib.sha512(file.read_bytes()).hexdigest()}}]
        return result


class Journal:
    def __init__(self):
        self.state = {'uploads': {}}
        self.events = []

    def save(self, key, entry):
        self.events.append((key, copy.deepcopy(entry)))
        self.state['uploads'][key] = copy.deepcopy(entry)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for loader, game in publish.TARGETS:
            path = self.root / publish.artifact_name(VERSION, loader, game)
            with zipfile.ZipFile(path, 'w') as archive:
                if loader == 'fabric':
                    archive.writestr('fabric.mod.json', json.dumps({'id': 'relics', 'name': 'Titan Relics',
                        'license': 'MIT', 'version': VERSION,
                        'depends': {'minecraft': '~26.2' if game == '26.2' else game}}))
                else:
                    archive.writestr('META-INF/neoforge.mods.toml', f'''license="MIT"
[[mods]]
modId="relics"
displayName="Titan Relics"
version="{VERSION}"
[[dependencies.relics]]
modId="minecraft"
versionRange="[{game}]"
''')
                archive.writestr('de/relics/Fixture.class', bytes.fromhex('cafebabe0000')
                                 + (65 if game == '1.21.1' else 69).to_bytes(2, 'big'))
                archive.writestr('LICENSE', (publish.ROOT / 'LICENSE').read_bytes())
                archive.writestr('CREDITS.md', (publish.ROOT / 'CREDITS.md').read_bytes())
        self.checksums()
        self.clients = {platform: API(platform) for platform in publish.PROJECTS}

    def checksums(self):
        (self.root / 'SHA256SUMS.txt').write_text(''.join(publish.sha256(p) + '  ' + p.name + '\n'
                                                       for p in sorted(self.root.glob('*.jar'))))

    def plan(self):
        return publish.make_plan(self.root, VERSION, 'Approved release notes.', self.clients)

    def test_plan_is_read_only_and_tags_all_four_targets_with_pinned_dependencies(self):
        plan = self.plan()
        self.assertEqual(len(plan), 4)
        for item, (loader, game) in zip(plan, publish.TARGETS):
            mr, cf = item['metadata']['modrinth'], item['metadata']['curseforge']
            self.assertEqual(mr['game_versions'], [game])
            self.assertEqual(mr['loaders'], [loader])
            self.assertEqual(mr['environment'], 'client_and_server')
            self.assertEqual(mr['version_type'], 'beta')
            self.assertEqual(len(mr['dependencies']), 2 if loader == 'fabric' else 1)
            self.assertIn('Fabric' if loader == 'fabric' else 'NeoForge', cf['gameVersionNames'])
            self.assertEqual(len(cf['relations']['projects']), len(mr['dependencies']))
        self.assertFalse(any(c.uploads for c in self.clients.values()))

    def test_incomplete_or_modified_bundle_is_rejected_before_any_api_calls(self):
        file = next(self.root.glob('*.jar'))
        original = file.read_bytes()
        file.write_bytes(original + b'changed')
        with self.assertRaises(ValueError):
            self.plan()
        file.write_bytes(original)
        file.unlink()
        with self.assertRaises(ValueError):
            self.plan()

    def test_missing_catalog_tag_or_pinned_dependency_fails_closed(self):
        with patch.object(self.clients['curseforge'], 'request', return_value=[]):
            with self.assertRaises(ValueError):
                self.plan()
        with patch.object(self.clients['modrinth'], 'request', return_value=[]):
            with self.assertRaises(ValueError):
                self.plan()

    def test_upload_intent_is_recorded_before_post_and_rerun_never_duplicates(self):
        plan, journal = self.plan(), Journal()
        with patch.object(publish, 'verify_upload') as verify:
            self.assertEqual(publish.execute(plan, self.root, self.clients, journal), [])
            self.assertEqual(len(verify.call_args_list), 8)
            self.assertEqual(len(journal.events), 24)
            self.assertEqual(journal.events[0][1]['phase'], 'uploading')
            self.assertEqual(journal.events[1][1]['phase'], 'uploaded')
            self.assertEqual(journal.events[2][1]['phase'], 'verified')
            publish.execute(plan, self.root, self.clients, journal)
        self.assertEqual([len(c.uploads) for c in self.clients.values()], [4, 4])

    def test_unknown_previous_curseforge_post_never_retries(self):
        plan, journal = self.plan(), Journal()
        journal.save('curseforge:' + plan[0]['filename'], {'phase': 'uploading'})
        with patch.object(publish, 'verify_upload'), self.assertRaises(RuntimeError):
            publish.execute(plan, self.root, self.clients, journal)
        self.assertEqual(self.clients['curseforge'].uploads, [])

    def test_curseforge_only_does_not_read_or_upload_modrinth_versions(self):
        plan, journal = self.plan(), Journal()
        with patch.object(self.clients['modrinth'], 'request', side_effect=AssertionError('Unselected platform')), \
                patch.object(publish, 'verify_upload'):
            publish.execute(plan, self.root, self.clients, journal, ['curseforge'])
            publish.execute(plan, self.root, self.clients, journal, ['curseforge'])
        self.assertEqual(self.clients['modrinth'].uploads, [])
        self.assertEqual(len(self.clients['curseforge'].uploads), 4)
        self.assertTrue(all(key.startswith('curseforge:') for key in journal.state['uploads']))

    def test_invalid_or_duplicate_platform_selection_fails_before_mutation(self):
        plan = self.plan()
        for platforms in ([], ['other'], ['curseforge', 'curseforge']):
            with self.subTest(platforms=platforms), self.assertRaises(ValueError):
                publish.execute(plan, self.root, self.clients, Journal(), platforms)
        self.assertFalse(any(client.uploads for client in self.clients.values()))

    def test_pending_moderation_keeps_receipts_without_duplicate_uploads(self):
        plan, journal = self.plan(), Journal()
        with patch.object(publish, 'verify_upload', side_effect=RuntimeError('Not available yet')):
            self.assertEqual(len(publish.execute(plan, self.root, self.clients, journal)), 8)
            publish.execute(plan, self.root, self.clients, journal)
        self.assertEqual([len(c.uploads) for c in self.clients.values()], [4, 4])

    def test_conflicting_modrinth_hash_fails_before_any_upload(self):
        item = self.plan()[0]
        existing = self.clients['modrinth'].upload('/version', item['metadata']['modrinth'], self.root / item['filename'])
        existing['files'][0]['hashes']['sha512'] = 'wrong'
        self.clients['modrinth'].versions = [existing]
        self.clients['modrinth'].uploads.clear()
        with self.assertRaises(ValueError):
            publish.execute(self.plan(), self.root, self.clients, Journal())
        self.assertFalse(any(c.uploads for c in self.clients.values()))

    def test_download_checksum_failure_is_not_mistaken_for_pending_moderation(self):
        item = self.plan()[0]
        with patch.object(publish, 'download', return_value=b'wrong'), self.assertRaises(ValueError):
            publish.verify_upload('curseforge', {'id': 12345}, item)

    def test_execute_needs_exact_approval_before_network_or_files(self):
        with patch.object(sys, 'argv', ['publish', '--tag', 'v' + VERSION, '--directory', 'missing',
                                       '--notes', 'missing', '--execute']), patch.dict(os.environ, {}, clear=True):
            with patch.object(Client, 'request') as request, self.assertRaises(ValueError):
                publish.main()
            request.assert_not_called()

    def test_pending_survival_notes_block_even_with_upload_approval(self):
        notes = self.root / 'notes.md'
        notes.write_text('SURVIVAL_ACCEPTANCE: pending')
        tag = 'v' + VERSION
        with patch.object(sys, 'argv', ['publish', '--tag', tag, '--approved-tag', tag,
                                      '--directory', 'missing', '--notes', str(notes), '--execute']), \
                patch.dict(os.environ, {'PLATFORM_PUBLICATION_APPROVED': tag}):
            with patch.object(Client, 'request') as request, self.assertRaises(ValueError):
                publish.main()
            request.assert_not_called()

    def test_unreviewed_development_suffix_is_not_a_release_channel(self):
        with self.assertRaises(ValueError):
            publish.channel(VERSION + '-dev')

    def test_project_setup_never_requests_status_change_or_upload(self):
        fields = project_fields()
        self.assertEqual(fields['license_id'], 'MIT')
        self.assertNotIn('status', fields)
        self.assertNotIn('requested_status', fields)
        self.assertIn('The Archive In Between', fields['body'])
        self.assertIn('Josh White', fields['body'])
        fake = unittest.mock.Mock()
        fake.request.return_value = {'id': PROJECT, 'status': 'approved'}
        with self.assertRaises(ValueError):
            apply(fake)
        self.assertEqual(fake.request.call_count, 1)


if __name__ == '__main__':
    unittest.main()
