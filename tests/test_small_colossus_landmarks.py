"""Serialized V10 geometry, routes, clearance, rotations and preservation."""
import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_small_colossus_landmarks import ROOT,OLD,OUT,STEM,V9,PARENT_HASH
from build_gameplay_interiors import digest,cells
from inspect_ots_result import read_structure
from schem_to_nbt import read_schematic
from validate_gameplay_handoff import inspect,reachable

def covers(r,p):return all(a<=v<=b for v,a,b in zip(p,r['min'],r['max']))
def rotate(p,n):
    x,y,z=p;sx,sz=111,113
    for _ in range(n):x,z=sz-1-z,x;sx,sz=sz,sx
    return x,y,z

class SmallColossusLandmarks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root,cls.blocks=read_structure(OUT/(STEM+'.nbt'))
        _,cls.old=read_structure(OLD/(V9+'.nbt'))
        cls.side=json.loads((OUT/(STEM+'.gameplay.json')).read_text())
        cls.design=json.loads((OUT/(STEM+'.design.json')).read_text())
        cls.oldside=json.loads((OLD/(V9+'.gameplay.json')).read_text())
    def test_independent_exports_and_native_handoff(self):
        registry={}
        for name in ('gameplay-registry-26.2.json','gameplay-interiors-feedback-20261027-registry.json'):
            registry.update(json.loads((ROOT/'docs/project/reviews'/name).read_text())['blocks'])
        report=inspect(OUT/(STEM+'.gameplay.json'),registry)
        self.assertEqual(self.root['size'],[111,80,113]);self.assertEqual(self.root['DataVersion'],3105)
        self.assertEqual(self.side['ground_y'],13)
        self.assertEqual(read_schematic((OUT/(STEM+'.schem')).read_bytes())[1],self.blocks)
        self.assertEqual(digest(OLD/(V9+'.nbt')),PARENT_HASH)
        self.assertGreater(report['tiles'],0)
    def test_only_frame_and_old_placeholder_changed(self):
        delta={p for p in self.old.keys()|self.blocks.keys() if self.old.get(p)!=self.blocks.get(p)}
        self.assertEqual(len(delta),29)
        for p in delta:
            x,y,z=p
            self.assertTrue(p==(73,19,80) or (67<=x<=68 and 44<=y<=48 and 51<=z<=55))
            if p!=(73,19,80):self.assertNotIn(p,self.old)
        self.assertEqual(self.blocks[(73,18,80)],self.old[(73,18,80)])
        self.assertNotIn((73,19,80),self.blocks)
        old_design=json.loads((OLD/(V9+'.design.json')).read_text())
        self.assertEqual(self.design['paths'][:len(old_design['paths'])],old_design['paths'])
        self.assertEqual(self.side['regions'][:-2],self.oldside['regions'])
        m=self.side['markers'];self.assertEqual(len(m),1)
        self.assertEqual(m[0],dict(self.oldside['markers'][0],pos=[67,44,53],facing='west'))
        self.assertEqual(sum(s=='minecraft:waxed_cut_copper' for s in self.blocks.values()),sum(s=='minecraft:waxed_cut_copper' for s in self.old.values()))
    def test_full_route_and_headroom(self):
        for a,b in [((62,14,40),(62,19,69)),((62,19,69),(61,19,82)),((61,19,82),(61,43,58)),((61,43,58),(66,44,53)),((62,14,40),(67,44,53))]:
            self.assertTrue(reachable(self.blocks,a,b),(a,b))
        regions=self.side['regions']
        for route in self.design['paths']:
            for x,y,z in route['feet']:
                self.assertIn((x,y-1,z),self.blocks)
                for dy in range(3):
                    p=(x,y+dy,z);self.assertNotIn(p,self.blocks);self.assertTrue(any(covers(r,p) for r in regions),p)
        # The approach is a 3-wide supported strip, not an isolated perch.
        for x in range(64,67):
            for z in range(52,57):
                self.assertIn((x,43,z),self.blocks)
                for y in range(44,47):self.assertNotIn((x,y,z),self.blocks)
    def test_lid_clearance_frame_and_four_rotations(self):
        regions=self.side['regions'][-2:]
        volume=set().union(*(set(cells(r['min'],r['max'])) for r in regions))
        free=volume-self.blocks.keys();solid=volume&self.blocks.keys()
        required={(67,y,53) for y in range(45,51)}|{(66,y,53) for y in range(44,47)}
        self.assertTrue(required<=free)
        for n in range(4):
            rc={rotate(p,n) for p in free};rs={rotate(p,n) for p in solid}
            self.assertFalse(rc&rs);self.assertTrue({rotate(p,n) for p in required}<=rc)
            p=rotate((67,44,53),n);q=rotate((66,44,53),n)
            self.assertEqual((q[0]-p[0],q[2]-p[2]),[(-1,0),(0,-1),(1,0),(0,1)][n])
            self.assertTrue(all(rotate((68,y,53),n) in rs for y in range(44,48)))

if __name__=='__main__':unittest.main()
