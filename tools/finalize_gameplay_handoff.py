"""Verify editable sources and publish one exact machine-readable builder index."""
import hashlib
import json
import subprocess
from build_gameplay_interiors import ROOT,ASSETS,STEMS
from validate_gameplay_handoff import inspect

def main():
    subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe',
                    '--background','--python-exit-code','1','--python','tools/render_gameplay_interiors.py','--','verify'],cwd=ROOT,check=True)
    registry=json.loads((ROOT/'docs/project/reviews/gameplay-registry-26.2.json').read_text())['blocks']
    index={'schema_version':1,'baseline_commit':'59259872bb4eeb740fcf5fb137a0745f6b62db9a',
           'target':'Minecraft 26.2 / Fabric','status':'builder candidates; visual/runtime integration pending',
           'sidecar_extension':'Optional arm_clearance for the large detached arm; native terrain only, preserve source solids',
           'assets':{},'unchanged_skulls':{name:a for name,a in ASSETS.items() if 'skull' in name}}
    for name,stem in STEMS.items():
        folder=(ROOT/ASSETS[name]['source']).parent.parent/stem
        sidecar=folder/(stem+'.gameplay.json');report=inspect(sidecar,registry)
        source=json.loads((folder/'source-verification.json').read_text())
        report['editable_source']=source
        (folder/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
        files={}
        for suffix in ('.nbt','.schem','.gameplay.json','.design.json','-source.blend','-review.png','-markers-review.png'):
            p=folder/(stem+suffix)
            # Git stores these text artifacts with LF. Bind the published bytes,
            # not Windows-only CRLF bytes that change on another checkout.
            if suffix.endswith('.json'):
                p.write_text(p.read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
            files[suffix]={'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
        index['assets'][name]={'files':files,'size':report['size'],'ground_y':ASSETS[name]['ground_y'],
                               'blocks':report['blocks'],'markers':report['markers'],'regions':report['regions']}
    out=ROOT/'docs/project/reviews/gameplay-interiors-handoff.json'
    out.write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8',newline='\n');print(out)

if __name__=='__main__':main()
