"""Build a separately adapted Alpha 5 target without changing the primary artifact."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import shutil
from build_mc1211 import find_gradle
from prepare_alpha5_port import ROOT, VERSION, prepare


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--loader',default='fabric',choices=('fabric','neoforge'))
    parser.add_argument('--minecraft',default='1.21.1',choices=('1.21.1','26.2'))
    parser.add_argument('--java-home',type=Path,required=True)
    parser.add_argument('--gradle')
    parser.add_argument('--tasks',nargs='+',default=['build'])
    parser.add_argument('--log',type=Path)
    parser.add_argument('--rerun-tasks',action='store_true')
    parser.add_argument('--output',type=Path,default=ROOT/'dist')
    parser.add_argument('--client',type=Path,help='Matching Minecraft client asset JAR, otherwise use the prepared cache')
    args=parser.parse_args()
    report=prepare(args.loader,args.minecraft)
    project=ROOT/f'compat/alpha5-{args.loader}-{args.minecraft}'
    env=os.environ.copy();env['JAVA_HOME']=str(args.java_home.resolve())
    command=[find_gradle(args.gradle),'--no-daemon',*args.tasks]
    if args.rerun_tasks:command.append('--rerun-tasks')
    print(f"Prepared {args.loader} {args.minecraft}: {len(report['sources'])} Java sources",flush=True)
    if args.log:
        args.log.parent.mkdir(parents=True,exist_ok=True)
        with args.log.open('wb') as log:
            result=subprocess.run(command,cwd=project,env=env,stdout=log,stderr=subprocess.STDOUT)
        print('Gradle exit:',result.returncode,'log:',args.log,flush=True)
    else:result=subprocess.run(command,cwd=project,env=env)
    if result.returncode:return result.returncode
    if 'build' in args.tasks:
        from verify_alpha5_port import verify
        suffix='-neoforge' if args.loader=='neoforge' else ''
        artifact=project/f'build/libs/relics-{VERSION}+mc{args.minecraft}{suffix}.jar'
        record=verify(artifact,args.loader,args.minecraft)
        from verify_port_assets import verify as verify_assets
        candidates=[args.client] if args.client else [Path.home()/f'.gradle/caches/fabric-loom/{args.minecraft}/minecraft-client.jar',
            Path.home()/f'.gradle/caches/fabric-loom/{args.minecraft}/minecraft-merged.jar',
            Path.home()/f'.gradle/caches/neoformruntime/artifacts/minecraft_{args.minecraft}_client.jar']
        client=next((p for p in candidates if p and p.is_file()),None)
        if client is None:raise ValueError('Provide --client with the matching Minecraft client assets')
        record['assets']=verify_assets(artifact,client)
        args.output.mkdir(parents=True,exist_ok=True)
        destination=args.output/artifact.name
        if not destination.exists() or destination.read_bytes()!=artifact.read_bytes():
            temporary=destination.with_suffix('.jar.new');shutil.copy2(artifact,temporary);os.replace(temporary,destination)
        (args.output/f'SHA256SUMS-{args.loader}-mc{args.minecraft}.txt').write_text(record['sha256']+'  '+artifact.name+'\n',encoding='utf-8')
        (project/'build/build-verification.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(record,indent=2),flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
