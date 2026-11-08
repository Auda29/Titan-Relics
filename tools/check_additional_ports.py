"""Build and exercise the additional release targets in isolated temporary worlds."""
from __future__ import annotations
import argparse,os,subprocess,sys
from pathlib import Path
from prepare_additional_ports import ROOT,TARGETS
from release_version import release_version


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--java-home',type=Path,required=True)
    parser.add_argument('--java21-home',type=Path,required=True)
    parser.add_argument('--gradle',default='gradle')
    parser.add_argument('--loader',choices=('fabric','neoforge'))
    parser.add_argument('--minecraft',choices=tuple(TARGETS))
    parser.add_argument('--skip-runtime',action='store_true',help='Build only, without claiming a runtime validation')
    parser.add_argument('--output',type=Path,default=ROOT/'dist')
    args=parser.parse_args();version=release_version()
    def run(*command):subprocess.run([sys.executable,*map(str,command)],cwd=ROOT,check=True)
    for minecraft in ([args.minecraft] if args.minecraft else TARGETS):
        java=(args.java21_home if TARGETS[minecraft]['java']==21 else args.java_home)/'bin/java'
        for loader in ([args.loader] if args.loader else ['fabric','neoforge']):
            build=[ROOT/'tools/build_alpha5_port.py','--loader',loader,'--minecraft',minecraft,
                   '--java-home',args.java_home,'--gradle',args.gradle,'--output',args.output]
            run(*build)
            sums=args.output/f'SHA256SUMS-{loader}-mc{minecraft}.txt';first=sums.read_bytes()
            run(*build,'--rerun-tasks')
            if sums.read_bytes()!=first:raise ValueError(f'Non-reproducible {loader}/{minecraft} artifact')
            if args.skip_runtime:continue
            suffix='-neoforge' if loader=='neoforge' else ''
            artifact=args.output/f'relics-{version}+mc{minecraft}{suffix}.jar'
            profile=ROOT/f'compat/alpha5-{loader}-{minecraft}/build'
            if loader=='neoforge':
                run(ROOT/'tools/additional_port_runtime.py','--loader',loader,'--minecraft',minecraft,'--java',java)
                test_mod=profile/f'validation/relics-alpha5-port-checks+mc{minecraft}-neoforge.jar'
            elif minecraft=='26.3':test_mod=profile/f'libs/relics-{version}-port-tests-dev.jar'
            else:test_mod=profile/f'libs/relics-alpha5-port-checks+mc{minecraft}.jar'
            run(ROOT/'tools/test_alpha5_port_server.py','--loader',loader,'--minecraft',minecraft,
                '--java',java,'--artifact',artifact,'--test-mod',test_mod,'--accept-eula','--suite',
                '--distribution-preset','discovery','--reload-preset','expedition','--world-load-checks')
            run(ROOT/'tools/test_alpha5_port_server.py','--loader',loader,'--minecraft',minecraft,
                '--java',java,'--artifact',artifact,'--accept-eula','--distribution-preset','tower-only')


if __name__=='__main__':main()
