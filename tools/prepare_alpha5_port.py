"""Generate isolated Alpha 5 source/resource adapters; preserve released targets."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import gzip
import struct
from prepare_mc1211 import port_java

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.1.0-alpha.5.0'


def legacy_java(name: str, text: str) -> str:
    initializers = [line for line in text.splitlines(True) if any(
        x in line for x in ('RelicItems.initialize();', 'RelicGameplay.initialize();', 'DistributionRuntime.initialize();'))]
    text = port_java(name, text)
    if name == 'RelicWorldgen.java':
        text = text.replace('    public void onInitialize() {', '    public void onInitialize() {\n' + ''.join(initializers))
    text = text.replace('.identifier()', '.location()')
    text = text.replace('net.minecraft.world.entity.animal.golem.', 'net.minecraft.world.entity.animal.')
    text = text.replace('net.minecraft.world.entity.animal.pig.Pig', 'net.minecraft.world.entity.animal.Pig')
    text = text.replace('net.minecraft.world.entity.animal.chicken.Chicken', 'net.minecraft.world.entity.animal.Chicken')
    text = text.replace('EntityTypes', 'EntityType').replace('EntitySpawnReason', 'MobSpawnType')
    text = text.replace('.snapTo(', '.moveTo(')
    text = text.replace('.markUnsaved()', '.setUnsaved(true)')
    text = text.replace('height.getMaxY()', '(height.getMaxBuildHeight()-1)')
    text = text.replace('import net.minecraft.server.permissions.Permissions;\n', '')
    text = re.sub(r'source\s*->\s*source.permissions\(\).hasPermission\((?:net.minecraft.server.permissions.)?Permissions.COMMANDS_GAMEMASTER\)', 'source -> source.hasPermission(2)', text)
    text = text.replace('player.level()', 'player.serverLevel()')
    text = text.replace('getInventory().getNonEquipmentItems()', 'getInventory().items')
    text = text.replace('inventory.getNonEquipmentItems()', 'inventory.items')
    text = text.replace('MobEffects.RESISTANCE', 'MobEffects.DAMAGE_RESISTANCE')
    text = text.replace('Blocks.FIREFLY_BUSH', 'Blocks.FERN')
    text = re.sub(r'(EntityType\.\w+)\.create\(level,\s*MobSpawnType\.\w+\)', r'\1.create(level)', text)
    text = text.replace('EntityType.ENDERMAN.canSpawn(level)', '(level.getDifficulty()!=net.minecraft.world.Difficulty.PEACEFUL)')
    text = text.replace('getStateData()', 'getData()').replace('TrialSpawnerStateData', 'TrialSpawnerData')
    text = text.replace('getWorldData().overworldData().getRespawnData().pos()', 'overworld().getSharedSpawnPos()')
    text = text.replace('getWorldGenSettings().options()', 'getWorldData().worldGenOptions()')
    if name in ('DistributionRuntime.java','NaturalInteriors.java'):
        text = text.replace('pos.x()', 'pos.x').replace('pos.z()', 'pos.z')
        text = text.replace('chunk.x()', 'chunk.x').replace('chunk.z()', 'chunk.z')
    text = text.replace('getPos().x()', 'getPos().x').replace('getPos().z()', 'getPos().z')
    if name == 'RelicItems.java':
        text = text.replace('net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents','net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents')
        text = text.replace('CreativeModeTabEvents.modifyOutputEvent', 'ItemGroupEvents.modifyEntriesEvent')
        text = text.replace('.setId(ResourceKey.create(Registries.ITEM, id(name)))', '')
        text = text.replace('SmithingTemplateItem.createArmorTrimTemplate(properties("monolith_armor_trim_smithing_template"))','SmithingTemplateItem.createArmorTrimTemplate(id("monolith"))')
        text = text.replace('var model = id((core ? "machine_core" : "salvage_magnet") + suffix);', 'var model = new net.minecraft.world.item.component.CustomModelData(left == capacity ? 0 : left == 0 ? 2 : 1);')
        text = text.replace('DataComponents.ITEM_MODEL', 'DataComponents.CUSTOM_MODEL_DATA')
    if name == 'BudgetItem.java':
        text = text.replace('import net.minecraft.world.item.component.TooltipDisplay;\n','')
        text = text.replace('ItemStack stack, ServerLevel level, Entity entity, EquipmentSlot slot','ItemStack stack, net.minecraft.world.level.Level level, Entity entity, int slot, boolean selected')
        text = text.replace('TooltipContext context, TooltipDisplay display,\n                                          Consumer<Component> tooltip','TooltipContext context, java.util.List<Component> tooltip')
        text = text.replace('tooltip.accept(', 'tooltip.add(')
    if name == 'RelicGameplay.java':
        text = text.replace('START_LEVEL_TICK', 'START_WORLD_TICK')
        start=text.index('        UseItemCallback.EVENT.register('); end=text.index('        GameplayFixtures.initialize();',start)
        callback=text[start:end].replace('return InteractionResult.PASS;', 'return net.minecraft.world.InteractionResultHolder.pass(player.getItemInHand(hand));').replace('return InteractionResult.SUCCESS;', 'return net.minecraft.world.InteractionResultHolder.success(player.getItemInHand(hand));')
        text=text[:start]+callback+text[end:]
        text=text.replace('var key=ResourceKey.create(Registries.RECIPE,RelicItems.id(core?"machine_core_recharge":"salvage_magnet_repair"));', 'var key=RelicItems.id(core?"machine_core_recharge":"salvage_magnet_repair");')
        text=text.replace('data.getCompoundOrEmpty(AttachmentTarget.NBT_ATTACHMENT_KEY).getListOrEmpty("relics:delivery_receipts")', 'data.getCompound(AttachmentTarget.NBT_ATTACHMENT_KEY).getList("relics:delivery_receipts",8)')
        text=text.replace('tag.asString().orElse(null)', 'tag.getAsString()')
        text=re.sub(r'(\w+)\.getTrialSpawner\(\)\.overrideEntityToSpawn\(EntityType\.IRON_GOLEM,\s*level\)', r'RelicPresentation.preview(\1.getTrialSpawner())', text)
    if name == 'TrialPresentationAccessor.java':
        text=text.replace('\n}', '''
    @Accessor("nextSpawnData") void relics$previewData(java.util.Optional<net.minecraft.world.level.SpawnData> data);
}''')
    if name == 'RelicPresentation.java':
        text=text.replace('    private RelicPresentation() { }', '''    private RelicPresentation() { }
    public static void preview(TrialSpawner spawner) {
        var entity=new net.minecraft.nbt.CompoundTag();entity.putString("id","minecraft:iron_golem");
        ((TrialPresentationAccessor)(Object)spawner.getData()).relics$previewData(java.util.Optional.of(new net.minecraft.world.level.SpawnData(entity,java.util.Optional.empty(),java.util.Optional.empty())));
        spawner.markUpdated();
    }
''')
    if name == 'TreeAnimalCapAccess.java':
        text=text.replace('    @Invoker("canSpawnForCategoryGlobal") boolean relics$global(MobCategory category);\n','')
        text=text.replace('@Invoker("canSpawnForCategoryLocal")', '@Invoker("canSpawnForCategory")')
    if name == 'TreeAnimals.java':
        text=text.replace('caps.relics$global(MobCategory.CREATURE)', 'global(context.state(),MobCategory.CREATURE)')
        text=text.replace('    private TreeAnimals() { }', '''    private TreeAnimals() { }
    public static boolean global(NaturalSpawner.SpawnState state,MobCategory category) {
        return state.getMobCategoryCounts().getInt(category)<category.getMaxInstancesPerChunk()*state.getSpawnableChunkCount()/289;
    }
''')
    if name == 'NaturalInteriors.java':
        text=text.replace('block("waxed_copper_chest")','block("chest")')
        text=text.replace('(level,chunk,generated)->', '(level,chunk)->')
        text=text.replace('BuiltInRegistries.BLOCK.getValue(id)', 'BuiltInRegistries.BLOCK.get(id)')
        text=text.replace('element.getTemplateLocation()', '((de.relics.mixin.LegacyPoolTemplateAccess)(Object)element).relics$template().left().orElseThrow()')
    if name == 'TerrainValidator.java':
        text=text.replace('t.key().location()', 't.getFirst().location()').replace('tag.stream()', 'tag.getSecond().stream()').replace('tag.key().location()', 'tag.getFirst().location()')
        text=text.replace('structures.getOrThrow(ResourceKey.create(Registries.STRUCTURE,id(name)))', 'structures.getHolderOrThrow(ResourceKey.create(Registries.STRUCTURE,id(name)))')
    if name == 'TreeAnimals.java': text=text.replace('choice.get().type()', 'choice.get().type').replace('data.type()', 'data.type')
    if name == 'TreeAnimalSpawnMixin.java': text=text.replace('List<MobCategory> categories','boolean friendly,boolean hostile,boolean persistent')
    if name == 'NaturalPieceMixin.java': text=text.replace('tag.getString("relics_natural_site").orElse(null)', 'tag.contains("relics_natural_site",8)?tag.getString("relics_natural_site"):null')
    if name == 'DistributionLocateMixin.java':
        text=text.replace('registry.listElements()', 'registry.holders()')
        text=text.replace('new net.minecraft.network.chat.ClickEvent.SuggestCommand(', 'new net.minecraft.network.chat.ClickEvent(net.minecraft.network.chat.ClickEvent.Action.SUGGEST_COMMAND,')
    if name == 'DistributionSpawnMixin.java':
        text=text.replace('import net.minecraft.server.level.progress.LevelLoadListener;\n', '')
        text=text.replace('ZZLnet/minecraft/server/level/progress/LevelLoadListener;', 'ZZ')
        text=text.replace('boolean debug,LevelLoadListener listener,Operation<Void>', 'boolean debug,Operation<Void>')
        text=text.replace('original.call(level,data,bonus,debug,listener)', 'original.call(level,data,bonus,debug)')
    if name == 'DistributionChunkMapAccessor.java':
        text=text.replace('import net.minecraft.server.level.ChunkTaskDispatcher;', 'import net.minecraft.util.thread.ProcessorHandle;\nimport net.minecraft.server.level.ChunkTaskPriorityQueueSorter;')
        text=text.replace('@Accessor("worldgenTaskDispatcher")', '@Accessor("worldgenMailbox")')
        text=text.replace('ChunkTaskDispatcher relics$worldgenDispatcher()', 'ProcessorHandle<ChunkTaskPriorityQueueSorter.Message<Runnable>> relics$worldgenDispatcher()')
    if name == 'DistributionStartsMixin.java':
        text=text.replace('dispatcher.submit(task,', 'dispatcher.tell(net.minecraft.server.level.ChunkTaskPriorityQueueSorter.message(task,')
        text=text.replace('center::getQueueLevel);', 'center::getQueueLevel));')
    if name == 'DefenseGolemMixin.java':
        text=text.replace('import net.minecraft.world.level.storage.ValueInput;', 'import net.minecraft.nbt.CompoundTag;')
        text=text.replace('import net.minecraft.world.level.storage.ValueOutput;\n', '')
        text=text.replace('ValueInput input', 'CompoundTag input').replace('ValueOutput output','CompoundTag output')
        text=text.replace('input.getStringOr("relics_defense_encounter", null)', 'input.contains("relics_defense_encounter",8)?input.getString("relics_defense_encounter"):null')
        text=text.replace('(target, world) ->', 'target ->')
    if name == 'ExpeditionMapMixin.java':
        text=text.replace('ServerLevel level, Entity entity, EquipmentSlot slot, CallbackInfo ci', 'net.minecraft.world.level.Level level, Entity entity, int slot, boolean selected, CallbackInfo ci')
        text=text.replace('if (RelicGameplay.updateMap(stack, level))', 'if (level instanceof ServerLevel server && RelicGameplay.updateMap(stack, server))')
    if name == 'CoreFurnaceMixin.java':
        text=text.replace('import net.minecraft.world.level.storage.ValueInput;', 'import net.minecraft.nbt.CompoundTag;\nimport net.minecraft.core.HolderLookup;')
        text=text.replace('import net.minecraft.world.level.storage.ValueOutput;\n','')
        text=text.replace('ValueInput input, CallbackInfo ci','CompoundTag input, HolderLookup.Provider registries, CallbackInfo ci')
        text=text.replace('ValueOutput output, CallbackInfo ci','CompoundTag output, HolderLookup.Provider registries, CallbackInfo ci')
        text=text.replace('input.getBooleanOr("relics_core_mode", false)', 'input.getBoolean("relics_core_mode")')
        text=text.replace('litTimeRemaining','litTime').replace('litTotalTime','litDuration').replace('cookingTimer','cookingProgress')
        text=text.replace('boolean canBurn(NonNullList<ItemStack> items, int maximum, ItemStack output)', 'boolean canBurn(net.minecraft.core.RegistryAccess registries, net.minecraft.world.item.crafting.RecipeHolder<?> recipe, NonNullList<ItemStack> items, int maximum)')
        text=text.replace('void burn(NonNullList<ItemStack> items, ItemStack input, ItemStack output)', 'boolean burn(net.minecraft.core.RegistryAccess registries, net.minecraft.world.item.crafting.RecipeHolder<?> recipe, NonNullList<ItemStack> items, int maximum)')
        text=text.replace('relics$tick(ServerLevel level,', 'relics$tick(net.minecraft.world.level.Level rawLevel,')
        text=text.replace('        CoreFurnaceMixin self =', '        if (!(rawLevel instanceof ServerLevel level)) return;\n        CoreFurnaceMixin self =')
        text=text.replace('assemble(new SingleRecipeInput(input))','assemble(new SingleRecipeInput(input),level.registryAccess())')
        text=text.replace('canBurn(self.items, furnace.getMaxStackSize(), result)', 'canBurn(level.registryAccess(), recipe, self.items, furnace.getMaxStackSize())')
        text=text.replace('burn(self.items, input, result)', 'burn(level.registryAccess(), recipe, self.items, furnace.getMaxStackSize())')
        text=text.replace('.cookingTime()', '.getCookingTime()')
    return text


def legacy_resources(resources: Path):
    """Replace the single unavailable vegetation block, keeping every cell and NBT field."""
    changes={}
    old=b'minecraft:firefly_bush';new=b'minecraft:fern'
    for path in sorted((resources/'data/relics/structure').glob('*.nbt')):
        content=path.read_bytes();raw=gzip.decompress(content)
        needle=struct.pack('>H',len(old))+old
        if needle not in raw: continue
        raw=raw.replace(needle,struct.pack('>H',len(new))+new)
        path.write_bytes(gzip.compress(raw,mtime=0))
        changes[path.name]={'source_sha256':hashlib.sha256(content).hexdigest(),'target_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    for path in sorted(resources.glob('relics.*integration.json')):
        data=json.loads(path.read_text(encoding='utf-8').replace('"minecraft:waxed_copper_chest"','"minecraft:chest"'))
        for entry in data['structures']:
            for field in ('single_template','worldgen_template'):
                record=entry[field]
                if record['path'] in changes:record['sha256']=changes[record['path']]['target_sha256']
            if entry['single_template']['path'] in changes:entry['sha256']=entry['single_template']['sha256']
            if 'gameplay' in entry:
                entry['gameplay']['replaceable_blocks']=[b for b in entry['gameplay'].get('replaceable_blocks',[]) if b not in ('minecraft:bush','minecraft:pale_oak_log','minecraft:pale_oak_leaves')]
        data['compatibility_target']='1.21.1'
        data['block_substitutions']={'minecraft:firefly_bush':'minecraft:fern','minecraft:waxed_copper_chest':'minecraft:chest'}
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    # 1.21.1 uses integer custom-model data and the older armor-trim atlas layout.
    for item in ('machine_core','salvage_magnet'):
        path=resources/f'assets/relics/models/item/{item}.json';data=json.loads(path.read_bytes())
        data['overrides']=[{'predicate':{'custom_model_data':i},'model':f'relics:item/{item}_{suffix}'} for i,suffix in ((1,'partial'),(2,'empty'))]
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    for path in sorted((resources/'data/relics/recipe').glob('*.json')):
        data=json.loads(path.read_bytes())
        def ingredient(value):
            if isinstance(value,str):return {'tag':value[1:]} if value.startswith('#') else {'item':value}
            return value
        if data['type']=='minecraft:crafting_shaped':data['key']={k:ingredient(v) for k,v in data['key'].items()}
        if data['type']=='minecraft:smithing_trim':
            for field in ('template','base','addition'):data[field]=ingredient(data[field])
            data.pop('pattern',None)
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    trim=resources/'data/relics/trim_pattern/monolith.json';data=json.loads(trim.read_bytes());data['template_item']='relics:monolith_armor_trim_smithing_template'
    trim.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    atlas=resources/'assets/minecraft/atlases/armor_trims.json';data=json.loads(atlas.read_bytes())
    for source in data['sources']:
        source['textures']=['relics:trims/models/armor/monolith','relics:trims/models/armor/monolith_leggings']
        source['permutations'].pop('resin',None)
    atlas.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    destination=resources/'assets/relics/textures/trims/models/armor';destination.mkdir(parents=True,exist_ok=True)
    for source,target in (('humanoid/monolith','monolith'),('humanoid_leggings/monolith','monolith_leggings')):
        shutil.copy2(resources/f'assets/relics/textures/trims/entity/{source}.png',destination/f'{target}.png')
    return changes


def legacy_test(name: str,text: str) -> str:
    text=legacy_java(name,text)
    text=text.replace('io.netty.channel.ChannelFutureListener','net.minecraft.network.PacketSendListener')
    text=text.replace('getNonEquipmentItems()', 'items')
    text=text.replace('NaturalSpawner.spawnForChunk(level,chunk,population,List.of(MobCategory.CREATURE))','NaturalSpawner.spawnForChunk(level,chunk,population,true,false,true)')
    text=text.replace('((TreeAnimalCapAccess)(Object)global).relics$global(MobCategory.CREATURE)', 'TreeAnimals.global(global,MobCategory.CREATURE)')
    text=text.replace('player.load(net.minecraft.world.level.storage.TagValueInput.create(net.minecraft.util.ProblemReporter.DISCARDING,level.registryAccess(),\n                    net.minecraft.nbt.NbtIo.readCompressed(saved,net.minecraft.nbt.NbtAccounter.unlimitedHeap())))', 'player.load(net.minecraft.nbt.NbtIo.readCompressed(saved,net.minecraft.nbt.NbtAccounter.unlimitedHeap()))')
    text=re.sub(r'(\w+)\.getServer\(\)\.getPlayerList\(\)\.getPlayersByUUID\(\)', r'((de.relics.testmixin.LegacyPlayerListAccess)(Object)\1.getServer().getPlayerList()).relics$players()', text)
    text=text.replace('contains(recipe)', 'contains(recipe.location())')
    text=text.replace('ClientboundRecipeBookAddPacket r && !r.entries().isEmpty()', 'ClientboundRecipePacket r && !r.getRecipes().isEmpty()')
    text=text.replace('.hurtServer(world,', '.hurt(')
    return text


def prepare(loader='fabric', minecraft='1.21.1'):
    if loader != 'fabric' or minecraft != '1.21.1':
        raise ValueError('This adapter currently supports the first requested target only')
    project = ROOT / 'compat/alpha5-fabric-1.21.1'
    output = project / 'build/generated'
    # Only recreate this generated directory; old profiles and their artifacts are untouched.
    if output.exists():
        assert output.resolve().is_relative_to((project/'build').resolve())
        shutil.rmtree(output)
    resources = output/'resources'
    resources.mkdir(parents=True)
    from build import write_archive
    import zipfile
    # Share the exact selected resources, including all frozen interior revisions.
    packaged = project/'build/source-resources.jar'
    write_archive(packaged)
    with zipfile.ZipFile(packaged) as archive:
        archive.extractall(resources)
    metadata = json.loads((resources/'fabric.mod.json').read_bytes())
    metadata['version'] = VERSION
    metadata['depends'].update(minecraft='1.21.1', java='>=21')
    metadata['depends'].pop('fabric-resource-loader-v1', None)
    metadata['depends']['fabric-resource-loader-v0'] = '*'
    metadata['depends'].pop('fabric-creative-tab-api-v1', None)
    metadata['depends']['fabric-item-group-api-v1'] = '*'
    (resources/'fabric.mod.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    (resources/'pack.mcmeta').write_text(json.dumps({'pack':{'pack_format':48,'supported_formats':[34,48],'description':'Relic Mod Alpha 5.0 for Fabric 1.21.1'}})+'\n',encoding='utf-8')
    mixins = json.loads((resources/'relics.mixins.json').read_bytes())
    mixins['compatibilityLevel'] = 'JAVA_21'
    mixins['mixins'].append('LegacyPoolTemplateAccess')
    (resources/'relics.mixins.json').write_text(json.dumps(mixins,indent=2)+'\n',encoding='utf-8')
    substitutions=legacy_resources(resources)
    sources=[]
    for source in sorted((ROOT/'src/main/java').rglob('*.java')):
        relative=source.relative_to(ROOT/'src/main/java')
        destination=output/'java'/relative
        destination.parent.mkdir(parents=True,exist_ok=True)
        text=legacy_java(source.name,source.read_text(encoding='utf-8'))
        override=project/'src/main/adapters'/relative
        if override.exists(): text=override.read_text(encoding='utf-8')
        destination.write_text(text,encoding='utf-8',newline='\n')
        sources.append({'path':relative.as_posix(),'sha256':hashlib.sha256(destination.read_bytes()).hexdigest()})
    for adapter in sorted((project/'src/main/adapters').rglob('*.java')):
        relative=adapter.relative_to(project/'src/main/adapters');destination=output/'java'/relative
        if destination.exists():continue
        destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(adapter,destination)
        sources.append({'path':relative.as_posix(),'sha256':hashlib.sha256(destination.read_bytes()).hexdigest()})
    for name in ('GameplayPresentationChecks.java','TreeAuraChecks.java','TreeAnimalChecks.java','TreeAnimalProbeMixin.java','NaturalInteriorChecks.java','DistributionRuntimeChecks.java'):
        source=ROOT/'src/test/java/de/relics'/name
        destination=output/'test/de/relics'/name;destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_text(legacy_test(name,source.read_text(encoding='utf-8')),encoding='utf-8',newline='\n')
    for adapter in sorted((project/'src/test/adapters').rglob('*.java')):
        destination=output/'test'/adapter.relative_to(project/'src/test/adapters')
        destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(adapter,destination)
    test_resources=output/'test-resources';test_resources.mkdir(parents=True)
    (test_resources/'fabric.mod.json').write_text(json.dumps({'schemaVersion':1,'id':'relics-port-checks','version':'1','environment':'server',
        'entrypoints':{'main':['de.relics.GameplayPresentationChecks','de.relics.TreeAuraChecks','de.relics.TreeAnimalChecks','de.relics.PortChecks','de.relics.NaturalInteriorChecks','de.relics.DistributionRuntimeChecks']},
        'mixins':['animal-probe.mixins.json'],'depends':{'relics':'*'}}),encoding='utf-8')
    (test_resources/'animal-probe.mixins.json').write_text(json.dumps({'required':True,'package':'de.relics.testmixin','compatibilityLevel':'JAVA_21',
        'mixins':['TreeAnimalProbeMixin','LegacyPlayerListAccess'],'injectors':{'defaultRequire':1}}),encoding='utf-8')
    report={'loader':loader,'minecraft':minecraft,'version':VERSION,'sources':sources,'template_substitutions':substitutions}
    (project/'build/adapter-manifest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--loader',default='fabric')
    parser.add_argument('--minecraft',default='1.21.1')
    args=parser.parse_args()
    report=prepare(args.loader,args.minecraft)
    print(f"Prepared {report['loader']} {report['minecraft']}: {len(report['sources'])} Java sources")
