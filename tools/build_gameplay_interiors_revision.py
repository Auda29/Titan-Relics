"""Feedback revisions, built on the maintained original builders without changing them."""
import argparse
from build_gameplay_interiors import Builder, BUILDERS, ROOT, ASSETS, STONE, WORN, TRIM

STEMS = {'colossus':'colossus-v6-interiors', 'small_colossus':'small-colossus-v9-interiors',
         'ruined_tower':'ruined-tower-v9-interiors', 'obelisk':'obelisk-v6-archaeology'}

def build(name):
    b=Builder(name); BUILDERS[name](b)
    b.stem=STEMS[name]; b.out=(ROOT/ASSETS[name]['source']).parent.parent/b.stem
    previous=dict(b.blocks)
    if name=='colossus':
        # Broken aperture cut through the actual multiple front helmet layers.
        b.group='fractured-visor'
        for x in range(87,102):
            for y in range(170,177):
                if (x-94)**2/64+(y-173)**2/9 <= 1:
                    for z in range(145,164): b.put((x,y,z),None)
        # Fragmentary stained glass along edges, supported by the remaining shell.
        fragments=[]
        candidates=[]
        for p in previous:
            x,y,z=p
            if not (86<=x<=102 and 169<=y<=177 and 145<=z<=163 and p in b.blocks):continue
            neighbors=[(x+dx,y+dy,z+dz) for dx,dy,dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))]
            if any(q in previous and q not in b.blocks for q in neighbors):candidates.append(p)
        for p in sorted(candidates,key=lambda q:((q[0]*73+q[1]*31+q[2]*43)%101,q)):
            if all(sum(abs(a-c) for a,c in zip(p,q))>=4 for q in fragments):
                fragments.append(p)
                if len(fragments)==7:break
        assert len(fragments)==7
        for p in fragments:b.put(p,'minecraft:black_stained_glass')
        b.group='wrecked-cockpit-machinery'
        # Several bulky broken housings on the perimeter, away from the arena,
        # stations, hatch path and marker headroom. Base touches the deck.
        for x,z in [(77,180),(78,194),(104,196),(109,188),(81,183)]:
            b.box((x,169,z),(x+3,170,z+2),WORN)
            b.box((x,171,z),(x+1,173,z+2),STONE)
            b.box((x+2,171,z),(x+3,172,z+1),TRIM)
            b.put((x,174,z),'minecraft:chiseled_deepslate')
            b.put((x+2,171,z+2),'minecraft:polished_andesite')
        for x,z in [(80,178),(84,198),(100,199),(108,192)]:
            b.box((x,169,z),(x+1,169,z+3),TRIM)
            b.box((x,170,z),(x,172,z),WORN)
        for x in (87,98):
            b.box((x,169,194),(x+3,170,198),WORN)
            b.box((x,171,195),(x+1,175,197),TRIM)
            b.box((x+2,171,194),(x+3,173,196),STONE)
            b.box((x,176,195),(x+2,176,195),'minecraft:chiseled_deepslate')
            b.box((x+3,171,197),(x+3,172,198),'minecraft:polished_andesite')
        b.evidence['views']=[{'label':'Cockpit: five stations and ruined machinery','lo':[70,166,154],'hi':[126,176,207]},
                             {'label':'Front helmet / fractured visor','lo':[74,166,145],'hi':[115,185,170]},
                             {'label':'Independent arm access','lo':[99,72,61],'hi':[151,87,112]}]
    elif name=='small_colossus':
        b.group='salvaged-mechanical-ribs'
        for x,z,h in [(52,68,7),(53,81,6),(70,68,6),(71,76,7),(56,85,4)]:
            b.box((x,19,z),(x,19+h,z),TRIM)
            b.box((x,19+h,z),(x+2,19+h,z),WORN)
            b.put((x+2,18+h,z),'minecraft:chiseled_deepslate')
        b.group='stripped-machinery'
        for x,z in [(53,73),(68,72),(69,85),(55,83)]:
            b.box((x,19,z),(x+2,20,z+2),WORN)
            b.box((x,21,z),(x+1,22,z+1),TRIM)
            b.put((x+2,21,z),'minecraft:polished_andesite')
        b.evidence['views'][0]['hi']=[83,31,95]
    elif name=='ruined_tower':
        b.group='worn-hall-details'
        for x,z in [(44,39),(50,53),(62,54),(72,36),(68,29)]:
            b.box((x,15,z),(x+1,15,z+1),WORN)
            b.put((x,16,z),TRIM)
            b.put((x+1,16,z),'minecraft:chiseled_deepslate')
    else:
        b.group='excavation-landmarks'
        # Weathered, interrupted stone boundary stones, visible from ground level.
        for x,z,h in [(4,25,4),(4,34,3),(5,43,4),(15,44,3),(16,25,3),
                      (50,39,4),(52,40,3),(53,47,4),(52,54,3),(42,54,3)]:
            y=max(p[1] for p in previous if p[0]==x and p[2]==z and p[1]<16)
            for dy in range(h):
                p=(x,y+dy,z)
                if previous.get(p,'').find('terracotta')>=0: raise ValueError('protected terracotta')
                b.put(p,'minecraft:cut_sandstone' if dy%2==0 else 'minecraft:sandstone')
        b.evidence['views']=[{'label':'West excavation: boundary landmarks and brushing pockets','lo':[1,5,21],'hi':[19,17,49]},
                             {'label':'East excavation: boundary landmarks and brushing pockets','lo':[40,5,37],'hi':[56,17,57]}]
    b.evidence['feedback_revision']='2026-10-27; previous gameplay markers and regions preserved'
    return b

def main():
    p=argparse.ArgumentParser();p.add_argument('asset',choices=[*STEMS,'all']);a=p.parse_args()
    for name in STEMS if a.asset=='all' else [a.asset]: build(name).save()

if __name__=='__main__':main()
