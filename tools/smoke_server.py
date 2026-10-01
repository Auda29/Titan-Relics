"""Run an isolated, local Fabric 26.2 server and save actual runtime evidence.

No downloads or profile edits. --accept-eula explicitly accepts Minecraft's EULA
for this test server: https://aka.ms/MinecraftEULA . Each run gets a fresh world.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import re
import shutil
import socket
import struct
import subprocess
import threading
import time
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CACHE = Path("E:/Roaming/ModrinthApp")
DEFAULT_JAVA = DEFAULT_CACHE / "meta/java_versions/zulu25.36.205-ca-jre25.0.4.1-win_x64/bin/java.exe"
DEFAULT_SERVER = Path.home() / ".gradle/caches/fabric-loom/26.2/minecraft-server.jar"
BASE_MODS = ["fabric-api-0.160.0+26.2.jar", "lithostitched-1.8.0+beta6-fabric-26.2.jar"]
INTEGRATION_MODS = ["tectonic-3.0.26-fabric-26.2.jar", "Terralith_26.2_v2.6.4.jar",
                    "BiomesOPlenty-fabric-26.2-26.2.0.0.28.jar", "dungeons-and-taverns-5.3.2.jar",
                    "GlitchCore-fabric-26.2-26.2.0.0.0.jar", "TerraBlender-fabric-26.2-26.2.0.0.2.jar"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_nbt(data: bytes) -> dict:
    """Read standard big-endian NBT including chunk long arrays."""
    stream = io.BytesIO(data)

    def take(count):
        result = stream.read(count)
        if len(result) != count:
            raise ValueError("Truncated NBT")
        return result

    def number(fmt):
        return struct.unpack(">" + fmt, take(struct.calcsize(">" + fmt)))[0]

    def string():
        return take(number("H")).decode("utf-8", errors="replace")

    def value(tag):
        if tag in (1, 2, 3, 4, 5, 6):
            return number({1: "b", 2: "h", 3: "i", 4: "q", 5: "f", 6: "d"}[tag])
        if tag == 8:
            return string()
        if tag == 9:
            child, count = number("B"), number("i")
            if count < 0:
                raise ValueError("Negative NBT length")
            return [value(child) for _ in range(count)]
        if tag == 10:
            result = {}
            while (child := number("B")) != 0:
                name = string()
                result[name] = value(child)
            return result
        if tag in (7, 11, 12):
            count = number("i")
            if count < 0:
                raise ValueError("Negative NBT length")
            if tag == 7:
                return take(count)
            return [number("i" if tag == 11 else "q") for _ in range(count)]
        raise ValueError(f"Unknown NBT tag {tag}")

    if number("B") != 10:
        raise ValueError("Expected compound NBT root")
    string()
    return value(10)


def inspect_world(world: Path) -> dict:
    """Read saved chunks. Structure starts prove natural generation, not /place."""
    starts, chunks, errors = [], 0, []
    region_directory = world / "dimensions/minecraft/overworld/region"
    if not region_directory.exists():
        region_directory = world / "region"
    for region in sorted(region_directory.glob("*.mca")):
        data = region.read_bytes()
        for index in range(1024):
            offset = int.from_bytes(data[index * 4:index * 4 + 3], "big") * 4096
            if not offset:
                continue
            try:
                length = int.from_bytes(data[offset:offset + 4], "big")
                compression = data[offset + 4]
                payload = data[offset + 5:offset + 4 + length]
                if compression == 1:
                    payload = gzip.decompress(payload)
                elif compression == 2:
                    payload = zlib.decompress(payload)
                elif compression != 3:
                    raise ValueError(f"Unsupported region compression {compression}")
                chunk = read_nbt(payload)
                chunks += 1
                for key, start in chunk.get("structures", {}).get("starts", {}).items():
                    if key.startswith("relics:") and start.get("id") != "INVALID":
                        children = start.get("Children", [])
                        starts.append({"structure": key, "chunk": [chunk.get("xPos"), chunk.get("zPos")],
                                       "status": chunk.get("Status"), "pieces": len(children),
                                       "bounding_boxes": [c.get("BB") for c in children]})
            except Exception as exc:
                errors.append({"region": region.name, "slot": index, "error": str(exc)})
    return {"saved_chunks": chunks, "natural_structure_starts": starts, "read_errors": errors}


def prepare_classpath(cache: Path, bundler: Path, destination: Path) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    classpath = []
    with zipfile.ZipFile(bundler) as archive:
        for kind in ("versions", "libraries"):
            for line in archive.read(f"META-INF/{kind}.list").decode().splitlines():
                expected, _, relative = line.split("\t")
                path = (destination / kind / relative).resolve()
                if not path.is_relative_to(destination.resolve()):
                    raise ValueError(f"Bundled library path escapes runtime directory: {relative}")
                path.parent.mkdir(parents=True, exist_ok=True)
                content = archive.read(f"META-INF/{kind}/{relative}")
                if hashlib.sha256(content).hexdigest() != expected:
                    raise ValueError(f"Bundled library hash mismatch: {relative}")
                if not path.exists() or sha256(path) != expected:
                    path.write_bytes(content)
                classpath.append(path)
    version = json.loads((cache / "meta/versions/26.2-0.19.5/26.2-0.19.5.json").read_text())
    for library in version["libraries"]:
        if library["name"].startswith(("net.fabricmc:", "org.ow2.asm:")):
            group, artifact, version_number = library["name"].split(":")[:3]
            path = cache / "meta/libraries" / group.replace(".", "/") / artifact / version_number / f"{artifact}-{version_number}.jar"
            if not path.is_file():
                raise FileNotFoundError(path)
            classpath.append(path)
    return classpath


class Console:
    def __init__(self, process, log_path):
        self.process = process
        self.lines = []
        self.condition = threading.Condition()
        self.log_path = log_path
        self.thread = threading.Thread(target=self._read, daemon=True)
        self.thread.start()

    def _read(self):
        with self.log_path.open("w", encoding="utf-8") as output:
            for line in self.process.stdout:
                output.write(line)
                output.flush()
                with self.condition:
                    self.lines.append(line.rstrip())
                    self.condition.notify_all()
                print(line.rstrip(), flush=True)

    def wait(self, pattern, start=0, timeout=120):
        deadline = time.monotonic() + timeout
        with self.condition:
            while True:
                for line in self.lines[start:]:
                    if re.search(pattern, line):
                        return line
                if self.process.poll() is not None:
                    raise RuntimeError(f"Server exited {self.process.returncode}; see {self.log_path}")
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f"No response matching {pattern!r} after {timeout}s")
                self.condition.wait(min(remaining, 1))

    def command(self, command, pattern=None, timeout=120):
        start = len(self.lines)
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()
        if pattern:
            return self.wait(pattern, start, timeout)
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accept-eula", action="store_true")
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--java", type=Path, default=DEFAULT_JAVA)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--server-bundler", type=Path, default=DEFAULT_SERVER)
    parser.add_argument("--mods-source", type=Path, default=DEFAULT_CACHE / "profiles/TerraVista/mods")
    parser.add_argument("--integration", action="store_true")
    parser.add_argument("--showcase", action="store_true", help="Build a flat creative preview world; validate manual placements instead of natural starts")
    parser.add_argument("--settings-pack", type=Path, help="Copy an already generated settings ZIP into the fresh world's datapacks")
    parser.add_argument("--disabled-structure", action="append", choices=["obelisk", "colossus", "titan_skull"], default=[],
                        help="Expect locate to find no natural instance of this disabled structure; manual templates still run")
    parser.add_argument("--seed", type=int, default=731204)
    parser.add_argument("--startup-timeout", type=int, default=180)
    parser.add_argument("--command-timeout", type=int, default=180)
    parser.add_argument("--prepare-only", action="store_true", help="Extract cached server libraries, without starting Java")
    args = parser.parse_args()
    smoke = ROOT / "build/smoke"
    smoke.mkdir(parents=True, exist_ok=True)
    classpath = prepare_classpath(args.cache, args.server_bundler, smoke / "runtime")
    if args.prepare_only:
        print(f"Prepared {len(classpath)} cached classpath entries in {smoke / 'runtime'}")
        return 0
    if not args.accept_eula:
        parser.error("Read https://aka.ms/MinecraftEULA and pass --accept-eula to accept it for this isolated test server")
    current_version = json.loads((ROOT / "src/main/resources/fabric.mod.json").read_text(encoding="utf-8"))["version"]
    artifact = args.artifact or ROOT / "dist" / f"relics-{current_version}+mc26.2.jar"
    if artifact is None or not artifact.is_file():
        parser.error("Build the alpha first or pass --artifact")
    run = smoke / (time.strftime("run-%Y%m%d-%H%M%S") + f"-{time.time_ns() % 1000000:06d}")
    (run / "mods").mkdir(parents=True)
    if args.settings_pack:
        packs = run / "world/datapacks"
        packs.mkdir(parents=True, exist_ok=True)
        shutil.copy2(args.settings_pack, packs / args.settings_pack.name)
    files = [artifact] + [args.mods_source / name for name in BASE_MODS + (INTEGRATION_MODS if args.integration else [])]
    evidence = {"seed": args.seed, "run_directory": str(run), "integration": args.integration, "showcase": args.showcase,
                "eula_accepted_explicitly": True, "artifacts": [], "commands": [], "passed": False}
    expected_structures = {"relics:" + name for name in ("obelisk", "colossus", "titan_skull") if name not in args.disabled_structure}
    evidence["expected_natural_structures"] = sorted(expected_structures)
    if args.settings_pack:
        settings_snapshot = run / "world/datapacks" / args.settings_pack.name
        with zipfile.ZipFile(settings_snapshot) as archive:
            overrides = {name: json.loads(archive.read(f"data/relics/worldgen/structure_set/{name}.json"))
                         for name in ("obelisk", "colossus", "titan_skull")}
        evidence["settings_pack"] = {"file": args.settings_pack.name, "sha256": sha256(settings_snapshot),
                                     "structure_set_overrides": overrides}
    for source in files:
        shutil.copy2(source, run / "mods" / source.name)
        evidence["artifacts"].append({"file": source.name, "sha256": sha256(run / "mods" / source.name)})
    # The world must be verified against the exact JAR loaded for this run,
    # even if another developer rebuilds dist/ while the server is running.
    artifact = run / "mods" / artifact.name
    with socket.socket() as candidate:
        candidate.bind(("127.0.0.1", 0))
        port = candidate.getsockname()[1]
    (run / "eula.txt").write_text("# Explicitly accepted by the caller for this isolated test\neula=true\n")
    properties = {"server-ip": "127.0.0.1", "server-port": port, "online-mode": "true", "white-list": "true",
                  "enforce-whitelist": "true", "max-players": 1, "enable-query": "false", "enable-rcon": "false",
                  "level-name": "world", "level-seed": args.seed, "level-type": "minecraft:normal",
                  "generate-structures": "true", "gamemode": "creative", "difficulty": "peaceful",
                  "view-distance": 2, "simulation-distance": 2, "pause-when-empty-seconds": 0,
                   "max-tick-time": 180000, "spawn-protection": 0, "initial-disabled-packs": ""}
    if args.showcase:
        properties.update({"level-type": "minecraft:flat", "generator-settings": json.dumps({
            "biome": "minecraft:plains", "lakes": False, "features": False,
            "layers": [{"block": "minecraft:bedrock", "height": 1},
                       {"block": "minecraft:stone", "height": 124},
                       {"block": "minecraft:dirt", "height": 2},
                       {"block": "minecraft:grass_block", "height": 1}],
            "structure_overrides": []})})
    (run / "server.properties").write_text("".join(f"{key}={value}\n" for key, value in properties.items()))
    arguments = ["-Xms512M", "-Xmx4G", "-Djava.awt.headless=true", "-cp", ";".join(map(str, classpath)),
                 "net.fabricmc.loader.impl.launch.knot.KnotServer", "nogui"]
    # A Java argument file avoids Windows' process command-line length limit.
    argfile = run / "java-args.txt"
    argfile.write_text("\n".join('"' + arg.replace("\\", "/").replace('"', '\\"') + '"' for arg in arguments), encoding="utf-8")
    process = subprocess.Popen([str(args.java), "@" + str(argfile)], cwd=run, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                               encoding="utf-8", errors="replace", bufsize=1,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    console = Console(process, run / "console.log")

    def command(text, pattern, timeout=None):
        started = time.monotonic()
        response = console.command(text, pattern, timeout or args.command_timeout)
        evidence["commands"].append({"command": text, "response": response,
                                     "elapsed_seconds": round(time.monotonic() - started, 4)})
        return response

    def load_area(x1, z1, x2, z2):
        # Split by chunk columns: /forceload permits at most 256 chunks per command.
        rows = z2 // 16 - z1 // 16 + 1
        columns = min(8, 256 // rows)
        if columns < 1:
            raise ValueError("Area exceeds the supported /forceload row count")
        for cx in range(x1 // 16, x2 // 16 + 1, columns):
            end_x = min((cx + columns) * 16 - 1, x2)
            command(f"forceload add {cx * 16} {z1} {end_x} {z2}",
                    r"Marked|force loaded|force-loaded|No chunks")
        for check_x in range(x1 // 16 * 16, x2 // 16 * 16 + 1, 16):
            for check_z in range(z1 // 16 * 16, z2 // 16 * 16 + 1, 16):
                deadline = time.monotonic() + args.command_timeout
                while True:
                    loaded = command(f"execute if loaded {check_x} 80 {check_z}", r"Test passed|Test failed")
                    if "Test passed" in loaded:
                        break
                    if time.monotonic() > deadline:
                        raise TimeoutError(f"Chunk {check_x}, {check_z} did not finish generating")
                    time.sleep(1)

    try:
        evidence["startup"] = console.wait(r'Done \(', timeout=args.startup_timeout)
        command("gamerule minecraft:spawn_mobs false", r"Gamerule|Unknown|Incorrect")
        command("gamerule minecraft:random_tick_speed 0", r"Gamerule|Unknown|Incorrect")
        if args.settings_pack:
            response = command("datapack list enabled", r"data pack")
            evidence["settings_pack"]["enabled_response"] = response
            if args.settings_pack.name not in response:
                raise RuntimeError("Expected settings datapack is not in the server's enabled list")
        # Manual command placements and natural starts are recorded separately.
        for name, x, y, sx, sz in (("obelisk", 0, 56, 25, 25),
                                   ("colossus", 256, -13, 181, 227),
                                   ("titan_skull", 768, 56, 121, 203)):
            load_area(x, 0, x + sx - 1, sz - 1)
            response = command(f"place template relics:{name} {x} {y} 0", r"Loaded template|Failed|Could not|Unknown|Incorrect")
            evidence.setdefault("manual_placements", []).append({"structure": f"relics:{name}",
                      "requested_position": [x, y, 0], "method": "place template",
                      "success": "Loaded template" in response, "response": response})
            command("forceload remove all", r"Unmarked|Removed|No chunks|force.loaded")
        command("setworldspawn 220 64 -40", r"Set the world spawn")
        for name in (() if args.showcase else ("obelisk", "colossus", "titan_skull")):
            if name in args.disabled_structure:
                response = command(f"locate structure relics:{name}", r"nearest|Could not find|Unknown|Incorrect", timeout=60)
                evidence.setdefault("disabled_locate_results", []).append({"structure": f"relics:{name}",
                              "response": response, "passed": "Could not find a structure" in response,
                              "elapsed_seconds": evidence["commands"][-1]["elapsed_seconds"]})
                continue
            response = command(f"locate structure relics:{name}", r"nearest|Could not find|Unknown|Incorrect")
            match = re.search(r"\[(-?\d+),\s*(?:~|-?\d+),\s*(-?\d+)\]", response)
            located = {"structure": f"relics:{name}", "response": response}
            if match:
                x, z = map(int, match.groups())
                located["position"] = [x, z]
                # /locate reports the start anchor, not the rotated footprint center.
                # Generate and save that start, then force its actual full bounding box.
                load_area(x, z, x + 15, z + 15)
                command("save-all flush", r"Saved the game", timeout=240)
                starts = inspect_world(run / "world")["natural_structure_starts"]
                start = next((s for s in starts if s["structure"] == f"relics:{name}" and
                              s["chunk"] == [x // 16, z // 16]), None)
                if not start or not start["bounding_boxes"]:
                    raise RuntimeError(f"No saved natural start at the located {name} anchor")
                boxes = start["bounding_boxes"]
                load_area(min(b[0] for b in boxes), min(b[2] for b in boxes),
                          max(b[3] for b in boxes), max(b[5] for b in boxes))
                located["bounding_boxes"] = boxes
                command("save-all flush", r"Saved the game", timeout=240)
                command("forceload remove all", r"Unmarked|Removed|No chunks|force.loaded")
            evidence.setdefault("locate_results", []).append(located)
        command("save-all flush", r"Saved the game", timeout=240)
    except Exception as exc:
        evidence["failure"] = f"{type(exc).__name__}: {exc}"
    finally:
        if process.poll() is None:
            try:
                console.command("stop")
                process.wait(timeout=90)
            except Exception as exc:
                evidence["shutdown_failure"] = str(exc)
                process.terminate()
                try:
                    process.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=15)
        console.thread.join(timeout=5)
        evidence["exit_code"] = process.returncode
        try:
            evidence["world"] = inspect_world(run / "world")
            from verify_world import verify_world
            evidence["world_blocks"] = verify_world(run / "world", artifact)
            if args.showcase:
                from verify_world import AnvilWorld, verify_piece
                world = AnvilWorld(run / "world")
                checks = []
                with zipfile.ZipFile(artifact) as archive:
                    for placement in evidence.get("manual_placements", []):
                        name = placement["structure"].split(":")[1]
                        template = read_nbt(gzip.decompress(archive.read(f"data/relics/structure/{name}.nbt")))
                        x, y, z = placement["requested_position"]
                        size = template["size"]
                        child = {"rotation": "NONE", "PosX": x, "PosY": y, "PosZ": z,
                                 "BB": [x, y, z, x + size[0] - 1, y + size[1] - 1, z + size[2] - 1]}
                        checks.append(verify_piece(world, placement["structure"], child, template, skip_nature=False))
                evidence["showcase_blocks"] = {"instances": checks, "read_errors": world.read_errors,
                                               "passed": len(checks) == 3 and all(c["passed"] for c in checks) and not world.read_errors}
        except Exception as exc:
            evidence["world"] = {"natural_structure_starts": [], "read_errors": [str(exc)]}
            evidence["world_blocks"] = {"fully_verified_structures": [], "read_errors": [str(exc)],
                                        "verification_errors": [], "passed": False}
        evidence["log_errors"] = [line for line in console.lines if re.search(r"/ERROR\]|Exception|Failed to parse|Failed to load", line)]
        found = {start["structure"] for start in evidence["world"]["natural_structure_starts"]}
        perflib_present = any("Unable to locate English counter names in registry Perflib 009" in line
                              for line in evidence["log_errors"])
        evidence["environment_diagnostics"] = [line for line in evidence["log_errors"]
            if "Unable to locate English counter names in registry Perflib 009" in line
            or (perflib_present and line == "com.sun.jna.platform.win32.Win32Exception: Falscher Parameter.")]
        evidence["blocking_log_errors"] = [line for line in evidence["log_errors"]
                                           if line not in evidence["environment_diagnostics"]]
        evidence["clean_log"] = not evidence["log_errors"]
        evidence["passed"] = (not evidence.get("failure") and not evidence.get("shutdown_failure") and
                              process.returncode == 0 and not evidence["blocking_log_errors"] and
                               len(evidence.get("manual_placements", [])) == 3 and
                              all(p["success"] for p in evidence.get("manual_placements", [])) and
                              len(evidence.get("disabled_locate_results", [])) == len(args.disabled_structure) and
                              all(p["passed"] for p in evidence.get("disabled_locate_results", [])) and
                              expected_structures <= found and
                              not ({"relics:" + name for name in args.disabled_structure} & found) and
                              not evidence["world"]["read_errors"] and
                              expected_structures <= set(evidence["world_blocks"]["fully_verified_structures"]) and
                              evidence["world_blocks"].get("complete_instance_failures", 0) == 0 and
                              not evidence["world_blocks"]["read_errors"] and
                               not evidence["world_blocks"]["verification_errors"])
        if args.showcase:
            evidence["passed"] = (not evidence.get("failure") and not evidence.get("shutdown_failure") and
                                  process.returncode == 0 and not evidence["blocking_log_errors"] and
                                  len(evidence.get("manual_placements", [])) == 3 and
                                  all(p["success"] for p in evidence["manual_placements"]) and
                                  evidence.get("showcase_blocks", {}).get("passed", False))
        payload = json.dumps(evidence, indent=2, ensure_ascii=False) + "\n"
        (run / "report.json").write_text(payload, encoding="utf-8")
        (smoke / "report.json").write_text(payload, encoding="utf-8")
    print(f"Smoke passed={evidence['passed']}; report={smoke / 'report.json'}")
    return 0 if evidence["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
