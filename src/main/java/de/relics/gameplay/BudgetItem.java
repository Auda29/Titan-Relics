package de.relics.gameplay;

import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.TooltipDisplay;
import java.util.function.Consumer;

public final class BudgetItem extends Item {
    private final boolean core;
    public BudgetItem(Properties properties, boolean core) { super(properties); this.core = core; }
    @Override public boolean isBarVisible(ItemStack stack) { return false; }
    @Override public void inventoryTick(ItemStack stack, ServerLevel level, Entity entity, EquipmentSlot slot) {
        RelicItems.updateIcon(stack, core);
    }
    @Override public void appendHoverText(ItemStack stack, TooltipContext context, TooltipDisplay display,
                                          Consumer<Component> tooltip, TooltipFlag flag) {
        int remaining = RelicItems.remaining(stack, core);
        tooltip.accept(Component.translatable(core ? "tooltip.relics.core_charge" : "tooltip.relics.magnet_wear",
                remaining, core ? RelicItems.CORE_CAPACITY : RelicItems.MAGNET_CAPACITY));
        if (remaining == 0) tooltip.accept(Component.translatable(core ? "tooltip.relics.core_empty" : "tooltip.relics.magnet_broken"));
        if (!core) tooltip.accept(Component.translatable("tooltip.relics.magnet_offhand"));
    }
}
