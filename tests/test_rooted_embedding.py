"""Platform removal and exact retained anatomy for the October 7 candidates."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from inspect_ots_result import read_structure
from rooted_embedding import remove_terrain
from terrain_foundations import supported_blocks, TOE_RADIUS, padding
from audit_rooted_sites import main as audit_rooted_sites


class RootedEmbeddingTests(unittest.TestCase):
    def test_runtime_audit_keeps_native_leaf_cavity_failure_explicit(self):
        report = json.loads((ROOT / 'docs/testing/rooted-embedding-20261007-runtime-audit.json').read_bytes())
        self.assertTrue(report['support_checks_passed'])
        self.assertFalse(report['passed'])
        skull = next(i for i in report['instances'] if i['id'] == 'titan_skull_2')
        self.assertFalse(skull['strict_air_only_probes_passed'])
        self.assertEqual(len(skull['blocked_face_probe_cells']), 3)
        for cell in skull['blocked_face_probe_cells']:
            self.assertEqual(cell['state']['Name'], 'minecraft:oak_leaves')
            self.assertFalse(cell['relic_protected'])
            self.assertTrue(cell['unchanged_at_same_world_position'])

    def test_runtime_audit_rejects_failed_or_unrelated_terrain_reload(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / 'natural.json'
            source.write_text(json.dumps({'passed': True, 'showcase': False, 'run_directory': str(directory),
                                          'world_blocks': {'instances': []}}))
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            preview = directory / 'preview.json'
            for strict, passed, checksum in ((False, True, digest), (True, False, digest), (True, True, 'wrong')):
                preview.write_text(json.dumps({'strict_natural_verification_passed': strict,
                                               'verification': {'passed': passed},
                                               'source_report_sha256': checksum}))
                with self.subTest(strict=strict, passed=passed, checksum=checksum), patch('sys.argv', [
                        'audit_rooted_sites.py', '--report', str(source), '--preview-report', str(preview),
                        '--output', str(directory / 'audit.json')]):
                    with self.assertRaisesRegex(ValueError, 'exact natural run'):
                        audit_rooted_sites()

    def test_shared_anatomy_material_is_not_mistaken_for_ground(self):
        cells = {(0, 0, 0): 'minecraft:dirt', (1, 0, 0): 'minecraft:brown_terracotta',
                 (2, 0, 0): 'minecraft:moss_block', (2, 25, 0): 'minecraft:moss_block',
                 (3, 0, 0): 'minecraft:spruce_log[axis=y]'}
        materials = {'terrain_fill': 'minecraft:dirt', 'terrain_patch': 'minecraft:brown_terracotta',
                     'root': 'minecraft:brown_terracotta', 'moss': 'minecraft:moss_block'}
        art, report = remove_terrain(cells, materials, tree=True)
        self.assertNotIn((0, 0, 0), art)
        self.assertNotIn((2, 0, 0), art)
        self.assertEqual(art[1, 0, 0], 'minecraft:brown_terracotta')
        self.assertEqual(art[2, 25, 0], 'minecraft:moss_block')
        self.assertEqual(report['removed_terrain_cells'], 2)

    def test_actual_candidates_preserve_art_and_never_regrow_platforms(self):
        index = json.loads((ROOT / 'docs/project/rooted-candidates-20261007.json').read_text())
        self.assertEqual({a['id'] for a in index['structures']}, {'titan_skull_rock', 'titan_skull_2', 'world_tree'})
        for a in index['structures']:
            with self.subTest(asset=a['id']):
                path = ROOT / a['source']
                report = json.loads(path.with_name('verification.json').read_text())
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), a['sha256'])
                old = ROOT / report['source']
                self.assertEqual(hashlib.sha256(old.read_bytes()).hexdigest(), report['source_sha256'])
                old_root, before = read_structure(old)
                config = json.loads((old.parents[2] / (old.stem + '.json')).read_text())
                root, after = read_structure(path)
                art, _ = remove_terrain(before, config['materials'], tree=a['id'] == 'world_tree',
                                        old_ground=report['old_ground_y'])
                shift = report['source_translation'][1]
                expected = {(x, y + shift, z): s for (x, y, z), s in art.items()}
                self.assertTrue(expected.items() <= after.items())
                self.assertEqual(root['DataVersion'], old_root['DataVersion'])
                self.assertEqual(a['ground_y'] - shift - report['old_ground_y'], report['additional_burial'])
                additions = set(after) - set(expected)
                if a['id'] == 'world_tree':
                    self.assertGreater(len(additions), 10000)
                    self.assertTrue(all(after[p] == 'minecraft:spruce_log[axis=y]' for p in additions))
                    self.assertLess(min(p[1] for p in additions), shift)
                    self.assertLessEqual(max(p[1] - shift for p in additions), 10)
                    self.assertEqual(report['new_wood_face_connected'], len(additions))
                    _, accepted = read_structure(ROOT / 'relics/world-tree/design/generated/world-tree-v4/world-tree-v4.nbt')
                    for (x, y, z), state in accepted.items():
                        if '_log[' in state or '_leaves[' in state:
                            self.assertEqual(after[x, y + shift, z], state)
                else:
                    self.assertFalse(additions)
                self.assertFalse(any(s in report['terrain_states'] for s in after.values()))
                natural, _, foundation = supported_blocks(after, a)
                self.assertEqual(natural, {(x + TOE_RADIUS, y + padding(a), z + TOE_RADIUS): s
                                           for (x, y, z), s in after.items()})
                self.assertEqual(foundation['added_blocks'], 0)
                self.assertEqual(foundation['toe_columns'], 0)


if __name__ == '__main__':
    unittest.main()
