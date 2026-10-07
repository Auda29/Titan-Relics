"""Select pinned art and derive surface-anchored natural templates for Alpha 4.9."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from relic_assets import decode_nbt, encode_structure
from relic_catalog import ASSETS, ROOT, worldgen_resources
from terrain_foundations import POLICY, RUNTIME_POLICY, supported_blocks


def export_relics(output: Path, manifest_path: Path) -> dict:
    manifest = {"selection": "alpha4", "revision": "2026-10-07-shallow-skull-footprint-and-sparse-root-strands",
                "foundation_policy": POLICY,
                "runtime_contact_policy": RUNTIME_POLICY,
                "air_policy": "omit; preserve existing terrain", "structures": []}
    prepared = []
    # Validate all input first: fail closed if the other thread changes an export.
    for name, contract in ASSETS.items():
        source = ROOT / contract["source"]
        data = source.read_bytes()
        checksum = hashlib.sha256(data).hexdigest()
        verified = json.loads((source.parent / "verification.json").read_text(encoding="utf-8"))
        root = decode_nbt(data)
        if checksum != contract["sha256"] or checksum != verified["nbt_sha256"]:
            raise ValueError(f"Source export hash changed: {source}")
        if root["size"] != contract["size"] or len(root["blocks"]) != contract["blocks"]:
            raise ValueError(f"Unexpected export dimensions/block count: {source}")
        if root.get("entities") or any("nbt" in block for block in root["blocks"]):
            raise ValueError(f"Unexpected entities/block entities: {source}")
        palette = []
        for state in root["palette"]:
            text = state["Name"]
            if state.get("Properties"):
                text += "[" + ",".join(f"{k}={v}" for k, v in sorted(state["Properties"].items())) + "]"
            if state["Name"] in ("minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:jigsaw"):
                raise ValueError(f"Unexpected authored air/anchor in omitted-air export: {source}")
            palette.append(text)
        blocks = {tuple(b["pos"]): palette[b["state"]] for b in root["blocks"]}
        if len(blocks) != contract["blocks"]:
            raise ValueError(f"Duplicate block positions: {source}")
        blocks, natural_size, foundation = supported_blocks(blocks, contract)
        # Jigsaw's projected piece origin is independent of anchor Y, but its
        # generation stub/biome query is not. Put that query at the surface,
        # rather than in a cave underneath the correctly buried structure.
        anchor = (natural_size[0] // 2, foundation['ground_y'] - 1, natural_size[2] // 2)
        final_state = blocks.get(anchor, "minecraft:structure_void")
        blocks[anchor] = "minecraft:jigsaw[orientation=north_up]"
        entity = {k: (8, v) for k, v in {
            "id": "minecraft:jigsaw", "name": "relics:center", "target": "minecraft:empty",
            "pool": "minecraft:empty", "joint": "rollable", "final_state": final_state,
        }.items()}
        entity.update(selection_priority=(3, 0), placement_priority=(3, 0))
        natural = encode_structure(blocks, tuple(natural_size), root["DataVersion"], {anchor: entity})
        prepared.append((name, data, natural))
        manifest["structures"].append({
            "id": name, **contract, "data_version": root["DataVersion"],
            "single_template": {"path": f"{name}.nbt", "sha256": checksum},
            "worldgen_template": {"path": f"{name}_worldgen.nbt", "sha256": hashlib.sha256(natural).hexdigest(),
                                  "anchor": list(anchor), "final_state": final_state,
                                  "size": natural_size, "foundation": foundation},
        })
    output.mkdir(parents=True, exist_ok=True)
    for name, data, natural in prepared:
        (output / f"{name}.nbt").write_bytes(data)
        (output / f"{name}_worldgen.nbt").write_bytes(natural)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    return manifest


def integrate(resources: Path = ROOT / "src/main/resources") -> dict:
    result = export_relics(resources / "data/relics/structure", resources / "relics.integration.json")
    for relative, data in worldgen_resources().items():
        path = resources / "data/relics" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result


if __name__ == "__main__":
    integrate()
