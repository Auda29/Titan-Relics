"""Runtime-evidence gates without modifying a Minecraft profile or save."""
import copy
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from install_test_profile import validate_reports
import install_test_profile as installer
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

    def test_terrain_only_install_keeps_showcase_gate_and_preserves_existing_world(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            profile=root/'profile';mods=profile/'mods';mods.mkdir(parents=True)
            save=profile/'saves'/'existing';save.mkdir(parents=True)
            (save/'preserve.txt').write_bytes(b'unchanged save')
            def jar(path,mod_id):
                with zipfile.ZipFile(path,'w') as archive:
                    archive.writestr('fabric.mod.json',json.dumps({'id':mod_id}))
            old=mods/'relics-old.jar';jar(old,'relics');old_bytes=old.read_bytes()
            jar(mods/'fabric-api.jar','fabric-api');jar(mods/'lithostitched.jar','lithostitched')
            resources=root/'src/main/resources';resources.mkdir(parents=True)
            version='0.1.0-alpha.4.9'
            (resources/'fabric.mod.json').write_text(json.dumps({'version':version}))
            dist=root/'dist';dist.mkdir()
            artifact=dist/f'relics-{version}+mc26.2.jar';jar(artifact,'relics')
            artifacts=[{'file':artifact.name,'sha256':hashlib.sha256(artifact.read_bytes()).hexdigest()}]
            natural=copy.deepcopy(self.natural)
            for instance in natural['world_blocks']['instances']:instance['mismatch_kinds']={}
            natural['artifacts']=artifacts
            showcase=dict(self.showcase,artifacts=artifacts)
            np=root/'natural.json';sp=root/'showcase.json'
            np.write_text(json.dumps(natural));sp.write_text(json.dumps(dict(showcase,passed=False)))
            with patch.object(installer,'ROOT',root),patch.object(installer.subprocess,'run',
                    return_value=SimpleNamespace(stdout='')),patch('sys.argv',[
                    'install_test_profile.py','--profile',str(profile),'--natural-report',str(np),
                    '--showcase-report',str(sp),'--no-showcase-world']),contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(ValueError,'Showcase runtime'):
                    installer.main()
                self.assertEqual(old.read_bytes(),old_bytes)
                sp.write_text(json.dumps(showcase))
                self.assertEqual(installer.main(),0)
            self.assertFalse(old.exists())
            self.assertEqual((mods/artifact.name).read_bytes(),artifact.read_bytes())
            backup=next((root/'build/profile-backups').iterdir())
            self.assertEqual((backup/old.name).read_bytes(),old_bytes)
            record=json.loads((backup/'installation.json').read_bytes())
            self.assertIsNone(record['showcase_world'])
            self.assertIsNone(record['world_title'])
            self.assertEqual([p.name for p in (profile/'saves').iterdir()],['existing'])
            self.assertEqual((save/'preserve.txt').read_bytes(),b'unchanged save')

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
