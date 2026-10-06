"""Regression for the pedestal failure and the accepted Tree boundary."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from embedding_relief import sculpt


class EmbeddingReliefTests(unittest.TestCase):
    def test_high_contact_no_longer_locks_a_tall_central_pedestal(self):
        materials={'bone':'bone','terrain_top':'grass','terrain_patch':'patch','terrain_fill':'dirt'}
        blocks={(x,y,z):'dirt' for x in range(20) for z in range(20) for y in range(26)}
        blocks[10,26,10]='bone';blocks[2,5,2]='bone'
        result,art,report=sculpt(blocks,8,materials)
        self.assertEqual(result[10,26,10],'bone')
        self.assertNotIn((10,25,10),result)
        self.assertIn((2,4,2),result)
        self.assertLessEqual(max(y for (x,y,z) in result if (x,y,z) not in art),9)
        self.assertGreater(report['removed_cells'],5000)

    def test_only_low_moss_pads_change_and_wood_foliage_remain_exact(self):
        materials={'wood':'oak_log','leaf':'oak_leaves','moss':'moss','terrain_top':'grass','terrain_patch':'rooted','terrain_fill':'dirt'}
        blocks={(x,y,z):'moss' for x in range(12) for z in range(12) for y in range(8,13)}
        blocks.update({(4,9,4):'oak_log',(4,10,4):'oak_log',(4,30,4):'oak_leaves',(5,28,5):'moss'})
        result,art,report=sculpt(blocks,8,materials,moss_pads=True)
        for p in ((4,9,4),(4,10,4),(4,30,4),(5,28,5)):self.assertEqual(blocks[p],result[p])
        self.assertIn((4,8,4),result)
        self.assertLess(sum(s=='moss' and p[1]<=13 for p,s in result.items()),100)
        self.assertTrue(report['low_moss_pads_reworked'])
        self.assertEqual((result,art,report),sculpt(blocks,8,materials,moss_pads=True))
