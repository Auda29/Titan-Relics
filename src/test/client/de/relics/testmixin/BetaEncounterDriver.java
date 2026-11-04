package de.relics.clientqa;

import de.relics.gameplay.*;
import net.minecraft.client.Minecraft;
import net.minecraft.core.*;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.inventory.ContainerInput;
import net.minecraft.world.item.*;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.*;
import net.minecraft.world.entity.animal.golem.IronGolem;
import net.minecraft.world.entity.item.ItemEntity;
import java.nio.file.*;

/** Operator-prepared arena, real connections and client-originated attacks/key use. */
public final class BetaEncounterDriver {
    private static int stage,ticks,cycle;
    private static long nextArena;
    private static long started;
    private static BlockPos SPAWNER=new BlockPos(0,120,0),VAULT=new BlockPos(-2,120,0);
    private static void log(String value)throws Exception{Files.writeString(Path.of("encounter-actions.log"),System.currentTimeMillis()+" "+value+"\n",StandardOpenOption.CREATE,StandardOpenOption.APPEND);}
    public static void client(Minecraft c)throws Exception{
        if(c.player==null||c.level==null)return;
        if(c.player.isDeadOrDying()){c.player.respawn();log("client normal respawn request");return;}
        BlockPos vault=null;for(var pos:BlockPos.betweenClosed(c.player.blockPosition().offset(-5,-2,-5),c.player.blockPosition().offset(5,3,5)))if(c.level.getBlockState(pos).is(Blocks.VAULT)){vault=pos.immutable();break;}
        var golems=c.level.getEntitiesOfClass(IronGolem.class,c.player.getBoundingBox().inflate(5));
        for(var g:golems){c.gameMode.attack(c.player,g);c.player.swing(InteractionHand.MAIN_HAND);log("client attack "+g.getUUID());}
        for(int i=0;i<36;i++)if(c.player.getInventory().getItem(i).is(RelicItems.COLOSSUS_KEY)){
            if(i!=0){int slot=i<9?36+i:i;c.gameMode.handleContainerInput(c.player.inventoryMenu.containerId,slot,0,ContainerInput.SWAP,c.player);return;}
            if(vault==null)return; c.player.getInventory().setSelectedSlot(0);
            c.gameMode.useItemOn(c.player,InteractionHand.MAIN_HAND,new BlockHitResult(Vec3.atCenterOf(vault),Direction.NORTH,vault,false));log("client use key at vault");return;
        }
    }
    public static void tick(Minecraft c)throws Exception{
        var s=c.getSingleplayerServer();ticks++;
        if(stage==0){s.setUsesAuthentication(false);s.getConnection().startTcpServerListener(java.net.InetAddress.getByName("127.0.0.1"),Integer.getInteger("relics.qa.port",25781));Files.writeString(Path.of("encounter-ready.txt"),"127.0.0.1");stage=1;return;}
        if(stage==3){if(System.currentTimeMillis()<nextArena)return;cycle++;SPAWNER=new BlockPos(cycle*32,120,0);VAULT=SPAWNER.offset(-2,0,0);stage=1;}
        if(stage==1){if(s.getPlayerList().getPlayerCount()<2)return;
            s.submit(()->{var w=s.overworld();for(int x=cycle*2-1;x<=cycle*2+1;x++)for(int z=-1;z<=1;z++)w.getChunk(x,z);
                for(int x=-8;x<=8;x++)for(int z=-8;z<=8;z++){w.setBlock(new BlockPos(x+cycle*32,119,z),Blocks.STONE.defaultBlockState(),3);for(int y=120;y<127;y++)w.setBlock(new BlockPos(x+cycle*32,y,z),Blocks.AIR.defaultBlockState(),3);}
                w.setBlock(SPAWNER,Blocks.TRIAL_SPAWNER.defaultBlockState(),3);w.setBlock(VAULT,Blocks.VAULT.defaultBlockState(),3);
                RelicGameplay.registerFixture(w,"networkqa"+cycle,SPAWNER,SPAWNER.offset(0,0,4),VAULT);
                for(var p:s.getPlayerList().getPlayers()){if(cycle==0){p.getInventory().clearContent();p.getInventory().setItem(0,new ItemStack(Items.DIAMOND_SWORD));}p.setInvulnerable(true);}
                s.getCommands().performPrefixedCommand(s.createCommandSourceStack(),"tp @a "+(cycle*32+0.5)+" 120 2.5");return true;}).get();
            if(cycle==0)started=System.currentTimeMillis();log("operator arena prepared; real players="+s.getPlayerList().getPlayers().stream().map(p->p.getStringUUID()).toList());stage=2;return;
        }
        if(stage==2){
            client(c);
            String state=s.submit(()->{var w=s.overworld();var ledger=RelicGameplay.ledger(s);var site=ledger.state.sites.get("fixture:networkqa"+cycle);
                for(var p:s.getPlayerList().getPlayers()){
                    p.setInvulnerable(true);
                    for(var d:ledger.state.deliveries.values())if(d.source.equals("fixture:networkqa"+cycle)&&d.player.equals(p.getStringUUID())&&d.reward==GameplayLedger.Reward.CORE&&d.phase!=GameplayLedger.DeliveryPhase.DELIVERED){
                        int keys=0;for(int i=0;i<36;i++)if(p.getInventory().getItem(i).is(RelicItems.COLOSSUS_KEY))keys+=p.getInventory().getItem(i).getCount();
                        if(!d.keyPaid||keys!=0)throw new AssertionError("Key was not consumed before core delivery");
                        System.out.println("QA_KEY_CONSUMED_BEFORE_CORE "+p.getStringUUID()+" delivery="+d.id+" phase="+d.phase+" keys="+keys);
                    }
                    if(site.phase==GameplayLedger.TrialPhase.ACTIVE && site.golem!=null){var golem=w.getEntity(java.util.UUID.fromString(site.golem));if(golem!=null && p.distanceToSqr(golem.position())>9)s.getCommands().performPrefixedCommand(s.createCommandSourceStack(),"tp "+p.getName().getString()+" "+golem.getX()+" "+golem.getY()+" "+golem.getZ());}
                    var items=w.getEntitiesOfClass(ItemEntity.class,new AABB(cycle*32-16,110,-16,cycle*32+16,140,16)).stream().filter(RewardDrops::isReward).filter(e->ledger.state.deliveries.get(RewardDrops.id(e)).player.equals(p.getStringUUID())).toList();
                    if(!items.isEmpty()){var e=items.getFirst();System.out.println("QA_PHYSICAL_DROP "+p.getStringUUID()+" "+e.getUUID()+" "+e.getItem());if(p.distanceToSqr(e.position())>0.5)s.getCommands().performPrefixedCommand(s.createCommandSourceStack(),"tp "+p.getName().getString()+" "+e.getX()+" "+e.getY()+" "+e.getZ());}
                    else {boolean key=false;for(int i=0;i<36;i++)if(p.getInventory().getItem(i).is(RelicItems.COLOSSUS_KEY))key=true;if(key && p.distanceToSqr(cycle*32-2.5,120,-2.5)>1)s.getCommands().performPrefixedCommand(s.createCommandSourceStack(),"tp "+p.getName().getString()+" "+(cycle*32-2.5)+" 120 -2.5");}
                }
                return new com.google.gson.Gson().toJson(ledger.state);}).get();
            log(state);
            boolean complete=s.submit(()->RelicGameplay.ledger(s).state.deliveries.values().stream().filter(d->d.source.equals("fixture:networkqa"+cycle)&&d.phase==GameplayLedger.DeliveryPhase.DELIVERED).count()==4).get();
            if(complete){net.minecraft.client.Screenshot.grab(c,true);log("PASS encounter cycle="+cycle);Files.writeString(Path.of("encounter-final.json"),state);if(System.currentTimeMillis()-started>=1200000){Files.writeString(Path.of("long-session-proof.txt"),"duration_ms="+(System.currentTimeMillis()-started)+" completed_events="+(cycle+1));c.stop();stage=4;}else{nextArena=System.currentTimeMillis()+45000;stage=3;}}
            if(System.currentTimeMillis()-started>1500000)throw new AssertionError("Encounter progress timeout");
        }
    }
}
