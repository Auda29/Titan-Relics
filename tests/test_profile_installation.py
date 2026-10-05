"""Runtime-evidence gates without modifying a Minecraft profile or save."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from install_test_profile import validate_reports
from relic_catalog import ASSETS


class InstallationGateTests(unittest.TestCase):
    def setUp(self):
        instances = [{"structure": "relics:" + name, "bounding_box_matches": True,
                      "missing_chunks": [], "incomplete_chunks": [], "checked_blocks": 1000,
                      "mismatch_count": 0} for name in ASSETS]
        self.natural = {"passed": True, "exit_code": 0, "blocking_log_errors": [],
                        "expected_natural_structures": [i["structure"] for i in instances],
                        "world_blocks": {"instances": copy.deepcopy(instances), "read_errors": [], "verification_errors": []}}
        self.showcase = {"passed": True, "showcase": True, "showcase_blocks": {"instances": instances}}

    def test_complete_current_runtime_evidence_qualifies(self):
        validate_reports(self.natural, self.showcase)

    def test_failed_showcase_does_not_qualify_even_with_override(self):
        self.showcase["passed"] = False
        with self.assertRaisesRegex(ValueError, "Showcase runtime"):
            validate_reports(self.natural, self.showcase, True)

    def test_subset_showcase_does_not_qualify(self):
        self.showcase["showcase_blocks"]["instances"].pop()
        with self.assertRaisesRegex(ValueError, "every current relic"):
            validate_reports(self.natural, self.showcase, True)

    def test_missing_rock_variant_cannot_be_overridden(self):
        self.natural["world_blocks"]["instances"] = [i for i in self.natural["world_blocks"]["instances"]
                                                       if i["structure"] != "relics:titan_skull_rock"]
        with self.assertRaisesRegex(ValueError, "missing/incomplete"):
            validate_reports(self.natural, self.showcase, True)

    def test_minor_edits_require_explicit_acknowledgement(self):
        self.natural["passed"] = False
        self.natural["world_blocks"]["instances"][0]["mismatch_count"] = 9
        with self.assertRaisesRegex(ValueError, "acknowledgement"):
            validate_reports(self.natural, self.showcase)
        validate_reports(self.natural, self.showcase, True)
        self.assertFalse(self.natural["passed"])  # Never relabel strict failure as a pass.

    def test_one_percent_edits_or_missing_chunks_cannot_be_overridden(self):
        first = self.natural["world_blocks"]["instances"][0]
        first["mismatch_count"] = 10
        with self.assertRaises(ValueError):
            validate_reports(self.natural, self.showcase, True)
        first["mismatch_count"] = 0
        first["missing_chunks"] = [[0, 0]]
        with self.assertRaises(ValueError):
            validate_reports(self.natural, self.showcase, True)


if __name__ == "__main__":
    unittest.main()
