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
sys.path.insert(0, str(ROOT / "tools"))
from relic_catalog import ASSETS, FAMILIES, members


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
        for name in FAMILIES:
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

    def test_titan_skull_can_be_disabled_independently(self):
        generated = configure.settings_resources("normal", ["titan_skull"])
        skull = json.loads(generated["data/relics/worldgen/structure_set/titan_skull.json"])
        self.assertEqual(skull["structures"], [])
        self.assertEqual(skull["placement"]["salt"], 206091303)
        for name in ("obelisk", "colossus"):
            data = json.loads(generated[f"data/relics/worldgen/structure_set/{name}.json"])
            self.assertEqual(len(data["structures"]), 1)

    def test_every_family_can_be_disabled_without_disabling_other_families(self):
        for disabled in FAMILIES:
            generated = configure.settings_resources("normal", [disabled])
            for family in FAMILIES:
                data = json.loads(generated[f"data/relics/worldgen/structure_set/{family}.json"])
                expected = [] if family == disabled else ["relics:" + name for name in members(family)]
                self.assertEqual([s["structure"] for s in data["structures"]], expected)

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
    def test_archive_retains_canonical_license_and_credits_instead_of_stale_copies(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            resources = root / 'resources'
            resources.mkdir()
            for name in ('LICENSE', 'CREDITS.md'):
                (resources / name).write_text('stale notice', encoding='utf-8')
            build.write_archive(root / 'player.jar', resources)
            with zipfile.ZipFile(root / 'player.jar') as archive:
                for name in ('LICENSE', 'CREDITS.md'):
                    self.assertEqual(archive.namelist().count(name), 1)
                    self.assertEqual(archive.read(name).decode('utf-8'),
                                     (ROOT / name).read_text(encoding='utf-8'))

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
        for name in ASSETS:
            pool = json.loads((build.RESOURCES / f"data/relics/worldgen/template_pool/{name}.json").read_text())
            self.assertEqual(len(pool["elements"]), 1)
            self.assertEqual(pool["elements"][0]["element"]["location"], f"relics:{name}_worldgen")
            structure = json.loads((build.RESOURCES / f"data/relics/worldgen/structure/{name}.json").read_text())
            self.assertEqual(structure["delegate"]["size"], 1)
            self.assertEqual(structure["delegate"]["start_pool"], f"relics:{name}")

    def test_archive_excludes_stale_and_nested_debug_templates(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            resources = root / "resources"
            for relative in ("colossus.nbt", "colossus_worldgen.nbt", "old_candidate.nbt",
                             "debug/colossus.nbt", "colossus/tile_0.nbt"):
                path = resources / "data/relics/structure" / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"fixture")
            build.write_archive(root / "test.jar", resources)
            with zipfile.ZipFile(root / "test.jar") as archive:
                self.assertEqual(set(archive.namelist()), {"LICENSE", "CREDITS.md", "data/relics/structure/colossus.nbt",
                                                         "data/relics/structure/colossus_worldgen.nbt"})


if __name__ == "__main__":
    unittest.main()
