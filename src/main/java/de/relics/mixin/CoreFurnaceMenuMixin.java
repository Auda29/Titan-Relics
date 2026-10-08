package de.relics.mixin;

import de.relics.gameplay.RelicItems;
import net.minecraft.world.inventory.AbstractFurnaceMenu;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.Container;
import net.minecraft.world.inventory.ContainerData;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(AbstractFurnaceMenu.class)
public abstract class CoreFurnaceMenuMixin {
    @Shadow @Final private Container container;
    @Shadow @Final private ContainerData data;
    @Unique private boolean relics$coreWorking() {
        ItemStack core = container.getItem(1);
        return data.get(0) == 0 && data.get(2) > 0 && RelicItems.core(core) && RelicItems.remaining(core, true) > 0;
    }
    @Inject(method = "isFuel", at = @At("HEAD"), cancellable = true)
    private void relics$fuel(ItemStack stack, CallbackInfoReturnable<Boolean> cir) {
        if (RelicItems.core(stack)) cir.setReturnValue(stack.getCount() == 1 && RelicItems.remaining(stack, true) > 0);
    }
    @Inject(method = "isLit", at = @At("HEAD"), cancellable = true)
    private void relics$heat(CallbackInfoReturnable<Boolean> cir) { if (relics$coreWorking()) cir.setReturnValue(true); }
    @Inject(method = "getLitProgress", at = @At("HEAD"), cancellable = true)
    private void relics$flame(CallbackInfoReturnable<Float> cir) { if (relics$coreWorking()) cir.setReturnValue(1.0F); }
}
