package de.relics.gameplay;

import de.relics.mixin.TrialPresentationAccessor;
import de.relics.mixin.VaultPresentationAccessor;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.level.block.entity.vault.*;
import net.minecraft.world.level.block.entity.trialspawner.*;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.item.ItemStack;
import java.util.*;
import static de.relics.gameplay.GameplayLedger.*;

/** Native block states, transition sounds and events; personal grants remain in the ledger. */
public final class RelicPresentation {
    private RelicPresentation() { }
    public static void trial(ServerLevel level,BlockPos pos,TrialSpawner spawner,Site site,long time) {
        TrialSpawnerState next=site.phase==TrialPhase.READY
                ?(site.activationAt>0?TrialSpawnerState.ACTIVE:TrialSpawnerState.WAITING_FOR_PLAYERS)
                :site.phase!=TrialPhase.COOLDOWN?TrialSpawnerState.ACTIVE
                :time<site.rewardAnimationUntil-40?TrialSpawnerState.WAITING_FOR_REWARD_EJECTION
                :time<site.rewardAnimationUntil?TrialSpawnerState.EJECTING_REWARD:TrialSpawnerState.COOLDOWN;
        var data=(TrialPresentationAccessor)spawner.getStateData();
        long spawn=site.phase==TrialPhase.READY?site.activationAt:0;
        if(data.relics$nextSpawn()!=spawn){data.relics$nextSpawn(spawn);spawner.markUpdated();}
        var previous=spawner.getState();
        if(previous==next)return;
        spawner.setState(level,next);
        if(next==TrialSpawnerState.EJECTING_REWARD)level.playSound(null,pos,SoundEvents.TRIAL_SPAWNER_OPEN_SHUTTER,SoundSource.BLOCKS);
        if(previous==TrialSpawnerState.EJECTING_REWARD)level.playSound(null,pos,SoundEvents.TRIAL_SPAWNER_CLOSE_SHUTTER,SoundSource.BLOCKS);
    }
    public static void vault(ServerLevel level,BlockPos pos,VaultSharedData shared,Site site,GameplayLedger ledger) {
        if(!(level.getBlockEntity(pos) instanceof VaultBlockEntity entity))return;
        var state=level.getBlockState(pos);var previous=state.getValue(BlockStateProperties.VAULT_STATE);
        var config=entity.getConfig();var access=(VaultPresentationAccessor)shared;
        Set<UUID> players=new HashSet<>();
        double range=previous==VaultState.INACTIVE?config.activationRange():config.deactivationRange();
        for(var id:config.playerDetector().detect(level,config.entitySelector(),pos,range,true)) {
            var player=level.getPlayerByUUID(id);
            if(player!=null && player.isAlive() && !player.isCreative() && !player.isSpectator()
                    && !ledger.state.vaultClaims.containsKey(site.id+":"+id))players.add(id);
        }
        boolean changed=!players.equals(access.relics$connected());
        if(changed)access.relics$connected(players);
        long time=level.getServer().overworld().getGameTime(),left=site.vaultAnimationUntil-time;
        VaultState next=left>40?VaultState.UNLOCKING:left>0?VaultState.EJECTING
                :players.isEmpty()?VaultState.INACTIVE:VaultState.ACTIVE;
        ItemStack preview=next==VaultState.INACTIVE || left>0 && left<=20?ItemStack.EMPTY:new ItemStack(RelicItems.MACHINE_CORE);
        if(!ItemStack.isSameItemSameComponents(shared.getDisplayItem(),preview)) {shared.setDisplayItem(preview);changed=true;}
        var updated=state.setValue(BlockStateProperties.VAULT_STATE,next).setValue(BlockStateProperties.OMINOUS,false);
        if(updated!=state) {
            level.setBlock(pos,updated,3);
            if(previous!=next)previous.onTransition(level,pos,next,config,shared,false);
            changed=true;
        }
        if(changed){entity.setChanged();level.sendBlockUpdated(pos,state,updated,2);}
    }
    public static long beginVault(ServerLevel level,Site site,long time) {
        BlockPos pos=new BlockPos(site.vault.x(),site.vault.y(),site.vault.z());
        if(!site.vault.dimension().equals(level.dimension().identifier().toString())
                || level.getChunkSource().getChunkNow(pos.getX()>>4,pos.getZ()>>4)==null
                || !(level.getBlockEntity(pos) instanceof VaultBlockEntity))return 0;
        site.vaultAnimationUntil=time+54;
        return time+34;
    }
    public static void reward(ServerLevel level,Delivery delivery,Site site) {
        if(site==null || delivery.reward==Reward.EMERALDS)return;
        Point point=delivery.reward==Reward.CORE?site.vault:site.spawner;
        if(!point.dimension().equals(level.dimension().identifier().toString())
                || level.getChunkSource().getChunkNow(point.x()>>4,point.z()>>4)==null)return;
        BlockPos pos=new BlockPos(point.x(),point.y(),point.z());
        if(delivery.reward==Reward.CORE) {
            level.levelEvent(3017,pos,0);
            level.playSound(null,pos,SoundEvents.VAULT_EJECT_ITEM,SoundSource.BLOCKS);
        }else level.levelEvent(3014,pos,0);
    }
}
