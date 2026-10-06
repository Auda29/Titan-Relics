"""Check the new V1s against independent conversion, palette and geometry evidence."""
import argparse
import hashlib
import json
from pathlib import Path

import inspect_ots_result as base
from inspect_ots_result import read_structure,require

ROOT=Path(__file__).resolve().parents[1]


def check(config_path,review=False):
    config=json.loads(config_path.read_text());output=ROOT/config['output'];out=output.parent;stem=output.stem
    base.CONFIG,base.OUT,base.STEM=config,out,stem
    summary=base.check()
    design=json.loads((out/f'{stem}.design.json').read_text());features=design['new_relic_v1']
    root,blocks=read_structure(out/f'{stem}.nbt')
    require(hashlib.sha256((out/f'{stem}-source.blend').read_bytes()).hexdigest()==design['source_blend_sha256'],'Source blend changed')
    low,high=design['source_bounds_blender'];scale=design['blocks_per_source_unit']
    def local(p):return (round((p[0]-low[0])*scale),round((p[1]-low[2])*scale),round((p[2]+high[1])*scale))
    def neighbors(p,r):return [(p[0]+x,p[1]+y,p[2]+z) for x in range(-r,r+1) for y in range(-r,r+1) for z in range(-r,r+1)]
    cavities=[]
    for point in features['void_probes_source']:
        p=local(point);occupied=[q for q in neighbors(p,1) if q in blocks]
        require(not occupied,f'Blocked cavity at source {point}: {len(occupied)} blocks')
        cavities.append(p)
    supports=[]
    for point in features['solid_probes_source']:
        p=local(point);count=sum(q in blocks for q in neighbors(p,2))
        require(count>=5,f'Missing structural member near source {point}')
        supports.append({'source':point,'local':p,'nearby_blocks':count})
    planned=config['planned_site_size']
    require(root['size'][1]==config['height'],'Height differs from the chosen V1 export')
    require(all(.72<=actual/target<=1.3 for actual,target in zip(root['size'],planned)),'Envelope deviates too far from working brief')
    checks={'family':features['family'],'planned_size':planned,'actual_size':root['size'],
            'void_probes_local':cavities,'structural_samples':supports,'ground_level':design['ground_level_nbt_approx']}
    if features['family']=='tree':
        leaves={s for s in blocks.values() if 'leaves' in s}
        require(leaves and all('persistent=true' in s for s in leaves),'Leaves would decay')
        require(all(q in blocks for point in features['solid_probes_source'] for q in neighbors(local(point),1)),
                'Trunk contains holes at solid-volume probes')
        require(not any('copper' in s or 'iron' in s for s in blocks.values()),'Unexpected valuable metal in tree')
        checks['persistent_leaf_states']=sorted(leaves);checks['solid_trunk_3x3x3_probes']=3
    if features['family']=='small-colossus':
        require(hashlib.sha256((ROOT/design['archive_source']).read_bytes()).hexdigest()==design['archive_source_sha256'],'Archive changed')
        hand=features['hand']
        require(abs(hand['basis_determinant']-1)<1e-5 and hand['palmar_normal_source'][1]>.99,'Hand chirality/orientation changed')
        for tip in hand['finger_tips_source']:
            require(sum(p in blocks for p in neighbors(local(tip),2))>=3,'Finger tip lost')
        checks['preserved_archive_meshes']=len(design['preserved_archive_meshes']);checks['right_palm_up']=True
    if features['family']=='skull-2':
        if 'revision_v2' in design:
            parent=design['revision_v2']
            require(hashlib.sha256((ROOT/parent['source']).read_bytes()).hexdigest()==parent['source_sha256'],
                    'Preserved Skull 2 V1 source changed')
            # At the posterior center, the rounded base must now reach nominal
            # ground instead of remaining suspended above an earth hummock.
            posterior=[y-design['ground_level_nbt_approx'] for (x,y,z),s in blocks.items()
                       if s in {'minecraft:bone_block','minecraft:calcite','minecraft:dripstone_block','minecraft:moss_block'}
                       and abs(x/scale+low[0])<12 and 25<z/scale-high[1]<42]
            require(posterior and min(posterior)<=0,'Posterior skull still floats above nominal ground')
            checks['posterior_lowest_above_ground']=min(posterior)
        require(not features['crown_included'] and not features['spine_included'],'Wrong skull design family')
        sword=features['sword'];origin,axis=sword['entry_source'],sword['axis_source']
        for t in (-14,10,32,58):
            p=local([a+t*b for a,b in zip(origin,axis)])
            require(sum(q in blocks for q in neighbors(p,3))>10,f'Sword section missing at t={t}')
        require(not any('iron' in s or 'diamond' in s or 'gold' in s for s in blocks.values()),'Bulk valuable sword material')
        checks['embedded_sword_sections']=4
        weapon={p for p,s in blocks.items() if s in {'minecraft:tuff','minecraft:andesite','minecraft:polished_deepslate','minecraft:gray_terracotta'}}
        bone={p for p,s in blocks.items() if s in {'minecraft:bone_block','minecraft:calcite','minecraft:dripstone_block'}}
        contacts=sum(q in bone for x,y,z in weapon for q in ((x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)))
        require(contacts>=20,'Sword lacks substantial face-contact with surviving cranial bone')
        checks['sword_bone_contact_faces']=contacts
    checks['source_blend_sha256']=design['source_blend_sha256']
    summary['new_relic_v1']=checks
    (out/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    if review:base.contact_sheet(summary)
    print(json.dumps(checks,indent=2));return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('config',type=Path);parser.add_argument('--review',action='store_true')
    args=parser.parse_args();check(args.config,args.review)
