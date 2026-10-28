"""Extract native armor geometry/alpha and prepare paletted inspection textures.

Requires cached Minecraft 26.2 client, JDK25, Pillow and the previous player JAR
or the bounded before.zip snapshot. Native texture copies stay under build/.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import zipfile
from PIL import Image
from compile_worldgen import ROOT,compile_libraries

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--client',type=Path,required=True)
    parser.add_argument('--java-home',type=Path,required=True)
    parser.add_argument('--before-archive',type=Path,required=True)
    args=parser.parse_args()
    cache=ROOT/'build/monolith-trim-20261028';native=cache/'native-assets';native.mkdir(parents=True,exist_ok=True)
    checksum=hashlib.sha256(args.client.read_bytes()).hexdigest()
    if checksum!='40896ee9f1e2bec3c934daac7e93d41e9e3d9c2f8ae0ca366d52ffbfd1afa290':
        raise ValueError('Client differs from the inspected pinned 26.2 client')
    with zipfile.ZipFile(args.client) as archive:
        for kind in ('humanoid','humanoid_leggings'):
            (native/f'{kind}-netherite.png').write_bytes(archive.read(f'assets/minecraft/textures/entity/equipment/{kind}/netherite.png'))
        for name in ('trim_palette','emerald','amethyst','copper'):
            (native/f'{name}.png').write_bytes(archive.read(f'assets/minecraft/textures/trims/color_palettes/{name}.png'))
    java=args.java_home.resolve()/'bin';cp=os.pathsep.join(map(str,[args.client.resolve(),*compile_libraries()]))
    subprocess.run([str(java/'javac.exe'),'-cp',cp,'-d',str(cache),str(ROOT/'tools/ArmorUvEvidence.java')],check=True)
    subprocess.run([str(java/'java.exe'),'-cp',str(cache)+os.pathsep+cp,'ArmorUvEvidence',str(cache/'native-armor-uv.json')],check=True)
    evidence=json.loads((cache/'native-armor-uv.json').read_text());evidence['client_sha256']=checksum;evidence['opaque_uv']={}
    key=list(Image.open(native/'trim_palette.png').convert('RGBA').get_flattened_data())
    with zipfile.ZipFile(args.before_archive) as previous:
        for kind in ('humanoid','humanoid_leggings'):
            base=Image.open(native/f'{kind}-netherite.png').convert('RGBA')
            evidence['opaque_uv'][kind]=[y*64+x for y in range(32) for x in range(64) if base.getpixel((x,y))[3]]
            relative=f'assets/relics/textures/trims/entity/{kind}/monolith.png'
            old_path=relative if relative in previous.namelist() else 'src/main/resources/'+relative
            masks={'before':Image.open(io.BytesIO(previous.read(old_path))).convert('RGBA'),
                   'after':Image.open(ROOT/'src/main/resources'/relative).convert('RGBA')}
            for variant,mask in masks.items():
                for material in ('emerald','amethyst','copper'):
                    colors=list(Image.open(native/f'{material}.png').convert('RGBA').get_flattened_data());mapping=dict(zip(key,colors));out=base.copy()
                    for y in range(32):
                        for x in range(64):
                            color=mask.getpixel((x,y))
                            if color[3]:out.putpixel((x,y),mapping[color])
                    out.save(cache/f'{variant}-{material}-{kind}.png')
    (ROOT/'docs/project/reviews/monolith-native-armor-26.2.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
    print('Native polygons, equipment alpha and paletted inspection textures prepared')

if __name__=='__main__':main()
