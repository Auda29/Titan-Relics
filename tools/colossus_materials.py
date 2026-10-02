"""Deterministic palette-only study and shape-preserving Sponge v2 serialization."""
from collections import deque
import gzip
import struct

from relic_assets import named, nbt_payload

NEIGHBORS=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))


def metal_family(state):
    if state in ("minecraft:exposed_copper","minecraft:exposed_cut_copper",
                 "minecraft:cut_copper","minecraft:weathered_copper"):
        return "copper"
    if state=="minecraft:raw_iron_block": return "iron"
    return None


def remap(blocks,design,spec):
    if "panel_salvage" in spec:
        return remap_panels(blocks,design,spec)
    low,high=design["source_bounds_blender"]
    scale=design["blocks_per_source_unit"]
    def source(p): return (p[0]/scale+low[0],p[1]/scale+low[2],p[2]/scale-high[1])
    retained=set()
    zones=[]
    for zone in spec["salvage_zones"]:
        distances={p:sum((a-b)**2 for a,b in zip(source(p),zone["center_source"]))
                   for p,state in blocks.items() if metal_family(state)==zone["family"] and p not in retained}
        eligible={p for p,d in distances.items() if d<=zone["radius_source"]**2}
        if not eligible: raise ValueError(f"No existing metal in salvage zone: {zone['name']}")
        seed=min(eligible,key=lambda p:(distances[p],p))
        queue=deque([seed]);seen={seed};selected=[]
        while queue and len(selected)<zone["max_blocks"]:
            p=queue.popleft();selected.append(p)
            neighbors=[tuple(a+b for a,b in zip(p,delta)) for delta in NEIGHBORS]
            for q in sorted(neighbors,key=lambda q:(distances.get(q,float('inf')),q)):
                if q in eligible and q not in seen:
                    seen.add(q);queue.append(q)
        retained.update(selected)
        zones.append({**zone,"blocks":len(selected),"positions_nbt":sorted(selected)})
    result={p:(s if p in retained else spec["replacements"].get(s,s)) for p,s in blocks.items()}
    assert result.keys()==blocks.keys()
    return result,zones


def components(positions):
    """Face-connected components, including pre-existing isolated export fragments."""
    unseen=set(positions)
    result=[]
    while unseen:
        seed=min(unseen);unseen.remove(seed)
        pending=[seed];group={seed}
        while pending:
            x,y,z=pending.pop()
            for dx,dy,dz in NEIGHBORS:
                q=(x+dx,y+dy,z+dz)
                if q in unseen:
                    unseen.remove(q);group.add(q);pending.append(q)
        result.append(group)
    return sorted(result,key=lambda c:(-len(c),min(c)))


def preserve_connections(blocks,removable,width=1):
    """Keep permanent backing paths so mining cannot split any original component.

    Existing disconnected fragments are not silently joined by adding geometry.
    Each surviving original component must remain one face-connected component.
    Shortest paths minimize how much proposed copper must become permanent stone.
    """
    restored=set()
    for original in components(blocks):
        available=original & removable
        if not available: continue
        remaining=original-removable
        groups=components(remaining)
        if len(groups)<2: continue
        anchor=groups[0]
        distance={p:0 for p in anchor};parent={}
        queue=deque(sorted(anchor))
        while queue:
            p=queue.popleft()
            for d in NEIGHBORS:
                q=tuple(a+b for a,b in zip(p,d))
                if q not in original: continue
                weight=int(q in removable)
                cost=distance[p]+weight
                if cost<distance.get(q,float('inf')):
                    distance[q]=cost;parent[q]=p
                    if weight: queue.append(q)
                    else: queue.appendleft(q)
        paths=set()
        for group in groups[1:]:
            p=min(group,key=lambda p:(distance[p],p))
            while p not in anchor and p not in paths:
                paths.add(p);p=parent[p]
        permanent=paths & removable
        # Broaden the protected paths within existing geometry; never add blocks.
        for _ in range(width):
            permanent|={q for p in permanent for d in NEIGHBORS
                        if (q:=tuple(a+b for a,b in zip(p,d))) in available}
        restored|=permanent
    return removable-restored,restored


