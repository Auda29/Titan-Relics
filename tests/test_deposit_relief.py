from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from deposit_relief import erode


class DepositReliefTests(unittest.TestCase):
    def test_erosion_keeps_supporting_contacts_and_breaks_symmetric_contours(self):
        materials={'bone':'bone','terrain_top':'grass','terrain_patch':'patch','terrain_fill':'earth'}
        blocks={}
        for x in range(-18,19):
            for z in range(-18,19):
                top=max(0,10-max(abs(x),abs(z))//2)
                for y in range(-4,top+1):blocks[x,y,z]='grass' if y==top else 'earth'
        for x in range(-2,3):
            for z in range(-2,3):blocks[x,11,z]='bone'
        result,report=erode(blocks,0,materials)
        self.assertEqual((result,report),erode(blocks,0,materials))
        self.assertGreater(report['removed_soil_cells'],500)
        self.assertEqual({p for p,s in result.items() if s=='bone'},{p for p,s in blocks.items() if s=='bone'})
        for x in range(-2,3):
            for z in range(-2,3):
                top=10-max(abs(x),abs(z))//2
                self.assertEqual(result[x,top,z],blocks[x,top,z])
        tops={(x,z):max(y for a,y,b in result if (a,b)==(x,z)) for x,z in ((14,0),(-14,0),(0,14),(0,-14))}
        self.assertGreater(len(set(tops.values())),1)

    def test_shared_moss_material_is_art_not_erasable_terrain(self):
        materials={'moss':'moss','terrain_top':'moss','terrain_patch':'soil','terrain_fill':'soil'}
        blocks={(x,y,0):'soil' for x in range(30) for y in range(5)}
        blocks[29,5,0]='moss'
        result,report=erode(blocks,0,materials)
        self.assertEqual(result[29,5,0],'moss')
        self.assertEqual(result[29,4,0],'soil')
        self.assertNotIn('moss',report['terrain_states'])

    def test_explicit_derived_root_support_lock_keeps_its_entire_soil_column(self):
        materials={'wood':'wood','terrain_top':'grass','terrain_patch':'earth','terrain_fill':'earth'}
        blocks={(x,y,z):'earth' for x in range(20) for z in range(20) for y in range(-4,6)}
        result,_=erode(blocks,0,materials,protected_columns={(16,16)})
        for y in range(-4,6):self.assertEqual(result[16,y,16],blocks[16,y,16])
        self.assertLess(len(result),len(blocks))
