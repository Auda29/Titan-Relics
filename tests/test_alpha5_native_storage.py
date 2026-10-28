"""The independent world verifier must require the correct persisted loader data."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from verify_world import protected_cell,protection_sections


class NativeProtectionStorageTests(unittest.TestCase):
    def test_negative_sections_and_signed_high_bits_survive_both_loader_formats(self):
        for pos in ((-3,-17,-7),(15,0,3)):
            index=((pos[1]&15)<<8)|((pos[2]&15)<<4)|(pos[0]&15)
            mask=[0]*64;value=1<<(index&63)
            mask[index>>6]=value if value<1<<63 else value-(1<<64)
            sections={str(pos[1]//16):mask}
            for loader,value in (('fabric',sections),('neoforge',{'sections':sections})):
                chunk={loader+':attachments':{'relics:placed_cells':value}}
                with self.subTest(loader=loader,pos=pos):
                    self.assertTrue(protected_cell(chunk,pos,loader=loader))
                    self.assertTrue(protected_cell(chunk,pos))
                    self.assertFalse(protected_cell(chunk,(pos[0]-1,pos[1],pos[2]),loader=loader))
                    self.assertFalse(protected_cell(chunk,pos,loader='fabric' if loader=='neoforge' else 'neoforge'))

    def test_ambiguous_and_malformed_native_data_fail_closed(self):
        dual={'fabric:attachments':{'relics:placed_cells':{}},'neoforge:attachments':{'relics:placed_cells':{'sections':{}}}}
        with self.assertRaisesRegex(ValueError,'Ambiguous'):protection_sections(dual)
        for malformed in ([],{}, {'sections':[]}, {'0':[0]*64}):
            with self.subTest(value=malformed),self.assertRaisesRegex(ValueError,'Invalid NeoForge'):
                protected_cell({'neoforge:attachments':{'relics:placed_cells':malformed}},(0,0,0),loader='neoforge')


if __name__=='__main__':unittest.main()
