package de.relics.testmixin;

import com.google.gson.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.Consumer;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.chunk.ChunkAccess;
import net.minecraft.core.registries.Registries;
import org.spongepowered.asm.mixin.*;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Actual DH generator jobs, confined to a 2x2 region of a fresh test world. */
@Mixin(MinecraftServer.class)
public abstract class BetaDhGenerationProbe {
    @Unique private Object relics$generator;
    @Unique private CompletableFuture<?> relics$future;
    @Unique private ExecutorService relics$pool;
    @Unique private final List<JsonObject> relics$chunks=Collections.synchronizedList(new ArrayList<>());
    @Unique private final JsonObject relics$result=new JsonObject();
    @Unique private int relics$stage,relics$ticks,relics$x,relics$z;
    @Unique private int relics$minX,relics$minZ,relics$width=2;
    @Unique private long relics$started;

    @Inject(method="tickServer",at=@At("RETURN"))
    private void relics$test(CallbackInfo ci){
        if(++relics$ticks%5!=0 || relics$stage==3 || !Files.exists(Path.of("dh-request.json")))return;
        var server=(MinecraftServer)(Object)this;
        try{
            if(relics$stage==0){
                var file=server.getWorldPath(net.minecraft.world.level.storage.LevelResource.ROOT).resolve("data/relics_distribution_v1.json");
                if(!Files.exists(file))return;
                var envelope=JsonParser.parseString(Files.readString(file)).getAsJsonObject();
                var state=JsonParser.parseString(envelope.get("payload").getAsString()).getAsJsonObject();
                if(!state.has("unique") || state.get("unique").isJsonNull())return;
                var site=state.getAsJsonObject("unique");var candidate=site.getAsJsonObject("candidate");
                relics$x=Math.floorDiv(candidate.get("x").getAsInt(),16);relics$z=Math.floorDiv(candidate.get("z").getAsInt(),16);
                relics$result.add("site",site.deepCopy());
                var request=JsonParser.parseString(Files.readString(Path.of("dh-request.json"))).getAsJsonObject();
                relics$minX=Math.floorDiv(relics$x,2)*2;relics$minZ=Math.floorDiv(relics$z,2)*2;
                boolean full=request.has("fullFootprint") && request.get("fullFootprint").getAsBoolean();
                if(full){
                    relics$minX=Math.floorDiv(Math.floorDiv(site.get("minX").getAsInt(),16),2)*2;
                    relics$minZ=Math.floorDiv(Math.floorDiv(site.get("minZ").getAsInt(),16),2)*2;
                    int span=Math.max(Math.floorDiv(site.get("maxX").getAsInt(),16)-relics$minX+1,Math.floorDiv(site.get("maxZ").getAsInt(),16)-relics$minZ+1);
                    relics$width=((span+1)/2)*2;
                }
                var region=new JsonObject();region.addProperty("minChunkX",relics$minX);region.addProperty("minChunkZ",relics$minZ);region.addProperty("widthInChunks",relics$width);relics$result.add("requestedRegion",region);
                relics$result.addProperty("initiallyLoaded",server.overworld().hasChunk(relics$x,relics$z));
                if(server.overworld().hasChunk(relics$x,relics$z))throw new AssertionError("Target was already normally loaded");
                var wrapperClass=Class.forName("com.seibel.distanthorizons.common.wrappers.world.ServerLevelWrapper");
                var wrapper=wrapperClass.getMethod("getWrapper",ServerLevel.class).invoke(null,server.overworld());
                var dhLevel=wrapperClass.getMethod("getDhLevel").invoke(wrapper);if(dhLevel==null)return;
                var generatorClass=Class.forName("com.seibel.distanthorizons.common.wrappers.worldGeneration.DhChunkGenerator");
                relics$generator=generatorClass.getConstructors()[0].newInstance(dhLevel);
                relics$pool=Executors.newSingleThreadExecutor(r->{var t=new Thread(r,"Bounded DH compatibility probe");t.setDaemon(true);return t;});
                relics$queue(server,full?"INTERNAL_SERVER":"FEATURES");relics$stage=full?2:1;
            }else{
                relics$generator.getClass().getMethod("updateAllFutures").invoke(relics$generator);
                if(System.currentTimeMillis()-relics$started>180000)throw new AssertionError("Bounded DH generation timeout");
                if(!relics$future.isDone())return;
                relics$future.join();var row=new JsonObject();row.addProperty("seconds",(System.currentTimeMillis()-relics$started)/1000.0);
                var chunks=new JsonArray();for(var chunk:relics$chunks)chunks.add(chunk.deepCopy());row.add("chunks",chunks);
                row.addProperty("normallyLoadedAfter",server.overworld().hasChunk(relics$x,relics$z));
                relics$result.add(relics$stage==1?"FEATURES":"INTERNAL_SERVER",row);
                if(relics$stage==1){relics$queue(server,"INTERNAL_SERVER");relics$stage=2;}
                else{relics$result.addProperty("completed",true);Files.writeString(Path.of("dh-proof.json"),relics$result.toString());relics$generator.getClass().getMethod("close").invoke(relics$generator);relics$pool.shutdownNow();relics$stage=3;}
            }
        }catch(Throwable ex){
            try{relics$result.addProperty("failure",ex.toString());relics$result.addProperty("trace",Arrays.toString(ex.getStackTrace()));Files.writeString(Path.of("dh-proof.json"),relics$result.toString());}catch(Exception ignored){}
            if(relics$pool!=null)relics$pool.shutdownNow();relics$stage=3;
        }
    }

    @Unique @SuppressWarnings({"unchecked","rawtypes"})
    private void relics$queue(MinecraftServer server,String mode)throws Exception{
        relics$chunks.clear();relics$started=System.currentTimeMillis();
        Class<? extends Enum> modes=(Class<? extends Enum>)Class.forName("com.seibel.distanthorizons.api.enums.worldGeneration.EDhApiDistantGeneratorMode");
        Class<? extends Enum> steps=(Class<? extends Enum>)Class.forName("com.seibel.distanthorizons.api.enums.worldGeneration.EDhApiWorldGenerationStep");
        Consumer<Object> consumer=wrapped->{try{
            var chunk=(ChunkAccess)wrapped.getClass().getMethod("getChunk").invoke(wrapped);
            var row=new JsonObject();row.addProperty("chunkX",chunk.getPos().x());row.addProperty("chunkZ",chunk.getPos().z());
            var starts=new JsonArray();var registry=server.registryAccess().lookupOrThrow(Registries.STRUCTURE);
            for(var entry:chunk.getAllStarts().entrySet())if(entry.getValue().isValid())starts.add(registry.getKey(entry.getKey()).toString());
            row.add("validStructureStarts",starts);relics$chunks.add(row);
        }catch(Exception ex){throw new RuntimeException(ex);}};
        relics$future=(CompletableFuture<?>)relics$generator.getClass().getMethod("queueGenEvent",int.class,int.class,int.class,modes,steps,ExecutorService.class,Consumer.class)
                .invoke(relics$generator,relics$minX,relics$minZ,relics$width,Enum.valueOf(modes,mode),Enum.valueOf(steps,"FEATURES"),relics$pool,consumer);
    }
}
