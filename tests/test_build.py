"""Validate configuration overrides and reproducible packaging."""
import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


build = module("build")
configure = module("configure")


class ConfigurationTests(unittest.TestCase):
    def test_disabled_structure_preserves_salt_and_removes_candidates(self):
        generated = configure.settings_resources("frequent", ["colossus"])
        colossus = json.loads(generated["data/relics/worldgen/structure_set/colossus.json"])
        original = json.loads((ROOT / "src/main/resources/data/relics/worldgen/structure_set/colossus.json").read_text())
        self.assertEqual(colossus["structures"], [])
        self.assertEqual(colossus["placement"]["salt"], original["placement"]["salt"])
        obelisk = json.loads(generated["data/relics/worldgen/structure_set/obelisk.json"])
        self.assertEqual(obelisk["structures"][0]["structure"], "relics:obelisk")

    def test_preset_spacing_is_valid_and_ordered(self):
        for name in ("obelisk", "colossus"):
            spacings = []
            for preset in ("frequent", "normal", "rare"):
                data = json.loads(configure.settings_resources(preset, [])[f"data/relics/worldgen/structure_set/{name}.json"])
                p = data["placement"]
                self.assertGreater(p["spacing"], p["separation"])
                self.assertGreater(p["separation"], 0)
                spacings.append(p["spacing"])
            self.assertEqual(spacings, sorted(set(spacings)))

    def test_invalid_settings_fail(self):
        with self.assertRaises(ValueError):
            configure.settings_resources("unexpected", [])
        with self.assertRaises(ValueError):
            configure.settings_resources("normal", ["typo"])

    def test_settings_archive_has_fixed_portable_metadata(self):
        with tempfile.TemporaryDirectory() as td:
            destination = Path(td) / "settings.zip"
            subprocess.run([sys.executable, str(ROOT / "tools/configure.py"), "--disable", "colossus",
                            "--output", str(destination)], check=True, capture_output=True)
            with zipfile.ZipFile(destination) as archive:
                for info in archive.infolist():
                    self.assertEqual(info.create_system, 3)
                    self.assertEqual(info.external_attr, 0o100644 << 16)
                    self.assertEqual(info.date_time, (2026, 1, 1, 0, 0, 0))


class PackagingTests(unittest.TestCase):
    def test_archive_is_identical_despite_changed_source_timestamp(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            resources = root / "resources"
            resources.mkdir()
            source = resources / "example.json"
            source.write_text('{"value": 1}\n', encoding="utf-8")
            first = build.write_archive(root / "first.jar", resources)
            source.touch()
            second = build.write_archive(root / "second.jar", resources)
            self.assertEqual(first, second)
            with zipfile.ZipFile(root / "second.jar") as z:
                self.assertEqual(json.loads(z.read("example.json")), json.loads(source.read_bytes()))
                info = z.getinfo("example.json")
                self.assertEqual(info.create_system, 3)
                self.assertEqual(info.external_attr, 0o100644 << 16)
                self.assertEqual(info.date_time, (2026, 1, 1, 0, 0, 0))

    def test_json_packaging_ignores_windows_line_endings_and_key_order(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            resources = root / "resources"
            resources.mkdir()
            source = resources / "example.json"
            source.write_bytes(b'{"a": 1,\r\n"b": 2}\r\n')
            first = build.write_archive(root / "first.jar", resources)
            source.write_bytes(b'{"b": 2,\n"a": 1}\n')
            self.assertEqual(first, build.write_archive(root / "second.jar", resources))

    def test_loaded_resource_graph_has_complete_fixed_templates(self):
        build.check_resources()
        for name in ("obelisk", "colossus"):
            pool = json.loads((build.RESOURCES / f"data/relics/worldgen/template_pool/{name}.json").read_text())
            self.assertEqual(len(pool["elements"]), 1)
            self.assertEqual(pool["elements"][0]["element"]["location"], f"relics:{name}")
            structure = json.loads((build.RESOURCES / f"data/relics/worldgen/structure/{name}.json").read_text())
            self.assertEqual(structure["delegate"]["size"], 1)
            self.assertEqual(structure["delegate"]["start_pool"], f"relics:{name}")


if __name__ == "__main__":
    unittest.main()
