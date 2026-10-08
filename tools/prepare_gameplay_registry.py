"""Pin the 26.2 block/property report used by the architectural handoff checks.

Only generated metadata is downloaded; no Minecraft installation is needed.
"""
import hashlib
import json
import urllib.request
from build_gameplay_interiors import ROOT,ASSETS,STEMS,NATIVE
from inspect_ots_result import read_structure

URL='https://raw.githubusercontent.com/misode/mcmeta/26.2-summary/blocks/data.json'
SHA256='0b1470910281d2f7ac36544672fc04befcd600c9dab1574d0636727ae6531726'
OUTPUT=ROOT/'docs/project/reviews/gameplay-registry-26.2.json'

def main():
    cache=ROOT/'.work/interiors/blocks-26.2.json'
    if not cache.exists():
        cache.parent.mkdir(parents=True,exist_ok=True)
        cache.write_bytes(urllib.request.urlopen(URL,timeout=30).read())
    data=cache.read_bytes()
    if hashlib.sha256(data).hexdigest()!=SHA256:raise ValueError('26.2 registry report changed')
    registry=json.loads(data);names={s.removeprefix('minecraft:') for s in NATIVE}
    for name,stem in STEMS.items():
        path=(ROOT/ASSETS[name]['source']).parent.parent/stem/(stem+'.nbt')
        _,blocks=read_structure(path)
        names.update(s.split('[')[0].removeprefix('minecraft:') for s in blocks.values())
    excerpt={'minecraft_version':'26.2','source_url':URL,'source_sha256':SHA256,
             'scope':'Block names, allowed properties and defaults only; not a runtime placement test',
             'blocks':{name:registry[name] for name in sorted(names)}}
    OUTPUT.write_text(json.dumps(excerpt,indent=2)+'\n');print(OUTPUT)

if __name__=='__main__':main()
