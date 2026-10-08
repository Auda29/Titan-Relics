"""Compile placement and gameplay Java components against cached Minecraft/Fabric.

No Gradle, remapping or downloads: Minecraft 26.2 ships unobfuscated classes.
Set JAVA_HOME to a JDK 25 (a JRE is not sufficient for compiling).
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
JAVA_SOURCES = ROOT / "src/main/java"


def find_javac(java_home: Path | None = None) -> Path:
    homes = [java_home, os.environ.get("JAVA_HOME"),
             Path("E:/Temp/opencode/relic-jdk25/jdk-25.0.4.1+1")]
    for home in homes:
        if home:
            candidate = Path(home) / "bin" / ("javac.exe" if os.name == "nt" else "javac")
            if candidate.is_file():
                return candidate
    located = shutil.which("javac")
    if located:
        return Path(located)
    raise ValueError("Placement code needs JDK 25; set JAVA_HOME or pass --java-home")


def source_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(JAVA_SOURCES.rglob("*.java")):
        digest.update(path.relative_to(JAVA_SOURCES).as_posix().encode() + b"\0")
        digest.update(path.read_text(encoding="utf-8").replace("\r\n", "\n").encode())
    return digest.hexdigest()


def compile_libraries() -> list[Path]:
    """Prefer an explicit portable dependency cache; otherwise use local game caches."""
    prepared = ROOT / "build/worldgen-dependencies/classpath.json"
    if prepared.is_file():
        entries = json.loads(prepared.read_text(encoding="utf-8"))
        paths = []
        for entry in entries:
            path = prepared.parent / entry["file"]
            if (not path.resolve().is_relative_to(prepared.parent.resolve()) or
                    hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]):
                raise ValueError("Worldgen build dependency differs from its recorded checksum")
            paths.append(path)
        return paths
    from smoke_server import DEFAULT_CACHE, DEFAULT_SERVER, prepare_classpath

    if not DEFAULT_SERVER.is_file():
        raise ValueError("Prepare Java dependencies with tools/setup_worldgen_build.py --accept-downloads")
    libraries = prepare_classpath(DEFAULT_CACHE, DEFAULT_SERVER, ROOT / "build/smoke/runtime")
    lithostitched = DEFAULT_CACHE / "profiles/Relic Test/mods/lithostitched-1.8.0-fabric-26.2.jar"
    if not lithostitched.is_file():
        lithostitched = DEFAULT_CACHE / "profiles/TerraVista/mods" / lithostitched.name
    if not lithostitched.is_file():
        raise FileNotFoundError("Cached Lithostitched 1.8.0 JAR is required for compiling")
    fabric_api = lithostitched.parent / "fabric-api-0.161.0+26.2.jar"
    nested = ROOT / "build/worldgen-local-api"
    nested.mkdir(parents=True, exist_ok=True)
    for outer in [fabric_api, next(p for p in libraries if p.name == "fabric-loader-0.19.5.jar")]:
        with zipfile.ZipFile(outer) as archive:
            for name in archive.namelist():
                if name.startswith("META-INF/jars/") and name.endswith(".jar"):
                    path = nested / Path(name).name
                    path.write_bytes(archive.read(name))
                    libraries.append(path)
    return [*libraries, lithostitched]


def compile_worldgen(java_home: Path | None = None) -> Path:
    compiler = find_javac(java_home)
    version = subprocess.run([str(compiler), "-version"], capture_output=True, text=True, check=True)
    if not (version.stdout + version.stderr).strip().startswith("javac 25."):
        raise ValueError("Placement code must be built with JDK 25; set JAVA_HOME or pass --java-home")
    libraries = compile_libraries()
    input_source_hash = source_hash()
    destination = ROOT / "build/worldgen-classes"
    destination.mkdir(parents=True, exist_ok=True)
    # Publish only after successful compilation; never ship stale .class files.
    with tempfile.TemporaryDirectory(dir=destination.parent, prefix="worldgen-compile-") as td:
        staging = Path(td)
        arguments = ["--release", "25", "-encoding", "UTF-8", "-g:none", "-proc:none",
                     "-classpath", os.pathsep.join(map(str, libraries)), "-d", str(staging)]
        arguments += [str(p) for p in sorted(JAVA_SOURCES.rglob("*.java"))]
        argfile = staging / "javac-args.txt"
        argfile.write_text("\n".join('"' + a.replace("\\", "/").replace('"', '\\"') + '"'
                                     for a in arguments), encoding="utf-8")
        subprocess.run([str(compiler), "@" + str(argfile)], check=True, cwd=ROOT)
        if source_hash() != input_source_hash:
            raise ValueError("Placement source changed during compilation; retry with stable inputs")
        classes = sorted(staging.rglob("*.class"))
        manifest = {"source_sha256": input_source_hash, "compiler": (version.stdout + version.stderr).strip(),
                    "classes": {p.relative_to(staging).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in classes}}
        for path in classes:
            target = destination / path.relative_to(staging)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
        (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return destination


def checked_classes(directory: Path) -> list[Path]:
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest["source_sha256"] != source_hash() or not manifest["classes"]:
        raise ValueError("Stale or missing placement classes; rebuild with JDK 25")
    classes = []
    for relative, checksum in sorted(manifest["classes"].items()):
        path = directory / relative
        if not path.resolve().is_relative_to(directory.resolve()) or path.suffix != ".class":
            raise ValueError("Invalid placement class path")
        if hashlib.sha256(path.read_bytes()).hexdigest() != checksum:
            raise ValueError("Modified placement class; rebuild with JDK 25")
        classes.append(path)
    return classes
