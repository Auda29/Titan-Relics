package de.relics.gameplay;

import com.google.gson.*;
import com.mojang.serialization.Codec;
import de.relics.RelicProtection;
import de.relics.distribution.*;
import de.relics.mixin.NaturalBrushAccessor;
import net.fabricmc.fabric.api.attachment.v1.*;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerChunkEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.player.UseBlockCallback;
import net.fabricmc.fabric.api.event.player.PlayerBlockBreakEvents;
import net.minecraft.core.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.*;
import net.minecraft.world.Container;
import net.minecraft.world.entity.*;
import net.minecraft.world.item.*;
import net.minecraft.world.level.*;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.entity.*;
import net.minecraft.world.level.block.state.*;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.chunk.*;
import net.minecraft.world.level.levelgen.structure.*;
import net.minecraft.world.level.levelgen.structure.pools.SinglePoolElement;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import java.nio.charset.StandardCharsets;
import java.util.*;

/** Native chunk placement and server-thread, once-per-chunk gameplay initialization. */
public final class NaturalInteriors {
    public static final String REVISION="interiors-20261027-v1", LEGACY="legacy";
    private static final Gson JSON=new Gson();
    private static final Map<ServerLevel,Set<ChunkPos>> PENDING=new HashMap<>();
    public record Certificate(String revision,String asset,String site,int x,int y,int z,int rotation) { }
    public static final class ChunkData {
        public Map<String,Certificate> sites=new LinkedHashMap<>();
        public Set<String> completed=new HashSet<>();
    }
    private static final AttachmentType<ChunkData> DATA=AttachmentRegistry.create(
            Identifier.fromNamespaceAndPath("relics","natural_interiors"),b->b.initializer(ChunkData::new)
                    .persistent(Codec.STRING.xmap(s->JSON.fromJson(s,ChunkData.class),JSON::toJson)));
    private static final class Catalog {
        static final JsonObject MANIFEST=loadManifest();
        static final Map<String,JsonObject> ASSETS=new HashMap<>();
        static { for(var entry:MANIFEST.getAsJsonArray("structures")) {
            var asset=entry.getAsJsonObject();if(asset.has("gameplay"))ASSETS.put(asset.get("id").getAsString(),asset);
        } }
    }
    private static JsonObject loadManifest() {
        try(var in=NaturalInteriors.class.getResourceAsStream("/relics.gameplay.integration.json")) {
            if(in==null)throw new IllegalStateException("Missing approved gameplay contracts");
            var data=JsonParser.parseString(new String(in.readAllBytes(),StandardCharsets.UTF_8)).getAsJsonObject();
            if(!data.get("revision").getAsString().equals(REVISION))throw new IllegalStateException("Unknown interior revision");
            return data;
        }catch(Exception error){throw new IllegalStateException("Cannot read approved gameplay contracts",error);}
    }
    public static JsonObject manifest(){return Catalog.MANIFEST;}
    public static boolean hasAsset(String asset){return Catalog.ASSETS.containsKey(asset);}
    public static void initialize(){
        ServerChunkEvents.CHUNK_LOAD.register((level,chunk,generated)->{
            if(((AttachmentTarget)chunk).getAttached(DATA)!=null)PENDING.computeIfAbsent(level,key->new LinkedHashSet<>()).add(chunk.getPos());
        });
        ServerTickEvents.START_SERVER_TICK.register(server->{
            for(var entry:List.copyOf(PENDING.entrySet())) {
                var level=entry.getKey();if(level.getServer()!=server)continue;
                var positions=new ArrayList<>(entry.getValue());entry.getValue().clear();
                for(var pos:positions) {
                    var chunk=level.getChunkSource().getChunkNow(pos.x(),pos.z());
                    if(chunk!=null)load(level,chunk); // FULL future has been published; no chunk loads here.
                }
            }
        });
        ServerLifecycleEvents.SERVER_STOPPED.register(server->PENDING.keySet().removeIf(l->l.getServer()==server));
        UseBlockCallback.EVENT.register((player,level,hand,hit)->level instanceof ServerLevel serverLevel && pending(serverLevel,hit.getBlockPos())
                ?net.minecraft.world.InteractionResult.FAIL:net.minecraft.world.InteractionResult.PASS);
        PlayerBlockBreakEvents.BEFORE.register((level,player,pos,state,entity)->!(level instanceof ServerLevel serverLevel) || !pending(serverLevel,pos));
    }
    private static boolean pending(ServerLevel level,BlockPos pos) {
        var chunk=level.getChunkSource().getChunkNow(pos.getX()>>4,pos.getZ()>>4);if(chunk==null)return false;
        var data=((AttachmentTarget)chunk).getAttached(DATA);if(data==null)return false;
        for(var cert:data.sites.values())for(var entry:contract(cert).getAsJsonArray("markers")) {
            var marker=entry.getAsJsonObject();if(marker(cert,marker).equals(pos) && !data.completed.contains(cert.site()+"/"+marker.get("id").getAsString()))return true;
        }
        return false;
    }
    public static String certificate(long seed,DistributionPlanner.Site site) {
        return JSON.toJson(new Certificate(REVISION,site.asset(),"natural:"+seed+":"+site.asset()+":"+
                site.candidate().cell().x()+":"+site.candidate().cell().z(),site.originX(),site.originY(),site.originZ(),site.candidate().rotation()));
    }
    private static JsonObject contract(Certificate c) {
        if(!REVISION.equals(c.revision()) || c.rotation()<0 || c.rotation()>3 || !hasAsset(c.asset()) || !c.site().startsWith("natural:"))
            throw new IllegalStateException("Invalid frozen natural piece provenance");
        return Catalog.ASSETS.get(c.asset()).getAsJsonObject("gameplay");
    }
    public static BlockPos transform(Certificate cert,int x,int y,int z) {
        return StructureTemplate.transform(new BlockPos(x,y,z),Mirror.NONE,Rotation.values()[cert.rotation()],BlockPos.ZERO)
                .offset(cert.x(),cert.y(),cert.z());
    }
    public static BlockPos marker(Certificate cert,JsonObject marker) {
        var offset=contract(cert).getAsJsonArray("offset");var pos=marker.getAsJsonArray("pos");
        return transform(cert,pos.get(0).getAsInt()+offset.get(0).getAsInt(),pos.get(1).getAsInt()+offset.get(1).getAsInt(),pos.get(2).getAsInt()+offset.get(2).getAsInt());
    }
    private static Block block(String name) {
        var id=Identifier.withDefaultNamespace(name);
        if(!BuiltInRegistries.BLOCK.containsKey(id))throw new IllegalStateException("Missing native block "+id);
        return BuiltInRegistries.BLOCK.getValue(id);
    }
    public static void afterPlacement(WorldGenLevel level,StructureManager manager,BoundingBox box,ChunkPos chunk,
            PoolElementStructurePiece piece,String provenance) {
        Certificate cert=JSON.fromJson(provenance,Certificate.class);var contract=contract(cert);
        var runtime=DistributionRuntime.get(level.getLevel());
        if(runtime==null || !runtime.interiorRevision().equals(REVISION))throw new IllegalStateException("Natural interiors in a legacy world");
        if(!(piece.getElement() instanceof SinglePoolElement element) || !element.getTemplateLocation().toString().equals("relics:"+cert.asset()+"_gameplay_worldgen")
                || !piece.getPosition().equals(new BlockPos(cert.x(),cert.y(),cert.z())) || piece.getRotation().ordinal()!=cert.rotation())
            throw new IllegalStateException("Natural piece and frozen provenance disagree");
        var otherBoxes=manager.startsForStructure(chunk,s->!manager.registryAccess().lookupOrThrow(net.minecraft.core.registries.Registries.STRUCTURE)
                .getKey(s).toString().equals("relics:"+cert.asset())).stream().map(StructureStart::getBoundingBox).toList();
        Set<String> replaceable=new HashSet<>();contract.getAsJsonArray("replaceable_blocks").forEach(s->replaceable.add(s.getAsString()));
        for(var item:contract.getAsJsonArray("clearance_runs")) {
            var run=item.getAsJsonArray();int x=run.get(0).getAsInt(),y=run.get(1).getAsInt();
            for(int z=run.get(2).getAsInt();z<=run.get(3).getAsInt();z++) {
                BlockPos p=transform(cert,x,y,z);if(!box.isInside(p) || (p.getX()>>4)!=chunk.x() || (p.getZ()>>4)!=chunk.z())continue;
                if(otherBoxes.stream().anyMatch(b->b.isInside(p)) || RelicProtection.protectedAt(level,p))continue;
                BlockState state=level.getBlockState(p);
                if(state.isAir() || replaceable.contains(BuiltInRegistries.BLOCK.getKey(state.getBlock()).toString())) {
                    if(!state.isAir())level.setBlock(p,Blocks.AIR.defaultBlockState(),2);
                    RelicProtection.recordCell(level,p);
                }
            }
        }
        var owning=level.getChunk(chunk.x(),chunk.z());var data=((AttachmentTarget)owning).getAttachedOrCreate(DATA);
        Certificate previous=data.sites.putIfAbsent(cert.site(),cert);
        if(previous!=null && !previous.equals(cert))throw new IllegalStateException("Conflicting natural chunk provenance");
        for(var item:contract.getAsJsonArray("markers")) {
            var m=item.getAsJsonObject();String role=m.get("role").getAsString();
            BlockPos p=marker(cert,m);if(!box.isInside(p) || (p.getX()>>4)!=chunk.x() || (p.getZ()>>4)!=chunk.z())continue;
            BlockState replacement=null;
            if(role.endsWith("_chest"))replacement=block("waxed_copper_chest").defaultBlockState();
            else if(role.equals("colossus_trial_spawner"))replacement=Blocks.TRIAL_SPAWNER.defaultBlockState();
            else if(role.equals("colossus_vault"))replacement=Blocks.VAULT.defaultBlockState();
            else if(role.startsWith("archaeology_"))replacement=Blocks.SUSPICIOUS_SAND.defaultBlockState();
            if(replacement!=null) {
                String expected=m.get("expected_block").getAsString();
                if(!BuiltInRegistries.BLOCK.getKey(level.getBlockState(p).getBlock()).toString().equals(expected))
                    throw new IllegalStateException("Natural placeholder mismatch at "+p);
                if(replacement.hasProperty(BlockStateProperties.HORIZONTAL_FACING) && m.has("facing"))
                    replacement=replacement.setValue(BlockStateProperties.HORIZONTAL_FACING,Rotation.values()[cert.rotation()].rotate(Direction.valueOf(m.get("facing").getAsString().toUpperCase(Locale.ROOT))));
                int depth=RelicProtection.RELIC_PLACEMENT_DEPTH.get();RelicProtection.RELIC_PLACEMENT_DEPTH.set(depth+1);
                try{level.setBlock(p,replacement,2);}finally{RelicProtection.RELIC_PLACEMENT_DEPTH.set(depth);}
                RelicProtection.recordCell(level,p);
            }
        }
        owning.markUnsaved();
    }
    private static BlockPos role(Certificate c,String role) {
        for(var item:contract(c).getAsJsonArray("markers"))if(item.getAsJsonObject().get("role").getAsString().equals(role))return marker(c,item.getAsJsonObject());
        throw new IllegalStateException("Missing natural role "+role);
    }
    private static void load(ServerLevel level,LevelChunk chunk) {
        var data=((AttachmentTarget)chunk).getAttached(DATA);if(data==null)return;
        if(data.sites==null || data.completed==null)throw new IllegalStateException("Incomplete natural chunk action state");
        for(var cert:data.sites.values()) {
            if(cert.asset().equals("colossus"))RelicGameplay.registerNatural(level,cert.site(),role(cert,"colossus_trial_spawner"),role(cert,"colossus_golem_spawn"),role(cert,"colossus_vault"));
            if(cert.asset().equals("world_tree"))RelicGameplay.registerNaturalTree(level,cert.site(),role(cert,"tree_aura_anchor"));
            for(var item:contract(cert).getAsJsonArray("markers")) {
                var m=item.getAsJsonObject();BlockPos p=marker(cert,m);if(!new ChunkPos(p.getX()>>4,p.getZ()>>4).equals(chunk.getPos()))continue;
                String action=cert.site()+"/"+m.get("id").getAsString();if(data.completed.contains(action))continue;
                String role=m.get("role").getAsString();var random=new java.util.Random(seed(level.getSeed(),action));
                BlockEntity be=chunk.getBlockEntity(p);
                if(role.endsWith("_chest")) {
                    if(!(be instanceof Container chest))throw new IllegalStateException("Natural chest unavailable at "+p);
                    List<ItemStack> loot=chestLoot(cert.asset(),role,random);
                    for(int i=0;i<loot.size();i++)chest.setItem(i,loot.get(i));be.setChanged();
                } else if(role.startsWith("archaeology_")) {
                    if(!(be instanceof BrushableBlockEntity brush))throw new IllegalStateException("Natural archaeology unavailable at "+p);
                    ItemStack reward=switch(role) {
                        case "archaeology_trim"->new ItemStack(RelicItems.MONOLITH_TEMPLATE);
                        case "archaeology_map"->RelicGameplay.archaeologyMap(level,action);
                        default->ordinaryFind(random);
                    };
                    ((NaturalBrushAccessor)brush).relics$setItem(reward);be.setChanged();
                } else if(role.equals("colossus_vault") || role.equals("colossus_trial_spawner")) {
                    RelicGameplay.configureNaturalBlock(level,p,role);
                } else if(role.equals("tower_enderman_spawn")) {
                    UUID uuid=UUID.nameUUIDFromBytes(action.getBytes(StandardCharsets.UTF_8));
                    if(level.getEntity(uuid)==null) {
                        var mob=EntityTypes.ENDERMAN.create(level,EntitySpawnReason.STRUCTURE);
                        if(mob==null)throw new IllegalStateException("Cannot create natural Enderman");
                        mob.setUUID(uuid);mob.snapTo(p.getX()+.5,p.getY(),p.getZ()+.5,0,0);
                        if(!level.addFreshEntity(mob))throw new IllegalStateException("Cannot add natural Enderman "+uuid);
                    }
                }
                // Block entity contents and completed actions serialize together
                // in this owning chunk. Loading a saved completed chunk never refills it.
                data.completed.add(action);chunk.markUnsaved();
            }
        }
    }
    public static long seed(long seed,String action) {
        long h=0xcbf29ce484222325L;for(byte b:action.getBytes(StandardCharsets.UTF_8))h=(h^(b&255))*0x100000001b3L;
        return DistributionPlanner.mix(seed^h);
    }
    private static List<ItemStack> chestLoot(String asset,String role,java.util.Random r) {
        List<ItemStack> result=new ArrayList<>();
        if(asset.equals("ruined_tower")) {result.add(new ItemStack(r.nextInt(20)==0?Items.ENDER_EYE:Items.ENDER_PEARL,1));
            if(result.getFirst().is(Items.ENDER_PEARL))result.getFirst().setCount(4+r.nextInt(3));return result;}
        boolean large=asset.equals("colossus");
        result.add(new ItemStack(Items.COPPER_INGOT,(large?24:12)+r.nextInt(large?17:9)));
        result.add(new ItemStack(Items.IRON_INGOT,(large?8:4)+r.nextInt(large?9:5)));
        int dust=r.nextInt(large?5:3),shards=r.nextInt(large?3:2);
        if(dust>0)result.add(new ItemStack(Items.REDSTONE,dust));if(shards>0)result.add(new ItemStack(Items.AMETHYST_SHARD,shards));
        if(large && role.equals("colossus_arm_magnet_chest") || !large && r.nextInt(10)==0) {
            var magnet=new ItemStack(RelicItems.SALVAGE_MAGNET);
            if(!large)magnet.set(RelicItems.MAGNET_WEAR,new ItemBudget(1,0));result.add(magnet);
        }
        return result;
    }
    private static ItemStack ordinaryFind(java.util.Random r) {
        int roll=r.nextInt(100);
        Item item=roll<25?new Item[]{Items.ANGLER_POTTERY_SHERD,Items.ARCHER_POTTERY_SHERD,Items.ARMS_UP_POTTERY_SHERD,Items.BLADE_POTTERY_SHERD}[r.nextInt(4)]
                :roll<45?Items.CLAY_BALL:roll<60?Items.BRICK:roll<70?Items.BONE:roll<80?Items.STRING:roll<90?Items.WHEAT_SEEDS:roll<95?Items.IRON_NUGGET:Items.COPPER_INGOT;
        return new ItemStack(item);
    }
}
