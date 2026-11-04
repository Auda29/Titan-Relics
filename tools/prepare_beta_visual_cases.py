"""Generate labelled camera commands from the tested JAR's own integration manifest."""
import argparse,gzip,json,zipfile,math
from pathlib import Path
from smoke_server import read_nbt

def camera(blocks,target):
    """Find an unobstructed eye position in the authored template, without editing it."""
    tx,ty,tz=target
    empty=lambda p: blocks.get(tuple(math.floor(v) for v in p),'minecraft:air') in ('minecraft:air','minecraft:cave_air','minecraft:void_air')
    candidates=[]
    for dy in (2,3,4,6,8,10,14):
        for dx,dz in ((0,-4),(0,4),(-4,0),(4,0),(-4,-4),(4,4),(-8,0),(8,0),(0,-8),(0,8)):
            eye=(tx+.5+dx,ty+.5+dy,tz+.5+dz)
            if not empty(eye) or not empty((eye[0],eye[1]-1,eye[2])):continue
            aim=(tx+.5,ty+.5,tz+.5)
            ray=[tuple(eye[k]+(aim[k]-eye[k])*t/40 for k in range(3)) for t in range(40)]
            clear=all(tuple(math.floor(v) for v in p)==target or empty(p) for p in ray)
            if clear:candidates.append((dx*dx+dz*dz+dy*dy,eye,aim))
    if not candidates:return None
    _,eye,aim=min(candidates)
    return eye,aim

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--artifact',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--minecraft',required=True);a=ap.parse_args()
    scenes=[]
    with zipfile.ZipFile(a.artifact) as z:
        manifest=json.loads(z.read('relics.gameplay.tree_skull.integration.json'))
        for n,asset in enumerate(x for x in manifest['structures'] if x['id'] in ['colossus','obelisk','small_colossus','world_tree','ruined_tower','titan_skull','titan_skull_2']):
            name=asset['worldgen_template']['path'];d=read_nbt(gzip.decompress(z.read('data/relics/structure/'+name)));sx,sy,sz=d['size'];x=n*1024;y=80
            cx=x+sx/2;cy=y+sy/2;cz=sz/2;distance=max(sx,sy,sz)*0.65
            blocks={tuple(v['pos']):d['palette'][v['state']]['Name'] for v in d['blocks']}
            commands=['gamemode spectator @a','time set day','weather clear','effect give @a minecraft:night_vision infinite 0 true','forceload remove all',f'forceload add {x} 0 {x+sx} {sz}',f'tp @a {cx} {max(195,cy+sy*.1)} {-distance} facing {cx} {cy} {cz}']
            scenes.append(dict(label=asset['id']+' load footprint',commands=commands,wait_ms=5000))
            commands=[]
            # Clear only the operator exhibition volume BEFORE placing the exact template.
            # Every fill stays below vanilla's 32768-block limit on both versions.
            for ax in range(0,sx+1,16):
                for az in range(0,sz+1,16):
                    commands.append(f'fill {x+ax} {y} {az} {x+min(sx,ax+15)} {min(200,y+sy)} {min(sz,az+15)} minecraft:air')
            commands.append(f'place template relics:{name[:-4]} {x} {y} 0')
            gameplay=asset.get('gameplay',{});off=gameplay.get('offset',[0,0,0]);markers=gameplay.get('markers',[])
            for m in markers:
                role=m['role'];block=None
                if role.endswith('_chest'):block='minecraft:chest' if a.minecraft=='1.21.1' else 'minecraft:waxed_copper_chest'
                elif role=='colossus_trial_spawner':block='minecraft:trial_spawner'
                elif role=='colossus_vault':block='minecraft:vault'
                elif role.startswith('archaeology_'):block='minecraft:suspicious_sand'
                if block:
                    px,py,pz=[b+c for b,c in zip(m['pos'],off)]
                    if 'facing' in m:block+='[facing='+m['facing']+']'
                    commands.append(f'setblock {x+px} {y+py} {pz} {block}')
            scenes.append(dict(label=asset['id']+' whole model front; operator marker replacements',commands=commands,wait_ms=20000))
            scenes.append(dict(label=asset['id']+' whole model reverse',commands=[f'tp @a {cx} {max(195,cy+sy*.15)} {sz+distance} facing {cx} {cy} {cz}'],wait_ms=15000))
            chosen=[m for m in markers if m['role'].endswith('_chest') or m['role'] in ['colossus_trial_spawner','colossus_vault','tree_amethyst_center','archaeology_map']]
            for m in chosen:
                local=tuple(b+c for b,c in zip(m['pos'],off))
                view=camera(blocks,local)
                if view is None and m['role']=='tree_amethyst_center':
                    for p,b in blocks.items():
                        if b=='minecraft:amethyst_block' and sum((p[k]-local[k])**2 for k in range(3))<50:
                            view=camera(blocks,p)
                            if view:break
                px,py,pz=local;px+=x;py+=y
                facing=m.get('facing','north');dx,dz={'north':(0,-3),'south':(0,3),'east':(3,0),'west':(-3,0)}[facing]
                command=f'tp @a {px+.5+dx} {py+1.2} {pz+.5+dz} facing {px+.5} {py+.5} {pz+.5}'
                if view:
                    eye,aim=view;command=f'tp @a {x+eye[0]} {y+eye[1]-1.62} {eye[2]} facing {x+aim[0]} {y+aim[1]} {aim[2]}'
                scenes.append(dict(label=asset['id']+' interior '+m['role'],commands=[command],wait_ms=7000))
            if asset['id']=='world_tree':
                plant='minecraft:fern' if a.minecraft=='1.21.1' else 'minecraft:firefly_bush'
                found=next((b for b in d['blocks'] if d['palette'][b['state']]['Name']==plant and camera(blocks,tuple(b['pos']))),None)
                if found:
                    eye,aim=camera(blocks,tuple(found['pos']))
                    scenes.append(dict(label='world_tree native plant '+plant,commands=[f'tp @a {x+eye[0]} {y+eye[1]-1.62} {eye[2]} facing {x+aim[0]} {y+aim[1]} {aim[2]}'],wait_ms=7000))
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(scenes,indent=2))

if __name__=='__main__':main()
