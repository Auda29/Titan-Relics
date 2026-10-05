"""Compact evidence preserves failed results and the complete report's hash."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from record_runtime_evidence import summarize


class RuntimeEvidenceTests(unittest.TestCase):
    def test_summary_preserves_failure_counts_and_source_hash_portably(self):
        report = {"run_directory": r"C:\checkout\build\smoke\run-test", "seed": 42,
                  "passed": False, "exit_code": 0, "artifacts": [],
                  "world_blocks": {"instances": [{"structure": "relics:colossus", "checked_blocks": 100,
                                                  "mismatch_count": 1, "passed": False}]}}
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "report.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            result = summarize(path)
            self.assertEqual(result["run"], "run-test")
            self.assertEqual(result["report_sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertFalse(result["passed"])
            self.assertEqual(result["instances"][0]["mismatch_count"], 1)
            self.assertFalse(result["instances"][0]["passed"])

    def test_unfinished_report_is_not_published_as_completed_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "report.json"
            path.write_text('{"passed": false}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "completed runtime report"):
                summarize(path)


if __name__ == "__main__":
    unittest.main()
