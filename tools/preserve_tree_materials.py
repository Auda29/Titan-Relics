"""Stabilize wood/wood ray-hit ties against an accepted tree during ground-only edits."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

from colossus_materials import encode_schematic
from schem_to_nbt import read_schematic

ROOT=Path(__file__).resolve().parents[1]


def preserve(blocks,baseline,terrain,wood):
    old={p:s for p,s in baseline.items() if s not in terrain}
    new={p:s for p,s in blocks.items() if s not in terrain}
    if old.keys()!=new.keys():raise ValueError('Ground revision changed non-terrain geometry')
    edits={p:s for p,s in old.items() if new[p]!=s}
    if any(s not in wood or new[p] not in wood for p,s in edits.items()):
        raise ValueError('Ground revision changed a material outside wood/wood overlap ties')
    return blocks|edits,len(edits)


def main(config_path):
    config=json.loads(config_path.read_text());output=ROOT/config['output']
    source=ROOT/config['preserve_tree_palette_from']
    original=source.read_bytes();digest=hashlib.sha256(original).hexdigest()
    verification=json.loads((source.parent/'verification.json').read_text())
    if digest!=verification['schematic_sha256']:raise ValueError('Accepted baseline schematic changed')
    old_size,old,old_version,_=read_schematic(original)
    raw=output.read_bytes();size,blocks,version,offset=read_schematic(raw)
    if (size,version)!=(old_size,old_version):raise ValueError('Ground revision changed dimensions/version')
    terrain={config['materials'][k] for k in ('terrain_top','terrain_patch','terrain_fill')}
    wood={config['materials'][k] for k in ('wood','bark','cut')}
    result,count=preserve(blocks,old,terrain,wood)
    encoded=encode_schematic(result,size,version,offset)
    report_path=output.with_suffix('.ots.json');report=json.loads(report_path.read_text())
    report['accepted_tree_materials']={'source':source.relative_to(ROOT).as_posix(),'sha256':digest,
        'upstream_schematic_sha256':hashlib.sha256(raw).hexdigest(),'wood_overlap_ties_restored':count}
    report['schematic_sha256']=hashlib.sha256(encoded).hexdigest();report['blocks']=dict(Counter(result.values()))
    output.write_bytes(encoded);report_path.write_text(json.dumps(report,indent=2)+'\n')
    print(f'Accepted tree: {count} wood/wood overlap ties restored; non-terrain positions identical')


if __name__=='__main__':main(Path(sys.argv[1]))
