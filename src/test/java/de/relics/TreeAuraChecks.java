package de.relics;

import com.mojang.authlib.GameProfile;
import de.relics.gameplay.*;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.minecraft.commands.Commands;
import net.minecraft.core.BlockPos;
import net.minecraft.network.Connection;
import net.minecraft.network.protocol.*;
import net.minecraft.server.level.*;
import net.minecraft.server.network.*;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.Level;
import java.nio.file.*;
import java.util.*;

/** Isolated native adapter proof, including anchors three spatial cells away. */
public final class TreeAuraChecks implements ModInitializer {
    private static class Sink extends Connection {
        Sink(){super(PacketFlow.SERVERBOUND);}
        @Override public void send(Packet<?> p) { }
        @Override public void send(Packet<?> p,io.netty.channel.ChannelFutureListener l) { }
        @Override public void send(Packet<?> p,io.netty.channel.ChannelFutureListener l,boolean f) { }
    }
    private static void check(boolean ok,String message){if(!ok)throw new AssertionError(message);}
    private static ServerPlayer player(ServerLevel level) {
        var profile=new GameProfile(UUID.randomUUID(),"TreeAuraProbe");
        var p=new ServerPlayer(level.getServer(),level,profile,ClientInformation.createDefault());
        p.connection=new ServerGamePacketListenerImpl(level.getServer(),new Sink(),p,CommonListenerCookie.createInitial(profile,false));
        p.setGameMode(GameType.SURVIVAL);return p;
    }
    @Override public void onInitialize() {
        CommandRegistrationCallback.EVENT.register((d,r,e)->d.register(Commands.literal("relicstreeauratest").executes(c->{
            try {
                var level=c.getSource().getLevel();var p=player(level);int count=0;
                for(var anchor:List.of(new BlockPos(-33,120,-33),new BlockPos(255,80,255))) {
                    String id="radius80-"+anchor.getX();var journal=RelicGameplay.ledger(level.getServer());
                    var saved=journal.state.trees.get("fixture:"+id);
                    if(saved==null)RelicGameplay.registerFixtureTree(level,id,anchor);
                    else check(saved.equals(RelicGameplay.point(level,anchor)),"Persisted anchor changed");
                    for(int axis=0;axis<3;axis++)for(int sign:new int[]{-1,1})for(double distance:new double[]{79.999,80.0,80.001}) {
                        double[] pos={anchor.getX()+.5,anchor.getY()+.5,anchor.getZ()+.5};pos[axis]+=sign*distance;
                        p.removeAllEffects();p.setPos(pos[0],pos[1],pos[2]);RelicGameplay.refreshTree(p);
                        for(var effect:List.of(MobEffects.REGENERATION,MobEffects.RESISTANCE)) {
                            check(p.hasEffect(effect)==(distance<=80.0),"Wrong sphere boundary "+Arrays.toString(pos));
                            if(distance<=80.0)check(p.getEffect(effect).getDuration()==6000
                                    && p.getEffect(effect).getAmplifier()==1,"Expected level II and five-minute duration");
                        }
                        count++;
                    }
                    p.removeAllEffects();p.setPos(anchor.getX()+64.5,anchor.getY()+64.5,anchor.getZ()+.5);
                    RelicGameplay.refreshTree(p);check(!p.hasEffect(MobEffects.REGENERATION) && !p.hasEffect(MobEffects.RESISTANCE),"Aura became a box");count++;
                    for(var mode:List.of(GameType.CREATIVE,GameType.SPECTATOR,GameType.ADVENTURE)) {
                        p.removeAllEffects();p.setGameMode(mode);p.setPos(anchor.getX()+.5,anchor.getY()+.5,anchor.getZ()+.5);
                        RelicGameplay.refreshTree(p);
                        for(var effect:List.of(MobEffects.REGENERATION,MobEffects.RESISTANCE))
                            check(p.hasEffect(effect)==(mode==GameType.ADVENTURE),"Eligibility changed");
                        count++;
                    }
                    p.setGameMode(GameType.SURVIVAL);
                    p.removeAllEffects();p.setPos(anchor.getX()+.5,anchor.getY()+.5,anchor.getZ()+.5);
                    for(var effect:List.of(MobEffects.REGENERATION,MobEffects.RESISTANCE))p.addEffect(new MobEffectInstance(effect,12000,2));
                    RelicGameplay.refreshTree(p);
                    for(var effect:List.of(MobEffects.REGENERATION,MobEffects.RESISTANCE))
                        check(p.getEffect(effect).getAmplifier()==2 && p.getEffect(effect).getDuration()==12000,"Stronger existing effect was downgraded");
                    count++;
                    p.removeAllEffects();
                    for(var effect:List.of(MobEffects.REGENERATION,MobEffects.RESISTANCE))p.addEffect(new MobEffectInstance(effect,12000,1));
                    RelicGameplay.refreshTree(p);
                    for(var effect:List.of(MobEffects.REGENERATION,MobEffects.RESISTANCE))check(p.getEffect(effect).getDuration()==12000,"Longer effect shortened");
                    count++;
                    p.removeAllEffects();RelicGameplay.refreshTree(p);
                    p.setPos(anchor.getX()+81.5,anchor.getY()+.5,anchor.getZ()+.5);RelicGameplay.refreshTree(p);
                    for(var effect:List.of(MobEffects.REGENERATION,MobEffects.RESISTANCE))
                        check(p.getEffect(effect).getDuration()==6000 && p.getEffect(effect).getAmplifier()==1,"Leaving range removed the five-minute tail");
                    count++;
                }
                var other=player(level.getServer().getLevel(Level.NETHER));other.setPos(-32.5,120.5,-32.5);
                RelicGameplay.refreshTree(other);check(!other.hasEffect(MobEffects.REGENERATION) && !other.hasEffect(MobEffects.RESISTANCE),"Aura crossed dimensions");count++;
                String proof="radius=80.0\npositions_and_modes="+count+"\nspatial_three_cell_lookup=true\nspherical_boundary=true\nregeneration_level=2\nresistance_level=2\nduration_ticks=6000\nnormal_effect_merge=true\nleaving_range_retains_both=true\n";
                Files.writeString(Path.of("tree-aura-proof.txt"),proof);System.out.println("TREE_AURA_PASS "+proof.replace('\n',' '));
            }catch(Throwable error){error.printStackTrace();System.out.println("TREE_AURA_FAIL "+error);}
            return 1;
        })));
    }
}
