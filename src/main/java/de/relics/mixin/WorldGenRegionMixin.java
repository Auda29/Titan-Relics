package de.relics.mixin;

import de.relics.RelicProtection;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.WorldGenRegion;
import net.minecraft.world.level.block.state.BlockState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(WorldGenRegion.class)
public abstract class WorldGenRegionMixin {
    @Inject(method = "setBlock", at = @At("HEAD"), cancellable = true)
    private void relics$preservePlacedCells(BlockPos pos, BlockState state, int flags, int recursion,
            CallbackInfoReturnable<Boolean> callback) {
        var region = (WorldGenRegion) (Object) this;
        if (RelicProtection.protectedAt(region, pos)) {
            // Do not prevent a leaf-distance/other same-block state update.
            if (region.getBlockState(pos).getBlock() != state.getBlock()) {
                callback.setReturnValue(false);
            }
        }
    }
}
