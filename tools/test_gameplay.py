"""Compile and run real 26.2 item/recipe and ledger tests, without starting a server.

Uses the prepared checksum-verified cache and JDK 25. No downloads, EULA acceptance,
Minecraft world creation, profile changes or fixture registration on real saves.
"""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile
from compile_worldgen import compile_libraries, compile_worldgen, find_javac

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--java-home', type=Path)
    args = parser.parse_args()
    classes = compile_worldgen(args.java_home)
    compiler = find_javac(args.java_home)
    libraries = compile_libraries()
    with tempfile.TemporaryDirectory(dir=ROOT / 'build', prefix='gameplay-unit-') as directory:
        temporary = Path(directory)
        cp = os.pathsep.join(map(str, [classes, *libraries]))
        subprocess.run([str(compiler), '--release', '25', '-encoding', 'UTF-8', '-proc:none',
                        '-classpath', cp, '-d', str(temporary),
                        str(ROOT / 'src/test/java/de/relics/GameplayTests.java'),
                        str(ROOT / 'src/test/java/de/relics/GameplayMixinTargets.java')], check=True)
        subprocess.run([str(compiler.parent / ('java.exe' if os.name == 'nt' else 'java')),
                        '-classpath', os.pathsep.join([str(temporary), cp]), 'de.relics.GameplayTests',
                        str(ROOT / 'src/main/resources'), str(temporary)], cwd=temporary, check=True)

if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode) from None
