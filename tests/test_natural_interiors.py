"""Acceptance contracts for the approved export selected by natural generation."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from inspect_ots_result import read_structure
from integrate_gameplay_interiors import integrate,INDEX,REVISION

class NaturalInteriorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resources=ROOT/'src/main/resources'
        cls.old=json.loads((cls.resources/'relics.integration.json').read_text())
        cls.new=json.loads((cls.resources/'relics.gameplay.integration.json').read_text())
        cls.index=json.loads(INDEX.read_text())

    def test_every_approved_export_is_selected_without_changing_legacy(self):
        self.assertEqual(self.new['revision'],REVISION)
        active={a['id']:a for a in self.new['structures'] if 'gameplay' in a}
        self.assertEqual(set(active),{'colossus','small_colossus','ruined_tower','obelisk','world_tree'})
        for name,asset in active.items():
            files=self.index['assets'][name]['files']
            self.assertEqual(asset['single_template']['sha256'],files['.nbt']['sha256'])
            self.assertEqual(asset['gameplay']['sidecar_sha256'],files['.gameplay.json']['sha256'])
            side=json.loads((ROOT/files['.gameplay.json']['path']).read_text())
            self.assertEqual(asset['gameplay']['markers'],side['markers'])
            old=next(a for a in self.old['structures'] if a['id']==name)
            self.assertEqual(asset['worldgen_template']['size'],old['worldgen_template']['size'])
            for kind in ('single_template','worldgen_template'):
                target=self.resources/'data/relics/structure'/old[kind]['path']
                self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(),old[kind]['sha256'])
        for asset in self.new['structures']:
            if asset['id'] not in active:self.assertEqual(asset,next(a for a in self.old['structures'] if a['id']==asset['id']))

    def test_clearance_never_erases_authored_geometry_or_injected_markers(self):
        for asset in self.new['structures']:
            if 'gameplay' not in asset:continue
            contract=asset['gameplay'];offset=contract['offset']
            _,raw=read_structure(self.resources/'data/relics/structure'/asset['single_template']['path'])
            _,natural=read_structure(self.resources/'data/relics/structure'/asset['worldgen_template']['path'])
            clear={(x,y,z) for x,y,z0,z1 in contract['clearance_runs'] for z in range(z0,z1+1)}
            if asset['id'] in ('colossus','small_colossus','ruined_tower'):self.assertTrue(clear)
            self.assertFalse(clear.intersection(tuple(v+o for v,o in zip(p,offset)) for p in raw))
            self.assertFalse(clear.intersection(natural))
            for m in contract['markers']:
                if 'expected_block' in m:self.assertNotIn(tuple(v+o for v,o in zip(m['pos'],offset)),clear)

    def test_skip_generation_rejects_tampered_marker_contract(self):
        with tempfile.TemporaryDirectory() as temporary:
            resources=Path(temporary)
            shutil.copyfile(self.resources/'relics.integration.json',resources/'relics.integration.json')
            integrate(resources)
            path=resources/'relics.gameplay.integration.json';manifest=json.loads(path.read_text())
            asset=next(a for a in manifest['structures'] if a['id']=='colossus')
            asset['gameplay']['markers'][0]['pos'][0]+=1
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,'Stale approved gameplay manifest'):integrate(resources,verify=True)

if __name__=='__main__':unittest.main()
