package de.relics.mixin;

import de.relics.distribution.DistributionRuntime;
import net.minecraft.world.level.chunk.ChunkGeneratorStructureState;
import net.minecraft.world.level.levelgen.structure.placement.StructurePlacement;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(StructurePlacement.class)
public abstract class DistributionPlacementMixin {
    @Inject(method="isStructureChunk",at=@At("HEAD"),cancellable=true)
    private void relics$sharedPlacement(ChunkGeneratorStructureState state,int x,int z,CallbackInfoReturnable<Boolean> ci) {
        Boolean result=DistributionRuntime.placement(this,state,x,z);
        if(result!=null)ci.setReturnValue(result);
    }
}
