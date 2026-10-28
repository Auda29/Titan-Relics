"""Verify published handoff bytes, including Windows-authored provenance on POSIX."""
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class ReleaseHandoffs(unittest.TestCase):
    def test_all_october_28_bindings_survive_git_export(self):
        checked=0
        def verify(relative,sha,size=None):
            nonlocal checked
            path=ROOT/relative.replace('\\','/')
            self.assertTrue(path.resolve().is_relative_to(ROOT.resolve()))
            data=path.read_bytes();self.assertEqual(hashlib.sha256(data).hexdigest(),sha,relative)
            if size is not None:self.assertEqual(len(data),size,relative)
            checked+=1
        def walk(value):
            if isinstance(value,dict):
                if 'path' in value and 'sha256' in value:verify(value['path'],value['sha256'],value.get('bytes'))
                for item in value.values():walk(item)
            elif isinstance(value,list):
                for item in value:walk(item)
        for index in (ROOT/'docs/project/reviews').glob('*20261028-handoff.json'):walk(json.loads(index.read_text(encoding='utf-8')))
        manifest=ROOT/'relics/titan-skull/design/generated/titan-skull-2-v2-embedded-side-v1/hashes.json'
        for path,sha in json.loads(manifest.read_text()).items():verify(path,sha)
        self.assertGreaterEqual(checked,1598)

if __name__=='__main__':unittest.main()
