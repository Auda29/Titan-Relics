import gzip
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from relic_assets import decode_nbt, named, nbt_payload
from schem_to_nbt import convert, read_schematic


def payload(tag, value):
    if tag == 2:
        return struct.pack(">h", value)
    if tag == 7:
        return struct.pack(">i", len(value)) + value
    if tag == 11:
        return struct.pack(">i", len(value)) + b"".join(struct.pack(">i", v) for v in value)
    if tag == 10:
        return b"".join(named(t, k, payload(t, v)) for k, (t, v) in value.items()) + b"\0"
    return nbt_payload(tag, value)


def fixture(version=2, raw=bytes([0, 1, 2, 1, 1, 1, 1, 1]), extra=None, palette=None):
    root = {"Version": (3, version), "DataVersion": (3, 4903),
            "Width": (2, 2), "Height": (2, 2), "Length": (2, 2), "Offset": (11, [-5, 6, 7])}
    blocks = {"Palette": (10, palette or {"minecraft:air": (3, 0), "minecraft:stone": (3, 1),
              "minecraft:oak_stairs[facing=east,half=top,shape=straight,waterlogged=false]": (3, 2)}),
              "Data" if version == 3 else "BlockData": (7, raw)}
    if version == 3:
        root["Blocks"] = (10, blocks)
    else:
        root.update(blocks)
    root.update(extra or {})
    if version == 3:
        root = {"Schematic": (10, root)}
    return gzip.compress(named(10, "Schematic" if version == 2 else "", payload(10, root)), mtime=0)


def restore(root):
    return {tuple(b["pos"]): root["palette"][b["state"]] for b in root["blocks"]}


class SchematicTests(unittest.TestCase):
    def test_versions_coordinates_and_air(self):
        for version in (2, 3):
            size, blocks, data_version, offset = read_schematic(fixture(version))
            self.assertEqual(size, (2, 2, 2))
            self.assertEqual(data_version, 4903)
            self.assertEqual(offset, [-5, 6, 7])
            self.assertNotIn((0, 0, 0), blocks)
            self.assertTrue(blocks[(0, 0, 1)].startswith("minecraft:oak_stairs["))
            self.assertEqual(blocks[(1, 1, 1)], "minecraft:stone")
            self.assertEqual(len(read_schematic(fixture(version), "keep")[1]), 8)

    def test_multibyte_palette_indices_and_structure_void(self):
        palette = {"minecraft:stone": (3, 128), "minecraft:structure_void": (3, 0)}
        _, blocks, _, _ = read_schematic(fixture(raw=b"\x80\x01" * 7 + b"\0", palette=palette), "keep")
        self.assertEqual(len(blocks), 7)
        self.assertNotIn((1, 1, 1), blocks)

    def test_rejects_unsupported_and_corrupt_data(self):
        cases = [fixture(version=1), fixture(raw=b"\x01"), fixture(raw=b"\x03" * 8),
                 fixture(raw=b"\x01" * 9), fixture(raw=b"\x80" * 8),
                 fixture(extra={"BlockEntities": (9, (10, [{"Id": (8, "minecraft:chest")}]))}),
                 fixture(extra={"Entities": (9, (10, [{"Id": (8, "minecraft:pig")}]))}),
                 fixture(extra={"Width": (2, -1)}), fixture(extra={"DataVersion": (3, 0)}),
                 fixture(palette={"minecraft:stone": (3, 1), "minecraft:dirt": (3, 1)})]
        for data in cases:
            with self.subTest(data=data), self.assertRaises(ValueError):
                read_schematic(data)
        with self.assertRaises(ValueError):
            decode_nbt(b"\x0a\0\0\x07\0\x01x\xff\xff\xff\xff\0")

    def test_conversion_properties_tiles_and_determinism(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "model.schem"
            output = Path(directory) / "model.nbt"
            source.write_bytes(fixture(3))
            manifest = convert(source, output, "omit", tile_size=1)
            data = output.read_bytes()
            root = decode_nbt(data)
            self.assertEqual(root["size"], [2, 2, 2])
            states = restore(root)
            self.assertEqual(states[(0, 0, 1)]["Properties"]["facing"], "east")
            recovered = {}
            for tile in manifest["tiles"]:
                for pos, state in restore(decode_nbt((output.parent / tile["path"]).read_bytes())).items():
                    recovered[tuple(v + o for v, o in zip(pos, tile["origin"]))] = state
            self.assertEqual(recovered, states)
            self.assertEqual(json.loads(output.with_suffix(".manifest.json").read_text()), manifest)
            convert(source, output, "omit", tile_size=1)
            self.assertEqual(output.read_bytes(), data)
            with self.assertRaises(ValueError):
                convert(source, source, "omit")


if __name__ == "__main__":
    unittest.main()
