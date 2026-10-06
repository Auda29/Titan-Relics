"""Pinned Alpha 4.6 visual assets and provisional placement contracts.

Candidate selection is for in-game review, not a new artistic approval. No model
is regenerated here. Families group biome variants for density/disable settings.
"""
from pathlib import Path
from terrain_foundations import natural_ground, natural_size

ROOT = Path(__file__).resolve().parents[1]


def optional(name):
    return {"id": name, "required": False}


MEADOW = ["minecraft:plains", "minecraft:sunflower_plains", "minecraft:meadow",
          optional("terralith:blooming_valley"), optional("terralith:blooming_plateau"),
          optional("biomesoplenty:prairie")]
DRY = ["minecraft:savanna", optional("terralith:steppe"), optional("biomesoplenty:scrubland")]
SAND = ["minecraft:desert", optional("terralith:desert_spires"), optional("terralith:desert_canyon"),
        optional("biomesoplenty:dryland")]
ROCK = ["minecraft:windswept_hills", "minecraft:windswept_gravelly_hills",
        "minecraft:stony_shore", "minecraft:stony_peaks",
        optional("terralith:rocky_mountains")]


def asset(folder, stem, size, blocks, ground_y, family, biomes, slope, sha256, accepted=True):
    return {"source": f"relics/{folder}/design/generated/{stem}/{stem}.nbt",
            "version": stem, "size": size, "blocks": blocks, "ground_y": ground_y,
            "family": family, "biomes": biomes, "slope": slope,
            "sha256": sha256, "visually_accepted": accepted}


ASSETS = {
    "colossus": asset("colossus", "colossus-v4-1-materials-b", [181, 209, 235], 223161, 77,
                      "colossus", MEADOW + DRY, 16,
                      "a355b20349513cb27e6feb6fc171ca413d71da2cdb5717f7995afb4128d879b8"),
    "obelisk": asset("obelisk", "obelisk-v4-2", [59, 185, 60], 94422, 8,
                     "obelisk", SAND + ["minecraft:badlands", optional("terralith:gravel_desert"),
                                        optional("biomesoplenty:wasteland")], 6,
                     "ed116dcbca2a41fe403695a816e419a32a647d325c1d907d8dc1797f551cda3e"),
    "titan_skull": asset("titan-skull", "titan-skull-v4-meadow-ground-v3", [117, 79, 179], 111328, 16,
                         "titan_skull", MEADOW, 4,
                         "b189932ac224097ba030a649ea2b44c898aaa4fdfbddb42b8797c32851ae5969", False),
    "titan_skull_dry": asset("titan-skull", "titan-skull-v4-dry-ground-v3", [117, 79, 179], 111328, 16,
                             "titan_skull", DRY, 4,
                             "0d948527040a395b55615dce8704d72a2d5528b44c0b0c69ff94ea06b465eb67", False),
    "titan_skull_sand": asset("titan-skull", "titan-skull-v4-sand-ground-v3", [117, 79, 179], 111328, 16,
                              "titan_skull", SAND, 4,
                              "7106438dd1a0389dc5953f48351fa8a4aebfa1af3becd671d16288ab847bd0aa", False),
    "titan_skull_rock": asset("titan-skull", "titan-skull-v4-rock-ground-v3", [117, 79, 179], 111288, 16,
                              "titan_skull", ROCK, 6,
                              "6303836dd1d816900a84897ad31cd4a74e659820612d61c677612e267b47051f", False),
    "small_colossus": asset("colossus", "small-colossus-v7-ground-v3", [111, 80, 113], 233448, 13,
                             "small_colossus", MEADOW + DRY, 4,
                             "a64a22e00ae9d3499df0d0110273caa1db5e0075168fbbf9eb0c6978f2484021", False),
    "world_tree": asset("world-tree", "world-tree-v4-1-ground-v3", [187, 216, 185], 291903, 8,
                         "world_tree", MEADOW + ["minecraft:forest", "minecraft:flower_forest",
                                              "minecraft:birch_forest", "minecraft:old_growth_birch_forest"], 6,
                        "fee50813242408123f4adcd1a0bacb476799359fce8e80ba5d59a49085823163", False),
    "ruined_tower": asset("ruined-tower", "ruined-tower-v7-ground-v3", [111, 232, 93], 272528, 12,
                          "ruined_tower", MEADOW + DRY + SAND, 6,
                          "faf9644ce0772f8b289c5c892016cdecbd94c65a45f3bde98fdca58c2adcc600", False),
    "titan_skull_2": asset("titan-skull", "titan-skull-2-v2", [99, 136, 99], 46922, 22,
                          "titan_skull_2", MEADOW + DRY, 4,
                          "955703762402efc16d9d05a957a78368553ed019c35aec4aa659ee3754f3522b", False),
}
FAMILIES = tuple(dict.fromkeys(a["family"] for a in ASSETS.values()))
NORMAL_DENSITY = {"obelisk": (64, 32), "colossus": (80, 40), "titan_skull": (48, 24),
                  "small_colossus": (48, 24), "world_tree": (96, 48),
                  "ruined_tower": (80, 40), "titan_skull_2": (64, 32)}
SALTS = {"obelisk": 206091301, "colossus": 206091302, "titan_skull": 206091303,
         "small_colossus": 206091304, "world_tree": 206091305,
         "ruined_tower": 206091306, "titan_skull_2": 206091307}


