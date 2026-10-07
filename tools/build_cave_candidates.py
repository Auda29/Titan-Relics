"""Two scoped Alpha 4.9 candidates: sparse Tree strands and shallow Skull 2 burial."""
import hashlib
import json
from pathlib import Path

from branching_roots import grow_strands
from colossus_materials import encode_schematic
from inspect_ots_result import read_structure
from relic_catalog import ASSETS
from rooted_embedding import remove_terrain
from schem_to_nbt import convert, read_schematic

ROOT = Path(__file__).resolve().parents[1]


def main():
    previous = 'world-tree-v4-1-ground-v3'
    stem = 'world-tree-v4-3-strands'
    design = ROOT / 'relics/world-tree/design'
    source = design / 'generated' / previous / (previous + '.nbt')
    digest = 'fee50813242408123f4adcd1a0bacb476799359fce8e80ba5d59a49085823163'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
    config = json.loads((design / (previous + '.json')).read_bytes())
    root, blocks = read_structure(source)
    art, report = remove_terrain(blocks, config['materials'], tree=True, old_ground=8)
    result, geometry = grow_strands(art, root['size'])
    report.update(geometry)
    translated = {(x,y+12,z):s for (x,y,z),s in result.items()}
    size = [root['size'][0], root['size'][1]+12, root['size'][2]]
    assert all(0 <= p[k] < size[k] for p in translated for k in range(3))
    out = design / 'generated' / stem
    out.mkdir(parents=True, exist_ok=True)
    path = out / (stem + '.schem')
    path.write_bytes(encode_schematic(translated, size, root['DataVersion'], [0,0,0]))
    convert(path, path.with_suffix('.nbt'), 'omit', 32)
    _, actual = read_structure(path.with_suffix('.nbt'))
    assert actual == translated == read_schematic(path.read_bytes())[1]
    manifest = json.loads(path.with_suffix('.manifest.json').read_bytes())
    recovered = {}
    for tile in manifest['tiles']:
        _, cells = read_structure(out/tile['path'])
        for p,s in cells.items():
            q = tuple(a+b for a,b in zip(p,tile['origin']))
            assert q not in recovered
            recovered[q] = s
    assert recovered == actual
    _, accepted = read_structure(design / 'generated/world-tree-v4/world-tree-v4.nbt')
    for (x,y,z),s in accepted.items():
        if '_log[' in s or '_leaves[' in s:
            assert actual[x,y+12,z] == s
    tree = {**ASSETS['world_tree'], 'source': path.with_suffix('.nbt').relative_to(ROOT).as_posix(),
            'version': stem, 'size': size, 'blocks': len(actual), 'ground_y': 24,
            'sha256': hashlib.sha256(path.with_suffix('.nbt').read_bytes()).hexdigest(),
            'foundation_mode': 'embedded_art', 'root_support': True,
            'max_support_depth': 2, 'surface_contact_depth': 3, 'follow_art': True,
            'visually_accepted': False}
    report.update(source=source.relative_to(ROOT).as_posix(), source_sha256=digest,
                  source_translation=[0,12,0], old_ground_y=8, effective_ground_y_in_source_coordinates=12,
                  additional_burial=4, preserved_art_cells=len(art), all_original_art_preserved=True,
                  accepted_v4_wood_and_leaves_preserved=True, authored_terrain_cells=0,
                  nbt_sha256=tree['sha256'], schematic_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  size=size, blocks=len(actual), tiles=len(manifest['tiles']), data_version=root['DataVersion'],
                  placement_contract=tree, in_game_tested=False,
                  checks=['pinned source', 'accepted original art after declared translation',
                          'new strand connectivity', 'no footprint extrusion', 'schematic/NBT identity', 'lossless tiles'])
    (out/'verification.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    config.pop('input', None)
    config.update(output=path.relative_to(ROOT).as_posix(), authoring='block-rooted-embedding-derivative',
                  source_nbt=source.relative_to(ROOT).as_posix(), height=size[1], ground_y=24,
                  title=stem.upper(), subtitle='Sparse tapered root strands / short surface contacts / open caves')
    (design/(stem+'.json')).write_text(json.dumps(config, indent=2)+'\n', encoding='utf-8')
    path.with_suffix('.design.json').write_text(json.dumps({'name':stem, 'rooted_embedding':report,
        'visual_acceptance':'User-requested cave-contact candidate; review pending'}, indent=2)+'\n', encoding='utf-8')
    # Full raw Skull/sword anatomy remains the pinned source. Only the derived
    # natural template excludes the deeply buried slice, leaving native cave rock.
    skull = {**ASSETS['titan_skull_2'], 'ground_y': 28, 'buried_clip_depth': 6,
             'max_support_depth': 2, 'surface_contact_depth': 6, 'follow_art': True,
             'visually_accepted': False}
    assert hashlib.sha256((ROOT/skull['source']).read_bytes()).hexdigest() == skull['sha256']
    index = ROOT/'docs/project/cave-candidates-20261007.json'
    index.write_text(json.dumps({'status':'two visual candidates; default selection unchanged',
        'scope':'Skull 2 shallow natural footprint and Tree strands; rock Skull retains Alpha 4.8',
        'structures':[{'id':'titan_skull_2', **skull}, {'id':'world_tree', **tree}]}, indent=2)+'\n', encoding='utf-8')
    print(f'Tree: {len(actual)} blocks, {geometry["new_wood_cells"]} new connected strand cells, {len(geometry["strands"])} paths')
    print(index)


if __name__ == '__main__':
    main()
