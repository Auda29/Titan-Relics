"""Install a runtime-verified JAR and new showcase world; never modify existing saves."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import time
import zipfile

from relic_assets import decode_nbt
from relic_catalog import ASSETS
from terrain_foundations import POLICY

ROOT = Path(__file__).resolve().parents[1]


def prepare_level(data: bytes, title: str) -> bytes:
    """Change two unique typed tags; preserve every other level.dat byte and type."""
    raw = gzip.decompress(data)
    decoded = decode_nbt(raw)["Data"]
    old_name = decoded["LevelName"].encode("utf-8")
    new_name = title.encode("utf-8")
    name_tag = b"\x08\x00\x09LevelName"
    before = name_tag + struct.pack(">H", len(old_name)) + old_name
    commands_tag = b"\x01\x00\x0dallowCommands"
    commands = commands_tag + bytes([decoded["allowCommands"]])
    if raw.count(before) != 1 or raw.count(commands) != 1:
        raise ValueError("Expected unique LevelName and allowCommands tags")
    raw = raw.replace(before, name_tag + struct.pack(">H", len(new_name)) + new_name, 1)
    raw = raw.replace(commands, commands_tag + b"\x01", 1)
    checked = decode_nbt(raw)["Data"]
    if checked["LevelName"] != title or checked["allowCommands"] != 1:
        raise ValueError("Could not prepare showcase level metadata")
    return gzip.compress(raw, mtime=0)


def validate_natural(natural: dict, expected: set[str], allow_feature_overwrites=False):
    """Do not let a terrain preview bypass the same natural-placement safety gate."""
    if not expected or set(natural.get("expected_natural_structures", [])) != expected:
        raise ValueError("Natural report must inspect every expected relic and biome variant")
    checks = natural.get("world_blocks", {})
    instances = checks.get("instances", [])
    requires_contact = natural.get("asset_selection", {}).get("foundation_policy") == POLICY
    complete = (not natural.get("failure") and not natural.get("shutdown_failure") and
                natural.get("exit_code") == 0 and not natural.get("blocking_log_errors") and
                 not checks.get("read_errors") and not checks.get("verification_errors") and not checks.get("overlaps") and
                expected <= {i["structure"] for i in instances} and
                all(i["bounding_box_matches"] and not i["missing_chunks"] and not i["incomplete_chunks"] and
                    i["checked_blocks"] > 0 and i["mismatch_count"] / i["checked_blocks"] < 0.01 and
                     i.get("foundation_contact", {}).get("passed", not requires_contact) and
                     i.get("feature_protection", {}).get("passed", not requires_contact)
                    for i in instances))
    if not complete:
        raise ValueError("Natural verification is missing/incomplete or contains substantial edits/errors")
    strict = natural.get("passed") and all(i["mismatch_count"] == 0 for i in instances)
    if not strict and not allow_feature_overwrites:
        raise ValueError("Natural verification failed; minor feature edits require explicit acknowledgement")


def validate_reports(natural: dict, showcase: dict, allow_feature_overwrites=False):
    """Fail closed on subset tests, incomplete models or substantial natural edits."""
    expected = {"relics:" + name for name in ASSETS}
    if not showcase.get("passed") or not showcase.get("showcase"):
        raise ValueError("Showcase runtime checks must pass before installation")
    if expected != {i["structure"] for i in showcase.get("showcase_blocks", {}).get("instances", [])}:
        raise ValueError("Showcase must verify every current relic and biome variant")
    validate_natural(natural, expected, allow_feature_overwrites)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--natural-report", type=Path, required=True)
    parser.add_argument("--showcase-report", type=Path, required=True)
    parser.add_argument("--no-showcase-world", action="store_true",
                        help="Keep the complete showcase acceptance gate, but do not add a flat inspection save")
    parser.add_argument("--allow-feature-overwrites", action="store_true",
                        help="Install a visual-test build with documented small natural feature edits; strict verification remains failed")
    args = parser.parse_args()
    if sys.platform == "win32":
        running = subprocess.run([
            "powershell", "-NoProfile", "-Command",
            "Get-Process java,javaw -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id",
        ], capture_output=True, text=True)
        if running.stdout.strip():
            raise ValueError("Close Minecraft and local Java test servers before installing")
    natural = json.loads(args.natural_report.read_text(encoding="utf-8"))
    showcase = json.loads(args.showcase_report.read_text(encoding="utf-8"))
    validate_reports(natural, showcase, args.allow_feature_overwrites)
    if not args.profile.is_dir():
        raise ValueError("Selected profile does not exist")
    version = json.loads((ROOT / "src/main/resources/fabric.mod.json").read_text())["version"]
    artifact = ROOT / "dist" / f"relics-{version}+mc26.2.jar"
    checksum = hashlib.sha256(artifact.read_bytes()).hexdigest()
    for report in (natural, showcase):
        expected = next(a["sha256"] for a in report["artifacts"] if a["file"] == artifact.name)
        if checksum != expected:
            raise ValueError("Current JAR differs from the tested artifact")
    mods = args.profile / "mods"
    relic_jars, ids = [], set()
    for jar in mods.glob("*.jar"):
        with zipfile.ZipFile(jar) as archive:
            if "fabric.mod.json" not in archive.namelist():
                continue
            metadata = json.loads(archive.read("fabric.mod.json"))
            ids.add(metadata["id"])
            if metadata["id"] == "relics":
                relic_jars.append(jar)
    if not {"fabric-api", "lithostitched"} <= ids:
        raise ValueError("Existing profile must contain Fabric API and Lithostitched")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = ROOT / f"build/profile-backups/{version}-upgrade-{stamp}"
    backup.mkdir(parents=True, exist_ok=False)
    for jar in relic_jars:
        shutil.copy2(jar, backup / jar.name)
        if hashlib.sha256(jar.read_bytes()).digest() != hashlib.sha256((backup / jar.name).read_bytes()).digest():
            raise ValueError("Backup verification failed")
    label = version.removeprefix("0.1.0-alpha.")
    title = None
    world = None
    if not args.no_showcase_world:
        title = f"Relic Alpha {label} Showcase {stamp}"
        source_world = Path(showcase["run_directory"]) / "world"
        prepared_level = prepare_level((source_world / "level.dat").read_bytes(), title)
        world = args.profile / "saves" / title
        shutil.copytree(source_world, world)
        (world / "level.dat").write_bytes(prepared_level)
    pending = mods / (artifact.name + ".pending")
    shutil.copy2(artifact, pending)
    if hashlib.sha256(pending.read_bytes()).hexdigest() != checksum:
        raise ValueError("Installed copy checksum mismatch")
    for jar in relic_jars:
        jar.unlink()  # Only identified Relic JARs, already individually backed up.
    pending.replace(mods / artifact.name)
    result = {"artifact": str(mods / artifact.name), "sha256": checksum,
              "backup": str(backup), "showcase_world": str(world) if world is not None else None, "world_title": title,
              "existing_worlds_modified": False, "strict_natural_verification_passed": natural["passed"],
              "feature_overwrites_acknowledged": args.allow_feature_overwrites,
              "natural_mismatches": [{"structure": i["structure"], "count": i["mismatch_count"],
                                      "kinds": i["mismatch_kinds"]} for i in natural["world_blocks"]["instances"]]}
    (backup / "installation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
