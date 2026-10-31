"""Generate native Alpha 5 NeoForge profiles with no Fabric API dependency."""
from __future__ import annotations
import hashlib,json,re,shutil,zipfile
from pathlib import Path
from release_version import release_version

ROOT=Path(__file__).resolve().parents[1]
VERSION=release_version()
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
    if name=='RelicGameplay.java' and minecraft=='26.2':
        text=text.replace('data.getCompoundOrEmpty(AttachmentTarget.NBT_ATTACHMENT_KEY).getListOrEmpty("relics:delivery_receipts")',
            'data.getCompoundOrEmpty(AttachmentTarget.NBT_ATTACHMENT_KEY).getCompoundOrEmpty("relics:delivery_receipts").getListOrEmpty("value")')
    if test:
        text=text.replace(' implements ModInitializer','').replace('@Override public void onInitialize()', 'public void onInitialize()')
        text=text.replace('package de.relics;', 'package de.relics.validation;\nimport de.relics.*;')
        text=text.replace('de.relics.testmixin','de.relics.validation.mixin').replace('de.relics.TreeAnimalChecks','de.relics.validation.TreeAnimalChecks')
        text=re.sub(r'(\w+)\.getServer\(\)\.getPlayerList\(\)\.getPlayers\(\)',r'((de.relics.validation.mixin.LegacyPlayerListAccess)(Object)\1.getServer().getPlayerList()).relics$listPlayers()',text)
        text=re.sub(r'(\w+)\.getServer\(\)\.getPlayerList\(\)\.getPlayersByUUID\(\)',r'((de.relics.validation.mixin.LegacyPlayerListAccess)(Object)\1.getServer().getPlayerList()).relics$players()',text)
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


def modern_platform(name,text):
    text=text.replace('ResourceLocation','Identifier')
    if name=='RelicWorldgen.java':
        text=re.sub(r'    public static final .*? TERRAIN_SUPPORT=.*?;\n','',text)
        text=text.replace('()->TERRAIN_SUPPORT','()->TerrainSupportProcessor.CODEC')
    if name=='NeoAttachments.java':
        text=text.replace('if(id.getPath().equals("placed_cells"))codec=codec.fieldOf("sections").codec();','')
        text=text.replace('builder.serialize(codec);','builder.serialize(codec.fieldOf(id.getPath().equals("placed_cells")?"sections":"value"));')
    if name=='NeoEvents.java':
        text=text.replace('BlockEvent.BreakEvent','net.neoforged.neoforge.event.level.block.BreakBlockEvent')
        text=text.replace('level.getBlockEntity(event.getPos()))){event.setCanceled(true);break;}', 'level.getBlockEntity(event.getPos()))){event.setCanceled(true);event.setNotifyClient(true);break;}')
        text=text.replace('player.getServer()','player.level().getServer()')
        text=text.replace('result instanceof InteractionResultHolder<?> holder && holder.getResult()!=InteractionResult.PASS','result instanceof InteractionResult holder && holder!=InteractionResult.PASS')
        text=text.replace('event.setCancellationResult(holder.getResult())','event.setCancellationResult(holder)')
    return text


def modern_checks(text):
    text=text.replace('registryOrThrow(', 'lookupOrThrow(').replace('.location()', '.identifier()').replace('level.getRecipeManager()', 'level.recipeAccess()')
    text=text.replace('.byKey(id)', '.byKey(ResourceKey.create(Registries.RECIPE,id))')
    text=text.replace('recipe.getIngredients().size()', '((net.minecraft.world.item.crafting.display.ShapedCraftingRecipeDisplay)recipe.display().getFirst()).ingredients().size()')
    text=text.replace('.assemble(ingredients,level.registryAccess())','.assemble(ingredients)').replace('.assemble(smithingInput,level.registryAccess())','.assemble(smithingInput)')
    return text


