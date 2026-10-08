package de.relics.gameplay;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.CraftingInput;
import net.minecraft.world.item.crafting.CustomRecipe;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.level.Level;

/** CraftingInput trims blank borders. Core's all-empty bottom row is normalized away. */
public final class MaintenanceRecipe extends CustomRecipe {
    public static final RecipeSerializer<MaintenanceRecipe> CORE = serializer(true);
    public static final RecipeSerializer<MaintenanceRecipe> MAGNET = serializer(false);
    private final boolean core;
    public MaintenanceRecipe(boolean core) { this.core = core; }
    private static RecipeSerializer<MaintenanceRecipe> serializer(boolean core) {
        return new RecipeSerializer<>(MapCodec.unit(() -> new MaintenanceRecipe(core)),
                StreamCodec.unit(new MaintenanceRecipe(core)));
    }
    public static void initialize() {
        Registry.register(BuiltInRegistries.RECIPE_SERIALIZER, RelicItems.id("machine_core_recharge"), CORE);
        Registry.register(BuiltInRegistries.RECIPE_SERIALIZER, RelicItems.id("salvage_magnet_repair"), MAGNET);
    }
    @Override public boolean matches(CraftingInput input, Level level) {
        if (input.width() != 3 || input.height() != (core ? 2 : 3)) return false;
        if (!input.getItem(0, 0).isEmpty() || !input.getItem(2, 0).isEmpty() || !input.getItem(1, 0).is(Items.AMETHYST_SHARD)) return false;
        ItemStack relic = input.getItem(1, 1);
        if (!(core ? RelicItems.core(relic) : RelicItems.magnet(relic))) return false;
        if (relic.getCount() != 1 || !relic.has(core ? RelicItems.CORE_CHARGE : RelicItems.MAGNET_WEAR)) return false;
        int remaining = RelicItems.remaining(relic, core);
        if (core ? remaining != 0 : remaining >= RelicItems.MAGNET_CAPACITY) return false;
        var metal = core ? Items.COAL_BLOCK : Items.IRON_INGOT;
        if (!input.getItem(0, 1).is(metal) || !input.getItem(2, 1).is(metal)) return false;
        return core || input.getItem(0, 2).is(metal) && input.getItem(2, 2).is(metal) && input.getItem(1, 2).isEmpty();
    }
    @Override public ItemStack assemble(CraftingInput input) {
        if (!matches(input, null)) return ItemStack.EMPTY;
        ItemStack result = input.getItem(1, 1).copyWithCount(1);
        RelicItems.setRemaining(result, core, core ? RelicItems.CORE_CAPACITY : RelicItems.MAGNET_CAPACITY);
        return result;
    }
    @Override public RecipeSerializer<? extends CustomRecipe> getSerializer() { return core ? CORE : MAGNET; }
}
