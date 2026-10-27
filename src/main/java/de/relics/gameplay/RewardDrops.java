package de.relics.gameplay;

import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import com.mojang.serialization.Codec;
import net.fabricmc.fabric.api.attachment.v1.*;
import net.fabricmc.fabric.api.event.lifecycle.v1.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.*;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.*;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.*;
import net.minecraft.world.item.*;
import org.slf4j.*;
import java.util.*;
import static de.relics.gameplay.GameplayLedger.*;

/** One saved, personal world entity per reward; pickup commits the existing player receipt. */
public final class RewardDrops {
    private static final Logger LOG=LoggerFactory.getLogger("relics/reward-drops");
    private static final AttachmentType<String> ID=AttachmentRegistry.create(RelicItems.id("reward_drop"),b->b.persistent(Codec.STRING));
    private static final Map<ServerLevel,Set<UUID>> LOADED=new HashMap<>();
    private RewardDrops() { }
    public static boolean isReward(ItemEntity item){return ((AttachmentTarget)item).getAttached(ID)!=null;}
    public static String id(ItemEntity item){return ((AttachmentTarget)item).getAttached(ID);}
    private static Delivery delivery(ItemEntity item) {
        if(!(item.level() instanceof ServerLevel level))return null;
        var d=RelicGameplay.ledger(level.getServer()).state.deliveries.get(id(item));
        return d!=null && item.getStringUUID().equals(d.dropUuid)?d:null;
    }
    public static void initialize() {
        ServerEntityEvents.ENTITY_LOAD.register((entity,level)->{
            if(entity instanceof ItemEntity item && isReward(item)) {
                LOADED.computeIfAbsent(level,key->new HashSet<>()).add(item.getUUID());reconcile(item);
            }
        });
        ServerEntityEvents.ENTITY_UNLOAD.register((entity,level)->{
            var set=LOADED.get(level);if(set!=null)set.remove(entity.getUUID());
        });
        ServerTickEvents.END_SERVER_TICK.register(server->{if(server.overworld().getGameTime()%20==0)reconcileLoaded(server);});
        ServerLifecycleEvents.SERVER_STOPPED.register(server->LOADED.keySet().removeIf(level->level.getServer()==server));
    }
    private static void reconcile(ItemEntity item) {
        var d=delivery(item);if(d==null){item.setNeverPickUp();LOG.error("Unknown reward entity {}; preserve ledger and entity data",item.getUUID());return;}
        var level=(ServerLevel)item.level();var journal=RelicGameplay.ledger(level.getServer());boolean changed=false;
        if(d.phase==DeliveryPhase.IN_FLIGHT && RelicGameplay.savedReceipt(level.getServer(),d.player,d.id)) {
            d.phase=DeliveryPhase.DELIVERED;changed=true;
        } else if(d.phase==DeliveryPhase.DROP_RESERVED && (d.reward==Reward.KEY
                || RelicGameplay.savedReceipt(level.getServer(),d.player,dispatchReceipt(d)))) {
            d.phase=DeliveryPhase.DROPPED;changed=true;
        }
        if(changed)journal.flush();
        if(d.phase==DeliveryPhase.DELIVERED){item.discard();return;}
        item.setTarget(UUID.fromString(d.player));item.setUnlimitedLifetime();item.setInvulnerable(true);
    }
    public static void reconcileLoaded(MinecraftServer server) {
        for(var entry:List.copyOf(LOADED.entrySet()))if(entry.getKey().getServer()==server)
            for(var uuid:List.copyOf(entry.getValue())) {
                var entity=entry.getKey().getEntity(uuid);
                if(entity instanceof ItemEntity item)reconcile(item);
            }
    }
    private static String dispatchReceipt(Delivery d){return "drop-payment:"+d.id;}
    public static boolean payKey(ServerPlayer player,Delivery d,ItemStack key) {
        if(d.keyPaid)return true;
        if(d.phase!=DeliveryPhase.QUEUED || !d.player.equals(player.getStringUUID()) || !key.is(RelicItems.COLOSSUS_KEY))return false;
        var journal=RelicGameplay.ledger(player.level().getServer());
        d.phase=DeliveryPhase.PAYMENT_PENDING;journal.flush();
        key.shrink(1);
        if(!RelicGameplay.recordReceipt(player,dispatchReceipt(d))) {
            d.phase=DeliveryPhase.AMBIGUOUS;journal.flush();
            LOG.error("Vault key payment not confirmed for {}; claim held",d.id);return false;
        }
        d.keyPaid=true;d.phase=DeliveryPhase.QUEUED;journal.flush();return true;
    }
    public static boolean reconcilePayment(ServerPlayer player,Delivery d) {
        if(d.phase!=DeliveryPhase.PAYMENT_PENDING)return false;
        if(RelicGameplay.hasReceipt(player,dispatchReceipt(d))) {d.keyPaid=true;d.phase=DeliveryPhase.QUEUED;}
        else d.phase=DeliveryPhase.AMBIGUOUS;
        return true;
    }
    public static void dispatch(ServerPlayer player,Delivery d,ItemStack payment,ItemStack reward) {
        var server=player.level().getServer();var journal=RelicGameplay.ledger(server);
        if(d.phase!=DeliveryPhase.QUEUED || d.reward==Reward.EMERALDS)return;
        var site=journal.state.sites.get(d.source);
        if(site==null)throw new IllegalStateException("Reward has no saved source: "+d.id);
        Point point=d.reward==Reward.CORE?site.vault:site.spawner;
        var level=server.getLevel(ResourceKey.create(Registries.DIMENSION,Identifier.parse(point.dimension())));
        if(level==null || level.getChunkSource().getChunkNow(point.x()>>4,point.z()>>4)==null)return;
        long time=server.overworld().getGameTime();
        if(d.reward==Reward.CORE) {
            if(!payKey(player,d,payment))return;
            if(!d.presentationStarted) {
                if(site.vaultAnimationUntil>time)return;
                d.notBefore=RelicPresentation.beginVault(level,site,time);d.presentationStarted=true;journal.flush();
            }
            if(time<d.notBefore)return;
        }
        d.dropUuid=UUID.randomUUID().toString();d.dropPoint=point;d.phase=DeliveryPhase.DROP_RESERVED;journal.flush();
        var item=new ItemEntity(level,point.x()+.5,point.y()+1.2,point.z()+.5,reward.copy(),
                level.getRandom().nextGaussian()*.04,.2,level.getRandom().nextGaussian()*.04);
        item.setUUID(UUID.fromString(d.dropUuid));item.setTarget(UUID.fromString(d.player));
        item.setDefaultPickUpDelay();item.setUnlimitedLifetime();item.setInvulnerable(true);
        ((AttachmentTarget)item).setAttached(ID,d.id);
        if(!level.addFreshEntity(item)) {LOG.error("Reward entity insertion failed for {}; reserved UUID retained",d.id);return;}
        d.phase=DeliveryPhase.DROPPED;journal.flush();RelicPresentation.reward(level,d,site);
    }
    public static boolean allowPickup(ItemEntity item,Player player) {
        if(!isReward(item) || !(item.level() instanceof ServerLevel))return true;
        var d=delivery(item);
        if(d!=null && d.phase==DeliveryPhase.DELIVERED)item.discard();
        return d!=null && d.phase==DeliveryPhase.DROPPED && d.player.equals(player.getStringUUID())
                && player.isAlive() && !player.isCreative() && !player.isSpectator();
    }
    public static boolean pickup(ItemEntity item,Inventory inventory,ItemStack incoming,Operation<Boolean> original,Player player) {
        if(!isReward(item))return original.call(inventory,incoming);
        if(!(player instanceof ServerPlayer recipient) || !allowPickup(item,player))return false;
        var d=delivery(item);var journal=RelicGameplay.ledger(recipient.level().getServer());
        var expected=new ItemStack(d.reward==Reward.CORE?RelicItems.MACHINE_CORE:RelicItems.COLOSSUS_KEY);
        if(incoming.getCount()!=1 || !ItemStack.isSameItemSameComponents(incoming,expected))return false;
        if(RelicGameplay.hasReceipt(recipient,d.id)) {d.phase=DeliveryPhase.DELIVERED;journal.flush();item.discard();return false;}
        if(inventory.getNonEquipmentItems().stream().noneMatch(s->s.isEmpty()
                || ItemStack.isSameItemSameComponents(s,incoming) && s.getCount()<s.getMaxStackSize()))return false;
        d.phase=DeliveryPhase.IN_FLIGHT;journal.flush();
        int before=incoming.getCount();boolean result=original.call(inventory,incoming);
        if(incoming.getCount()==before){d.phase=DeliveryPhase.DROPPED;journal.flush();return result;}
        if(!incoming.isEmpty())throw new IllegalStateException("Partial one-item reward pickup: "+d.id);
        if(RelicGameplay.recordReceipt(recipient,d.id)){d.phase=DeliveryPhase.DELIVERED;journal.flush();}
        else LOG.error("Reward pickup receipt not saved for {}; retain IN_FLIGHT",d.id);
        return result;
    }
}
