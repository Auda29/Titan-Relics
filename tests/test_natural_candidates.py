"""A nominated site never substitutes for actual natural structure generation."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from smoke_server import read_candidate_sites


class NaturalCandidateTests(unittest.TestCase):
    def read(self, data):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'candidates.json'
            path.write_text(json.dumps(data))
            return read_candidate_sites(path, {'test': {}}, 731204)

    def test_seed_matched_chunk_origins_are_accepted_as_nominations_only(self):
        self.assertEqual(self.read({'seed': 731204, 'candidates': {'test': [{'x': -16, 'z': 32}]}}),
                         {'test': [{'x': -16, 'z': 32}]})

    def test_missing_templates_or_wrong_seed_fail(self):
        for data in ({'seed': 1, 'candidates': {'test': [{'x': 0, 'z': 0}]}},
                     {'seed': 731204, 'candidates': {}},
                     {'seed': 731204, 'candidates': {'test': []}}):
            with self.assertRaises(ValueError):
                self.read(data)

    def test_non_chunk_or_non_integer_coordinates_fail(self):
        for x in (1, 16.0, True, None):
            with self.assertRaises(ValueError):
                self.read({'seed': 731204, 'candidates': {'test': [{'x': x, 'z': 0}]}})
