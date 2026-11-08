"""Release boundaries: exact versions, complete bundles, verified uploads and immutable reruns."""
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import release_ci
from release_version import release_version, tag_version

VERSION = '0.1.0-alpha.5.0.3'
TAG = 'v' + VERSION


def fixture_jar(path, loader, game, version=VERSION, major=None, class_name='de/relics/Fixture.class'):
    """Synthetic metadata/class headers exercise the release gate, not Minecraft runtime behavior."""
    with zipfile.ZipFile(path, 'w') as archive:
        if loader == 'fabric':
            archive.writestr('fabric.mod.json', json.dumps({'id': 'relics', 'version': version,
                'depends': {'minecraft': '~26.2' if game == '26.2' else game}}))
        else:
            archive.writestr('META-INF/neoforge.mods.toml', f'''[[mods]]
modId="relics"
version="{version}"
[[dependencies.relics]]
modId="minecraft"
versionRange="[{game}]"
''')
        archive.writestr(class_name, bytes.fromhex('cafebabe0000')
                         + (major or (65 if game.startswith('1.') else 69)).to_bytes(2, 'big'))


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / 'dist'
        self.source.mkdir()
        self.destination = self.source / 'release'
        for loader, game in release_ci.TARGETS:
            fixture_jar(self.source / release_ci.artifact_name(VERSION, loader, game), loader, game)

    def test_expanded_release_requires_eight_targets_and_preserves_beta_one(self):
        version='1.0.1-beta.1'
        targets=release_ci.release_targets(version)
        self.assertEqual(len(targets),8)
        self.assertEqual(len(release_ci.release_targets('1.0.0-beta.1')),4)
        self.assertEqual(len(release_ci.release_targets('1.0.0-beta.2')),8)
        self.assertEqual(len(release_ci.release_targets('1.0.0')),8)
        for loader,game in targets:
            fixture_jar(self.source/release_ci.artifact_name(version,loader,game),loader,game,version=version)
        absent=self.source/release_ci.artifact_name(version,'neoforge','26.3')
        raw=absent.read_bytes();absent.unlink()
        with self.assertRaises(FileNotFoundError):release_ci.bundle(self.source,self.destination,version)
        self.assertFalse(self.destination.exists())
        absent.write_bytes(raw)
        files=release_ci.bundle(self.source,self.destination,version)
        self.assertEqual(len(files),9)
        self.assertEqual(len((self.destination/'SHA256SUMS.txt').read_text().splitlines()),8)

    def test_explicit_latest_beta_policy_keeps_other_prereleases_unchanged(self):
        self.assertEqual(release_ci.github_policy('1.0.0-beta.2'),{'latest':True,'prerelease':False})
        self.assertEqual(release_ci.github_policy('1.0.0-beta.1'),{'latest':False,'prerelease':True})

    def test_tag_validation_accepts_shared_and_historical_tags_and_rejects_injection(self):
        for tag in (TAG, 'v1.2.3', TAG + '+mc26.2', TAG + '+mc1.21.1-neoforge'):
            self.assertTrue(tag_version(tag))
        for bad in ('', VERSION, 'v01.2.3', TAG + '+mc21.2', TAG + '+mc1.21.2',
                    TAG + '\nother', TAG + ';echo bad', 'v../../tmp', TAG + '$(bad)'):
            with self.subTest(tag=bad), self.assertRaises(ValueError):
                tag_version(bad)

    def test_tag_override_changes_primary_archive_and_both_native_metadata_dependencies(self):
        from build import write_archive
        import prepare_alpha5_neoforge
        import tomllib
        resources = self.root / 'resources'
        resources.mkdir()
        (resources / 'fabric.mod.json').write_text(json.dumps({'id': 'relics', 'version': VERSION}))
        newer = '0.1.0-alpha.5.0.4'
        with patch.dict(os.environ, {'RELICS_RELEASE_VERSION': newer}):
            self.assertEqual(release_version(VERSION), newer)
            write_archive(self.root / 'new.jar', resources=resources)
        with zipfile.ZipFile(self.root / 'new.jar') as archive:
            self.assertEqual(json.loads(archive.read('fabric.mod.json'))['version'], newer)
        self.assertEqual(json.loads((resources / 'fabric.mod.json').read_text())['version'], VERSION)
        with patch.object(prepare_alpha5_neoforge, 'VERSION', newer):
            for game in ('26.2', '1.21.1'):
                self.assertEqual(tomllib.loads(prepare_alpha5_neoforge.metadata(game))['mods'][0]['version'], newer)
                self.assertEqual(tomllib.loads(prepare_alpha5_neoforge.metadata(game))['license'], 'MIT')
                checks = tomllib.loads(prepare_alpha5_neoforge.metadata(game, 'checks'))
                self.assertEqual(checks['dependencies']['relics_port_checks'][0]['versionRange'], '[' + newer + ']')
        with patch.dict(os.environ, {'RELICS_RELEASE_VERSION': ''}), self.assertRaises(ValueError):
            release_version(VERSION)

    def test_bundle_requires_all_four_exact_targets_before_producing_release_files(self):
        absent = self.source / release_ci.artifact_name(VERSION, 'neoforge', '26.2')
        absent.unlink()
        with self.assertRaises(FileNotFoundError):
            release_ci.bundle(self.source, self.destination, VERSION)
        self.assertFalse(self.destination.exists())

    def test_wrong_version_loader_target_and_diagnostic_classes_are_blocked(self):
        name = release_ci.artifact_name(VERSION, 'fabric', '1.21.1')
        for kwargs in ({'version': '9.9.9'}, {'game': '26.2'}, {'major': 69},
                       {'class_name': 'de/relics/testmixin/PlanningFingerprintProbe.class'}):
            options = {'game': '1.21.1', **kwargs}
            fixture_jar(self.source / name, 'fabric', **options)
            with self.subTest(options=options), self.assertRaises(ValueError):
                release_ci.bundle(self.source, self.destination, VERSION)
        self.assertFalse(self.destination.exists())

    def test_checksums_cover_exactly_four_jars_and_stale_bundle_cannot_be_overwritten(self):
        files = release_ci.bundle(self.source, self.destination, VERSION)
        self.assertEqual(len(files), 5)
        rows = (self.destination / 'SHA256SUMS.txt').read_text().splitlines()
        self.assertEqual(len(rows), 4)
        for row in rows:
            digest, name = row.split('  ')
            self.assertEqual(digest, release_ci.sha256(self.destination / name))
        self.assertEqual(files, release_ci.bundle(self.source, self.destination, VERSION))
        (self.destination / 'SHA256SUMS.txt').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'manifest differs'):
            release_ci.bundle(self.source, self.destination, VERSION)

    def fake_remote(self, draft, present=None, corrupt=False):
        files = release_ci.bundle(self.source, self.destination, VERSION)
        all_files = {file.name: file.read_bytes() for file in files}
        remote = {name: raw for name, raw in all_files.items() if present is None or name in present}
        state = {'draft': draft, 'exists': draft is not None}
        events = []

        def cli(*args):
            events.append(args)
            if args[:2] == ('release', 'view'):
                if not state['exists']:
                    raise RuntimeError('release not found')
                return json.dumps({'isDraft': state['draft'], 'isPrerelease': True,
                    'assets': [{'name': name} for name in remote], 'url': 'https://github.com/test/repo/releases/tag/' + TAG})
            if args[0] == 'api':
                return json.dumps({'body': 'Changes generated from commits.'})
            if args[:2] == ('release', 'create'):
                self.assertIn('--draft', args)
                self.assertIn('--verify-tag', args)
                state.update(draft=True, exists=True)
                return ''
            if args[:2] == ('release', 'upload'):
                self.assertNotIn('--clobber', args)
                for file in args[5:]:
                    remote[file.name] = file.read_bytes()
                return ''
            if args[:2] == ('release', 'download'):
                destination = Path(args[args.index('--dir') + 1])
                for index, arg in enumerate(args):
                    if arg == '--pattern':
                        name = args[index + 1]
                        (destination / name).write_bytes(b'corrupt' if corrupt else remote[name])
                return ''
            if args[:2] == ('release', 'edit'):
                self.assertEqual(set(remote), set(all_files))
                self.assertEqual(remote, all_files)
                self.assertEqual(events[-2][:2], ('release', 'download'))
                state['draft'] = False
                return ''
            self.fail('Unexpected gh call: ' + str(args))

        return cli, events, state

    def publish_fixture(self):
        return release_ci.publish(TAG, 'test/repo', self.destination)

    def test_manual_dispatch_cannot_publish_even_with_a_token(self):
        with patch.dict(os.environ, {'GITHUB_EVENT_NAME': 'workflow_dispatch', 'GITHUB_REF': 'refs/heads/main'}), \
                patch.object(release_ci, 'gh') as cli, self.assertRaises(ValueError):
            self.publish_fixture()
        cli.assert_not_called()

    def test_new_release_is_a_draft_until_all_downloads_match(self):
        cli, events, state = self.fake_remote(None, present=set())
        with patch.dict(os.environ, {'GITHUB_EVENT_NAME': 'push', 'GITHUB_REF': 'refs/tags/' + TAG}), \
                patch.object(release_ci, 'gh', cli), patch.object(release_ci, 'ROOT', self.root):
            self.assertIn('/releases/tag/', self.publish_fixture())
        self.assertFalse(state['draft'])
        self.assertTrue(any(call[:2] == ('release', 'upload') for call in events))

    def test_published_rerun_verifies_downloads_without_mutation(self):
        cli, events, state = self.fake_remote(False)
        with patch.dict(os.environ, {'GITHUB_EVENT_NAME': 'push', 'GITHUB_REF': 'refs/tags/' + TAG}), \
                patch.object(release_ci, 'gh', cli):
            self.publish_fixture()
        self.assertFalse(any(call[1] in ('edit', 'create', 'upload') for call in events))

    def test_interrupted_draft_resumes_without_replacing_existing_files(self):
        retained = release_ci.artifact_name(VERSION, 'fabric', '26.2')
        cli, events, state = self.fake_remote(True, present={retained})
        with patch.dict(os.environ, {'GITHUB_EVENT_NAME': 'push', 'GITHUB_REF': 'refs/tags/' + TAG}), \
                patch.object(release_ci, 'gh', cli):
            self.publish_fixture()
        self.assertFalse(state['draft'])
        uploads = [call for call in events if call[:2] == ('release', 'upload')]
        self.assertEqual(len(uploads), 1)
        self.assertNotIn(retained, [file.name for file in uploads[0][5:]])

    def test_failed_download_verification_leaves_new_release_as_a_draft(self):
        cli, events, state = self.fake_remote(None, present=set(), corrupt=True)
        with patch.dict(os.environ, {'GITHUB_EVENT_NAME': 'push', 'GITHUB_REF': 'refs/tags/' + TAG}), \
                patch.object(release_ci, 'gh', cli), patch.object(release_ci, 'ROOT', self.root), \
                self.assertRaisesRegex(ValueError, 'Remote release asset differs'):
            self.publish_fixture()
        self.assertTrue(state['draft'])
        self.assertFalse(any(call[:2] == ('release', 'edit') for call in events))

    def test_published_missing_files_and_changed_downloads_remain_untouched(self):
        for present, corrupt in ((set(), False), (None, True)):
            cli, events, state = self.fake_remote(False, present=present, corrupt=corrupt)
            with patch.dict(os.environ, {'GITHUB_EVENT_NAME': 'push', 'GITHUB_REF': 'refs/tags/' + TAG}), \
                    patch.object(release_ci, 'gh', cli), self.assertRaises(ValueError):
                self.publish_fixture()
            self.assertFalse(any(call[1] in ('edit', 'create', 'upload') for call in events))


if __name__ == '__main__':
    unittest.main()
