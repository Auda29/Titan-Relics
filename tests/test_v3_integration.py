"""Historical V3 exports and shared showcase metadata regression fixtures."""
import hashlib
import gzip
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from integrate_v3 import ASSETS, export_v3
from relic_assets import decode_nbt
from install_test_profile import prepare_level
from verify_world import rotate


class V3IntegrationTests(unittest.TestCase):
    def test_showcase_metadata_edit_preserves_unrelated_nbt_types(self):
        raw = (b"\x0a\x00\x00\x0a\x00\x04Data"
               b"\x08\x00\x09LevelName\x00\x05world"
               b"\x01\x00\x0dallowCommands\x00"
               b"\x04\x00\x04Time\x00\x00\x00\x00\x00\x00\x12\x34\x00\x00")
        modified = prepare_level(gzip.compress(raw), "Relic V3 Showcase")
        data = decode_nbt(modified)["Data"]
        self.assertEqual(data["LevelName"], "Relic V3 Showcase")
        self.assertEqual(data["allowCommands"], 1)
        self.assertEqual(data["Time"], 0x1234)
        self.assertIn(b"\x04\x00\x04Time", gzip.decompress(modified))

    def test_selected_exports_are_byte_identical_and_preserve_data_version(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            manifest = export_v3(output, output / "manifest.json")
            for entry in manifest["structures"]:
                data = (output / entry["single_template"]["path"]).read_bytes()
                self.assertEqual(data, (ROOT / entry["source"]).read_bytes())
                self.assertEqual(hashlib.sha256(data).hexdigest(), entry["single_template"]["sha256"])
                self.assertEqual(decode_nbt(data)["DataVersion"], 3105)
                natural = decode_nbt((output / entry["worldgen_template"]["path"]).read_bytes())
                original = decode_nbt(data)
                def states(root):
                    return {tuple(b["pos"]): root["palette"][b["state"]]["Name"] for b in root["blocks"]}
                restored = states(natural)
                anchor = tuple(entry["worldgen_template"]["anchor"])
                marker = next(b for b in natural["blocks"] if tuple(b["pos"]) == anchor)
                self.assertEqual(marker["nbt"]["name"], "relics:center")
                final = marker["nbt"]["final_state"]
                if final == "minecraft:structure_void":
                    del restored[anchor]
                else:
                    restored[anchor] = final
                self.assertEqual(restored, states(original))

    def test_centered_footprints_stay_within_eight_chunk_reference_radius(self):
        for contract in ASSETS.values():
            sx, _, sz = contract["size"]
            for rotation in ("NONE", "CLOCKWISE_90", "CLOCKWISE_180", "COUNTERCLOCKWISE_90"):
                anchor = rotate((sx // 2, 0, sz // 2), rotation)
                for x in (0, sx - 1):
                    for z in (0, sz - 1):
                        corner = rotate((x, 0, z), rotation)
                        for coordinate in (0, 2):
                            self.assertLessEqual(abs((corner[coordinate] - anchor[coordinate]) // 16), 8)


if __name__ == "__main__":
    unittest.main()
