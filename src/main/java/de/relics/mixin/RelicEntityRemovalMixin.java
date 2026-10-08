package de.relics.mixin;

import de.relics.gameplay.RelicGameplay;
import net.minecraft.world.entity.Entity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(Entity.class)
public abstract class RelicEntityRemovalMixin {
    @Inject(method = "remove", at = @At("HEAD"))
    private void relics$remove(Entity.RemovalReason reason, CallbackInfo ci) {
        RelicGameplay.entityRemoved((Entity)(Object)this, reason);
    }
}
