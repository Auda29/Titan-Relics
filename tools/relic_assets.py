#!/usr/bin/env python3
"""Generate original Relic alpha block geometry and deterministic Java structure NBT.

No third-party libraries. Coordinates are X/Y/Z, front is negative Z. A missing
coordinate preserves existing terrain; minecraft:air deliberately removes it.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
import gzip
import hashlib
import json
import math
from pathlib import Path
import struct

AIR = "minecraft:air"
Pos = tuple[int, int, int]


def noise(x: int, y: int, z: int, seed: int) -> float:
    """Stable coordinate hash, independent of iteration order and Python hash seed."""
    n = (x * 374761393 + y * 668265263 + z * 2147483647 + seed * 1274126177) & 0xffffffff
    n = ((n ^ (n >> 13)) * 1274126177) & 0xffffffff
    return ((n ^ (n >> 16)) & 0xffffffff) / 4294967296


@dataclass
class Model:
    id: str
    size: Pos
    ground_y: int
    seed: int
    blocks: dict[Pos, str] = field(default_factory=dict)
    landmarks: dict = field(default_factory=dict)

    def put(self, x: int, y: int, z: int, block: str) -> None:
        if not (0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.size[2]):
            raise ValueError(f"{self.id}: outside model bounds: {(x,y,z)}")
        self.blocks[x, y, z] = block if ":" in block else "minecraft:" + block

    def box(self, lo: Pos, hi: Pos, block: str) -> None:
        for x in range(lo[0], hi[0] + 1):
            for y in range(lo[1], hi[1] + 1):
                for z in range(lo[2], hi[2] + 1):
                    self.put(x, y, z, block)

    def ellipsoid(self, center, radius, block, inner=0.0) -> None:
        for x in range(max(0, math.floor(center[0]-radius[0])), min(self.size[0], math.ceil(center[0]+radius[0])+1)):
            for y in range(max(0, math.floor(center[1]-radius[1])), min(self.size[1], math.ceil(center[1]+radius[1])+1)):
                for z in range(max(0, math.floor(center[2]-radius[2])), min(self.size[2], math.ceil(center[2]+radius[2])+1)):
                    d = sum(((v-c)/r)**2 for v,c,r in zip((x,y,z),center,radius))
                    if inner <= d <= 1:
                        self.put(x,y,z,block(x,y,z,d) if callable(block) else block)


def obelisk(seed: int = 2913) -> Model:
    m = Model("obelisk", (25, 70, 25), 3, seed)
    # An irregular low sandstone skirt, never a rectangular air clearing.
    for x in range(25):
        for z in range(25):
            r = ((x-12)/12)**2 + ((z-12)/11)**2
            if r < .90 + .13*math.sin(x*.6) + .08*math.cos(z):
                top = max(0, int(3.8 - r*3 + .6*math.sin(x*.4+z*.3)))
                for y in range(top+1):
                    m.put(x,y,z,"sandstone" if y<top else "sand")
    m.box((7,1,7),(17,3,17),"cut_sandstone")
    m.box((8,4,8),(16,5,16),"smooth_sandstone")
    for x in range(9,16):
        for y in range(6,70):
            for z in range(9,16):
                # Restrained seam on one face; broad uninterrupted planes elsewhere.
                edge = x in (9,15) and z in (9,15)
                material = "polished_deepslate" if edge else "deepslate_tiles"
                if z == 9 and x == 12 and 13 < y < 47:
                    material = "polished_basalt"
                if y < 12 and noise(x,y,z,seed) < .13:
                    material = "cracked_deepslate_tiles"
                if x == 15 and z == 9 and 50 <= y < 55:
                    continue
                m.put(x,y,z,material)
    # A later traveller's low broken shelter, human-sized beside the monument.
    m.box((3,2,15),(3,3,20),"sandstone")
    m.box((4,2,20),(6,2,20),"sandstone")
    # Connected fractures cut into a darker core instead of random surface speckles.
    for low, high, phase in ((18, 36, 0), (47, 63, 2)):
        for y in range(low, high):
            x = 11 + ((y // 4 + phase) % 4)
            m.put(x,y,9,AIR)
            m.put(x,y,10,"polished_basalt")
            m.put(max(9,x-1),y,9,"cracked_deepslate_tiles")
            if y % 5 < 2:
                m.put(min(15,x+1),y,9,AIR)
    for y in range(30,53):
        z = 11 + ((y // 5) % 3)
        m.put(15,y,z,AIR)
        m.put(14,y,z,"polished_basalt")
        m.put(15,y,min(15,z+1),"cracked_deepslate_tiles")
    # Two large edge losses leave the flat-topped monolith recognizable.
    for y in range(34,42):
        for x,z in ((9,9),(9,10),(10,9)):
            if y < 40 or x == z:
                m.put(x,y,z,AIR)
    for y in range(63,70):
        m.put(15,y,15,AIR)
        if y >= 67:
            m.put(14,y,15,AIR)
            m.put(15,y,14,AIR)
    # Windward sand banks cover parts of the plinth, with supported sand caps.
    for x in range(4,22):
        for z in range(4,22):
            r = ((x-9)/9)**2 + ((z-15)/8)**2
            top = int(6.5-4*r+.7*math.sin(z*.7))
            if top < 1 or (9 <= x <= 15 and 9 <= z <= 15):
                continue
            for y in range(top+1):
                if y < 6 or (x,y,z) not in m.blocks:
                    m.put(x,y,z,"sand" if y == top else "sandstone")
    for cx,cz in ((18,9),(19,16),(7,6)):
        m.ellipsoid((cx,3,cz),(2,2,2),"cobbled_deepslate")
    m.landmarks = {"shaft": {"origin":[9,6,9],"size":[7,64,7]}, "resting_place":[5,3,18],
                   "fractures":{"front_y":[18,63],"right_y":[30,53]}, "sand_bank":[8,5,15]}
    return m


def colossus(seed: int = 2913) -> Model:
    m = Model("colossus", (100, 66, 76), 10, seed)

    def armor(x,y,z,d=0):
        # Large coherent panel fields rather than per-block metallic confetti.
        if y % 11 == 0 or x in (27,53):
            return "polished_deepslate"
        return "deepslate_tiles" if noise(x//5,y//5,z//5,seed)>.18 else "cracked_deepslate_tiles"

    # Buried waist, barrel chest, two different shoulder states and a neck collar.
    m.ellipsoid((40,8,39),(22,11,17),armor)
    m.ellipsoid((40,26,39),(23,22,17),armor)
    m.ellipsoid((16,36,39),(12,11,13),armor)
    m.ellipsoid((64,35,39),(10,10,11),"polished_deepslate")
    # Left upper arm remains attached and rests against the ground.
    m.ellipsoid((12,20,40),(8,19,10),armor)
    m.ellipsoid((13,7,34),(9,7,12),"deepslate_tiles")
    m.ellipsoid((40,45,40),(10,5,10),"polished_deepslate")
    # Helmet: stepped bevels and a projecting brow, not a spherical cartoon head.
    for y in range(46,65):
        bevel = max(0,y-60)
        for x in range(29+bevel,52-bevel):
            for z in range(30+bevel//2,51-bevel//2):
                if abs(x-40)+abs(z-40)<21-bevel:
                    m.put(x,y,z,armor(x,y,z))
    m.box((28,55,28),(52,57,31),"polished_deepslate")
    m.box((31,51,29),(49,54,31),"black_concrete")
    m.box((38,48,28),(42,52,30),"polished_deepslate")
    # Asymmetric missing helmet corner exposes a dark layer.
    for x in range(47,52):
        for y in range(58,64):
            for z in range(30,37):
                m.blocks.pop((x,y,z),None)
    # Only narrow oxidized metal rings: resources are a visible, limited accent.
    for x in range(27,54):
        for y in range(13,39):
            r = math.hypot(x-40,y-26)
            if 10.4 < r < 12:
                m.put(x,y,23,"waxed_weathered_cut_copper")
                m.put(x,y,24,"polished_deepslate")
    # Deliberately hollow machine room. Explicit air survives hills at placement.
    m.ellipsoid((40,26,39),(17,17,12),AIR)
    # Circular broken chest aperture connects the room to daylight.
    for x in range(29,52):
        for y in range(16,37):
            if (x-40)**2 + (y-26)**2 < 10**2:
                for z in range(20,33):
                    m.put(x,y,z,AIR)
    # Main accessible entrance stays at one floor height. No jump puzzle needed.
    m.box((35,9,23),(45,9,44),"cobbled_deepslate")
    m.box((36,10,23),(44,16,42),AIR)
    # Short, worn apron. The three-block central walk remains continuous.
    for z in range(14,23):
        half_width = 2 + (z-14)//3
        for x in range(40-half_width,41+half_width):
            edge = abs(x-40) > 1
            if edge and noise(x,9,z,seed) < .36:
                continue
            m.put(x,9,z,"cobbled_deepslate" if not edge or noise(x,0,z,seed)>.4 else "moss_block")
            # Buried support prevents floating pavement on uneven sites.
            for y in range(9):
                m.put(x,y,z,"dirt")
        m.box((39,10,z),(41,12,z),AIR)
    m.box((29,9,31),(51,9,47),"deepslate_tiles")
    m.box((30,10,30),(50,17,47),AIR)
    # Deep internal ribs and a ring lying at the back of the room.
    for x in (28,52):
        m.box((x,10,35),(x+1,28,37),"polished_basalt")
    for x in range(32,49):
        for y in range(12,29):
            if 6 < math.hypot(x-40,y-20) < 8:
                m.put(x,y,49,"polished_deepslate")
    # Small later shelter and workbench inside one protected edge. No loot/BE.
    m.box((30,10,40),(30,13,44),"oak_log")
    m.box((30,14,40),(34,14,44),"oak_planks")
    m.put(31,10,43,"crafting_table")
    # A daylight break in the right upper chest keeps the chamber legible.
    m.box((45,35,32),(49,44,36),AIR)

    # Detached forearm, with an exposed joint and readable separated fingers.
    m.ellipsoid((83,9,27),(8,8,10),"polished_deepslate")
    m.ellipsoid((85,8,42),(8,7,18),armor)
    m.ellipsoid((85,6,58),(9,5,8),"deepslate_tiles")
    for i in range(4):
        x = 78+i*5
        m.box((x,3,61),(x+2,6,69-(i%2)*2),"polished_deepslate")
    m.ellipsoid((74,5,57),(3,3,7),"deepslate_tiles")
    weather_colossus(m)
    # Earth collects around the lower body and forearm, never above the doorway.
    for cx,cz,rx,rz,peak in ((39,41,31,25,9),(84,45,14,26,5),(40,23,12,12,9)):
        for x in range(max(0,cx-rx),min(100,cx+rx+1)):
            for z in range(max(0,cz-rz),min(76,cz+rz+1)):
                r = ((x-cx)/rx)**2+((z-cz)/rz)**2
                top = int(peak*(1-r)+1.5*math.sin(x*.25+z*.15))
                if top < 0: continue
                for y in range(top+1):
                    if (x,y,z) not in m.blocks:
                        m.put(x,y,z,"grass_block" if y==top else "dirt")
    # Broad moss patches only on actual upward-facing armour. Leaves are persistent.
    top_surfaces = [p for p,b in m.blocks.items() if b != AIR and m.blocks.get((p[0],p[1]+1,p[2]),AIR)==AIR]
    for x,y,z in top_surfaces:
        patch = math.sin(x*.16+seed)+math.cos(z*.19)+math.sin(y*.13)
        exposed_armor = any(word in m.blocks[x,y,z] for word in ("deepslate", "basalt"))
        wet_side = ((x-17)/24)**2 + ((z-41)/24)**2 < 1 or (x<44 and z>40)
        if y>17 and wet_side and patch>-.15 and exposed_armor:
            m.put(x,y,z,"moss_block")
            if noise(x//3,y//3,z//3,seed)>.57 and y+1<66:
                for dy in range(1, 3 if y<62 else 2):
                    if y+dy<66 and m.blocks.get((x,y+dy,z),AIR)==AIR:
                        m.put(x,y+dy,z,"azalea_leaves[persistent=true,distance=1,waterlogged=false]")
    # Long damp streaks follow exposed surfaces on one side of the torso.
    for (x,y,z),block in list(m.blocks.items()):
        if 7<x<29 and 20<y<44 and z<40 and "deepslate" in block:
            if m.blocks.get((x,y,z-1),AIR)==AIR and math.sin(x*.45)+math.cos(y*.13)>.55:
                m.put(x,y,z,"moss_block")
    # Reassert the protected walk so later decoration cannot block it.
    m.box((39,10,14),(41,12,22),AIR)
    m.box((37,10,23),(43,12,44),AIR)
    m.landmarks = {"entrance":[40,10,14],"machine_room":[40,10,40],"chest_aperture":[40,26,23],"detached_arm":[85,8,42],"head":[40,55,39],"protected_walk":{"from":[40,10,14],"to":[40,10,44],"width":3,"clearance":3},
                   "armor_breach":[57,34,32],"broken_helmet":[48,59,34]}
    return m


def weather_colossus(m: Model) -> None:
    """Large readable losses, exposed framing and fallen plates, all authored geometry."""
    # The broken helmet exposes a recessed frame, not another solid front face.
    m.ellipsoid((48,61,33),(9,8,9),AIR)
    for x in (43,47):
        m.box((x,55,38),(x,62,39),"polished_basalt")
    m.box((42,56,38),(49,56,39),"polished_basalt[axis=x]")
    for y in range(48,61):
        x = 33 + (y//4)%3
        for z in (29,30):
            if (x,y,z) in m.blocks:
                m.put(x,y,z,AIR)
    # Right chest and shoulder have lost a large section of outer armour.
    m.ellipsoid((57,34,30),(10,11,9),AIR)
    for x in (52,57,62):
        m.box((x,26,36),(x+1,39-(x-52)//2,37),"polished_basalt")
    m.box((51,29,36),(64,30,37),"polished_basalt[axis=x]")
    m.box((55,31,37),(56,35,38),"waxed_weathered_cut_copper")
    # A missing arc breaks the otherwise pristine breast ring.
    for x in range(46,53):
        for y in range(32,39):
            for z in (23,24):
                m.put(x,y,z,AIR)
    # Gouges run along the detached forearm and expose its longitudinal core.
    for z in range(32,53):
        x = 84+(z//5)%3
        for y in range(11,17):
            if (x,y,z) in m.blocks:
                m.put(x,y,z,AIR)
        m.put(x,10,z,"polished_basalt[axis=z]")
    # Coherent cracked fields border the breaches. Keep the broad dark palette.
    for (x,y,z),block in list(m.blocks.items()):
        if block == "minecraft:deepslate_tiles":
            fracture = abs(x-(30+(y//5)%4))<=1 and z<35 and 20<y<48
            if fracture or (x>48 and z<39 and 25<y<45):
                m.put(x,y,z,"cracked_deepslate_tiles")
    # Tilted plate fragments sink into the soil outside the protected entrance.
    for cx,cz,rx,rz in ((29,19,5,4),(53,17,4,5),(69,30,4,3)):
        for x in range(cx-rx,cx+rx+1):
            for z in range(cz-rz,cz+rz+1):
                if ((x-cx)/rx)**2+((z-cz)/rz)**2 < 1+.1*math.sin(z):
                    top = 8 + (x-cx+rx)//3
                    for y in range(5,top+1):
                        m.put(x,y,z,"cracked_deepslate_tiles" if y==top else "cobbled_deepslate")


# Minimal NBT writer and reader, kept explicit to make serialization auditable.
# Values are (tag id, payload); Java lists retain their element tag even when empty.
def named(tag: int, name: str, payload: bytes) -> bytes:
    raw = name.encode("utf-8")
    return bytes([tag])+struct.pack(">H",len(raw))+raw+payload


def nbt_payload(tag: int, value) -> bytes:
    if tag == 3: return struct.pack(">i",value)
    if tag == 8:
        raw=value.encode("utf-8")
        return struct.pack(">H",len(raw))+raw
    if tag == 9:
        item_tag,values=value
        return bytes([item_tag])+struct.pack(">i",len(values))+b"".join(nbt_payload(item_tag,v) for v in values)
    if tag == 10:
        return b"".join(named(t,k,nbt_payload(t,v)) for k,(t,v) in value.items())+b"\0"
    raise ValueError(f"Unsupported tag {tag}")


def decode_nbt(data: bytes) -> dict:
    """Small independent cursor reader, useful for export validation."""
    if data[:2] == b"\x1f\x8b": data=gzip.decompress(data)
    cursor=0
    def take(n):
        nonlocal cursor
        if n<0: raise ValueError("Negative NBT length")
        result=data[cursor:cursor+n]
        if len(result)!=n: raise ValueError("Truncated NBT")
        cursor+=n
        return result
    def string(): return take(struct.unpack(">H",take(2))[0]).decode("utf-8")
    def value(tag):
        formats={1:(">b",1),2:(">h",2),4:(">q",8),5:(">f",4),6:(">d",8)}
        if tag in formats:
            fmt,length=formats[tag]
            return struct.unpack(fmt,take(length))[0]
        if tag==7: return take(struct.unpack(">i",take(4))[0])
        if tag in (11,12):
            count=struct.unpack(">i",take(4))[0]
            if count<0: raise ValueError("Negative array length")
            fmt,length=(">i",4) if tag==11 else (">q",8)
            return [struct.unpack(fmt,take(length))[0] for _ in range(count)]
        if tag==3: return struct.unpack(">i",take(4))[0]
        if tag==8: return string()
        if tag==9:
            element=take(1)[0]; count=struct.unpack(">i",take(4))[0]
            if count<0: raise ValueError("Negative list length")
            return [value(element) for _ in range(count)]
        if tag==10:
            result={}
            while True:
                child=take(1)[0]
                if child==0: return result
                key=string(); result[key]=value(child)
        raise ValueError(f"Unsupported tag {tag}")
    if take(1)!=b"\x0a": raise ValueError("Expected compound root")
    string(); result=value(10)
    if cursor!=len(data): raise ValueError("Trailing NBT data")
    return result


def block_state(block: str) -> dict:
    name,_,properties=block.partition("[")
    result={"Name":(8,name)}
    if properties:
        result["Properties"]=(10,{k:(8,v) for k,v in (p.split("=",1) for p in properties.rstrip("]").split(","))})
    return result


def encode_structure(blocks: dict[Pos,str], size: Pos, data_version: int, block_entities: dict | None = None) -> bytes:
    if data_version<=0: raise ValueError("DataVersion must be positive")
    palette=sorted(set(blocks.values()))
    lookup={b:i for i,b in enumerate(palette)}
    entries = []
    for p, b in sorted(blocks.items()):
        entry = {"pos": (9, (3, list(p))), "state": (3, lookup[b])}
        if block_entities and p in block_entities:
            entry["nbt"] = (10, block_entities[p])
        entries.append(entry)
    root={"DataVersion":(3,data_version),"size":(9,(3,list(size))),"palette":(9,(10,[block_state(b) for b in palette])),
          "blocks":(9,(10,entries)),"entities":(9,(10,[]))}
    data = bytearray(gzip.compress(named(10,"",nbt_payload(10,root)),mtime=0))
    # Python 3.11/3.12 delegate this header to zlib, whose OS byte varies by host.
    # 255 means unspecified OS and matches Python 3.13+'s canonical gzip header.
    data[9] = 255
    return bytes(data)


def tiles(model: Model, tile_size: int=32):
    if not 1<=tile_size<=128: raise ValueError("tile_size must be 1..128")
    groups=defaultdict(dict)
    for pos,block in model.blocks.items():
        origin=tuple(v//tile_size*tile_size for v in pos)
        local=tuple(v-o for v,o in zip(pos,origin))
        groups[origin][local]=block
    for origin,blocks in sorted(groups.items()):
        size=tuple(min(tile_size,total-o) for total,o in zip(model.size,origin))
        yield origin,size,blocks


def export_models(output: Path, data_version: int, seed=2913, tile_size=32, single_template=False) -> dict:
    manifest={"schema_version":1,"generator":"tools/relic_assets.py","seed":seed,"data_version":data_version,"tile_size":tile_size,
              "coordinate_system":"XYZ; front -Z; tile origins relative to whole structure minimum corner",
              "air_policy":"Missing coordinates preserve terrain. Explicit minecraft:air clears only designed interior/entrance.","structures":[]}
    for model in (obelisk(seed),colossus(seed)):
        parts=[]
        for origin,size,blocks in tiles(model,tile_size):
            relative=f"{model.id}/tile_{origin[0]}_{origin[1]}_{origin[2]}.nbt"
            path=output/relative; path.parent.mkdir(parents=True,exist_ok=True)
            data=encode_structure(blocks,size,data_version); path.write_bytes(data)
            parts.append({"path":relative,"origin":list(origin),"size":list(size),"blocks":len(blocks),"sha256":hashlib.sha256(data).hexdigest()})
        entry={"id":model.id,"size":list(model.size),"ground_y":model.ground_y,"solid_blocks":sum(b!=AIR for b in model.blocks.values()),
               "explicit_air_blocks":sum(b==AIR for b in model.blocks.values()),"palette_counts":dict(sorted(Counter(model.blocks.values()).items())),"landmarks":model.landmarks,"tiles":parts}
        if single_template:
            data=encode_structure(model.blocks,model.size,data_version)
            path=output/f"{model.id}.nbt"; path.write_bytes(data)
            entry["single_template"]={"path":path.name,"sha256":hashlib.sha256(data).hexdigest()}
        manifest["structures"].append(entry)
    return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--data-version",type=int,required=True)
    parser.add_argument("--seed",type=int,default=2913)
    parser.add_argument("--tile-size",type=int,default=32)
    parser.add_argument("--manifest",type=Path,default=Path("structures-src/generated/manifest.json"))
    parser.add_argument("--single-template",action="store_true")
    args=parser.parse_args()
    manifest=export_models(args.output,args.data_version,args.seed,args.tile_size,args.single_template)
    args.manifest.parent.mkdir(parents=True,exist_ok=True)
    args.manifest.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    for model in manifest["structures"]:
        print(f"{model['id']}: {model['size']}, {model['solid_blocks']} solid blocks, {len(model['tiles'])} rigid tiles")


if __name__=="__main__": main()
