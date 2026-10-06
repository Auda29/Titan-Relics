"""Pinned Alpha 4.5 visual assets and provisional placement contracts.

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
    "titan_skull": asset("titan-skull", "titan-skull-v4-meadow-ground-v2", [117, 79, 179], 123861, 8,
                         "titan_skull", MEADOW, 12,
                         "fcfef99961773832f54b24ff585d5e96a64bf9e3ed2ac7b0888158e8804c7f6b", False),
    "titan_skull_dry": asset("titan-skull", "titan-skull-v4-dry-ground-v2", [117, 79, 179], 123861, 8,
                             "titan_skull", DRY, 12,
                             "3cd8249a3401c39f162bf62217d68ad00fcd385a507aeb9d794e54e3351fdc20", False),
    "titan_skull_sand": asset("titan-skull", "titan-skull-v4-sand-ground-v2", [117, 79, 179], 123861, 8,
                              "titan_skull", SAND, 12,
                              "358bd8f318ef5ad0ea1c6b27292fb5b30f94ebb0afa937bf778f16d9ff47a829", False),
    "titan_skull_rock": asset("titan-skull", "titan-skull-v4-rock-ground-v2", [117, 79, 179], 123861, 8,
                              "titan_skull", ROCK, 12,
                              "fd6ce1c124b0d5ac51777644e0b7214f053a32bf8460b1e30b9e3fe1f0aaeacf", False),
    "small_colossus": asset("colossus", "small-colossus-v7-ground-v2", [111, 80, 113], 233492, 9,
                             "small_colossus", MEADOW + DRY, 12,
                             "5a1afb7dc0b8cb30bba6428cc612aa26dcfe6f63d4cfca7a5aaca41edb5a5843", False),
    "world_tree": asset("world-tree", "world-tree-v4-1-ground-v2", [187, 216, 185], 292646, 8,
                        "world_tree", MEADOW + ["minecraft:forest", "minecraft:flower_forest",
                                              "minecraft:birch_forest", "minecraft:old_growth_birch_forest"], 12,
                        "5ba0b4f73f0e1fd5087f2ecdb28849a78f3297caffbbb2d6b5b58b98ce2ebaf6", False),
    "ruined_tower": asset("ruined-tower", "ruined-tower-v6-ground-v2", [111, 232, 93], 297352, 12,
                          "ruined_tower", MEADOW + DRY + SAND, 10,
                          "88a7f0d218b1f5343cbbf3ebef1bd46e70df060d866cf36d3473107a03dbe4bd", False),
    "titan_skull_2": asset("titan-skull", "titan-skull-2-v1-ground-v2", [105, 144, 107], 85152, 12,
                          "titan_skull_2", MEADOW + DRY, 12,
                          "1d4b8da9d888355da29d7d3caa1b419f00d1ef3ed051fa018ac0ad0efa5565b6", False),
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
