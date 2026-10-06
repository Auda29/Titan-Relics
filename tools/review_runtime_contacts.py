"""Compare saved blocks at the exact Alpha 4.6 contact failures; no world writes."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from relic_assets import decode_nbt
from terrain_foundations import SOILS, TOE_RADIUS, padding
from verify_world import AIR_NAMES, AnvilWorld, protected_cell, transform

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before', type=Path, required=True)
    parser.add_argument('--after', type=Path, required=True)
    parser.add_argument('--tree-gaps', type=Path, required=True)
    parser.add_argument('--buried-gaps', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    reports = [json.loads(p.read_bytes()) for p in (args.before, args.after)]
    if not all(r['passed'] and not r['showcase'] for r in reports):
        raise ValueError('Both worlds must have completed strict core natural verification')
    worlds = [AnvilWorld(Path(r['run_directory']) / 'world') for r in reports]
    roots = json.loads(args.tree_gaps.read_bytes())['instances'][0]['gaps']
    root = max((g for g in roots if g['height_above_nominal_ground'] <= 0),
               key=lambda g: g['height_above_nominal_ground'])
    buried = {i['structure']: i for i in json.loads(args.buried_gaps.read_bytes())['instances']}
    small = buried['relics:small_colossus']['gaps']
    selections = [('world_tree', 'Wurzel am Bodenniveau', root['raw_position']),
                  ('ruined_tower', 'Vergrabene Mauerunterseite', buried['relics:ruined_tower']['gaps'][0]['raw_position']),
                  ('small_colossus', 'Wasser unter dem kleinen Colossus',
                   next(g['raw_position'] for g in small if g['below'] == 'minecraft:water'))]
    canvas = Image.new('RGB', (1500, 1160), '#f1ede3')
    draw = ImageDraw.Draw(canvas)
    font = lambda n: ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', n)
    draw.text((24, 12), 'BODENKONTAKTE / DIESELBEN NATÜRLICHEN STANDORTE', font=font(28), fill='#28392d')
    draw.text((24, 55), 'Links: Alpha 4.6 | Rechts: Kontaktkorrektur | Blockgenaue Schnitte aus gespeicherten Welten', font=font(20), fill='#28392d')
    draw.text((24, 88), 'Dunkel: Modell | Braun: Erde | Orange: zusätzliche geschützte Stützen | Grün: Gelände | Blau: Wasser', font=font(18), fill='#28392d')
    records = []
    for row, (name, title, target) in enumerate(selections):
        x, y, z = target
        y0 = 140 + row * 325
        draw.text((24, y0), f'{title} / {name} / raw {target}', font=font(22), fill='#28392d')
        record = {'id': name, 'raw_position': target, 'world_positions': [], 'substrate': []}
        for column, (report, world) in enumerate(zip(reports, worlds)):
            contract = next(c for c in report['asset_selection']['structures'] if c['id'] == name)
            instance = next(i for i in report['world_blocks']['instances'] if i['structure'] == 'relics:' + name)
            data = (ROOT / contract['source']).read_bytes()
            assert hashlib.sha256(data).hexdigest() == contract['sha256']
            nbt = decode_nbt(data)
            blocks = {tuple(b['pos']): nbt['palette'][b['state']]['Name'] for b in nbt['blocks']}
            def position(yy, zz):
                return transform((x + TOE_RADIUS, yy + padding(contract), zz + TOE_RADIUS),
                                 instance['rotation'], instance['origin'])
            point = position(y, z)
            record['world_positions'].append(list(point))
            record['substrate'].append(world.block(*position(y - 1, z))['Name'])
            for dz in range(-25, 26):
                for dy in range(-15, 8):
                    p = position(y + dy, z + dz)
                    actual = world.block(*p)
                    color = '#dce7ec'
                    if actual is None:
                        color = '#d796bc'
                    elif actual['Name'] == 'minecraft:water':
                        color = '#518dc0'
                    elif actual['Name'] not in AIR_NAMES:
                        raw = x, y + dy, z + dz
                        if raw in blocks:
                            color = '#98724c' if blocks[raw] in SOILS else '#303a37'
                        elif protected_cell(world.chunk(p[0] // 16, p[2] // 16), p):
                            color = '#e1a44d'
                        else:
                            color = '#708b60'
                    px, py = 24 + column * 744 + (dz + 25) * 13, y0 + 36 + (7 - dy) * 11
                    draw.rectangle((px, py, px + 12, py + 10), fill=color)
            px, py = 24 + column * 744 + 25 * 13, y0 + 36 + 8 * 11
            draw.rectangle((px - 2, py - 2, px + 14, py + 12), outline='#ec3434', width=2)
        assert record['world_positions'][0] == record['world_positions'][1], 'Comparisons must share the exact world location'
        assert record['substrate'][0] in AIR_NAMES | {'minecraft:water', 'minecraft:lava'}
        assert record['substrate'][1] not in AIR_NAMES | {'minecraft:water', 'minecraft:lava'}
        records.append(record)
    draw.text((24, 1120), 'Rot: geprüfter Anschlussblock. Diagnoseansicht aus Weltdaten; keine neuen Minecraft-Client-Fotos.', font=font(19), fill='#28392d')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.output)
    evidence = {'scope': 'Read-only, same-position saved-world cross sections', 'records': records,
                'reports': [{'path': p.as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                            for p in (args.before, args.after)], 'read_errors': [w.read_errors for w in worlds]}
    assert not any(evidence['read_errors'])
    args.output.with_suffix('.json').write_text(json.dumps(evidence, indent=2) + '\n', encoding='utf-8')
    print(args.output)


if __name__ == '__main__':
    main()
