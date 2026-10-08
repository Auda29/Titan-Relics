package de.relics.mixin;

import de.relics.gameplay.CoreFurnace;
import net.minecraft.world.level.block.entity.BaseContainerBlockEntity;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(BaseContainerBlockEntity.class)
public abstract class CoreContainerMixin {
    @Inject(method = "removeItem", at = @At("RETURN"))
    private void relics$remove(int slot, int amount, CallbackInfoReturnable<ItemStack> cir) {
        if (slot == 1 && !cir.getReturnValue().isEmpty() && this instanceof CoreFurnace core) core.relics$resetCoreProgress();
    }
    @Inject(method = "removeItemNoUpdate", at = @At("RETURN"))
    private void relics$removeAll(int slot, CallbackInfoReturnable<ItemStack> cir) {
        if (slot == 1 && !cir.getReturnValue().isEmpty() && this instanceof CoreFurnace core) core.relics$resetCoreProgress();
    }
    @Inject(method = "clearContent", at = @At("HEAD"))
    private void relics$clear(CallbackInfo ci) { if (this instanceof CoreFurnace core) core.relics$resetCoreProgress(); }
}
