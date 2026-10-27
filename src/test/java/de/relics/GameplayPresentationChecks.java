package de.relics;

import com.mojang.authlib.GameProfile;
import de.relics.gameplay.*;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.commands.Commands;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.Connection;
import net.minecraft.network.protocol.*;
import net.minecraft.network.protocol.game.*;
import net.minecraft.server.level.*;
import net.minecraft.server.network.*;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.animal.golem.IronGolem;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.level.block.entity.HopperBlockEntity;
import net.minecraft.world.item.*;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.entity.trialspawner.*;
import net.minecraft.world.level.block.entity.vault.*;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.GameType;
import net.minecraft.world.phys.AABB;
import java.nio.file.*;
import java.util.*;
import static de.relics.gameplay.GameplayLedger.*;

/** Isolated actual mixin/server adapter test. Packet sink replaces graphical clients. */
public final class GameplayPresentationChecks implements ModInitializer {
    private static final BlockPos SPAWNER=new BlockPos(0,120,0),GOLEM=new BlockPos(0,120,4),VAULT=new BlockPos(-2,120,0);
    private static final Set<TrialSpawnerState> trialStates=EnumSet.noneOf(TrialSpawnerState.class);
    private static final Set<VaultState> vaultStates=EnumSet.noneOf(VaultState.class);
    private static final List<Packet<?>> packets=new ArrayList<>();
    private static ServerPlayer a,b;
    private static ServerLevel world;
    private static int stage=-1;
    private static long started,killed;
    private static ItemEntity magnetProbe;
    private static double maxMagnetSpeed;
    private static String collectedId;
    private static UUID collectedUuid;
    private static long inventoryProbeAt;
    private static class PacketSink extends Connection {
        PacketSink(){super(PacketFlow.SERVERBOUND);}
        @Override public void send(Packet<?> p){packets.add(p);}
        @Override public void send(Packet<?> p,io.netty.channel.ChannelFutureListener listener){packets.add(p);}
        @Override public void send(Packet<?> p,io.netty.channel.ChannelFutureListener listener,boolean flush){packets.add(p);}
    }
    private static void require(boolean value,String message){if(!value)throw new AssertionError(message);}
    private static ServerPlayer player(ServerLevel level,String name,double x) {
        var profile=new GameProfile(UUID.nameUUIDFromBytes(name.getBytes(java.nio.charset.StandardCharsets.UTF_8)),name);
        var player=new ServerPlayer(level.getServer(),level,profile,ClientInformation.createDefault());
        player.connection=new ServerGamePacketListenerImpl(level.getServer(),new PacketSink(),player,CommonListenerCookie.createInitial(profile,false));
        Path saved=level.getServer().getWorldPath(net.minecraft.world.level.storage.LevelResource.PLAYER_DATA_DIR).resolve(player.getStringUUID()+".dat");
        if(Files.exists(saved))try {
            player.load(net.minecraft.world.level.storage.TagValueInput.create(net.minecraft.util.ProblemReporter.DISCARDING,level.registryAccess(),
                    net.minecraft.nbt.NbtIo.readCompressed(saved,net.minecraft.nbt.NbtAccounter.unlimitedHeap())));
        }catch(Exception error){throw new IllegalStateException(error);}
        player.setPos(x,120,-2.5);player.setNoGravity(true);player.setInvulnerable(true);
        player.setGameMode(GameType.SURVIVAL);level.addNewPlayer(player);
        level.getServer().getPlayerList().getPlayers().add(player);
        level.getServer().getPlayerList().getPlayersByUUID().put(player.getUUID(),player);return player;
    }
    private static List<ItemEntity> drops(ServerPlayer player,Item item) {
        return world.getEntitiesOfClass(ItemEntity.class,new AABB(-16,110,-16,16,140,16)).stream()
                .filter(e->e.getItem().is(item) && RewardDrops.isReward(e))
                .filter(e->RelicGameplay.ledger(world.getServer()).state.deliveries.get(RewardDrops.id(e)).player.equals(player.getStringUUID())).toList();
    }
    private static void collect(ServerPlayer player,ItemEntity item) {
        require(!item.hasPickUpDelay(),"Reward pickup delay has not expired");item.playerTouch(player);
    }
    private static void removePlayers() {
        for(var player:new ServerPlayer[]{a,b})if(player!=null){world.getServer().getPlayerList().getPlayers().remove(player);
            world.getServer().getPlayerList().getPlayersByUUID().remove(player.getUUID());player.discard();}
    }
    private static int count(ServerPlayer player,Item item) {
        return player.getInventory().getNonEquipmentItems().stream().filter(s->s.is(item)).mapToInt(ItemStack::getCount).sum();
    }
    private static void insert(ServerPlayer player) {
        var block=(VaultBlockEntity)world.getBlockEntity(VAULT);
        ItemStack key=player.getInventory().getNonEquipmentItems().stream().filter(s->s.is(RelicItems.COLOSSUS_KEY)).findFirst().orElse(ItemStack.EMPTY);
        VaultBlockEntity.Server.tryInsertKey(world,VAULT,world.getBlockState(VAULT),block.getConfig(),block.getServerData(),block.getSharedData(),player,key);
    }
    @Override public void onInitialize() {
        CommandRegistrationCallback.EVENT.register((dispatcher,registries,environment)->dispatcher.register(Commands.literal("relicspresentationtest").executes(c->{
            try {
                world=c.getSource().getLevel();started=world.getGameTime();
                for(int x=-8;x<=8;x++)for(int z=-8;z<=8;z++) {
                    world.setBlock(new BlockPos(x,119,z),Blocks.STONE.defaultBlockState(),3);
                    for(int y=120;y<126;y++)world.setBlock(new BlockPos(x,y,z),Blocks.AIR.defaultBlockState(),3);
                }
                world.setBlock(SPAWNER,Blocks.TRIAL_SPAWNER.defaultBlockState(),3);
                world.setBlock(VAULT,Blocks.VAULT.defaultBlockState(),3);
                RelicGameplay.registerFixture(world,"presentation",SPAWNER,GOLEM,VAULT);
                a=player(world,"RelicProbeA",.5);b=player(world,"RelicProbeB",1.5);
                a.getInventory().add(new ItemStack(RelicItems.MACHINE_CORE));RelicGameplay.unlockMaintenance(a);
                var recipe=ResourceKey.create(Registries.RECIPE,RelicItems.id("machine_core_recharge"));
                require(a.getRecipeBook().contains(recipe),"Core possession unlocks actual server recipe book");
                require(packets.stream().anyMatch(p->p instanceof ClientboundRecipeBookAddPacket r && !r.entries().isEmpty()),"Recipe display packet missing");
                a.getInventory().clearContent();stage=0;
                System.out.println("PRESENTATION_STARTED");
            }catch(Throwable failure){fail(failure);}
            return 1;
        }).then(Commands.literal("reload").executes(c->{
            try {
                var level=c.getSource().getLevel();var ledger=RelicGameplay.ledger(level.getServer());
                var site=ledger.state.sites.get("fixture:presentation");
                require(site!=null && site.phase==TrialPhase.COOLDOWN && site.rewardAnimationUntil>0 && site.vaultAnimationUntil>0,"Saved presentation timeline missing");
                require(ledger.state.vaultClaims.size()==2 && ledger.state.deliveries.size()==4
                        && ledger.state.deliveries.values().stream().filter(d->d.phase==DeliveryPhase.DELIVERED).count()==3
                        && ledger.state.deliveries.values().stream().filter(d->d.phase==DeliveryPhase.DROPPED).count()==1,"Saved uncollected drop or claims lost on restart");
                require(ledger.state.deliveries.values().stream().filter(d->d.reward==Reward.CORE).allMatch(d->d.presentationStarted && d.notBefore>0),"Vault sequence not saved");
                world=level;started=world.getGameTime();a=null;b=player(world,"RelicProbeB",1.5);stage=10;
                RelicGameplay.reconcilePlayer(b);
            }catch(Throwable failure){fail(failure);}
            return 1;
        }))));
        ServerTickEvents.END_SERVER_TICK.register(server->{if(stage<0)return;try{tick();}catch(Throwable failure){fail(failure);}});
    }
    private static void fail(Throwable failure){stage=-1;failure.printStackTrace();System.out.println("PRESENTATION_FAIL "+failure);}
    private static void tick()throws Exception {
        long now=world.getGameTime();require(now-started<600,"Presentation test timed out");
        Site site=RelicGameplay.ledger(world.getServer()).state.sites.get("fixture:presentation");
        var spawner=((net.minecraft.world.level.block.entity.TrialSpawnerBlockEntity)world.getBlockEntity(SPAWNER)).getTrialSpawner();
        var trial=spawner.getState();var vault=world.getBlockState(VAULT).getValue(BlockStateProperties.VAULT_STATE);
        trialStates.add(trial);vaultStates.add(vault);
        if(stage==0 && site.activationAt>0) {
            require(site.phase==TrialPhase.READY && site.activationAt>now,"Spawner must wind up before spawning");
            require(trial==TrialSpawnerState.ACTIVE,"Native spinning state missing during windup");stage=1;
        }else if(stage==1 && site.phase==TrialPhase.ACTIVE) {
            var golems=world.getEntitiesOfClass(IronGolem.class,new AABB(-8,119,-8,8,128,8));
            require(golems.size()==1 && site.participants.size()==2,"One golem for two participants");
            require(now>=site.activationAt,"Golem spawned before windup");
            golems.getFirst().hurtServer(world,world.damageSources().genericKill(),10000);killed=now;
            require(site.phase==TrialPhase.COOLDOWN,"Defeat did not queue rewards");
            require(count(a,RelicItems.COLOSSUS_KEY)==0 && count(b,RelicItems.COLOSSUS_KEY)==0,"Keys bypassed reward animation");stage=2;
            for(int slot=0;slot<36;slot++)a.getInventory().setItem(slot,new ItemStack(Items.COBBLESTONE,64));
        }else if(stage==2 && drops(a,RelicItems.COLOSSUS_KEY).size()==1 && drops(b,RelicItems.COLOSSUS_KEY).size()==1
                && !drops(a,RelicItems.COLOSSUS_KEY).getFirst().hasPickUpDelay() && !drops(b,RelicItems.COLOSSUS_KEY).getFirst().hasPickUpDelay()) {
            require(now>=killed+60,"Key delivered before shutter phase");
            require(trialStates.contains(TrialSpawnerState.WAITING_FOR_REWARD_EJECTION) && trialStates.contains(TrialSpawnerState.EJECTING_REWARD),"Trial shutter states skipped");
            require(count(a,RelicItems.COLOSSUS_KEY)==0 && count(b,RelicItems.COLOSSUS_KEY)==0,"Reward bypassed world ejection");
            var keyA=drops(a,RelicItems.COLOSSUS_KEY).getFirst();var keyB=drops(b,RelicItems.COLOSSUS_KEY).getFirst();
            require(keyA.getUUID().toString().equals(RelicGameplay.ledger(world.getServer()).state.deliveries.get(RewardDrops.id(keyA)).dropUuid),"Drop has no stable saved UUID");
            keyA.playerTouch(b);require(count(b,RelicItems.COLOSSUS_KEY)==0 && keyA.isAlive(),"Other participant stole personal key");
            require(!HopperBlockEntity.addItem(new SimpleContainer(5),keyA) && keyA.getItem().getCount()==1,"Hopper stole personal reward");
            var normalContainer=new SimpleContainer(5);
            require(HopperBlockEntity.addItem(normalContainer,new ItemEntity(world,0,121,0,new ItemStack(Items.DIRT)))
                    && normalContainer.getItem(0).is(Items.DIRT),"Ordinary hopper pickup changed");
            for(int slot=0;slot<36;slot++)a.getInventory().setItem(slot,new ItemStack(Items.COBBLESTONE,64));
            keyA.playerTouch(a);require(keyA.isAlive() && !keyA.getItem().isEmpty(),"Full inventory consumed physical reward");
            a.getInventory().clearContent();collect(a,keyA);collect(b,keyB);
            require(count(a,RelicItems.COLOSSUS_KEY)==1 && count(b,RelicItems.COLOSSUS_KEY)==1,"Owned pickup failed");
            insert(a);insert(a);
            require(count(a,RelicItems.MACHINE_CORE)==0 && count(a,RelicItems.COLOSSUS_KEY)==0,"Vault must consume the key immediately, before core ejection");
            require(RelicGameplay.ledger(world.getServer()).state.deliveries.get("vault:fixture:presentation:"+a.getStringUUID()).keyPaid,"Immediate key debit was not saved");stage=3;
        }else if(stage==3 && drops(a,RelicItems.MACHINE_CORE).size()==1 && !drops(a,RelicItems.MACHINE_CORE).getFirst().hasPickUpDelay()) {
            require(count(a,RelicItems.COLOSSUS_KEY)==0,"Vault key not consumed once");
            require(count(a,RelicItems.MACHINE_CORE)==0,"Core was inserted directly into inventory");
            require(vaultStates.contains(VaultState.UNLOCKING) && vaultStates.contains(VaultState.EJECTING),"Native Vault opening states skipped");
            var core=drops(a,RelicItems.MACHINE_CORE).getFirst();core.playerTouch(b);
            require(count(b,RelicItems.MACHINE_CORE)==0,"Other participant stole core");collect(a,core);
            require(count(a,RelicItems.MACHINE_CORE)==1,"Physical core pickup failed");
            var key=new ItemStack(RelicItems.COLOSSUS_KEY);a.getInventory().add(key);insert(a);
            require(count(a,RelicItems.COLOSSUS_KEY)==1 && count(a,RelicItems.MACHINE_CORE)==1,"Repeated Vault claim consumed key or paid twice");
            a.getInventory().getNonEquipmentItems().stream().filter(s->s.is(RelicItems.COLOSSUS_KEY)).forEach(s->s.setCount(0));
            insert(b);require(count(b,RelicItems.COLOSSUS_KEY)==0 && count(b,RelicItems.MACHINE_CORE)==0,"Second player key was not consumed before waiting for a free Vault");stage=4;
        }else if(stage==4 && drops(b,RelicItems.MACHINE_CORE).size()==1 && now>site.vaultAnimationUntil) {
            require(count(b,RelicItems.COLOSSUS_KEY)==0,"Second participant lost entitlement");
            require(count(b,RelicItems.MACHINE_CORE)==0,"Uncollected core appeared in inventory");
            require(vault==VaultState.INACTIVE,"Vault did not close after all players claimed");
            var ledger=RelicGameplay.ledger(world.getServer());
            require(ledger.state.deliveries.size()==4 && ledger.state.deliveries.values().stream().filter(d->d.phase==DeliveryPhase.DELIVERED).count()==3
                    && ledger.state.deliveries.values().stream().filter(d->d.phase==DeliveryPhase.DROPPED).count()==1,"Pickup receipts or uncollected entitlement failed");
            var ids=packets.stream().filter(p->p instanceof ClientboundLevelEventPacket).map(p->((ClientboundLevelEventPacket)p).getType()).distinct().sorted().toList();
            require(ids.containsAll(List.of(3011,3012,3013,3014,3017)),"Client effect packets missing: "+ids);
            String proof="trial_states="+trialStates+"\nvault_states="+vaultStates+"\nevent_packets="+ids+"\ncollected=3; uncollected=1\ncore_uuid="+drops(b,RelicItems.MACHINE_CORE).getFirst().getUUID()+"\n";
            Files.writeString(Path.of("presentation-proof.txt"),proof);stage=-1;
            removePlayers();System.out.println("PRESENTATION_PASS "+proof.replace('\n',' '));
        }else if(stage==10 && drops(b,RelicItems.MACHINE_CORE).size()==1 && !drops(b,RelicItems.MACHINE_CORE).getFirst().hasPickUpDelay()) {
            var item=drops(b,RelicItems.MACHINE_CORE).getFirst();
            require(Files.readString(Path.of("presentation-proof.txt")).contains(item.getUUID().toString()),"Restart replaced the original reward entity");
            require(count(b,RelicItems.MACHINE_CORE)==0 && !item.hasPickUpDelay(),"Saved drop state: count="+count(b,RelicItems.MACHINE_CORE)+", pickupDelay="+item.hasPickUpDelay());
            collectedId=RewardDrops.id(item);collectedUuid=item.getUUID();
            collect(b,item);require(count(b,RelicItems.MACHINE_CORE)==1,"Persisted reward cannot be collected");
            var ledger=RelicGameplay.ledger(world.getServer());
            require(ledger.state.deliveries.values().stream().allMatch(d->d.phase==DeliveryPhase.DELIVERED),"Pickup receipt failed after restart");
            var finalLedger=new GameplayLedger(world.getServer().getWorldPath(net.minecraft.world.level.storage.LevelResource.ROOT).resolve("data/relics_gameplay_v1.json"));
            require(finalLedger.state.deliveries.values().stream().allMatch(d->d.phase==DeliveryPhase.DELIVERED),"Physical pickup was not committed");
            for(var e:world.getEntitiesOfClass(ItemEntity.class,new AABB(-16,110,-16,16,140,16)))if(!RewardDrops.isReward(e))e.discard();
            b.setItemSlot(net.minecraft.world.entity.EquipmentSlot.OFFHAND,new ItemStack(RelicItems.SALVAGE_MAGNET));
            magnetProbe=new ItemEntity(world,b.getX()+6,b.getY()+3,b.getZ(),new ItemStack(Items.COPPER_INGOT,3));
            magnetProbe.setNoPickUpDelay();world.addFreshEntity(magnetProbe);maxMagnetSpeed=0;stage=11;
        }else if(stage==11) {
            if(!magnetProbe.isRemoved()) {
                maxMagnetSpeed=Math.max(maxMagnetSpeed,magnetProbe.getDeltaMovement().length());
                if(magnetProbe.distanceToSqr(b)<1)magnetProbe.playerTouch(b);
            }
            if(count(b,Items.COPPER_INGOT)==3) {
                require(maxMagnetSpeed>.35 && maxMagnetSpeed<=SalvageMagnet.MAX_SPEED+1e-8,"Magnet velocity did not use increased cap: "+maxMagnetSpeed);
                require(RelicItems.remaining(b.getOffhandItem(),false)==999,"Successful native magnet pickup did not debit exactly once");
                var stale=new ItemEntity(world,-2,122,0,new ItemStack(RelicItems.MACHINE_CORE));stale.setUUID(collectedUuid);
                var field=RewardDrops.class.getDeclaredField("ID");field.setAccessible(true);
                @SuppressWarnings("unchecked") var attachment=(net.fabricmc.fabric.api.attachment.v1.AttachmentType<String>)field.get(null);
                ((net.fabricmc.fabric.api.attachment.v1.AttachmentTarget)stale).setAttached(attachment,collectedId);
                world.addFreshEntity(stale);
                require(stale.isRemoved() && count(b,RelicItems.MACHINE_CORE)==1,"Stale entity snapshot duplicated an acknowledged core");
                Files.writeString(Path.of("magnet-proof.txt"),"offhand_max_speed="+maxMagnetSpeed+"\noffhand_remaining=999\n");
                b.getInventory().setItem(18,b.getMainHandItem());
                b.setItemSlot(net.minecraft.world.entity.EquipmentSlot.MAINHAND,new ItemStack(RelicItems.SALVAGE_MAGNET));
                require(SalvageMagnet.heldMagnet(b)==b.getMainHandItem(),"Main hand must win when both hands hold a magnet");
                magnetProbe=new ItemEntity(world,b.getX()+6,b.getY()+3,b.getZ(),new ItemStack(Items.GOLD_INGOT,2));
                magnetProbe.setNoPickUpDelay();world.addFreshEntity(magnetProbe);maxMagnetSpeed=0;stage=12;
            }
        }else if(stage==12) {
            if(!magnetProbe.isRemoved()) {
                maxMagnetSpeed=Math.max(maxMagnetSpeed,magnetProbe.getDeltaMovement().length());
                if(magnetProbe.distanceToSqr(b)<1)magnetProbe.playerTouch(b);
            }
            if(count(b,Items.GOLD_INGOT)==2) {
                require(maxMagnetSpeed>.35 && maxMagnetSpeed<=SalvageMagnet.MAX_SPEED+1e-8,"Main-hand attraction is missing or too fast");
                require(RelicItems.remaining(b.getMainHandItem(),false)==999 && RelicItems.remaining(b.getOffhandItem(),false)==999,"Main-hand pickup charged the wrong magnet or both magnets");
                b.getInventory().setItem(17,b.getOffhandItem());b.setItemSlot(net.minecraft.world.entity.EquipmentSlot.OFFHAND,ItemStack.EMPTY);
                require(SalvageMagnet.heldMagnet(b)==b.getMainHandItem(),"Magnet with only main hand equipped is inactive");
                b.getInventory().setItem(16,b.getMainHandItem());b.setItemSlot(net.minecraft.world.entity.EquipmentSlot.MAINHAND,ItemStack.EMPTY);
                require(SalvageMagnet.heldMagnet(b).isEmpty(),"Magnet in ordinary inventory is active");
                magnetProbe=new ItemEntity(world,b.getX()+6,120.1,b.getZ(),new ItemStack(Items.DIAMOND),0,0,0);
                magnetProbe.setNoPickUpDelay();world.addFreshEntity(magnetProbe);inventoryProbeAt=now;stage=13;
                Files.writeString(Path.of("magnet-proof.txt"),"main_hand_max_speed="+maxMagnetSpeed+"\nmain_hand_remaining=999\n",StandardOpenOption.APPEND);
            }
        }else if(stage==13 && now-inventoryProbeAt>=24) {
            require(magnetProbe.isAlive() && Math.abs(magnetProbe.getX()-(b.getX()+6))<.001 && count(b,Items.DIAMOND)==0,"Inventory-only magnet attracted an item");
            Files.writeString(Path.of("magnet-proof.txt"),"inventory_only_inactive=true\n",StandardOpenOption.APPEND);
            stage=-1;removePlayers();System.out.println("PRESENTATION_RELOAD_PASS original drop and payments saved; both hands collect; inventory-only inactive");
        }
    }
}
