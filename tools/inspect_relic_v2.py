"""Block-exact export checks and feature probes for the October 4 visual revisions."""
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
    base.CONFIG,base.OUT,base.STEM=config,out,stem
    summary=base.check()
    meta=json.loads(output.with_suffix('.design.json').read_text());feature=meta['new_relic_v1']
    root,blocks=read_structure(output.with_suffix('.nbt'))
    require(hashlib.sha256((out/f'{stem}-source.blend').read_bytes()).hexdigest()==meta['source_blend_sha256'],'Source model changed')
    low,high=meta['source_bounds_blender'];scale=meta['blocks_per_source_unit']
    def local(p):return (round((p[0]-low[0])*scale),round((p[1]-low[2])*scale),round((p[2]+high[1])*scale))
    def around(p,r):return [(p[0]+x,p[1]+y,p[2]+z) for x in range(-r,r+1) for y in range(-r,r+1) for z in range(-r,r+1)]
    for point in feature['void_probes_source']:
        require(not any(p in blocks for p in around(local(point),1)),f'Blocked cavity at {point}')
    for point in feature['solid_probes_source']:
        require(sum(p in blocks for p in around(local(point),2))>=5,f'Missing structure at {point}')
    require(root['size'][1]==config['height'],'Incorrect export height')
    require(all(.72<=v/t<=1.3 for v,t in zip(root['size'],config['planned_site_size'])),'Unexpected footprint')
    checks={'family':feature['family'],'ground_level':meta['ground_level_nbt_approx'],
            'void_probes':len(feature['void_probes_source']),'structural_probes':len(feature['solid_probes_source']),
            'source_blend_sha256':meta['source_blend_sha256']}
    if 'revision_v4' in meta:
        parent=meta['revision_v4']
        require(hashlib.sha256((ROOT/parent['source']).read_bytes()).hexdigest()==parent['source_sha256'],
                'Preserved V3 comparison source changed')
    if 'revision_v5' in meta:
        parent=meta['revision_v5']
        require(hashlib.sha256((ROOT/parent['source']).read_bytes()).hexdigest()==parent['source_sha256'],
                'Preserved V4 comparison source changed')
    if feature['family']=='tower':
        revision=meta['revision_v2']
        require(hashlib.sha256((ROOT/revision['source']).read_bytes()).hexdigest()==revision['source_sha256'],'V1 source changed')
        visible=root['size'][1]-meta['ground_level_nbt_approx']
        require(visible==220,'Tower must have 220 visible block layers')
        require(meta['ground_level_nbt_approx']==12,'Foundation depth changed')
        checks['visible_height']=visible;checks['source_preserved']=True
        if 'revision_v3' in meta:
            parent=meta['revision_v3']
            require(hashlib.sha256((ROOT/parent['source']).read_bytes()).hexdigest()==parent['source_sha256'],'V2 source changed')
            checks.update(partial_storeys=parent['partial_storeys'],broken_stair_flights=parent['broken_stair_flights'])
    if feature['family']=='tree':
        leaves={state for state in blocks.values() if 'leaves' in state}
        require(leaves and all('persistent=true' in state for state in leaves),'Leaves can decay')
        require(all(p in blocks for q in feature['solid_probes_source'] for p in around(local(q),1)), 'Trunk sample not solid')
        checks['persistent_leaf_states']=sorted(leaves)
        checks['terminal_boughs']=meta['revision_v2']['terminal_boughs']
        require(checks['terminal_boughs']>=80,'Fine crown branching is missing')
        wood={config['materials'][key] for key in ('wood','bark','cut')}
        for point in feature['branch_tip_probes_source']:
            require(any(blocks.get(p) in wood for p in around(local(point),2)),f'Missing woody branch tip near {point}')
        checks['exported_branch_tip_probes']=len(feature['branch_tip_probes_source'])
        if 'revision_v4' in meta:
            converter=json.loads(output.with_suffix('.ots.json').read_text())
            priority=converter.get('structural_material_priority',{})
            require(priority.get('materials')==config.get('structural_material_priority')==['wood','bark','cut'],
                    'Tree structural material priority was not used by the converter')
            checks['structural_overlap_cells_preserved']=priority['replaced_overlap_cells']
            woody={p for p,s in blocks.items() if s in wood}
            start=next(p for p in around(local(feature['solid_probes_source'][0]),1) if p in woody)
            seen={start};queue=deque([start])
            while queue:
                x,y,z=queue.popleft()
                for p in ((x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)):
                    if p in woody and p not in seen:seen.add(p);queue.append(p)
            for point in meta['revision_v4']['fork_probes_source']+feature['branch_tip_probes_source']:
                require(any(p in seen for p in around(local(point),2)),f'Woody fork detached from trunk at {point}')
            checks['trunk_connected_woody_probes']=len(meta['revision_v4']['fork_probes_source'])+len(feature['branch_tip_probes_source'])
        if 'revision_v4_1' in meta:
            parent=meta['revision_v4_1'];source=ROOT/parent['source']
            require(hashlib.sha256(source.read_bytes()).hexdigest()==parent['source_sha256'],'Accepted tree source changed')
            old_root,old=read_structure(source.with_name('world-tree-v4.nbt'))
            require(root['size']==old_root['size'],'Ground revision changed tree dimensions')
            terrain={config['materials'][key] for key in ('terrain_top','terrain_patch','terrain_fill')}
            require({p:s for p,s in blocks.items() if s not in terrain}=={p:s for p,s in old.items() if s not in terrain},
                    'Ground-only revision changed accepted wood, foliage or root details')
            checks['accepted_non_terrain_blocks_identical']=True
    if feature['family']=='small-colossus':
        hand=feature['hand']
        require(abs(hand['basis_determinant']-1)<1e-5 and hand['palmar_normal_source'][1]>.99,'Incorrect right-hand orientation')
        for tip in hand['finger_tips_source']:
            require(sum(p in blocks for p in around(local(tip),2))>=3,'Missing finger')
        # Prove a face-connected structural path between head/collar and buried body.
        structure={p for p,s in blocks.items() if s not in {config['materials'][k] for k in ('moss','growth','terrain_top','terrain_patch','terrain_fill')}}
        revision=meta.get('revision_v3',{})
        collar=revision.get('collar_probe_source',(-5,47,2))
        start=next((p for p in around(local(collar),3) if p in structure),None)
        require(start is not None,'Missing collar')
        seen={start};queue=deque([start])
        while queue:
            x,y,z=queue.popleft()
            for p in ((x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)):
                if p in structure and p not in seen:seen.add(p);queue.append(p)
        require(any(y<meta['ground_level_nbt_approx'] for x,y,z in seen),'Head is disconnected from buried body')
        checks['collar_to_buried_body_connected']=True
        checks['copper_blocks']=sum('copper' in s for s in blocks.values())
        if revision:
            require(any(p in seen for p in around(local(revision['head_connection_probe_source']),2)),
                    'Mask is disconnected from the collar/body')
            checks['mask_to_body_connected']=True
            for wrist in (feature['hand']['wrist_source'],(-45,5,-19)):
                require(any(p in seen for p in around(local(wrist),2)),f'Attached arm is disconnected at {wrist}')
            checks['both_attached_arms_connected']=True
            def source(p):return (p[0]/scale+low[0],p[1]/scale+low[2],p[2]/scale-high[1])
            points=[source(p) for p in structure]
            # Undo the authored list before measuring the central torso, excluding the arms.
            straight=[(x-revision['sideways_shear']*max(0,y-8),y,z-revision['forward_shear']*max(0,y-8)) for x,y,z in points]
            widths=[]
            for key in ('waist_band_source_y','chest_band_source_y'):
                lo,hi=revision[key]
                band=[x for x,y,z in straight if lo<=y<=hi and abs(x)<17 and -12<=z<=13]
                require(band,f'Missing torso band: {key}');widths.append(max(band)-min(band)+1/scale)
            ratio=widths[0]/widths[1]
            require(ratio<.65,f'Waist is not visibly narrower than the chest: {ratio}')
            mask=[p for p in points if p[1]>55]
            mask_size=[max(p[i] for p in mask)-min(p[i] for p in mask)+1/scale for i in range(3)]
            require(mask_size[1]/mask_size[0]>1.15,'Mask does not read as elongated')
            checks.update(waist_to_chest_width_ratio=ratio,mask_bounds_source_units=mask_size,
                          mask_height_to_width_ratio=mask_size[1]/mask_size[0])
    summary[next(key for key in ('revision_v5','revision_v4_1','revision_v4','revision_v3','revision_v2') if key in meta)]=checks
    (out/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    if review:base.contact_sheet(summary)
    print(json.dumps(checks,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('config',type=Path);parser.add_argument('--review',action='store_true')
    args=parser.parse_args();check(args.config,args.review)
