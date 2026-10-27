"""Run the production distribution planner/journal against deterministic synthetic terrain."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile
from compile_worldgen import ROOT, compile_libraries, compile_worldgen, find_javac


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--java-home', type=Path)
    args = parser.parse_args()
    classes = compile_worldgen(args.java_home)
    compiler = find_javac(args.java_home)
    cp = os.pathsep.join(map(str, [classes, *compile_libraries()]))
    with tempfile.TemporaryDirectory(dir=ROOT / 'build', prefix='distribution-unit-') as directory:
        subprocess.run([str(compiler), '--release', '25', '-encoding', 'UTF-8', '-proc:none',
                        '-classpath', cp, '-d', directory,
                        str(ROOT / 'src/test/java/de/relics/DistributionTests.java'),
                        str(ROOT / 'src/test/java/de/relics/LocationSearchTests.java'),
                        str(ROOT / 'src/test/java/de/relics/WorldgenGateTests.java')], check=True)
        subprocess.run([str(compiler.with_name('java.exe' if os.name == 'nt' else 'java')),
                        '-classpath', os.pathsep.join([directory, cp]), 'de.relics.WorldgenGateTests'], cwd=directory, check=True)
        subprocess.run([str(compiler.with_name('java.exe' if os.name == 'nt' else 'java')),
                        '-classpath', os.pathsep.join([directory, cp]), 'de.relics.LocationSearchTests'], cwd=directory, check=True)
        subprocess.run([str(compiler.with_name('java.exe' if os.name == 'nt' else 'java')),
                        '-classpath', os.pathsep.join([directory, cp]), 'de.relics.DistributionTests',
                        directory], cwd=directory, check=True)


if __name__ == '__main__':
    main()
