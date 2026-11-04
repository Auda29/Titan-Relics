package de.relics.testmixin;

import com.google.gson.*;
import java.lang.management.ManagementFactory;
import java.nio.file.*;
import java.util.*;
import net.minecraft.server.MinecraftServer;
import org.spongepowered.asm.mixin.*;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Test-only tick/heap/chunk telemetry. Contains no Relic dependency. */
@Mixin(MinecraftServer.class)
public abstract class BetaPerformanceProbe {
    @Unique private long relics$start;
    @Unique private int relics$ticks;
    @Unique private String relics$phase="startup";
    @Unique private final Map<String,List<Double>> relics$samples=new LinkedHashMap<>();
    @Unique private long relics$heapPeak;
    @Unique private int relics$ioRetries;

    @Inject(method="tickServer",at=@At("HEAD"))
    private void relics$begin(CallbackInfo ci){relics$start=System.nanoTime();}

    @Inject(method="tickServer",at=@At("RETURN"))
    private void relics$end(CallbackInfo ci)throws Exception{
        double elapsed=(System.nanoTime()-relics$start)/1e6;
        relics$samples.computeIfAbsent(relics$phase,k->new ArrayList<>()).add(elapsed);
        relics$heapPeak=Math.max(relics$heapPeak,ManagementFactory.getMemoryMXBean().getHeapMemoryUsage().getUsed());
        if(++relics$ticks%20!=0)return;
        try{
        if(Files.exists(Path.of("bench-phase.txt"))){var phase=Files.readString(Path.of("bench-phase.txt")).strip();if(!phase.isEmpty())relics$phase=phase;}
        var report=new JsonObject();report.addProperty("ticks",relics$ticks);report.addProperty("phase",relics$phase);report.addProperty("heapPeakBytes",relics$heapPeak);
        report.addProperty("probeIoRetries",relics$ioRetries);
        var phases=new JsonObject();
        for(var entry:relics$samples.entrySet()){
            var sorted=entry.getValue().stream().mapToDouble(Double::doubleValue).sorted().toArray();
            var row=new JsonObject();row.addProperty("ticks",sorted.length);
            row.addProperty("meanMs",Arrays.stream(sorted).average().orElse(0));
            row.addProperty("p95Ms",sorted[Math.max(0,(int)Math.ceil(sorted.length*.95)-1)]);
            row.addProperty("maxMs",sorted[sorted.length-1]);phases.add(entry.getKey(),row);
        }
        report.add("phases",phases);
        if(Files.exists(Path.of("bench-chunks-request.json"))){
            var request=JsonParser.parseString(Files.readString(Path.of("bench-chunks-request.json"))).getAsJsonObject();
            int loaded=0,total=0;var level=((MinecraftServer)(Object)this).overworld();
            for(int x=request.get("minX").getAsInt();x<=request.get("maxX").getAsInt();x++)
                for(int z=request.get("minZ").getAsInt();z<=request.get("maxZ").getAsInt();z++){total++;if(level.hasChunk(x,z))loaded++;}
            var chunks=new JsonObject();chunks.addProperty("id",request.get("id").getAsString());chunks.addProperty("loaded",loaded);chunks.addProperty("total",total);report.add("chunks",chunks);
        }
        Path temporary=Path.of("bench-metrics.pending.json"),target=Path.of("bench-metrics.json");
        Files.writeString(temporary,report.toString());Files.move(temporary,target,StandardCopyOption.REPLACE_EXISTING);
        }catch(java.io.IOException | JsonParseException transientReadOrRename){relics$ioRetries++;}
    }
}
