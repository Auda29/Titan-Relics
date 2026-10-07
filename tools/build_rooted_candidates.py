"""Preserve Alpha 4.7 exports; build three deeper, platform-free model candidates."""
import hashlib
import json
from pathlib import Path

from colossus_materials import encode_schematic
from inspect_ots_result import read_structure
from relic_catalog import ASSETS
from rooted_embedding import grow_roots, remove_terrain
from schem_to_nbt import convert, read_schematic

ROOT = Path(__file__).resolve().parents[1]
SPECS = {
    'titan_skull_rock': ('titan-skull-v4-rock-ground-v3', 'titan-skull-v4-rock-embedded-v1', 16, 22, 0,
                       '6303836dd1d816900a84897ad31cd4a74e659820612d61c677612e267b47051f'),
    'titan_skull_2': ('titan-skull-2-v2', 'titan-skull-2-v2-embedded-v1', 22, 28, 0,
                    '955703762402efc16d9d05a957a78368553ed019c35aec4aa659ee3754f3522b'),
    'world_tree': ('world-tree-v4-1-ground-v3', 'world-tree-v4-2-rooted', 8, 12, 12,
                  'fee50813242408123f4adcd1a0bacb476799359fce8e80ba5d59a49085823163'),
}


def build(name):
    previous, stem, old_ground, ground, shift, checksum = SPECS[name]
    folder = 'world-tree' if name == 'world_tree' else 'titan-skull'
    design = ROOT / f'relics/{folder}/design'
    source = design / 'generated' / previous / (previous + '.nbt')
    assert hashlib.sha256(source.read_bytes()).hexdigest() == checksum
    config = json.loads((design / (previous + '.json')).read_text())
    root, blocks = read_structure(source)
    art, report = remove_terrain(blocks, config['materials'], tree=name == 'world_tree', old_ground=old_ground)
    result = dict(art)
    if name == 'world_tree':
        result, roots = grow_roots(art, root['size'], old_ground)
        report.update(roots)
    translated = {(x, y + shift, z): s for (x, y, z), s in result.items()}
    size = list(root['size'])
    size[1] += shift
    assert all(0 <= p[i] < size[i] for p in translated for i in range(3))
    assert all(translated[x, y + shift, z] == s for (x, y, z), s in art.items())
    if name == 'titan_skull_2':
        parent = json.loads(source.with_name('verification.json').read_text())['new_relic_v1']
        for x, y, z in parent['void_probes_local']:
            assert all((x + dx, y + dy, z + dz) not in translated
                       for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1))
        report['void_probes_local'] = parent['void_probes_local']
        report['sword_bone_contact_faces'] = parent['sword_bone_contact_faces']
    out = design / 'generated' / stem
    out.mkdir(parents=True, exist_ok=True)
    schem = out / (stem + '.schem')
    schem.write_bytes(encode_schematic(translated, size, root['DataVersion'], [0, 0, 0]))
    convert(schem, schem.with_suffix('.nbt'), 'omit', 32)
    _, actual = read_structure(schem.with_suffix('.nbt'))
    assert actual == translated == read_schematic(schem.read_bytes())[1]
    manifest = json.loads(schem.with_suffix('.manifest.json').read_text())
    recovered = {}
    for tile in manifest['tiles']:
        _, cells = read_structure(out / tile['path'])
        for p, s in cells.items():
            q = tuple(a + b for a, b in zip(p, tile['origin']))
            assert q not in recovered
            recovered[q] = s
    assert recovered == translated
    contract = {**ASSETS[name], 'source': schem.with_suffix('.nbt').relative_to(ROOT).as_posix(),
                'version': stem, 'size': size, 'blocks': len(actual), 'ground_y': ground + shift,
                'sha256': hashlib.sha256(schem.with_suffix('.nbt').read_bytes()).hexdigest(),
                'foundation_mode': 'embedded_art', 'visually_accepted': False}
    if name == 'world_tree':
        contract['root_support'] = True
    report.update(source=source.relative_to(ROOT).as_posix(), source_sha256=checksum,
                  source_translation=[0, shift, 0], old_ground_y=old_ground,
                  effective_ground_y_in_source_coordinates=ground, additional_burial=ground - old_ground,
                  preserved_art_cells=len(art), all_original_art_preserved=True,
                  nbt_sha256=contract['sha256'], schematic_sha256=hashlib.sha256(schem.read_bytes()).hexdigest(),
                  blocks=len(actual), size=size, data_version=root['DataVersion'], tiles=len(manifest['tiles']),
                  placement_contract=contract, authored_terrain_cells=0, in_game_tested=False,
                  checks=['pinned source hash', 'exact original art after declared translation',
                          'no authored terrain platforms', 'schematic/NBT equality', 'lossless tiles', 'bounds'])
    if name == 'world_tree':
        _, accepted = read_structure(design / 'generated/world-tree-v4/world-tree-v4.nbt')
        for p, s in accepted.items():
            if '_log[' in s or '_leaves[' in s:
                assert translated[p[0], p[1] + shift, p[2]] == s
        report['accepted_v4_wood_and_leaves_preserved'] = True
    (out / 'verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    config.pop('input', None)
    config.update(output=schem.relative_to(ROOT).as_posix(), authoring='block-rooted-embedding-derivative',
                  source_nbt=source.relative_to(ROOT).as_posix(), height=size[1], ground_y=ground + shift,
                  title=stem.upper(), subtitle='Native terrain / deeper burial / no authored soil platform',
                  review_footer='Actual NBT candidate; original art retained, native terrain supplies the surface.')
    (design / (stem + '.json')).write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    (out / (stem + '.design.json')).write_text(json.dumps({'name': stem, 'rooted_embedding': report,
        'source_translation': [0, shift, 0], 'ground_level_nbt_approx': ground + shift,
        'visual_acceptance': 'October 7 user-requested candidate; review pending'}, indent=2) + '\n', encoding='utf-8')
    assert hashlib.sha256(source.read_bytes()).hexdigest() == checksum
    print(name, len(actual), 'blocks; burial +', ground - old_ground, '; removed ground', report['removed_terrain_cells'])
    return {'id': name, **contract}


def main():
    records = [build(name) for name in SPECS]
    output = ROOT / 'docs/project/rooted-candidates-20261007.json'
    output.write_text(json.dumps({'status': 'visual candidates; default selection unchanged',
        'scope': 'Deeper native-terrain embedding and wood root continuations, with no authored terrain platform',
        'structures': records}, indent=2) + '\n', encoding='utf-8')
    print(output)


if __name__ == '__main__':
    main()
