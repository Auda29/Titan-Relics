package de.relics.mixin;

import de.relics.gameplay.RelicGameplay;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.MapItem;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(MapItem.class)
public abstract class ExpeditionMapMixin {
    @Inject(method = "inventoryTick", at = @At("HEAD"), cancellable = true)
    private void relics$update(ItemStack stack, ServerLevel level, Entity entity, EquipmentSlot slot, CallbackInfo ci) {
        if (RelicGameplay.updateMap(stack, level)) ci.cancel();
    }
}
