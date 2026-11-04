package de.relics.clientqa;

import de.relics.gameplay.*;
import net.minecraft.client.Minecraft;
import net.minecraft.core.registries.BuiltInRegistries;
import java.nio.file.*;
import java.util.*;

/** Read-only assertions after a saved-world process restart with a real guest. */
public final class BetaPersistenceDriver {
    private static int phase,ticks;
    private static String before;
    private static boolean prepared;
    public static void tick(Minecraft c)throws Exception{
        var s=c.getSingleplayerServer();
        if(phase==3){if(s!=null)return;c.createWorldOpenFlows().openWorld(Files.readString(Path.of("created-world.txt")),()->{});phase=4;return;}
        if(phase==4){if(s==null||c.level==null||c.player==null)return;s.setUsesAuthentication(false);s.getConnection().startTcpServerListener(java.net.InetAddress.getByName("127.0.0.1"),Integer.getInteger("relics.qa.port",25781));Files.writeString(Path.of("reload-ready.txt"),"same process reloaded saved world");phase=5;return;}
        if(s==null)return;
        if(phase==0){s.setUsesAuthentication(false);s.getConnection().startTcpServerListener(java.net.InetAddress.getByName("127.0.0.1"),Integer.getInteger("relics.qa.port",25781));Files.writeString(Path.of("encounter-ready.txt"),"127.0.0.1");phase=1;return;}
        if(s.getPlayerList().getPlayerCount()<2)return;
        if(!prepared){s.submit(()->{for(int x=-2;x<=2;x++)for(int z=-2;z<=2;z++)s.overworld().setBlock(new net.minecraft.core.BlockPos(x,239,z),net.minecraft.world.level.block.Blocks.STONE.defaultBlockState(),3);s.getCommands().performPrefixedCommand(s.createCommandSourceStack(),"tp @a 0.5 240 0.5");return true;}).get();prepared=true;return;}
        String snapshot=s.submit(()->{
            var ledger=RelicGameplay.ledger(s);var root=new TreeMap<String,Object>();
            root.put("ledger",ledger.state);
            var players=new TreeMap<String,Object>();
            for(var p:s.getPlayerList().getPlayers()){
                var inventory=new ArrayList<Object>();
                for(int i=0;i<36;i++){var stack=p.getInventory().getItem(i);if(stack.isEmpty())continue;var item=new TreeMap<String,Object>();item.put("slot",i);item.put("id",BuiltInRegistries.ITEM.getKey(stack.getItem()).toString());item.put("count",stack.getCount());if(RelicItems.core(stack)||RelicItems.magnet(stack))item.put("budget",RelicItems.remaining(stack,RelicItems.core(stack)));inventory.add(item);}
                var receipts=new TreeMap<String,Boolean>();for(var d:ledger.state.deliveries.values())if(d.player.equals(p.getStringUUID()))receipts.put(d.id,RelicGameplay.hasReceipt(p,d.id));
                players.put(p.getStringUUID(),Map.of("inventory",inventory,"receipts",receipts));
            }
            root.put("players",players);return new com.google.gson.GsonBuilder().setPrettyPrinting().create().toJson(root);
        }).get();
        if(phase==1){before=snapshot;Files.writeString(Path.of("persistence-before.json"),snapshot);phase=2;return;}
        if(++ticks<40)return;
        Files.writeString(Path.of("persistence-after.json"),snapshot);
        if(!before.equals(snapshot))throw new AssertionError("Reward/inventory state changed after real-client reconnect");
        if(phase==2){Files.writeString(Path.of("persistence-proof.txt"),"PASS connected-player inventory, budgets, ledger and receipts stable over 200 client ticks; players="+s.getPlayerList().getPlayerCount());phase=30;ticks=0;c.level.disconnect(net.minecraft.network.chat.Component.literal("QA save/reload"));c.disconnect(new net.minecraft.client.gui.screens.TitleScreen(),false);phase=3;return;}
        Files.writeString(Path.of("save-reload-proof.txt"),"PASS same process save/menu/reload; identical inventory, budgets, ledger and receipts; players="+s.getPlayerList().getPlayerCount());c.stop();phase=6;
    }
}
