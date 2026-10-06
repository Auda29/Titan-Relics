"""Keep per-relic documentation and asset paths consistent without Blender."""
import ast
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RELICS = ("colossus", "obelisk", "titan-skull", "ruined-tower", "world-tree")


class RepositoryLayoutTests(unittest.TestCase):
    def test_each_relic_has_separate_documentation_design_and_gameplay(self):
        for relic in RELICS:
            directory = ROOT / "relics" / relic
            with self.subTest(relic=relic):
                self.assertTrue((directory / "README.md").is_file())
                for area in ("docs", "design", "gameplay"):
                    self.assertTrue((directory / area).is_dir())

    def test_local_documentation_links_resolve(self):
        documents = list(ROOT.glob("*.md"))
        documents += list((ROOT / "docs").rglob("*.md"))
        documents += list((ROOT / "relics").rglob("*.md"))
        for document in documents:
            text = document.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^\s)]+)\)", text):
                if re.match(r"(?:[a-z]+:|#|/)", target):
                    continue
                path = target.split("#", 1)[0]
                with self.subTest(document=document.relative_to(ROOT), target=target):
                    self.assertTrue((document.parent / path).exists(), "Broken local documentation link")

    def test_asset_configs_and_published_reports_share_relocated_paths(self):
        configs = sorted((ROOT / "relics").glob("*/design/*.json"))
        self.assertTrue(configs, "No asset configurations found")
        for path in configs:
            with self.subTest(config=path.relative_to(ROOT)):
                config = json.loads(path.read_text(encoding="utf-8"))
                directory = path.parent / "generated"
                if config.get('authoring')=='block-terrain-derivative':
                    source=ROOT/config['source_nbt'];output=ROOT/config['output']
                    self.assertTrue(source.is_file())
                    self.assertTrue(source.is_relative_to(directory))
                    self.assertTrue(output.is_relative_to(directory))
                    self.assertNotEqual(source,output.with_suffix('.nbt'))
                    self.assertTrue(output.is_file())
                    self.assertTrue(output.with_suffix('.nbt').is_file())
                    report=json.loads((output.parent/'verification.json').read_text())
                    self.assertEqual(report['source'],config['source_nbt'])
                    self.assertTrue(report['non_terrain_cells_identical'])
                    self.assertTrue(report['contact_columns_identical'])
                    continue
                input_path = ROOT / config["input"]
                output = ROOT / config["output"]
                self.assertTrue(input_path.is_relative_to(directory))
                self.assertTrue(output.is_relative_to(directory))
                self.assertEqual(input_path.parent, output.parent)
                self.assertEqual(input_path.suffix, ".obj")
                self.assertEqual(output.suffix, ".schem")
                self.assertTrue(output.is_file())
                self.assertTrue(output.with_suffix(".nbt").is_file())
                report = json.loads(output.with_suffix(".ots.json").read_text(encoding="utf-8"))
                self.assertEqual(report["input"], config["input"])
                self.assertEqual(report["output"], config["output"])
                comparison = config.get("preview", {}).get("comparison", "")
                if comparison.startswith("relics/"):
                    self.assertTrue((ROOT / comparison).is_file())

    def test_python_tools_do_not_use_the_old_asset_root(self):
        for path in (ROOT / "tools").glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    with self.subTest(tool=path.name, value=node.value[:80]):
                        self.assertFalse(node.value.startswith("design/"), "Stale shared design path")


if __name__ == "__main__":
    unittest.main()
