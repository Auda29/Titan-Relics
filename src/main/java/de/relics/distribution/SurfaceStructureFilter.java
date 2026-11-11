package de.relics.distribution;

import java.util.*;
import java.util.concurrent.*;
import java.util.function.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.chunk.ChunkAccess;
import net.minecraft.world.level.chunk.status.*;
import net.minecraft.world.level.levelgen.structure.*;
import static de.relics.distribution.SurfaceStructurePolicy.*;

/** Only newly generated Overworld starts, before native cache/ref/terrain publication. */
public final class SurfaceStructureFilter {
    private record Frame(ServerLevel level,ChunkAccess chunk,StructurePublication publication) { }
    private static final ThreadLocal<Frame> ACTIVE=new ThreadLocal<>();
    private SurfaceStructureFilter() { }
    public static State snapshot(ServerLevel level) {
        int dependency=ChunkPyramid.GENERATION_PYRAMID.getStepTo(ChunkStatus.FULL).getAccumulatedRadiusOf(ChunkStatus.STRUCTURE_STARTS);
        // Native spawn stays within 128 blocks; include chunk rounding and the full generation halo.
        if(128L+16L*(dependency+2)>BOOTSTRAP_RADIUS)
            throw new IllegalStateException("Native initial-spawn dependencies exceed the supported surface-filter bootstrap region");
        var registry=level.registryAccess().lookupOrThrow(Registries.STRUCTURE);
        List<String> targets=new ArrayList<>(),exempt=new ArrayList<>();
        registry.getTags().forEach(tag->{
            String name=tag.key().location().toString();
            List<String> dest=name.equals("relics:surface_overlap_targets")?targets:name.equals("relics:surface_overlap_exempt")?exempt:null;
            if(dest!=null)tag.stream().map(h->h.unwrapKey().orElseThrow().identifier().toString()).forEach(dest::add);
        });
        return new State(REVISION,BOOTSTRAP_RADIUS,targets,exempt);
    }
    public static CompletableFuture<ChunkAccess> around(ServerLevel level,ChunkAccess chunk,
            Supplier<CompletableFuture<ChunkAccess>> original,Executor nativeLane) {
        var runtime=DistributionRuntime.get(level);
        if(runtime==null || runtime.surfacePolicy()==null)return original.get();
        // Loading already persisted starts uses loadStructureStarts, never this wrapper.
        var publication=new StructurePublication();Frame previous=ACTIVE.get();
        CompletableFuture<ChunkAccess> generated;
        ACTIVE.set(new Frame(level,chunk,publication));
        try{generated=original.get();}finally{if(previous==null)ACTIVE.remove();else ACTIVE.set(previous);}
        return publication.finish(generated,value->filter(level,value,runtime),nativeLane);
    }
    public static boolean capture(ServerLevel level,ChunkAccess chunk,Runnable publish) {
        Frame frame=ACTIVE.get();if(frame==null || frame.level!=level || frame.chunk!=chunk)return false;
        frame.publication.capture(publish);return true;
    }
    private record Removal(Structure structure,StructureStart start,CompletableFuture<Boolean> decision) { }
    private static CompletableFuture<Runnable> filter(ServerLevel level,ChunkAccess chunk,DistributionRuntime runtime) {
        State policy=runtime.surfacePolicy();var registry=level.registryAccess().lookupOrThrow(Registries.STRUCTURE);
        List<Removal> removals=new ArrayList<>();
        for(var entry:chunk.getAllStarts().entrySet()) {
            StructureStart start=entry.getValue();if(!start.isValid())continue;
            String id=registry.getKey(entry.getKey()).toString();if(!policy.eligible(id))continue;
            List<Box> pieces=start.getPieces().stream().map(p->{var b=p.getBoundingBox();return new Box(b.minX(),b.minY(),b.minZ(),b.maxX(),b.maxY(),b.maxZ());}).toList();
            var pos=start.getChunkPos();
            if(runtime.surfaceBootstrap(pos.x(),pos.z(),pieces))continue;
            if(!selected(level.getSeed(),level.dimension().identifier().toString(),id,pos.x(),pos.z()))continue;
            removals.add(new Removal(entry.getKey(),start,runtime.surfaceCollision(pieces)));
        }
        return CompletableFuture.allOf(removals.stream().map(Removal::decision).toArray(CompletableFuture[]::new)).thenApply(ignored->()->{
            for(Removal r:removals)if(r.decision.getNow(false)) {
                if(chunk.getStartForStructure(r.structure)!=r.start)throw new IllegalStateException("Foreign structure changed during filtered publication");
                chunk.setStartForStructure(r.structure,StructureStart.INVALID_START);runtime.surfaceSuppressed.increment();
            }
        });
    }
}
