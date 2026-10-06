import sys
from pathlib import Path
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from preserve_tree_materials import preserve


class TreeMaterialPreservationTests(unittest.TestCase):
    def test_only_wood_overlap_ties_are_restored_and_added_soil_is_kept(self):
        old={(0,0,0):'log',(1,0,0):'leaf'}
        new={(0,0,0):'bark',(1,0,0):'leaf',(2,0,0):'soil'}
        result,count=preserve(new,old,{'soil'},{'log','bark'})
        self.assertEqual(result,old|{(2,0,0):'soil'})
        self.assertEqual(count,1)
        self.assertEqual(new[(0,0,0)],'bark')

    def test_moved_branch_and_lost_foliage_cannot_be_silently_restored(self):
        old={(0,0,0):'log',(1,0,0):'leaf'}
        for changed in ({(0,0,1):'log',(1,0,0):'leaf'},
                        {(0,0,0):'log',(1,0,0):'soil'},
                        {(0,0,0):'log',(1,0,0):'log'}):
            with self.subTest(changed=changed),self.assertRaises(ValueError):
                preserve(changed,old,{'soil'},{'log','bark'})
