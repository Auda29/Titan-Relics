"""Revision-specific checks on exported files and native registry evidence."""
import hashlib
import json
import subprocess
from build_gameplay_interiors import Builder, BUILDERS, ROOT, ASSETS, STEMS as ORIGINAL
from build_gameplay_interiors_revision import STEMS, build
from inspect_ots_result import read_structure
from schem_to_nbt import read_schematic
from validate_gameplay_handoff import inspect, reachable, require

def folder(name,stem):return (ROOT/ASSETS[name]['source']).parent.parent/stem

def native_registry():
    jar=ROOT/'build/worldgen-dependencies/versions/26.2/server-26.2.jar'
    java=ROOT/'build/toolchains/zulu25.36.205-ca-jdk25.0.4.1-win_x64/bin/java.exe'
    cp=(ROOT/'build/distribution-classpath.txt').read_text().strip()
    result=subprocess.run([str(java),'-cp',cp,str(ROOT/'tools/InteriorRegistryEvidence.java')],cwd=ROOT,capture_output=True,text=True,check=True)
    expected='minecraft:black_stained_glass: properties=[]; states=1'
    require(expected in result.stdout,'Native registry evidence missing')
    record={'minecraft_version':'26.2','server_jar_sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),
            'query':'tools/InteriorRegistryEvidence.java','result':expected,
            'blocks':{'black_stained_glass':[{},{}]}}
    out=ROOT/'docs/project/reviews/gameplay-interiors-feedback-20261027-registry.json'
    out.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    registry=json.loads((ROOT/'docs/project/reviews/gameplay-registry-26.2.json').read_text())['blocks']
    registry.update(record['blocks']);return registry

def check(name,registry):
    stem=STEMS[name];newdir=folder(name,stem);oldstem=ORIGINAL[name];olddir=folder(name,oldstem)
    side=json.loads((newdir/(stem+'.gameplay.json')).read_text());oldside=json.loads((olddir/(oldstem+'.gameplay.json')).read_text())
    root,blocks=read_structure(newdir/(stem+'.nbt'));oldroot,old=read_structure(olddir/(oldstem+'.nbt'))
    require(root['size']==oldroot['size'] and root['DataVersion']==oldroot['DataVersion']==3105,'Bounds or provenance changed')
    schem=read_schematic((newdir/(stem+'.schem')).read_bytes())
    oldschem=read_schematic((olddir/(oldstem+'.schem')).read_bytes())
    require(schem[0]==oldschem[0] and schem[2:]==oldschem[2:] and schem[1]==blocks,'Schematic dimensions, offset or provenance changed')
    require(side['markers']==oldside['markers'] and side['regions']==oldside['regions'],'Original marker contract changed')
    maintained=build(name);require(maintained.blocks==blocks,'Maintained revision does not reproduce NBT')
    report=inspect(newdir/(stem+'.gameplay.json'),registry)
    diff={p for p in old.keys()|blocks.keys() if old.get(p)!=blocks.get(p)}
    require(diff,'Empty revision')
    if name=='colossus':
        prior=Builder(name);BUILDERS[name](prior)
        require(not any(prior.groups.get(p)=='crew-stations' for p in diff),'Crew station altered')
        require(len([p for p in diff if maintained.groups.get(p)=='wrecked-cockpit-machinery'])>=250,'Insufficient cockpit detail')
        require(sum(s=='minecraft:black_stained_glass' for s in blocks.values())>=5,'Glass remnants absent')
        require(all((94,y,z) not in blocks for y in (172,173) for z in range(125,164)),'Visor line of sight blocked')
        require(reachable(blocks,(143,78,104),(110,78,70)),'Arm route blocked')
        report['revision_checks']=['five station blocks exact','substantial cockpit geometry','two clear sightlines through helmet','independent arm route']
    elif name=='small_colossus':
        require(len(diff)>=120,'Missing salvage detail')
        require(reachable(blocks,(62,14,40),(73,19,80)),'Breast entry to chest blocked')
        require(not any(p[1]>=39 for p in diff),'Stripped upper cockpit altered')
        report['revision_checks']=['salvage geometry','entry to chest','upper cockpit unchanged']
    elif name=='ruined_tower':
        require(len(diff)>=25,'Missing hall detail')
        require(reachable(blocks,(57,15,20),(72,15,55)),'Chest route blocked')
        target=next(m['pos'] for m in side['markers'] if m['role']=='tower_upper_destination')
        require(not reachable(blocks,(57,15,20),target),'Ascent unexpectedly walkable')
        require(all(p[1]<19 for p in diff),'Ascent modified')
        report['revision_checks']=['hall detail','chest route','all original ascent geometry and gaps preserved']
    else:
        require(all(p[1]<16 and 'terracotta' not in old.get(p,'') for p in diff),'Protected monument altered')
        for lo,hi in ((0,20),(40,58)):
            require(sum(1 for p in diff if lo<=p[0]<=hi and maintained.groups.get(p)=='excavation-landmarks')>=12,'Excavation landmarks missing')
        report['revision_checks']=['landmarks at both areas','monument and terracotta exact','eight open supported brushing tops']
    report['revision_changed_blocks']=len(diff)
    (newdir/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    return report

if __name__=='__main__':
    registry=native_registry()
    for name in STEMS:check(name,registry)
