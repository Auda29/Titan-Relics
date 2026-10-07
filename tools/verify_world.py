#!/usr/bin/env python3
"""Compare naturally generated saved structures with the NBT shipped in an artifact.

Read-only. Includes every fixed block and authored air cell across chunk boundaries.
Natural soil/vegetation is counted separately because world features can change it.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import gzip
import hashlib
import json
from pathlib import Path
import zipfile
import zlib

from smoke_server import read_nbt

AIR_NAMES = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air"}
NATURE_NAMES = {"minecraft:grass_block", "minecraft:dirt", "minecraft:azalea_leaves"}


def palette_index(data: list[int], palette_size: int, index: int) -> int:
    """Decode modern padded block storage. Entries never span two longs."""
    if not 0 <= index < 4096:
        raise ValueError("Section block index must be 0..4095")
    if palette_size < 1:
        raise ValueError("Empty block palette")
    if palette_size == 1:
        return 0
    bits = max(4, (palette_size - 1).bit_length())
    per_long = 64 // bits
    word = data[index // per_long] & ((1 << 64) - 1)
    result = (word >> ((index % per_long) * bits)) & ((1 << bits) - 1)
    if result >= palette_size:
        raise ValueError("Block state palette index out of range")
    return result


class AnvilWorld:
    def __init__(self, world: Path):
        self.world = Path(world)
        modern = self.world / "dimensions/minecraft/overworld/region"
        self.region_directory = modern if modern.is_dir() else self.world / "region"
        self.read_errors = []

    @lru_cache(maxsize=8)
    def region(self, rx: int, rz: int) -> bytes | None:
        path = self.region_directory / f"r.{rx}.{rz}.mca"
        return path.read_bytes() if path.is_file() else None

    @lru_cache(maxsize=256)
    def chunk(self, cx: int, cz: int) -> dict | None:
        data = self.region(cx // 32, cz // 32)
        if data is None:
            return None
        slot = (cx % 32) + (cz % 32) * 32
        offset = int.from_bytes(data[slot * 4:slot * 4 + 3], "big") * 4096
        if not offset:
            return None
        length = int.from_bytes(data[offset:offset + 4], "big")
        compression = data[offset + 4]
        if compression & 128:
            payload = (self.region_directory / f"c.{cx}.{cz}.mcc").read_bytes()
            compression &= 127
        else:
            payload = data[offset + 5:offset + 4 + length]
        if compression == 1:
            payload = gzip.decompress(payload)
        elif compression == 2:
            payload = zlib.decompress(payload)
        elif compression != 3:
            raise ValueError(f"Unsupported Anvil compression {compression}")
        return read_nbt(payload)

    def chunks(self):
        for path in sorted(self.region_directory.glob("r.*.*.mca")):
            _, rx, rz, _ = path.name.split(".")
            rx, rz = int(rx), int(rz)
            data = self.region(rx, rz)
            for slot in range(1024):
                if not int.from_bytes(data[slot * 4:slot * 4 + 3], "big"):
                    continue
                cx, cz = rx * 32 + slot % 32, rz * 32 + slot // 32
                try:
                    chunk = self.chunk(cx, cz)
                    if chunk is not None:
                        yield chunk
                except Exception as exc:
                    self.read_errors.append({"chunk": [cx, cz], "error": str(exc)})

    @lru_cache(maxsize=2048)
    def section(self, cx, cy, cz):
        chunk = self.chunk(cx, cz)
        if chunk is None:
            return None
        for section in chunk.get("sections", []):
            if section["Y"] == cy:
                return section.get("block_states", {"palette": [{"Name": "minecraft:air"}]})
        return {"palette": [{"Name": "minecraft:air"}]}

    def block(self, x: int, y: int, z: int) -> dict | None:
        section = self.section(x // 16, y // 16, z // 16)
        if section is None:
            return None
        palette = section["palette"]
        index = (y % 16) * 256 + (z % 16) * 16 + x % 16
        return palette[palette_index(section.get("data", []), len(palette), index)]


def rotate(pos, rotation):
    x, y, z = pos
    rotation = rotation.upper()
    if rotation == "NONE":
        return x, y, z
    if rotation == "CLOCKWISE_90":
        return -z, y, x
    if rotation == "CLOCKWISE_180":
        return -x, y, -z
    if rotation == "COUNTERCLOCKWISE_90":
        return z, y, -x
    raise ValueError(f"Unsupported piece rotation {rotation}")


def transform(pos, rotation, origin):
    return tuple(v + o for v, o in zip(rotate(pos, rotation), origin))


def rotate_properties(properties, rotation):
    result = dict(properties)
    turns = {"NONE": 0, "CLOCKWISE_90": 1, "CLOCKWISE_180": 2, "COUNTERCLOCKWISE_90": 3}[rotation.upper()]
    if turns % 2 and result.get("axis") in ("x", "z"):
        result["axis"] = "z" if result["axis"] == "x" else "x"
    directions = ["north", "east", "south", "west"]
    if result.get("facing") in directions:
        result["facing"] = directions[(directions.index(result["facing"]) + turns) % 4]
    return result


def states_match(expected, actual, rotation):
    if expected["Name"] in AIR_NAMES:
        return actual["Name"] in AIR_NAMES
    if expected["Name"] != actual["Name"]:
        return False
    props = rotate_properties(expected.get("Properties", {}), rotation)
    # Persistent leaves never decay, but distance-to-log is still recalculated
    # by scheduled neighbour updates even with random ticks disabled. Validate
    # the dynamic value's range, not the export's initial distance=7 sentinel.
    if (expected["Name"].endswith("_leaves") and props.get("persistent") == "true"
            and "distance" in props):
        if actual.get("Properties", {}).get("distance") not in {str(v) for v in range(1, 8)}:
            return False
        del props["distance"]
    return all(actual.get("Properties", {}).get(key) == value for key, value in props.items())


def protected_cell(chunk, pos):
    """Read the exact saved attachment bits, including negative section coordinates."""
    x, y, z = pos
    mask = chunk.get("fabric:attachments", {}).get("relics:placed_cells", {}).get(str(y // 16))
    if mask is None:
        return False
    if len(mask) != 64:
        raise ValueError("Invalid saved relic protection mask")
    index = (y % 16) * 256 + (z % 16) * 16 + x % 16
    return bool((mask[index // 64] & ((1 << 64) - 1)) & (1 << (index % 64)))


def verify_piece(world, name, child, template, max_examples=20, skip_nature=True):
    rotation = child["rotation"]
    origin = [child["PosX"], child["PosY"], child["PosZ"]]
    chunks, missing, incomplete = set(), set(), set()
    mismatch_kinds, examples = Counter(), []
    matched = checked = air_checked = nature_skipped = normalized_leaf_distance = 0
    for block in template["blocks"]:
        expected = template["palette"][block["state"]]
        if skip_nature and expected["Name"] in NATURE_NAMES:
            nature_skipped += 1
            continue
        pos = transform(block["pos"], rotation, origin)
        cp = pos[0] // 16, pos[2] // 16
        chunks.add(cp)
        chunk = world.chunk(*cp)
        if chunk is None:
            missing.add(cp)
            continue
        if chunk.get("Status", "").split(":")[-1] != "full":
            incomplete.add(cp)
        actual = world.block(*pos)
        checked += 1
        air_checked += expected["Name"] in AIR_NAMES
        if states_match(expected, actual, rotation):
            matched += 1
            if (expected["Name"].endswith("_leaves") and expected.get("Properties", {}).get("persistent") == "true"
                    and expected.get("Properties", {}).get("distance") != actual.get("Properties", {}).get("distance")):
                normalized_leaf_distance += 1
        else:
            mismatch_kinds[expected["Name"] + " -> " + actual["Name"]] += 1
            if len(examples) < max_examples:
                examples.append({"local": block["pos"], "world": list(pos), "expected": expected, "actual": actual})
    corners = [transform((x, y, z), rotation, origin)
               for x in (0, template["size"][0] - 1)
               for y in (0, template["size"][1] - 1)
               for z in (0, template["size"][2] - 1)]
    expected_bb = [min(c[i] for c in corners) for i in range(3)] + [max(c[i] for c in corners) for i in range(3)]
    bounding_box_matches = child.get("BB") == expected_bb
    return {"structure": name, "template": child.get("pool_element", {}).get("location"), "origin": origin, "rotation": rotation,
            "bounding_box": child.get("BB"), "expected_bounding_box": expected_bb, "bounding_box_matches": bounding_box_matches,
             "checked_blocks": checked, "matched_blocks": matched, "checked_air": air_checked, "nature_cells_skipped": nature_skipped,
             "normalized_persistent_leaf_distance": normalized_leaf_distance,
            "mismatch_count": checked - matched, "mismatch_kinds": dict(mismatch_kinds), "mismatch_examples": examples,
            "chunks_spanned": len(chunks), "missing_chunks": sorted(map(list, missing)), "incomplete_chunks": sorted(map(list, incomplete)),
            "passed": checked > 0 and matched == checked and not missing and not incomplete and len(chunks) > 1 and bounding_box_matches}


def verify_world(world_path: Path, artifact: Path, expected_structures=None) -> dict:
    world = AnvilWorld(world_path)
    instances, errors = [], []
    starts = [(name, start, [chunk.get("xPos"), chunk.get("zPos")])
              for chunk in world.chunks()
              for name, start in chunk.get("structures", {}).get("starts", {}).items()
              if name.startswith("relics:") and start.get("id") != "INVALID"]
    with zipfile.ZipFile(artifact) as archive:
        selection = json.loads(archive.read('relics.integration.json'))
        contracts = {a['id']: a for a in selection['structures']}
        if expected_structures is None:
            expected_structures = {"relics:" + path.rsplit("/", 1)[-1].removesuffix(".json")
                                   for path in archive.namelist()
                                   if path.startswith("data/relics/worldgen/structure/") and path.endswith(".json")}
        for name, start, cp in starts:
            for child in start.get("Children", []):
                try:
                    location = child["pool_element"]["location"]
                    namespace, path = location.split(":", 1)
                    # Compare the actual padded natural template, restoring its
                    # center anchor to the final state used by jigsaw placement.
                    template = read_nbt(gzip.decompress(archive.read(f"data/{namespace}/structure/{path}.nbt")))
                    restored = []
                    for block in template['blocks']:
                        if template['palette'][block['state']]['Name'] == 'minecraft:jigsaw':
                            final = block['nbt']['final_state']
                            if final == 'minecraft:structure_void':
                                continue
                            name_part, _, properties = final.partition('[')
                            state = {'Name': name_part}
                            if properties:
                                state['Properties'] = dict(p.split('=') for p in properties.rstrip(']').split(','))
                            template['palette'].append(state)
                            block = {'pos': block['pos'], 'state': len(template['palette']) - 1}
                        restored.append(block)
                    template['blocks'] = restored
                    result = verify_piece(world, name, child, template)
                    foundation = contracts.get(name.split(':')[-1], {}).get('worldgen_template', {}).get('foundation')
                    if foundation:
                        from terrain_foundations import SOILS
                        bottom_columns = {}
                        for block in template['blocks']:
                            x, y, z = block['pos']
                            if (y <= foundation['ground_y'] and
                                    template['palette'][block['state']]['Name'] in SOILS):
                                bottom_columns[x,z] = min(y, bottom_columns.get((x,z), y))
                        contacts = [(x, y, z) for (x, z), y in bottom_columns.items()]
                        if foundation.get('contact_mode') == 'embedded_art':
                            authored = {tuple(b['pos']) for b in template['blocks']}
                            contacts = [tuple(b['pos']) for b in template['blocks']
                                        if b['pos'][1] <= foundation['ground_y']
                                        and not template['palette'][b['state']]['Name'].endswith('_leaves')
                                        and template['palette'][b['state']]['Name'] not in AIR_NAMES
                                        and (b['pos'][0], b['pos'][1] - 1, b['pos'][2]) not in authored]
                        unsupported=[]
                        for x, y, z in contacts:
                            p = transform((x,y-1,z), child['rotation'], result['origin'])
                            state = world.block(*p)['Name']
                            if (state in AIR_NAMES or state.endswith('_leaves') or
                                    state in {'minecraft:water','minecraft:lava','minecraft:short_grass',
                                              'minecraft:tall_grass','minecraft:fern','minecraft:large_fern',
                                              'minecraft:snow','minecraft:vine'}):
                                unsupported.append(list(p))
                        result['foundation_contact'] = {'columns':len({(x,z) for x,y,z in contacts}),
                            'undersides_checked': len(contacts), 'mode': foundation.get('contact_mode', 'soil_columns'),
                            'unsupported_columns':len(unsupported),'examples':unsupported[:20],
                            'passed':bool(contacts) and not unsupported}
                        result['passed'] = result['passed'] and result['foundation_contact']['passed']
                        if foundation.get('feature_protection') == 'relics:placed_cells':
                            absent, checked_masks = [], 0
                            for block in template['blocks']:
                                if template['palette'][block['state']]['Name'] in AIR_NAMES:
                                    continue
                                p = transform(block['pos'], child['rotation'], result['origin'])
                                chunk = world.chunk(p[0] // 16, p[2] // 16)
                                checked_masks += 1
                                if chunk is None or not protected_cell(chunk, p):
                                    absent.append(list(p))
                            result['feature_protection'] = {'checked_cells': checked_masks,
                                'unprotected_cells': len(absent), 'examples': absent[:20],
                                'passed': checked_masks > 0 and not absent}
                            result['passed'] = result['passed'] and result['feature_protection']['passed']
                    result["start_chunk"] = cp
                    instances.append(result)
                except Exception as exc:
                    errors.append({"structure": name, "chunk": cp, "error": str(exc)})
    overlaps = structure_overlaps(instances)
    passed_types = {r["structure"] for r in instances if r["passed"]}
    complete_failures = [r for r in instances if not r["missing_chunks"] and not r["incomplete_chunks"] and not r["passed"]]
    return {"world": str(world_path), "artifact": str(artifact), "artifact_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
            "source": "saved natural structure starts and saved block states, compared with shipped NBT",
            "nature_exclusions": sorted(NATURE_NAMES), "instances": instances, "read_errors": world.read_errors, "verification_errors": errors,
            "fully_verified_structures": sorted(passed_types),
            "complete_instance_failures": len(complete_failures),
              "expected_structures": sorted(expected_structures),
              "overlaps": overlaps,
              "passed": set(expected_structures) <= passed_types and not world.read_errors and not errors
                        and not complete_failures and not overlaps}


def structure_overlaps(instances):
    """Horizontal footprint overlap is unsafe even if relics have different heights."""
    overlaps = []
    for index, first in enumerate(instances):
        for second in instances[index + 1:]:
            a, b = first["bounding_box"], second["bounding_box"]
            if a is None or b is None:
                continue
            if a[0] <= b[3] and b[0] <= a[3] and a[2] <= b[5] and b[2] <= a[5]:
                overlaps.append({"first": first["structure"], "second": second["structure"],
                                 "first_box": a, "second_box": b})
    return overlaps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--world", type=Path, required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("build/world-verification.json"))
    args = parser.parse_args()
    result = verify_world(args.world, args.artifact)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"World block verification passed={result['passed']}; instances={len(result['instances'])}; report={args.output}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
