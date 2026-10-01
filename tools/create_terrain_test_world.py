"""Prepare a separate normal-terrain creative save from a recorded natural worldgen run."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time

from install_test_profile import prepare_level
from relic_assets import decode_nbt
from smoke_server import Console, DEFAULT_CACHE, DEFAULT_JAVA, DEFAULT_SERVER, ROOT, inspect_world, prepare_classpath, sha256
from verify_world import AIR_NAMES, AnvilWorld, verify_world


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accept-eula", action="store_true")
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True, help="Completed normal-terrain runtime report")
    args = parser.parse_args()
    if not args.accept_eula:
        parser.error("Read https://aka.ms/MinecraftEULA and pass --accept-eula for this isolated local server")
    source_report = json.loads(args.report.read_text(encoding="utf-8"))
    if source_report.get("showcase") or source_report.get("failure") or source_report.get("exit_code") != 0:
        raise ValueError("A completed normal-terrain server run is required")
    instances = source_report["world_blocks"]["instances"]
    expected = {"relics:colossus", "relics:obelisk", "relics:titan_skull"}
    if (not expected <= {i["structure"] for i in instances} or
            any(i["missing_chunks"] or i["incomplete_chunks"] or not i["bounding_box_matches"] for i in instances)):
        raise ValueError("Source world must contain all three complete natural relics")
    if sys.platform == "win32":
        processes = subprocess.run(["powershell", "-NoProfile", "-Command",
            "Get-Process java,javaw -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id"],
            capture_output=True, text=True)
        if processes.stdout.strip():
            raise ValueError("Close Minecraft and Java test servers before preparing the new save")
    if not (args.profile / "saves").is_dir():
        raise ValueError("The selected test profile's saves directory must exist")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    title = f"Relic V3 Terrain {stamp}"
    run = ROOT / f"build/terrain-preview/{stamp}"
    run.mkdir(parents=True, exist_ok=False)
    (run / "mods").mkdir()
    for entry in source_report["artifacts"]:
        source = args.profile / "mods" / entry["file"]
        if sha256(source) != entry["sha256"]:
            raise ValueError(f"Installed dependency/artifact differs from tested run: {source.name}")
        shutil.copy2(source, run / "mods" / source.name)
    source_world = Path(source_report["run_directory"]) / "world"
    # The old harness placed manual comparison models exclusively in Overworld
    # regions (0,0) and (1,0). Omit their blocks, entities and POI during the copy.
    # Source files are never deleted. Those areas regenerate normally if visited.
    manual_regions = {"r.0.0.mca", "r.1.0.mca"}
    overworld = source_world / "dimensions/minecraft/overworld"
    def ignore(directory, names):
        directory = Path(directory)
        is_overworld = directory.is_relative_to(overworld) or directory.parent == source_world
        if is_overworld and directory.name in {"region", "entities", "poi"}:
            return set(names) & manual_regions
        return set()
    world_path = run / "world"
    shutil.copytree(source_world, world_path, ignore=ignore)
    (world_path / "level.dat").write_bytes(prepare_level((world_path / "level.dat").read_bytes(), title))
    colossus = next(i for i in instances if i["structure"] == "relics:colossus")
    bb = colossus["bounding_box"]
    if colossus["rotation"] != "COUNTERCLOCKWISE_90":
        raise ValueError("This recorded preview expects the tested west-facing Colossus")
    view_x, view_z = bb[0] - 48, (bb[2] + bb[5]) // 2
    classpath = prepare_classpath(DEFAULT_CACHE, DEFAULT_SERVER, ROOT / "build/smoke/runtime")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    properties = {"server-ip": "127.0.0.1", "server-port": port, "online-mode": "true",
                  "white-list": "true", "enforce-whitelist": "true", "max-players": 1,
                  "enable-query": "false", "enable-rcon": "false", "level-name": "world",
                  "level-type": "minecraft:normal", "level-seed": source_report["seed"],
                  "generate-structures": "true", "gamemode": "creative", "difficulty": "normal",
                  "view-distance": 2, "simulation-distance": 2, "pause-when-empty-seconds": 0,
                  "max-tick-time": 180000, "spawn-protection": 0}
    (run / "server.properties").write_text("".join(f"{k}={v}\n" for k, v in properties.items()))
    (run / "eula.txt").write_text("# Explicitly accepted for this isolated preview server\neula=true\n")
    arguments = ["-Xms512M", "-Xmx4G", "-Djava.awt.headless=true", "-cp", ";".join(map(str, classpath)),
                 "net.fabricmc.loader.impl.launch.knot.KnotServer", "nogui"]
    argfile = run / "java-args.txt"
    argfile.write_text("\n".join('"' + a.replace("\\", "/") + '"' for a in arguments), encoding="utf-8")
    process = subprocess.Popen([str(DEFAULT_JAVA), "@" + str(argfile)], cwd=run, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                               encoding="utf-8", errors="replace", bufsize=1,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    console = Console(process, run / "console.log")
    commands = []
    def command(text, pattern):
        response = console.command(text, pattern + r"|Incomplete|Incorrect|Unknown command|Expected", timeout=180)
        if any(error in response for error in ("Incomplete", "Incorrect", "Unknown command", "Expected")):
            raise RuntimeError(f"Minecraft rejected {text!r}: {response}")
        commands.append({"command": text, "response": response})
        return response
    try:
        console.wait(r"Done \(", timeout=240)
        command(f"forceload add {view_x - 16} {view_z - 16} {view_x + 16} {view_z + 16}", r"Marked|force loaded")
        for x in range((view_x - 16) // 16 * 16, (view_x + 16) // 16 * 16 + 1, 16):
            for z in range((view_z - 16) // 16 * 16, (view_z + 16) // 16 * 16 + 1, 16):
                deadline = time.monotonic() + 180
                while "Test passed" not in command(f"execute if loaded {x} 80 {z}", r"Test passed|Test failed"):
                    if time.monotonic() > deadline:
                        raise TimeoutError("Preview spawn chunk did not finish generating")
                    time.sleep(1)
        command("save-all flush", r"Saved the game")
        saved = AnvilWorld(world_path)
        ground = next(y + 1 for y in range(319, -64, -1)
                      if saved.block(view_x, y, view_z)["Name"] not in AIR_NAMES)
        command(f"setworldspawn {view_x} {ground} {view_z} -90 0", r"Set the world spawn")
        command("gamerule minecraft:spawn_mobs true", r"Gamerule")
        command("gamerule minecraft:random_tick_speed 3", r"Gamerule")
        command("difficulty normal", r"difficulty|Difficulty")
        command("time set day", r"Set .*time|time marker")
        command("weather clear", r"weather|Weather")
        command("forceload remove all", r"Unmarked|Removed|No chunks")
        command("save-all flush", r"Saved the game")
    finally:
        if process.poll() is None:
            console.command("stop")
            process.wait(timeout=90)
        console.thread.join(timeout=5)
    if process.returncode != 0:
        raise RuntimeError("Preview server did not shut down cleanly")
    loaded = decode_nbt((world_path / "level.dat").read_bytes())["Data"]
    if loaded["LevelName"] != title or loaded["GameType"] != 1 or loaded["allowCommands"] != 1:
        raise ValueError("New save must retain its unique title, creative mode and cheats")
    artifact = next(run / "mods" / a["file"] for a in source_report["artifacts"] if a["file"].startswith("relics-"))
    verification = verify_world(world_path, artifact)
    if (not expected <= {i["structure"] for i in verification["instances"]} or
            any(i["missing_chunks"] or i["incomplete_chunks"] for i in verification["instances"]) or
            verification["read_errors"] or verification["verification_errors"]):
        raise ValueError("Natural relics must remain complete in the new terrain copy")
    destination = args.profile / "saves" / title
    shutil.copytree(world_path, destination)
    result = {"world_title": title, "world_path": str(destination), "seed": source_report["seed"],
              "spawn": loaded["spawn"], "manual_test_regions_omitted": sorted(manual_regions),
              "existing_worlds_modified": False, "commands": commands,
              "natural_structure_starts": inspect_world(destination)["natural_structure_starts"],
              "verification": verification}
    (run / "report.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("world_title", "world_path", "seed", "spawn")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
