package de.relics.gameplay;

import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.SmithingTemplateItem;

public final class RelicItems {
    public static final int CORE_CAPACITY = 256;
    public static final int MAGNET_CAPACITY = 1000;
    public static final DataComponentType<String> MAP_ORIGIN = Registry.register(BuiltInRegistries.DATA_COMPONENT_TYPE,
            id("map_origin"), DataComponentType.<String>builder().persistent(com.mojang.serialization.Codec.STRING)
                    .networkSynchronized(ByteBufCodecs.STRING_UTF8).build());
    public static final DataComponentType<ItemBudget> CORE_CHARGE = budget("core_charge", CORE_CAPACITY);
    public static final DataComponentType<ItemBudget> MAGNET_WEAR = budget("magnet_wear", MAGNET_CAPACITY);
    public static final Item MACHINE_CORE = register("machine_core", new BudgetItem(properties("machine_core")
            .stacksTo(1).component(CORE_CHARGE, new ItemBudget(1, CORE_CAPACITY)), true));
    public static final Item SALVAGE_MAGNET = register("salvage_magnet", new BudgetItem(properties("salvage_magnet")
            .stacksTo(1).component(MAGNET_WEAR, new ItemBudget(1, MAGNET_CAPACITY)), false));
    public static final Item COLOSSUS_KEY = register("colossus_key", new Item(properties("colossus_key")));
    public static final Item MONOLITH_TEMPLATE = register("monolith_armor_trim_smithing_template",
            SmithingTemplateItem.createArmorTrimTemplate(properties("monolith_armor_trim_smithing_template")));

    private RelicItems() { }
    public static Identifier id(String path) { return Identifier.fromNamespaceAndPath("relics", path); }
    private static Item.Properties properties(String name) {
        return new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id(name))).rarity(Rarity.RARE);
    }
    private static Item register(String name, Item item) { return Registry.register(BuiltInRegistries.ITEM, id(name), item); }
    private static DataComponentType<ItemBudget> budget(String name, int capacity) {
        var codec = ItemBudget.codec(capacity);
        return Registry.register(BuiltInRegistries.DATA_COMPONENT_TYPE, id(name),
                DataComponentType.<ItemBudget>builder().persistent(codec).networkSynchronized(ByteBufCodecs.fromCodec(codec)).build());
    }
    public static boolean core(ItemStack stack) { return stack.is(MACHINE_CORE); }
    public static boolean magnet(ItemStack stack) { return stack.is(SALVAGE_MAGNET); }
    public static int remaining(ItemStack stack, boolean core) {
        var value = stack.get(core ? CORE_CHARGE : MAGNET_WEAR);
        return value == null ? 0 : Math.min(value.remaining(), core ? CORE_CAPACITY : MAGNET_CAPACITY);
    }
    public static void setRemaining(ItemStack stack, boolean core, int remaining) {
        int capacity = core ? CORE_CAPACITY : MAGNET_CAPACITY;
        if (remaining < 0 || remaining > capacity) throw new IllegalArgumentException("Out-of-range relic charge");
        stack.set(core ? CORE_CHARGE : MAGNET_WEAR, new ItemBudget(1, remaining));
        updateIcon(stack, core);
    }
    public static void updateIcon(ItemStack stack, boolean core) {
        int left = remaining(stack, core), capacity = core ? CORE_CAPACITY : MAGNET_CAPACITY;
        String suffix = left == capacity ? "" : left == 0 ? "_empty" : "_partial";
        var model = id((core ? "machine_core" : "salvage_magnet") + suffix);
        if (!model.equals(stack.get(DataComponents.ITEM_MODEL))) stack.set(DataComponents.ITEM_MODEL, model);
    }
    public static void initialize() {
        MaintenanceRecipe.initialize();
        CreativeModeTabEvents.modifyOutputEvent(ResourceKey.create(Registries.CREATIVE_MODE_TAB,
                Identifier.fromNamespaceAndPath("minecraft", "tools_and_utilities"))).register(entries -> {
            entries.accept(MACHINE_CORE); entries.accept(SALVAGE_MAGNET); entries.accept(COLOSSUS_KEY);
        });
        CreativeModeTabEvents.modifyOutputEvent(ResourceKey.create(Registries.CREATIVE_MODE_TAB,
                Identifier.fromNamespaceAndPath("minecraft", "ingredients"))).register(entries -> entries.accept(MONOLITH_TEMPLATE));
    }
}
