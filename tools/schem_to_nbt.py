"""Convert Sponge v2/v3 schematics to Java structure templates, without Minecraft."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from relic_assets import decode_nbt, encode_structure


AIR = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air"}
STATE = re.compile(r"[a-z0-9_.-]+:[a-z0-9_./-]+(?:\[[a-z0-9_]+=[a-z0-9_]+(?:,[a-z0-9_]+=[a-z0-9_]+)*\])?\Z")


def read_schematic(data: bytes, air: str = "omit") -> tuple[tuple[int, int, int], dict, int, list]:
    """Use local XYZ coordinates; schematic Offset is placement metadata only."""
    if air not in ("omit", "keep"):
        raise ValueError("Air policy must be omit or keep")
    root = decode_nbt(data)
    root = root.get("Schematic", root)
    version = root.get("Version")
    if version not in (2, 3):
        raise ValueError(f"Unsupported Sponge schematic version {version!r}; expected 2 or 3")
    size = tuple(root.get(key) for key in ("Width", "Height", "Length"))
    if any(type(n) is not int or n <= 0 for n in size):
        raise ValueError("Width, Height and Length must be positive integers")
    container = root.get("Blocks", {}) if version == 3 else root
    if not isinstance(container, dict):
        raise ValueError("Invalid Blocks compound")
    # Silent loss of inventories or entities would be worse than a clear refusal.
    if root.get("Entities") or container.get("BlockEntities") or container.get("TileEntities"):
        raise ValueError("Entities/block entities are not supported; export a blocks-only schematic")
    palette = container.get("Palette")
    raw = container.get("Data" if version == 3 else "BlockData")
    if not isinstance(palette, dict) or not palette or not isinstance(raw, bytes):
        raise ValueError("Missing block Palette or byte-array block data")
    lookup = {}
    for state, index in palette.items():
        if not STATE.fullmatch(state):
            raise ValueError(f"Invalid namespaced block state: {state!r}")
        if type(index) is not int or index < 0 or index in lookup:
            raise ValueError("Palette indices must be unique nonnegative integers")
        lookup[index] = state
    width, height, length = size
    volume = width * height * length
    if volume > len(raw):
        raise ValueError("Block data is too short for the declared dimensions")
    blocks = {}
    cursor = 0
    for index in range(volume):
        value = 0
        for shift in range(0, 35, 7):
            if cursor >= len(raw):
                raise ValueError("Truncated block-data VarInt")
            byte = raw[cursor]
            cursor += 1
            value |= (byte & 127) << shift
            if not byte & 128:
                break
        else:
            raise ValueError("Block-data VarInt exceeds five bytes")
        if value > 0x7fffffff or value not in lookup:
            raise ValueError(f"Unknown or invalid palette index {value}")
        state = lookup[value]
        if state == "minecraft:structure_void" or (air == "omit" and state in AIR):
            continue
        # Sponge: X changes fastest, then Z, then Y. Java templates use XYZ.
        pos = (index % width, index // (width * length), (index // width) % length)
        blocks[pos] = state
    if cursor != len(raw):
        raise ValueError("Trailing block data after declared volume")
    data_version = root.get("DataVersion")
    if type(data_version) is not int or data_version <= 0:
        raise ValueError("Missing or invalid DataVersion")
    offset = root.get("Offset", [0, 0, 0])
    if not isinstance(offset, list) or len(offset) != 3 or any(type(n) is not int for n in offset):
        raise ValueError("Offset must contain three integers")
    return size, blocks, data_version, offset


def convert(source: Path, output: Path, air: str, tile_size: int | None = None) -> dict:
    if source.resolve() == output.resolve():
        raise ValueError("Input and output must differ")
    if tile_size is not None and not 1 <= tile_size <= 128:
        raise ValueError("Tile size must be between 1 and 128")
    size, blocks, data_version, offset = read_schematic(source.read_bytes(), air)
    manifest = {"source": source.name, "size": list(size), "data_version": data_version,
                "source_offset": offset, "air_policy": air, "blocks": len(blocks), "tiles": []}
    data = encode_structure(blocks, size, data_version)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    if tile_size is not None:
        groups = {}
        for pos, state in blocks.items():
            origin = tuple(v // tile_size * tile_size for v in pos)
            local = tuple(v - o for v, o in zip(pos, origin))
            groups.setdefault(origin, {})[local] = state
        tile_dir = output.parent / (output.stem + "_tiles")
        tile_dir.mkdir(parents=True, exist_ok=True)
        for origin, entries in sorted(groups.items()):
            tile_extent = tuple(min(tile_size, total - o) for total, o in zip(size, origin))
            name = f"tile_{origin[0]}_{origin[1]}_{origin[2]}.nbt"
            (tile_dir / name).write_bytes(encode_structure(entries, tile_extent, data_version))
            manifest["tiles"].append({"path": f"{tile_dir.name}/{name}",
                                      "origin": list(origin), "size": list(tile_extent)})
    output.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--air", choices=("omit", "keep"), required=True,
                        help="omit preserves terrain; keep clears all schematic air, including outside the model")
    parser.add_argument("--tile-size", type=int, help="Also export rigid tiles and their relative origins (1..128)")
    args = parser.parse_args()
    try:
        manifest = convert(args.source, args.output, args.air, args.tile_size)
    except (ValueError, OSError, TypeError, AttributeError) as exc:
        parser.exit(1, f"Conversion failed: {exc}\n")
    print(f"{args.output}: {manifest['size']}, {manifest['blocks']} blocks, {len(manifest['tiles'])} tiles")


if __name__ == "__main__":
    main()
