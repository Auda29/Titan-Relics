"""Launch installed native NeoForge servers from new isolated test directories."""
from pathlib import Path
import hashlib
import re
import shlex
import zipfile

from prepare_alpha5_neoforge import TARGETS

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def installed_arguments(server: Path, minecraft: str) -> tuple[list[str], dict]:
    server = server.resolve()
    version = TARGETS[minecraft]['neo']
    argfile = server / f'libraries/net/neoforged/neoforge/{version}/unix_args.txt'
    if not argfile.exists():argfile=argfile.with_name('win_args.txt')
    raw = argfile.read_text(encoding='utf-8')
    args = shlex.split(raw, posix=True)
    if '--fml.mcVersion' not in args or args[args.index('--fml.mcVersion') + 1] != minecraft:
        raise ValueError('NeoForge server target mismatch')
    if args[args.index('--fml.neoForgeVersion') + 1] != version:
        raise ValueError('NeoForge server version mismatch')
    # Relocate only installed library references, leaving mods/world in the new run.
    libs = (server / 'libraries').as_posix()
    args = [arg.replace('libraries/', libs + '/').replace('-DlibraryDirectory=libraries',
            '-DlibraryDirectory=' + libs) for arg in args]
    files = sorted({match.group() for match in re.finditer(r'libraries/[^\s;:]+\.jar', raw)})
    # The loader discovers patched game/NeoForge artifacts via its installation
    # metadata rather than putting all of them directly on the JVM classpath.
    for root in ('net/neoforged/neoforge/' + version, 'net/neoforged/minecraft-server-patched/' + version):
        files.extend(p.relative_to(server).as_posix() for p in (server / 'libraries' / root).glob('*.jar'))
    files = sorted(set(files))
    evidence = {'neoforge_version': version, 'installed_server': server.as_posix(),
                'argument_file_sha256': sha256(argfile),
                'libraries': [{'file': name, 'sha256': sha256(server / name)} for name in files]}
    return args, evidence


def logging_arguments(server: Path, minecraft: str, run: Path) -> tuple[list[str], dict]:
    """Retain NeoForge logging levels/appenders/full traces, avoid xEx class init.

    Log4j 2.26's extended throwable renderer re-initializes failed Linux/BSD
    Netty native classes while formatting ordinary DEBUG probe failures on
    Windows. Plain full traces avoid this logger crash without filtering errors.
    """
    if minecraft not in ('26.2','1.21.11','26.3'):
        return [], {}
    loaders=sorted((server/'libraries/net/neoforged/fancymodloader/loader').glob('*/*.jar'))
    if len(loaders)!=1:raise ValueError('Expected one installed FML logger template')
    loader=loaders[0]
    with zipfile.ZipFile(loader) as archive:
        raw = archive.read('net/neoforged/fml/startup/log4j2.xml')
    if raw.count(b'%xEx') != 2:
        raise ValueError('Native logger template changed; review before adjusting')
    file = run / 'neoforge-log4j2.xml'
    file.write_bytes(raw.replace(b'%xEx', b'%ex{full}'))
    return ['-Dlog4j.configurationFile=' + file.resolve().as_uri()], {
        'logging_adapter': 'Two extended throwable renderers replaced by plain full traces; no level, appender or error filter changes',
        'original_logging_sha256': hashlib.sha256(raw).hexdigest(),
        'runtime_logging_sha256': sha256(file)}
