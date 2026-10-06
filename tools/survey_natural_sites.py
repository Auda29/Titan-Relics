"""Nominate vanilla candidate chunks; saved natural starts are still required as proof."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import zipfile

from compile_worldgen import ROOT, compile_libraries, find_javac


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifact', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=731204)
    parser.add_argument('--rings', type=int, default=100)
    parser.add_argument('--count', type=int, default=2)
    args = parser.parse_args()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.artifact) as archive:
        selection = json.loads(archive.read('relics.integration.json'))
        for contract in selection['structures']:
            contract['resource'] = json.loads(archive.read(f"data/relics/worldgen/structure/{contract['id']}.json"))
        sets = {a['family']: json.loads(archive.read(f"data/relics/worldgen/structure_set/{a['family']}.json"))
                for a in selection['structures']}
    contracts = output.with_suffix('.contracts.json')
    contracts.write_text(json.dumps({'structures': selection['structures'], 'sets': sets}), encoding='utf-8')
    classes = output.parent / 'classes'
    classes.mkdir(exist_ok=True)
    compiler = find_javac()
    cp = os.pathsep.join(map(str, [*compile_libraries(), ROOT / 'build/worldgen-classes', classes]))
    subprocess.run([str(compiler), '-encoding', 'UTF-8', '-proc:none', '-classpath', cp, '-d', str(classes),
                    str(ROOT / 'tools/java/de/relics/NaturalSiteSurvey.java')], check=True)
    arguments = ['-Xmx2G', '-Djava.awt.headless=true', '-classpath', cp, 'de.relics.NaturalSiteSurvey',
                 str(contracts), str(args.seed), str(args.rings), str(args.count), str(output)]
    argfile = output.with_suffix('.args.txt')
    argfile.write_text('\n'.join('"' + a.replace('\\', '/') + '"' for a in arguments), encoding='utf-8')
    subprocess.run([str(compiler.with_name('java.exe')), '@' + str(argfile)], check=True, cwd=output.parent)


if __name__ == '__main__':
    main()
