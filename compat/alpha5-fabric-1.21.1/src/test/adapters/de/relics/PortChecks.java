package de.relics;

import de.relics.gameplay.*;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.minecraft.commands.Commands;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.*;
import net.minecraft.world.item.crafting.*;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.AbstractFurnaceBlockEntity;
import net.minecraft.server.level.ServerLevel;
import java.nio.file.*;
import java.util.*;

/** Additional checks execute on the actual production mod under its loader. */
public final class PortChecks implements ModInitializer {
    private static int checks;
    private static void check(boolean value,String message){checks++;if(!value)throw new AssertionError(message);}
    private static CraftingInput input(boolean core,ItemStack relic) {
        var metal=core?Items.COAL_BLOCK:Items.IRON_INGOT;
        var slots=new ArrayList<>(List.of(ItemStack.EMPTY,new ItemStack(Items.AMETHYST_SHARD),ItemStack.EMPTY,
                new ItemStack(metal),relic,new ItemStack(metal)));
        if(!core)slots.addAll(List.of(new ItemStack(metal),ItemStack.EMPTY,new ItemStack(metal)));
        return CraftingInput.of(3,core?2:3,slots);
    }
    private static void run(ServerLevel level) throws Exception {
        checks=0;
        RecipeNetworkChecks.run(level);
        for(boolean core:new boolean[]{true,false}) {
            var id=RelicItems.id(core?"machine_core_recharge":"salvage_magnet_repair");
            var holder=level.getRecipeManager().byKey(id).orElseThrow();
            check(holder.value() instanceof MaintenanceRecipe,"Missing native maintenance serializer");
            var recipe=(MaintenanceRecipe)holder.value();
            check(recipe.getIngredients().size()==(core?6:9),"Recipe book lacks native shaped ingredients");
            var relic=new ItemStack(core?RelicItems.MACHINE_CORE:RelicItems.SALVAGE_MAGNET);
            check(!recipe.matches(input(core,relic),level),"Full relic must not be maintained");
            RelicItems.setRemaining(relic,core,0);relic.set(DataComponents.CUSTOM_NAME,Component.literal("Preserve my relic"));
            var ingredients=input(core,relic);check(recipe.matches(ingredients,level),"Depleted relic maintenance rejected");
            var result=recipe.assemble(ingredients,level.registryAccess());
            check(RelicItems.remaining(result,core)==(core?256:1000),"Incorrect maintained capacity");
            check(result.get(DataComponents.CUSTOM_NAME).equals(relic.get(DataComponents.CUSTOM_NAME)),"Maintenance lost components");
            check(RelicItems.remaining(relic,core)==0,"Crafting mutated original input");
            if(core){RelicItems.setRemaining(relic,true,1);check(!recipe.matches(input(true,relic),level),"Partially active core recharged");}
        }
        check(level.registryAccess().registryOrThrow(Registries.TRIM_PATTERN).containsKey(RelicItems.id("monolith")),"Missing Monolith trim pattern");
        var smithingInput=new SmithingRecipeInput(new ItemStack(RelicItems.MONOLITH_TEMPLATE),new ItemStack(Items.NETHERITE_CHESTPLATE),new ItemStack(Items.AMETHYST_SHARD));
        var smithing=level.getRecipeManager().getRecipeFor(RecipeType.SMITHING,smithingInput,level).orElseThrow();
        var trimmed=smithing.value().assemble(smithingInput,level.registryAccess());
        check(trimmed.is(Items.NETHERITE_CHESTPLATE) && trimmed.has(DataComponents.TRIM),"Native smithing did not apply the trim");
        check(trimmed.get(DataComponents.TRIM).pattern().unwrapKey().orElseThrow().location().equals(RelicItems.id("monolith")),"Applied a different trim pattern");
        var pos=new BlockPos(16,120,16);
        boolean restarted=Files.exists(Path.of("port-core-proof.txt"));
        if(restarted) {
            check(level.getBlockEntity(pos) instanceof AbstractFurnaceBlockEntity,"Furnace lost after restart");
            var saved=(AbstractFurnaceBlockEntity)level.getBlockEntity(pos);
            check(saved.getItem(2).is(Items.IRON_INGOT) && saved.getItem(2).getCount()==2,"Processed output lost after restart");
            check(RelicItems.remaining(saved.getItem(1),true)==0,"Core charge changed after restart");
        }
        level.setBlock(pos,Blocks.BLAST_FURNACE.defaultBlockState(),3);
        var furnace=(AbstractFurnaceBlockEntity)level.getBlockEntity(pos);
        furnace.clearContent();furnace.setItem(0,new ItemStack(Items.RAW_IRON,5));
        var core=new ItemStack(RelicItems.MACHINE_CORE);RelicItems.setRemaining(core,true,2);furnace.setItem(1,core);
        check(furnace.canPlaceItem(1,core),"Core fuel insertion rejected");
        for(int i=0;i<1000;i++)AbstractFurnaceBlockEntity.serverTick(level,pos,level.getBlockState(pos),furnace);
        check(furnace.getItem(2).is(Items.IRON_INGOT) && furnace.getItem(2).getCount()==2,"Core did not limit processing to two operations");
        check(furnace.getItem(0).getCount()==3 && RelicItems.remaining(core,true)==0,"Core processing changed input or budget incorrectly");
        check(!furnace.canPlaceItem(1,core),"Depleted core accepted as active fuel");
        check(!level.getBlockState(pos).getValue(net.minecraft.world.level.block.AbstractFurnaceBlock.LIT),"Depleted core furnace remains lit");
        var probe=new net.minecraft.server.level.ServerPlayer(level.getServer(),level,
                new com.mojang.authlib.GameProfile(UUID.randomUUID(),"CoreMenuProbe"),net.minecraft.server.level.ClientInformation.createDefault());
        var data=new net.minecraft.world.inventory.SimpleContainerData(4);data.set(2,1);
        RelicItems.setRemaining(core,true,1);
        var menu=new net.minecraft.world.inventory.BlastFurnaceMenu(1,probe.getInventory(),furnace,data);
        check(menu.getSlot(1).mayPlace(core) && menu.isLit() && menu.getLitProgress()==1.0F,"Core menu fuel and flame state missing");
        RelicItems.setRemaining(core,true,0);
        check(!menu.getSlot(1).mayPlace(core) && !menu.isLit(),"Depleted core remains active in furnace menu");
        check(de.relics.distribution.DistributionRuntime.get(level)!=null,"Fresh world did not initialize distribution");
        Files.writeString(Path.of("port-core-proof.txt"),"checks="+checks+"\nrestart="+restarted+"\ncore_operations=2\nrecipe_book=shaped\n");
        System.out.println("PORT_PASS core and recipes: "+checks+" checks; restart="+restarted);
    }
    @Override public void onInitialize() {
        CommandRegistrationCallback.EVENT.register((d,r,e)->d.register(Commands.literal("relicsporttest").executes(c->{
            try{run(c.getSource().getLevel());}catch(Throwable error){error.printStackTrace();System.out.println("PORT_FAIL "+error);}
            return 1;
        })));
    }
}
