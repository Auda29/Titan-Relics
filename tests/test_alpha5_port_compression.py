"""Derived 1.21.1 template bytes must not depend on the host zlib OS marker."""
import gzip
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from prepare_alpha5_port import legacy_gzip


class PortCompressionTests(unittest.TestCase):
    def test_linux_and_windows_zlib_headers_produce_the_same_ported_bytes(self):
        raw=b'unchanged structure payload'*100
        stream=gzip.compress(raw,mtime=0)
        outputs=[]
        for host in (3,10):
            with patch('prepare_alpha5_port.gzip.compress',return_value=stream[:9]+bytes([host])+stream[10:]):
                outputs.append(legacy_gzip(raw))
        self.assertEqual(outputs[0],outputs[1])
        self.assertEqual(gzip.decompress(outputs[0]),raw)


if __name__=='__main__':unittest.main()
