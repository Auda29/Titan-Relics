"""Audit saved runtime additions and the retained Skull 2 face cavities."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from relic_assets import decode_nbt
from terrain_foundations import TOE_RADIUS, padding
from verify_world import AIR_NAMES, AnvilWorld, protected_cell, transform

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--baseline-report', type=Path, help='Compare occupied probe cells at the same world coordinates')
    parser.add_argument('--preview-report', type=Path, help='Audit the installed terrain copy after verified reload')
    args = parser.parse_args()
    data = args.report.read_bytes()
    report = json.loads(data)
    assert report['passed'] and not report['showcase']
    world_path = Path(report['run_directory']) / 'world'
    verification = report['world_blocks']
    preview_evidence = {}
    if args.preview_report:
        preview_data = args.preview_report.read_bytes()
        preview = json.loads(preview_data)
        if (not preview.get('strict_natural_verification_passed') or not preview['verification'].get('passed')
                or preview['source_report_sha256'] != hashlib.sha256(data).hexdigest()):
            raise ValueError('A passing terrain reload from this exact natural run is required')
        world_path = Path(preview['world_path'])
        verification = preview['verification']
        preview_evidence = {'source_preview_report': args.preview_report.as_posix(),
                            'source_preview_report_sha256': hashlib.sha256(preview_data).hexdigest(),
                            'world': str(world_path)}
    world = AnvilWorld(world_path)
    baseline = None
    baseline_evidence = {}
    if args.baseline_report:
        baseline_data = args.baseline_report.read_bytes()
        before = json.loads(baseline_data)
        assert before['passed'] and not before['showcase'] and before['seed'] == report['seed']
        baseline = AnvilWorld(Path(before['run_directory']) / 'world')
        baseline_evidence = {'baseline_report': args.baseline_report.as_posix(),
                             'baseline_report_sha256': hashlib.sha256(baseline_data).hexdigest()}
    checks = []
    for instance in verification['instances']:
        name = instance['structure'].split(':')[1]
        a = next(a for a in report['asset_selection']['structures'] if a['id'] == name)
        if a.get('foundation_mode') != 'embedded_art':
            continue
        source = ROOT / a['source']
        assert hashlib.sha256(source.read_bytes()).hexdigest() == a['sha256']
        template = decode_nbt(source.read_bytes())
        def pos(p):
            x, y, z = p
            return transform((x + TOE_RADIUS, y + padding(a), z + TOE_RADIUS), instance['rotation'], instance['origin'])
        authored = {pos(b['pos']) for b in template['blocks']}
        bb = instance['bounding_box']
        extra = {}
        for cx in range(bb[0] // 16, bb[3] // 16 + 1):
            for cz in range(bb[2] // 16, bb[5] // 16 + 1):
                chunk = world.chunk(cx, cz)
                assert chunk is not None
                for cy, words in chunk.get('fabric:attachments', {}).get('relics:placed_cells', {}).items():
                    assert len(words) == 64
                    for word_index, signed in enumerate(words):
                        bits = signed & ((1 << 64) - 1)
                        while bits:
                            bit = (bits & -bits).bit_length() - 1
                            index = word_index * 64 + bit
                            p = (cx * 16 + index % 16, int(cy) * 16 + index // 256, cz * 16 + index % 256 // 16)
                            if bb[0] <= p[0] <= bb[3] and bb[2] <= p[2] <= bb[5] and p not in authored:
                                extra[p] = world.block(*p)['Name']
                            bits &= bits - 1
        ground = instance['origin'][1] + a['worldgen_template']['foundation']['ground_y']
        blocked = []
        provenance = json.loads(source.with_name('verification.json').read_text())
        for point in provenance.get('void_probes_local', []):
            x, y, z = point
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        p = pos((x + dx, y + dy, z + dz))
                        state = world.block(*p)
                        if state is None or state['Name'] not in AIR_NAMES:
                            chunk = world.chunk(p[0] // 16, p[2] // 16)
                            observation = {'world_position': p, 'state': state,
                                           'relic_protected': protected_cell(chunk, p) if chunk else None}
                            if baseline is not None:
                                old_state = baseline.block(*p)
                                old_chunk = baseline.chunk(p[0] // 16, p[2] // 16)
                                observation.update(baseline_state=old_state,
                                    baseline_relic_protected=protected_cell(old_chunk, p) if old_chunk else None,
                                    unchanged_at_same_world_position=old_state == state)
                            blocked.append(observation)
        invalid = [p for p, s in extra.items() if s in AIR_NAMES | {'minecraft:water', 'minecraft:lava'} or p[1] >= ground]
        check = {'id': name, 'source_sha256': a['sha256'], 'authored_cells': len(authored),
                 'additional_runtime_cells': len(extra), 'runtime_materials': dict(sorted(Counter(extra.values()).items())),
                 'highest_addition_relative_to_ground': max((p[1] - ground for p in extra), default=None),
                 'invalid_added_supports': invalid, 'face_void_probes': len(provenance.get('void_probes_local', [])),
                 'blocked_face_probe_cells': blocked, 'support_checks_passed': not invalid,
                 'strict_air_only_probes_passed': not blocked, 'passed': not invalid and not blocked}
        checks.append(check)
    result = {'source_report': args.report.as_posix(), 'source_report_sha256': hashlib.sha256(data).hexdigest(),
               **baseline_evidence, **preview_evidence,
              'scope': 'Exact saved mask additions and strict air-only 3x3x3 face-cavity checks; even native leaves fail the latter',
              'instances': checks, 'read_errors': world.read_errors,
              'baseline_read_errors': baseline.read_errors if baseline is not None else [],
              'support_checks_passed': len(checks) == 3 and all(c['support_checks_passed'] for c in checks) and not world.read_errors,
              'passed': len(checks) == 3 and all(c['passed'] for c in checks) and not world.read_errors
                        and (baseline is None or not baseline.read_errors)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
