package de.relics;

import com.google.gson.JsonParser;
import com.mojang.serialization.JsonOps;
import de.relics.gameplay.*;
import io.netty.buffer.Unpooled;
import net.minecraft.core.RegistryAccess;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.game.ClientboundUpdateRecipesPacket;
import net.minecraft.resources.RegistryOps;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.*;
import net.minecraft.world.item.crafting.*;
import java.nio.file.*;
import java.util.*;

/** Encode actual game packets, not just calls to Connection.send. */
public final class RecipeNetworkChecks {
    private static int checks;
    private static void check(boolean value,String message) {
        checks++;if(!value)throw new AssertionError(message);
    }
    private static <T> T roundTrip(StreamCodec<RegistryFriendlyByteBuf,T> codec,T value,RegistryAccess registries) {
        var buffer=new RegistryFriendlyByteBuf(Unpooled.buffer(),registries);
        try {
            codec.encode(buffer,value);
            T decoded=codec.decode(buffer);
            check(buffer.readableBytes()==0,"Network codec left unread bytes");
            return decoded;
        }finally{buffer.release();}
    }
    private static CraftingInput input(boolean core,ItemStack relic) {
        var metal=core?Items.COAL_BLOCK:Items.IRON_INGOT;
        var slots=new ArrayList<>(List.of(ItemStack.EMPTY,new ItemStack(Items.AMETHYST_SHARD),ItemStack.EMPTY,
                new ItemStack(metal),relic,new ItemStack(metal)));
        if(!core)slots.addAll(List.of(new ItemStack(metal),ItemStack.EMPTY,new ItemStack(metal)));
        return CraftingInput.of(3,core?2:3,slots);
    }
    private static void decodedBehavior(Recipe<?> value,boolean core,ServerLevel level) {
        check(value instanceof MaintenanceRecipe,"Decoded a different recipe class");
        var recipe=(MaintenanceRecipe)value;
        check(recipe.getSerializer()==(core?MaintenanceRecipe.CORE:MaintenanceRecipe.MAGNET),"Recipe variant changed");
        check(recipe.getIngredients().size()==(core?6:9),"Decoded recipe book pattern changed");
        var relic=new ItemStack(core?RelicItems.MACHINE_CORE:RelicItems.SALVAGE_MAGNET);
        check(!recipe.matches(input(core,relic),level),"Decoded recipe accepts a full relic");
        RelicItems.setRemaining(relic,core,0);
        relic.set(DataComponents.CUSTOM_NAME,net.minecraft.network.chat.Component.literal("Network recipe probe"));
        var ingredients=input(core,relic);
        check(recipe.matches(ingredients,level),"Decoded recipe rejects depleted relic");
        var result=recipe.assemble(ingredients,level.registryAccess());
        check(RelicItems.remaining(result,core)==(core?256:1000),"Decoded recipe grants wrong budget");
        check(result.get(DataComponents.CUSTOM_NAME).equals(relic.get(DataComponents.CUSTOM_NAME)),"Decoded recipe loses components");
        check(RelicItems.remaining(relic,core)==0,"Decoded recipe mutates crafting input");
    }
    private static void updatePacket(ServerLevel level) {
        // VERSIONED_PACKET_START
        var all=level.getRecipeManager().getRecipes();
        var decoded=roundTrip(ClientboundUpdateRecipesPacket.STREAM_CODEC,new ClientboundUpdateRecipesPacket(all),level.registryAccess());
        check(decoded.getRecipes().size()==all.size(),"Recipe synchronization lost recipes");
        for(boolean core:new boolean[]{true,false}) {
            var id=RelicItems.id(core?"machine_core_recharge":"salvage_magnet_repair");
            var matches=decoded.getRecipes().stream().filter(r->r.id().equals(id)).toList();
            check(matches.size()==1,"Full synchronization lost/duplicated maintenance recipe");
            decodedBehavior(matches.getFirst().value(),core,level);
        }
        // VERSIONED_PACKET_END
    }
    public static void run(ServerLevel level) throws Exception {
        checks=0;
        for(boolean core:new boolean[]{true,false}) {
            var id=RelicItems.id(core?"machine_core_recharge":"salvage_magnet_repair");
            var holder=level.getRecipeManager().byKey(id).orElseThrow();
            var parsed=Recipe.CODEC.parse(RegistryOps.create(JsonOps.INSTANCE,level.registryAccess()),
                    JsonParser.parseString("{\"type\":\""+id+"\"}")).getOrThrow();
            check(parsed!=holder.value(),"Fixture must use distinct recipe instances");
            for(Recipe<?> original:List.of(holder.value(),parsed,new MaintenanceRecipe(core))) {
                var decoded=roundTrip(Recipe.STREAM_CODEC,original,level.registryAccess());
                check(decoded!=original,"Network decode reused server recipe instance");
                decodedBehavior(decoded,core,level);
            }
            var decodedHolder=roundTrip(RecipeHolder.STREAM_CODEC,holder,level.registryAccess());
            check(decodedHolder.id().equals(holder.id()),"Recipe holder lost its ID");
            decodedBehavior(decodedHolder.value(),core,level);
            var buffer=new RegistryFriendlyByteBuf(Unpooled.buffer(),level.registryAccess());
            try {
                boolean rejected=false;
                try{(core?MaintenanceRecipe.CORE:MaintenanceRecipe.MAGNET).streamCodec().encode(buffer,new MaintenanceRecipe(!core));}
                catch(IllegalStateException expected){rejected=true;}
                check(rejected,"Serializer accepted opposite maintenance variant");
            }finally{buffer.release();}
        }
        updatePacket(level);
        String proof="checks="+checks+"\nindependent_recipe_instances=true\nrecipe_and_holder_roundtrip=true\nfull_update_packet_roundtrip=true\nwrong_variant_rejected=true\ndecoded_crafting_preserves_components=true\n";
        Files.writeString(Path.of("recipe-network-proof.txt"),proof);
        System.out.println("RECIPE_NETWORK_PASS "+proof.replace('\n',' '));
    }
}
