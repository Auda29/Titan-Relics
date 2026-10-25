package de.relics.mixin;

import com.mojang.datafixers.util.Pair;
import de.relics.distribution.DistributionRuntime;
import net.minecraft.core.*;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.structure.Structure;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Vanilla structure-map searches must never fall back to independent nominal relic sets. */
@Mixin(ChunkGenerator.class)
public abstract class DistributionMapLocateMixin {
    @Inject(method="findNearestMapStructure",at=@At("HEAD"),cancellable=true)
    private void relics$mapTarget(ServerLevel level,HolderSet<Structure> requested,BlockPos origin,int radius,boolean skipKnown,
            CallbackInfoReturnable<Pair<BlockPos,Holder<Structure>>> ci) {
        var runtime=DistributionRuntime.get(level);if(runtime==null)return;
        if(requested.stream().noneMatch(h->h.unwrapKey().map(k->k.identifier().getNamespace().equals("relics")).orElse(false)))return;
        // No independent random-spread scan and no chunk generation. Persistent
        // expedition maps retain their explicit pending state through MAP_ORIGIN.
        ci.setReturnValue(runtime.mapTarget(requested));
    }
}
