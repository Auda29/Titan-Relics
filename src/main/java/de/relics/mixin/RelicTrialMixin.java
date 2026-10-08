package de.relics.mixin;

import de.relics.gameplay.RelicGameplay;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.entity.trialspawner.TrialSpawner;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(TrialSpawner.class)
public abstract class RelicTrialMixin {
    @Inject(method = "tickServer", at = @At("HEAD"), cancellable = true)
    private void relics$trial(ServerLevel level, BlockPos pos, boolean ominous, CallbackInfo ci) {
        if (RelicGameplay.tickTrial(level, pos, (TrialSpawner)(Object)this)) ci.cancel();
    }
}
