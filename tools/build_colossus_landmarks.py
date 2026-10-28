"""Colossus V7, a local derivative of the released V6 NBT and sidecars."""
import copy
import json
from pathlib import Path
from build_gameplay_interiors import Builder, ROOT, ASSETS, STONE, WORN, TRIM, NATIVE, digest
from inspect_ots_result import read_structure

STEM='colossus-v7-landmarks'
V6='colossus-v6-interiors'
BASE=(ROOT/ASSETS['colossus']['source']).parent.parent
OLD=BASE/V6
OUT=BASE/STEM

def build():
    b=Builder('colossus')
    v6path=OLD/(V6+'.nbt')
    side=json.loads((OLD/(V6+'.gameplay.json')).read_text())
    assert digest(v6path)==side['source_sha256']=='4c65e4cc8fd57dbccacf765241df70951a95e65e886b4ac4f17d9ebaf96c3b99'
    root,blocks=read_structure(v6path)
    b.root=root; b.old=dict(blocks); b.blocks=dict(blocks)
    b.markers=copy.deepcopy(side['markers']); b.regions=copy.deepcopy(side['regions'])
    design=json.loads((OLD/(V6+'.design.json')).read_text())
    b.paths=copy.deepcopy(design['paths']); b.evidence=copy.deepcopy(design['evidence'])
    b.stem=STEM; b.out=OUT
    markers={m['role']:m for m in b.markers}
    def move(role,pos):
        m=markers[role]; old=tuple(m['pos']); state=m.get('expected_block')
        if state: assert b.blocks.get(old)==state; b.put(old,None)
        m['pos']=list(pos)
        if state: b.put(pos,state)
    # Arm niche: open to the south and sky; no block above the chest.
    b.group='arm-find-frame'
    b.box((108,77,69),(112,77,72),STONE)
    b.box((108,78,69),(112,81,69),WORN)
    for x in (108,112):
        b.box((x,78,70),(x,83,70),TRIM)
        b.put((x,84,70),'minecraft:chiseled_deepslate')
    b.box((109,82,69),(111,82,69),STONE)
    b.region('arm_clearance',(109,78,70),(112,82,73))
    # Open guard frame, with the spawner exposed on its deck in the room centre.
    b.group='central-guard-frame'
    move('colossus_trial_spawner',(94,169,183))
    move('colossus_golem_spawn',(94,169,190))
    for x in (91,97):
        for z in (180,186):
            b.box((x,169,z),(x,171,z),TRIM)
            b.put((x,172,z),'minecraft:chiseled_deepslate')
    b.box((92,172,180),(96,172,180),WORN)
    for x in (92,93,95,96): b.put((x,172,186),WORN)
    for x in (92,93,95,96): b.put((x,168,183),'minecraft:polished_andesite')
    # Replace the central crew station's existing instrument with the vault.
    b.group='central-vault-console'
    b.put((94,170,164),None); b.put((94,171,164),None)
    move('colossus_vault',(94,169,164))
    b.put((93,171,164),'minecraft:chiseled_deepslate')
    b.put((95,171,164),'minecraft:chiseled_deepslate')
    b.region('cockpit_clearance',(93,169,164),(95,173,165))
    b.evidence['v7_parent']={'nbt':v6path.relative_to(ROOT).as_posix(),'sha256':digest(v6path)}
    b.evidence['views']=[{'label':'Arm find frame, open top and approach','lo':[104,74,65],'hi':[117,85,78]},
        {'label':'Central guard frame, trial spawner placeholder','lo':[88,167,176],'hi':[101,174,190]},
        {'label':'Central crew station and vault placeholder','lo':[89,167,161],'hi':[100,174,172]}]
    b.evidence['arm_route_note']='Additional bounded arm_clearance covers the find and lid space; source solids are excluded by integration.'
    b.evidence['feedback_revision']='V7 local landmarks, native placeholders; gameplay integration pending'
    return b

if __name__=='__main__':
    build().save()
    path=OUT/(STEM+'.design.json')
    design=json.loads(path.read_text())
    design['change_reference']='V6 NBT specified by evidence.v7_parent; baseline retains original catalog provenance'
    path.write_text(json.dumps(design,indent=2)+'\n',encoding='utf-8',newline='\n')


