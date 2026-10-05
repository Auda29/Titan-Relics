"""Run headless tests against Minecraft's actual block/processor APIs, without a server."""
import os
from pathlib import Path
import subprocess

from compile_worldgen import ROOT, compile_worldgen, compile_libraries, find_javac


def main():
    classes = compile_worldgen()
    compiler = find_javac()
    libraries = [*compile_libraries(), classes]
    output = ROOT / "build/worldgen-test-classes"
    output.mkdir(parents=True, exist_ok=True)
    sources = sorted((ROOT / "src/test/java").rglob("*.java"))
    argfile = output / "javac-args.txt"
    args = ["--release", "25", "-encoding", "UTF-8", "-proc:none", "-classpath",
            os.pathsep.join(map(str, libraries)), "-d", str(output), *map(str, sources)]
    argfile.write_text("\n".join('"' + a.replace("\\", "/") + '"' for a in args), encoding="utf-8")
    subprocess.run([str(compiler), "@" + str(argfile)], check=True)
    runtime_args = ["-Djava.awt.headless=true", "-cp", os.pathsep.join(map(str, [output, *libraries])),
                    "de.relics.WorldgenTests"]
    runtime_file = output / "java-args.txt"
    runtime_file.write_text("\n".join('"' + a.replace("\\", "/") + '"' for a in runtime_args), encoding="utf-8")
    subprocess.run([str(compiler.with_name("java.exe" if os.name == "nt" else "java")), "@" + str(runtime_file)], check=True)


if __name__ == "__main__":
    main()
