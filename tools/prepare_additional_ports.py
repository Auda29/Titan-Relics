"""Generate isolated 1.21.11/26.3 sources and resources from the frozen selection."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import shutil
import zipfile

from release_version import release_version

ROOT = Path(__file__).resolve().parents[1]
TARGETS = json.loads((ROOT / 'compat/additional-targets.json').read_text())


def port_java(name, text, minecraft, test=False):
    """Version-specific adaptations, shared by the two loader profiles."""
    if minecraft == '1.21.11':
        text = text.replace('EntityTypes', 'EntityType').replace('START_LEVEL_TICK','START_WORLD_TICK')
        text = text.replace('ChunkPos.pack(', 'ChunkPos.asLong(').replace('.isWithinWriteZone(', '.ensureCanWrite(')
        for receiver in ['getPos()', 'context.chunkPos()']:
            for axis in ['x','z']: text = text.replace(receiver+'.'+axis+'()',receiver+'.'+axis)
        if name in ['NaturalInteriors.java','DistributionRuntime.java','SeparatedPlacementCondition.java']:
            for receiver in ['pos','chunk'] + (['candidate'] if name=='SeparatedPlacementCondition.java' else []):
                for axis in ['x','z']: text=text.replace(receiver+'.'+axis+'()', receiver+'.'+axis)
        text = text.replace('EntityType.ENDERMAN.canSpawn(level)', '(level.getDifficulty()!=net.minecraft.world.Difficulty.PEACEFUL)')
        text = text.replace('graphics.centeredText(', 'graphics.drawCenteredString(').replace('graphics.textWithWordWrap(', 'graphics.drawWordWrap(').replace('graphics.text(', 'graphics.drawString(')
        text = text.replace('getWorldGenSettings().options()', 'getWorldData().worldGenOptions()')
        text = text.replace('(level,chunk,generated)->', '(level,chunk)->')
        if name == 'TerrainSupportProcessor.java':
            # Reuse only the processor's record/class and chunk-local clipping adaptation.
            from prepare_mc1211 import port_java as old_processor
            text = old_processor(name,text).replace('net.minecraft.resources.ResourceLocation','net.minecraft.resources.Identifier').replace('.getMinBuildHeight()', '.getMinY()')
        if name == 'RelicWorldgen.java':
            text=text.replace('public final class RelicWorldgen implements ModInitializer {',
              'public final class RelicWorldgen implements ModInitializer {\n    public static final net.minecraft.world.level.levelgen.structure.templatesystem.StructureProcessorType<TerrainSupportProcessor> TERRAIN_SUPPORT = () -> TerrainSupportProcessor.CODEC;')
            text=text.replace('TerrainSupportProcessor.CODEC);','TERRAIN_SUPPORT);')
        if name == 'RelicItems.java':
            text=text.replace('net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents','net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents').replace('CreativeModeTabEvents.modifyOutputEvent','ItemGroupEvents.modifyEntriesEvent')
        if name == 'CoreFurnaceMixin.java':
            text=text.replace('assemble(new SingleRecipeInput(input))','assemble(new SingleRecipeInput(input),level.registryAccess())')
            signature='net.minecraft.core.RegistryAccess registries, net.minecraft.world.item.crafting.RecipeHolder<? extends AbstractCookingRecipe> recipe, SingleRecipeInput input, NonNullList<ItemStack> items, int maximum'
            text=text.replace('boolean canBurn(NonNullList<ItemStack> items, int maximum, ItemStack output)', 'boolean canBurn('+signature+')')
            text=text.replace('void burn(NonNullList<ItemStack> items, ItemStack input, ItemStack output)', 'boolean burn('+signature+')')
            text=text.replace('canBurn(self.items, furnace.getMaxStackSize(), result)', 'canBurn(level.registryAccess(),recipe,new SingleRecipeInput(input),self.items,furnace.getMaxStackSize())')
            text=text.replace('burn(self.items, input, result)', 'burn(level.registryAccess(),recipe,new SingleRecipeInput(input),self.items,furnace.getMaxStackSize())')
        text=text.replace('level.getRecipeManager()', 'level.recipeAccess()')
        if name == 'MaintenanceRecipe.java':
            text=text.replace('import net.minecraft.world.item.ItemStackTemplate;','')
            text=text.replace('public MaintenanceRecipe(boolean core) {','public MaintenanceRecipe(boolean core) { super(net.minecraft.world.item.crafting.CraftingBookCategory.MISC);')
            text=text.replace('return new RecipeSerializer<>(MapCodec.unit(() -> new MaintenanceRecipe(core)),\n                StreamCodec.<net.minecraft.network.RegistryFriendlyByteBuf,Boolean>unit(core).map(MaintenanceRecipe::new,recipe->recipe.core));', '''return new RecipeSerializer<>() {
            public MapCodec<MaintenanceRecipe> codec() { return MapCodec.unit(() -> new MaintenanceRecipe(core)); }
            public StreamCodec<net.minecraft.network.RegistryFriendlyByteBuf,MaintenanceRecipe> streamCodec() {
                return StreamCodec.<net.minecraft.network.RegistryFriendlyByteBuf,Boolean>unit(core).map(MaintenanceRecipe::new,recipe->recipe.core);
            }
        };''')
            text=text.replace('assemble(CraftingInput input)', 'assemble(CraftingInput input, net.minecraft.core.HolderLookup.Provider registries)')
            text=text.replace('ItemStackTemplate.fromNonEmptyStack(depleted)','depleted')
        if test:
            text=text.replace('.assemble(ingredients)', '.assemble(ingredients,level.registryAccess())').replace('.assemble(smithingInput)', '.assemble(smithingInput,level.registryAccess())')
            text=re.sub(r'(\w+)\.getServer\(\)\.getPlayerList\(\)\.getPlayersByUUID\(\)',r'((de.relics.testmixin.LegacyPlayerListAccess)(Object)\1.getServer().getPlayerList()).relics$players()',text)
        if name=='WorldLoadCheck.java':
            text=text.replace('dimensions/minecraft/overworld/data/minecraft/world_border.dat','data/world_border.dat')
            start=text.index('            // STEM_INPUTS_BEGIN');end=text.index('            // STEM_INPUTS_END')
            text=text[:start]+'''            var options=stem.worldData().worldGenOptions();
            var generator=stem.registries().compositeAccess().lookupOrThrow(net.minecraft.core.registries.Registries.LEVEL_STEM).getValue(LevelStem.OVERWORLD).generator();
'''+text[end:]
        text=text.replace('GuiGraphicsExtractor','GuiGraphics').replace('extractRenderState','render').replace('extractBackground','renderBackground')
        text=text.replace('.gui.setScreen(', '.setScreen(').replace('.gui.screen()', '.screen')
    else:
        text=text.replace('dev.worldgen.lithostitched.Lithostitched','dev.worldgen.lithostitched.impl.Lithostitched')
        text=text.replace('dev.worldgen.lithostitched.worldgen.structure.DelegatingStructure','dev.worldgen.lithostitched.impl.worldgen.structure.DelegatingStructure')
        if name=='DistributionPlacementMixin.java':text=text.replace('import net.minecraft.world.level.levelgen.structure.placement.StructurePlacement;', 'import net.minecraft.world.level.levelgen.structure.placement.AbstractSpreadingStructurePlacement;').replace('@Mixin(StructurePlacement.class)', '@Mixin(AbstractSpreadingStructurePlacement.class)')
        sampler='createClimateSampler(net.minecraft.world.level.levelgen.densityfunction.SamplerContext.EMPTY_UNCACHED)'
        text=text.replace('.sampler()', '.'+sampler)
        text=text.replace('context.biomeSource()', 'context.biomeResolver()')
        if name=='AllGridPlacementCondition.java':
            text=text.replace(', context.randomState().'+sampler, '')
        text=text.replace('generator.getBiomeSource().getNoiseBiome(', 'generator.getBiomeSource().createUncachedResolver(random).getNoiseBiome(')
        text=text.replace(',random.'+sampler+')', ')')
        if name=='DistributionRuntime.java':
            text=text.replace('level.getChunkSource().randomState().'+sampler+'.findSpawnPosition()',
              'net.minecraft.world.level.levelgen.NoiseSpawnFinder.findSpawnPosition(((net.minecraft.world.level.levelgen.NoiseBasedChunkGenerator)level.getChunkSource().getGenerator()).generatorSettings().value().spawnTarget(),level.getChunkSource().randomState().samplersWithContext(net.minecraft.world.level.levelgen.densityfunction.SamplerContext.EMPTY_UNCACHED))')
        text=text.replace('level.getStructureManager()', 'level.getStructureTemplateManager()')
        text=text.replace('startsForStructure(chunk,', 'startsForStructure(chunk.x(),chunk.z(),')
        text=text.replace('generator,generator.getBiomeSource(),random,templates,', 'generator,generator.getBiomeSource(),random.'+sampler+',random,templates,')
        text=text.replace('context.predicate().test(data.type(),pos,chunk)', 'context.predicate().test(data.type(),level,pos,chunk)')
        text=text.replace('.hurtMarked', '.needsSync').replace('.setInvulnerable(', '.setPermanentlyInvulnerable(')
        text=text.replace('player.drop(map,false)', 'player.drop(map,false,net.minecraft.util.Prediction.SERVER_ONLY)')
        if test:
            text=text.replace('(type,pos,ch)->', '(type,spawnLevel,pos,ch)->')
            if name=='RecipeNetworkChecks.java':text=text.replace('var parsed=Recipe.CODEC.parse(', 'var parsed=Recipe.DIRECT_CODEC.parse(')
            if name=='TreeAnimalChecks.java':
                text=text.replace('return NaturalSpawner.createState(chunks,entities,(key,consumer)->consumer.accept(level.getChunkSource().getChunkNow(ChunkPos.getX(key),ChunkPos.getZ(key))),', 'var state=de.relics.testmixin.SpawnStateProbe.relics$create(chunks,new it.unimi.dsi.fastutil.objects.Object2IntOpenHashMap<>(),new net.minecraft.world.level.PotentialCalculator(),')
                text=text.replace('new LocalMobCapCalculator(level.getChunkSource().chunkMap));', '''new LocalMobCapCalculator(level.getChunkSource().chunkMap));
        for(var entity:entities)((de.relics.testmixin.SpawnStateProbe)(Object)state).relics$after((Mob)entity,level.getChunkAt(entity.blockPosition()));
        return state;''')
        if name=='EarlyLithostitchedPreparation.java':
            text=text.replace('applyModifiersAndInjections(registries,','applyModifiersAndInjections(null,registries,')
            text=text.replace('    private EarlyLithostitchedPreparation() { }', '''    private static final ThreadLocal<Boolean> ACTIVE=ThreadLocal.withInitial(()->false);
    public static boolean preparing(){return ACTIVE.get();}
    private EarlyLithostitchedPreparation() { }''')
            text=text.replace('        try {', '        ACTIVE.set(true);\n        try {')
            text=text.replace('throw error;}', 'throw error;}finally{ACTIVE.remove();}')
        if name=='EarlyLithostitchedPreparationMixin.java':
            text=text.replace('relics$prepared(RegistryAccess registries,','relics$prepared(net.minecraft.server.MinecraftServer server,RegistryAccess registries,')
            text=text.replace('original.call(registries,dimensions,seed)', 'original.call(server,registries,dimensions,seed)')
    if test and name=='TreeAnimalChecks.java':
        start=text.index('                level.getRandom().setSeed(731204L);')
        end=text.index('                check(successes>0,',start)
        text=text[:start]+'''                // Plains can choose a horse-only pack. Sample independent capped
                // populations without changing the cap or the production hook.
                for(int trial=0;trial<20 && successes==0;trial++) {
                    for(var mob:level.getEntitiesOfClass(Mob.class,new net.minecraft.world.phys.AABB(4096,159,4096,4128,165,4128)))mob.discard();
                    population=state(level,289,List.of());
                    level.getRandom().setSeed(731204L+trial);
                    for(int i=0;i<4000 && population.getMobCategoryCounts().getInt(MobCategory.CREATURE)<10;i++)
                        NaturalSpawner.spawnForChunk(level,chunk,population,List.of(MobCategory.CREATURE));
                }
'''+text[end:]
    return text

def resources_for(output, minecraft):
    from build import write_archive
    resources = output / 'resources'
    packaged = output.parent / 'source-resources.jar'
    write_archive(packaged)
    with zipfile.ZipFile(packaged) as archive:
        archive.extractall(resources)
    target = TARGETS[minecraft]
    data_format = target['data_pack']
    (resources / 'pack.mcmeta').write_text(json.dumps({'pack': {
        'description': 'Titan Relics for Minecraft ' + minecraft,
        'min_format': data_format, 'max_format': data_format}}, indent=2) + '\n')
    if minecraft=='26.3':
        def state_names(value):
            if isinstance(value,list):return [state_names(v) for v in value]
            if isinstance(value,dict):return {('id' if k=='Name' else 'properties' if k=='Properties' else k):state_names(v) for k,v in value.items()}
            return value
        for path in (resources/'data').rglob('*.json'):
            path.write_text(json.dumps(state_names(json.loads(path.read_text())),indent=2)+'\n')
        (resources/'assets/minecraft/atlases/armor_trims.json').unlink()
        for path in (resources/'assets/relics/textures/trims/entity').rglob('*.png'):
            path.with_suffix('.png.mcmeta').write_text(json.dumps({'palette':{'base_palette':'minecraft:trim_base'}})+'\n')
    for path in resources.glob('relics.*integration.json'):
        data = json.loads(path.read_text())
        data['compatibility_target'] = minecraft
        path.write_text(json.dumps(data, indent=2) + '\n')
    return resources


def prepare(loader, minecraft, output_dir=None):
    if minecraft not in TARGETS:
        raise ValueError('Unknown additional Minecraft target')
    if loader == 'neoforge':
        return prepare_native(minecraft)
    if loader != 'fabric':raise ValueError('Unknown loader')
    target = TARGETS[minecraft]
    project = ROOT / f'compat/alpha5-{loader}-{minecraft}'
    output = output_dir or project / 'build/generated'
    if output.exists():
        assert output.resolve().is_relative_to((ROOT / 'compat').resolve())
        shutil.rmtree(output)
    output.mkdir(parents=True)
    resources = resources_for(output, minecraft)
    metadata = json.loads((resources / 'fabric.mod.json').read_text())
    metadata['version'] = release_version()
    metadata['depends'].update(minecraft=minecraft, java='>=' + str(target['java']),
                               lithostitched=target['lithostitched'])
    if minecraft=='1.21.11':
        metadata['depends'].pop('fabric-creative-tab-api-v1',None)
        metadata['depends']['fabric-item-group-api-v1']='*'
    (resources / 'fabric.mod.json').write_text(json.dumps(metadata, indent=2) + '\n')
    for name in ['relics.mixins.json', 'relics.client.mixins.json']:
        path = resources / name
        data = json.loads(path.read_text())
        data['compatibilityLevel'] = 'JAVA_' + str(target['java'])
        path.write_text(json.dumps(data, indent=2) + '\n')
    mixins = resources / 'relics.mixins.json'
    config = json.loads(mixins.read_text())
    if minecraft == '1.21.11':
        config['mixins'] += ['LithostitchedPreflightRegistryMixin','LithostitchedPreflightSeedMixin']
    else:
        config['mixins'] += ['AbstractOreFeatureMixin','LithostitchedPreflightLevelMixin']
    mixins.write_text(json.dumps(config,indent=2)+'\n')
    sources = []
    for base in [ROOT / 'src/main/java', ROOT / 'src/client/java']:
        for path in sorted(base.rglob('*.java')):
            relative = path.relative_to(base)
            destination = output / 'java' / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            text = port_java(path.name, path.read_text(), minecraft)
            override = project / 'src/main/adapters' / relative
            if override.exists():
                text = override.read_text()
            destination.write_text(text, encoding='utf-8', newline='\n')
            sources.append({'path': relative.as_posix(), 'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()})
    for path in sorted((project / 'src/main/adapters').rglob('*.java')):
        relative = path.relative_to(project / 'src/main/adapters')
        destination = output / 'java' / relative
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_text(path.read_text(),encoding='utf-8',newline='\n')
    from prepare_alpha5_neoforge import modern_checks, modern_recipe_packet
    tests = [ROOT / 'src/test/java/de/relics' / name for name in
             ['GameplayPresentationChecks.java', 'TreeAuraChecks.java', 'TreeAnimalChecks.java', 'TreeAnimalProbeMixin.java']]
    tests += [ROOT / 'compat/alpha5-fabric-1.21.1/src/test/adapters/de/relics' / name
              for name in ['PortChecks.java', 'RecipeNetworkChecks.java']]
    if minecraft=='1.21.11':tests.append(ROOT/'compat/alpha5-fabric-1.21.1/src/test/adapters/de/relics/testmixin/LegacyPlayerListAccess.java')
    for path in tests:
        text = path.read_text()
        if path.name in ['PortChecks.java', 'RecipeNetworkChecks.java']:
            text = modern_checks(text)
        if path.name == 'RecipeNetworkChecks.java':
            text = modern_recipe_packet(text)
        text = port_java(path.name, text, minecraft, test=True)
        destination = output / 'test/de/relics' / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding='utf-8', newline='\n')
    if minecraft=='26.3':
        probe=output/'test/de/relics/SpawnStateProbe.java'
        probe.write_text('''package de.relics.testmixin;
@org.spongepowered.asm.mixin.Mixin(net.minecraft.world.level.NaturalSpawner.SpawnState.class)
public interface SpawnStateProbe {
    @org.spongepowered.asm.mixin.gen.Invoker("<init>") static net.minecraft.world.level.NaturalSpawner.SpawnState relics$create(int chunks,it.unimi.dsi.fastutil.objects.Object2IntOpenHashMap<net.minecraft.world.entity.MobCategory> counts,net.minecraft.world.level.PotentialCalculator potential,net.minecraft.world.level.LocalMobCapCalculator caps){throw new AssertionError();}
    @org.spongepowered.asm.mixin.gen.Invoker("afterSpawn") void relics$after(net.minecraft.world.entity.Mob mob,net.minecraft.world.level.chunk.ChunkAccess chunk);
}
''')
    test_resources = output / 'test-resources'
    test_resources.mkdir()
    (test_resources / 'fabric.mod.json').write_text(json.dumps({
        'schemaVersion': 1, 'id': 'relics-port-checks', 'version': '1', 'environment': 'server',
        'entrypoints': {'main': ['de.relics.PortChecks', 'de.relics.GameplayPresentationChecks',
                                 'de.relics.TreeAuraChecks', 'de.relics.TreeAnimalChecks']},
        'mixins': ['animal-probe.mixins.json'], 'depends': {'relics': release_version()}}))
    (test_resources / 'animal-probe.mixins.json').write_text(json.dumps({
        'required': True, 'package': 'de.relics.testmixin', 'compatibilityLevel': 'JAVA_' + str(target['java']),
        'mixins': ['TreeAnimalProbeMixin']+(['LegacyPlayerListAccess'] if minecraft=='1.21.11' else ['SpawnStateProbe']), 'injectors': {'defaultRequire': 1}}))
    sources=[{'path':p.relative_to(output/'java').as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((output/'java').rglob('*.java'))]
    report = {'loader': loader, 'minecraft': minecraft, 'version': release_version(), 'sources': sources}
    if output_dir is None:(project / 'build/adapter-manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def prepare_native(minecraft):
    """Share the game adaptation with Fabric, then replace all loader entrypoints/APIs."""
    from prepare_alpha5_neoforge import COMMON, native_java, modern_platform, metadata, TARGETS as NATIVE_TARGETS
    project=ROOT/f'compat/alpha5-neoforge-{minecraft}'
    source=project/'build/fabric-adapted'
    prepare('fabric',minecraft,output_dir=source)
    target=TARGETS[minecraft]
    output=project/'build/generated'
    if output.exists():shutil.rmtree(output)
    shutil.copytree(source,output)
    resources=output/'resources';(resources/'fabric.mod.json').unlink()
    descriptor=resources/'META-INF/neoforge.mods.toml';descriptor.parent.mkdir(parents=True,exist_ok=True)
    descriptor.write_text(metadata(minecraft))
    for path in resources.glob('relics.*integration.json'):
        data=json.loads(path.read_text());data.update(loader='neoforge',protection_storage='neoforge:attachments/relics:placed_cells/sections')
        path.write_text(json.dumps(data,indent=2)+'\n')
    mixins=resources/'relics.mixins.json';data=json.loads(mixins.read_text());data['mixins'].remove('EarlyBiomePreparationMixin')
    mixins.write_text(json.dumps(data,indent=2)+'\n')
    def platform(name,text):
        result=modern_platform(name,text)
        if minecraft=='1.21.11' and name=='NeoEvents.java':
            result=result.replace('net.neoforged.neoforge.event.level.block.BreakBlockEvent','BlockEvent.BreakEvent').replace('event.setNotifyClient(true);','')
        if name=='NeoEvents.java':return result
        if minecraft=='1.21.11' and name=='RelicWorldgen.java':
            result=text.replace('ResourceLocation','Identifier')
        return port_java(name,result,minecraft)
    java=output/'java'
    for path in sorted(java.rglob('*.java')):
        if path.name in ['RelicModMenu.java','EarlyBiomePreparationMixin.java']:
            path.unlink();continue
        relative=path.relative_to(java);common=COMMON/relative
        path.write_text(platform(path.name,common.read_text()) if common.exists() else native_java(path.name,path.read_text(),minecraft))
    for path in sorted(COMMON.rglob('*.java')):
        destination=java/path.relative_to(COMMON)
        if not destination.exists():
            destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(platform(path.name,path.read_text()))
    tests=output/'test';shutil.rmtree(tests)
    for path in sorted((source/'test').rglob('*.java')):
        text=native_java(path.name,path.read_text(),minecraft,test=True)
        if minecraft=='26.3':text=text.replace('(type,pos,ch)->','(type,spawnLevel,pos,ch)->')
        package='de/relics/validation/mixin' if 'package de.relics.validation.mixin;' in text else 'de/relics/validation'
        destination=tests/package/path.name;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(text)
    common_tests=ROOT/'compat/alpha5-neoforge-common/src/test/adapters'
    for path in common_tests.rglob('*.java'):
        destination=tests/path.relative_to(common_tests);destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,destination)
    (tests/'de/relics/validation/PortTestMod.java').write_text('''package de.relics.validation;
@net.neoforged.fml.common.Mod("relics_port_checks")
public final class PortTestMod {
    public PortTestMod(){NativeSpawnChecks.initialize();new GameplayPresentationChecks().onInitialize();
        new TreeAuraChecks().onInitialize();new TreeAnimalChecks().onInitialize();new PortChecks().onInitialize();}
}
''')
    if minecraft!='1.21.11':
        access=ROOT/'compat/alpha5-fabric-1.21.1/src/test/adapters/de/relics/testmixin/LegacyPlayerListAccess.java'
        text=native_java(access.name,access.read_text(),minecraft,test=True)
        (tests/'de/relics/validation/mixin/LegacyPlayerListAccess.java').write_text(text)
    tr=output/'test-resources';shutil.rmtree(tr);(tr/'META-INF').mkdir(parents=True)
    (tr/'META-INF/neoforge.mods.toml').write_text(metadata(minecraft,'checks'))
    (tr/'animal-probe.mixins.json').write_text(json.dumps({'required':True,'package':'de.relics.validation.mixin',
        'compatibilityLevel':'JAVA_'+str(target['java']),'mixins':['TreeAnimalProbeMixin','LegacyPlayerListAccess','ConnectionChannelAccess']+(['SpawnStateProbe'] if minecraft=='26.3' else []),
        'injectors':{'defaultRequire':1}}))
    sources=[{'path':p.relative_to(java).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(java.rglob('*.java'))]
    report={'loader':'neoforge','minecraft':minecraft,'version':release_version(),'sources':sources,'neoforge':target['neoforge']}
    (project/'build/adapter-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
