package de.relics;

import com.mojang.authlib.GameProfile;
import de.relics.gameplay.*;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.commands.Commands;
import net.minecraft.core.BlockPos;
import net.minecraft.network.Connection;
import net.minecraft.network.protocol.*;
import net.minecraft.server.level.*;
import net.minecraft.server.network.*;
import net.minecraft.world.entity.animal.golem.IronGolem;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.*;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.entity.vault.VaultBlockEntity;
import net.minecraft.world.phys.AABB;
import java.nio.file.*;
import java.util.*;

/** Real natural markers and native mixins; a packet sink replaces a graphical client. */
public final class NaturalEncounterChecks implements ModInitializer {
    private static ServerPlayer player;
    private static ServerLevel level;
    private static GameplayLedger.Site site;
    private static int stage=-1;
    private static long start;
    private static final List<String> proof=new ArrayList<>();
    private static class Sink extends Connection {
        Sink(){super(PacketFlow.SERVERBOUND);}
        @Override public void send(Packet<?> p){}
        @Override public void send(Packet<?> p,io.netty.channel.ChannelFutureListener listener){}
        @Override public void send(Packet<?> p,io.netty.channel.ChannelFutureListener listener,boolean flush){}
    }
    private static void require(boolean ok,String message){if(!ok)throw new AssertionError(message);}
    private static int count(Item item){return player.getInventory().getNonEquipmentItems().stream().filter(s->s.is(item)).mapToInt(ItemStack::getCount).sum();}
    private static BlockPos pos(GameplayLedger.Point p){return new BlockPos(p.x(),p.y(),p.z());}
    private static List<ItemEntity> drops(Item item,GameplayLedger.Point point){
        return level.getEntitiesOfClass(ItemEntity.class,new AABB(pos(point)).inflate(8)).stream()
                .filter(e->e.getItem().is(item) && RewardDrops.isReward(e)).toList();
    }
    @Override public void onInitialize(){
        CommandRegistrationCallback.EVENT.register((dispatcher,registries,environment)->dispatcher.register(Commands.literal("relicsnaturalencountertest").executes(c->{
            try{
                level=c.getSource().getLevel();site=RelicGameplay.ledger(level.getServer()).state.sites.values().stream().filter(s->!s.fixture).findFirst().orElseThrow();
                var profile=new GameProfile(UUID.nameUUIDFromBytes(("LandmarkProbe:"+site.id).getBytes(java.nio.charset.StandardCharsets.UTF_8)),"LandmarkProbe");
                player=new ServerPlayer(level.getServer(),level,profile,ClientInformation.createDefault());
                player.connection=new ServerGamePacketListenerImpl(level.getServer(),new Sink(),player,CommonListenerCookie.createInitial(profile,false));
                player.setPos(site.spawner.x()+.5,site.spawner.y(),site.spawner.z()-3.5);
                player.setNoGravity(true);player.setInvulnerable(true);player.setGameMode(GameType.SURVIVAL);level.addNewPlayer(player);
                level.getServer().getPlayerList().getPlayers().add(player);level.getServer().getPlayerList().getPlayersByUUID().put(player.getUUID(),player);
                start=level.getGameTime();stage=0;proof.clear();System.out.println("NATURAL_ENCOUNTER_STARTED");
            }catch(Throwable t){fail(t);}return 1;
        })));
        ServerTickEvents.END_SERVER_TICK.register(server->{if(stage>=0)try{tick();}catch(Throwable t){fail(t);}});
    }
    private static void cleanup(){
        if(player!=null){level.getServer().getPlayerList().getPlayers().remove(player);level.getServer().getPlayerList().getPlayersByUUID().remove(player.getUUID());player.discard();}
        stage=-1;
    }
    private static void fail(Throwable t){cleanup();t.printStackTrace();System.out.println("NATURAL_ENCOUNTER_FAIL "+t);}
    private static void tick() throws Exception {
        require(level.getGameTime()-start<1000,"Natural encounter timeout at stage "+stage);
        if(stage==0){
            var golems=level.getEntitiesOfClass(IronGolem.class,new AABB(pos(site.golemSpawn)).inflate(4));
            if(golems.isEmpty())return;
            require(golems.size()==1 && site.participants.contains(player.getStringUUID()),"Natural golem/participant mismatch");
            require(golems.getFirst().distanceToSqr(site.golemSpawn.x()+.5,site.golemSpawn.y(),site.golemSpawn.z()+.5)<4,"Golem outside reserved marker");
            proof.add("natural golem spawned in marker clearance");golems.getFirst().hurtServer(level,level.damageSources().genericKill(),10000);stage=1;
        }else if(stage==1){
            var keys=drops(RelicItems.COLOSSUS_KEY,site.spawner);if(keys.isEmpty() || keys.getFirst().hasPickUpDelay())return;
            require(keys.size()==1 && count(RelicItems.COLOSSUS_KEY)==0,"Key must be a single world drop");
            keys.getFirst().playerTouch(player);require(count(RelicItems.COLOSSUS_KEY)==1,"Natural key pickup failed");
            proof.add("key ejected at central guard structure and collected");
            player.setPos(site.vault.x()+.5,site.vault.y(),site.vault.z()+2.5);stage=2;
        }else if(stage==2){
            var block=(VaultBlockEntity)level.getBlockEntity(pos(site.vault));
            var key=player.getInventory().getNonEquipmentItems().stream().filter(s->s.is(RelicItems.COLOSSUS_KEY)).findFirst().orElseThrow();
            VaultBlockEntity.Server.tryInsertKey(level,pos(site.vault),level.getBlockState(pos(site.vault)),block.getConfig(),block.getServerData(),block.getSharedData(),player,key);
            require(count(RelicItems.COLOSSUS_KEY)==0 && count(RelicItems.MACHINE_CORE)==0,"Vault must debit immediately before world ejection");
            proof.add("console vault consumed key immediately");stage=3;
        }else if(stage==3){
            var cores=drops(RelicItems.MACHINE_CORE,site.vault);if(cores.isEmpty() || cores.getFirst().hasPickUpDelay())return;
            require(cores.size()==1 && count(RelicItems.MACHINE_CORE)==0,"Core must be a single world drop");
            cores.getFirst().playerTouch(player);require(count(RelicItems.MACHINE_CORE)==1,"Natural console core pickup failed");
            proof.add("console core ejected into world and collected separately");
            Files.writeString(Path.of("natural-encounter-proof.txt"),String.join("\n",proof)+"\n");cleanup();System.out.println("NATURAL_ENCOUNTER_PASS");
        }
    }
}
