"""Compile/remap isolated Fabric QA sources using existing caches only."""
import os
from pathlib import Path
import subprocess
import zipfile

from compile_worldgen import ROOT, compile_libraries
from test_beta_performance import JAVA, ARTIFACTS


def compile_sources(mc, directory, sources):
    directory.mkdir(parents=True, exist_ok=True)
    java_files=[]
    for name,text in sources.items():
        if mc=='1.21.1':
            from prepare_alpha5_port import legacy_client
            text=legacy_client(text).replace('method="tick"','method="method_1574"').replace('method="tickServer"','method="method_3748"')
            text=text.replace('.lookupOrThrow(','.registryOrThrow(').replace('chunk.getPos().x()','chunk.getPos().x').replace('chunk.getPos().z()','chunk.getPos().z')
            text=text.replace('Screenshot.grab(client,true)','Screenshot.grab(client.gameDirectory,client.getMainRenderTarget(),message->{})')
        file=directory/name;file.write_text(text,encoding='utf-8');java_files.append(file)
    cp=os.pathsep.join(map(str,[ARTIFACTS/f'relics-0.1.0-alpha.5.0.5+mc{mc}.jar',Path.home()/'.gradle/caches/fabric-loom/26.2/minecraft-client.jar',*compile_libraries()]))
    if mc=='1.21.1':cp=(ROOT/'compat/alpha5-fabric-1.21.1/build/runtime-classpath.txt').read_text().strip()
    glfw=next(p for p in Path('E:/Roaming/ModrinthApp/meta/libraries/org/lwjgl/lwjgl-glfw').glob('*/lwjgl-glfw-*.jar') if 'natives' not in p.name)
    cp+=os.pathsep+str(glfw)
    with (directory/'compile.log').open('wb') as log:
        subprocess.run([str(JAVA[mc].with_name('javac.exe')),'-J-Djava.io.tmpdir='+str(directory),'--release','21' if mc=='1.21.1' else '25',
                        '-proc:none','-encoding','UTF-8','-cp',cp,'-d',str(directory),*map(str,java_files)],stdout=log,stderr=subprocess.STDOUT,check=True)
    raw=directory/'probe-named.jar'
    with zipfile.ZipFile(raw,'w') as z:
        for p in directory.rglob('*.class'):z.write(p,p.relative_to(directory).as_posix())
    jar=raw
    if mc=='1.21.1':
        modules=Path.home()/'.gradle/caches/modules-2/files-2.1'
        remapper_cp=[*modules.glob('net.fabricmc/tiny-remapper/0.14.0/*/*.jar'),*modules.glob('net.fabricmc/mapping-io/*/*/*.jar'),*modules.glob('org.ow2.asm/*/9.10.1/*/*.jar')]
        mappings=Path.home()/'.gradle/caches/fabric-loom/1.21.1/loom.mappings.1_21_1.layered+hash.2198-v2/mappings.tiny';jar=directory/'probe-intermediary.jar'
        with (directory/'remap.log').open('wb') as log:
            subprocess.run([str(JAVA[mc]),'-Djava.io.tmpdir='+str(directory),'-cp',os.pathsep.join(map(str,remapper_cp)),'net.fabricmc.tinyremapper.Main',
                            str(raw),str(jar),str(mappings),'named','intermediary',*cp.split(os.pathsep)],stdout=log,stderr=subprocess.STDOUT,check=True)
    with zipfile.ZipFile(jar) as z:return {n:z.read(n) for n in z.namelist() if n.endswith('.class')}
