package de.relics.mixin;

import de.relics.gameplay.RewardDrops;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.*;

@Mixin(ItemEntity.class)
public abstract class RewardDropMixin {
    @Inject(method="playerTouch",at=@At("HEAD"),cancellable=true)
    private void relics$personal(Player player,CallbackInfo ci) {
        if(!RewardDrops.allowPickup((ItemEntity)(Object)this,player))ci.cancel();
    }
    @Inject(method="isMergable",at=@At("HEAD"),cancellable=true)
    private void relics$separate(CallbackInfoReturnable<Boolean> cir) {
        if(RewardDrops.isReward((ItemEntity)(Object)this))cir.setReturnValue(false);
    }
}