def remap_panels(blocks,design,spec):
    low,high=design["source_bounds_blender"];scale=design["blocks_per_source_unit"]
    def source(p): return (p[0]/scale+low[0],p[1]/scale+low[2],p[2]/scale-high[1])
    coordinates={p:source(p) for p in blocks}
    groups=[];selected=set()
    for panel in spec["panel_salvage"]:
        lo,hi=panel["bounds_source"]
        positions={p for p,state in blocks.items() if metal_family(state)=="copper"
                   and all(a<=v<=b for v,a,b in zip(coordinates[p],lo,hi))}-selected
        selected|=positions
        groups.append((panel,positions))
    # Keep the initial study's small iron site, independently of the larger panels.
    iron_spec={**spec,"salvage_zones":[z for z in spec["salvage_zones"] if z["family"]=="iron"]}
    iron_spec.pop("panel_salvage")
    _,iron_zones=remap(blocks,design,iron_spec)
    for zone in iron_zones: selected.update(map(tuple,zone["positions_nbt"]))
    selected,restored=preserve_connections(blocks,selected,spec["support_path_width"])
    zones=[]
    for panel,positions in groups:
        kept=positions & selected;lo,hi=panel["bounds_source"]
        zones.append({**panel,"family":"copper","center_source":[(a+b)/2 for a,b in zip(lo,hi)],
                      "radius_source":max(b-a for a,b in zip(lo,hi))/2,
                      "candidate_blocks":len(positions),"protected_backing_blocks":len(positions-kept),
                      "blocks":len(kept),"positions_nbt":sorted(kept)})
    for zone in iron_zones:
        kept=set(map(tuple,zone["positions_nbt"])) & selected
        zones.append({**zone,"blocks":len(kept),"positions_nbt":sorted(kept)})
    result={p:(state if p in selected else spec["replacements"].get(state,state)) for p,state in blocks.items()}
    copper=sum(metal_family(s)=="copper" for s in result.values())
    iron=9*sum(metal_family(s)=="iron" for s in result.values())
    assert copper<spec["resource_limits_exclusive"]["copper_blocks"]
    assert iron<spec["resource_limits_exclusive"]["raw_iron_items"]
    assert result.keys()==blocks.keys()
    return result,zones


def encode_schematic(blocks,size,data_version,offset):
    """Write a blocks-only Sponge v2 schematic, preserving the supplied grid origin."""
    if len(size)!=3 or any(type(n) is not int or not 0<n<=32767 for n in size):
        raise ValueError("Invalid schematic dimensions")
    if any(not all(0<=v<n for v,n in zip(p,size)) for p in blocks):
        raise ValueError("Block outside schematic bounds")
    if len(offset)!=3 or data_version<=0: raise ValueError("Invalid export metadata")
    palette=["minecraft:air"]+sorted(set(blocks.values())-{"minecraft:air"})
    lookup={s:i for i,s in enumerate(palette)}
    def varint(n):
        result=bytearray()
        while n>127:
            result.append((n&127)|128);n>>=7
        result.append(n)
        return bytes(result)
    encoded=[varint(i) for i in range(len(palette))]
    width,height,length=size
    data=b"".join(encoded[lookup[blocks.get((x,y,z),"minecraft:air")]]
                   for y in range(height) for z in range(length) for x in range(width))
    fields=b"".join(named(3,k,struct.pack(">i",v)) for k,v in
                    [("Version",2),("DataVersion",data_version),("PaletteMax",len(palette))])
    fields+=b"".join(named(2,k,struct.pack(">h",v)) for k,v in zip(("Width","Height","Length"),size))
    fields+=named(11,"Offset",struct.pack(">i",3)+struct.pack(">iii",*offset))
    fields+=named(10,"Palette",nbt_payload(10,{s:(3,i) for i,s in enumerate(palette)}))
    fields+=named(7,"BlockData",struct.pack(">i",len(data))+data)
    fields+=named(9,"BlockEntities",nbt_payload(9,(10,[])))
    raw=bytearray(gzip.compress(named(10,"Schematic",fields+b"\0"),mtime=0))
    raw[9]=255
    return bytes(raw)
