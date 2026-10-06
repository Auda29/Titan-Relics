import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from terrain_foundations import TOE_RADIUS, padding
from verify_tree_contacts import root_contacts
from verify_world import transform


class World:
    def __init__(self, blocks):
        self.blocks = blocks

    def block(self, x, y, z):
        return self.blocks.get((x, y, z), {"Name": "minecraft:air"})


class TreeContactTests(unittest.TestCase):
    def setUp(self):
        self.contract = {"ground_y": 8, "slope": 12}
        self.instance = {"origin": [100, 50, -200], "rotation": "CLOCKWISE_90"}
        self.log = {"Name": "minecraft:spruce_log", "Properties": {"axis": "y"}}

    def placed(self, y):
        return transform((TOE_RADIUS, y + padding(self.contract), TOE_RADIUS),
                         self.instance["rotation"], self.instance["origin"])

    def test_ground_level_air_and_water_gaps_fail_but_earth_contact_passes(self):
        position = self.placed(8)
        below = position[0], position[1] - 1, position[2]
        for state, passed in (("minecraft:air", False), ("minecraft:water", False), ("minecraft:dirt", True)):
            with self.subTest(state=state):
                result = root_contacts(World({position: self.log, below: {"Name": state}}),
                                       {(0, 8, 0): self.log}, self.contract, self.instance)
                self.assertEqual(result["passed"], passed)
                self.assertEqual(result["ground_level_gap_columns"], 0 if passed else 1)

    def test_raised_low_arch_is_reported_without_failing_or_filling_it(self):
        position = self.placed(9)
        world = World({position: self.log})
        result = root_contacts(world, {(0, 9, 0): self.log, (1, 12, 0): self.log}, self.contract, self.instance)
        self.assertTrue(result["passed"])
        self.assertEqual(result["low_root_columns"], 1)
        self.assertEqual(result["low_root_gap_columns"], 1)
        self.assertEqual(result["ground_level_gap_columns"], 0)
        self.assertEqual(world.blocks, {position: self.log})

    def test_missing_expected_root_fails_even_when_the_ground_is_present(self):
        x, y, z = self.placed(8)
        result = root_contacts(World({(x, y - 1, z): {"Name": "minecraft:dirt"}}),
                               {(0, 8, 0): self.log}, self.contract, self.instance)
        self.assertFalse(result["passed"])
        self.assertEqual(result["missing_expected_wood"], [[x, y, z]])
