"""Check exact V4 exports, plated body mass, optical/grille features and connected pincers."""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path

import inspect_ots_result as base
from inspect_ots_result import require,read_structure

ROOT=Path(__file__).resolve().parents[1]


def check(config_path,review=False):
    config=json.loads(config_path.read_text());output=ROOT/config['output'];out=output.parent;stem=output.stem
    base.CONFIG,base.OUT,base.STEM=config,out,stem;summary=base.check()
    meta=json.loads(output.with_suffix('.design.json').read_text());features=meta['revision_v4']
    root,blocks=read_structure(output.with_suffix('.nbt'))
    require(hashlib.sha256((out/f'{stem}-source.blend').read_bytes()).hexdigest()==meta['source_blend_sha256'],'Source model changed')
    require(config['reference']==meta['reference']=='https://www.instagram.com/reel/Da-s0zqi7OQ/','Wrong primary reference')
    for key in ('revision_v5','revision_v6'):
        if key not in meta:continue
        revision=meta[key]
        require(hashlib.sha256((ROOT/revision['source']).read_bytes()).hexdigest()==revision['source_sha256'],
                'Preserved comparison source changed')
    require(root['size'][1]==config['height'],'Incorrect total height')
    require(all(.72<=v/t<=1.3 for v,t in zip(root['size'],config['planned_site_size'])),'Unexpected footprint')
    low,high=meta['source_bounds_blender'];scale=meta['blocks_per_source_unit']
    def local(p):return (round((p[0]-low[0])*scale),round((p[1]-low[2])*scale),round((p[2]+high[1])*scale))
    def source(p):return (p[0]/scale+low[0],p[1]/scale+low[2],p[2]/scale-high[1])
    def around(p,r):return [(p[0]+x,p[1]+y,p[2]+z) for x in range(-r,r+1) for y in range(-r,r+1) for z in range(-r,r+1)]
    for p in features['solid_core_probes_source']:
        require(all(q in blocks for q in around(local(p),1)),f'Body/head core is hollow at {p}')
    soil={config['materials'][key] for key in ('terrain_top','terrain_patch','terrain_fill','moss','growth')}
    structure={p for p,s in blocks.items() if s not in soil}
    start=local(features['body_connection_source']);require(start in structure,'Missing central body core')
    seen={start};queue=deque([start])
    while queue:
        x,y,z=queue.popleft()
        for p in ((x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)):
            if p in structure and p not in seen:seen.add(p);queue.append(p)
    require(any(p in seen for p in around(local(features['head_connection_source']),2)),'Head is disconnected')
    require(any(p[1]<meta['ground_level_nbt_approx'] for p in seen),'Body has no buried structural connection')
    optics=features['head_optics'];require(len(optics)==6,'Expected six head optics')
    optical_counts=[]
    for optic in optics+[port for hand in features['pincers'] for port in hand['ports']]:
        count=sum(blocks.get(p)==config['materials']['dark'] for p in around(local(optic['dark_probe_source']),3))
        require(count>=3,f'Optical lens missing: {optic["name"]}')
        optical_counts.append({'name':optic['name'],'nearby_dark_blocks':count})
    rib_counts=[]
    for p in features['grille_rib_probes_source']:
        count=sum(blocks.get(q)==config['materials']['joint'] for q in around(local(p),1))
        require(count>=2,f'Missing grille rib near {p}');rib_counts.append(count)
    for hand in features['pincers']:
        require(any(p in seen for p in around(local(hand['center_source']),2)),f'Disconnected pincer: {hand["name"]}')
        for tip in hand['tine_tips_source']:
            require(any(p in seen and blocks.get(p)==config['materials']['claw'] for p in around(local(tip),2)),
                    f'Missing or disconnected blade tip: {hand["name"]}, {tip}')
    points=[source(p) for p in structure];widths=[]
    for y in features['continuous_body_source_y']:
        band=[x for x,py,z in points if abs(py-y)<1.5 and abs(x)<29 and -15<=z<=28]
        require(band,'Missing central body band');width=max(band)-min(band)+1/scale
        require(width>=40,f'Torso is too narrow at source Y{y}: {width}')
        widths.append({'source_y':y,'width_source_units':width})
    report=json.loads(output.with_suffix('.ots.json').read_text())
    require(report['filled_voxels']>10000,'Closed plated masses were not filled')
    if 'revision_v6' in meta:
        for point in meta['revision_v6']['plate_probes_source']:
            require(any(p in seen for p in around(local(point),2)),f'Disconnected armour plate near {point}')
    revision_key=next(key for key in ('revision_v6','revision_v5','revision_v4') if key in meta)
    summary[revision_key]={'reference':config['reference'],'source_blend_sha256':meta['source_blend_sha256'],
                            'ground_level':meta['ground_level_nbt_approx'],'visible_layers':root['size'][1]-meta['ground_level_nbt_approx'],
                            'head_and_pincers_connected_to_buried_body':True,'six_head_optics':True,
                            'optical_probes':optical_counts,'grille_rib_neighborhoods':rib_counts,
                            'solid_core_3x3x3_probes':len(features['solid_core_probes_source']),
                            'continuous_body_widths':widths,'filled_voxels':report['filled_voxels'],
                             'copper_blocks':sum('copper' in s for s in blocks.values())}
    if 'revision_v6' in meta:
        summary[revision_key]['connected_plate_probes']=len(meta['revision_v6']['plate_probes_source'])
    (out/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    if review:base.contact_sheet(summary)
    print(json.dumps(summary[revision_key],indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('config',type=Path);parser.add_argument('--review',action='store_true')
    args=parser.parse_args();check(args.config,args.review)
