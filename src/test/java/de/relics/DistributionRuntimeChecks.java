package de.relics;

import com.google.gson.*;
import com.mojang.serialization.JsonOps;
import de.relics.gameplay.*;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.component.DataComponents;
import net.minecraft.resources.RegistryOps;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.MapItem;
import net.minecraft.world.level.storage.LevelResource;
import java.nio.file.*;
import java.util.*;

/** Separate, non-distributed test mod. Executes actual map codecs/storage in the production loader. */
public final class DistributionRuntimeChecks implements ModInitializer {
    private static final Map<MinecraftServer,List<ItemStack>> MAPS=new HashMap<>();
    private static final Set<MinecraftServer> DONE=new HashSet<>();
    @Override public void onInitialize() {
        ServerLifecycleEvents.SERVER_STARTED.register(server->{
            try {
                Path file=file(server);List<ItemStack> maps=new ArrayList<>();
                var ops=RegistryOps.create(JsonOps.INSTANCE,server.registryAccess());
                if(Files.exists(file)) {
                    for(JsonElement encoded:JsonParser.parseString(Files.readString(file)).getAsJsonArray())
                        maps.add(ItemStack.CODEC.parse(ops,encoded).getOrThrow());
                } else {
                    var first=RelicGameplay.createPendingMap(server.overworld(),"runtime-proof:first");
                    if(first.has(DataComponents.MAP_ID))throw new AssertionError("Uncommitted destination already has a map ID");
                    maps.add(first);maps.add(first.copy());
                    maps.add(RelicGameplay.createPendingMap(server.overworld(),"runtime-proof:second"));
                    JsonArray encoded=new JsonArray();for(ItemStack map:maps)encoded.add(ItemStack.CODEC.encodeStart(ops,map).getOrThrow());
                    Files.writeString(file,encoded.toString());
                    System.out.println("PASS: unresolved expedition maps have no map ID or fabricated target");
                }
                MAPS.put(server,maps);
            }catch(Exception error){throw new IllegalStateException("Distribution map runtime setup",error);}
        });
        ServerTickEvents.END_SERVER_TICK.register(server->{
            if(DONE.contains(server) || !MAPS.containsKey(server))return;
            var ledger=RelicGameplay.ledger(server);
            if(ledger.state.targetUnavailable) {
                for(ItemStack map:MAPS.get(server)) {
                    if(!RelicGameplay.updateMap(map,server.overworld()) || map.has(DataComponents.MAP_ID))
                        throw new AssertionError("Unavailable destination fabricated a resolved map");
                }
                DONE.add(server);
                System.out.println("Relic distribution unavailable checks passed: finite border exhausted; no fabricated target or map ID");
                return;
            }
            if(ledger.state.committedTarget==null)return;
            try {
                var maps=MAPS.get(server);Integer savedFirst=null;
                Path file=file(server);boolean reloaded=Files.exists(file);
                if(reloaded && maps.getFirst().has(DataComponents.MAP_ID))savedFirst=maps.getFirst().get(DataComponents.MAP_ID).id();
                for(ItemStack map:maps) {
                    if(RelicGameplay.updateMap(map,server.overworld()))throw new AssertionError("Committed target still pending");
                    var id=map.get(DataComponents.MAP_ID);
                    if(id==null || !ExpeditionMaps.matches(MapItem.getSavedData(id,server.overworld()),ledger.state.committedTarget))
                        throw new AssertionError("Map center/dimension differs from global destination");
                }
                if(!maps.get(0).get(DataComponents.MAP_ID).equals(maps.get(1).get(DataComponents.MAP_ID)))
                    throw new AssertionError("Copied map origin allocated a different map ID");
                if(savedFirst!=null && savedFirst!=maps.getFirst().get(DataComponents.MAP_ID).id())
                    throw new AssertionError("Reload replaced a valid saved map ID");
                var ops=RegistryOps.create(JsonOps.INSTANCE,server.registryAccess());JsonArray encoded=new JsonArray();
                for(ItemStack map:maps)encoded.add(ItemStack.CODEC.encodeStart(ops,map).getOrThrow());
                Files.writeString(file,new GsonBuilder().setPrettyPrinting().create().toJson(encoded));
                DONE.add(server);
                System.out.println("Relic distribution map checks passed: pending, two origins, copied map IDs, saved target and "+(reloaded?"actual reload":"actual server map codecs"));
            }catch(Exception error){throw new IllegalStateException("Distribution map runtime checks",error);}
        });
    }
    private static Path file(MinecraftServer server){return server.getWorldPath(LevelResource.ROOT).resolve("data/relics_distribution_test_maps.json");}
}
