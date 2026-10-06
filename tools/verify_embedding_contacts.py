"""Audit buried raw-Y0 art undersides in saved natural worlds, without filling them."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from relic_assets import decode_nbt
from terrain_foundations import TOE_RADIUS, padding
from verify_world import AIR_NAMES, AnvilWorld, states_match, transform

ROOT = Path(__file__).resolve().parents[1]
GAP_NAMES = AIR_NAMES | {'minecraft:water', 'minecraft:lava'}


def boundary_art_cells(blocks, terrain_states, rework_low_moss=False):
    """Select the derivative's immutable art at its finite raw-template floor."""
    return {p: state for p, state in blocks.items() if p[1] == 0
            and state['Name'] not in terrain_states
            and not (rework_low_moss and state['Name'] == 'minecraft:moss_block')}


def buried_contacts(world, cells, contract, instance):
    below_names, gaps, missing = Counter(), [], []
    for raw_position, expected in sorted(cells.items()):
        x, y, z = raw_position
        position = transform((x + TOE_RADIUS, y + padding(contract), z + TOE_RADIUS),
                             instance['rotation'], instance['origin'])
        actual = world.block(*position)
        if actual is None or not states_match(expected, actual, instance['rotation']):
            missing.append(list(position))
        below = world.block(position[0], position[1] - 1, position[2])
        below_names[below['Name'] if below else 'missing_chunk'] += 1
        if below is None or below['Name'] in GAP_NAMES:
            gaps.append({'raw_position': list(raw_position), 'world_position': list(position),
                         'below': below['Name'] if below else 'missing_chunk'})
    return {'structure': instance['structure'], 'boundary_art_cells_checked': len(cells),
            'substrate_states': dict(sorted(below_names.items())),
            'missing_expected_art': missing, 'unsupported_cells': len(gaps), 'gaps': gaps,
            'passed': not missing and not gaps,
            'scope': 'Immutable art at raw Y0; immediate saved-world substrate must be present, non-air and non-fluid'}


def audit(report_path, preview_path=None):
    data = report_path.read_bytes()
    report = json.loads(data)
    if report.get('showcase') or not report.get('passed') or report.get('exit_code') != 0:
        raise ValueError('A passing complete natural-runtime report is required')
    verification = report['world_blocks']
    world_path = Path(report['run_directory']) / 'world'
    result = {'source_report': str(report_path), 'source_report_sha256': hashlib.sha256(data).hexdigest()}
    if preview_path:
        preview_data = preview_path.read_bytes()
        preview = json.loads(preview_data)
        if not preview.get('strict_natural_verification_passed') or not preview['verification'].get('passed'):
            raise ValueError('Terrain copy must pass strict post-reload verification')
        if preview['source_report_sha256'] != result['source_report_sha256']:
            raise ValueError('Terrain copy belongs to a different natural run')
        verification = preview['verification']
        world_path = Path(preview['world_path'])
        result.update(source_preview_report=str(preview_path),
                      source_preview_report_sha256=hashlib.sha256(preview_data).hexdigest())
    world = AnvilWorld(world_path)
    checks, sources, required = [], [], set()
    for contract in report['asset_selection']['structures']:
        source = ROOT / contract['source']
        export = source.read_bytes()
        if hashlib.sha256(export).hexdigest() != contract['sha256']:
            raise ValueError('Source differs from recorded runtime selection')
        provenance_data = source.with_name('verification.json').read_bytes()
        provenance = json.loads(provenance_data)
        count = provenance.get('buried_boundary_undersides_requiring_runtime_check', 0)
        if not count:
            continue
        if provenance['nbt_sha256'] != contract['sha256'] or provenance['placement_contract'] != {
                k: contract[k] for k in provenance['placement_contract']}:
            raise ValueError('Derivative provenance differs from recorded selection')
        template = decode_nbt(export)
        blocks = {tuple(b['pos']): template['palette'][b['state']] for b in template['blocks']}
        terrain = {state.split('[')[0] for state in provenance['terrain_states']}
        cells = boundary_art_cells(blocks, terrain, provenance['low_moss_pads_reworked'])
        if len(cells) != count:
            raise ValueError('Boundary category differs from derivative verification')
        required.add('relics:' + contract['id'])
        sources.append({'id': contract['id'], 'source_nbt_sha256': contract['sha256'],
                        'verification_sha256': hashlib.sha256(provenance_data).hexdigest()})
        for instance in verification['instances']:
            if instance['structure'] == 'relics:' + contract['id']:
                checks.append(buried_contacts(world, cells, contract, instance))
    result.update(world=str(world_path), sources=sources, instances=checks, read_errors=world.read_errors,
                  passed=bool(required) and required <= {c['structure'] for c in checks}
                  and all(c['passed'] for c in checks) and not world.read_errors)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--preview-report', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.report, args.preview_report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'passed': result['passed'], 'instances': len(result['instances']),
                      'boundary_art_cells_checked': sum(c['boundary_art_cells_checked'] for c in result['instances']),
                      'unsupported_cells': sum(c['unsupported_cells'] for c in result['instances'])}, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
