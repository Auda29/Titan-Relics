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
from integrate_gameplay_interiors import integrate,INDEX,REVISION,MANIFESTS,PREVIOUS_REVISION,LANDMARK_REVISION,SMALL_LANDMARK_REVISION,SHORT_ENTRY_REVISION,TREE_SKULL_REVISION,bound_files,source_path

class NaturalInteriorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resources=ROOT/'src/main/resources'
        cls.old=json.loads((cls.resources/'relics.integration.json').read_text())
        cls.new=json.loads((cls.resources/MANIFESTS[REVISION]).read_text())
        cls.index=json.loads(INDEX.read_text())

    def test_every_approved_export_is_selected_without_changing_legacy(self):
        self.assertEqual(self.new['revision'],REVISION)
        active={a['id']:a for a in self.new['structures'] if 'gameplay' in a}
        self.assertEqual(set(active),{'colossus','small_colossus','ruined_tower','obelisk','world_tree','titan_skull_2'})
        for name,asset in active.items():
            if name=='titan_skull_2':
                binding=self.index['visual_assets'][name];side=json.loads(source_path(binding['path']).read_text())
                self.assertEqual(asset['single_template']['sha256'],side['sha256'])
                self.assertEqual(asset['gameplay']['selection_handoff_sha256'],binding['sha256'])
                self.assertEqual(asset['gameplay']['markers'],[])
                continue
            files=bound_files(self.index['assets'][name])
            self.assertEqual(asset['single_template']['sha256'],files['.nbt']['sha256'])
            self.assertEqual(asset['gameplay']['sidecar_sha256'],files['.gameplay.json']['sha256'])
            side=json.loads(source_path(files['.gameplay.json']['path']).read_text())
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
            path=resources/MANIFESTS[REVISION];manifest=json.loads(path.read_text())
            asset=next(a for a in manifest['structures'] if a['id']=='colossus')
            asset['gameplay']['markers'][0]['pos'][0]+=1
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,'Stale approved gameplay manifest'):integrate(resources,verify=True)

    def test_previous_interior_templates_and_manifest_remain_exact(self):
        # V6 worlds retain their saved marker coordinates and frozen fingerprint.
        integrate(self.resources,verify=True,revision=PREVIOUS_REVISION)
        previous=json.loads((self.resources/MANIFESTS[PREVIOUS_REVISION]).read_text())
        old=next(a for a in previous['structures'] if a['id']=='colossus')
        new=next(a for a in self.new['structures'] if a['id']=='colossus')
        self.assertNotEqual(old['single_template']['path'],new['single_template']['path'])
        self.assertNotEqual(old['worldgen_template']['path'],new['worldgen_template']['path'])
        self.assertEqual(old['gameplay']['asset_version'],'colossus-v6-interiors')
        self.assertEqual(new['gameplay']['asset_version'],'colossus-v7-landmarks')
        for entry in previous['structures']:
            for kind in ('single_template','worldgen_template'):
                path=self.resources/'data/relics/structure'/entry[kind]['path']
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),entry[kind]['sha256'])

    def test_landmark_chest_top_is_reserved_as_air(self):
        colossus=next(a for a in self.new['structures'] if a['id']=='colossus')
        c=colossus['gameplay'];offset=c['offset']
        marker=next(m for m in c['markers'] if m['role']=='colossus_arm_magnet_chest')
        x,y,z=[v+o for v,o in zip(marker['pos'],offset)]
        clear={(x,y,z) for x,y,z0,z1 in c['clearance_runs'] for z in range(z0,z1+1)}
        self.assertTrue({(x,y+d,z) for d in range(1,4)}<=clear)
        _,natural=read_structure(self.resources/'data/relics/structure'/colossus['worldgen_template']['path'])
        self.assertFalse({(x,y+d,z) for d in range(1,4)} & natural.keys())
        self.assertIn('minecraft:coal_ore',c['replaceable_blocks'])
        self.assertIn('minecraft:deepslate_iron_ore',c['replaceable_blocks'])
        previous=json.loads((self.resources/MANIFESTS[PREVIOUS_REVISION]).read_text())
        old=next(a for a in previous['structures'] if a['id']=='colossus')
        self.assertNotIn('minecraft:coal_ore',old['gameplay']['replaceable_blocks'])

    def test_v2_world_contract_keeps_its_exact_frozen_bytes(self):
        integrate(self.resources,verify=True,revision=LANDMARK_REVISION)
        expected={PREVIOUS_REVISION:'8af3ed4996f7dddce8182c184a4aa0b434a469f248005b2428322ce0bc116407',
                  LANDMARK_REVISION:'82fc688fc07514017654858eb24a33998625a864722e162e3eb02bfb3f58228e',
                  SMALL_LANDMARK_REVISION:'2a1c6b7ad244ebf845d075327f5fb3f71483fb527f9a223e2994a25661df15a1'}
        for revision,sha in expected.items():
            self.assertEqual(hashlib.sha256((self.resources/MANIFESTS[revision]).read_bytes()).hexdigest(),sha)

    def test_small_upper_chest_and_lid_survive_shorter_v11_entry(self):
        small=next(a for a in self.new['structures'] if a['id']=='small_colossus');c=small['gameplay']
        marker=next(m for m in c['markers'] if m['role']=='small_magnet_chest')
        self.assertEqual(marker['pos'],[67,44,53]);self.assertEqual(marker['facing'],'west')
        self.assertEqual(c['asset_version'],'small-colossus-v11-short-entry')
        x,y,z=[v+o for v,o in zip(marker['pos'],c['offset'])]
        clear={(x,y,z) for x,y,z0,z1 in c['clearance_runs'] for z in range(z0,z1+1)}
        self.assertTrue({(x,y+d,z) for d in range(1,7)}<=clear)
        self.assertIn('minecraft:coal_ore',c['replaceable_blocks'])
        old=json.loads((self.resources/MANIFESTS[LANDMARK_REVISION]).read_text())
        prev=next(a for a in old['structures'] if a['id']=='small_colossus')
        self.assertNotEqual(small['worldgen_template']['path'],prev['worldgen_template']['path'])
        self.assertEqual(prev['gameplay']['markers'][0]['pos'],[73,19,80])

    def test_v4_merges_both_models_and_preserves_accepted_assets(self):
        old=json.loads((self.resources/MANIFESTS[SMALL_LANDMARK_REVISION]).read_text())
        previous={a['id']:a for a in old['structures']}
        active={a['id']:a for a in self.new['structures']}
        for name in ('colossus','obelisk','world_tree'):
            for field in ('single_template','worldgen_template'):
                self.assertEqual(active[name][field],previous[name][field])
            # Only the revision label changes for the already accepted geometry.
            self.assertEqual({k:v for k,v in active[name]['gameplay'].items() if k!='version'},
                             {k:v for k,v in previous[name]['gameplay'].items() if k!='version'})
        for name in ('small_colossus','ruined_tower'):
            self.assertNotEqual(active[name]['worldgen_template']['path'],previous[name]['worldgen_template']['path'])
            self.assertFalse(active[name]['visually_accepted'])
        for name in ('colossus','obelisk'):self.assertTrue(active[name]['visually_accepted'])
        tower=active['ruined_tower'];contract=tower['gameplay']
        chest=next(m for m in contract['markers'] if m['role'].endswith('_chest'))
        self.assertEqual(chest['pos'],[58,15,55]);self.assertEqual(chest['facing'],'north')
        self.assertEqual(contract['asset_version'],'ruined-tower-v11-upper-chest')
        p=tuple(v+o for v,o in zip(chest['pos'],contract['offset']))
        clear={(x,y,z) for x,y,z0,z1 in contract['clearance_runs'] for z in range(z0,z1+1)}
        self.assertIn((p[0],p[1]+1,p[2]),clear)
        self.assertIn('minecraft:iron_ore',contract['replaceable_blocks'])
        self.assertIn('minecraft:bush',contract['replaceable_blocks'])
        self.assertNotIn('minecraft:bush',previous['ruined_tower']['gameplay']['replaceable_blocks'])

    def test_v5_only_changes_skull_selection_and_freezes_v4(self):
        old_path=self.resources/MANIFESTS[SHORT_ENTRY_REVISION]
        self.assertEqual(hashlib.sha256(old_path.read_bytes()).hexdigest(),
            '9edf03417e27289a733730139130a846b3d36ddf637d5d35f4a18ac8d9713ecc')
        old=json.loads(old_path.read_text())
        v5=json.loads((self.resources/MANIFESTS[TREE_SKULL_REVISION]).read_text())
        for prior in old['structures']:
            current=next(a for a in v5['structures'] if a['id']==prior['id'])
            if prior['id']=='titan_skull_2':
                self.assertNotEqual(current['single_template'],prior['single_template'])
                self.assertEqual(current['worldgen_template']['size'],prior['worldgen_template']['size'])
                self.assertEqual(current['gameplay']['clearance_runs'],[])
            else:
                expected=json.loads(json.dumps(prior))
                if 'gameplay' in expected:expected['gameplay']['version']=TREE_SKULL_REVISION
                self.assertEqual(current,expected)

if __name__=='__main__':unittest.main()
