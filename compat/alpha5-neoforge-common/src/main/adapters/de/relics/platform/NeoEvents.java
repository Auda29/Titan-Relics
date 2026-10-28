package de.relics.platform;

import com.mojang.brigadier.CommandDispatcher;
import net.minecraft.commands.*;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.*;
import net.minecraft.world.*;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.*;
import net.minecraft.world.level.*;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.chunk.LevelChunk;
import net.minecraft.world.phys.BlockHitResult;
import net.neoforged.bus.api.*;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.*;
import net.neoforged.neoforge.event.entity.*;
import net.neoforged.neoforge.event.entity.living.LivingDropsEvent;
import net.neoforged.neoforge.event.entity.player.*;
import net.neoforged.neoforge.event.level.*;
import net.neoforged.neoforge.event.server.*;
import net.neoforged.neoforge.event.tick.*;
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.function.*;

/** Native bus adapters keep gameplay algorithms shared while using NeoForge events. */
public final class NeoEvents {
    private NeoEvents() { }
    public static final class Event<T> {
        private final List<T> listeners=new CopyOnWriteArrayList<>();
        public void register(T listener){listeners.add(listener);}
    }
    @FunctionalInterface public interface CommandsCallback {void register(CommandDispatcher<CommandSourceStack> dispatcher,CommandBuildContext context,Commands.CommandSelection environment);}
    @FunctionalInterface public interface ReloadCallback {void reload(MinecraftServer server,Object resources,boolean success);}
    @FunctionalInterface public interface ItemUse {Object use(Player player,Level level,InteractionHand hand);}
    @FunctionalInterface public interface BlockUse {InteractionResult use(Player player,Level level,InteractionHand hand,BlockHitResult hit);}
    @FunctionalInterface public interface BreakBefore {boolean before(Level level,Player player,BlockPos pos,BlockState state,BlockEntity entity);}
    @FunctionalInterface public interface Join {void joined(Joined handler,Object sender,MinecraftServer server);}
    public static final class Joined {public final ServerPlayer player;Joined(ServerPlayer value){player=value;}}
    @FunctionalInterface public interface Entries {void accept(net.minecraft.world.level.ItemLike item);}
    public static final class CommandRegistrationCallback {public static final Event<CommandsCallback> EVENT=new Event<>();}
    public static final class ServerLifecycleEvents {
        public static final Event<Consumer<MinecraftServer>> SERVER_STARTED=new Event<>(),SERVER_STOPPING=new Event<>(),SERVER_STOPPED=new Event<>();
        public static final Event<ReloadCallback> END_DATA_PACK_RELOAD=new Event<>();
    }
    public static final class ServerTickEvents {
        public static final Event<Consumer<MinecraftServer>> START_SERVER_TICK=new Event<>(),END_SERVER_TICK=new Event<>();
        public static final Event<Consumer<ServerLevel>> START_LEVEL_TICK=new Event<>(),START_WORLD_TICK=START_LEVEL_TICK;
    }
    public static final class ServerEntityEvents {
        public static final Event<BiConsumer<Entity,ServerLevel>> ENTITY_LOAD=new Event<>(),ENTITY_UNLOAD=new Event<>();
    }
    public static final class ServerChunkEvents {public static final Event<BiConsumer<ServerLevel,LevelChunk>> CHUNK_LOAD=new Event<>();}
    public static final class ServerLivingEntityEvents {public static final Event<BiConsumer<LivingEntity,DamageSource>> AFTER_DEATH=new Event<>();}
    public static final class ServerPlayConnectionEvents {public static final Event<Join> JOIN=new Event<>();}
    public static final class UseItemCallback {public static final Event<ItemUse> EVENT=new Event<>();}
    public static final class UseBlockCallback {public static final Event<BlockUse> EVENT=new Event<>();}
    public static final class PlayerBlockBreakEvents {public static final Event<BreakBefore> BEFORE=new Event<>();}
    public static final class ItemGroupEvents {
        private static final Map<ResourceKey<CreativeModeTab>,Event<Consumer<Entries>>> GROUPS=new HashMap<>();
        public static Event<Consumer<Entries>> modifyEntriesEvent(ResourceKey<CreativeModeTab> key){return GROUPS.computeIfAbsent(key,k->new Event<>());}
    }
    public static final class CreativeModeTabEvents {
        public static Event<Consumer<Entries>> modifyOutputEvent(ResourceKey<CreativeModeTab> key){return ItemGroupEvents.modifyEntriesEvent(key);}
    }
    public static void initialize(IEventBus modBus) {
        NeoForge.EVENT_BUS.addListener((RegisterCommandsEvent event)->{
            for(var callback:CommandRegistrationCallback.EVENT.listeners)callback.register(event.getDispatcher(),event.getBuildContext(),event.getCommandSelection());
        });
        NeoForge.EVENT_BUS.addListener((ServerStartedEvent event)->{for(var cb:ServerLifecycleEvents.SERVER_STARTED.listeners)cb.accept(event.getServer());});
        NeoForge.EVENT_BUS.addListener((ServerStoppingEvent event)->{for(var cb:ServerLifecycleEvents.SERVER_STOPPING.listeners)cb.accept(event.getServer());});
        NeoForge.EVENT_BUS.addListener((ServerStoppedEvent event)->{for(var cb:ServerLifecycleEvents.SERVER_STOPPED.listeners)cb.accept(event.getServer());});
        NeoForge.EVENT_BUS.addListener((ServerTickEvent.Pre event)->{for(var cb:ServerTickEvents.START_SERVER_TICK.listeners)cb.accept(event.getServer());});
        NeoForge.EVENT_BUS.addListener((ServerTickEvent.Post event)->{for(var cb:ServerTickEvents.END_SERVER_TICK.listeners)cb.accept(event.getServer());});
        NeoForge.EVENT_BUS.addListener((LevelTickEvent.Pre event)->{if(event.getLevel() instanceof ServerLevel level)for(var cb:ServerTickEvents.START_LEVEL_TICK.listeners)cb.accept(level);});
        NeoForge.EVENT_BUS.addListener((EntityJoinLevelEvent event)->{
            if(event.getLevel() instanceof ServerLevel level) {
                for(var cb:ServerEntityEvents.ENTITY_LOAD.listeners)cb.accept(event.getEntity(),level);
                if(event.getEntity().isRemoved())event.setCanceled(true);
            }
        });
        NeoForge.EVENT_BUS.addListener((EntityLeaveLevelEvent event)->{if(event.getLevel() instanceof ServerLevel level)for(var cb:ServerEntityEvents.ENTITY_UNLOAD.listeners)cb.accept(event.getEntity(),level);});
        NeoForge.EVENT_BUS.addListener((ChunkEvent.Load event)->{
            if(event.getLevel() instanceof ServerLevel level && event.getChunk() instanceof LevelChunk chunk)
                for(var cb:ServerChunkEvents.CHUNK_LOAD.listeners)cb.accept(level,chunk);
        });
        // Drops are reached after death was accepted. Even cancelled loot still
        // represents a confirmed death, unlike a cancellable pre-death event.
        NeoForge.EVENT_BUS.addListener(EventPriority.LOWEST,true,(LivingDropsEvent event)->{
            if(event.getEntity().level() instanceof ServerLevel)for(var cb:ServerLivingEntityEvents.AFTER_DEATH.listeners)cb.accept(event.getEntity(),event.getSource());
        });
        NeoForge.EVENT_BUS.addListener((PlayerEvent.PlayerLoggedInEvent event)->{
            if(event.getEntity() instanceof ServerPlayer player)for(var cb:ServerPlayConnectionEvents.JOIN.listeners)cb.joined(new Joined(player),null,player.getServer());
        });
        NeoForge.EVENT_BUS.addListener((OnDatapackSyncEvent event)->{
            if(event.getPlayer()==null)for(var cb:ServerLifecycleEvents.END_DATA_PACK_RELOAD.listeners)cb.reload(event.getPlayerList().getServer(),null,true);
        });
        NeoForge.EVENT_BUS.addListener((PlayerInteractEvent.RightClickItem event)->{
            for(var cb:UseItemCallback.EVENT.listeners) {
                Object result=cb.use(event.getEntity(),event.getLevel(),event.getHand());
                if(result instanceof InteractionResultHolder<?> holder && holder.getResult()!=InteractionResult.PASS) {
                    event.setCancellationResult(holder.getResult());event.setCanceled(true);break;
                }
            }
        });
        NeoForge.EVENT_BUS.addListener((PlayerInteractEvent.RightClickBlock event)->{
            for(var cb:UseBlockCallback.EVENT.listeners) {
                var result=cb.use(event.getEntity(),event.getLevel(),event.getHand(),event.getHitVec());
                if(result!=InteractionResult.PASS){event.setCancellationResult(result);event.setCanceled(true);break;}
            }
        });
        NeoForge.EVENT_BUS.addListener((BlockEvent.BreakEvent event)->{
            if(event.getLevel() instanceof Level level)for(var cb:PlayerBlockBreakEvents.BEFORE.listeners)
                if(!cb.before(level,event.getPlayer(),event.getPos(),event.getState(),level.getBlockEntity(event.getPos()))){event.setCanceled(true);break;}
        });
        modBus.addListener((BuildCreativeModeTabContentsEvent event)->{
            var callbacks=ItemGroupEvents.GROUPS.get(event.getTabKey());
            if(callbacks!=null)for(var cb:callbacks.listeners)cb.accept(item->event.accept(new ItemStack(item),CreativeModeTab.TabVisibility.PARENT_AND_SEARCH_TABS));
        });
    }
}