def members(family):
    return tuple(name for name, contract in ASSETS.items() if contract["family"] == family)


def footprint_grid(contract):
    # Five-by-five samples include the padded footprint edge in
    # either horizontal rotation. Center anchors keep every corner within 8 chunks.
    size = natural_size(contract)
    radius = ((max(size[0], size[2]) + 2) // 4) * 2
    return radius, radius // 2


def reservations(family):
    """One-way priority prevents cycles; reserve even unsuitable earlier candidates.

    All family placements remain configurable vanilla random_spread sets. A
    disabled set releases its space; new spacing is read from the world's registry.
    """
    radii = {f: max((max(natural_size(ASSETS[n])[0::2]) + 1) // 2 for n in members(f))
             for f in FAMILIES}
    result = [{"set": f"relics:{other}",
             "clearance_chunks": (radii[family] + radii[other] + 31) // 16}
            for other in FAMILIES[:FAMILIES.index(family)]]
    result.append({"set": f"relics:{family}", "clearance_chunks": (2 * radii[family] + 31) // 16,
                   "earlier_only": True})
    return result


def worldgen_resources():
    """Canonical derived resources; conservative, provisional vanilla placement."""
    resources = {}
    for name, a in ASSETS.items():
        radius, distance = footprint_grid(a)
        ground = natural_ground(a)
        # Leave at least eight blocks below the Overworld ceiling (319).
        ceiling = min(230, 311 - (a["size"][1] - a["ground_y"] - 1))
        conditions = [
            {"type": "lithostitched:height_filter", "heightmap": "WORLD_SURFACE_WG",
             "permitted_range": {"min_inclusive": -a["slope"], "max_inclusive": a["slope"]},
             "range_type": "heightmap_relative"},
            {"type": "lithostitched:height_filter", "heightmap": "OCEAN_FLOOR_WG",
              "permitted_range": {"min_inclusive": 63, "max_inclusive": ceiling}, "range_type": "absolute"},
            {"type": "relics:dry_land"},
            {"type": "lithostitched:not", "condition": {"type": "lithostitched:any_of", "conditions": [
                {"type": "lithostitched:in_biome", "biomes": "#minecraft:is_ocean"},
                {"type": "lithostitched:in_biome", "biomes": "#minecraft:is_river"}]}},
        ]
        # Earth/sand palettes must match across the sampled site, not just at the
        # anchor. Mineral deposits may cross a rocky-biome edge; otherwise the
        # 180-block pure-rock requirement rejects nearly every vanilla rocky site.
        # The delegate's center biome and all-site land/slope/height checks still
        # apply to the rock variant, without painting grass across a desert edge.
        if a["family"] == "titan_skull" and name != "titan_skull_rock":
            conditions.append({"type": "lithostitched:in_biome", "biomes": f"#relics:has_structure/{name}"})
        resources[f"worldgen/structure/{name}.json"] = {
            "type": "lithostitched:delegating", "delegate": {
                "type": "minecraft:jigsaw", "biomes": f"#relics:has_structure/{name}",
                "step": "top_layer_modification", "spawn_overrides": {}, "terrain_adaptation": "none",
                "start_pool": f"relics:{name}", "start_jigsaw_name": "relics:center", "size": 1,
                "start_height": {"absolute": 1 - ground},
                "project_start_to_heightmap": "WORLD_SURFACE_WG", "max_distance_from_center": 128,
                "use_expansion_hack": False, "dimension_padding": 8, "liquid_settings": "ignore_waterlogging"},
            "spawn_condition": {"type": "relics:separated", "reservations": reservations(a["family"]),
                "terrain_condition": {"type": "lithostitched:offset", "offset": [0, ground - 1, 0],
                "condition": {"type": "relics:all_grid", "radius": radius,
                    "distance_between_points": distance, "allowed_count": 25,
                    "condition": {"type": "lithostitched:all_of", "conditions": conditions}}}}}
        resources[f"worldgen/template_pool/{name}.json"] = {
            "name": f"relics:{name}", "fallback": "minecraft:empty", "elements": [{"weight": 1, "element": {
                "element_type": "minecraft:single_pool_element", "location": f"relics:{name}_worldgen",
                "processors": f"relics:{name}_terrain", "projection": "rigid"}}]}
        resources[f"worldgen/processor_list/{name}_terrain.json"] = {
            "processors": [{"processor_type": "relics:terrain_support", "ground_y": ground}]}
        resources[f"tags/worldgen/biome/has_structure/{name}.json"] = {"replace": False, "values": a["biomes"]}
    for family in FAMILIES:
        spacing, separation = NORMAL_DENSITY[family]
        resources[f"worldgen/structure_set/{family}.json"] = {
            "structures": [{"structure": f"relics:{name}", "weight": 1} for name in members(family)],
            "placement": {"type": "minecraft:random_spread", "spacing": spacing,
                          "separation": separation, "salt": SALTS[family]}}
        resources[f"tags/worldgen/structure/{family}.json"] = {
            "replace": False, "values": [f"relics:{name}" for name in members(family)]}
    resources["tags/worldgen/structure/relics.json"] = {"replace": False, "values": [f"relics:{name}" for name in ASSETS]}
    return resources
