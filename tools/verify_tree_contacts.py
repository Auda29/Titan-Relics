"""Check actual low root/terrain contacts in a completed natural Minecraft run."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from relic_assets import decode_nbt
from terrain_foundations import TOE_RADIUS, padding
from verify_world import AIR_NAMES, AnvilWorld, states_match, transform

ROOT = Path(__file__).resolve().parents[1]
GAP_NAMES = AIR_NAMES | {"minecraft:water", "minecraft:lava"}


def root_contacts(world, blocks, contract, instance):
    """Report raised root arches separately; ground-level gaps fail the check."""
    ground = contract["ground_y"]
    pad = padding(contract)
    lowest = {}
    for (x, y, z), state in blocks.items():
        if state["Name"].endswith("_log"):
            key = x, z
            if key not in lowest or y < lowest[key][0]:
                lowest[key] = y, state
    contacts, missing, gaps = 0, [], []
    for (x, z), (y, expected) in sorted(lowest.items()):
        if y > ground + 2:
            continue  # Do not turn taller intentional root arches into pillars.
        position = transform((x + TOE_RADIUS, y + pad, z + TOE_RADIUS),
                             instance["rotation"], instance["origin"])
        actual = world.block(*position)
        if actual is None or not states_match(expected, actual, instance["rotation"]):
            missing.append(list(position))
        below = world.block(position[0], position[1] - 1, position[2])
        if below is None or below["Name"] in GAP_NAMES:
            gaps.append({"raw_position": [x, y, z], "world_position": list(position),
                         "height_above_nominal_ground": y - ground,
                         "below": below["Name"] if below else "missing_chunk"})
        else:
            contacts += 1
    at_ground = [g for g in gaps if g["height_above_nominal_ground"] <= 0]
    return {"structure": "relics:world_tree", "low_root_columns": contacts + len(gaps),
            "direct_contacts": contacts, "missing_expected_wood": missing,
            "low_root_gap_columns": len(gaps), "ground_level_gap_columns": len(at_ground),
            "gaps_by_root_height_above_nominal_ground": dict(sorted(Counter(
                g["height_above_nominal_ground"] for g in gaps).items())),
            "gaps": gaps, "passed": not missing and not at_ground,
            "scope": "Lowest log per X/Z column at/below nominal ground +2; raised arches are reported, not filled"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    if report.get("showcase") or not report.get("passed"):
        raise ValueError("A passing complete natural-runtime report is required")
    contract = next(a for a in report["asset_selection"]["structures"] if a["id"] == "world_tree")
    data = (ROOT / contract["source"]).read_bytes()
    if hashlib.sha256(data).hexdigest() != contract["sha256"]:
        raise ValueError("Source export differs from the recorded natural run")
    template = decode_nbt(data)
    blocks = {tuple(b["pos"]): template["palette"][b["state"]] for b in template["blocks"]}
    world = AnvilWorld(Path(report["run_directory"]) / "world")
    checks = [root_contacts(world, blocks, contract, instance)
              for instance in report["world_blocks"]["instances"]
              if instance["structure"] == "relics:world_tree"]
    result = {"source_report": str(args.report), "source_report_sha256": hashlib.sha256(args.report.read_bytes()).hexdigest(),
              "source_nbt_sha256": contract["sha256"], "instances": checks,
              "read_errors": world.read_errors, "passed": bool(checks) and all(c["passed"] for c in checks) and not world.read_errors}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"passed": result["passed"], "instances": len(checks),
                      "ground_level_gap_columns": sum(c["ground_level_gap_columns"] for c in checks),
                      "raised_root_gap_columns": sum(c["low_root_gap_columns"] - c["ground_level_gap_columns"] for c in checks)}, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
