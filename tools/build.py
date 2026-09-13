"""Reproducible, dependency-free build for the data-only Fabric mod."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "src/main/resources"
DATA_VERSION = 4903


def check_resources(resources: Path = RESOURCES) -> dict:
    metadata = json.loads((resources / "fabric.mod.json").read_text(encoding="utf-8"))
    for path in resources.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    pack = json.loads((resources / "pack.mcmeta").read_text(encoding="utf-8"))
    if pack["pack"]["min_format"] != [107, 1]:
        raise ValueError("Minecraft 26.2 pack format must be 107.1")
    required = [
        f"data/relics/{kind}/{name}.{extension}"
        for name in ("obelisk", "colossus")
        for kind, extension in (("structure", "nbt"), ("worldgen/structure", "json"),
                                ("worldgen/template_pool", "json"))
    ]
    for relative in required:
        if not (resources / relative).is_file():
            raise ValueError(f"Missing required resource: {relative}")
    return metadata


def write_archive(destination: Path, resources: Path = RESOURCES) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(resources.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(resources).as_posix()
            # Tile exports are editable source/debug assets; natural generation uses whole templates.
            if relative.startswith("data/relics/structure/") and "/tile_" in relative:
                continue
            info = zipfile.ZipInfo(relative, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3  # Fixed Unix metadata, independent of the build host.
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            content = path.read_bytes()
            if path.suffix == ".json" or path.name == "pack.mcmeta":
                # Canonical UTF-8/LF independent of checkout line endings and editor formatting.
                content = (json.dumps(json.loads(content.decode("utf-8-sig")),
                                      ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return hashlib.sha256(destination.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-generation", action="store_true", help="Package existing, validated assets")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    if not args.skip_generation:
        subprocess.run([
            sys.executable, str(ROOT / "tools/relic_assets.py"),
            "--output", str(RESOURCES / "data/relics/structure"),
            "--data-version", str(DATA_VERSION), "--seed", "2913",
            "--manifest", str(ROOT / "structures-src/generated/manifest.json"),
            "--single-template",
        ], check=True, cwd=ROOT)
    metadata = check_resources()
    artifact = args.output.resolve() / f"relics-{metadata['version']}+mc26.2.jar"
    checksum = write_archive(artifact)
    (artifact.parent / "SHA256SUMS.txt").write_text(f"{checksum}  {artifact.name}\n", encoding="utf-8")
    print(f"Built {artifact}\nSHA256 {checksum}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
