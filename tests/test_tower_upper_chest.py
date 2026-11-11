"""Upper-platform chest: preserved tower, playable access, exact exports and revisions."""
import copy,hashlib,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_tower_upper_chest import ROOT,OLD,OUT,PARENT,STEM
from inspect_ots_result import read_structure
from schem_to_nbt import read_schematic
from validate_gameplay_handoff import inspect,reachable
from integrate_gameplay_interiors import MANIFESTS,REVISION,TREE_SKULL_REVISION

class TowerUpperChest(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.root,c.blocks=read_structure(OUT/(STEM+'.nbt'));_,c.old=read_structure(OLD/(PARENT+'.nbt'))
  c.side=json.loads((OUT/(STEM+'.gameplay.json')).read_text());c.prior=json.loads((OLD/(PARENT+'.gameplay.json')).read_text())
  c.design=json.loads((OUT/(STEM+'.design.json')).read_text());c.old_design=json.loads((OLD/(PARENT+'.design.json')).read_text())
 def test_additions_stay_on_existing_landing_and_preserve_all_old_blocks(self):
  self.assertEqual(self.root['size'],[111,232,93]);self.assertEqual(self.side['ground_y'],12)
  self.assertTrue(self.old.items()<=self.blocks.items())
  added=self.blocks.keys()-self.old.keys();self.assertEqual(len(added),21)
  for x,y,z in added:
   self.assertTrue(71<=x<=75 and 174<=y<=178 and 55<=z<=56)
   self.assertIn((x,173,z),self.old)
  self.assertEqual(self.side['markers'][:-1],self.prior['markers'])
  self.assertEqual(self.side['regions'][:-1],self.prior['regions'])
  self.assertEqual(self.design['paths'][:-1],self.old_design['paths'])
  self.assertEqual(self.design['evidence']['stair_gaps'],self.old_design['evidence']['stair_gaps'])
  self.assertEqual(sum(m['role'].endswith('_chest') for m in self.side['markers']),2)
 def test_access_lid_and_all_rotations(self):
  m=self.side['markers'][-1];self.assertEqual((m['role'],m['pos'],m['facing']),('tower_summit_chest',[73,174,56],'south'))
  self.assertTrue(reachable(self.blocks,(72,174,57),(73,174,57)))
  clear={(73,y,56) for y in range(175,179)}|{(x,y,57) for x in [72,73] for y in range(174,177)}
  self.assertFalse(clear & self.blocks.keys())
  def rotate(p,n):
   x,y,z=p
   for _ in range(n):x,z=-z,x
   return x-1000,y+40,z-2000
  for n in range(4):
   points={rotate(p,n) for p in self.blocks};self.assertFalse({rotate(p,n) for p in clear}&points)
   chest=rotate((73,174,56),n);front=rotate((73,174,57),n)
   self.assertEqual((front[0]-chest[0],front[2]-chest[2]),[(0,1),(-1,0),(0,-1),(1,0)][n])
   self.assertIn(rotate((73,173,56),n),points)
 def test_exact_export_and_native_registry(self):
  self.assertEqual(read_schematic((OUT/(STEM+'.schem')).read_bytes())[1],self.blocks)
  registry={}
  for name in ['gameplay-registry-26.2.json','gameplay-interiors-feedback-20261027-registry.json','tower-upper-chest-20261111-registry.json']:registry.update(json.loads((ROOT/'docs/project/reviews'/name).read_text())['blocks'])
  self.assertGreater(inspect(OUT/(STEM+'.gameplay.json'),registry)['tiles'],0)
 def test_v6_preserves_v5_and_only_selects_new_tower(self):
  resources=ROOT/'src/main/resources';prior=resources/MANIFESTS[TREE_SKULL_REVISION]
  self.assertEqual(hashlib.sha256(prior.read_bytes()).hexdigest(),'a8494d0746f93c156ce492d82ed87f99bd521c8734d2a7c32e3726865bfc2560')
  old=json.loads(prior.read_text());new=json.loads((resources/MANIFESTS[REVISION]).read_text())
  for a,b in zip(old['structures'],new['structures']):
   self.assertEqual(a['id'],b['id'])
   if a['id']=='ruined_tower':
    self.assertNotEqual(a['single_template'],b['single_template']);self.assertEqual(a['worldgen_template']['size'],b['worldgen_template']['size']);self.assertEqual(a['worldgen_template']['foundation'],b['worldgen_template']['foundation'])
   else:
    expected=copy.deepcopy(a)
    if 'gameplay' in expected:expected['gameplay']['version']=REVISION
    self.assertEqual(expected,b)

if __name__=='__main__':unittest.main()
