"""Read actual NBT for close inspection and an exposed tree branch/roots view."""
import argparse
import json
from pathlib import Path
import sys

import bpy

sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_ots_preview as renderer

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--config',type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    renderer.CONFIG=json.loads(args.config.read_text());output=ROOT/renderer.CONFIG['output']
    renderer.OUT,renderer.STEM=output.parent,output.stem
    renderer.ATLAS=ROOT/renderer.CONFIG.get('preview_atlas',str(Path(renderer.CONFIG['repository'])/'res/atlases'))
    metadata=json.loads(output.with_suffix('.design.json').read_text());family=metadata['new_relic_v1']['family']
    low,high=metadata['source_bounds_blender'];scale=metadata['blocks_per_source_unit']
    root=renderer.decode_nbt(output.with_suffix('.nbt').read_bytes())
    palette=[p['Name'] for p in root['palette']]
    states={tuple(b['pos']):palette[b['state']] for b in root['blocks']}
    def source(p):return (p[0]/scale+low[0],p[1]/scale+low[2],p[2]/scale-high[1])
    if family=='tree':
        views=[('Root arches / actual blocks',lambda p:source(p)[1]<48,(130,210,125)),
               ('Woody skeleton / leaves hidden for inspection',lambda p:'leaves' not in states[tuple(p)],(160,250,100))]
    elif family=='small-colossus':
        views=[('Right palm and curled fingers',lambda p:source(p)[0]>27 and source(p)[2]>17,(120,-240,170)),
               ('Compact body / rear breach',lambda p:source(p)[0]<29,(110,-250,115))]
    elif family=='skull-2':
        views=[('Face and open jaw',lambda p:source(p)[1]<69,(45,290,75)),
               ('Sword entry and crossguard',lambda p:source(p)[1]>49,(80,250,105))]
    else:
        views=[('Ground joins and lower threshold',lambda p:source(p)[1]<65,(130,230,100)),
               ('Broken crown and sky slots',lambda p:source(p)[1]>105,(120,230,120))]
    for index,(label,predicate,direction) in enumerate(views):
        bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
        renderer.blocks_from_nbt(predicate=predicate)
        center,corners=renderer.stage();renderer.render(f'11-detail-{index+1}.png',center,corners,direction)
    (renderer.OUT/'detail-views.json').write_text(json.dumps([
        {'image':f'11-detail-{i+1}.png','label':label} for i,(label,_,_) in enumerate(views)],indent=2)+'\n')


if __name__=='__main__':main()
