"""Regression checks on feedback revisions, using the exported block data."""
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_gameplay_interiors import ROOT,ASSETS,STEMS as OLD
from build_gameplay_interiors_revision import STEMS
from inspect_ots_result import read_structure
from validate_gameplay_handoff import reachable

class RevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets={}
        for name,stem in STEMS.items():
            folder=(ROOT/ASSETS[name]['source']).parent.parent/stem
            prior=(ROOT/ASSETS[name]['source']).parent.parent/OLD[name]
            _,blocks=read_structure(folder/(stem+'.nbt'));_,old=read_structure(prior/(OLD[name]+'.nbt'))
            side=json.loads((folder/(stem+'.gameplay.json')).read_text())
            cls.assets[name]=(blocks,old,side)

    def test_visor_and_machinery(self):
        b,old,side=self.assets['colossus']
        self.assertTrue(all((94,y,z) not in b for y in (172,173) for z in range(125,164)))
        self.assertGreaterEqual(sum(v=='minecraft:black_stained_glass' for v in b.values()),5)
        self.assertGreaterEqual(sum(old.get(p)!=s and 75<=p[0]<=112 and 169<=p[1]<=176 and 175<=p[2]<=201 for p,s in b.items()),400)
        self.assertTrue(reachable(b,(143,78,104),(110,78,70)))

    def test_salvage_and_tower_routes(self):
        b,old,side=self.assets['small_colossus']
        self.assertGreaterEqual(sum(old.get(p)!=s for p,s in b.items()),120)
        self.assertTrue(reachable(b,(62,14,40),(73,19,80)))
        b,old,side=self.assets['ruined_tower']
        self.assertTrue(reachable(b,(57,15,20),(72,15,55)))
        target=next(m['pos'] for m in side['markers'] if m['role']=='tower_upper_destination')
        self.assertFalse(reachable(b,(57,15,20),target))

    def test_two_excavations_and_open_brush_positions(self):
        b,old,side=self.assets['obelisk'];points=[p for p,s in b.items() if old.get(p)!=s]
        self.assertGreaterEqual(sum(p[0]<20 for p in points),12)
        self.assertGreaterEqual(sum(p[0]>39 for p in points),12)
        self.assertEqual(len(side['markers']),8)
        for marker in side['markers']:
            x,y,z=marker['pos'];self.assertNotIn((x,y+1,z),b);self.assertIn((x,y-1,z),b)

if __name__=='__main__':unittest.main()
