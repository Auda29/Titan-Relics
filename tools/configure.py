"""Create a world-specific override datapack; the installed mod stays unchanged."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PRESETS = {
    "rare": {"obelisk": (96, 48), "colossus": (120, 60)},
    "normal": {"obelisk": (64, 32), "colossus": (80, 40)},
    "frequent": {"obelisk": (32, 16), "colossus": (40, 20)},
}


def settings_resources(density: str, disabled: list[str]) -> dict[str, bytes]:
    if density not in PRESETS:
        raise ValueError(f"Unknown density: {density}")
    if set(disabled) - {"obelisk", "colossus"}:
        raise ValueError("Only obelisk and colossus can be disabled")
    result = {}
    for name, (spacing, separation) in PRESETS[density].items():
        relative = f"data/relics/worldgen/structure_set/{name}.json"
        data = json.loads((ROOT / "src/main/resources" / relative).read_text(encoding="utf-8"))
        data["placement"].update(spacing=spacing, separation=separation)
        # Empty sets also remove locator candidates; frequency=0 still scans them.
        if name in disabled:
            data["structures"] = []
        result[relative] = (json.dumps(data, indent=2) + "\n").encode()
    result["pack.mcmeta"] = (json.dumps({"pack": {
        "description": f"Relic Mod settings: {density}; disabled: {', '.join(disabled) or 'none'}",
        "min_format": [107, 1], "max_format": [107, 1],
    }}, indent=2) + "\n").encode()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--density", choices=PRESETS, default="normal")
    parser.add_argument("--disable", choices=("obelisk", "colossus"), action="append", default=[])
    parser.add_argument("--output", type=Path, default=ROOT / "dist/relics-settings.zip")
    args = parser.parse_args()
    resources = settings_resources(args.density, sorted(set(args.disable)))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, value in sorted(resources.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3  # Match the canonical mod archive on every OS.
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, value)
    print(f"Created {args.output.resolve()}")
    print("Install in this world's datapacks folder with higher priority than the mod, then restart.")
    print("Only new generation changes. Already generated structures remain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
