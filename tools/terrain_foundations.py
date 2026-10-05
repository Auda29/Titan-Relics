"""Deterministic soil-column foundations for rigid natural relic templates.

Extend authored near-ground terrain columns and low surrounding toes, preserving
every existing model cell. Pad X/Y/Z to keep all foundation positions inside NBT.
"""
import heapq

POLICY = 'near-ground-soil-columns-v4-protected-runtime-contact'
TOE_RADIUS = 8
SOILS = {'minecraft:dirt', 'minecraft:rooted_dirt', 'minecraft:coarse_dirt',
         'minecraft:grass_block', 'minecraft:moss_block', 'minecraft:podzol',
         'minecraft:sand', 'minecraft:sandstone', 'minecraft:smooth_sandstone', 'minecraft:red_sand',
         'minecraft:red_sandstone', 'minecraft:gravel', 'minecraft:stone',
         'minecraft:andesite', 'minecraft:tuff'}


def padding(contract):
    return max(0, contract['slope'] + 4 - contract['ground_y'])


def natural_ground(contract):
    return contract['ground_y'] + padding(contract)


def natural_size(contract):
    x,y,z=contract['size']
    return [x+2*TOE_RADIUS,y+padding(contract),z+2*TOE_RADIUS]


def supported_blocks(blocks, contract):
    ground = contract['ground_y']
    bottom = ground - contract['slope'] - 4
    pad = padding(contract)
    columns = {}
    for (x, y, z), state in blocks.items():
        if y <= ground + 4 and state.split('[')[0] in SOILS:
            previous = columns.get((x, z))
            if previous is None or y < previous[0]:
                columns[x, z] = y, state.split('[')[0]
    result = {(x+TOE_RADIUS, y + pad, z+TOE_RADIUS): state for (x, y, z), state in blocks.items()}
    added = 0
    fills = {}
    for (x, z), (y, state) in columns.items():
        if state in {'minecraft:sand', 'minecraft:sandstone', 'minecraft:smooth_sandstone'}:
            fill = 'minecraft:sandstone'
        elif state in {'minecraft:red_sand', 'minecraft:red_sandstone'}:
            fill = 'minecraft:red_sandstone'
        elif state in {'minecraft:stone', 'minecraft:andesite', 'minecraft:tuff', 'minecraft:gravel'}:
            fill = 'minecraft:stone'
        else:
            fill = 'minecraft:dirt'
        fills[x,z] = fill
        for height in range(bottom, y):
            pos = x+TOE_RADIUS, height + pad, z+TOE_RADIUS
            if pos not in result:
                result[pos] = fill
                added += 1
    # A stepped talus toe removes the sheer skirt at a downhill edge. Its top
    # drops two blocks per horizontal step; the outer toe is below the admitted
    # surface floor. Propagate only into columns without an authored soil contact.
    queue=[];tops={}
    for (x,z),(y,_) in columns.items():
        heapq.heappush(queue, (-(y-1),0,x,z,fills[x,z]))
    while queue:
        negative,steps,x,z,fill=heapq.heappop(queue);top=-negative
        if steps>=TOE_RADIUS or top-2<bottom:continue
        for dx,dz in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
            key=x+dx,z+dz;new_top=top-2
            if key in columns or (key in tops and tops[key][0]>=new_top):continue
            tops[key]=(new_top,fill);heapq.heappush(queue,(-new_top,steps+1,*key,fill))
    toe_blocks=0
    for (x,z),(top,fill) in tops.items():
        for y in range(bottom,top+1):
            pos=x+TOE_RADIUS,y+pad,z+TOE_RADIUS
            if pos not in result:
                result[pos]='minecraft:grass_block[snowy=false]' if y==top and fill=='minecraft:dirt' else fill
                added+=1;toe_blocks+=1
    size = natural_size(contract)
    return result, size, {'method': POLICY, 'vertical_padding': pad, 'horizontal_padding': TOE_RADIUS,
                          'runtime_processor': 'relics:terrain_support',
                          'feature_protection': 'relics:placed_cells',
                         'toe_blocks':toe_blocks, 'toe_columns':len(tops),
                         'ground_y': ground + pad, 'bottom_below_ground': ground - bottom,
                         'supported_columns': len(columns), 'added_blocks': added}
