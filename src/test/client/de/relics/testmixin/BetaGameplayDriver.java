package de.relics.clientqa;

import de.relics.gameplay.*;
import net.minecraft.client.Minecraft;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.inventory.ContainerInput;
import net.minecraft.world.item.*;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.*;
import java.nio.file.*;

/** Isolated QA driver. Ingredients are fixtures; output is taken through normal client clicks. */
public final class BetaGameplayDriver {
    private static int step, recipe, wait, retries;
    private static final BlockPos TABLE=new BlockPos(0,120,0);
    private static void log(String text) throws Exception {
        Files.writeString(Path.of("gameplay-actions.log"),System.currentTimeMillis()+" "+text+"\n",StandardOpenOption.CREATE,StandardOpenOption.APPEND);
    }
    private static void require(boolean test,String text){if(!test)throw new AssertionError(text);}
    private static ItemStack[] inputs(){
        ItemStack[] a=new ItemStack[9];java.util.Arrays.fill(a,ItemStack.EMPTY);
        if(recipe==0){for(int i=0;i<9;i++)a[i]=new ItemStack(Items.DIAMOND);a[1]=new ItemStack(RelicItems.MONOLITH_TEMPLATE);a[4]=new ItemStack(net.minecraft.core.registries.BuiltInRegistries.ITEM.getValue(net.minecraft.resources.Identifier.parse("minecraft:copper_block")));}
        if(recipe==1 || recipe==2){boolean core=recipe==1;a[1]=new ItemStack(Items.AMETHYST_SHARD);a[3]=new ItemStack(core?Items.COAL_BLOCK:Items.IRON_INGOT);a[5]=a[3].copy();a[4]=new ItemStack(core?RelicItems.MACHINE_CORE:RelicItems.SALVAGE_MAGNET);RelicItems.setRemaining(a[4],core,0);if(!core){a[6]=a[3].copy();a[8]=a[3].copy();}}
        if(recipe==3){a[0]=new ItemStack(RelicItems.MONOLITH_TEMPLATE);a[1]=new ItemStack(Items.DIAMOND_CHESTPLATE);a[2]=new ItemStack(Items.AMETHYST_SHARD);}
        return a;
    }
    public static void tick(Minecraft c) throws Exception {
        if(wait++%2!=0)return;
        var server=c.getSingleplayerServer();
        if(step==0){
            server.submit(()->{var p=server.getPlayerList().getPlayer(c.player.getUUID());var w=server.overworld();for(int x=-1;x<=1;x++)for(int z=-1;z<=1;z++)w.getChunk(x,z);
                for(int x=-4;x<=4;x++)for(int z=-4;z<=4;z++){w.setBlock(new BlockPos(x,119,z),Blocks.STONE.defaultBlockState(),3);for(int y=120;y<125;y++)w.setBlock(new BlockPos(x,y,z),Blocks.AIR.defaultBlockState(),3);}
                w.setBlock(TABLE,(recipe==3?Blocks.SMITHING_TABLE:Blocks.CRAFTING_TABLE).defaultBlockState(),3);
                server.getCommands().performPrefixedCommand(server.createCommandSourceStack(),"tp @a 0.5 120 -2.5");
                if(recipe==0)p.getInventory().clearContent();else for(int i=0;i<9;i++){var kept=p.getInventory().getItem(i);if(!kept.isEmpty()){p.getInventory().setItem(17+recipe,kept);p.getInventory().setItem(i,ItemStack.EMPTY);}}var a=inputs();for(int i=0;i<9;i++)p.getInventory().setItem(i,a[i]);p.inventoryMenu.broadcastChanges();return true;}).get();
            log("operator ingredients recipe="+recipe+" "+java.util.Arrays.toString(inputs()));step=1;return;
        }
        if(step==1){if(!c.level.getBlockState(TABLE).is(recipe==3?Blocks.SMITHING_TABLE:Blocks.CRAFTING_TABLE)||c.player.distanceToSqr(Vec3.atCenterOf(TABLE))>25){require(retries++<60,"Arena synchronization timeout client="+c.level.getBlockState(TABLE)+" pos="+c.player.position()+" server="+server.submit(()->server.overworld().getBlockState(TABLE).toString()).get());return;}c.gameMode.useItemOn(c.player,InteractionHand.MAIN_HAND,new BlockHitResult(Vec3.atCenterOf(TABLE),Direction.NORTH,TABLE,false));step=2;return;}
        var menu=c.player.containerMenu;
        if(step==2){if(menu==c.player.inventoryMenu){require(retries++<60,"Block interaction did not open menu");step=1;return;}retries=0;log("GUI "+c.gui.screen().getClass().getName()+" slots="+menu.slots.size());step=3;return;}
        if(step>=3 && step<12){int i=step-3;var a=inputs();if(!a[i].isEmpty()){
            int source=menu.slots.size()-9+i;int target=recipe==3?i:i+1;
            c.gameMode.handleContainerInput(menu.containerId,source,0,ContainerInput.PICKUP,c.player);
            c.gameMode.handleContainerInput(menu.containerId,target,0,ContainerInput.PICKUP,c.player);
        }step++;return;}
        if(step==12){int result=recipe==3?3:0;var stack=menu.getSlot(result).getItem();require(!stack.isEmpty(),"No crafting result recipe="+recipe);log("result before take recipe="+recipe+" "+stack);
            if(recipe<3){Object screen=c.gui.screen();boolean found=false;for(Class<?> type=screen.getClass();type!=null;type=type.getSuperclass())for(var field:type.getDeclaredFields())if(net.minecraft.client.gui.screens.recipebook.RecipeBookComponent.class.isAssignableFrom(field.getType())){field.setAccessible(true);var book=(net.minecraft.client.gui.screens.recipebook.RecipeBookComponent)field.get(screen);if(!book.isVisible())book.toggleVisibility();require(book.isVisible(),"Recipe book did not open");found=true;}require(found,"No recipe book component");log("recipe book visible recipe="+recipe);}
            step++;return;}
        if(step==13){net.minecraft.client.Screenshot.grab(c,true);c.gameMode.handleContainerInput(menu.containerId,recipe==3?3:0,0,ContainerInput.QUICK_MOVE,c.player);step++;return;}
        if(step==14){
            String proof=server.submit(()->{var p=server.getPlayerList().getPlayer(c.player.getUUID());var m=p.containerMenu;for(int i=recipe==3?0:1;i<(recipe==3?3:10);i++)require(m.getSlot(i).getItem().isEmpty(),"Unconsumed ingredient slot="+i);
                Item expected=recipe==0?RelicItems.MONOLITH_TEMPLATE:recipe==1?RelicItems.MACHINE_CORE:recipe==2?RelicItems.SALVAGE_MAGNET:Items.DIAMOND_CHESTPLATE;
                int count=0;for(int i=0;i<36;i++){var s=p.getInventory().getItem(i);if(s.is(expected)){count+=s.getCount();if(recipe==1||recipe==2)require(RelicItems.remaining(s,recipe==1)==(recipe==1?256:1000),"Budget not restored");if(recipe==3)require(s.has(net.minecraft.core.component.DataComponents.TRIM),"Trim missing");}}
                require(count==(recipe==0?2:1),"Wrong result count "+count);return "PASS recipe="+recipe+" count="+count+" ingredients consumed; server menu="+m.getClass().getSimpleName();}).get();log(proof);c.player.closeContainer();recipe++;step=recipe==4?15:0;return;
        }
        if(step==15){Files.writeString(Path.of("gameplay-proof.txt"),"PASS four actual client crafting/smithing paths");c.stop();step++;}
    }
}
