package de.relics.testmixin;
import de.relics.distribution.*;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.*;
import net.minecraft.client.gui.screens.worldselection.CreateWorldScreen;
import net.minecraft.client.gui.components.Button;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.storage.LevelResource;
import org.spongepowered.asm.mixin.*;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import java.nio.file.*;
@Mixin(Minecraft.class)
public abstract class BetaClientBootstrap {
 @Unique private int relics$ticks,relics$phase,relics$joined,relics$maxPlayers;
 @Inject(method="tick",at=@At("TAIL")) private void relics$probe(CallbackInfo ci) {
 var client=(Minecraft)(Object)this; client.options.getSoundSourceOptionInstance(net.minecraft.sounds.SoundSource.MASTER).set(0.0); org.lwjgl.glfw.GLFW.glfwHideWindow(client.getWindow().handle());
 if(++relics$ticks<150 || relics$ticks%30!=0)return;
 try {
 var screen=client.gui.screen();
 if(relics$phase==0) {
 if(!(screen instanceof TitleScreen)){if(relics$ticks>300)client.gui.setScreen(new TitleScreen());return;}
 if(System.getProperty("relics.acceptance.join")!=null) {
 String address="127.0.0.1:"+System.getProperty("relics.acceptance.join");
 net.minecraft.client.gui.screens.ConnectScreen.startConnecting(new TitleScreen(),client,net.minecraft.client.multiplayer.resolver.ServerAddress.parseString(address),new net.minecraft.client.multiplayer.ServerData("Isolated acceptance",address,net.minecraft.client.multiplayer.ServerData.Type.OTHER),false,null);
 relics$phase=20;return;}
 if(Files.exists(DistributionConfig.file()))throw new AssertionError("Unexpected installation defaults");
 if(!DistributionConfig.load().equals(DistributionSettings.DISCOVERY))throw new AssertionError("Factory default differs");
 if(Files.exists(Path.of("created-world.txt"))) {String name=Files.readString(Path.of("created-world.txt")); client.createWorldOpenFlows().openWorld(name,()->client.gui.setScreen(new TitleScreen()));relics$phase=4;}
 else {Screen parent=new TitleScreen();CreateWorldScreen.openFresh(client,()->client.gui.setScreen(parent));relics$phase=1;}return;
 }
 if(relics$phase==1 && screen instanceof CreateWorldScreen creation) {
 creation.getUiState().setName("Beta Factory Acceptance");creation.getUiState().setSeed("731204");
 if(!((de.relics.client.WorldDistributionDraft)creation).relics$draft().equals(DistributionSettings.DISCOVERY))throw new AssertionError("New world draft differs");
 net.minecraft.client.Screenshot.grab(client,true);relics$phase=2;return;
 }
 if(relics$phase==2) {
 screen.children().stream().filter(Button.class::isInstance).map(Button.class::cast).filter(v->v.getMessage().getString().equals(Component.translatable("selectWorld.create").getString())).findFirst().orElseThrow().onPress(null);relics$phase=3;return;
 }
 if((relics$phase==3 || relics$phase==4) && client.level!=null && client.player!=null && client.getSingleplayerServer()!=null) {
 Path root=client.getSingleplayerServer().getWorldPath(LevelResource.ROOT);Path f=root.resolve("data/relics_distribution_v1.json");
 if(!Files.exists(f))return;var state=new DistributionJournal(f,null).state;if(!state.frozen)return;
 if(!state.settings.equals(DistributionSettings.DISCOVERY))throw new AssertionError("Frozen settings differ from DISCOVERY");
 if(Files.exists(DistributionConfig.file()))throw new AssertionError("Factory check wrote installation defaults");
 Files.writeString(Path.of("created-world.txt"),root.toAbsolutePath().normalize().getFileName().toString());
 Files.writeString(Path.of(relics$phase==3?"creation-proof.txt":"restart-proof.txt"),"PASS actual integrated world; frozen DISCOVERY; absent installation defaults; player="+client.player.getUUID()+"; ticks="+relics$ticks+"; phase="+relics$phase);
 client.gui.setScreen(null);relics$phase=5;return;
 }
 if(relics$phase==20 && client.level!=null && client.player!=null){
 Files.writeString(Path.of("connected-proof.txt"),"connected real client "+client.player.getUUID()+" remote="+System.getProperty("relics.acceptance.join"));
 net.minecraft.client.Screenshot.grab(client,true);relics$joined=relics$ticks;relics$phase=21;return;}
 if(relics$phase==21 && relics$ticks-relics$joined>=400){client.stop();relics$phase=22;return;}
 if(relics$phase==30){
 int count=client.getSingleplayerServer().getPlayerList().getPlayerCount();relics$maxPlayers=Math.max(relics$maxPlayers,count);
 Files.writeString(Path.of("host-players.txt"),"ticks="+(relics$ticks-relics$joined)+" current="+count+" peak="+relics$maxPlayers+" players="+client.getSingleplayerServer().getPlayerList().getPlayers().stream().map(v->v.getUUID().toString()).toList());
 if(relics$ticks-relics$joined>=3600){net.minecraft.client.Screenshot.grab(client,true);Files.writeString(Path.of("multiplayer-proof.txt"),"host 3600 ticks; peak="+relics$maxPlayers);relics$phase=6;}return;}
 if(relics$phase==5 && Boolean.getBoolean("relics.acceptance.host")) {
 var server=client.getSingleplayerServer();server.setUsesAuthentication(false);server.getConnection().startTcpServerListener(java.net.InetAddress.getByName("127.0.0.1"),Integer.getInteger("relics.acceptance.port"));
 Files.writeString(Path.of("host-ready.txt"),"loopback listener started");relics$joined=relics$ticks;relics$phase=30;return;}
 if(relics$phase==5 && Boolean.getBoolean("relics.acceptance.arena")) {
 var server=client.getSingleplayerServer();server.execute(()->{
 for(int x=-2;x<=4;x++)for(int z=-2;z<=4;z++)server.overworld().getChunk(x,z);
 for(String command:java.util.List.of("gamemode spectator @a","time set day","weather clear","forceload add 0 0 112 96","tp @a 55 100 -65 facing 55 65 46"))server.getCommands().performPrefixedCommand(server.createCommandSourceStack(),command);
 });relics$joined=relics$ticks;relics$phase=40;return;}
 if(relics$phase==40 && relics$ticks-relics$joined>=200){var server=client.getSingleplayerServer();server.execute(()->server.getCommands().performPrefixedCommand(server.createCommandSourceStack(),"place template relics:ruined_tower_gameplay_v10 0 -50 0"));relics$phase=41;return;}
 if(relics$phase==41 && relics$ticks-relics$joined>=500){net.minecraft.client.Screenshot.grab(client,true);Files.writeString(Path.of("arena-proof.txt"),"Operator-prepared tower renderer; no reward or crafting interaction claimed");relics$phase=6;return;}
 if(relics$phase==5){net.minecraft.client.Screenshot.grab(client,true);relics$phase=6;return;}
 if(relics$phase==6){Files.writeString(Path.of("menu-proof.txt"),"PASS factory world render and persisted settings");client.stop();relics$phase=7;}
 }catch(Throwable e){try{Files.writeString(Path.of("acceptance-failure.txt"),"phase="+relics$phase+" "+e);}catch(Exception ignored){}throw new IllegalStateException(e);}
 }
}
