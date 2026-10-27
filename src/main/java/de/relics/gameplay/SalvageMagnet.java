package de.relics.gameplay;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.HitResult;
import java.util.HashMap;
import java.util.Map;

/** Spatial queries around a magnet held in either hand; ordinary inventory slots stay inactive. */
public final class SalvageMagnet {
    public static final double ACCELERATION=0.08*1.10, MAX_SPEED=0.35*1.10;
    private SalvageMagnet() { }
    public static ItemStack heldMagnet(Player player) {
        var main=player.getMainHandItem();
        if(RelicItems.magnet(main) && RelicItems.remaining(main,false)>0)return main;
        var off=player.getOffhandItem();
        return RelicItems.magnet(off) && RelicItems.remaining(off,false)>0?off:ItemStack.EMPTY;
    }
    public static boolean eligible(ItemEntity item, ServerPlayer player) {
        if (item.isRemoved() || item.hasPickUpDelay() || !player.isAlive() || player.isCreative() || player.isSpectator()
                || item.level() != player.level() || item.distanceToSqr(player) > 64) return false;
        ItemStack magnet = heldMagnet(player);
        if (!RelicItems.magnet(magnet) || RelicItems.remaining(magnet, false) == 0 || item.getItem().isEmpty()) return false;
        var target = ((de.relics.mixin.ItemPickupOwnerAccessor)item).relics$pickupOwner();
        if (target != null && !target.equals(player.getUUID())) return false;
        if (!hasSpace(player, item.getItem())) return false;
        return player.level().clip(new ClipContext(item.getBoundingBox().getCenter(), player.position().add(0, 0.5, 0),
                ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, item)).getType() == HitResult.Type.MISS;
    }
    private static boolean hasSpace(Player player, ItemStack incoming) {
        for (ItemStack slot : player.getInventory().getNonEquipmentItems())
            if (slot.isEmpty() || ItemStack.isSameItemSameComponents(slot, incoming) && slot.getCount() < slot.getMaxStackSize()) return true;
        return false;
    }
    public static void scan(ServerLevel level) {
        if (level.getGameTime() % 4 != 0) return;
        Map<ItemEntity, ServerPlayer> nearest = new HashMap<>();
        for (ServerPlayer player : level.players()) {
            ItemStack magnet = heldMagnet(player);
            if (!RelicItems.magnet(magnet) || RelicItems.remaining(magnet, false) == 0 || !player.isAlive() || player.isCreative() || player.isSpectator()) continue;
            for (ItemEntity item : level.getEntitiesOfClass(ItemEntity.class, player.getBoundingBox().inflate(8))) {
                if (!eligible(item, player)) continue;
                ServerPlayer existing = nearest.get(item);
                if (existing == null || nearer(item.distanceToSqr(player), player.getUUID(), item.distanceToSqr(existing), existing.getUUID()))
                    nearest.put(item, player);
            }
        }
        nearest.forEach((item, player) -> ((MagnetAttraction)item).relics$select(player));
    }
    public static boolean nearer(double distance, java.util.UUID player, double otherDistance, java.util.UUID other) {
        return distance < otherDistance || distance == otherDistance && player.compareTo(other) < 0;
    }
}
