"""Missing native palettes must be caught even when dedicated servers load successfully."""
import json
from pathlib import Path
import sys,tempfile,unittest,zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from verify_port_assets import verify


class PortAssetsTests(unittest.TestCase):
    def test_unavailable_material_palette_rejects_the_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);mod=root/'mod.jar';game=root/'client.jar'
            atlas={'sources':[{'type':'minecraft:paletted_permutations','palette_key':'minecraft:trims/color_palettes/trim_palette',
                'textures':['relics:trims/models/armor/monolith'],'permutations':{'copper_darker':'minecraft:trims/color_palettes/copper_darker'}}]}
            with zipfile.ZipFile(mod,'w') as z:
                z.writestr('assets/minecraft/atlases/armor_trims.json',json.dumps(atlas))
                z.writestr('assets/relics/textures/trims/models/armor/monolith.png',b'checked separately by image tests')
            with zipfile.ZipFile(game,'w') as z:z.writestr('assets/minecraft/textures/trims/color_palettes/trim_palette.png',b'palette')
            with self.assertRaisesRegex(ValueError,'copper_darker'):verify(mod,game)
            with zipfile.ZipFile(game,'a') as z:z.writestr('assets/minecraft/textures/trims/color_palettes/copper_darker.png',b'palette')
            self.assertTrue(verify(mod,game)['passed'])


if __name__=='__main__':unittest.main()
