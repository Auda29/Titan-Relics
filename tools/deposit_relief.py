"""Deterministic block-scale erosion of authored terrain; preserve every art cell."""
from collections import deque
import math


def noise(x,z,scale):
    def value(i,j):
        n=((i*374761393+j*668265263)^0x4D381A7B)&0xffffffff
        n=((n^(n>>13))*1274126177)&0xffffffff
        return (n^(n>>16))/0xffffffff
    x/=scale;z/=scale;i=math.floor(x);j=math.floor(z);u=x-i;v=z-j
    u=u*u*(3-2*u);v=v*v*(3-2*v)
    return (value(i,j)*(1-u)+value(i+1,j)*u)*(1-v)+(value(i,j+1)*(1-u)+value(i+1,j+1)*u)*v


def erode(blocks,ground,materials,protected_columns=()):
    declared={v for k,v in materials.items() if k.startswith('terrain_')}
    art={v for k,v in materials.items() if not k.startswith('terrain_')}
    terrain=declared-art  # E.g. Skull 2 moss also belongs to the skull itself.
    columns={};structure={}
    for (x,y,z),state in blocks.items():
        if state in terrain:columns.setdefault((x,z),[]).append(y)
        else:structure.setdefault((x,z),[]).append(y)
    tops={p:max(ys) for p,ys in columns.items()}
    # Lock terrain directly below/alongside existing non-terrain contact cells.
    contact=set(protected_columns)&columns.keys()
    for (x,z),ys in columns.items():
        for dx,dz in ((0,0),(1,0),(-1,0),(0,1),(0,-1)):
            solids=structure.get((x+dx,z+dz),())
            # Buried root tips can rely on a derived soil column whose authored
            # cap is higher than the tip. Protect that column as well.
            if any(y<=tops[x,z]+2 for y in solids):
                contact.add((x,z));break
    distance={p:0 for p in contact};queue=deque(sorted(contact))
    while queue:
        x,z=queue.popleft()
        for p in ((x-1,z),(x+1,z),(x,z-1),(x,z+1)):
            if p in columns and p not in distance:
                distance[p]=distance[x,z]+1;queue.append(p)
    result=dict(blocks);removed=0;changed=0
    for (x,z),ys in columns.items():
        top=tops[x,z];d=distance.get((x,z),32)
        if top<ground-2 or d<=2:continue
        # Unequal erosion lobes and meandering shallow runnels interrupt nested
        # contour rings. No random single-cell peppering, lifted soil or new mound.
        broad=noise(x,z,19);fine=noise(x+31,z-17,6)
        channel=max(0,1-abs(noise(x+8,z-5,11)-.5)*9)
        available=max(0,top-ground+3)
        amount=min(max(0,(d-2)*.9),available*(.25+.45*broad+.25*channel)+fine*.8)
        new_top=top-int(amount)
        if new_top==top:continue
        changed+=1
        for y in ys:
            if y>new_top:del result[x,y,z];removed+=1
        if (x,new_top,z) in result:
            # Keep sand/gravel supported by the solid deposit, with no buried grass.
            cap=materials['terrain_patch'] if noise(x-19,z+47,8)>.68 else materials['terrain_top']
            if cap not in terrain:cap=materials['terrain_fill']
            if cap in ('minecraft:sand','minecraft:gravel') and (x,new_top-1,z) not in result:
                cap=materials['terrain_fill']
            result[x,new_top,z]=cap
    for p,s in list(result.items()):
        if s=='minecraft:grass_block[snowy=false]' and (p[0],p[1]+1,p[2]) in result:
            if p not in blocks or blocks[p] in terrain:result[p]=materials['terrain_fill']
    assert {p:s for p,s in result.items() if s not in terrain}=={p:s for p,s in blocks.items() if s not in terrain}
    assert all(result.get((x,y,z))==blocks[x,y,z] for x,z in contact for y in columns[x,z])
    return result,{'algorithm':'contact-preserving-eroded-deposits-v1','terrain_states':sorted(terrain),
        'protected_contact_columns':len(contact),'modified_columns':changed,'removed_soil_cells':removed,
        'non_terrain_cells_identical':True,'contact_columns_identical':True}
