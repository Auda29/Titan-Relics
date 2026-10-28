"""V7 regression checks on independent, serialized exports, not runtime generation."""
import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_colossus_landmarks import ROOT,OLD,OUT,STEM,V6
from build_gameplay_interiors import NATIVE
from inspect_ots_result import read_structure
from schem_to_nbt import read_schematic
from validate_gameplay_handoff import reachable,validate

def rotate(p,size,n):
    x,y,z=p; sx,_,sz=size
    for _ in range(n): x,z=sz-1-z,x; sx,sz=sz,sx
    return x,y,z

def covers(r,p): return all(a<=v<=b for v,a,b in zip(p,r['min'],r['max']))

class ColossusLandmarks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root,cls.blocks=read_structure(OUT/(STEM+'.nbt'));cls.oldroot,cls.old=read_structure(OLD/(V6+'.nbt'))
        cls.side=json.loads((OUT/(STEM+'.gameplay.json')).read_text());cls.oldside=json.loads((OLD/(V6+'.gameplay.json')).read_text())
        cls.registry=json.loads((ROOT/'docs/project/reviews/gameplay-registry-26.2.json').read_text())['blocks']
        cls.registry.update(json.loads((ROOT/'docs/project/reviews/gameplay-interiors-feedback-20261027-registry.json').read_text())['blocks'])
    def test_serialization_and_native_contract(self):
        self.assertEqual(self.root['size'],self.oldroot['size']);self.assertEqual(self.root['DataVersion'],self.oldroot['DataVersion'])
        a=read_schematic((OUT/(STEM+'.schem')).read_bytes());b=read_schematic((OLD/(V6+'.schem')).read_bytes())
        self.assertEqual(a[0],b[0]);self.assertEqual(a[2:],b[2:]);self.assertEqual(a[1],self.blocks)
        validate(self.side,self.blocks,self.root['size'],self.registry)
        self.assertEqual(self.side['ground_y'],self.oldside['ground_y'])
    def test_changes_are_local_and_stations_visor_preserved(self):
        diff={p for p in self.old.keys()|self.blocks.keys() if self.old.get(p)!=self.blocks.get(p)}
        def local(p):
            x,y,z=p
            return (108<=x<=112 and 77<=y<=84 and 69<=z<=72) or (91<=x<=97 and 168<=y<=172 and 180<=z<=193) or (93<=x<=95 and 169<=y<=171 and z==164) or p==(84,169,190)
        self.assertTrue(diff);self.assertFalse([p for p in diff if not local(p)])
        for x,z in [(82,174),(87,168),(101,168),(106,174)]:
            for dx in (-1,0,1):
                for y in (169,170,171):
                    for dz in range(-2,2): self.assertEqual(self.blocks.get((x+dx,y,z+dz)),self.old.get((x+dx,y,z+dz)))
        self.assertTrue(all((94,y,z) not in self.blocks for y in (172,173) for z in range(125,164)))
    def test_routes_roles_and_floor(self):
        markers={m['role']:m for m in self.side['markers']}
        self.assertEqual(len(markers),5);self.assertEqual(markers['colossus_arm_magnet_chest']['pos'],[110,78,70])
        self.assertEqual(markers['colossus_trial_spawner']['pos'],[94,169,183]);self.assertEqual(markers['colossus_vault']['pos'],[94,169,164]);self.assertEqual(markers['colossus_vault']['facing'],'south')
        self.assertEqual(markers['colossus_golem_spawn']['pos'],[94,169,190])
        self.assertNotIn((94,169,193),self.blocks);self.assertNotIn((84,169,190),self.blocks)
        self.assertTrue(any(r['role']=='cockpit_clearance' and covers(r,(94,170,164)) for r in self.side['regions']))
        for start,end in [((143,78,104),(110,78,70)),((118,169,182),(94,169,183)),((118,169,182),(94,169,164))]: self.assertTrue(reachable(self.blocks,start,end))
        for x in range(93,96):
            for z in range(189,192):
                self.assertIn((x,168,z),self.blocks)
                for y in range(169,173):self.assertNotIn((x,y,z),self.blocks)
    def test_arm_clearance_and_four_rotations(self):
        regions=[r for r in self.side['regions'] if r['role']=='arm_clearance']
        self.assertTrue(all(set(r['replaceable_blocks'])==set(NATIVE) for r in regions))
        points=[(143-i,78,104-i) for i in range(33)]+[(110,78,71),(110,78,70)]
        for x,y,z in points:
            for dy in range(1,4) if (x,z)==(110,70) else range(3):
                p=(x,y+dy,z);self.assertNotIn(p,self.blocks);self.assertTrue(any(covers(r,p) for r in regions),p)
        # Runtime compiler clears only source-free cells; verify rotated membership and facing.
        cells={(x,y,z) for r in regions for x in range(r['min'][0],r['max'][0]+1) for y in range(r['min'][1],r['max'][1]+1) for z in range(r['min'][2],r['max'][2]+1)}
        clear=cells-self.blocks.keys();size=self.root['size'];dirs=['north','east','south','west']
        for n in range(4):
            rotated_clear={rotate(p,size,n) for p in clear};rotated_solid={rotate(p,size,n) for p in self.blocks if p in cells}
            self.assertFalse(rotated_clear & rotated_solid)
            self.assertIn(rotate((110,79,70),size,n),rotated_clear)
            for m in self.side['markers']:
                if 'facing' in m:
                    face=dirs[(dirs.index(m['facing'])+n)%4]
                    vectors={'north':(0,-1),'east':(1,0),'south':(0,1),'west':(-1,0)}
                    x,y,z=m['pos']; dx,dz=vectors[m['facing']]
                    p=rotate((x,y,z),size,n); q=rotate((x+dx,y,z+dz),size,n)
                    self.assertEqual((q[0]-p[0],q[2]-p[2]),vectors[face])

if __name__=='__main__':unittest.main()
