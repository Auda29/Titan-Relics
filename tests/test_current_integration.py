"""Current selection identity, placements, variants and fail-closed packaging."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build import check_resources
from integrate_relics import export_relics, integrate
from relic_assets import decode_nbt
from relic_catalog import ASSETS, FAMILIES, members, worldgen_resources
from verify_world import rotate, states_match
from create_terrain_test_world import front_view, placement_regions
from terrain_foundations import natural_ground, natural_size, supported_blocks


def states(root):
    return {tuple(b["pos"]): root["palette"][b["state"]] for b in root["blocks"]}


class CurrentIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.output = Path(cls.directory.name)
        cls.manifest = export_relics(cls.output, cls.output / "manifest.json")

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_all_ten_exports_are_byte_identical_with_original_data_version(self):
        self.assertEqual(len(self.manifest["structures"]), 10)
        self.assertEqual(len(FAMILIES), 7)
        for a in self.manifest["structures"]:
            data = (self.output / a["single_template"]["path"]).read_bytes()
            self.assertEqual(data, (ROOT / a["source"]).read_bytes())
            self.assertEqual(hashlib.sha256(data).hexdigest(), ASSETS[a["id"]]["sha256"])
            self.assertEqual(decode_nbt(data)["DataVersion"], 3105)

    def test_alpha49_selects_cave_candidates_and_keeps_eight_other_natural_templates(self):
        unchanged_hashes = {
            "colossus": "a355b20349513cb27e6feb6fc171ca413d71da2cdb5717f7995afb4128d879b8",
            "obelisk": "ed116dcbca2a41fe403695a816e419a32a647d325c1d907d8dc1797f551cda3e",
        }
        revisions = {
            "titan_skull": ("titan-skull-v4-meadow-ground-v3", [117, 79, 179], 111328, 16, 12,
                            "b189932ac224097ba030a649ea2b44c898aaa4fdfbddb42b8797c32851ae5969"),
            "titan_skull_dry": ("titan-skull-v4-dry-ground-v3", [117, 79, 179], 111328, 16, 12,
                                "0d948527040a395b55615dce8704d72a2d5528b44c0b0c69ff94ea06b465eb67"),
            "titan_skull_sand": ("titan-skull-v4-sand-ground-v3", [117, 79, 179], 111328, 16, 12,
                                 "7106438dd1a0389dc5953f48351fa8a4aebfa1af3becd671d16288ab847bd0aa"),
            "titan_skull_rock": ("titan-skull-v4-rock-embedded-v1", [117, 79, 179], 20131, 22, 12,
                                 "b60d3ab92e4e8b99e5674f82588c38c25a7e7fe9eb8135a3fdf22a576f7b30c4"),
            "small_colossus": ("small-colossus-v7-ground-v3", [111, 80, 113], 233448, 13, 4,
                               "a64a22e00ae9d3499df0d0110273caa1db5e0075168fbbf9eb0c6978f2484021"),
            "world_tree": ("world-tree-v4-3-strands", [187, 228, 185], 289005, 24, 6,
                           "4f4fed24edd04f207c76162dc441093fc485e90149c8bc106cf51cc4a1248f14"),
            "ruined_tower": ("ruined-tower-v7-ground-v3", [111, 232, 93], 272528, 12, 6,
                             "faf9644ce0772f8b289c5c892016cdecbd94c65a45f3bde98fdca58c2adcc600"),
            "titan_skull_2": ("titan-skull-2-v2-embedded-v1", [99, 136, 99], 32569, 28, 4,
                             "80d4cb89afd047eca45b54b53c95cd32d130b54dec834e6664e3fe3786a86dcd"),
        }
        for name, contract in ASSETS.items():
            if name in revisions:
                self.assertEqual(tuple(contract[key] for key in
                                       ("version", "size", "blocks", "ground_y", "slope", "sha256")), revisions[name])
                self.assertFalse(contract["visually_accepted"])
            else:
                self.assertEqual(contract["sha256"], unchanged_hashes[name])
        candidates = json.loads((ROOT / 'docs/project/rooted-candidates-20261007.json').read_text())
        embedded = {'titan_skull_rock', 'titan_skull_2', 'world_tree'}
        self.assertEqual({a['id'] for a in candidates['structures']}, embedded)
        for record in candidates['structures']:
            if record['id'] == 'titan_skull_rock':
                self.assertEqual(ASSETS[record['id']], {k: v for k, v in record.items() if k != 'id'})
        cave = json.loads((ROOT / 'docs/project/cave-candidates-20261007.json').read_text())
        self.assertEqual({a['id'] for a in cave['structures']}, {'titan_skull_2', 'world_tree'})
        for record in cave['structures']:
            self.assertEqual(ASSETS[record['id']], {k: v for k, v in record.items() if k != 'id'})
        # Pinned Alpha 4.8 natural hashes; this regression also runs in fresh
        # checkouts without local JARs, smoke worlds or build artifacts.
        unchanged_natural = {
            'colossus': 'b5cd823a55ca9008b146d35aa98d1766195b3debaad56abbf7daebee212e0311',
            'obelisk': 'bf62468045e160c992297250faa00dc021c1e21672be6c6033df81f043987486',
            'titan_skull': '43f1e442cc080fcddb14b187cffb8863d299ebb74da90219d54aba8f128402b4',
            'titan_skull_dry': 'ef6fb103bdfad1a2d75ddd5509f6ff1e434f9d0b7091a236b7963250b663c626',
            'titan_skull_sand': 'a4077f3951709e090dc3f27ca4e46d8f995fac2176cac8157f16460fbd981648',
            'titan_skull_rock': '39a15f133729293e9d4819a32ccbbaa06503e4caca1b42abb862b104d4882e90',
            'small_colossus': 'd98db6baf095236669ed6069a54bd86aa274df3efbcbafd673ec969999768906',
            'ruined_tower': 'df160837cd20d1481fa420dbcdf976856aa6b937cfa2979a9ed0aea118fd1d0f',
        }
        for name, digest in unchanged_natural.items():
            current = next(a for a in self.manifest['structures'] if a['id'] == name)
            self.assertEqual(current['worldgen_template']['sha256'], digest)
        for name, contract in ASSETS.items():
            self.assertEqual(contract.get('foundation_mode') == 'embedded_art', name in embedded)
            self.assertEqual(contract.get('root_support', False), name == 'world_tree')
            self.assertEqual('max_support_depth' in contract, name in ('titan_skull_2', 'world_tree'))

    def test_preserved_ground_v2_exports_keep_their_original_art_and_supports(self):
        from build_deposit_relief import baseline_contract, NAMES
        def block_states(root):
            return {pos: state['Name'] + ('[' + ','.join(f'{k}={v}' for k, v in sorted(state['Properties'].items())) + ']'
                                         if state.get('Properties') else '') for pos, state in states(root).items()}
        for name in NAMES:
            with self.subTest(asset=name):
                source = baseline_contract(name, tower_v6=True)
                selected_path = (ROOT / source['source']).parent.parent / (source['version'] + '-ground-v2')
                report = json.loads((selected_path / 'verification.json').read_text())
                self.assertEqual(report['source'], source['source'])
                self.assertEqual(report['source_sha256'], source['sha256'])
                original_bytes = (ROOT / source['source']).read_bytes()
                self.assertEqual(hashlib.sha256(original_bytes).hexdigest(), source['sha256'])
                current = decode_nbt((selected_path / (source['version'] + '-ground-v2.nbt')).read_bytes())
                previous = decode_nbt(original_bytes)
                self.assertEqual(current['size'], previous['size'])
                self.assertEqual(current['DataVersion'], previous['DataVersion'])
                terrain = set(report['terrain_states'])
                self.assertEqual({p: s for p, s in block_states(current).items() if s not in terrain},
                                 {p: s for p, s in block_states(previous).items() if s not in terrain})
                self.assertEqual(len(previous['blocks']) - len(current['blocks']), report['removed_soil_cells'])
                old_natural, _, foundation = supported_blocks(block_states(previous), source)
                present, _, _ = supported_blocks(block_states(current), source)
                pad, horizontal = foundation['vertical_padding'], foundation['horizontal_padding']
                checked = 0
                for (x, y, z), state in block_states(previous).items():
                    below = (x + horizontal, y - 1 + pad, z + horizontal)
                    if state not in terrain and below in old_natural:
                        checked += 1
                        self.assertIn(below, present, f'New air under previously supported art at {(x, y, z)}')
                self.assertEqual(checked, report['supported_art_cells_checked'])
                self.assertGreater(checked, 0)

    def test_deposit_builder_keeps_its_preserved_inputs_after_current_selection_changes(self):
        from build_deposit_relief import baseline_contract, BASELINE_GEOMETRY, NAMES
        for name in NAMES:
            baseline = baseline_contract(name)
            self.assertFalse(baseline['version'].endswith('-ground-v2'))
            self.assertNotEqual(baseline['source'], ASSETS[name]['source'])
            self.assertEqual(hashlib.sha256((ROOT / baseline['source']).read_bytes()).hexdigest(), baseline['sha256'])
            self.assertEqual((baseline['size'], baseline['ground_y'], baseline['slope']), BASELINE_GEOMETRY[name])
            self.assertNotIn('foundation_mode', baseline)
            self.assertNotIn('root_support', baseline)
            self.assertNotIn('uphill_slope', baseline)
            for key in ('buried_clip_depth', 'max_support_depth', 'surface_contact_depth', 'follow_art'):
                self.assertNotIn(key, baseline)
        self.assertEqual(baseline_contract('ruined_tower')['version'], 'ruined-tower-v5')
        self.assertEqual(baseline_contract('ruined_tower', True)['version'], 'ruined-tower-v6')

    def test_historical_ground_v3_preserves_art_and_low_supports_not_high_pedestals(self):
        from build_embedding_relief import baseline, BASELINES
        from embedding_relief import sculpt
        from inspect_ots_result import read_structure
        from terrain_foundations import TOE_RADIUS, padding
        historical = {a['id']: {k: v for k, v in a.items() if k != 'id'} for a in
                      json.loads((ROOT / 'docs/project/embedding-candidates-20261006.json').read_text())['structures']}
        total_checked = 0
        for name in BASELINES:
            with self.subTest(asset=name):
                selected = historical[name]
                source, old_ground, ground, slope, digest = baseline(name)
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), digest)
                self.assertEqual(selected['ground_y'], ground)
                self.assertEqual(selected['slope'], slope)
                self.assertNotEqual(selected['source'], source.relative_to(ROOT).as_posix())
                config = json.loads((source.parents[2] / (source.stem + '.json')).read_text())
                root, original = read_structure(source)
                _, art, _ = sculpt(original, ground, config['materials'], moss_pads=name == 'world_tree')
                current_root, current = read_structure(ROOT / selected['source'])
                report = json.loads((ROOT / selected['source']).with_name('verification.json').read_text())
                self.assertEqual(report['source_sha256'], digest)
                self.assertEqual(report['source'], source.relative_to(ROOT).as_posix())
                original_contract = {k: v for k, v in selected.items() if k != 'uphill_slope'}
                self.assertEqual(report['placement_contract'], {**original_contract, 'slope': slope})
                self.assertEqual(current_root['size'], root['size'])
                self.assertEqual(current_root['DataVersion'], root['DataVersion'])
                self.assertEqual({p: s for p, s in current.items() if p in art}, art)
                self.assertLessEqual(max(p[1] - ground for p in current if p not in art), 1)
                old_contract = {'size': root['size'], 'ground_y': old_ground,
                                'slope': 10 if name == 'ruined_tower' else 12}
                old_natural, _, _ = supported_blocks(original, old_contract)
                natural, _, _ = supported_blocks(current, selected)
                checked = 0
                for x, y, z in art:
                    if not 0 < y <= ground + 2:
                        continue
                    old_below = x + TOE_RADIUS, y - 1 + padding(old_contract), z + TOE_RADIUS
                    if old_below in old_natural:
                        checked += 1
                        self.assertIn((x + TOE_RADIUS, y - 1 + padding(selected), z + TOE_RADIUS), natural)
                self.assertEqual(checked, report['low_art_undersides_checked'])
                self.assertEqual(sum(y == 0 for x, y, z in art),
                                 report['buried_boundary_undersides_requiring_runtime_check'])
                total_checked += checked
        self.assertEqual(total_checked, 101038)

    def test_historical_candidate_index_preserves_art_and_original_site_tolerance(self):
        index = json.loads((ROOT / 'docs/project/embedding-candidates-20261006.json').read_text())
        self.assertEqual(len(index['structures']), 8)
        for record in index['structures']:
            selected = ASSETS[record['id']]
            old_slope = (6 if record['id'] == 'titan_skull_rock' else 4) if selected['family'] == 'titan_skull' else selected['slope']
            historical = {k: v for k, v in record.items() if k != 'id'}
            self.assertEqual(record['slope'], old_slope)
            source = ROOT / record['source']
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), record['sha256'])
            provenance = json.loads(source.with_name('verification.json').read_text())
            if 'placement_contract' in provenance:
                self.assertEqual(provenance['placement_contract'], historical)
            if not selected.get('foundation_mode'):
                original_contract = {k: v for k, v in selected.items() if k != 'uphill_slope'}
                self.assertEqual(historical, {**original_contract, 'slope': old_slope})
            self.assertEqual(selected.get('uphill_slope'), {'titan_skull_rock': 18, 'small_colossus': 12}.get(record['id']))

    def test_rooted_tree_keeps_accepted_art_and_adds_only_connected_low_wood(self):
        contract = ASSETS["world_tree"]
        current = decode_nbt((ROOT / contract["source"]).read_bytes())
        previous = decode_nbt((ROOT / "relics/world-tree/design/generated/world-tree-v4/world-tree-v4.nbt").read_bytes())
        provenance = json.loads((ROOT / contract['source']).with_name('verification.json').read_text())
        self.assertEqual(provenance['source_translation'], [0, 12, 0])
        self.assertEqual(current["size"], [previous['size'][0], previous['size'][1] + 12, previous['size'][2]])
        terrain = {"minecraft:grass_block", "minecraft:rooted_dirt", "minecraft:dirt"}
        original_art = {(x, y + 12, z): state for (x, y, z), state in states(previous).items()
                        if state['Name'] not in terrain
                        and not (state['Name'] == 'minecraft:moss_block' and y <= 13)}
        present = states(current)
        self.assertTrue(original_art.items() <= present.items())
        additions = set(present) - set(original_art)
        self.assertEqual(len(additions), 1883)
        self.assertEqual(provenance['new_wood_cells'], len(additions))
        self.assertEqual(provenance['new_wood_face_connected'], len(additions))
        self.assertEqual(len(provenance['strands']), 50)
        self.assertTrue(all(present[p]['Name'] == 'minecraft:spruce_log' and p[1] <= 22 for p in additions))
        for name in ('minecraft:oak_log', 'minecraft:spruce_log', 'minecraft:oak_leaves', 'minecraft:spruce_leaves'):
            expected = {(x, y + 12, z): state for (x, y, z), state in states(previous).items() if state['Name'] == name}
            self.assertTrue(expected.items() <= present.items())
            self.assertEqual({p: s for p, s in present.items() if s['Name'] == name and p not in additions}, expected)

    def test_current_build_and_runtime_use_the_updated_dependency_pins(self):
        from setup_worldgen_build import FABRIC_API_SHA256, LITHOSTITCHED_SHA256
        from smoke_server import BASE_MODS
        self.assertEqual(BASE_MODS, ["fabric-api-0.161.0+26.2.jar", "lithostitched-1.8.0-fabric-26.2.jar"])
        self.assertEqual(FABRIC_API_SHA256, "e5b858ceb13290c274e31cb888ff5a1a40cb91067e7ffab0b5b775aec51e216a")
        self.assertEqual(LITHOSTITCHED_SHA256, "4d74a8ec2023657352ae051f1a6270bff474bf3cc46013100eff5f9ddbbdd024")

    def test_natural_template_restores_model_and_adds_only_soil_support(self):
        for a in self.manifest["structures"]:
            raw = decode_nbt((self.output / a["single_template"]["path"]).read_bytes())
            natural = decode_nbt((self.output / a["worldgen_template"]["path"]).read_bytes())
            restored = states(natural)
            anchor = tuple(a["worldgen_template"]["anchor"])
            markers = [b for b in natural["blocks"] if "nbt" in b]
            self.assertEqual(len(markers), 1)
            self.assertEqual(markers[0]["nbt"]["name"], "relics:center")
            final_state = markers[0]["nbt"]["final_state"]
            self.assertEqual(natural["DataVersion"], raw["DataVersion"])
            if final_state == "minecraft:structure_void":
                del restored[anchor]
            else:
                restored[anchor] = {'Name': final_state}
            raw_states = {p: s['Name'] + ('[' + ','.join(f'{k}={v}' for k, v in sorted(s['Properties'].items())) + ']'
                                        if s.get('Properties') else '') for p, s in states(raw).items()}
            expected, size, report = supported_blocks(raw_states, a)
            actual = {p: s['Name'] + ('[' + ','.join(f'{k}={v}' for k, v in sorted(s['Properties'].items())) + ']'
                                     if s.get('Properties') else '') for p, s in restored.items()}
            self.assertEqual(actual, expected)
            self.assertEqual(natural['size'], size)
            self.assertEqual(a['worldgen_template']['foundation'], report)

    def test_burial_grid_ceiling_and_eight_chunk_radius_for_every_rotation(self):
        resources = worldgen_resources()
        for name, a in ASSETS.items():
            data = resources[f"worldgen/structure/{name}.json"]
            self.assertEqual(data["delegate"]["start_height"]["absolute"], 1 - natural_ground(a))
            self.assertEqual(data["delegate"]["step"], "top_layer_modification")
            terrain = data["spawn_condition"]["terrain_condition"]
            self.assertEqual(terrain["offset"], [0, 0, 0])
            exported = next(s for s in self.manifest['structures'] if s['id'] == name)
            anchor_y = exported['worldgen_template']['anchor'][1]
            self.assertEqual(anchor_y, natural_ground(a) - 1)
            # Vanilla Jigsaw: piece base=surface+start_height-1;
            # biome-query stub=surface+start_height+anchor_y.
            for surface in (63, 80, 120):
                self.assertEqual(surface + data['delegate']['start_height']['absolute'] - 1 + natural_ground(a), surface)
                self.assertEqual(surface + data['delegate']['start_height']['absolute'] + anchor_y, surface)
            grid = terrain["condition"]
            sx, sy, sz = natural_size(a)
            self.assertGreaterEqual(grid["radius"], (max(sx, sz) - 1) / 2)
            self.assertEqual(grid["allowed_count"], (2 * grid["radius"] // grid["distance_between_points"] + 1) ** 2)
            height_range = grid['condition']['conditions'][0]['permitted_range']
            self.assertEqual(height_range, {'min_inclusive': -a.get('uphill_slope', a['slope']), 'max_inclusive': a['slope']})
            ceiling = grid["condition"]["conditions"][1]["permitted_range"]["max_inclusive"]
            self.assertLessEqual(ceiling - natural_ground(a) + sy - 1, 311)
            for rotation in ("NONE", "CLOCKWISE_90", "CLOCKWISE_180", "COUNTERCLOCKWISE_90"):
                anchor = rotate((sx // 2, 0, sz // 2), rotation)
                for x in (0, sx - 1):
                    for z in (0, sz - 1):
                        corner = rotate((x, 0, z), rotation)
                        for axis in (0, 2):
                            # Start may land at any offset within its chunk.
                            for offset in range(16):
                                self.assertLessEqual(abs((corner[axis] - anchor[axis] + offset) // 16), 8)

    def test_skull_variants_have_disjoint_biomes_and_one_shared_structure_set(self):
        resources = worldgen_resources()
        seen = set()
        for name in members("titan_skull"):
            biomes = {v if isinstance(v, str) else v["id"] for v in ASSETS[name]["biomes"]}
            self.assertFalse(seen & biomes)
            seen.update(biomes)
            conditions = resources[f"worldgen/structure/{name}.json"]["spawn_condition"]["terrain_condition"]["condition"]["condition"]["conditions"]
            biome_condition = {"type": "lithostitched:in_biome", "biomes": f"#relics:has_structure/{name}"}
            if name == "titan_skull_rock":
                self.assertNotIn(biome_condition, conditions)
                self.assertEqual(resources[f"worldgen/structure/{name}.json"]["delegate"]["biomes"],
                                 f"#relics:has_structure/{name}")
            else:
                self.assertIn(biome_condition, conditions)
        entries = resources["worldgen/structure_set/titan_skull.json"]["structures"]
        self.assertEqual({e["structure"] for e in entries}, {"relics:" + n for n in members("titan_skull")})

    def test_stale_or_modified_assets_are_not_packaged_with_skip_generation(self):
        # Copy resource text and the already generated templates into an isolated
        # resource root; neither the model sources nor checkout assets are edited.
        import shutil
        with tempfile.TemporaryDirectory() as td:
            resources = Path(td)
            for filename in ("fabric.mod.json", "pack.mcmeta"):
                shutil.copyfile(ROOT / "src/main/resources" / filename, resources / filename)
            integrate(resources)
            check_resources(resources)
            manifest_path = resources / 'relics.integration.json'
            original = manifest_path.read_text()
            stale = json.loads(original)
            stale.pop('runtime_contact_policy')
            manifest_path.write_text(json.dumps(stale))
            with self.assertRaisesRegex(ValueError, 'Stale runtime contact policy'):
                check_resources(resources)
            stale = json.loads(original)
            stale['structures'][0]['worldgen_template']['anchor'][1] = 0
            manifest_path.write_text(json.dumps(stale))
            with self.assertRaisesRegex(ValueError, 'Stale surface anchor'):
                check_resources(resources)
            manifest_path.write_text(original)
            template = resources / "data/relics/structure/colossus.nbt"
            template.write_bytes(b"stale model")
            with self.assertRaisesRegex(ValueError, "stale template"):
                check_resources(resources)

    def test_persistent_leaves_allow_only_the_computed_distance_to_change(self):
        expected = {"Name": "minecraft:spruce_leaves", "Properties": {"distance": "7", "persistent": "true"}}
        for distance in range(1, 8):
            actual = {"Name": expected["Name"], "Properties": {"distance": str(distance), "persistent": "true"}}
            self.assertTrue(states_match(expected, actual, "NONE"))
        for props in ({"distance": "1", "persistent": "false"}, {"persistent": "true"},
                      {"distance": "0", "persistent": "true"}, {"distance": "8", "persistent": "true"}):
            self.assertFalse(states_match(expected, {"Name": expected["Name"], "Properties": props}, "NONE"))
        self.assertFalse(states_match(expected, {"Name": "minecraft:oak_leaves", "Properties": expected["Properties"]}, "NONE"))

    def test_terrain_preview_excludes_only_recorded_manual_regions(self):
        report = {"asset_selection": {"structures": [{"id": "test", "size": [33, 20, 33]}]},
                  "manual_placements": [{"structure": "relics:test", "requested_position": [-16, 50, 500]}]}
        self.assertEqual(placement_regions(report), {"r.-1.0.mca", "r.0.0.mca", "r.-1.1.mca", "r.0.1.mca"})

    def test_terrain_view_supports_every_natural_rotation(self):
        for rotation, expected in {"NONE": (10, -48, 0), "CLOCKWISE_90": (68, 15, 90),
                                   "CLOCKWISE_180": (10, 78, 180), "COUNTERCLOCKWISE_90": (-48, 15, -90)}.items():
            self.assertEqual(front_view({"bounding_box": [0, 0, 0, 20, 40, 30], "rotation": rotation}), expected)


if __name__ == "__main__":
    unittest.main()
