package de.relics;

import com.google.gson.*;
import de.relics.distribution.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerWorldEvents;
import net.minecraft.commands.Commands;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.GameRules;
import net.minecraft.world.level.chunk.status.ChunkStatus;

/** Fabric 1.21.1 only, opt-in isolated loader probe. Never bundled in player JARs. */
public final class SurfaceStructureBootChecks implements ModInitializer {
    @Override public void onInitialize() {
        ServerWorldEvents.LOAD.register((server,level)->level.getGameRules().getRule(GameRules.RULE_SPAWN_CHUNK_RADIUS).set(0,server));
        CommandRegistrationCallback.EVENT.register((dispatcher,registries,environment)->dispatcher.register(Commands.literal("surfaceaudit").executes(context->{
            try {
                var level=context.getSource().getLevel();var runtime=DistributionRuntime.get(level);var gson=new GsonBuilder().setPrettyPrinting().create();
                var input=JsonParser.parseString(Files.readString(Path.of("surface-audit-input.json"))).getAsJsonObject();var output=new JsonObject();
                var actorField=DistributionRuntime.class.getDeclaredField("actor");actorField.setAccessible(true);var actor=(ScheduledExecutorService)actorField.get(runtime);
                var plannerField=DistributionRuntime.class.getDeclaredField("planner");plannerField.setAccessible(true);var planner=(DistributionPlanner)plannerField.get(runtime);
                var planned=new JsonArray();
                for(var e:input.getAsJsonArray("cells")) {
                    var a=e.getAsJsonArray();var cell=new DistributionPlanner.Cell(a.get(0).getAsInt(),a.get(1).getAsInt());
                    planned.add(gson.toJsonTree(actor.submit(()->planner.plan(cell)).get(180,TimeUnit.SECONDS)));
                }
                output.add("plans",planned);var starts=new JsonArray();
                for(var e:input.getAsJsonArray("starts")) {
                    var a=e.getAsJsonObject();int cx=a.get("x").getAsInt(),cz=a.get("z").getAsInt();String id=a.get("id").getAsString();
                    var chunk=level.getChunk(cx,cz,ChunkStatus.STRUCTURE_STARTS,true);
                    var type=level.registryAccess().registryOrThrow(Registries.STRUCTURE).get(ResourceLocation.parse(id));
                    var start=chunk.getStartForStructure(type);var row=new JsonObject();row.addProperty("id",id);row.addProperty("x",cx);row.addProperty("z",cz);
                    row.addProperty("valid",start!=null && start.isValid());row.addProperty("pieces",start!=null && start.isValid()?start.getPieces().size():0);
                    starts.add(row);
                }
                output.add("starts",starts);var blocks=new JsonArray();
                for(var e:input.getAsJsonArray("blocks")) {
                    var a=e.getAsJsonArray();var pos=new BlockPos(a.get(0).getAsInt(),a.get(1).getAsInt(),a.get(2).getAsInt());
                    level.getChunk(pos.getX()>>4,pos.getZ()>>4,ChunkStatus.FULL,true);var row=new JsonObject();row.add("position",e);
                    row.addProperty("block",net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(level.getBlockState(pos).getBlock()).toString());blocks.add(row);
                }
                output.add("blocks",blocks);output.add("runtime",JsonParser.parseString(runtime.status()));
                Files.writeString(Path.of("surface-audit-result.json"),gson.toJson(output));
                System.out.println("SURFACE_AUDIT_OK "+starts.size());return 1;
            }catch(Exception error){throw new IllegalStateException("Surface audit failed",error);}
        })));
    }
}
