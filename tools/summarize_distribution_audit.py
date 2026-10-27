"""Compare completed fixed-seed native audits, preserving failed baseline evidence."""
import argparse
from collections import Counter
from datetime import date
import hashlib
import json
import math
from pathlib import Path
import statistics

from compile_worldgen import ROOT


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def relative(path):
    return path.resolve().relative_to(ROOT).as_posix()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True, help='Original run directory, including a failed natural test')
    parser.add_argument('--corrected', type=Path, required=True, help='Completed corrected run directory')
    parser.add_argument('--artifact', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--regression-evidence', type=Path, action='append', default=[])
    args = parser.parse_args()
    manifest = load(args.corrected / 'manifest.json')
    assert not manifest['failures'], manifest['failures']
    assert len(manifest['completed']) == len(manifest['seeds']) == 30
    assert digest(args.artifact) == manifest['artifact_sha256']
    old, new = [], []
    proofs = []
    seed_results = []
    for seed in manifest['seeds']:
        before = load(args.baseline / str(seed) / 'audit.json')
        audit_path = args.corrected / str(seed) / 'audit.json'
        after = load(audit_path)
        entry = next(row for row in manifest['completed'] if row['seed'] == seed)
        assert digest(audit_path) == entry['audit_sha256']
        assert before['seed'] == after['seed'] == seed
        assert before['window'] == after['window']
        assert before['cell_count'] == after['cell_count']
        assert [c['candidate'] for c in before['cells']] == [c['candidate'] for c in after['cells']]
        for key in ('seed', 'spawnX', 'spawnZ', 'bootstrapX', 'bootstrapZ', 'fingerprint', 'unique'):
            assert before['snapshot'].get(key) == after['snapshot'].get(key), (seed, key)
        assert before['production_reverse_order_match'] and after['production_reverse_order_match']
        old.append(before)
        new.append(after)
        proof_path = args.corrected / str(seed) / 'natural-proof.json'
        assert digest(proof_path) == entry['natural_proof_sha256']
        assert digest(args.corrected / str(seed) / 'console.log') == entry['console_sha256']
        proof = load(proof_path)
        if proof['selected_sites']:
            assert proof['block_verification']['passed'], seed
            proofs.append({'seed': seed, 'path': relative(proof_path), 'sha256': digest(proof_path),
                           'selected_sites': proof['selected_sites'], **proof['block_verification']})
        sx, sz = after['snapshot']['spawnX'], after['snapshot']['spawnZ']
        distances = [math.hypot(s['x2'] / 2 - sx, s['z2'] / 2 - sz) for s in after['accepted_sites']]
        seed_results.append({'seed': seed, 'cells': after['cell_count'],
                             'before': len(before['accepted_sites']), 'after': len(after['accepted_sites']),
                             'accepted_by_family': after['accepted_by_family'],
                             'nearest_repeatable_from_spawn': min(distances) if distances else None,
                             'audit_path': relative(audit_path), 'audit_sha256': digest(audit_path),
                             'elapsed_seconds': after['elapsed_seconds'], 'sites': after['accepted_sites']})

    def totals(audits):
        families, outcomes = Counter(), Counter()
        outside = 0
        for audit in audits:
            families.update(audit['accepted_by_family'])
            outcomes.update(audit['outcomes'])
            lo_x, lo_z, hi_x, hi_z = audit['window']
            outside += sum(not (lo_x <= s['x2'] / 2 < hi_x and lo_z <= s['z2'] / 2 < hi_z)
                           for s in audit['accepted_sites'])
        return {'cells': sum(a['cell_count'] for a in audits), 'accepted': sum(families.values()),
                'accepted_by_family': dict(families), 'outcomes': dict(outcomes),
                'zero_repeatable_seeds': sum(not a['accepted_sites'] for a in audits),
                'accepted_centers_outside_nominal_window': outside}

    nearest = [s['nearest_repeatable_from_spawn'] for s in seed_results if s['nearest_repeatable_from_spawn'] is not None]
    template_entries = ('data/relics/structure/', 'data/relics/worldgen/')
    import zipfile
    original_artifact = ROOT / 'build/distribution-artifacts/relics-0.1.0-alpha.5.0-dev+mc26.2.jar'
    with zipfile.ZipFile(original_artifact) as baseline, zipfile.ZipFile(args.artifact) as corrected:
        assets = [n for n in baseline.namelist() if n.startswith(template_entries)]
        assert assets and all(baseline.read(n) == corrected.read(n) for n in assets)
        assert not any('DistributionAuditMod' in n or 'DistributionFailureLogger' in n
                       or 'DistributionRuntimeChecks' in n for n in corrected.namelist())
    report = {'schema_version': 1, 'date': date.today().isoformat(),
              'baseline_manifest': relative(args.baseline / 'manifest.json'),
              'corrected_manifest': relative(args.corrected / 'manifest.json'),
              'corrected_manifest_sha256': digest(args.corrected / 'manifest.json'),
              'artifact_sha256': manifest['artifact_sha256'], 'policy': new[0]['snapshot']['policy'],
              'audit_source_sha256': manifest['audit_source_sha256'], 'audit_jar_sha256': manifest['audit_jar_sha256'],
              'seed_count': 30, 'window_per_seed': [120000, 120000],
              'window_selection': 'same cells whose original nominal candidate lies in the window around the frozen initial spawn',
              'original': totals(old), 'corrected': totals(new),
              'all_original_candidates_spawns_unique_targets_fingerprints_unchanged': True,
              'all_production_reverse_order_matches': True, 'unchanged_worldgen_resource_entries': len(assets),
              'natural_proofs': proofs,
              'regression_evidence': [{'path': relative(p), 'sha256': digest(p), 'result': load(p)}
                                      for p in args.regression_evidence],
              'natural_fixed_blocks_checked': sum(i['checked_blocks'] for p in proofs for i in p['instances']),
              'nearest_repeatable_from_spawn': {'seeds_with_site': len(nearest), 'min': min(nearest),
                                              'median': statistics.median(nearest), 'max': max(nearest)},
              'seed_results': seed_results,
              'limitations': ['Finite Vanilla terrain sample, no terrain-mod or multiplayer acceptance.',
                              'Each window selects nominal opportunities. Moved centers can cross a window edge; no density claim for every physical center inside that rectangle.',
                              'Not every planned site is materialized. Natural proofs validate only the listed instances.',
                              'Diagnostic whole-window times include extra predicate explanations and reverse-order replanning; they are not per-chunk latency.',
                              'The original audit crash remains part of baseline evidence.']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('seed_count', 'original', 'corrected', 'natural_fixed_blocks_checked', 'nearest_repeatable_from_spawn')}, indent=2))
    print(args.output)


if __name__ == '__main__':
    main()