def modern_recipe_packet(text):
    body='''        var manager=level.recipeAccess();
        var packet=new ClientboundUpdateRecipesPacket(manager.getSynchronizedItemProperties(),manager.getSynchronizedStonecutterRecipes());
        var decoded=roundTrip(ClientboundUpdateRecipesPacket.STREAM_CODEC,packet,level.registryAccess());
        check(decoded.itemSets().keySet().equals(packet.itemSets().keySet()),"Recipe property synchronization changed keys");
        var entries=new ArrayList<net.minecraft.network.protocol.game.ClientboundRecipeBookAddPacket.Entry>();
        for(boolean core:new boolean[]{true,false}) {
            var id=RelicItems.id(core?"machine_core_recharge":"salvage_magnet_repair");
            int before=entries.size();
            manager.listDisplaysForRecipe(ResourceKey.create(Registries.RECIPE,id),
                    display->entries.add(new net.minecraft.network.protocol.game.ClientboundRecipeBookAddPacket.Entry(display,true,true)));
            check(entries.size()==before+1,"Recipe book lost maintenance display");
        }
        var book=roundTrip(net.minecraft.network.protocol.game.ClientboundRecipeBookAddPacket.STREAM_CODEC,
                new net.minecraft.network.protocol.game.ClientboundRecipeBookAddPacket(entries,true),level.registryAccess());
        check(book.replace() && book.entries().size()==2,"Recipe book synchronization lost entries");
        for(int i=0;i<2;i++) {
            var entry=book.entries().get(i);
            check(entry.contents().id().equals(entries.get(i).contents().id()),"Recipe display ID changed");
            check(entry.notification() && entry.highlight(),"Recipe display flags changed");
            check(entry.contents().display() instanceof net.minecraft.world.item.crafting.display.ShapedCraftingRecipeDisplay,"Non-shaped maintenance display");
            var shape=(net.minecraft.world.item.crafting.display.ShapedCraftingRecipeDisplay)entry.contents().display();
            check(shape.width()==3 && shape.height()==(i==0?2:3),"Recipe display shape changed");
        }
'''
    start=text.index('        // VERSIONED_PACKET_START')
    end=text.index('        // VERSIONED_PACKET_END',start)+len('        // VERSIONED_PACKET_END')
    text=text[:start]+body+text[end:]
    return text.replace('full_update_packet_roundtrip=true\\n','full_update_packet_roundtrip=true\\nrecipe_book_packet_roundtrip=true\\n')


