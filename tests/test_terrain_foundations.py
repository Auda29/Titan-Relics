"""Regression: a shallow exported earth mound must reach a permitted downhill slope."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from terrain_foundations import supported_blocks, TOE_RADIUS


class FoundationTests(unittest.TestCase):
    def test_downhill_contact_without_filling_arch_or_touching_source(self):
        contract = {'ground_y': 8, 'slope': 12, 'size': [9, 40, 9]}
        source = {(1, 5, 2): 'minecraft:dirt', (1, 8, 2): 'minecraft:grass_block',
                  (4, 20, 2): 'minecraft:moss_block', (5, 9, 5): 'minecraft:bone_block'}
        original = dict(source)
        result, size, report = supported_blocks(source, contract)
        shift = report['vertical_padding']
        self.assertEqual(source, original)
        self.assertEqual(size, [25, 48, 25])
        for surface in range(-12, 13):
            # Worst allowed surface is 12 below nominal ground; foundation is deeper.
            contact = 8 + surface + shift
            if contact < 5 + shift:
                self.assertIn((1+TOE_RADIUS, contact, 2+TOE_RADIUS), result)
        # No fill above the low talus reaches the existing arch's cavity.
        self.assertNotIn((5+TOE_RADIUS,8+shift,5+TOE_RADIUS),result)
        for (x, y, z), state in source.items():
            self.assertEqual(result[x+TOE_RADIUS, y + shift, z+TOE_RADIUS], state)

    def test_stable_sand_and_rock_fill(self):
        contract = {'ground_y': 2, 'slope': 6, 'size': [5, 20, 5]}
        result, _, _ = supported_blocks({(0, 0, 0): 'minecraft:sand', (4, 0, 4): 'minecraft:gravel'}, contract)
        self.assertEqual(result[TOE_RADIUS, 0, TOE_RADIUS], 'minecraft:sandstone')
        self.assertEqual(result[4+TOE_RADIUS, 0, 4+TOE_RADIUS], 'minecraft:stone')

    def test_talus_top_falls_away_and_stays_inside_padded_bounds(self):
        contract={'ground_y':8,'slope':12,'size':[9,40,9]}
        result,size,report=supported_blocks({(4,8,4):'minecraft:dirt'},contract)
        tops=[max(y for x,y,z in result if x==4+TOE_RADIUS+d and z==4+TOE_RADIUS) for d in (1,2,3)]
        self.assertEqual(tops,[13,11,9])
        self.assertTrue(all(0<=p[i]<size[i] for p in result for i in range(3)))
        self.assertGreater(report['toe_blocks'],0)


if __name__ == '__main__': unittest.main()
