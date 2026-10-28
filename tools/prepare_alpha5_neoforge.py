"""Generate native Alpha 5 NeoForge profiles with no Fabric API dependency."""
from __future__ import annotations
import hashlib,json,re,shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
COMMON=ROOT/'compat/alpha5-neoforge-common/src/main/adapters'
TARGETS={'1.21.1':{'neo':'21.1.256','java':21,'litho':'21.1'},'26.2':{'neo':'26.2.0.88','java':25,'litho':'26.2'}}


def native_java(name: str,text: str,minecraft: str,test=False):
    events={'CommandRegistrationCallback','ServerLifecycleEvents','ServerTickEvents','ServerEntityEvents','ServerChunkEvents',
            'ServerLivingEntityEvents','ServerPlayConnectionEvents','UseItemCallback','UseBlockCallback','PlayerBlockBreakEvents','ItemGroupEvents','CreativeModeTabEvents'}
    lines=[]
    for line in text.splitlines(True):
        if line.startswith('import net.fabricmc.fabric.api.attachment.v1.'):
            line=line.replace('net.fabricmc.fabric.api.attachment.v1.','de.relics.platform.NeoAttachments.')
        elif line.startswith('import net.fabricmc.fabric.api.event.lifecycle.v1.*;'):
            line='import de.relics.platform.NeoEvents.*;\n'
        elif line.startswith('import net.fabricmc.fabric.api.'):
            simple=line.strip().removesuffix(';').rsplit('.',1)[-1]
            if simple not in events:raise ValueError('Unreviewed native event: '+line)
            line='import de.relics.platform.NeoEvents.'+simple+';\n'
        elif test and line.startswith('import net.fabricmc.api.ModInitializer;'):continue
        lines.append(line)
    text=''.join(lines)
    text=text.replace('net.fabricmc.fabric.api.attachment.v1.','de.relics.platform.NeoAttachments.')
    text=re.sub(r'\(\((?:de\.relics\.platform\.NeoAttachments\.)?AttachmentTarget\)\s*(\w+)\)',r'de.relics.platform.NeoAttachments.AttachmentTarget.of(\1)',text)
    text=text.replace('(level,chunk,generated)->','(level,chunk)->')
    if name in ('RelicItems.java','MaintenanceRecipe.java'):
        text=text.replace('Registry.register(', 'de.relics.platform.NeoRegistrations.register(')
    if name=='RelicItems.java':
        assignments=[]
        def defer_item(match):
            assignments.append(match.group(1)+' = '+match.group(2)+';')
            return 'public static Item '+match.group(1)+';'
        text=re.sub(r'public static final Item (\w+) = (.*?);',defer_item,text,flags=re.S)
        if len(assignments)!=4:raise ValueError('Unreviewed native item declarations')
        text=text.replace('    private RelicItems() { }','    private RelicItems() { }\n    public static void registerItems() {\n        '+'\n        '.join(assignments)+'\n    }')
        text=text.replace('return de.relics.platform.NeoRegistrations.register(BuiltInRegistries.ITEM, id(name), item);','return Registry.register(BuiltInRegistries.ITEM, id(name), item);')
    if name=='CoreFurnaceMixin.java' and minecraft=='1.21.1':
        text=text.replace('NonNullList<ItemStack> items, int maximum)', 'NonNullList<ItemStack> items, int maximum, AbstractFurnaceBlockEntity furnace)')
        text=text.replace('self.items, furnace.getMaxStackSize())','self.items, furnace.getMaxStackSize(), furnace)')
    if name=='TreeAnimals.java':
        text=text.replace('mob.finalizeSpawn(level,','net.neoforged.neoforge.event.EventHooks.finalizeMobSpawn(mob,level,')
    if test:
        text=text.replace(' implements ModInitializer','').replace('@Override public void onInitialize()', 'public void onInitialize()')
        text=text.replace('package de.relics;', 'package de.relics.validation;\nimport de.relics.*;')
        text=text.replace('de.relics.testmixin','de.relics.validation.mixin').replace('de.relics.TreeAnimalChecks','de.relics.validation.TreeAnimalChecks')
        text=re.sub(r'(\w+)\.getServer\(\)\.getPlayerList\(\)\.getPlayers\(\)',r'((de.relics.validation.mixin.LegacyPlayerListAccess)(Object)\1.getServer().getPlayerList()).relics$listPlayers()',text)
        text=text.replace('super(PacketFlow.SERVERBOUND);','super(PacketFlow.SERVERBOUND);((de.relics.validation.mixin.ConnectionChannelAccess)(Object)this).relics$channel(new io.netty.channel.embedded.EmbeddedChannel());')
        if name=='LegacyPlayerListAccess.java':
            text=text.replace('\n}', '\n    @Accessor("players") java.util.List<ServerPlayer> relics$listPlayers();\n}')
        if name=='TreeAnimalChecks.java':
            text=text.replace('                String proof="natural_hook=true', '''                var cancelledPopulation=state(level,289,List.of());
                NativeSpawnChecks.cancelled=0;NativeSpawnChecks.cancel=true;
                try {
                    for(int i=0;i<4000 && NativeSpawnChecks.cancelled==0;i++)
                        TreeAnimals.withContext(cancelledPopulation,(type,pos,ch)->true,(mob,ch)->{throw new AssertionError("Cancelled mob charged population");},
                            ()->check(!TreeAnimals.afterNaturalSpawn(level,source,chunk),"Native cancellation ignored"));
                    check(NativeSpawnChecks.cancelled>0,"Native finalize event never reached");
                    check(cancelledPopulation.getMobCategoryCounts().getInt(MobCategory.CREATURE)==0,"Cancelled mob changed cap accounting");
                }finally{NativeSpawnChecks.cancel=false;}
                String proof="native_finalize_cancellation=true\\nnatural_hook=true''')
    if 'net.fabricmc.' in text:raise ValueError('Fabric reference in native '+name)
    return text


