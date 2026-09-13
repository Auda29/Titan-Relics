from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from verify_world import AnvilWorld, palette_index, rotate, states_match, transform, verify_piece


class WorldReaderTests(unittest.TestCase):
    def test_padded_longs_do_not_cross_word_boundaries(self):
        # 17 states need 5 bits: 12 entries per long, with four unused high bits.
        values = [i % 17 for i in range(4096)]
        words = []
        for begin in range(0, len(values), 12):
            word = sum(v << (5 * i) for i, v in enumerate(values[begin:begin + 12]))
            words.append(word)
        self.assertEqual([palette_index(words, 17, i) for i in range(4096)], values)
        self.assertEqual(palette_index([], 1, 4095), 0)

    def test_signed_longs_and_section_coordinate_order(self):
        self.assertEqual(palette_index([-1], 16, 15), 15)
        world = AnvilWorld(Path("unused"))
        indices = [0] * 256
        # Local x=15,y=15,z=0 gives offset 3855 and the high nibble of word240.
        indices[240] = -(1 << 60)
        palette = [{"Name": f"minecraft:test_{i}"} for i in range(16)]
        world.section = lambda cx, cy, cz: {"palette": palette, "data": indices}
        self.assertEqual(world.block(-1, -1, 0), palette[15])

    def test_four_rotations_preserve_origin_and_block_properties(self):
        self.assertEqual(rotate((2, 3, 5), "CLOCKWISE_90"), (-5, 3, 2))
        self.assertEqual(rotate((2, 3, 5), "COUNTERCLOCKWISE_90"), (5, 3, -2))
        self.assertEqual(transform((2, 3, 5), "CLOCKWISE_180", (10, 20, 30)), (8, 23, 25))
        pos = (2, 3, 5)
        for _ in range(4): pos = rotate(pos, "CLOCKWISE_90")
        self.assertEqual(pos, (2, 3, 5))
        self.assertTrue(states_match({"Name": "minecraft:oak_log", "Properties": {"axis": "x"}},
                                     {"Name": "minecraft:oak_log", "Properties": {"axis": "z"}}, "CLOCKWISE_90"))

    def test_verification_rejects_missing_far_chunk_and_wrong_block(self):
        class FakeWorld:
            def __init__(self): self.missing = False; self.wrong = False
            def chunk(self, cx, cz): return None if self.missing and cx == 1 else {"Status": "minecraft:full"}
            def block(self, x, y, z): return {"Name": "minecraft:dirt" if self.wrong and x == 16 else "minecraft:stone"}
        world = FakeWorld()
        template = {"size": [17, 1, 1], "palette": [{"Name": "minecraft:stone"}],
                    "blocks": [{"pos": [0, 0, 0], "state": 0}, {"pos": [16, 0, 0], "state": 0}]}
        child = {"rotation": "NONE", "PosX": 0, "PosY": 60, "PosZ": 0, "BB": [0, 60, 0, 16, 60, 0]}
        self.assertTrue(verify_piece(world, "relics:test", child, template)["passed"])
        world.missing = True
        result = verify_piece(world, "relics:test", child, template)
        self.assertFalse(result["passed"])
        self.assertEqual(result["missing_chunks"], [[1, 0]])
        world.missing = False; world.wrong = True
        self.assertEqual(verify_piece(world, "relics:test", child, template)["mismatch_count"], 1)


if __name__ == "__main__": unittest.main()
