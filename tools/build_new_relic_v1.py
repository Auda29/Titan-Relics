"""Reproduce each new V1 through Blender, pinned ObjToSchematic, NBT and review."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
ASSETS={
    'tower':('ruined-tower','ruined-tower-v1','create_ruined_tower_v1.py'),
    'tree':('world-tree','world-tree-v1','create_world_tree_v1.py'),
    'small-colossus':('colossus','small-colossus-v1','create_small_colossus_v1.py'),
    'skull-2':('titan-skull','titan-skull-2-v1','create_titan_skull_2_v1.py'),
}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('asset',choices=[*ASSETS,'all'])
    parser.add_argument('--blender',default=r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe')
    parser.add_argument('--skip-model',action='store_true',help='Export existing V1 source OBJ without regenerating geometry')
    parser.add_argument('--details-only',action='store_true',help='Render and assemble only the actual-NBT close views')
    parser.add_argument('--threads',type=int,default=8)
    args=parser.parse_args()
    def run(command):
        print('RUN:',subprocess.list2cmdline(list(map(str,command))),flush=True)
        subprocess.run(list(map(str,command)),cwd=ROOT,check=True)
    blender=[args.blender,'--background','--threads',str(args.threads),'--python-exit-code','1','--python']
    for name in ASSETS if args.asset=='all' else [args.asset]:
        relic,stem,generator=ASSETS[name]
        config=Path('relics')/relic/'design'/f'{stem}.json'
        settings=json.loads((ROOT/config).read_text());schem=Path(settings['output'])
        if args.details_only:
            run([*blender,'tools/render_new_relic_v1_details.py','--','--config',config])
            run([sys.executable,'tools/review_new_relic_v1_details.py',config])
            continue
        if not args.skip_model:run([*blender,'tools/'+generator])
        run(['node','--max-old-space-size=8192','tools/obj_to_schem.cjs',config])
        run([sys.executable,'tools/schem_to_nbt.py',schem,schem.with_suffix('.nbt'),'--air','omit','--tile-size','32'])
        if settings.get('preview_atlas'):
            run([sys.executable,'tools/prepare_foliage_preview.py'])
        run([*blender,'tools/render_ots_preview.py','--','--config',config])
        run([sys.executable,'tools/inspect_new_relic_v1.py',config,'--review'])
        run([*blender,'tools/render_new_relic_v1_details.py','--','--config',config])
        run([sys.executable,'tools/review_new_relic_v1_details.py',config])


if __name__=='__main__':main()
