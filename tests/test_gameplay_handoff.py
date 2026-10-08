"""Builder contract rejection cases and geometry evidence, not runtime integration."""
import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_gameplay_interiors import ROOT,ASSETS,STEMS
from inspect_ots_result import read_structure
from validate_gameplay_handoff import validate,reachable


class HandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=json.loads((ROOT/'docs/project/reviews/gameplay-registry-26.2.json').read_text())['blocks']
        cls.assets={}
        for name,stem in STEMS.items():
            folder=(ROOT/ASSETS[name]['source']).parent.parent/stem
            root,blocks=read_structure(folder/(stem+'.nbt'))
            cls.assets[name]=(json.loads((folder/(stem+'.gameplay.json')).read_text()),blocks,root['size'])

    def test_all_five_sidecars_validate(self):
        for name,(s,b,size) in self.assets.items():
            with self.subTest(name=name):self.assertEqual(validate(s,b,size,self.registry),name)

    def test_corrupt_bindings_roles_and_regions_rejected(self):
        s,b,size=self.assets['colossus']
        mutations=[lambda d:d.update(schema_version=2),lambda d:d.update(source_sha256='0'*64),
                   lambda d:d.update(source_nbt='../escape.nbt'),lambda d:d.update(size=[1,2,3]),
                   lambda d:d.update(ground_y=0),lambda d:d['markers'].pop(),
                   lambda d:d['markers'][0].update(pos=[-1,0,0]),
                   lambda d:d['markers'][0].update(role='invented_role'),
                   lambda d:d['regions'][0].update(max=[0,0,0]),
                   lambda d:d['regions'][0].update(replaceable_blocks=['minecraft:water'])]
        for mutation in mutations:
            bad=copy.deepcopy(s);mutation(bad)
            with self.assertRaises(ValueError):validate(bad,b,size,self.registry)

    def test_obstructed_spawn_and_wrong_placeholder_rejected(self):
        s,b,size=self.assets['ruined_tower'];bad=dict(b)
        m=next(m for m in s['markers'] if m['role']=='tower_enderman_spawn')
        x,y,z=m['pos'];bad[x,y+2,z]='minecraft:stone'
        with self.assertRaisesRegex(ValueError,'clearance'):validate(s,bad,size,self.registry)
        s,b,size=self.assets['obelisk'];bad=dict(b);bad[tuple(s['markers'][0]['pos'])]='minecraft:diamond_block'
        with self.assertRaisesRegex(ValueError,'Placeholder'):validate(s,bad,size,self.registry)

    def test_ground_routes_reach_rewards(self):
        for name,start,role in [('colossus',(143,78,104),'colossus_arm_magnet_chest'),
                                ('small_colossus',(62,14,40),'small_magnet_chest'),
                                ('ruined_tower',(57,15,20),'tower_ender_chest')]:
            s,b,_=self.assets[name];m=next(m for m in s['markers'] if m['role']==role)
            with self.subTest(name=name):self.assertTrue(reachable(b,start,m['pos']))

    def test_no_authored_continuous_tower_ascent(self):
        s,b,_=self.assets['ruined_tower'];target=next(m['pos'] for m in s['markers'] if m['role']=='tower_upper_destination')
        self.assertFalse(reachable(b,(57,15,20),target))

    def test_skull_exports_not_in_handoff(self):
        self.assertTrue(all('skull' not in name for name in self.assets))
        import hashlib
        for name,a in ASSETS.items():
            if 'skull' in name:self.assertEqual(hashlib.sha256((ROOT/a['source']).read_bytes()).hexdigest(),a['sha256'])

if __name__=='__main__':unittest.main()
