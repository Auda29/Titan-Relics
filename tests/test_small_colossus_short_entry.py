"""Serialized V11 geometry, routes, clearance, rotations and preservation."""
import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_small_colossus_short_entry import ROOT,OLD,OUT,STEM,V10,PARENT_HASH,write
from build_gameplay_interiors import digest,cells,ASSETS
from inspect_ots_result import read_structure
from schem_to_nbt import read_schematic
from validate_gameplay_handoff import inspect,reachable

def covers(r,p):return all(a<=v<=b for v,a,b in zip(p,r['min'],r['max']))
def rotate(p,n):
    x,y,z=p;sx,sz=111,113
    for _ in range(n):x,z=sz-1-z,x;sx,sz=sz,sx
    return x,y,z

class SmallColossusShortEntry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root,cls.blocks=read_structure(OUT/(STEM+'.nbt'))
        _,cls.old=read_structure(OLD/(V10+'.nbt'))
        cls.side=json.loads((OUT/(STEM+'.gameplay.json')).read_text())
        cls.design=json.loads((OUT/(STEM+'.design.json')).read_text())
        cls.oldside=json.loads((OLD/(V10+'.gameplay.json')).read_text())
    def test_independent_exports_and_native_handoff(self):
        registry={}
        for name in ('gameplay-registry-26.2.json','gameplay-interiors-feedback-20261027-registry.json'):
            registry.update(json.loads((ROOT/'docs/project/reviews'/name).read_text())['blocks'])
        report=inspect(OUT/(STEM+'.gameplay.json'),registry)
        self.assertEqual(self.root['size'],[111,80,113]);self.assertEqual(self.root['DataVersion'],3105)
        self.assertEqual(self.side['ground_y'],13)
        self.assertEqual(read_schematic((OUT/(STEM+'.schem')).read_bytes())[1],self.blocks)
        self.assertEqual(digest(OLD/(V10+'.nbt')),PARENT_HASH)
        self.assertGreater(report['tiles'],0)
        write(OUT/'verification.json',report)
    def test_bounded_entry_and_preserved_upper(self):
        delta={p for p in self.old.keys()|self.blocks.keys() if self.old.get(p)!=self.blocks.get(p)}
        expected={(x,13,z) for x in range(59,66) for z in range(40,46)}|{(x,14,46) for x in range(59,66)}
        self.assertEqual(delta,expected)
        _,catalog=read_structure(ROOT/ASSETS['small_colossus']['source'])
        self.assertFalse(delta & catalog.keys())
        self.assertTrue(all(p not in self.blocks for p in expected))
        self.assertEqual(self.side['markers'],self.oldside['markers'])
        old_design=json.loads((OLD/(V10+'.design.json')).read_text())
        self.assertEqual(self.design['paths'][1:],old_design['paths'][1:])
        self.assertEqual(self.design['paths'][0]['feet'],[[62,14,46]]+old_design['paths'][0]['feet'][7:])
        old_regions={r['id']:r for r in self.oldside['regions']}
        for r in self.side['regions']:
            old=old_regions.pop(r['id'])
            if r['id']=='small-interior-clearance-9':self.assertEqual(r,dict(old,min=[59,14,46]))
            else:self.assertEqual(r,old)
        self.assertEqual(set(old_regions),{'small-interior-clearance-'+str(i) for i in range(3,9)})
        for x in range(59,66):
            self.assertIn((x,13,46),self.blocks)
            for y in range(14,19):self.assertNotIn((x,y,46),self.blocks)
        # No low terrain mask remains in front of the new threshold.
        for r in self.side['regions']:
            self.assertFalse(r['min'][1]<19 and r['min'][2]<46)

    def test_full_route_and_headroom(self):
        for a,b in [((62,14,46),(62,19,69)),((62,19,69),(61,19,82)),((61,19,82),(61,43,58)),((61,43,58),(66,44,53)),((62,14,46),(67,44,53))]:
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
    def test_exact_walk_from_nominal_ground(self):
        from collections import deque
        vox=dict(self.blocks)
        # Test fixture only: nominal terrain top is Y13, one block below the threshold feet.
        for x in range(59,66):
            self.assertNotIn((x,12,45),vox);vox[(x,12,45)]='minecraft:stone'
        def clear(p):
            x,y,z=p
            return (x,y-1,z) in vox and all((x,y+d,z) not in vox for d in range(3))
        starts=[(62,13,45),(62,14,46),(62,19,69),(61,19,82),(61,43,58),(66,44,53)]
        paths=[]
        for start,target in zip(starts,starts[1:]):
            queue=deque([start]);parent={start:None};self.assertTrue(clear(start))
            while queue and target not in parent:
                x,y,z=queue.popleft()
                for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
                    for dy in (-1,0,1):
                        q=(x+dx,y+dy,z+dz)
                        if q in parent or not clear(q):continue
                        if dy>0 and (x,y+3,z) in vox:continue
                        if dy<0 and (q[0],y+2,q[2]) in vox:continue
                        parent[q]=(x,y,z);queue.append(q)
            self.assertIn(target,parent)
            path=[];p=target
            while p is not None:path.append(list(p));p=parent[p]
            paths.append(list(reversed(path)))
        write(OUT/'walk-verification.json',{'exact_targets':starts,'paths':paths,'headroom':3,'max_step':1,'nominal_terrain_fixture_only':True})

    def test_lid_clearance_frame_and_four_rotations(self):
        regions=self.side['regions']
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
