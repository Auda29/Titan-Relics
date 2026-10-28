package de.relics;

import com.mojang.authlib.GameProfile;
import de.relics.gameplay.*;
import de.relics.mixin.TreeAnimalCapAccess;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.minecraft.commands.Commands;
import net.minecraft.core.BlockPos;
import net.minecraft.network.Connection;
import net.minecraft.network.protocol.*;
import net.minecraft.server.level.*;
import net.minecraft.server.network.*;
import net.minecraft.world.entity.*;
import net.minecraft.world.level.*;
import net.minecraft.world.level.chunk.LevelChunk;
import java.nio.file.*;
import java.util.*;

/** Test-only observation of the production hook in an isolated grass/Plains fixture. */
public final class TreeAnimalChecks implements ModInitializer {
    private static int attempts,successes,beforeCount;
    private static NaturalSpawner.SpawnState observed;
    private static class Sink extends Connection {
        Sink(){super(PacketFlow.SERVERBOUND);}
        @Override public void send(Packet<?> p) { }
        @Override public void send(Packet<?> p,io.netty.channel.ChannelFutureListener l) { }
        @Override public void send(Packet<?> p,io.netty.channel.ChannelFutureListener l,boolean f) { }
    }
    private static void check(boolean value,String msg){if(!value)throw new AssertionError(msg);}
    public static void before() {
        try {
            var f=TreeAnimals.class.getDeclaredField("CONTEXT");f.setAccessible(true);
            Object c=((ThreadLocal<?>)f.get(null)).get();observed=null;
            if(c!=null){var m=c.getClass().getDeclaredMethod("state");m.setAccessible(true);observed=(NaturalSpawner.SpawnState)m.invoke(c);}
            beforeCount=observed==null?-1:observed.getMobCategoryCounts().getInt(MobCategory.CREATURE);attempts++;
        }catch(Exception error){throw new AssertionError(error);}
    }
    public static void after(boolean success) {
        if(!success)return;
        check(observed!=null && beforeCount<10,"Extra spawn bypassed the global creature cap");
        check(observed.getMobCategoryCounts().getInt(MobCategory.CREATURE)==beforeCount+1,"Extra spawn not charged to original SpawnState");successes++;
    }
    private static ServerPlayer player(ServerLevel level) {
        var profile=new GameProfile(UUID.randomUUID(),"AnimalProbe");var p=new ServerPlayer(level.getServer(),level,profile,ClientInformation.createDefault());
        p.connection=new ServerGamePacketListenerImpl(level.getServer(),new Sink(),p,CommonListenerCookie.createInitial(profile,false));
        p.setGameMode(GameType.SURVIVAL);p.setPos(4137.5,160,4104.5);p.setNoGravity(true);p.setInvulnerable(true);
        level.addNewPlayer(p);level.getServer().getPlayerList().getPlayers().add(p);level.getServer().getPlayerList().getPlayersByUUID().put(p.getUUID(),p);return p;
    }
    private static NaturalSpawner.SpawnState state(ServerLevel level,int chunks,Iterable<Entity> entities) {
        return NaturalSpawner.createState(chunks,entities,(key,consumer)->consumer.accept(level.getChunkSource().getChunkNow(ChunkPos.getX(key),ChunkPos.getZ(key))),
                new LocalMobCapCalculator(level.getChunkSource().chunkMap));
    }
    @Override public void onInitialize() {
        CommandRegistrationCallback.EVENT.register((d,r,e)->d.register(Commands.literal("relicstreeanimalstest").executes(c->{
            var level=c.getSource().getLevel();ServerPlayer p=null;
            try {
                p=player(level);var anchor=new BlockPos(4104,160,4104);var chunk=level.getChunk(256,256);
                if(!RelicGameplay.ledger(level.getServer()).state.trees.containsKey("fixture:animals"))RelicGameplay.registerFixtureTree(level,"animals",anchor);
                var source=EntityTypes.COW.create(level,EntitySpawnReason.NATURAL);source.setPos(4104.5,160,4104.5);
                check(!TreeAnimals.afterNaturalSpawn(level,source,chunk),"No independent spawn clock or fixture spawn amplification");
                var full=new ArrayList<Entity>();
                for(int i=0;i<10;i++){var cow=EntityTypes.COW.create(level,EntitySpawnReason.NATURAL);cow.setPos(4104.5,160,4104.5);full.add(cow);}
                var global=state(level,289,full);var local=state(level,2890,full);
                check(!((TreeAnimalCapAccess)(Object)global).relics$global(MobCategory.CREATURE),"Global cap fixture invalid");
                check(!((TreeAnimalCapAccess)(Object)local).relics$local(MobCategory.CREATURE,chunk.getPos()),"Local cap fixture invalid");
                for(var capped:List.of(global,local))TreeAnimals.withContext(capped,(type,pos,ch)->true,(mob,ch)->{throw new AssertionError("Cap callback reached");},
                        ()->check(!TreeAnimals.afterNaturalSpawn(level,source,chunk),"Full cap permitted an extra spawn"));
                attempts=0;successes=0;var population=state(level,289,List.of());
                check(((TreeAnimalCapAccess)(Object)population).relics$local(MobCategory.CREATURE,chunk.getPos()),"Empty local cap fixture has no tracked player");
                level.getRandom().setSeed(731204L);
                for(int i=0;i<4000 && population.getMobCategoryCounts().getInt(MobCategory.CREATURE)<10;i++)
                    NaturalSpawner.spawnForChunk(level,chunk,population,List.of(MobCategory.CREATURE));
                check(successes>0,"No production-hook extra spawn observed; attempts="+attempts);
                check(population.getMobCategoryCounts().getInt(MobCategory.CREATURE)>successes,"Extra spawn occurred without an original ordinary spawn");
                int normal=population.getMobCategoryCounts().getInt(MobCategory.CREATURE)-successes;
                check(successes<=normal,"More than one extra per original spawn");
                String proof="natural_hook=true\nextra_spawns="+successes+"\nordinary_spawns="+normal+"\nobserved_callbacks="+attempts+
                        "\nglobal_cap_blocked=true\nlocal_cap_blocked=true\nno_standalone_spawn=true\nshared_population_accounting=true\n";
                Files.writeString(Path.of("tree-animal-proof.txt"),proof);System.out.println("TREE_ANIMALS_PASS "+proof.replace('\n',' '));
            }catch(Throwable error){error.printStackTrace();System.out.println("TREE_ANIMALS_FAIL "+error);}
            finally{if(p!=null){level.getServer().getPlayerList().getPlayers().remove(p);level.getServer().getPlayerList().getPlayersByUUID().remove(p.getUUID());p.discard();}}
            return 1;
        })));
    }
}
