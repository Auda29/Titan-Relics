package de.relics;

import com.google.gson.*;
import de.relics.distribution.DistributionPlanner.Site;
import de.relics.gameplay.*;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.attachment.v1.*;
import net.minecraft.commands.Commands;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.Container;
import net.minecraft.world.item.*;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.entity.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

/** Non-distributed native integration proof and restart/non-refill probe. */
public class NaturalInteriorChecks implements ModInitializer {
    private static final Gson JSON=new GsonBuilder().setPrettyPrinting().create();
    @Override public void onInitialize() {
        CommandRegistrationCallback.EVENT.register((dispatcher,registries,environment)->dispatcher.register(
            Commands.literal("relicsinteriorstest").then(Commands.literal("verify").executes(c->{check(c.getSource().getLevel(),false);return 1;}))
                    .then(Commands.literal("mutate").executes(c->{check(c.getSource().getLevel(),true);return 1;}))));
    }
    @SuppressWarnings("unchecked") private static void check(ServerLevel level,boolean mutate) {
        try {
            Path config=Path.of(System.getProperty("relics.interior.testConfig"));
            boolean restarted=Files.exists(config.resolveSibling("mutated.txt"));
            JsonArray rows=JsonParser.parseString(Files.readString(config)).getAsJsonArray();
            JsonArray proof=new JsonArray();
            var field=NaturalInteriors.class.getDeclaredField("DATA");field.setAccessible(true);
            var attachment=(AttachmentType<NaturalInteriors.ChunkData>)field.get(null);
            for(var row:rows) {
                Site site=JSON.fromJson(row,Site.class);
                String revision=de.relics.distribution.DistributionRuntime.get(level).interiorRevision();
                String encoded=NaturalInteriors.certificate(level.getSeed(),site,revision);
                var cert=JSON.fromJson(encoded,NaturalInteriors.Certificate.class);
                JsonObject asset=null;
                for(var a:NaturalInteriors.manifest(revision).getAsJsonArray("structures"))if(a.getAsJsonObject().get("id").getAsString().equals(site.asset()))asset=a.getAsJsonObject();
                if(asset==null)throw new AssertionError("No approved natural template");
                if(!asset.has("gameplay")) {
                    if(!site.asset().equals("titan_skull_2"))throw new AssertionError("Missing gameplay contract");
                    JsonObject visual=new JsonObject();visual.addProperty("asset",site.asset());
                    visual.addProperty("visual_only",true);visual.addProperty("version",asset.get("version").getAsString());
                    proof.add(visual);continue;
                }
                JsonObject report=new JsonObject();report.addProperty("asset",site.asset());report.addProperty("site_id",cert.site());
                JsonArray markers=new JsonArray();
                for(var item:asset.getAsJsonObject("gameplay").getAsJsonArray("markers")) {
                    var m=item.getAsJsonObject();BlockPos p=NaturalInteriors.marker(cert,m);String role=m.get("role").getAsString();
                    var chunk=level.getChunkSource().getChunkNow(p.getX()>>4,p.getZ()>>4);
                    if(chunk==null)throw new AssertionError("Footprint not fully loaded");
                    var data=((AttachmentTarget)chunk).getAttached(attachment);
                    String action=cert.site()+"/"+m.get("id").getAsString();
                    if(data==null || !data.completed.contains(action)){System.out.println("INTERIORS_PENDING");return;}
                    JsonObject rec=new JsonObject();rec.addProperty("role",role);rec.addProperty("x",p.getX());rec.addProperty("y",p.getY());rec.addProperty("z",p.getZ());
                    rec.addProperty("block",BuiltInRegistries.BLOCK.getKey(level.getBlockState(p).getBlock()).toString());
                    if(!restarted && m.has("facing") && level.getBlockState(p).hasProperty(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING)) {
                        var expected=net.minecraft.world.level.block.Rotation.values()[cert.rotation()].rotate(
                                net.minecraft.core.Direction.valueOf(m.get("facing").getAsString().toUpperCase(java.util.Locale.ROOT)));
                        if(level.getBlockState(p).getValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING)!=expected)
                            throw new AssertionError("Rotated marker facing differs at "+p);
                    }
                    if(role.endsWith("_chest")) {
                        if(restarted) {if(!level.getBlockState(p).isAir())throw new AssertionError("Removed chest refilled");}
                        else {
                            if(!(chunk.getBlockEntity(p) instanceof Container chest))throw new AssertionError("Missing copper chest");
                            JsonArray loot=new JsonArray();boolean fullMagnet=false;
                            for(int i=0;i<chest.getContainerSize();i++)if(!chest.getItem(i).isEmpty()) {
                                var stack=chest.getItem(i);JsonObject entry=new JsonObject();entry.addProperty("item",BuiltInRegistries.ITEM.getKey(stack.getItem()).toString());entry.addProperty("count",stack.getCount());loot.add(entry);
                                if(stack.is(RelicItems.SALVAGE_MAGNET))fullMagnet=stack.get(RelicItems.MAGNET_WEAR).remaining()==1000;
                            }
                            if(loot.isEmpty())throw new AssertionError("Uninitialized natural loot");
                            if(site.asset().equals("colossus") && !fullMagnet)throw new AssertionError("Missing full arm magnet");
                            if((site.asset().equals("colossus") && !revision.equals("interiors-20261027-v1")
                                    || site.asset().equals("small_colossus") && Set.of("interiors-20261028-v3","interiors-20261028-v4","interiors-20261028-v5").contains(revision)
                                    || site.asset().equals("ruined_tower") && Set.of("interiors-20261028-v4","interiors-20261028-v5").contains(revision))
                                    && !level.getBlockState(p.above()).isAir())throw new AssertionError("Terrain blocks chest lid");
                            rec.add("loot",loot);if(mutate)level.setBlock(p,Blocks.AIR.defaultBlockState(),3);
                        }
                    } else if(role.startsWith("archaeology_")) {
                        if(restarted) {if(level.getBlockState(p).is(Blocks.SUSPICIOUS_SAND))throw new AssertionError("Consumed archaeology refilled");}
                        else {
                            if(!(chunk.getBlockEntity(p) instanceof BrushableBlockEntity brush) || brush.getItem().isEmpty())throw new AssertionError("Empty archaeology");
                            if(role.equals("archaeology_trim") && !brush.getItem().is(RelicItems.MONOLITH_TEMPLATE))throw new AssertionError("Missing guaranteed trim");
                            if(role.equals("archaeology_map")) {
                                var ledger=RelicGameplay.ledger(level.getServer()).state;
                                var origin=ledger.origins.get(action);
                                if(ledger.targetUnavailable) {
                                    if(!brush.getItem().is(Items.EMERALD) || brush.getItem().getCount()!=3 || origin.phase!=GameplayLedger.OriginPhase.COMPENSATED)
                                        throw new AssertionError("Missing finite archaeology compensation");
                                    var replay=RelicGameplay.archaeologyMap(level,action);
                                    if(!replay.is(Items.EMERALD) || replay.getCount()!=3)throw new AssertionError("Interrupted compensation assignment cannot replay");
                                } else {
                                    if(!brush.getItem().is(Items.FILLED_MAP) || !action.equals(brush.getItem().get(RelicItems.MAP_ORIGIN))
                                            || origin.phase!=GameplayLedger.OriginPhase.MAP_RESOLVED || !origin.target.equals(ledger.committedTarget)
                                            || brush.getItem().get(net.minecraft.core.component.DataComponents.MAP_ID)==null)
                                        throw new AssertionError("Archaeology map must resolve to the shared committed target");
                                    rec.addProperty("target",origin.target.toString());rec.addProperty("map_id",origin.mapId);
                                }
                            }
                            rec.addProperty("item",BuiltInRegistries.ITEM.getKey(brush.getItem().getItem()).toString());
                            if(mutate)level.setBlock(p,Blocks.SAND.defaultBlockState(),3);
                        }
                    } else if(role.equals("colossus_vault") || role.equals("colossus_trial_spawner")) {
                        var be=chunk.getBlockEntity(p);if(be==null)throw new AssertionError("Encounter block absent");
                        String nbt=be.saveWithFullMetadata(level.registryAccess()).toString();
                        if(role.equals("colossus_vault") && !nbt.contains("relics:colossus_key"))throw new AssertionError("Vault key not configured");
                        if(!RelicGameplay.ledger(level.getServer()).state.sites.containsKey(cert.site()))throw new AssertionError("Natural trial registration missing");
                    } else if(role.equals("tower_enderman_spawn")) {
                        UUID uuid=UUID.nameUUIDFromBytes(action.getBytes(StandardCharsets.UTF_8));var entity=level.getEntity(uuid);
                        if(restarted && entity!=null)throw new AssertionError("Enderman regenerated after removal");
                        if(!restarted && EntityTypes.ENDERMAN.canSpawn(level) && entity==null)throw new AssertionError("Initial Enderman absent");
                        if(!EntityTypes.ENDERMAN.canSpawn(level) && entity!=null)throw new AssertionError("Hostile encounter present on Peaceful");
                        rec.addProperty("uuid",uuid.toString());if(mutate && entity!=null)entity.discard();
                    } else if(role.equals("tree_aura_anchor")) {
                        var anchor=RelicGameplay.ledger(level.getServer()).state.trees.get(cert.site());
                        if(anchor==null || anchor.x()!=p.getX() || anchor.y()!=p.getY() || anchor.z()!=p.getZ())throw new AssertionError("Natural Tree anchor missing");
                    }
                    markers.add(rec);
                }
                report.add("markers",markers);proof.add(report);
            }
            if(mutate)Files.writeString(config.resolveSibling("mutated.txt"),"consumed test loot and removed test entities\n");
            Files.writeString(config.resolveSibling(mutate?"native-before-mutation.json":restarted?"native-after-restart.json":"native-initial.json"),JSON.toJson(proof));
            System.out.println("INTERIORS_PASS "+(mutate?"mutated":restarted?"restart-no-refill":"initial"));
        }catch(Throwable failure){failure.printStackTrace();System.out.println("INTERIORS_FAIL "+failure);}
    }
}
