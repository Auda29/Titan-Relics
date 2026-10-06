"""Buried raw-boundary contacts are checked in the world, not fabricated in NBT."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from verify_embedding_contacts import boundary_art_cells, buried_contacts
from verify_world import transform


class World:
    def __init__(self, blocks):
        self.blocks = blocks

    def block(self, x, y, z):
        return self.blocks.get((x, y, z))


class EmbeddingContactTests(unittest.TestCase):
    def test_boundary_category_excludes_only_declared_terrain_and_low_moss(self):
        blocks = {(0, 0, 0): {'Name': 'minecraft:oak_log'},
                  (1, 0, 0): {'Name': 'minecraft:dirt'},
                  (2, 0, 0): {'Name': 'minecraft:moss_block'},
                  (0, 1, 0): {'Name': 'minecraft:oak_log'}}
        self.assertEqual(set(boundary_art_cells(blocks, {'minecraft:dirt'}, True)), {(0, 0, 0)})
        self.assertEqual(set(boundary_art_cells(blocks, {'minecraft:dirt'})), {(0, 0, 0), (2, 0, 0)})

    def test_saved_substrate_passes_for_every_rotation_and_padding(self):
        cells = {(3, 0, 4): {'Name': 'minecraft:bone_block'}}
        for rotation in ('NONE', 'CLOCKWISE_90', 'CLOCKWISE_180', 'COUNTERCLOCKWISE_90'):
            for contract in ({'ground_y': 13, 'slope': 4}, {'ground_y': 8, 'slope': 6}):
                from terrain_foundations import padding
                instance = {'structure': 'relics:test', 'rotation': rotation, 'origin': [-20, 40, 30]}
                position = transform((11, padding(contract), 12), rotation, instance['origin'])
                below = position[0], position[1] - 1, position[2]
                world = World({position: cells[3, 0, 4], below: {'Name': 'minecraft:stone'}})
                check = buried_contacts(world, cells, contract, instance)
                self.assertTrue(check['passed'])
                self.assertEqual(check['boundary_art_cells_checked'], 1)
                self.assertEqual(check['substrate_states'], {'minecraft:stone': 1})

    def test_missing_art_and_missing_air_or_fluid_substrate_fail_closed(self):
        cells = {(0, 0, 0): {'Name': 'minecraft:bone_block'}}
        contract = {'ground_y': 13, 'slope': 4}
        instance = {'structure': 'relics:test', 'rotation': 'NONE', 'origin': [0, 30, 0]}
        for name in (None, 'minecraft:air', 'minecraft:cave_air', 'minecraft:void_air', 'minecraft:water', 'minecraft:lava'):
            world = World({(8, 30, 8): cells[0, 0, 0]})
            if name:
                world.blocks[8, 29, 8] = {'Name': name}
            check = buried_contacts(world, cells, contract, instance)
            self.assertFalse(check['passed'])
            self.assertEqual(check['unsupported_cells'], 1)
        check = buried_contacts(World({(8, 29, 8): {'Name': 'minecraft:stone'}}), cells, contract, instance)
        self.assertFalse(check['passed'])
        self.assertEqual(check['missing_expected_art'], [[8, 30, 8]])


if __name__ == '__main__':
    unittest.main()
