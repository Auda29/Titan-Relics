"""Select the checked-in V3 exports without modifying their geometry or DataVersion."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil

from relic_assets import decode_nbt, encode_structure

ROOT = Path(__file__).resolve().parents[1]
ASSETS = {
    "colossus": {"size": [181, 209, 227], "ground_y": 77, "blocks": 221221},
    "obelisk": {"size": [25, 185, 25], "ground_y": 8, "blocks": 93153},
    "titan_skull": {"size": [121, 79, 203], "ground_y": 8, "blocks": 264355},
}


def export_v3(output: Path, manifest_path: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    manifest = {"selection": "v3", "air_policy": "omit; preserve existing terrain", "structures": []}
    for name, contract in ASSETS.items():
        asset = name.replace("_", "-")
        source = ROOT / f"relics/{asset}/design/generated/{asset}-v3/{asset}-v3.nbt"
        data = source.read_bytes()
        root = decode_nbt(data)
        if root["size"] != contract["size"] or len(root["blocks"]) != contract["blocks"]:
            raise ValueError(f"Unexpected V3 export dimensions/block count: {source}")
        if root.get("entities") or any("nbt" in block for block in root["blocks"]):
            raise ValueError(f"Unexpected entities/block entities: {source}")
        destination = output / f"{name}.nbt"
        shutil.copyfile(source, destination)
        palette = []
        for state in root["palette"]:
            text = state["Name"]
            if state.get("Properties"):
                text += "[" + ",".join(f"{k}={v}" for k, v in state["Properties"].items()) + "]"
            palette.append(text)
        blocks = {tuple(b["pos"]): palette[b["state"]] for b in root["blocks"]}
        # Center the natural start in its chunk-reference radius. Y0 leaves the
        # established height/stub correction untouched; the marker is replaced
        # by the original block (or omitted structure_void) during generation.
        anchor = (contract["size"][0] // 2, 0, contract["size"][2] // 2)
        final_state = blocks.get(anchor, "minecraft:structure_void")
        blocks[anchor] = "minecraft:jigsaw[orientation=north_up]"
        entity = {k: (8, v) for k, v in {
            "id": "minecraft:jigsaw", "name": "relics:center", "target": "minecraft:empty",
            "pool": "minecraft:empty", "joint": "rollable", "final_state": final_state,
        }.items()}
        entity.update(selection_priority=(3, 0), placement_priority=(3, 0))
        natural = output / f"{name}_worldgen.nbt"
        natural_data = encode_structure(blocks, tuple(contract["size"]), root["DataVersion"], {anchor: entity})
        natural.write_bytes(natural_data)
        manifest["structures"].append({
            "id": name, **contract, "source": source.relative_to(ROOT).as_posix(),
            "data_version": root["DataVersion"],
            "single_template": {"path": destination.name, "sha256": hashlib.sha256(data).hexdigest()},
            "worldgen_template": {"path": natural.name, "sha256": hashlib.sha256(natural_data).hexdigest(),
                                  "anchor": list(anchor), "final_state": final_state},
        })
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    export_v3(ROOT / "src/main/resources/data/relics/structure",
              ROOT / "structures-src/generated/manifest.json")
