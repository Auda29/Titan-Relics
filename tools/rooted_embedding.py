"""Model-first embedding: native ground, downward root continuations, no soil pads."""
import math
from collections import deque

from deposit_relief import noise

WOOD = 'minecraft:spruce_log[axis=y]'


def remove_terrain(blocks, materials, *, tree=False, old_ground=8):
    terrain = {s for k, s in materials.items() if k.startswith('terrain_')}
    terrain -= {s for k, s in materials.items() if not k.startswith('terrain_')}
    # Only the explicitly mutable, low contact moss belongs to the ground pads.
    def ground(p, s):
        return s in terrain or (tree and s == materials['moss'] and p[1] <= old_ground + 5)
    art = {p: s for p, s in blocks.items() if not ground(p, s)}
    return art, {'removed_terrain_cells': len(blocks) - len(art), 'terrain_states': sorted(terrain)}


def grow_roots(art, size, ground=8):
    """Continue the existing low wood footprint with tapering buried toes and forks.

    Every original art cell is immutable. Depth follows footprint thickness;
    thin tips end sooner than the trunk and major buttresses. New forks follow
    the seven existing radial root groups, rather than a circular ground mound.
    """
    result = dict(art)
    bottoms = {}
    for (x, y, z), state in art.items():
        if '_log[' in state and y <= ground + 2:
            bottoms[x, z] = min(y, bottoms.get((x, z), y))
    distances = {}
    queue = deque()
    neighbors = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for x, z in bottoms:
        if any((x + dx, z + dz) not in bottoms for dx, dz in neighbors):
            distances[x, z] = 0
            queue.append((x, z))
    while queue:
        x, z = queue.popleft()
        for dx, dz in neighbors:
            q = x + dx, z + dz
            if q in bottoms and q not in distances:
                distances[q] = distances[x, z] + 1
                queue.append(q)
    for (x, z), top in sorted(bottoms.items()):
        bottom = -2 - min(8, int(distances[x, z] * 1.5)) - int(2 * noise(x, z, 11))
        for y in range(bottom, top):
            result.setdefault((x, y, z), WOOD)

    # Determine the actual trunk center from a solid section of the accepted NBT.
    trunk = [(x, z) for (x, y, z), s in art.items() if y == 30 and '_log[' in s]
    cx = sum(x for x, z in trunk) / len(trunk)
    cz = sum(z for x, z in trunk) / len(trunk)
    grafts = []
    for index, degrees in enumerate((-157, -102, -39, 24, 71, 131, 173)):
        angle = math.radians(degrees)
        dx, dz = math.cos(angle), math.sin(angle)
        candidates = [(x, z) for x, z in bottoms if
                      (x - cx) * dx + (z - cz) * dz > 25 and
                      abs((x - cx) * dz - (z - cz) * dx) < 12]
        if not candidates:
            raise ValueError(f'Missing accepted root group near {degrees} degrees')
        x, z = max(candidates, key=lambda p: (p[0] - cx) * dx + (p[1] - cz) * dz)
        start = (x, bottoms[x, z] + 1, z)
        for side in (-1, 1):
            length = 8 + (index * 3 + side) % 5
            end = (x + dx * length - dz * side * 3,
                   -7 - index % 4, z + dz * length + dx * side * 3)
            middle = (x + dx * length * .55 - dz * side,
                      min(start[1] - 3, 0), z + dz * length * .55 + dx * side)
            for step in range(49):
                t = step / 48
                center = [start[i] * (1 - t) ** 2 + 2 * middle[i] * t * (1 - t) + end[i] * t ** 2 for i in range(3)]
                radius = 2.2 * (1 - t) + .65 * t
                for xx in range(math.floor(center[0] - radius), math.ceil(center[0] + radius) + 1):
                    for yy in range(math.floor(center[1] - radius), math.ceil(center[1] + radius) + 1):
                        for zz in range(math.floor(center[2] - radius), math.ceil(center[2] + radius) + 1):
                            if (0 <= xx < size[0] and 0 <= zz < size[2] and -12 <= yy <= ground + 2
                                    and sum((a - b) ** 2 for a, b in zip((xx, yy, zz), center)) <= radius ** 2):
                                result.setdefault((xx, yy, zz), WOOD)
            grafts.append({'start': list(start), 'control': list(middle), 'end': list(end)})
    added = set(result) - set(art)
    # Independently prove that every new cell is face-connected to original wood.
    attached = set()
    queue = deque()
    n6 = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    for p in added:
        if any('_log[' in art.get(tuple(a + b for a, b in zip(p, d)), '') for d in n6):
            attached.add(p)
            queue.append(p)
    while queue:
        p = queue.popleft()
        for d in n6:
            q = tuple(a + b for a, b in zip(p, d))
            if q in added and q not in attached:
                attached.add(q)
                queue.append(q)
    if attached != added:
        raise ValueError(f'{len(added - attached)} new root cells lack an original-wood connection')
    assert all(result[p] == s for p, s in art.items())
    return result, {'root_columns_continued': len(bottoms), 'new_wood_cells': len(added),
                    'new_wood_face_connected': len(attached), 'forks': grafts,
                    'max_new_wood_y_before_padding': max(p[1] for p in added)}
