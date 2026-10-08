"""Versioned block-exact architectural derivatives of the pinned Alpha 4.9 art.

No worldgen/catalog mutation. Semantic placeholders are ordinary blocks; gameplay
initialization consumes the hash-bound v1 sidecar later. Old exports stay exact.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
import math
from pathlib import Path

from colossus_materials import encode_schematic
from inspect_ots_result import read_structure
from relic_catalog import ASSETS, ROOT
from schem_to_nbt import convert

STEMS = {'colossus':'colossus-v5-interiors', 'small_colossus':'small-colossus-v8-interiors',
         'ruined_tower':'ruined-tower-v8-interiors', 'obelisk':'obelisk-v5-archaeology',
         'world_tree':'world-tree-v5-refuge'}
STONE='minecraft:polished_deepslate'
WORN='minecraft:cracked_deepslate_tiles'
TRIM='minecraft:polished_basalt[axis=y]'
CHEST='minecraft:waxed_cut_copper'
NATIVE=['minecraft:stone','minecraft:deepslate','minecraft:dirt','minecraft:grass_block',
        'minecraft:coarse_dirt','minecraft:rooted_dirt','minecraft:sand','minecraft:gravel',
        'minecraft:granite','minecraft:diorite','minecraft:andesite','minecraft:tuff',
        'minecraft:short_grass','minecraft:tall_grass','minecraft:fern','minecraft:large_fern',
        'minecraft:oak_leaves','minecraft:birch_leaves','minecraft:spruce_leaves']

def cells(lo,hi):
    return itertools.product(*(range(a,b+1) for a,b in zip(lo,hi)))

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

class Builder:
    def __init__(self,name):
        self.name=name; self.a=ASSETS[name]; self.source=ROOT/self.a['source']
        assert digest(self.source)==self.a['sha256']
        self.root,self.old=read_structure(self.source);self.blocks=dict(self.old)
        self.groups={};self.markers=[];self.regions=[];self.evidence={};self.paths=[]
        self.stem=STEMS[name];self.out=self.source.parent.parent/self.stem
        self.group='architecture'

    def put(self,p,state):
        p=tuple(p)
        assert all(0<=v<n for v,n in zip(p,self.root['size'])),p
        if state is None:self.blocks.pop(p,None)
        else:self.blocks[p]=state
        self.groups[p]=self.group

    def box(self,lo,hi,state):
        for p in cells(lo,hi):self.put(p,state)

    def ellipsoid(self,c,r,state):
        for p in cells([math.floor(v-w) for v,w in zip(c,r)],[math.ceil(v+w) for v,w in zip(c,r)]):
            if sum(((v-a)/b)**2 for v,a,b in zip(p,c,r))<=1:self.put(p,state)

    def marker(self,role,pos,facing=None,placeholder=None):
        count=sum(m['role']==role for m in self.markers)
        marker={'id':role.replace('_','-')+f'-{count+1}','role':role,'pos':list(pos)}
        if facing:marker['facing']=facing
        if placeholder:
            self.put(pos,placeholder);marker['expected_block']=placeholder
        self.markers.append(marker)

    def region(self,role,lo,hi):
        r={'id':role.replace('_','-')+f'-{len(self.regions)+1}','role':role,'min':list(lo),'max':list(hi)}
        if role.endswith('_clearance'):r['replaceable_blocks']=NATIVE
        self.regions.append(r)

    def clearance(self,lo,hi,role):
        self.box(lo,hi,None);self.region(role,lo,hi)

    def path(self,name,points,height=3):
        self.paths.append({'name':name,'feet':[list(p) for p in points],'height':height})

    def save(self):
        self.out.mkdir(parents=True,exist_ok=True)
        path=self.out/(self.stem+'.schem')
        path.write_bytes(encode_schematic(self.blocks,self.root['size'],self.root['DataVersion'],[0,0,0]))
        manifest=convert(path,path.with_suffix('.nbt'),'omit',32)
        sidecar={'schema_version':1,'structure_id':'relics:'+self.name,'asset_version':self.stem,
                 'source_nbt':path.with_suffix('.nbt').relative_to(ROOT).as_posix(),
                 'source_sha256':digest(path.with_suffix('.nbt')),'size':self.root['size'],
                 'ground_y':self.a['ground_y'],'coordinate_space':'raw_template','source_facing':'north',
                 'markers':self.markers,'regions':self.regions}
        path.with_suffix('.gameplay.json').write_text(json.dumps(sidecar,indent=2)+'\n')
        changed={p for p in self.old.keys()|self.blocks.keys() if self.old.get(p)!=self.blocks.get(p)}
        design={'name':self.stem,'authoring':'block-exact architectural derivative; no global revoxelization',
                'baseline':self.a,'ground_level_nbt_approx':self.a['ground_y'],'size':self.root['size'],
                'data_version':self.root['DataVersion'],'in_game_tested':False,'visual_acceptance':'review pending',
                'evidence':self.evidence,'paths':self.paths,
                'changes':{'added':sum(p not in self.old for p in changed),
                           'removed':sum(p not in self.blocks for p in changed),
                           'remapped':sum(p in self.old and p in self.blocks for p in changed)},
                'changed_bounds':[[min(p[i] for p in changed) for i in range(3)],
                                  [max(p[i] for p in changed) for i in range(3)]],
                'changed_groups':dict(Counter(self.groups[p] for p in changed)),
                'nbt_sha256':sidecar['source_sha256'],'schematic_sha256':digest(path),'tiles':len(manifest['tiles']),
                'palette':dict(Counter(self.blocks.values()))}
        path.with_suffix('.design.json').write_text(json.dumps(design,indent=2)+'\n')
        # Local authoring groups are reproducible from this generator, not a second source.
        path.with_suffix('.groups.json').write_text(json.dumps({k:[list(p) for p in sorted(changed) if self.groups[p]==k and p in self.blocks] for k in set(self.groups.values())})+'\n')
        assert digest(self.source)==self.a['sha256']
        print(self.stem,len(self.blocks),design['changes'],len(self.markers),'markers')
        return path.with_suffix('.gameplay.json')

def large(b):
    b.group='cockpit-deck'
    # A single low deck joins the existing helmet shell. Five small stations,
    # rather than five giant seats or an unrelated multi-storey body interior.
    for x in range(72,117):
        for z in range(158,204):
            if (x-94)**2+(z-181)**2<=21**2:
                for y in (166,167,168):
                    if (x,y,z) not in b.old:b.put((x,y,z),WORN if (x*17+z*13)%23<2 else STONE)
    # The already hollow interior is reserved explicitly for terrain clearing.
    b.region('cockpit_clearance',(77,169,165),(110,181,198))
    b.group='hatch'
    b.clearance((108,169,179),(121,175,185),'hatch_clearance')
    b.box((107,167,178),(123,168,186),STONE)
    for z in (178,186):b.box((116,169,z),(118,175,z),TRIM)
    b.box((116,176,178),(118,177,186),TRIM)
    # Open frame makes the intended entry legible without a locked entry gadget.
    b.marker('colossus_hatch',(118,169,182),'east')
    b.group='crew-stations'
    stations=[(82,174),(87,168),(94,166),(101,168),(106,174)]
    for i,(x,z) in enumerate(stations):
        b.box((x-1,169,z),(x+1,169,z+1),TRIM)
        b.put((x,170,z+1),'minecraft:deepslate_tile_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
        b.box((x-1,169,z-2),(x+1,170,z-2),STONE)
        b.put((x,170,z-2),'minecraft:brown_terracotta')
        b.put((x,171,z-2),'minecraft:chiseled_deepslate')
        for dz in (2,3,4):b.put((x,168,z+dz),'minecraft:polished_andesite')
        # Instruments are inert geometric remains, not a control puzzle.
    b.group='trial-and-vault'
    b.box((91,169,179),(97,173,187),None)
    b.marker('colossus_golem_spawn',(94,169,183))
    b.marker('colossus_trial_spawner',(94,169,193),placeholder='minecraft:chiseled_deepslate')
    b.marker('colossus_vault',(84,169,190),'south','minecraft:polished_blackstone')
    b.path('hatch-to-arena',[(x,169,182) for x in range(94,122)],4)
    b.group='arm-exploration'
    points=[]
    # Enter the broken elbow, walk a short independent service trough. Hand and
    # palm/fingers are well outside this region and remain byte-exact.
    for i in range(33):
        x,z=143-i,104-i
        b.box((x-2,78,z-2),(x+2,81,z+2),None)
        b.box((x-2,76,z-2),(x+2,77,z+2),STONE)
        points.append((x,78,z))
    # Disjoint narrow stair-step regions, not a box erasing the surrounding arm.
    for x,y,z in points[::3]:b.region('arm_clearance',(x-2,y,z-2),(x+2,y+3,z+2))
    b.marker('colossus_arm_magnet_chest',(110,78,70),'south',CHEST)
    b.path('broken-elbow-to-arm-find',points,3)
    b.evidence={'crew_stations':stations,'crew_station_count':5,'body_cavity_preserved_below_y':135,
                'arm_route_note':'Bounded arm_clearance regions reserve the independent elbow passage.',
                'no_authored_ground_to_head_ascent':True,
                'views':[{'label':'Cockpit / hatch / five stations','lo':[70,166,154],'hi':[126,173,207]},
                         {'label':'Independent broken-arm exploration','lo':[99,72,61],'hi':[151,87,112]}]}

def small(b):
    b.group='collapsed-interior'
    b.ellipsoid((62,28,74),(20,12,17),None)
    b.ellipsoid((62,51,46),(12,13,15),None)
    b.region('small_interior_clearance',(43,18,58),(81,38,90))
    b.region('small_interior_clearance',(51,39,32),(73,63,60))
    b.box((48,17,60),(77,18,87),WORN)
    # A torn lower breast entry; its threshold remains near the ground datum.
    points=[]
    for z in range(40,70):
        y=min(19,14+max(0,z-43)//3)
        b.box((59,y,z),(65,y+4,z),None)
        b.box((59,13,z),(65,y-1,z),WORN)
        points.append((62,y,z))
        b.region('small_interior_clearance',(59,y,z),(65,y+4,z))
    b.path('breast-rupture-entry',points)
    # Sheared load ribs and loose remnants, no intact two-seat cockpit.
    for x,z,h in [(48,66,7),(75,85,5),(50,85,3)]:b.box((x,19,z),(x+1,19+h,z+1),TRIM)
    for x,z in [(55,76),(68,83),(71,63)]:b.box((x,19,z),(x+2,19,z+1),WORN)
    for x,z,top in [(49,70,31),(75,75,28),(52,83,26)]:
        b.box((x,19,z),(x,top,z+2),TRIM)
        b.box((x,top,z),(x+3,top,z),WORN)
    # Continuous damaged maintenance steps make the lost cockpit reachable.
    climb=[]
    for i in range(25):
        y,z=19+i,82-i
        b.box((59,y,z),(63,y+4,z),None)
        b.box((59,y-1,z),(63,y-1,z),STONE)
        climb.append((61,y,z))
        b.region('small_interior_clearance',(59,y,z),(63,y+4,z))
    b.box((53,42,36),(70,43,57),WORN)
    b.box((59,43,53),(63,47,59),None)
    for x in (54,69):b.box((x,44,40),(x,47,54),TRIM)
    b.box((54,44,38),(57,45,41),WORN)
    b.path('ruined-maintenance-climb',climb)
    b.marker('small_magnet_chest',(73,19,80),'west',CHEST)
    b.evidence={'intact_crew_seats':0,'views':[{'label':'Torn breast entry and salvage recess','lo':[40,12,38],'hi':[83,26,95]},
             {'label':'Severely decayed cockpit / connecting climb','lo':[48,29,28],'hi':[77,52,84]}]}

def tower(b):
    b.group='lower-hall'
    b.box((40,13,27),(77,14,58),WORN)
    b.clearance((41,15,28),(76,23,57),'tower_route_clearance')
    b.clearance((53,13,17),(60,22,28),'tower_route_clearance')
    b.box((53,12,17),(60,14,28),STONE)
    # Low partition ruins offer readable bays, with a broad central opening.
    for z in list(range(33,39))+list(range(49,55)):
        b.box((55,15,z),(56,20 if z%3 else 18,z),WORN)
    for x,z in [(43,54),(73,53),(43,30)]:b.box((x,15,z),(x+1,21,z+1),TRIM)
    b.marker('tower_entry',(57,15,20),'north')
    for x,z in [(47,34),(65,33),(47,45),(66,48),(71,40)]:
        b.box((x-1,15,z-1),(x+1,18,z+1),None)
        b.marker('tower_enderman_spawn',(x,15,z))
    b.marker('tower_ender_chest',(72,15,55),'north',CHEST)
    b.path('tower-entry',[(57,15,z) for z in range(20,34)])
    b.group='unfinished-ascent'
    ring=[(x,29,'east') for x in range(41,76)]+[(76,z,'south') for z in range(29,57)]+[(x,57,'west') for x in range(76,41,-1)]+[(41,z,'north') for z in range(57,29,-1)]
    gaps=[(31,37),(90,97),(157,164),(229,236),(289,296)]
    steps=[]
    for i in range(320):
        x,z,facing=ring[i%len(ring)];y=15+i//2
        lo=(x-1,y,z-1);hi=(x+1,y+4,z+1)
        b.box(lo,hi,None)
        b.region('tower_route_clearance',lo,hi)
        if any(a<=i<=c for a,c in gaps):continue
        b.box((x-1,y-2,z-1),(x+1,y-1,z+1),STONE)
        # Broad half-step treads alternate with landings. Native stair geometry.
        if i%2==0:
            for q in cells((x-1,y-1,z-1),(x+1,y-1,z+1)):
                b.put(q,f'minecraft:deepslate_tile_stairs[facing={facing},half=bottom,shape=straight,waterlogged=false]')
        steps.append((x,y,z))
    # End platform deliberately on a surviving rear wall; no extra reward.
    x,y,z=steps[-1]
    b.box((x-2,y-2,z-2),(x+3,y-1,min(z+5,63)),STONE)
    b.box((x-1,y,z-1),(x+2,y+3,z+2),None)
    b.marker('tower_upper_destination',(x,y,z))
    b.evidence={'stair_gaps':gaps,'stair_step_count':len(steps),'stair_start':list(steps[0]),'stair_end':list(steps[-1]),
                'views':[{'label':'Lower hall / five Enderman positions','lo':[36,11,16],'hi':[82,25,67]},
                         {'label':'Unfinished wall-side ascent / player-built gaps','lo':[38,25,26],'hi':[79,179,65]}]}

def obelisk(b):
    b.group='exterior-archaeology'
    positions=[(8,28),(13,35),(9,41),(45,45),(49,48),(44,51),(14,27),(48,42)]
    for i,(x,z) in enumerate(positions):
        y=max(p[1] for p in b.old if p[0]==x and p[2]==z and p[1]<16)+1
        # A small supported sand pocket, exposed at its top for careful brushing.
        b.put((x,y-1,z),'minecraft:sandstone')
        b.marker('archaeology_common' if i<6 else 'archaeology_trim' if i==6 else 'archaeology_map',
                 (x,y,z),placeholder='minecraft:sand')
        if i%2==0:
            for dx in (-1,1):b.put((x+dx,y-1,z),'minecraft:cut_sandstone')
    # Two low discontinuous excavation edges, no attached underground dungeon.
    for x,z in [(6,31),(7,31),(8,31),(10,31),(46,50),(47,50),(50,50)]:
        y=max(p[1] for p in b.old if p[0]==x and p[2]==z and p[1]<16)
        b.put((x,y,z),'minecraft:cut_sandstone')
    for x,z,h in [(5,27,2),(5,28,1),(5,29,2),(5,30,1),(6,30,1),
                  (44,54,1),(45,54,2),(46,54,1),(49,54,1),(50,54,2)]:
        y=max(p[1] for p in b.old if p[0]==x and p[2]==z and p[1]<16)
        b.box((x,y,z),(x,y+h,z),'minecraft:cut_sandstone')
    b.evidence={'monument_above_y16_exact':True,'brushable_positions':8,
                'views':[{'label':'West excavation / supported brushing pockets','lo':[2,5,21],'hi':[19,16,49]},
                         {'label':'East excavation / map find','lo':[42,5,38],'hi':[56,16,56]}]}

def tree(b):
    ground=b.a['ground_y'];b.group='amethyst-heart'
    b.ellipsoid((94,29,93),(3,3,3),'minecraft:amethyst_block')
    # A shallow viewing slit exposes the sphere without a new room/settlement.
    b.box((93,27,76),(95,31,89),None)
    b.marker('tree_amethyst_center',(94,29,93))
    b.marker('tree_aura_anchor',(94,24,93))
    b.group='root-lights';lights=[]
    def wood(s):return s and ('log' in s or 'wood' in s)
    # Irregular, mutually spaced luminous fungus set flush in actual root wood.
    candidates=sorted(p for p,s in b.old.items() if wood(s) and ground<=p[1]<=ground+5
                      and (p[0],p[1]+1,p[2]) not in b.old and ((p[0]-94)**2+(p[2]-93)**2)>15**2)
    for p in sorted(candidates,key=lambda p:((p[0]*73856093^p[2]*19349663)%100003,p)):
        if all(sum((a-c)**2 for a,c in zip(p,q))>=8**2 for q in lights):
            b.put(p,'minecraft:shroomlight');lights.append(p)
    # Face-supported lichen along trunk/root sides, tapering before +15.
    lichen=[]
    for x,y,z in sorted(b.old):
        if not ground<=y<=ground+14 or not wood(b.blocks.get((x,y,z))):continue
        if (x*11+y*19+z*7)%41!=0:continue
        for dx,dz,face in [(1,0,'west'),(-1,0,'east'),(0,1,'north'),(0,-1,'south')]:
            p=(x+dx,y,z+dz)
            if p not in b.blocks and all(sum((a-c)**2 for a,c in zip(p,q))>=4**2 for q in lichen):
                b.put(p,'minecraft:glow_lichen['+','.join(f'{f}={str(f==face).lower()}' for f in ('down','east','north','south','up'))+',waterlogged=false,west='+str(face=='west').lower()+']')
                lichen.append(p);break
    berries=[]
    for p,s in sorted(b.old.items()):
        x,y,z=p
        if not ground+4<=y<=ground+12 or not wood(b.blocks.get(p)):continue
        if (x,y-1,z) in b.blocks or (x,y-2,z) in b.blocks or (x*13+z*7)%9:continue
        if any((x-a)**2+(z-c)**2<9**2 for a,_,c in berries):continue
        b.put((x,y-1,z),'minecraft:cave_vines_plant[berries=true]')
        b.put((x,y-2,z),'minecraft:cave_vines[age=25,berries=true]');berries.append((x,y-1,z))
    bushes=[]
    # Dispersed small root-adjacent ground tufts. Native ground integration must
    # still measure final block light and support on real terrain.
    for x,z in [(65,84),(67,102),(75,117),(94,128),(114,108),(125,90),(119,72),(101,67),(82,68)]:
        p=(x,ground,z)
        if p in b.blocks:continue
        b.put((x,ground-1,z),'minecraft:rooted_dirt')
        b.put(p,'minecraft:firefly_bush');bushes.append(p)
    b.region('tree_lighting_scope',(44,ground-1,55),(138,ground+15,139))
    b.evidence={'local_trunk_base':[94,ground,93],'maximum_light_height':15,
                'shroomlights':lights,'lichen':lichen,'berries':berries,'firefly_bushes':bushes,
                'amethyst_radius':3,'budding_amethyst':False,'views':[{'label':'Root refuge / supported luminous growth','lo':[44,22,53],'hi':[140,41,143]},
                 {'label':'Cut through internal amethyst sphere / viewing slit','lo':[86,23,74],'hi':[102,29,100]}]}

BUILDERS={'colossus':large,'small_colossus':small,'ruined_tower':tower,'obelisk':obelisk,'world_tree':tree}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('asset',choices=[*BUILDERS,'all']);args=parser.parse_args()
    for name in BUILDERS if args.asset=='all' else [args.asset]:
        b=Builder(name);BUILDERS[name](b);b.save()

if __name__=='__main__':main()
