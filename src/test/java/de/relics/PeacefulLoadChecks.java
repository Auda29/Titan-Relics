package de.relics;

import com.google.gson.*;
import de.relics.gameplay.*;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.attachment.v1.*;
import net.minecraft.commands.Commands;
import net.minecraft.core.*;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.Container;
import net.minecraft.world.Difficulty;
import net.minecraft.world.item.*;
import java.nio.file.*;
import java.util.*;

/** Only loaded by the isolated world-copy regression server. */
public final class PeacefulLoadChecks implements ModInitializer {
    @Override public void onInitialize(){
        CommandRegistrationCallback.EVENT.register((dispatcher,registries,environment)->dispatcher.register(
            Commands.literal("relicspeacefulcheck").executes(c->verify(c.getSource().getLevel(),false))
                .then(Commands.literal("reload").executes(c->verify(c.getSource().getLevel(),true)))));
    }
    private static int verify(ServerLevel level,boolean reload){
        try {
            if(level.getDifficulty()!=(reload?Difficulty.NORMAL:Difficulty.PEACEFUL))throw new AssertionError("Wrong test difficulty");
            var cert=new Gson().fromJson(Files.readString(Path.of("target-certificate.json")),NaturalInteriors.Certificate.class);
            var field=NaturalInteriors.class.getDeclaredField("DATA");field.setAccessible(true);
            @SuppressWarnings("unchecked") var attachment=(AttachmentType<NaturalInteriors.ChunkData>)field.get(null);
            JsonObject asset=null;
            for(var entry:NaturalInteriors.manifest(cert.revision()).getAsJsonArray("structures"))
                if(entry.getAsJsonObject().get("id").getAsString().equals("ruined_tower"))asset=entry.getAsJsonObject();
            if(asset==null)throw new AssertionError("Missing tower contract");
            int actions=0,chests=0;
            for(var entry:asset.getAsJsonObject("gameplay").getAsJsonArray("markers")) {
                var marker=entry.getAsJsonObject();String role=marker.get("role").getAsString();
                if(!role.equals("tower_enderman_spawn") && !role.endsWith("_chest"))continue;
                BlockPos p=NaturalInteriors.marker(cert,marker);
                var chunk=level.getChunkSource().getChunkNow(p.getX()>>4,p.getZ()>>4);
                if(chunk==null)throw new AssertionError("Tower chunk absent");
                var data=((AttachmentTarget)chunk).getAttached(attachment);
                String action=cert.site()+"/"+marker.get("id").getAsString();
                if(data==null || !data.completed.contains(action))throw new AssertionError("Natural action not completed: "+action);
                if(role.equals("tower_enderman_spawn")) {
                    UUID id=UUID.nameUUIDFromBytes(action.getBytes(java.nio.charset.StandardCharsets.UTF_8));
                    if(level.getEntity(id)!=null)throw new AssertionError("Skipped hostile action respawned");actions++;
                }else{
                    if(!(chunk.getBlockEntity(p) instanceof Container chest))throw new AssertionError("Missing tower chest");
                    if(chest.isEmpty()!=reload)throw new AssertionError(reload?"Consumed loot refilled":"Tower chest not initialized after skipped mobs");
                    if(!reload){chest.clearContent();chunk.getBlockEntity(p).setChanged();chunk.markUnsaved();}chests++;
                }
            }
            if(actions!=5 || chests!=1)throw new AssertionError("Wrong checked role counts");
            Files.writeString(Path.of(reload?"peaceful-reload-proof.txt":"peaceful-proof.txt"),
                    "difficulty="+level.getDifficulty()+"\nskipped_hostile_actions=5\nchests=1\nno_refill="+reload+"\n");
            System.out.println(reload?"PEACEFUL_RELOAD_PASS":"PEACEFUL_LOAD_PASS");
        }catch(Throwable error){error.printStackTrace();System.out.println("PEACEFUL_LOAD_FAIL "+error);}
        return 1;
    }
}