def metadata(minecraft,mod='relics'):
    target=TARGETS[minecraft]
    if mod=='relics':
        return f'''modLoader="javafml"
loaderVersion="[1,)"
license="All-Rights-Reserved"
[[mods]]
modId="relics"
version="{VERSION}"
displayName="Relic Mod"
authors="Auda29"
description="Alpha 5 relic structures, exploration and finite personal rewards."
[[mixins]]
config="relics.mixins.json"
[[mixins]]
config="relics.client.mixins.json"
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
    return f'''modLoader="javafml"
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
versionRange="[{VERSION}]"
ordering="AFTER"
side="BOTH"
'''


def prepare(minecraft):
    if minecraft not in TARGETS:raise ValueError('Unknown native target')
    legacy=minecraft=='1.21.1'
    if legacy:
        from prepare_alpha5_port import prepare as fabric_prepare
        fabric_prepare('fabric','1.21.1')
        source=ROOT/'compat/alpha5-fabric-1.21.1/build/generated'
    else:source=ROOT/'src/main'
    project=ROOT/f'compat/alpha5-neoforge-{minecraft}';output=project/'build/generated'
    if output.exists():
        assert output.resolve().is_relative_to((project/'build').resolve());shutil.rmtree(output)
    if legacy:shutil.copytree(source/'resources',output/'resources')
    else:
        from build import write_archive
        bundle=project/'build/source-resources.jar';write_archive(bundle)
        with zipfile.ZipFile(bundle) as archive:archive.extractall(output/'resources')
    resources=output/'resources';(resources/'fabric.mod.json').unlink()
    path=resources/'META-INF/neoforge.mods.toml';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(metadata(minecraft),encoding='utf-8',newline='\n')
    for path in resources.glob('relics.*integration.json'):
        manifest=json.loads(path.read_bytes());manifest['compatibility_target']=minecraft;manifest['loader']='neoforge';manifest['protection_storage']='neoforge:attachments/relics:placed_cells/sections'
        path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    if not legacy:
        mixins=json.loads((resources/'relics.mixins.json').read_bytes());mixins['compatibilityLevel']='JAVA_25'
        (resources/'relics.mixins.json').write_text(json.dumps(mixins,indent=2)+'\n',encoding='utf-8')
    pack=json.loads((resources/'pack.mcmeta').read_bytes());pack['pack']['description']='Relic Mod Alpha 5.0 for NeoForge '+minecraft
    (resources/'pack.mcmeta').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8')
    sources=[]
    java_paths=list((source/'java').rglob('*.java'))
    if not legacy:java_paths+=list((ROOT/'src/client/java').rglob('*.java'))
    for path in sorted(java_paths):
        if path.name=='RelicModMenu.java':continue
        relative=path.relative_to(ROOT/'src/client/java' if path.is_relative_to(ROOT/'src/client/java') else source/'java');override=COMMON/relative
        text=(modern_platform(path.name,override.read_text(encoding='utf-8')) if not legacy else override.read_text(encoding='utf-8')) if override.exists() else native_java(path.name,path.read_text(encoding='utf-8'),minecraft)
        destination=output/'java'/relative;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(text,encoding='utf-8',newline='\n')
    for path in sorted(COMMON.rglob('*.java')):
        destination=output/'java'/path.relative_to(COMMON)
        if destination.exists():continue
        destination.parent.mkdir(parents=True,exist_ok=True)
        text=path.read_text(encoding='utf-8');destination.write_text(text if legacy else modern_platform(path.name,text),encoding='utf-8',newline='\n')
    for path in sorted((output/'java').rglob('*.java')):
        sources.append({'path':path.relative_to(output/'java').as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    test_source=source/'test' if legacy else ROOT/'src/test/java'
    selected={'GameplayPresentationChecks.java','TreeAuraChecks.java','TreeAnimalChecks.java','TreeAnimalProbeMixin.java','NaturalInteriorChecks.java','DistributionRuntimeChecks.java'}
    test_paths=list(test_source.rglob('*.java')) if legacy else [p for p in test_source.rglob('*.java') if p.name in selected]
    if not legacy:test_paths+=list((ROOT/'compat/alpha5-fabric-1.21.1/src/test/adapters').rglob('*.java'))
    for path in sorted(test_paths):
        relative=path.relative_to(test_source) if path.is_relative_to(test_source) else path.relative_to(ROOT/'compat/alpha5-fabric-1.21.1/src/test/adapters')
        if relative.parts[:3]==('de','relics','testmixin'):relative=Path('de/relics/validation/mixin')/path.name
        text=path.read_text(encoding='utf-8')
        if not legacy and path.name in ('PortChecks.java','RecipeNetworkChecks.java'):text=modern_checks(text)
        if not legacy and path.name=='RecipeNetworkChecks.java':text=modern_recipe_packet(text)
        text=native_java(path.name,text,minecraft,test=True)
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
    (test_resources/'animal-probe.mixins.json').write_text(json.dumps({'required':True,'package':'de.relics.validation.mixin','compatibilityLevel':'JAVA_'+str(TARGETS[minecraft]['java']),'mixins':['TreeAnimalProbeMixin','LegacyPlayerListAccess','ConnectionChannelAccess'],'injectors':{'defaultRequire':1}}),encoding='utf-8')
    report={'loader':'neoforge','minecraft':minecraft,'version':VERSION,'sources':sources,'neoforge':TARGETS[minecraft]['neo']}
    (project/'build/adapter-manifest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report
