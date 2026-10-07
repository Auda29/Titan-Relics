"""Read-only, matched saved-world solid-block crops for the three embedding revisions."""
import argparse
import hashlib
import json
from pathlib import Path

from relic_assets import encode_structure
from verify_world import AIR_NAMES, AnvilWorld, transform

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('titan_skull_rock', 'titan_skull_2', 'world_tree')
NON_CUBES = {'minecraft:short_grass', 'minecraft:tall_grass', 'minecraft:fern', 'minecraft:large_fern',
             'minecraft:dead_bush', 'minecraft:vine', 'minecraft:glow_lichen', 'minecraft:snow',
             'minecraft:dandelion', 'minecraft:poppy', 'minecraft:blue_orchid', 'minecraft:allium',
             'minecraft:azure_bluet', 'minecraft:oxeye_daisy', 'minecraft:cornflower', 'minecraft:lily_of_the_valley',
             'minecraft:sugar_cane', 'minecraft:seagrass', 'minecraft:tall_seagrass', 'minecraft:short_dry_grass',
             'minecraft:tall_dry_grass', 'minecraft:bush', 'minecraft:firefly_bush', 'minecraft:leaf_litter',
             'minecraft:wildflowers', 'minecraft:pink_petals'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before', type=Path, required=True)
    parser.add_argument('--after', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=ROOT / 'build/rooted-embedding/20261007/views')
    parser.add_argument('--structures', nargs='+', choices=NAMES, default=NAMES)
    args = parser.parse_args()
    reports = [json.loads(p.read_bytes()) for p in (args.before, args.after)]
    assert all(r['passed'] and not r['showcase'] for r in reports)
    args.output.mkdir(parents=True, exist_ok=True)
    records = []
    for name in args.structures:
        instances = [next(i for i in r['world_blocks']['instances'] if i['structure'] == 'relics:' + name) for r in reports]
        contracts = [next(a for a in r['asset_selection']['structures'] if a['id'] == name) for r in reports]
        assert instances[0]['rotation'] == instances[1]['rotation']
        assert instances[0]['origin'][0::2] == instances[1]['origin'][0::2]
        ground = instances[0]['origin'][1] + contracts[0]['worldgen_template']['foundation']['ground_y']
        assert ground == instances[1]['origin'][1] + contracts[1]['worldgen_template']['foundation']['ground_y']
        width, _, length = contracts[0]['worldgen_template']['size']
        y0 = ground - 10
        top = ground + {'titan_skull_rock': 66, 'titan_skull_2': 116, 'world_tree': 42}[name]
        for side, report, instance in zip(('before', 'after'), reports, instances):
            world = AnvilWorld(Path(report['run_directory']) / 'world')
            blocks = {}
            omitted = 0
            for x in range(width):
                for z in range(length):
                    wx, _, wz = transform((x, 0, z), instance['rotation'], instance['origin'])
                    for y in range(y0, top):
                        state = world.block(wx, y, wz)
                        if state is None:
                            raise ValueError(f'Missing saved chunk at {(wx, y, wz)}')
                        material = state['Name']
                        if material in AIR_NAMES:
                            continue
                        if material in NON_CUBES or material.endswith('_tulip'):
                            omitted += 1
                            continue
                        text = material
                        if state.get('Properties'):
                            text += '[' + ','.join(f'{k}={v}' for k, v in sorted(state['Properties'].items())) + ']'
                        blocks[x, y - y0, z] = text
            target = args.output / f'{name}-{side}.nbt'
            target.write_bytes(encode_structure(blocks, (width, top - y0, length), 4903))
            records.append({'id': name, 'side': side, 'path': target.relative_to(ROOT).as_posix(),
                            'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'blocks': len(blocks),
                            'nominal_ground_y': ground - y0, 'world_ground_y': ground,
                            'omitted_non_cube_plants': omitted, 'origin': instance['origin'],
                            'rotation': instance['rotation'], 'read_errors': world.read_errors})
            print(name, side, len(blocks), flush=True)
    (args.output / 'manifest.json').write_text(json.dumps({'scope':
        'Actual saved solid blocks, matched sites and crop bounds; small non-cube vegetation omitted for the cube renderer',
        'source_reports': [{'path': p.as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                           for p in (args.before, args.after)], 'records': records}, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
