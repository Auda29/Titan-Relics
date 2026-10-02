"""Shared deterministic V4 deposit fields; pure math is also used by validation."""
import math


def lobe(x, z, cx, cz, rx, rz, height, angle=0):
    a = math.radians(angle)
    dx, dz = x-cx, z-cz
    u, v = (dx*math.cos(a)+dz*math.sin(a))/rx, (-dx*math.sin(a)+dz*math.cos(a))/rz
    theta = math.atan2(v, u)
    edge = 1+.09*math.sin(theta*3+.7)+.05*math.sin(theta*7)
    f = max(0, 1-(u*u+v*v)/(edge*edge))
    return height*f*f*(1+.04*math.sin(x*.43+z*.31))


def skull_height(x, z):
    lobes = [(-17, 7, 27, 27, 11, -18), (17, 19, 29, 34, 19, 23),
             (1, 25, 24, 31, 24, -8), (2, 42, 20, 15, 17, 16),
             (15, 65, 21, 18, 10, -15), (22, 90, 28, 37, 14, 21),
             (33, 112, 24, 25, 11, -17), (29, 142, 20, 18, 4.6, 12),
             (-34, -6, 18, 12, 3.4, -20), (52, 109, 17, 11, 3.2, 34)]
    height = max(lobe(x,z,*p) for p in lobes)
    # Real gaps exposing native terrain at both spinal dislocations.
    for center, half_width in [(54, 3.5), (131, 3)]:
        fade = min(1, max(0, (abs(z-center)-half_width)/3))
        height *= fade*fade*(3-2*fade)
    # Keep the mouth approach and central oral cavity low.
    corridor = max(0, 1-abs(x)/13)*max(0, min(1, (8-z)/10))
    height = height*(1-corridor)+min(height, 2)*corridor
    return height if height >= .22 else 0


def obelisk_height(x, z):
    height = max(lobe(x,z,*p) for p in [(-15, 4, 16, 23, 3.3, -30),
                 (10, 14, 20, 13, 2.4, 25), (11,-16, 13, 18, 1.8, -18)])
    return height if height >= .2 else 0


def deposit_floor(height, depth):
    # The foundation tapers to the edge, rather than forming a flat buried slab.
    return -depth*min(1, height/6)


def build_deposits(height_fn, xs, zs, depth=8, spacing=.7):
    """Closed top/bottom surfaces plus dense slices; never fill skull cavities.

    Materials terrain_top/terrain_patch/terrain_fill must already exist in Blender.
    """
    import bpy
    from create_blender_colossus import xyz
    from create_titan_skull_v2 import mesh_object
    vertices, faces, materials, triangles = [], [], [], []
    for z in zs:
        for x in xs:
            h = height_fn(x,z)
            vertices.append(xyz((x,h,z)))
    n, count = len(xs), len(vertices)
    vertices += [xyz((x, deposit_floor(height_fn(x,z),depth),z)) for z in zs for x in xs]
    edge_counts = {}
    for j in range(len(zs)-1):
        for i in range(n-1):
            a = j*n+i
            for face in [(a,a+n,a+1),(a+1,a+n,a+n+1)]:
                points = [(vertices[k][0], vertices[k][2], -vertices[k][1]) for k in face]
                if max(p[1] for p in points) == 0:
                    continue
                faces.extend([face,tuple(k+count for k in reversed(face))])
                cx, cz = sum(p[0] for p in points)/3, sum(p[2] for p in points)/3
                patch = math.sin(cx*.16+cz*.09)+.55*math.sin(cz*.26-cx*.12) > 1.02
                materials.extend([int(patch),2])
                triangles.append(points)
                for p,q in zip(face,face[1:]+face[:1]):
                    key=tuple(sorted((p,q)))
                    edge_counts[key]=edge_counts.get(key,0)+1
    for (a,b), edges in edge_counts.items():
        if edges == 1 and (vertices[a]!=vertices[a+count] or vertices[b]!=vertices[b+count]):
            faces.append((a,b,b+count,a+count))
            materials.append(2)
    mesh_object("V4 | Separate tapered deposits",vertices,faces,
                ["terrain_top","terrain_patch","terrain_fill"],materials)
    # Clip triangular height prisms at each horizontal slice using both surfaces.
    def clip(poly, field, level, keep_above):
        result=[]
        for a,b in zip(poly,poly[1:]+poly[:1]):
            va,vb=a[field]-level,b[field]-level
            inside_a=va>=0 if keep_above else va<=0
            inside_b=vb>=0 if keep_above else vb<=0
            if inside_a: result.append(a)
            if inside_a != inside_b:
                t=va/(va-vb)
                result.append(tuple(a[k]+t*(b[k]-a[k]) for k in range(4)))
        return result
    vertices,faces=[],[]
    top=max(p[1] for triangle in triangles for p in triangle)
    for layer in range(math.ceil((top+depth)/spacing)):
        level=-depth+layer*spacing
        for triangle in triangles:
            poly=[(x,y,z,deposit_floor(y,depth)) for x,y,z in triangle]
            if max(p[1] for p in poly)<level or min(p[3] for p in poly)>level:
                continue
            poly=clip(poly,1,level,True)
            if poly: poly=clip(poly,3,level,False)
            if len(poly)<3: continue
            start=len(vertices)
            vertices.extend(xyz((p[0],level,p[2])) for p in poly)
            faces.append(tuple(range(start,start+len(poly))))
    mesh_object("V4 | Solid deposit interior slices",vertices,faces,["terrain_fill"])
