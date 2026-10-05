"""Build versioned visual relic candidates through Blender, ObjToSchematic and NBT."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
ASSETS={'tower':('ruined-tower','ruined-tower-v2'),
        'tree':('world-tree','world-tree-v2'),
        'small-colossus':('colossus','small-colossus-v2')}
EXTRA_ASSETS={'small-colossus-v3':('colossus','small-colossus-v3'),
              'small-colossus-v4':('colossus','small-colossus-v4'),
              'small-colossus-v5':('colossus','small-colossus-v5'),
              'world-tree-v3':('world-tree','world-tree-v3'),
              'ruined-tower-v3':('ruined-tower','ruined-tower-v3'),
              'world-tree-v4':('world-tree','world-tree-v4'),
              'small-colossus-v6':('colossus','small-colossus-v6'),
              'ruined-tower-v4':('ruined-tower','ruined-tower-v4')}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('asset',choices=[*ASSETS,*EXTRA_ASSETS,'all'],help='all reproduces the original three V2 assets')
    parser.add_argument('--blender',default=r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe')
    parser.add_argument('--threads',type=int,default=8)
    parser.add_argument('--skip-model',action='store_true')
    parser.add_argument('--review-only',action='store_true')
    args=parser.parse_args()
    def run(command):
        print('RUN:',subprocess.list2cmdline(list(map(str,command))),flush=True)
        subprocess.run(list(map(str,command)),cwd=ROOT,check=True)
    blender=[args.blender,'--background','--threads',str(args.threads),'--python-exit-code','1','--python']
    for key in ASSETS if args.asset=='all' else [args.asset]:
        relic,stem=(ASSETS|EXTRA_ASSETS)[key];config=Path('relics')/relic/'design'/f'{stem}.json'
        settings=json.loads((ROOT/config).read_text());schem=Path(settings['output'])
        inspector=settings.get('inspector','tools/inspect_relic_v2.py')
        if not args.review_only:
            if not args.skip_model:run([*blender,'tools/create_'+stem.replace('-','_')+'.py'])
            run(['node','--max-old-space-size=8192','tools/obj_to_schem.cjs',config])
            run([sys.executable,'tools/schem_to_nbt.py',schem,schem.with_suffix('.nbt'),'--air','omit','--tile-size','32'])
        run([sys.executable,inspector,config])
        if settings.get('preview_atlas'):run([sys.executable,'tools/prepare_foliage_preview.py'])
        run([*blender,'tools/render_ots_preview.py','--','--config',config])
        run([sys.executable,inspector,config,'--review'])
        run([*blender,'tools/render_new_relic_v1_details.py','--','--config',config])
        run([sys.executable,'tools/review_new_relic_v1_details.py',config])
        if settings.get('comparison_review'):
            run([sys.executable,settings['comparison_review']])


if __name__=='__main__':main()
