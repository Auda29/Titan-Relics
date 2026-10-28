"""Tower V10 export, preservation, route and rotation regression checks."""
import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_tower_chest import ROOT,OLD,OUT,STEM,V9,PARENT_HASH
from build_gameplay_interiors import digest,cells
from inspect_ots_result import read_structure
from schem_to_nbt import read_schematic
from validate_gameplay_handoff import inspect,reachable

def rotate(p,n):
    x,y,z=p;sx,sz=111,93
    for _ in range(n):x,z=sz-1-z,x;sx,sz=sz,sx
    return x,y,z
class TowerChest(unittest.TestCase):
    @classmethod
    def setUpClass(c):
        c.root,c.blocks=read_structure(OUT/(STEM+'.nbt'));_,c.old=read_structure(OLD/(V9+'.nbt'))
        c.side=json.loads((OUT/(STEM+'.gameplay.json')).read_text());c.oldside=json.loads((OLD/(V9+'.gameplay.json')).read_text())
        c.design=json.loads((OUT/(STEM+'.design.json')).read_text());c.olddesign=json.loads((OLD/(V9+'.design.json')).read_text())
    def test_exports_registry_tiles(self):
        reg={}
        for name in ('gameplay-registry-26.2.json','gameplay-interiors-feedback-20261027-registry.json'):reg.update(json.loads((ROOT/'docs/project/reviews'/name).read_text())['blocks'])
        report=inspect(OUT/(STEM+'.gameplay.json'),reg)
        self.assertEqual(self.root['size'],[111,232,93]);self.assertEqual(self.root['DataVersion'],3105);self.assertEqual(self.side['ground_y'],12)
        self.assertEqual(read_schematic((OUT/(STEM+'.schem')).read_bytes())[1],self.blocks)
        self.assertEqual(digest(OLD/(V9+'.nbt')),PARENT_HASH)
        self.assertGreater(report['tiles'],0)
    def test_local_delta_markers_and_ascent(self):
        delta={p for p in self.old.keys()|self.blocks.keys() if self.old.get(p)!=self.blocks.get(p)}
        self.assertEqual(len(delta),47)
        for p in delta:
            x,y,z=p
            self.assertTrue(p==(72,15,55) or (56<=x<=60 and 15<=y<=19 and 55<=z<=57))
            if p!=(72,15,55):self.assertNotIn(p,self.old)
        self.assertEqual(self.blocks[(72,14,55)],self.old[(72,14,55)]);self.assertNotIn((72,15,55),self.blocks)
        self.assertEqual(self.side['regions'][:-1],self.oldside['regions'])
        self.assertEqual(self.design['paths'][:-1],self.olddesign['paths'])
        self.assertEqual(self.design['evidence']['stair_gaps'],[[31,37],[90,97],[157,164],[229,236],[289,296]])
        for a,b in zip(self.oldside['markers'],self.side['markers']):
            self.assertEqual(b,dict(a,pos=[58,15,55],facing='north') if a['role']=='tower_ender_chest' else a)
        self.assertEqual(sum(m['role']=='tower_ender_chest' for m in self.side['markers']),1)
        self.assertEqual(sum('waxed_cut_copper'==s.split(':')[-1] for s in self.blocks.values()),1)
        self.assertEqual({p:s for p,s in self.blocks.items() if p[1]>=20},{p:s for p,s in self.old.items() if p[1]>=20})
    def test_routes_and_lid(self):
        for end in ((58,15,54),(41,15,29)):
            self.assertTrue(reachable(self.blocks,(57,15,20),end),end)
        for route in self.design['paths']:
            for x,y,z in route['feet']:
                self.assertIn((x,y-1,z),self.blocks)
                for dy in range(route['height']):self.assertNotIn((x,y+dy,z),self.blocks)
        for x in range(57,60):
            for z in range(52,55):
                self.assertIn((x,14,z),self.blocks)
                for y in range(15,19):self.assertNotIn((x,y,z),self.blocks)
        for y in range(16,22):self.assertNotIn((58,y,55),self.blocks)
    def test_four_rotations_spawn_source_masks_and_facing(self):
        volume=set().union(*(set(cells(r['min'],r['max'])) for r in self.side['regions']))
        solid=volume & self.blocks.keys();free=volume-self.blocks.keys()
        required={(58,y,55) for y in range(16,22)}|{(58,y,54) for y in range(15,19)}
        spawns=[m for m in self.side['markers'] if m['role']=='tower_enderman_spawn'];self.assertEqual(len(spawns),5)
        for m in spawns:
            x,y,z=m['pos']
            for a in range(x-1,x+2):
                for c in range(z-1,z+2):
                    self.assertEqual(self.blocks[(a,y-1,c)],self.old[(a,y-1,c)])
                    for h in range(y,y+4):required.add((a,h,c));self.assertNotIn((a,h,c),self.old)
        self.assertTrue(required<=free)
        for n in range(4):
            rc={rotate(p,n) for p in free};rs={rotate(p,n) for p in solid}
            self.assertFalse(rc&rs);self.assertTrue({rotate(p,n) for p in required}<=rc)
            p=rotate((58,15,55),n);q=rotate((58,15,54),n)
            self.assertEqual((q[0]-p[0],q[2]-p[2]),[(0,-1),(1,0),(0,1),(-1,0)][n])
            for m in spawns:
                x,y,z=m['pos']
                for a in range(x-1,x+2):
                    for c in range(z-1,z+2):self.assertIn(rotate((a,y-1,c),n),{rotate(p,n) for p in self.blocks if p[1]==14})
if __name__=='__main__':unittest.main()
