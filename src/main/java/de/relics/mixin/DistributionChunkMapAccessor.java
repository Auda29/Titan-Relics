package de.relics.mixin;

import net.minecraft.server.level.ChunkMap;
import net.minecraft.server.level.ChunkTaskDispatcher;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;

@Mixin(ChunkMap.class)
public interface DistributionChunkMapAccessor {
    @Accessor("worldgenTaskDispatcher")
    ChunkTaskDispatcher relics$worldgenDispatcher();
}
