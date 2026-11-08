"""Pinned, isolated runtime dependencies for the additional Java targets."""
from pathlib import Path
import hashlib,json,zipfile
from setup_worldgen_build import checked_download,fetch
from prepare_additional_ports import ROOT,TARGETS


def client_assets(minecraft):
    entry=TARGETS[minecraft]['downloads']['client']
    path=ROOT/f'build/new-version-ports/minecraft-client-{minecraft}.jar'
    checked_download(entry['url'],path,'sha1',entry['sha1'])
    return path


def fabric_classpath(minecraft):
    target=TARGETS[minecraft];cache=ROOT/f'build/new-version-ports/runtime-fabric-{minecraft}'
    bundler=cache/'server-bundler.jar';server=target['downloads']['server']
    checked_download(server['url'],bundler,'sha1',server['sha1'])
    classpath=[]
    with zipfile.ZipFile(bundler) as archive:
        for kind in ('versions','libraries'):
            for line in archive.read(f'META-INF/{kind}.list').decode().splitlines():
                checksum,_,relative=line.split('\t');path=cache/kind/relative
                if not path.resolve().is_relative_to(cache.resolve()):raise ValueError('Bundled path escapes cache')
                data=archive.read(f'META-INF/{kind}/{relative}')
                if hashlib.sha256(data).hexdigest()!=checksum:raise ValueError('Bundled checksum mismatch')
                path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);classpath.append(path)
    loader=target['fabric_loader']
    url=f'https://maven.fabricmc.net/net/fabricmc/fabric-loader/{loader}/fabric-loader-{loader}.jar'
    path=cache/f'fabric-loader-{loader}.jar'
    checked_download(url,path,'sha1',fetch(url+'.sha1').decode().strip());classpath.append(path)
    meta=json.loads(fetch(f'https://meta.fabricmc.net/v2/versions/loader/{minecraft}/{loader}'))
    for lib in meta['launcherMeta']['libraries']['common']:
        group,name,version=lib['name'].split(':');relative=f"{group.replace('.','/')}/{name}/{version}/{name}-{version}.jar"
        path=cache/'loader-libraries'/relative
        checked_download(lib['url']+relative,path,'sha256',lib['sha256']);classpath.append(path)
    if minecraft.startswith('1.'):
        url=f'https://maven.fabricmc.net/net/fabricmc/intermediary/{minecraft}/intermediary-{minecraft}.jar'
        path=cache/'intermediary.jar';checked_download(url,path,'sha1',fetch(url+'.sha1').decode().strip());classpath.append(path)
    return [p.resolve() for p in classpath]


def dependency(minecraft,key):
    entry=TARGETS[minecraft]['dependencies'][key]
    path=ROOT/'build/new-version-ports/dependencies'/minecraft/entry['filename']
    checked_download(entry['url'],path,'sha512',entry['sha512'])
    return path


def install_neoforge(minecraft,java):
    import subprocess
    target=TARGETS[minecraft];version=target['neoforge']
    root=ROOT/f'build/neoforge/runtime-{minecraft}'
    marker=root/f'libraries/net/neoforged/neoforge/{version}/unix_args.txt'
    if marker.exists():return root
    url=f'https://maven.neoforged.net/releases/net/neoforged/neoforge/{version}/neoforge-{version}-installer.jar'
    installer=ROOT/f'build/new-version-ports/neoforge-{version}-installer.jar'
    checked_download(url,installer,'sha256',fetch(url+'.sha256').decode().strip())
    root.mkdir(parents=True,exist_ok=True)
    subprocess.run([str(Path(java).resolve()),'-jar',str(installer.resolve()),'--installServer',str(root.resolve())],cwd=root,check=True)
    if not marker.exists():raise ValueError('Installer did not produce Unix launch arguments')
    return root


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--minecraft',choices=tuple(TARGETS),required=True)
    parser.add_argument('--loader',choices=('fabric','neoforge'),required=True)
    parser.add_argument('--java',type=Path)
    args=parser.parse_args()
    if args.loader=='neoforge':
        if not args.java:parser.error('--java required for NeoForge installer')
        print(install_neoforge(args.minecraft,args.java))
    else:print(json.dumps([str(p) for p in fabric_classpath(args.minecraft)],indent=2))
