"""Legacy-target adaptation retains pinned artwork and chunk-local placement safety."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from prepare_mc1211 import prepare, port_java
from relic_catalog import ASSETS, worldgen_resources
from build_mc1211 import verify_archive
from audit_mc1211 import main as audit_mc1211


class Minecraft1211CompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.output = Path(cls.directory.name)
        cls.report = prepare(cls.output)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_target_metadata_and_java_release_are_separate_from_26_2(self):
        metadata = json.loads((self.output / 'resources/fabric.mod.json').read_bytes())
        self.assertEqual(metadata['version'], '0.1.0-alpha.4.9')
        self.assertEqual(metadata['depends']['minecraft'], '1.21.1')
        self.assertEqual(metadata['depends']['java'], '>=21')
        self.assertEqual(metadata['depends']['lithostitched'], '1.8.0')
        self.assertIn('fabric-resource-loader-v0', metadata['depends'])
        self.assertNotIn('fabric-resource-loader-v1', metadata['depends'])
        pack = json.loads((self.output / 'resources/pack.mcmeta').read_bytes())
        self.assertEqual(pack['pack']['pack_format'], 48)
        mixins = json.loads((self.output / 'resources/relics.mixins.json').read_bytes())
        self.assertEqual(mixins['compatibilityLevel'], 'JAVA_21')
        self.assertTrue(mixins['required'])
        self.assertNotIn('refmap', mixins)
        self.assertEqual(json.loads((ROOT / 'src/main/resources/fabric.mod.json').read_bytes())['depends']['minecraft'], '~26.2')

    def test_all_twenty_templates_keep_exact_alpha49_bytes_and_old_data_version(self):
        manifest = json.loads((self.output / 'resources/relics.integration.json').read_bytes())
        current = json.loads((ROOT / 'src/main/resources/relics.integration.json').read_bytes())
        self.assertEqual(manifest['structures'], current['structures'])
        self.assertEqual(manifest['compatibility_target'], '1.21.1')
        for item in manifest['structures']:
            self.assertEqual(item['data_version'], 3105)
            self.assertEqual(item['sha256'], ASSETS[item['id']]['sha256'])
            for field in ('single_template', 'worldgen_template'):
                path = self.output / 'resources/data/relics/structure' / item[field]['path']
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item[field]['sha256'])

    def test_density_site_rules_and_contact_profiles_are_not_weakened(self):
        for path, expected in worldgen_resources().items():
            self.assertEqual(json.loads((self.output / 'resources/data/relics' / path).read_bytes()), expected)

    def test_old_full_template_processing_is_clipped_before_support_reads(self):
        text = (self.output / 'java/de/relics/TerrainSupportProcessor.java').read_text()
        self.assertIn('extends StructureProcessor', text)
        self.assertNotIn('public record TerrainSupportProcessor', text)
        self.assertLess(text.index('processed = processed.stream().filter'), text.index('var bottoms'))
        self.assertIn('settings.getBoundingBox().isInside(info.pos())', text)
        self.assertIn('level.getMinBuildHeight()', text)
        self.assertIn('return RelicWorldgen.TERRAIN_SUPPORT;', text)
        self.assertIn('pending.size() == maxSupportDepth', text)
        self.assertIn('maxSupportDepth < 0 || substrate', text)

    def test_protection_and_reservations_use_real_legacy_api_names(self):
        protection = (self.output / 'java/de/relics/RelicProtection.java').read_text()
        self.assertIn('ChunkPos.asLong(', protection)
        self.assertIn('chunk.setUnsaved(true)', protection)
        self.assertIn('region.ensureCanWrite(pos)', protection)
        registration = (self.output / 'java/de/relics/RelicWorldgen.java').read_text()
        self.assertIn('PLACEMENT_CONDITION_TYPE.location()', registration)
        self.assertIn('StructureProcessorType<TerrainSupportProcessor>', registration)
        reservations = (self.output / 'java/de/relics/SeparatedPlacementCondition.java').read_text()
        self.assertIn('.registryOrThrow(Registries.STRUCTURE_SET)', reservations)
        self.assertIn('context.chunkPos().x', reservations)

    def test_shared_immutable_protection_bitmask_does_not_need_an_adapter(self):
        source = (ROOT / 'src/main/java/de/relics/ProtectedCells.java').read_text()
        self.assertEqual(port_java('ProtectedCells.java', source), source)

    def test_release_payload_rejects_wrong_mod_game_or_java_before_publication(self):
        original = json.loads((self.output / 'resources/fabric.mod.json').read_bytes())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'wrong.jar'
            for field, value in (('id', 'not-relics'), ('minecraft', '~26.2'), ('java', '>=25')):
                metadata = json.loads(json.dumps(original))
                if field == 'id':
                    metadata['id'] = value
                else:
                    metadata['depends'][field] = value
                with zipfile.ZipFile(path, 'w') as archive:
                    archive.writestr('fabric.mod.json', json.dumps(metadata))
                with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'Wrong compatibility target'):
                    verify_archive(path)

    def test_independent_support_audit_cannot_reuse_failed_showcase_or_26_2_run(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / 'report.json'
            output = Path(directory) / 'audit.json'
            for passed, showcase, version, code in ((False, False, '1.21.1', 0),
                    (True, True, '1.21.1', 0), (True, False, '26.2', 0), (True, False, '1.21.1', 1)):
                report.write_text(json.dumps({'passed': passed, 'showcase': showcase,
                                              'minecraft_version': version, 'exit_code': code}))
                with self.subTest(passed=passed,showcase=showcase,version=version,code=code), patch('sys.argv',[
                        'audit_mc1211.py', '--report', str(report), '--output', str(output)]):
                    with self.assertRaisesRegex(ValueError, 'passing natural 1.21.1'):
                        audit_mc1211()
                self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
