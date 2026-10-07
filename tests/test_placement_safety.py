"""Reservation contracts, overlap checks and fail-closed installation of terrain fixes."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from compile_worldgen import checked_classes, source_hash
from relic_catalog import ASSETS, FAMILIES, members, reservations, worldgen_resources
from terrain_foundations import POLICY, natural_size, natural_ground
from verify_world import structure_overlaps
import test_profile_installation as profile_tests
from install_test_profile import validate_reports
from install_test_profile import validate_natural


class PlacementSafetyTests(unittest.TestCase):
    def test_each_pair_has_exactly_one_reservation_and_a_safe_radius(self):
        for index, family in enumerate(FAMILIES):
            entries = reservations(family)
            self.assertEqual([r["set"] for r in entries[:-1]], ["relics:" + f for f in FAMILIES[:index]])
            self.assertEqual(entries[-1]["set"], "relics:" + family)
            self.assertTrue(entries[-1]["earlier_only"])
            for entry in entries:
                other = entry["set"].split(":")[1]
                for name in members(family):
                    for other_name in members(other):
                        radius = max(natural_size(ASSETS[name])[0::2]) / 2
                        other_radius = max(natural_size(ASSETS[other_name])[0::2]) / 2
                        # Even at adversarial chunk offsets there is no shared column.
                        self.assertGreater((entry["clearance_chunks"] + 1) * 16 - 17, radius + other_radius)

    def test_every_natural_pool_uses_the_matching_ground_support_processor(self):
        resources = worldgen_resources()
        for name, contract in ASSETS.items():
            self.assertEqual(resources[f"worldgen/template_pool/{name}.json"]["elements"][0]["element"]["processors"],
                             f"relics:{name}_terrain")
            expected = {"processors": [{"processor_type": "relics:terrain_support", "ground_y": natural_ground(contract),
                                 "support_art": True, "art_fill": {"Name":
                                     "minecraft:sandstone" if name in ('obelisk','titan_skull_sand') else
                                     "minecraft:stone" if name=='titan_skull_rock' else "minecraft:dirt"}}]}
            if name == 'world_tree':
                expected['processors'][0]['root_support'] = True
            self.assertEqual(resources[f"worldgen/processor_list/{name}_terrain.json"], expected)

    def test_sea_level_land_still_requires_actual_dry_surface_at_every_sample(self):
        for data in worldgen_resources().values():
            if data.get("type") != "lithostitched:delegating":
                continue
            grid = data["spawn_condition"]["terrain_condition"]["condition"]
            self.assertEqual(grid["type"], "relics:all_grid")
            conditions = grid["condition"]["conditions"]
            self.assertEqual(conditions[1]["permitted_range"]["min_inclusive"], 63)
            self.assertIn({"type": "relics:dry_land"}, conditions)

    def test_horizontal_overlap_including_edges_and_negative_coordinates_is_reported(self):
        a = {"structure": "a", "bounding_box": [-100, 0, -100, 0, 100, 0]}
        b = {"structure": "b", "bounding_box": [0, 200, 0, 100, 300, 100]}
        self.assertEqual(len(structure_overlaps([a, b])), 1)
        b["bounding_box"][0] = 1
        self.assertEqual(structure_overlaps([a, b]), [])

    def test_unsupported_foundations_and_overlap_cannot_use_feature_allowance(self):
        fixture = profile_tests.InstallationGateTests()
        fixture.setUp()
        natural = copy.deepcopy(fixture.natural)
        natural["passed"] = False
        natural["world_blocks"]["instances"][0]["foundation_contact"] = {"passed": False}
        with self.assertRaisesRegex(ValueError, "missing/incomplete"):
            validate_reports(natural, fixture.showcase, True)
        natural["world_blocks"]["instances"][0]["foundation_contact"]["passed"] = True
        natural["world_blocks"]["overlaps"] = [{"first": "a", "second": "b"}]
        with self.assertRaises(ValueError):
            validate_reports(natural, fixture.showcase, True)

    def test_runtime_policy_requires_explicit_foundation_evidence(self):
        fixture = profile_tests.InstallationGateTests()
        fixture.setUp()
        fixture.natural["asset_selection"] = {"foundation_policy": POLICY}
        with self.assertRaises(ValueError):
            validate_reports(fixture.natural, fixture.showcase, True)
        for instance in fixture.natural["world_blocks"]["instances"]:
            instance["foundation_contact"] = {"passed": True}
        with self.assertRaises(ValueError):
            validate_reports(fixture.natural, fixture.showcase, True)
        for instance in fixture.natural["world_blocks"]["instances"]:
            instance["feature_protection"] = {"passed": True}
        validate_reports(fixture.natural, fixture.showcase)

    def test_terrain_preview_cannot_bypass_installation_gate(self):
        fixture = profile_tests.InstallationGateTests()
        fixture.setUp()
        expected = {"relics:" + name for name in ASSETS}
        first = fixture.natural["world_blocks"]["instances"][0]
        first["mismatch_count"] = 1
        with self.assertRaisesRegex(ValueError, "acknowledgement"):
            validate_natural(fixture.natural, expected)
        validate_natural(fixture.natural, expected, True)
        first["foundation_contact"] = {"passed": False}
        with self.assertRaisesRegex(ValueError, "missing/incomplete"):
            validate_natural(fixture.natural, expected, True)

    def test_packaging_rejects_stale_modified_or_escaping_java_classes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifest = {"source_sha256": "stale", "classes": {"example.class": "wrong"}}
            path = root / "manifest.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Stale"):
                checked_classes(root)
            manifest["source_sha256"] = source_hash()
            (root / "example.class").write_bytes(b"modified")
            path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Modified"):
                checked_classes(root)
            manifest["classes"] = {"../escape.class": "wrong"}
            path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Invalid"):
                checked_classes(root)


if __name__ == "__main__":
    unittest.main()
