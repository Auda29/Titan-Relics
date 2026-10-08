package de.relics.mixin;

import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import com.llamalad7.mixinextras.injector.wrapoperation.WrapOperation;
import de.relics.gameplay.RelicItems;
import de.relics.gameplay.SalvageMagnet;
import de.relics.gameplay.MagnetAttraction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.Vec3;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import java.util.UUID;

@Mixin(ItemEntity.class)
public abstract class SalvageMagnetMixin implements MagnetAttraction {
    @Unique private UUID relics$collector;
    @Unique private ItemStack relics$magnet;
    @Unique private long relics$lastPull = -1000;
    @Unique private long relics$lastScan;

    @Override public void relics$select(ServerPlayer player) {
        if (!player.getUUID().equals(relics$collector) || player.getOffhandItem() != relics$magnet) relics$lastPull = -1000;
        relics$collector = player.getUUID(); relics$magnet = player.getOffhandItem();
        relics$lastScan = player.level().getGameTime();
    }
    @Inject(method = "tick", at = @At("TAIL"))
    private void relics$pull(CallbackInfo ci) {
        ItemEntity item = (ItemEntity)(Object) this;
        if (!(item.level() instanceof ServerLevel level) || item.isRemoved()) return;
        if (relics$collector == null) return;
        ServerPlayer player = level.getServer().getPlayerList().getPlayer(relics$collector);
        if (player == null || level.getGameTime() - relics$lastScan > 4 || player.getOffhandItem() != relics$magnet || !SalvageMagnet.eligible(item, player)) {
            relics$collector = null; relics$magnet = null; return;
        }
        Vec3 direction = player.position().add(0, 0.5, 0).subtract(item.position()).normalize();
        Vec3 motion = item.getDeltaMovement().add(direction.scale(0.08));
        if (motion.lengthSqr() > 0.35 * 0.35) motion = motion.normalize().scale(0.35);
        item.setDeltaMovement(motion);
        item.hurtMarked = true;
        relics$lastPull = level.getGameTime();
    }
    @WrapOperation(method = "playerTouch", at = @At(value = "INVOKE", target = "Lnet/minecraft/world/entity/player/Inventory;add(Lnet/minecraft/world/item/ItemStack;)Z"))
    private boolean relics$chargePickup(Inventory inventory, ItemStack incoming, Operation<Boolean> original, Player player) {
        int before = incoming.getCount();
        boolean result = original.call(inventory, incoming);
        ItemEntity item = (ItemEntity)(Object) this;
        if (incoming.getCount() < before && player.getUUID().equals(relics$collector) && player.getOffhandItem() == relics$magnet
                && item.level().getGameTime() - relics$lastPull <= 4 && RelicItems.remaining(relics$magnet, false) > 0) {
            RelicItems.setRemaining(relics$magnet, false, RelicItems.remaining(relics$magnet, false) - 1);
        }
        if (incoming.getCount() < before) { relics$collector = null; relics$magnet = null; }
        return result;
    }
}
