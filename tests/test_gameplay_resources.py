"""Original artwork/resource wiring checks. No Minecraft or Fabric runtime claim."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import generate_gameplay_art as art

class GameplayResourceTests(unittest.TestCase):
    def test_original_art_generator_reproduces_committed_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(art, 'ROOT', root), patch.object(art, 'ASSETS', root / 'relics'):
                art.generate()
            files = list(root.rglob('*'))
            self.assertTrue(files)
            for generated in files:
                if not generated.is_file(): continue
                committed = ROOT / 'src/main/resources/assets' / generated.relative_to(root)
                with self.subTest(path=generated.relative_to(root)):
                    if generated.suffix == '.png':
                        # Compare artwork, not host/Pillow-specific PNG compression streams.
                        with Image.open(generated) as actual, Image.open(committed) as expected:
                            self.assertEqual((actual.mode,actual.size,actual.tobytes()),(expected.mode,expected.size,expected.tobytes()))
                    else:
                        self.assertNotIn(b'\r',generated.read_bytes(), 'Published JSON uses LF on every host')
                        self.assertEqual(hashlib.sha256(generated.read_bytes()).hexdigest(), hashlib.sha256(committed.read_bytes()).hexdigest())

    def test_item_sprites_models_and_states_have_complete_references(self):
        assets = ROOT / 'src/main/resources/assets/relics'
        for base in art.SPRITES:
            variants = ['', '_partial', '_empty'] if base in ('machine_core','salvage_magnet') else ['']
            hashes = set()
            for suffix in variants:
                name = base + suffix
                with self.subTest(name=name):
                    png = assets / 'textures/item' / f'{name}.png'
                    with Image.open(png) as image:
                        self.assertEqual(image.size, (16,16)); self.assertEqual(image.mode, 'RGBA')
                        hashes.add(hashlib.sha256(image.tobytes()).hexdigest())
                    item = json.loads((assets / 'items' / f'{name}.json').read_text())
                    self.assertEqual(item['model'], {'type':'minecraft:model','model':f'relics:item/{name}'})
                    model = json.loads((assets / 'models/item' / f'{name}.json').read_text())
                    self.assertEqual(model['parent'], 'minecraft:item/generated')
                    self.assertEqual(model['textures']['layer0'], f'relics:item/{name}')
            self.assertEqual(len(hashes),len(variants), 'Icon states must actually differ')

    def test_trim_atlas_is_additive_and_masks_use_palette_keys(self):
        assets = ROOT / 'src/main/resources/assets'
        atlas = json.loads((assets / 'minecraft/atlases/armor_trims.json').read_text())
        source = atlas['sources'][0]
        self.assertEqual(source['type'],'minecraft:paletted_permutations')
        self.assertEqual(len(source['textures']),2)
        self.assertEqual(len(source['permutations']),16)
        for resource in source['textures']:
            namespace,path = resource.split(':')
            with Image.open(assets / namespace / 'textures' / f'{path}.png') as image:
                self.assertEqual(image.size,(64,32))
                visible = [pixel for pixel in image.getdata() if pixel[3]]
                self.assertGreater(len(visible),0)
                self.assertLess(len(visible),200, 'Narrow trim, not full armor coverage')
                self.assertTrue(all(r==g==b and r in (192,128) and a==255 for r,g,b,a in visible))

    def test_translations_match_and_recipes_do_not_add_unapproved_construction(self):
        resources = ROOT / 'src/main/resources'
        en = json.loads((resources/'assets/relics/lang/en_us.json').read_text(encoding='utf-8'))
        de = json.loads((resources/'assets/relics/lang/de_de.json').read_text(encoding='utf-8'))
        self.assertEqual(set(en),set(de))
        self.assertEqual(de['item.relics.machine_core'],'Maschinenkern')
        self.assertEqual(de['item.relics.salvage_magnet'],'Bergungsmagnet')
        self.assertEqual({p.stem for p in (resources/'data/relics/recipe').glob('*.json')},
                         {'machine_core_recharge','salvage_magnet_repair','monolith_template_copy','monolith_armor_trim'})
        self.assertEqual(json.loads((resources/'data/relics/recipe/monolith_template_copy.json').read_text())['pattern'],['DTD','DCD','DDD'])

    def test_trim_stays_on_native_equipment_and_off_transparent_openings(self):
        # Native 26.2 baked meshes and equipment alpha were extracted separately
        # with ArmorUvEvidence.java; this catches arm/boot/face overpainting.
        evidence=json.loads((ROOT/'docs/project/reviews/monolith-native-armor-26.2.json').read_text())
        self.assertEqual(len(evidence['faces']),60)
        self.assertEqual({f['slot'] for f in evidence['faces']},{'head','chest','legs','feet'})
        for kind,opaque in evidence['opaque_uv'].items():
            mask=Image.open(ROOT/'src/main/resources/assets/relics/textures/trims/entity'/kind/'monolith.png').convert('RGBA')
            visible={y*64+x for y in range(32) for x in range(64) if mask.getpixel((x,y))[3]}
            self.assertTrue(visible<=set(opaque),kind+' paints transparent native armor')
            relevant=[f for f in evidence['faces'] if (f['slot']=='legs')==(kind=='humanoid_leggings')]
            used=set()
            for face in relevant:
                xs=[round(v[3]*64) for v in face['vertices']];ys=[round(v[4]*32) for v in face['vertices']]
                used.update(y*64+x for y in range(min(ys),max(ys)) for x in range(min(xs),max(xs)))
            self.assertTrue(visible<=used,'Trim outside baked native UV faces')

    def test_legacy_visual_metadata_does_not_inherit_gameplay_dependencies(self):
        legacy = json.loads((ROOT/'compat/mc1.21.1/visual-alpha49.fabric.mod.json').read_text())
        self.assertEqual(legacy['version'],'0.1.0-alpha.4.9')
        self.assertNotIn('fabric-creative-tab-api-v1',legacy['depends'])

    def test_fixed_reward_tables_have_no_extra_rolls_or_random_functions(self):
        resources=ROOT/'src/main/resources/data/relics/loot_table/gameplay'
        for name,item in [('trial_key','colossus_key'),('vault_core','machine_core')]:
            table=json.loads((resources/f'{name}.json').read_text())
            self.assertEqual(table,{'type':'minecraft:generic','pools':[{'rolls':1,'entries':[{'type':'minecraft:item','name':f'relics:{item}'}]}]})

if __name__ == '__main__': unittest.main()
