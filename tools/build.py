"""Reproducible build selecting pinned exports and compiling placement/gameplay Java code."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

from relic_catalog import ASSETS, worldgen_resources
from terrain_foundations import POLICY, RUNTIME_POLICY, natural_ground, natural_size
from compile_worldgen import compile_worldgen, checked_classes
from release_version import release_version

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
    for relative, expected in worldgen_resources().items():
        path = resources / "data/relics" / relative
        if not path.is_file() or json.loads(path.read_text(encoding="utf-8")) != expected:
            raise ValueError(f"Missing/stale worldgen resource: {relative}; run the default build")
    manifest_path = resources / "relics.integration.json"
    if not manifest_path.is_file():
        raise ValueError("Missing selection manifest; run the default build")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get('foundation_policy') != POLICY:
        raise ValueError('Stale foundation policy; run the default build')
    if manifest.get('runtime_contact_policy') != RUNTIME_POLICY:
        raise ValueError('Stale runtime contact policy; run the default build')
    if (manifest["selection"] != "alpha4" or len(manifest["structures"]) != len(ASSETS)
            or {a["id"] for a in manifest["structures"]} != set(ASSETS)):
        raise ValueError("Stale asset selection manifest")
    for entry in manifest["structures"]:
        if any(entry.get(k) != v for k, v in ASSETS[entry["id"]].items()):
            raise ValueError(f"Stale asset contract: {entry['id']}")
        size = natural_size(entry)
        if entry['worldgen_template']['anchor'] != [size[0] // 2, natural_ground(entry) - 1, size[2] // 2]:
            raise ValueError(f"Stale surface anchor: {entry['id']}")
        for key in ("single_template", "worldgen_template"):
            suffix = "" if key == "single_template" else "_worldgen"
            if entry[key]["path"] != f"{entry['id']}{suffix}.nbt":
                raise ValueError(f"Unexpected template path: {entry[key]['path']}")
            template = resources / "data/relics/structure" / entry[key]["path"]
            if not template.is_file() or hashlib.sha256(template.read_bytes()).hexdigest() != entry[key]["sha256"]:
                raise ValueError(f"Missing/stale template: {template}")
        if entry["single_template"]["sha256"] != ASSETS[entry["id"]]["sha256"]:
            raise ValueError(f"Wrong selected export: {entry['id']}")
    if resources == RESOURCES or (resources / 'relics.gameplay.integration.json').exists():
        from integrate_gameplay_interiors import integrate,MANIFESTS
        for revision in MANIFESTS:integrate(resources,verify=True,revision=revision)
    metadata['version'] = release_version(metadata['version'])
    return metadata


def write_archive(destination: Path, resources: Path = RESOURCES, classes: Path | None = None) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    selected_templates = {f"data/relics/structure/{name}{suffix}.nbt"
                          for name in ASSETS for suffix in ("", "_worldgen")}
    from integrate_gameplay_interiors import MANIFESTS
    for gameplay in (resources/name for name in MANIFESTS.values()):
        if not gameplay.exists():continue
        for entry in json.loads(gameplay.read_text())['structures']:
            for kind in ('single_template','worldgen_template'):
                p=resources/'data/relics/structure'/entry[kind]['path']
                if hashlib.sha256(p.read_bytes()).hexdigest()!=entry[kind]['sha256']:
                    raise ValueError('Stale gameplay template: '+str(p))
                selected_templates.add('data/relics/structure/'+entry[kind]['path'])
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(resources.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(resources).as_posix()
            if relative in ('LICENSE', 'CREDITS.md'):
                continue  # Always use the current canonical project notices below.
            # Tile exports are editable source/debug assets; natural generation uses whole templates.
            if relative.startswith("data/relics/structure/") and "/tile_" in relative:
                continue
            if relative.startswith("data/relics/structure/") and relative not in selected_templates:
                continue  # Do not ship stale design/debug templates from a previous selection.
            info = zipfile.ZipInfo(relative, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3  # Fixed Unix metadata, independent of the build host.
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            content = path.read_bytes()
            if path.suffix == ".json" or path.name == "pack.mcmeta":
                # Canonical UTF-8/LF independent of checkout line endings and editor formatting.
                data = json.loads(content.decode("utf-8-sig"))
                if relative == 'fabric.mod.json':
                    data['version'] = release_version(data['version'])
                content = (json.dumps(data,
                                      ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        # The ports extract this archive as their resource input, so all four
        # player targets retain the same license and attribution notices.
        for name in ('LICENSE', 'CREDITS.md'):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            content = (ROOT / name).read_text(encoding='utf-8').replace('\r\n', '\n').encode('utf-8')
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        if classes is not None:
            for path in checked_classes(classes):
                info = zipfile.ZipInfo(path.relative_to(classes).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return hashlib.sha256(destination.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-generation", action="store_true", help="Package existing, validated assets")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--java-home", type=Path, help="JDK 25 directory for placement/gameplay Java code")
    args = parser.parse_args()
    if not args.skip_generation:
        subprocess.run([sys.executable, str(ROOT / "tools/integrate_relics.py")], check=True, cwd=ROOT)
        subprocess.run([sys.executable, str(ROOT / "tools/integrate_gameplay_interiors.py")], check=True, cwd=ROOT)
    metadata = check_resources()
    classes = compile_worldgen(args.java_home)
    artifact = args.output.resolve() / f"relics-{metadata['version']}+mc26.2.jar"
    checksum = write_archive(artifact, classes=classes)
    (artifact.parent / "SHA256SUMS.txt").write_text(f"{checksum}  {artifact.name}\n", encoding="utf-8")
    print(f"Built {artifact}\nSHA256 {checksum}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