def metadata(minecraft,mod='relics'):
    target=TARGETS[minecraft]
    if mod=='relics':
        return f'''modLoader="javafml"
loaderVersion="[1,)"
license="All-Rights-Reserved"
[[mods]]
modId="relics"
version="0.1.0-alpha.5.0.1"
displayName="Relic Mod"
authors="Auda29"
description="Alpha 5 relic structures, exploration and finite personal rewards."
[[mixins]]
config="relics.mixins.json"
[[dependencies.relics]]
modId="minecraft"
type="required"
versionRange="[{minecraft}]"
ordering="NONE"
side="BOTH"
[[dependencies.relics]]
modId="neoforge"
type="required"
versionRange="[{target['neo']},)"
ordering="NONE"
side="BOTH"
[[dependencies.relics]]
modId="lithostitched"
type="required"
versionRange="[1.8.0]"
ordering="AFTER"
side="BOTH"
'''
    return '''modLoader="javafml"
loaderVersion="[1,)"
license="All-Rights-Reserved"
[[mods]]
modId="relics_port_checks"
version="1"
displayName="Isolated Relic port checks, not for players"
[[mixins]]
config="animal-probe.mixins.json"
[[dependencies.relics_port_checks]]
modId="relics"
type="required"
versionRange="[0.1.0-alpha.5.0.1]"
ordering="AFTER"
side="BOTH"
'''


def prepare(minecraft):
    if minecraft!='1.21.1':raise ValueError('Finish the requested 1.21.1 native target first')
    from prepare_alpha5_port import prepare as fabric_prepare
    fabric_prepare('fabric','1.21.1')
    source=ROOT/'compat/alpha5-fabric-1.21.1/build/generated'
    project=ROOT/f'compat/alpha5-neoforge-{minecraft}';output=project/'build/generated'
    if output.exists():
        assert output.resolve().is_relative_to((project/'build').resolve());shutil.rmtree(output)
    shutil.copytree(source/'resources',output/'resources')
    resources=output/'resources';(resources/'fabric.mod.json').unlink()
    path=resources/'META-INF/neoforge.mods.toml';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(metadata(minecraft),encoding='utf-8',newline='\n')
    for path in resources.glob('relics.*integration.json'):
        manifest=json.loads(path.read_bytes());manifest['loader']='neoforge';manifest['protection_storage']='neoforge:attachments/relics:placed_cells/sections'
        path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    pack=json.loads((resources/'pack.mcmeta').read_bytes());pack['pack']['description']='Relic Mod Alpha 5.0 for NeoForge '+minecraft
    (resources/'pack.mcmeta').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8')
    sources=[]
    for path in sorted((source/'java').rglob('*.java')):
        relative=path.relative_to(source/'java');override=COMMON/relative
        text=override.read_text(encoding='utf-8') if override.exists() else native_java(path.name,path.read_text(encoding='utf-8'),minecraft)
        destination=output/'java'/relative;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(text,encoding='utf-8',newline='\n')
    for path in sorted(COMMON.rglob('*.java')):
        destination=output/'java'/path.relative_to(COMMON)
        if destination.exists():continue
        destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,destination)
    for path in sorted((output/'java').rglob('*.java')):
        sources.append({'path':path.relative_to(output/'java').as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    for path in sorted((source/'test').rglob('*.java')):
        relative=path.relative_to(source/'test')
        if relative.parts[:3]==('de','relics','testmixin'):relative=Path('de/relics/validation/mixin')/path.name
        text=native_java(path.name,path.read_text(encoding='utf-8'),minecraft,test=True)
        if 'package de.relics.validation;' in text:relative=Path('de/relics/validation')/path.name
        destination=output/'test'/relative;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(text,encoding='utf-8',newline='\n')
    bootstrap=output/'test/de/relics/validation/PortTestMod.java'
    bootstrap.write_text('''package de.relics.validation;
@net.neoforged.fml.common.Mod("relics_port_checks")
public final class PortTestMod {
    public PortTestMod(){
        NativeSpawnChecks.initialize();
        new GameplayPresentationChecks().onInitialize();new TreeAuraChecks().onInitialize();
        new TreeAnimalChecks().onInitialize();new NaturalInteriorChecks().onInitialize();
        new DistributionRuntimeChecks().onInitialize();new PortChecks().onInitialize();
    }
}
''',encoding='utf-8',newline='\n')
    for adapter in (ROOT/'compat/alpha5-neoforge-common/src/test/adapters').rglob('*.java'):
        destination=output/'test'/adapter.relative_to(ROOT/'compat/alpha5-neoforge-common/src/test/adapters')
        destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(adapter,destination)
    test_resources=output/'test-resources';(test_resources/'META-INF').mkdir(parents=True)
    (test_resources/'META-INF/neoforge.mods.toml').write_text(metadata(minecraft,'checks'),encoding='utf-8',newline='\n')
    (test_resources/'animal-probe.mixins.json').write_text(json.dumps({'required':True,'package':'de.relics.validation.mixin','compatibilityLevel':'JAVA_21','mixins':['TreeAnimalProbeMixin','LegacyPlayerListAccess','ConnectionChannelAccess'],'injectors':{'defaultRequire':1}}),encoding='utf-8')
    report={'loader':'neoforge','minecraft':minecraft,'version':'0.1.0-alpha.5.0.1','sources':sources,'neoforge':TARGETS[minecraft]['neo']}
    (project/'build/adapter-manifest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report
