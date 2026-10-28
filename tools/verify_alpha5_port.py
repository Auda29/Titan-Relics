"""Check player artifacts against all frozen Alpha 5 template and target contracts."""
from __future__ import annotations
import argparse,gzip,hashlib,json,tomllib
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
VERSION='0.1.0-alpha.5.0.1'


def verify(path: Path,loader: str,minecraft: str) -> dict:
    with zipfile.ZipFile(path) as archive:
        names=archive.namelist()
        if len(names)!=len(set(names)):raise ValueError('Duplicate archive entries')
        java=21 if minecraft=='1.21.1' else 25
        if loader=='fabric':
            metadata=json.loads(archive.read('fabric.mod.json'))
            if metadata['id']!='relics' or metadata['version']!=VERSION or metadata['depends']['minecraft']!=minecraft:
                raise ValueError('Wrong version/loader/game target')
            if metadata['depends']['java']!='>='+str(java):raise ValueError('Wrong minimum Java version')
        elif loader=='neoforge':
            if 'fabric.mod.json' in names:raise ValueError('Fabric metadata in native archive')
            metadata=tomllib.loads(archive.read('META-INF/neoforge.mods.toml').decode())
            from prepare_alpha5_neoforge import TARGETS
            target=TARGETS[minecraft]
            if len(metadata['mods'])!=1 or metadata['mods'][0]['modId']!='relics' or metadata['mods'][0]['version']!=VERSION:raise ValueError('Wrong native mod metadata')
            dependencies={d['modId']:d for d in metadata['dependencies']['relics']}
            if set(dependencies)!={'minecraft','neoforge','lithostitched'}:raise ValueError('Wrong native dependencies')
            for mod,version in (('minecraft',f'[{minecraft}]'),('neoforge',f"[{target['neo']},)"),('lithostitched','[1.8.0]')):
                if dependencies[mod]['versionRange']!=version or dependencies[mod]['type']!='required':raise ValueError('Wrong native target pin')
        else:raise ValueError('Unknown loader')
        templates=set();manifests=[]
        for name in names:
            if not(name.startswith('relics.') and name.endswith('integration.json')):continue
            manifest=json.loads(archive.read(name));manifests.append(name)
            if manifest.get('compatibility_target')!=minecraft:raise ValueError('Missing compatibility contract: '+name)
            if loader=='neoforge' and manifest.get('loader')!='neoforge':raise ValueError('Wrong manifest loader')
            for entry in manifest['structures']:
                for field in ('single_template','worldgen_template'):
                    template='data/relics/structure/'+entry[field]['path'];templates.add(template)
                    if hashlib.sha256(archive.read(template)).hexdigest()!=entry[field]['sha256']:raise ValueError('Template binding mismatch: '+template)
        if len(manifests)!=6 or len(templates)!=40:raise ValueError('Missing frozen interior revision/template')
        if {n for n in names if n.endswith('.nbt')}!=templates:raise ValueError('Extra or missing templates')
        classes=[n for n in names if n.endswith('.class')]
        if not classes:raise ValueError('No runtime code')
        for name in classes:
            data=archive.read(name)
            if not name.startswith('de/relics/') or any(s in name for s in ('Checks','Tests','testmixin','validation/')):
                raise ValueError('Unexpected/test-only class in player artifact: '+name)
            if data[:4]!=bytes.fromhex('cafebabe') or int.from_bytes(data[6:8],'big')!=java+44:raise ValueError('Wrong Java class target: '+name)
            if loader=='neoforge' and b'net/fabricmc/' in data:raise ValueError('Fabric API in native class: '+name)
        if any(n.endswith('.jar') for n in names):raise ValueError('Bundled dependency JAR')
        mixins=json.loads(archive.read('relics.mixins.json'))
        if not mixins['required'] or mixins['compatibilityLevel']!='JAVA_'+str(java):raise ValueError('Wrong mixin target')
        for name in mixins['mixins']:
            if mixins['package'].replace('.','/')+'/'+name+'.class' not in classes:raise ValueError('Missing required mixin: '+name)
        substitutions=json.loads(archive.read('relics.gameplay.tree_skull.integration.json')).get('block_substitutions',{})
    return {'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'loader':loader,'minecraft':minecraft,
            'version':VERSION,'java_class_major':java+44,'templates':len(templates),'frozen_manifests':len(manifests),'runtime_classes':len(classes),'block_substitutions':substitutions,'passed':True}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('--loader',default='fabric');p.add_argument('--minecraft',default='1.21.1')
    a=p.parse_args();print(json.dumps(verify(a.artifact,a.loader,a.minecraft),indent=2))
