package de.relics.gameplay;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.world.item.*;
import net.minecraft.world.item.crafting.*;
import net.minecraft.world.level.Level;
import java.util.Map;

/** Native 1.21.1 shaped recipe supplies its pattern/result to the recipe book. */
public final class MaintenanceRecipe extends ShapedRecipe {
    public static final RecipeSerializer<MaintenanceRecipe> CORE=serializer(true),MAGNET=serializer(false);
    private final boolean core;
    public MaintenanceRecipe(boolean core) {
        super("relics",CraftingBookCategory.MISC,pattern(core),new ItemStack(core?RelicItems.MACHINE_CORE:RelicItems.SALVAGE_MAGNET),true);
        this.core=core;
    }
    private static ShapedRecipePattern pattern(boolean core) {
        return ShapedRecipePattern.of(Map.of('A',Ingredient.of(Items.AMETHYST_SHARD),
                'M',Ingredient.of(core?Items.COAL_BLOCK:Items.IRON_INGOT),
                'R',Ingredient.of(core?RelicItems.MACHINE_CORE:RelicItems.SALVAGE_MAGNET)),
                core?new String[]{" A ","MRM"}:new String[]{" A ","MRM","M M"});
    }
    private static RecipeSerializer<MaintenanceRecipe> serializer(boolean core) {
        return new RecipeSerializer<>() {
            public MapCodec<MaintenanceRecipe> codec(){return MapCodec.unit(()->new MaintenanceRecipe(core));}
            public StreamCodec<RegistryFriendlyByteBuf,MaintenanceRecipe> streamCodec(){
                // The serializer ID selects the variant; recipe instances are not singletons.
                return StreamCodec.<RegistryFriendlyByteBuf,Boolean>unit(core)
                        .map(MaintenanceRecipe::new,recipe->recipe.core);
            }
        };
    }
    public static void initialize() {
        Registry.register(BuiltInRegistries.RECIPE_SERIALIZER,RelicItems.id("machine_core_recharge"),CORE);
        Registry.register(BuiltInRegistries.RECIPE_SERIALIZER,RelicItems.id("salvage_magnet_repair"),MAGNET);
    }
    @Override public boolean matches(CraftingInput input,Level level) {
        if(input.width()!=3 || input.height()!=(core?2:3))return false;
        if(!input.getItem(0,0).isEmpty() || !input.getItem(2,0).isEmpty() || !input.getItem(1,0).is(Items.AMETHYST_SHARD))return false;
        ItemStack relic=input.getItem(1,1);
        if(!(core?RelicItems.core(relic):RelicItems.magnet(relic)) || relic.getCount()!=1
                || !relic.has(core?RelicItems.CORE_CHARGE:RelicItems.MAGNET_WEAR))return false;
        int remaining=RelicItems.remaining(relic,core);
        if(core?remaining!=0:remaining>=RelicItems.MAGNET_CAPACITY)return false;
        var metal=core?Items.COAL_BLOCK:Items.IRON_INGOT;
        if(!input.getItem(0,1).is(metal) || !input.getItem(2,1).is(metal))return false;
        return core || input.getItem(0,2).is(metal) && input.getItem(2,2).is(metal) && input.getItem(1,2).isEmpty();
    }
    @Override public ItemStack assemble(CraftingInput input,HolderLookup.Provider registries) {
        if(!matches(input,null))return ItemStack.EMPTY;
        ItemStack result=input.getItem(1,1).copyWithCount(1);
        RelicItems.setRemaining(result,core,core?RelicItems.CORE_CAPACITY:RelicItems.MAGNET_CAPACITY);
        return result;
    }
    @Override public RecipeSerializer<?> getSerializer(){return core?CORE:MAGNET;}
}
