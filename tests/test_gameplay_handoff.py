"""Builder contract rejection cases and geometry evidence, not runtime integration."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_gameplay_interiors import ROOT,ASSETS,STEMS,Builder,BUILDERS
from inspect_ots_result import read_structure
from schem_to_nbt import read_schematic
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

    def test_published_handoff_files_match_hashes_and_sizes(self):
        index=json.loads((ROOT/'docs/project/reviews/gameplay-interiors-handoff.json').read_text())
        self.assertEqual(index['schema_version'],1)
        self.assertEqual(index['target'],'Minecraft 26.2 / Fabric')
        self.assertEqual(set(index['assets']),set(STEMS))
        for name,asset in index['assets'].items():
            s,b,size=self.assets[name]
            self.assertEqual(asset['size'],list(size))
            self.assertEqual(asset['ground_y'],s['ground_y'])
            self.assertEqual(asset['blocks'],len(b))
            self.assertEqual(asset['markers'],len(s['markers']))
            self.assertEqual(asset['regions'],len(s['regions']))
            for suffix,entry in asset['files'].items():
                with self.subTest(name=name,suffix=suffix):
                    data=(ROOT/entry['path']).read_bytes()
                    self.assertEqual(len(data),entry['bytes'])
                    self.assertEqual(hashlib.sha256(data).hexdigest(),entry['sha256'])

    def test_maintained_builders_reproduce_export_geometry_and_markers(self):
        for name,(s,b,size) in self.assets.items():
            with self.subTest(name=name):
                builder=Builder(name);BUILDERS[name](builder)
                self.assertEqual(builder.root['size'],list(size))
                self.assertEqual(builder.blocks,b)
                self.assertEqual(builder.markers,s['markers'])
                self.assertEqual(builder.regions,s['regions'])

    def test_source_formats_have_no_embedded_runtime_data(self):
        for name,(s,b,size) in self.assets.items():
            with self.subTest(name=name):
                source=ROOT/s['source_nbt'];root,_=read_structure(source)
                self.assertEqual(root['DataVersion'],3105)
                self.assertFalse(root.get('entities'))
                self.assertTrue(all('nbt' not in entry for entry in root['blocks']))
                self.assertFalse(any(state in ('minecraft:air','minecraft:cave_air','minecraft:void_air') for state in b.values()))
                self.assertEqual(read_schematic(source.with_suffix('.schem').read_bytes())[1],b)

    def test_protected_geometry_and_resource_limits_remain_exact(self):
        for name in ('colossus','obelisk','world_tree'):
            _,b,_=self.assets[name];_,old=read_structure(ROOT/ASSETS[name]['source'])
            if name=='colossus':
                protected=lambda p,s:(p[2]>135 and p[1]<135) or p[2]<60
                self.assertLess(sum('copper' in s for s in b.values()),50000)
                self.assertLess(9*sum('raw_iron_block' in s for s in b.values()),256)
            elif name=='obelisk':protected=lambda p,s:'terracotta' in s or p[1]>=16
            else:
                protected=lambda p,s:p[1]>39
                self.assertFalse(any('budding_amethyst' in s for s in b.values()))
                lights=('shroomlight','glow_lichen','cave_vines','firefly_bush')
                self.assertTrue(all(p[1]<=ASSETS[name]['ground_y']+15 for p,s in b.items() if any(k in s for k in lights)))
            with self.subTest(name=name):
                self.assertEqual({p:s for p,s in old.items() if protected(p,s)},
                                 {p:s for p,s in b.items() if protected(p,s)})

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
        for name,a in ASSETS.items():
            if 'skull' in name:self.assertEqual(hashlib.sha256((ROOT/a['source']).read_bytes()).hexdigest(),a['sha256'])

if __name__=='__main__':unittest.main()
