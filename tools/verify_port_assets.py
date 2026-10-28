"""Resolve ported item models and trim palettes against the actual client asset JAR."""
from __future__ import annotations
import argparse,json,zipfile
from pathlib import Path


def verify(artifact: Path,client: Path) -> dict:
    checked=0
    with zipfile.ZipFile(artifact) as mod,zipfile.ZipFile(client) as vanilla:
        own=set(mod.namelist());native=set(vanilla.namelist())
        def require(identifier,kind):
            nonlocal checked
            if identifier.startswith('#'):return
            namespace,path=identifier.split(':',1) if ':' in identifier else ('minecraft',identifier)
            suffix='.png' if kind=='textures' else '.json'
            name=f'assets/{namespace}/{kind}/{path}{suffix}'
            if name not in own and name not in native:raise ValueError('Missing '+name)
            checked+=1
        for name in sorted(own):
            if name.startswith('assets/relics/models/') and name.endswith('.json'):
                data=json.loads(mod.read(name))
                if 'parent' in data:require(data['parent'],'models')
                for value in data.get('textures',{}).values():require(value,'textures')
                for override in data.get('overrides',[]):require(override['model'],'models')
            if '/atlases/' in name and name.endswith('.json'):
                for source in json.loads(mod.read(name))['sources']:
                    if source['type']!='minecraft:paletted_permutations':continue
                    require(source['palette_key'],'textures')
                    for value in source['permutations'].values():require(value,'textures')
                    for value in source['textures']:require(value,'textures')
    return {'asset_references_checked':checked,'client':client.name,'passed':True}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('--client',type=Path,required=True)
    a=p.parse_args();print(json.dumps(verify(a.artifact,a.client),indent=2))
