"""Build separate modern Fabric validation classes against the actual player JAR."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import zipfile
from compile_worldgen import ROOT,compile_libraries,find_javac
from prepare_alpha5_neoforge import modern_checks,modern_recipe_packet


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--java-home',type=Path,required=True)
    parser.add_argument('--artifact',type=Path,required=True)
    args=parser.parse_args()
    artifact=args.artifact.resolve()
    output=ROOT/'build/fabric26-checks';sources=output/'sources';classes=output/'classes'
    sources.mkdir(parents=True,exist_ok=True);classes.mkdir(parents=True,exist_ok=True)
    originals=[ROOT/'src/test/java/de/relics'/name for name in
               ('GameplayPresentationChecks.java','TreeAuraChecks.java','TreeAnimalChecks.java','TreeAnimalProbeMixin.java')]
    originals +=[ROOT/'compat/alpha5-fabric-1.21.1/src/test/adapters/de/relics'/name
                 for name in ('PortChecks.java','RecipeNetworkChecks.java')]
    generated=[]
    for source in originals:
        text=source.read_text(encoding='utf-8')
        if source.name in ('PortChecks.java','RecipeNetworkChecks.java'):text=modern_checks(text)
        if source.name=='RecipeNetworkChecks.java':text=modern_recipe_packet(text)
        path=sources/source.name;path.write_text(text,encoding='utf-8',newline='\n');generated.append(path)
    command=[str(find_javac(args.java_home)),'--release','25','-encoding','UTF-8','-proc:none','-g:none',
             '-classpath',os.pathsep.join(map(str,[artifact,*compile_libraries()])),'-d',str(classes),*map(str,generated)]
    subprocess.run(command,check=True)
    target=output/'relics-alpha5-port-checks+mc26.2.jar'
    with zipfile.ZipFile(artifact) as player:version=json.loads(player.read('fabric.mod.json'))['version']
    entries={p.relative_to(classes).as_posix():p.read_bytes() for p in classes.rglob('*.class')}
    entries['fabric.mod.json']=json.dumps({'schemaVersion':1,'id':'relics-fabric26-checks','version':'1','environment':'server',
        'entrypoints':{'main':['de.relics.PortChecks','de.relics.GameplayPresentationChecks','de.relics.TreeAuraChecks','de.relics.TreeAnimalChecks']},
        'mixins':['animal-probe.mixins.json'],'depends':{'relics':version}}).encode()
    entries['animal-probe.mixins.json']=json.dumps({'required':True,'package':'de.relics.testmixin','compatibilityLevel':'JAVA_25',
        'mixins':['TreeAnimalProbeMixin'],'injectors':{'defaultRequire':1}}).encode()
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,data in sorted(entries.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.create_system=3;info.external_attr=0o100644<<16
            archive.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    print(json.dumps({'validation_mod':str(target),'artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest()},indent=2))


if __name__=='__main__':main()
