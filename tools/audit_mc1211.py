"""Audit actual bounded supports and record face-cavity contents on a 1.21.1 site.

No fixed 26.2 world-coordinate cave boxes or same-site comparisons are reused
across game versions. Strict air-only findings stay separate from contact checks.
"""
import argparse
import hashlib
import json
from pathlib import Path

from audit_cave_candidates import support_checks
from relic_catalog import ROOT
from verify_world import AIR_NAMES, AnvilWorld, protected_cell, transform


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = json.loads(args.report.read_bytes())
    if (not report.get('passed') or report.get('showcase') or report.get('minecraft_version') != '1.21.1'
            or report.get('exit_code') != 0):
        raise ValueError('A completed passing natural 1.21.1 run is required')
    world = AnvilWorld(Path(report['run_directory']) / 'world')
    checks = support_checks(report, world)
    contract = next(a for a in report['asset_selection']['structures'] if a['id'] == 'titan_skull_2')
    instance = next(i for i in report['world_blocks']['instances'] if i['structure'] == 'relics:titan_skull_2')
    probes = json.loads((ROOT / contract['source']).with_name('verification.json').read_bytes())['void_probes_local']
    blocked = []
    for x, y, z in probes:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    pos = transform((x + 8 + dx, y + dy, z + 8 + dz), instance['rotation'], instance['origin'])
                    state = world.block(*pos)
                    if state is None:
                        raise ValueError('Missing saved face-cavity probe cell')
                    if state['Name'] not in AIR_NAMES:
                        blocked.append({'position': pos, 'state': state,
                                        'protected': protected_cell(world.chunk(pos[0] // 16, pos[2] // 16), pos)})
    result = {'scope': 'Independent runtime support-mask audit on 1.21.1; no cross-version fixed cave-box comparison',
              'source_report': args.report.as_posix(),
              'source_report_sha256': hashlib.sha256(args.report.read_bytes()).hexdigest(),
              'minecraft': '1.21.1', 'seed': report['seed'], 'supports': checks,
              'skull_face_probe': {'origin': instance['origin'], 'rotation': instance['rotation'],
                                  'checked_cells': len(probes) * 27, 'blocked': blocked,
                                  'strict_air_only_passed': not blocked,
                                  'scope': 'Omitted cells preserve native scenery; independent observation, not contact acceptance'},
              'read_errors': world.read_errors,
              'passed': all(c['passed'] for c in checks) and not world.read_errors}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
