package de.relics.mixin;

import de.relics.gameplay.RewardDrops;
import net.minecraft.world.Container;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.level.block.entity.HopperBlockEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(HopperBlockEntity.class)
public abstract class RewardHopperMixin {
    @Inject(method="addItem(Lnet/minecraft/world/Container;Lnet/minecraft/world/entity/item/ItemEntity;)Z",at=@At("HEAD"),cancellable=true)
    private static void relics$personal(Container container,ItemEntity item,CallbackInfoReturnable<Boolean> cir) {
        if(RewardDrops.isReward(item))cir.setReturnValue(false);
    }
}
