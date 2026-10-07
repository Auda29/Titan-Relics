"""Regression checks for cave preservation without granting missing surface contacts."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from collections import deque
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from inspect_ots_result import read_structure
from relic_catalog import ASSETS, worldgen_resources
from rooted_embedding import remove_terrain
from terrain_foundations import supported_blocks
from verify_world import limited_clearance
from audit_cave_candidates import main as audit_cave_candidates


class CaveEmbeddingTests(unittest.TestCase):
    def test_cave_audit_rejects_failed_or_unrelated_terrain_reload(self):
        with tempfile.TemporaryDirectory() as directory:
            directory=Path(directory)
            source=directory/'source.json'
            source.write_text(json.dumps({'passed':True,'showcase':False,'seed':731204,'run_directory':str(directory)}))
            digest=hashlib.sha256(source.read_bytes()).hexdigest()
            preview=directory/'preview.json'
            for strict,passed,checksum in ((False,True,digest),(True,False,digest),(True,True,'wrong')):
                preview.write_text(json.dumps({'strict_natural_verification_passed':strict,
                    'verification':{'passed':passed},'source_report_sha256':checksum}))
                with self.subTest(strict=strict,passed=passed,checksum=checksum),patch('sys.argv',[
                    'audit_cave_candidates.py','--before',str(source),'--after',str(source),
                    '--preview-report',str(preview),'--output',str(directory/'result.json')]):
                    with self.assertRaisesRegex(ValueError,'exact natural run'):
                        audit_cave_candidates()

    def test_short_missing_surface_contact_fails_but_long_cavity_is_reported(self):
        class World:
            def __init__(self, bottom): self.bottom = bottom
            def block(self, x, y, z):
                return {'Name': 'minecraft:stone' if y <= self.bottom else 'minecraft:air'}
        policy = {'ground_y':24, 'surface_contact_depth':3, 'max_support_depth':2}
        self.assertIsNone(limited_clearance(World(8), (0,9,0), 24, policy))
        self.assertIsNone(limited_clearance(World(7), (0,9,0), 24, policy))
        self.assertEqual(limited_clearance(World(6), (0,9,0), 24, policy), 'long_native_clearance')
        self.assertEqual(limited_clearance(World(8), (0,9,0), 20, policy), 'buried_root_underside')
        class Missing:
            def block(self, *p): return None
        with self.assertRaises(ValueError):
            limited_clearance(Missing(), (0,9,0), 24, policy)
        with self.assertRaises(ValueError):
            limited_clearance(Missing(), (0,9,0), 20, policy)

    def test_accepted_tree_is_exact_and_new_deep_wood_is_sparse_connected_strands(self):
        entries = json.loads((ROOT/'docs/project/cave-candidates-20261007.json').read_bytes())['structures']
        a = next(a for a in entries if a['id']=='world_tree')
        source = ROOT/a['source']
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), a['sha256'])
        _, after = read_structure(source)
        prior = ROOT/'relics/world-tree/design/generated/world-tree-v4-1-ground-v3/world-tree-v4-1-ground-v3.nbt'
        _, before = read_structure(prior)
        config = json.loads((prior.parents[2]/(prior.stem+'.json')).read_bytes())
        art,_ = remove_terrain(before, config['materials'], tree=True, old_ground=8)
        expected = {(x,y+12,z):s for (x,y,z),s in art.items()}
        self.assertTrue(expected.items() <= after.items())
        added = set(after)-set(expected)
        self.assertTrue(0 < len(added) < 5000)
        self.assertTrue(all(after[p]=='minecraft:spruce_log[axis=y]' for p in added))
        n6=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))
        seen={p for p in added if any('_log[' in expected.get(tuple(a+b for a,b in zip(p,d)), '') for d in n6)}
        queue=deque(seen)
        while queue:
            p=queue.popleft()
            for d in n6:
                q=tuple(a+b for a,b in zip(p,d))
                if q in added and q not in seen:
                    seen.add(q);queue.append(q)
        self.assertEqual(seen, added)
        # The former bulk extrusion occupied thousands of buried footprint cells.
        self.assertLess(len({(x,z) for x,y,z in added if y<12}), 600)
        self.assertTrue(any(y<8 for x,y,z in added))

    def test_natural_skull_clips_only_declared_deep_slice_and_keeps_raw_source(self):
        entries=json.loads((ROOT/'docs/project/cave-candidates-20261007.json').read_bytes())['structures']
        a=next(a for a in entries if a['id']=='titan_skull_2')
        self.assertEqual(a['ground_y'],28, 'Cave correction must not further lower the face opening')
        self.assertEqual(a['source'], ASSETS['titan_skull_2']['source'])
        data=(ROOT/a['source']).read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), '80d4cb89afd047eca45b54b53c95cd32d130b54dec834e6664e3fe3786a86dcd')
        _,raw=read_structure(ROOT/a['source'])
        cells,size,policy=supported_blocks(raw,a)
        floor=a['ground_y']-6
        self.assertEqual(cells,{(x+8,y,z+8):s for (x,y,z),s in raw.items() if y>=floor})
        self.assertEqual(policy['omitted_buried_cells'],sum(y<floor for x,y,z in raw))
        self.assertEqual(policy['omitted_buried_cells'],7309)
        self.assertEqual(len(cells),25260)
        self.assertEqual(policy['buried_clip_y'],floor)
        self.assertEqual(policy['added_blocks'],0)
        self.assertEqual(a['max_support_depth'],2)
        self.assertTrue(a['follow_art'])

    def test_only_two_processor_profiles_change_and_rock_is_identical(self):
        original=copy.deepcopy(ASSETS)
        entries=json.loads((ROOT/'docs/project/cave-candidates-20261007.json').read_bytes())['structures']
        historical=json.loads((ROOT/'docs/project/rooted-candidates-20261007.json').read_bytes())['structures']
        self.assertEqual({a['id'] for a in entries},{'world_tree','titan_skull_2'})
        try:
            for a in historical:
                if a['id'] in ('world_tree','titan_skull_2'):
                    ASSETS[a['id']]={k:v for k,v in a.items() if k!='id'}
            before=worldgen_resources()
            for a in entries: ASSETS[a['id']]={k:v for k,v in a.items() if k!='id'}
            after=worldgen_resources()
        finally:
            ASSETS.clear();ASSETS.update(original)
        for key in before:
            if 'world_tree' not in key and 'titan_skull_2' not in key:
                self.assertEqual(before[key],after[key],key)
        self.assertEqual({key for key in before if before[key]!=after[key]},
            {'worldgen/processor_list/titan_skull_2_terrain.json','worldgen/processor_list/world_tree_terrain.json'})


if __name__=='__main__':
    unittest.main()
