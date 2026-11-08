"""A remote authentication-key outage must not hide game/loader errors in local QA."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from test_alpha5_port_server import external_key_fetch_error,game_error

class PortConsoleTests(unittest.TestCase):
    def test_exact_remote_key_failure_is_retained_as_external(self):
        line='[15:00:52] [Yggdrasil Key Fetcher/ERROR] [mojang/YggdrasilServicesKeyInfo]: Failed to request yggdrasil public key'
        self.assertTrue(external_key_fetch_error(line))
        self.assertFalse(game_error(line))

    def test_registry_mixin_and_other_key_fetcher_errors_still_fail(self):
        for line in ('[main/ERROR]: Registry loading errors:',
                     '[main/ERROR]: Mixin apply failed',
                     '[Yggdrasil Key Fetcher/ERROR]: Unexpected runtime failure',
                     '[Server thread/ERROR]: Failed to request yggdrasil public key'):
            with self.subTest(line=line):self.assertTrue(game_error(line))
