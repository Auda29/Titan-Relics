package de.relics.mixin;

import com.llamalad7.mixinextras.injector.wrapmethod.WrapMethod;
import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import de.relics.distribution.DistributionRuntime;
import net.minecraft.server.level.GenerationChunkHolder;
import net.minecraft.util.StaticCache2D;
import net.minecraft.world.level.chunk.ChunkAccess;
import net.minecraft.world.level.chunk.status.*;
import org.spongepowered.asm.mixin.Mixin;
import java.util.concurrent.CompletableFuture;

@Mixin(ChunkStatusTasks.class)
public abstract class DistributionStartsMixin {
    @WrapMethod(method="generateStructureStarts")
    private static CompletableFuture<ChunkAccess> relics$plannedStarts(WorldGenContext context,ChunkStep step,
            StaticCache2D<GenerationChunkHolder> chunks,ChunkAccess chunk,Operation<CompletableFuture<ChunkAccess>> original) {
        var center=chunks.get(chunk.getPos().x(),chunk.getPos().z());
        var dispatcher=((DistributionChunkMapAccessor)context.level().getChunkSource().chunkMap).relics$worldgenDispatcher();
        java.util.concurrent.Executor worldgenExecutor=task->dispatcher.submit(task,
                net.minecraft.world.level.ChunkPos.pack(chunk.getPos().x(),chunk.getPos().z()),center::getQueueLevel);
        return DistributionRuntime.beforeStarts(context.level(),chunk,()->original.call(context,step,chunks,chunk),worldgenExecutor);
    }
}
