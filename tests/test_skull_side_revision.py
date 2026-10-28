"""Targeted artifact regressions; no runtime or world access."""
import gzip,hashlib,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_skull_side_revision import OUT,STEM,SOURCE,PIN,sha,record
from inspect_ots_result import read_structure
from schem_to_nbt import read_schematic
from verify_world import rotate
class SkullSideTests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.old,c.before=read_structure(SOURCE);c.nbt=OUT/(STEM+'.nbt');c.new,c.after=read_structure(c.nbt);c.h=json.loads((OUT/'handoff.json').read_text())
 def test_pinned_input_and_exact_removal(self):
  self.assertEqual(sha(SOURCE),PIN)
  removed=set(self.before)-set(self.after)
  self.assertEqual(len(removed),147)
  self.assertEqual(set(self.after)-set(self.before),set())
  self.assertEqual({self.before[p] for p in removed},{'minecraft:dripstone_block'})
  self.assertEqual([[f(p[i] for p in removed) for i in range(3)] for f in (min,max)],[[85,21,3],[92,25,12]])
  self.assertEqual({tuple(e['pos']):e['state'] for e in self.h['removed_cells']},{p:self.before[p] for p in removed})
  self.assertEqual(self.after,{p:s for p,s in self.before.items() if p not in removed})
 def test_all_remaining_record_bytes_and_metadata(self):
  retained=[e for e in self.old['blocks'] if tuple(e['pos']) in self.after]
  self.assertEqual(retained,self.new['blocks'])
  self.assertEqual({k:v for k,v in self.old.items() if k!='blocks'},{k:v for k,v in self.new.items() if k!='blocks'})
  raw=b''.join(map(record,retained))
  self.assertIn(raw,gzip.decompress(self.nbt.read_bytes()))
  self.assertIn(b''.join(map(record,self.old['blocks'])),gzip.decompress(SOURCE.read_bytes()))
  self.assertEqual(hashlib.sha256(raw).hexdigest(),self.h['remaining_cell_records_sha256'])
 def test_schematic_and_tiles(self):
  size,blocks,version,offset=read_schematic(self.nbt.with_suffix('.schem').read_bytes(),'omit')
  self.assertEqual(blocks,self.after);self.assertEqual(list(size),[99,136,99]);self.assertEqual(offset,[0,0,0]);self.assertEqual(version,self.old['DataVersion'])
  manifest=json.loads(self.nbt.with_suffix('.manifest.json').read_text());recovered={}
  for t in manifest['tiles']:
   root,b=read_structure(OUT/t['path']);self.assertEqual(root['size'],t['size'])
   for p,s in b.items():
    q=tuple(a+v for a,v in zip(p,t['origin']));self.assertNotIn(q,recovered);recovered[q]=s
  self.assertEqual(recovered,self.after)
 def test_four_placement_rotations(self):
  expected={'NONE':[0,0,0],'CLOCKWISE_90':[-98,0,0],'CLOCKWISE_180':[-98,0,-98],'COUNTERCLOCKWISE_90':[0,0,-98]}
  for row in self.h['rotations']:
   rotation=row['rotation'];before={rotate(p,rotation):s for p,s in self.before.items()};after={rotate(p,rotation):s for p,s in self.after.items()}
   self.assertEqual(row['rotated_min_offset'],expected[rotation]);self.assertEqual(row['size'],[99,136,99]);self.assertEqual(row['source'],self.h['source']);self.assertEqual(row['sha256'],sha(self.nbt))
   self.assertTrue(all(before[p]==s for p,s in after.items()));self.assertEqual(len(before)-len(after),147)
  self.assertEqual(len(self.h['rotations']),4);self.assertEqual(self.h['ground_y'],28);self.assertEqual(self.h['buried_clip_depth'],6)
 def test_blender_reopen_bound_to_current_artifact(self):
  v=json.loads((OUT/'source-verification.json').read_text())
  self.assertTrue(v['fresh_reopen']);self.assertTrue(v['independent_surface_rebuild_equal']);self.assertEqual(v['voxel_cells_equal_nbt'],32422)
  self.assertEqual(v['blend_sha256'],sha(OUT/(STEM+'-source.blend')));self.assertEqual(v['bound_nbt_sha256'],sha(self.nbt))
if __name__=='__main__':unittest.main()
