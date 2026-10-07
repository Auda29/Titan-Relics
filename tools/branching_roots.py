"""Sparse curved root strands below the accepted Tree, instead of footprint extrusion."""
from collections import deque
import math

WOOD = 'minecraft:spruce_log[axis=y]'
N6 = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def grow_strands(art, size):
    result = dict(art)
    bottoms = {}
    for (x, y, z), s in art.items():
        if '_log[' in s and y <= 10:
            bottoms[x, z] = min(y, bottoms.get((x, z), y))
    trunk = [(x, z) for (x, y, z), s in art.items() if y == 30 and '_log[' in s]
    cx, cz = (sum(p[i] for p in trunk) / len(trunk) for i in (0, 1))
    paths = []

    def strand(start, control, end, radius):
        for step in range(81):
            t = step / 80
            center = [start[i] * (1-t)**2 + 2*control[i]*t*(1-t) + end[i]*t*t for i in range(3)]
            r = radius * (1-t) + .58*t
            for x in range(math.floor(center[0]-r), math.ceil(center[0]+r)+1):
                for y in range(math.floor(center[1]-r), math.ceil(center[1]+r)+1):
                    for z in range(math.floor(center[2]-r), math.ceil(center[2]+r)+1):
                        if (0 <= x < size[0] and 0 <= z < size[2] and -12 <= y <= 10
                                and sum((a-b)**2 for a,b in zip((x,y,z),center)) <= r*r):
                            result.setdefault((x,y,z), WOOD)
        paths.append({'start': list(start), 'control': list(control), 'end': list(end),
                      'start_radius': radius, 'tip_radius': .58})

    for group, degrees in enumerate((-157, -102, -39, 24, 71, 131, 173)):
        angle = math.radians(degrees)
        dx, dz = math.cos(angle), math.sin(angle)
        used = []
        for ring, distance in enumerate((26, 38, 50, 62, 74)):
            candidates = [(x,z) for x,z in bottoms
                          if abs((x-cx)*dz-(z-cz)*dx) < 10
                          and abs((x-cx)*dx+(z-cz)*dz-distance) < 6]
            if not candidates:
                continue
            x,z = min(candidates, key=lambda p: (p[0]-cx-dx*distance)**2 + (p[1]-cz-dz*distance)**2)
            if any((x-xx)**2+(z-zz)**2 < 64 for xx,zz in used):
                continue
            used.append((x,z))
            start = (x, bottoms[x,z]+1, z)
            side = -1 if (group+ring)%2 else 1
            length = 6 + (group+ring)%4
            control = (x+dx*length*.35-dz*side*2, start[1]-4, z+dz*length*.35+dx*side*2)
            end = (x+dx*length-dz*side*3, -5-(group*2+ring)%5, z+dz*length+dx*side*3)
            strand(start, control, end, 2.0 if ring < 2 else 1.65)
            # A smaller fork leaves the main strand halfway down; different
            # endpoints leave genuine air channels rather than a shared skirt.
            branch = tuple((start[k]+2*control[k]+end[k])/4 for k in range(3))
            tip = (branch[0]+dx*4+dz*side*3, end[1]+2, branch[2]+dz*4-dx*side*3)
            bend = ((branch[0]+tip[0])/2, branch[1]-2, (branch[2]+tip[2])/2)
            strand(branch, bend, tip, 1.15)

    added = set(result)-set(art)
    connected = {p for p in added if any('_log[' in art.get(tuple(a+b for a,b in zip(p,d)), '') for d in N6)}
    queue = deque(connected)
    while queue:
        p = queue.popleft()
        for d in N6:
            q = tuple(a+b for a,b in zip(p,d))
            if q in added and q not in connected:
                connected.add(q)
                queue.append(q)
    # Voxelized sub-block tip fragments can meet only diagonally. Omit these
    # new fragments; accepted source art is never touched.
    for p in added-connected:
        del result[p]
    assert all(result[p] == s for p,s in art.items())
    return result, {'strands': paths, 'new_wood_cells': len(connected),
                    'new_wood_face_connected': len(connected),
                    'disconnected_tip_cells_omitted': len(added-connected),
                    'extruded_footprint_columns': 0,
                    'max_new_wood_y_before_padding': max(p[1] for p in connected)}
