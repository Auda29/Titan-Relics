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

    def test_alpha44_selects_latest_art_without_changing_the_other_seven_exports(self):
        unchanged_hashes = {
            "colossus": "a355b20349513cb27e6feb6fc171ca413d71da2cdb5717f7995afb4128d879b8",
            "obelisk": "ed116dcbca2a41fe403695a816e419a32a647d325c1d907d8dc1797f551cda3e",
            "titan_skull": "c4737780cc344b2a3f10743a7155a760df7342f22476308679a9a87545f59e79",
            "titan_skull_dry": "7c2ea0fde39ba7c9618001dd49e747d2c652e0646c854baf0fadcb6e5ed773a4",
            "titan_skull_sand": "05ba0c95f74e98eca366c11f4ebe1ceb1b3ce435b82c29d7101f65fd7da7d03e",
            "titan_skull_rock": "9c41e8bdc5333737ed7c37e6ab8f916aac0f77f32764d20cca4e2fb68e94620b",
            "titan_skull_2": "5a39ac6ef62c1d07eafed69ed8a7cbeb397b4a6d3c4a6f7bf7086fdabdac1b78",
        }
        revisions = {
            "small_colossus": ("small-colossus-v7", [111, 80, 113], 235933, 9,
                               "c48bb70ea3643070e94a44008721cb5c08fda74f80b4efee2e063a44b5436bb4"),
            "world_tree": ("world-tree-v4-1", [187, 216, 185], 293691, 8,
                           "b8235fd957029d39a534eef2f13924bc850155e46fd5872fc40f51ecce8eea37"),
            "ruined_tower": ("ruined-tower-v5", [111, 232, 93], 307417, 12,
                             "5be62afb4d6a3968e37c61b54e21941273c795921441dc9db8e705ced9f2765f"),
        }
        for name, contract in ASSETS.items():
            if name in revisions:
                self.assertEqual(tuple(contract[key] for key in
                                       ("version", "size", "blocks", "ground_y", "sha256")), revisions[name])
                self.assertFalse(contract["visually_accepted"])
            else:
                self.assertEqual(contract["sha256"], unchanged_hashes[name])

    def test_tree_ground_revision_keeps_every_accepted_non_terrain_cell(self):
        contract = ASSETS["world_tree"]
        current = decode_nbt((ROOT / contract["source"]).read_bytes())
        previous = decode_nbt((ROOT / "relics/world-tree/design/generated/world-tree-v4/world-tree-v4.nbt").read_bytes())
        self.assertEqual(current["size"], previous["size"])
        terrain = {"minecraft:grass_block", "minecraft:rooted_dirt", "minecraft:dirt"}
        def art(root):
            return {pos: state for pos, state in states(root).items() if state["Name"] not in terrain}
        self.assertEqual(art(current), art(previous))
        self.assertGreater(len(current["blocks"]), len(previous["blocks"]))

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
            self.assertEqual(terrain["offset"], [0, natural_ground(a) - 1, 0])
            grid = terrain["condition"]
            sx, sy, sz = natural_size(a)
            self.assertGreaterEqual(grid["radius"], (max(sx, sz) - 1) / 2)
            self.assertEqual(grid["allowed_count"], (2 * grid["radius"] // grid["distance_between_points"] + 1) ** 2)
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
