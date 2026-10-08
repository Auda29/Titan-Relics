package de.relics.gameplay;

import com.mojang.serialization.Codec;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.fabricmc.fabric.api.event.player.UseItemCallback;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.nbt.NbtIo;
import net.minecraft.nbt.NbtAccounter;
import net.minecraft.resources.ResourceKey;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.animal.golem.IronGolem;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.MapItem;
import net.minecraft.world.item.component.ItemLore;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.trialspawner.PlayerDetector;
import net.minecraft.world.level.block.entity.trialspawner.TrialSpawner;
import net.minecraft.world.level.block.entity.trialspawner.TrialSpawnerState;
import net.minecraft.world.level.block.entity.vault.VaultSharedData;
import net.minecraft.world.level.block.entity.vault.VaultBlockEntity;
import net.minecraft.world.level.block.entity.vault.VaultConfig;
import net.minecraft.world.level.block.entity.vault.VaultState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.saveddata.maps.MapDecorationTypes;
import net.minecraft.world.level.saveddata.maps.MapId;
import net.minecraft.world.level.saveddata.maps.MapItemSavedData;
import net.minecraft.world.level.storage.LevelResource;
import net.minecraft.world.phys.Vec3;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;
import static de.relics.gameplay.GameplayLedger.*;
import static de.relics.gameplay.RelicItems.MAP_ORIGIN;

/** Server-only adapters. Nothing recognizes player-built structures or migrates old sites. */
public final class RelicGameplay {
    private static final Logger LOG = LoggerFactory.getLogger("relics/gameplay");
    private static final AttachmentType<Set<String>> RECEIPTS = AttachmentRegistry.create(RelicItems.id("delivery_receipts"),
            builder -> builder.initializer(Set::of).persistent(Codec.STRING.listOf().xmap(Set::copyOf, List::copyOf)).copyOnDeath());
    private static final Map<MinecraftServer, Runtime> RUNTIMES = new WeakHashMap<>();

    private record TreeCell(String dimension, int x, int y, int z) { }
    private static final class Runtime {
        final GameplayLedger ledger;
        final Map<Point, Site> spawners = new HashMap<>(), vaults = new HashMap<>();
        final Map<TreeCell, List<Point>> treeCells = new HashMap<>();
        Runtime(MinecraftServer server) {
            ledger = new GameplayLedger(server.getWorldPath(LevelResource.ROOT).resolve("data/relics_gameplay_v1.json"));
            rebuild();
        }
        void rebuild() {
            spawners.clear(); vaults.clear(); treeCells.clear();
            for (Site site : ledger.state.sites.values()) { spawners.put(site.spawner, site); vaults.put(site.vault, site); }
            for (Point point : ledger.state.trees.values()) treeCells.computeIfAbsent(cell(point), key -> new ArrayList<>()).add(point);
        }
    }
    private RelicGameplay() { }
    public static GameplayLedger ledger(MinecraftServer server) { return runtime(server).ledger; }
    private static Runtime runtime(MinecraftServer server) {
        if (!server.isSameThread()) throw new IllegalStateException("Gameplay mutation outside server thread");
        return RUNTIMES.computeIfAbsent(server, Runtime::new);
    }
    public static Point point(ServerLevel level, BlockPos pos) {
        return new Point(level.dimension().identifier().toString(), pos.getX(), pos.getY(), pos.getZ());
    }
    private static BlockPos pos(Point point) { return new BlockPos(point.x(), point.y(), point.z()); }
    private static TreeCell cell(Point p) { return new TreeCell(p.dimension(), Math.floorDiv(p.x(), 32), Math.floorDiv(p.y(), 32), Math.floorDiv(p.z(), 32)); }
    private static boolean eligible(Player player) { return player.isAlive() && !player.isCreative() && !player.isSpectator(); }
    public static void initialize() {
        ServerLifecycleEvents.SERVER_STARTED.register(server -> runtime(server));
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> RUNTIMES.remove(server));
        ServerTickEvents.START_LEVEL_TICK.register(SalvageMagnet::scan);
        ServerEntityEvents.ENTITY_LOAD.register((entity, level) -> {
            if (entity instanceof DefenseGolem marked && marked.relics$encounter() != null
                    && ledger(level.getServer()).state.terminalGolems.contains(entity.getUUID().toString())) {
                // A stale entity save cannot revive an already confirmed completed/aborted encounter.
                LOG.warn("Discarding stale saved terminal defense golem {} (no new rewards)", entity.getUUID());
                entity.discard();
            }
        });
        ServerTickEvents.END_SERVER_TICK.register(server -> {
            if (server.overworld().getGameTime() % 20 != 0) return;
            for (ServerPlayer player : server.getPlayerList().getPlayers()) {
                refreshTree(player);
                deliverQueued(player);
            }
        });
        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> reconcilePlayer(handler.player));
        ServerLivingEntityEvents.AFTER_DEATH.register((entity, damage) -> {
            if (entity instanceof IronGolem && entity.level() instanceof ServerLevel level)
                finishEncounter(level, entity, true);
        });
        UseItemCallback.EVENT.register((player, level, hand) -> {
            if (!(player instanceof ServerPlayer serverPlayer) || !(level instanceof ServerLevel serverLevel)) return InteractionResult.PASS;
            ItemStack map = player.getItemInHand(hand);
            if (!map.is(Items.FILLED_MAP)) return InteractionResult.PASS;
            String id = map.get(MAP_ORIGIN);
            if (id == null) return InteractionResult.PASS;
            GameplayLedger journal = ledger(serverLevel.getServer());
            Origin origin = journal.state.origins.get(id);
            if (origin != null && origin.phase == OriginPhase.PENDING && journal.state.targetUnavailable && eligible(player)) {
                reserveCompensation(serverPlayer, origin, map);
                return InteractionResult.SUCCESS;
            }
            return InteractionResult.PASS;
        });
        GameplayFixtures.initialize();
    }
    /** Explicit isolated registration only; natural registration is gated on validated builder markers. */
    public static void registerFixture(ServerLevel level, String name, BlockPos spawner, BlockPos golem, BlockPos vault) {
        Runtime rt = runtime(level.getServer());
        String id = "fixture:" + name;
        if (rt.ledger.state.sites.containsKey(id) || rt.spawners.containsKey(point(level, spawner)) || rt.vaults.containsKey(point(level, vault)))
            throw new IllegalArgumentException("Fixture ID/anchor already registered; never overwrite claims");
        Site site = new Site(); site.id = id; site.fixture = true;
        site.spawner = point(level, spawner); site.golemSpawn = point(level, golem); site.vault = point(level, vault);
        rt.ledger.state.sites.put(id, site); rt.ledger.flush(); rt.rebuild();
        if (level.getBlockEntity(vault) instanceof VaultBlockEntity blockEntity) {
            VaultConfig previous = blockEntity.getConfig();
            var table = ResourceKey.create(Registries.LOOT_TABLE, RelicItems.id("gameplay/vault_core"));
            blockEntity.setConfig(new VaultConfig(table, previous.activationRange(), previous.deactivationRange(),
                    new ItemStack(RelicItems.COLOSSUS_KEY), Optional.of(table), previous.playerDetector(), previous.entitySelector()));
            blockEntity.setChanged();
        }
        if (level.getBlockEntity(spawner) instanceof net.minecraft.world.level.block.entity.TrialSpawnerBlockEntity blockEntity)
            blockEntity.getTrialSpawner().overrideEntityToSpawn(EntityTypes.IRON_GOLEM, level);
    }
    public static void registerFixtureTree(ServerLevel level, String name, BlockPos anchor) {
        Runtime rt = runtime(level.getServer());
        if (rt.ledger.state.trees.putIfAbsent("fixture:" + name, point(level, anchor)) != null)
            throw new IllegalArgumentException("Tree ID already registered");
        rt.ledger.flush(); rt.rebuild();
    }
    public static void refreshTree(ServerPlayer player) {
        if (!eligible(player)) return;
        Runtime rt = runtime(player.level().getServer());
        TreeCell cell = cell(point(player.level(), player.blockPosition()));
        for (int x = -1; x <= 1; x++) for (int y = -1; y <= 1; y++) for (int z = -1; z <= 1; z++) {
            for (Point anchor : rt.treeCells.getOrDefault(new TreeCell(cell.dimension, cell.x+x, cell.y+y, cell.z+z), List.of())) {
                if (TreeAura.contains(anchor, player.getX(), player.getY(), player.getZ())) {
                    // Normal merge retains stronger/longer active effects and hidden lower effects.
                    player.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 6000, 0, true, true));
                    return;
                }
            }
        }
    }
    public static boolean tickTrial(ServerLevel level, BlockPos block, TrialSpawner spawner) {
        Runtime rt = runtime(level.getServer());
        Site site = rt.spawners.get(point(level, block));
        if (site == null) return false;
        long time = level.getServer().overworld().getGameTime();
        // Marked trials never execute native ominous/wave/distance-untracking logic.
        if (spawner.isOminous()) spawner.removeOminous(level, block);
        var state = level.getBlockState(block);
        if (state.hasProperty(BlockStateProperties.OMINOUS) && state.getValue(BlockStateProperties.OMINOUS))
            level.setBlock(block, state.setValue(BlockStateProperties.OMINOUS, false), 3);
        boolean changed = false;
        if (site.phase == TrialPhase.COOLDOWN && time >= site.cooldown) { site.phase = TrialPhase.READY; changed = true; }
        Set<String> detected = new HashSet<>();
        if (site.phase != TrialPhase.COOLDOWN) {
            for (UUID id : PlayerDetector.NO_CREATIVE_PLAYERS.detect(level, spawner.getEntitySelector(), block, 14, true)) {
                Player player = level.getPlayerByUUID(id);
                if (player != null && eligible(player)) detected.add(id.toString());
            }
            if (site.phase != TrialPhase.READY && site.participants.addAll(detected)) changed = true;
        }
        if (site.phase == TrialPhase.READY && !detected.isEmpty() && spawner.canSpawnInLevel(level)) {
            IronGolem golem = EntityTypes.IRON_GOLEM.create(level, EntitySpawnReason.TRIAL_SPAWNER);
            if (golem != null && level.hasChunkAt(pos(site.golemSpawn))) {
                golem.setPos(Vec3.atBottomCenterOf(pos(site.golemSpawn)));
                if (level.noCollision(golem)) {
                    site.participants.clear(); site.participants.addAll(detected);
                    site.encounter = UUID.randomUUID().toString(); site.golem = golem.getUUID().toString();
                    site.phase = TrialPhase.SPAWN_PENDING;
                    rt.ledger.flush(); // UUID reserved BEFORE any entity can exist.
                    ((DefenseGolem)golem).relics$mark(site.encounter);
                    golem.setPersistenceRequired();
                    if (level.addFreshEntity(golem)) site.phase = TrialPhase.ACTIVE;
                    else { site.phase = TrialPhase.COOLDOWN; site.cooldown = time + 36000; site.participants.clear(); }
                    changed = true;
                }
            }
        } else if (site.phase == TrialPhase.ACTIVE || site.phase == TrialPhase.SPAWN_PENDING || site.phase == TrialPhase.ENTITY_UNKNOWN) {
            Entity tracked = level.getEntity(UUID.fromString(site.golem));
            if (tracked == null) {
                if (site.phase != TrialPhase.ENTITY_UNKNOWN) { site.phase = TrialPhase.ENTITY_UNKNOWN; changed = true; }
            } else if (tracked instanceof DefenseGolem marked && site.encounter.equals(marked.relics$encounter()) && tracked.isAlive()) {
                if (site.phase != TrialPhase.ACTIVE) { site.phase = TrialPhase.ACTIVE; changed = true; }
            }
            // Absence is not death: no chunk loading, replacement or reward.
        }
        if (changed) rt.ledger.flush();
        TrialSpawnerState visual = site.phase == TrialPhase.READY ? TrialSpawnerState.WAITING_FOR_PLAYERS
                : site.phase == TrialPhase.COOLDOWN ? TrialSpawnerState.COOLDOWN : TrialSpawnerState.ACTIVE;
        if (spawner.getState() != visual) spawner.setState(level, visual);
        return true;
    }
    public static void entityRemoved(Entity entity, Entity.RemovalReason reason) {
        if (entity instanceof DefenseGolem golem && golem.relics$encounter() != null
                && entity.level() instanceof ServerLevel level && reason.shouldDestroy() && reason != Entity.RemovalReason.KILLED)
            finishEncounter(level, entity, false);
    }
    private static void finishEncounter(ServerLevel level, Entity entity, boolean defeated) {
        if (!(entity instanceof DefenseGolem marked) || marked.relics$encounter() == null) return;
        GameplayLedger journal = ledger(level.getServer());
        for (Site site : journal.state.sites.values()) {
            if (journal.completeEncounter(site, entity.getUUID().toString(), marked.relics$encounter(), defeated,
                    level.getServer().overworld().getGameTime())) { journal.flush(); return; }
        }
    }
    public static boolean tickVault(ServerLevel level, BlockPos block, VaultSharedData shared) {
        if (!runtime(level.getServer()).vaults.containsKey(point(level, block))) return false;
        boolean changed = !shared.getDisplayItem().is(RelicItems.MACHINE_CORE);
        if (changed) shared.setDisplayItem(new ItemStack(RelicItems.MACHINE_CORE));
        var state = level.getBlockState(block);
        var next = state;
        if (state.hasProperty(BlockStateProperties.VAULT_STATE) && state.getValue(BlockStateProperties.VAULT_STATE) != VaultState.ACTIVE) {
            next = state.setValue(BlockStateProperties.VAULT_STATE, VaultState.ACTIVE); level.setBlock(block, next, 3); changed = true;
        }
        if (state.hasProperty(BlockStateProperties.OMINOUS) && state.getValue(BlockStateProperties.OMINOUS)) {
            next = next.setValue(BlockStateProperties.OMINOUS, false); level.setBlock(block,next,3); changed = true;
        }
        if (changed) {
            if (level.getBlockEntity(block) != null) level.getBlockEntity(block).setChanged();
            level.sendBlockUpdated(block, state, next, 2);
        }
        return true;
    }
    public static boolean claimVault(ServerLevel level, BlockPos block, Player player, ItemStack key) {
        Runtime rt = runtime(level.getServer()); Site site = rt.vaults.get(point(level, block));
        if (site == null) return false;
        if (!(player instanceof ServerPlayer recipient) || !eligible(player) || !key.is(RelicItems.COLOSSUS_KEY)) return true;
        Delivery delivery = rt.ledger.reserveVault(site, player.getUUID().toString());
        if (delivery == null) return true;
        rt.ledger.flush(); // reservation is unlimited and independent of VaultServerData's finite list.
        attemptDelivery(recipient, delivery, key);
        return true;
    }
    private static Set<String> receipts(ServerPlayer player) { return ((AttachmentTarget)player).getAttachedOrCreate(RECEIPTS); }
    public static void reconcilePlayer(ServerPlayer player) {
        GameplayLedger journal = ledger(player.level().getServer()); boolean changed = false;
        for (Delivery delivery : journal.state.deliveries.values()) if (delivery.player.equals(player.getUUID().toString())) {
            changed |= journal.reconcile(delivery, receipts(player));
            if (delivery.phase == DeliveryPhase.AMBIGUOUS) {
                LOG.error("Reward {} held for reconciliation; no automatic reissue", delivery.id);
                player.sendSystemMessage(Component.translatable("message.relics.reward_held"));
            }
        }
        if (changed) journal.flush();
        deliverQueued(player);
    }
    private static void deliverQueued(ServerPlayer player) {
        GameplayLedger journal = ledger(player.level().getServer());
        for (Delivery delivery : journal.state.deliveries.values()) {
            if (delivery.phase != DeliveryPhase.QUEUED || !delivery.player.equals(player.getUUID().toString())) continue;
            ItemStack payment = ItemStack.EMPTY;
            if (delivery.reward != Reward.KEY) {
                for (int slot = 0; slot < player.getInventory().getContainerSize(); slot++) {
                    ItemStack candidate = player.getInventory().getItem(slot);
                    if (delivery.reward == Reward.CORE ? candidate.is(RelicItems.COLOSSUS_KEY)
                            : candidate.is(Items.FILLED_MAP) && delivery.source.equals(candidate.get(MAP_ORIGIN))) { payment = candidate; break; }
                }
                if (payment.isEmpty()) continue;
            }
            attemptDelivery(player, delivery, payment);
        }
    }
    private static void attemptDelivery(ServerPlayer player, Delivery delivery, ItemStack payment) {
        GameplayLedger journal = ledger(player.level().getServer());
        if (delivery.phase != DeliveryPhase.QUEUED || !delivery.player.equals(player.getUUID().toString()) || !eligible(player)) return;
        if (receipts(player).contains(delivery.id)) { delivery.phase = DeliveryPhase.DELIVERED; journal.flush(); return; }
        ItemStack reward = switch (delivery.reward) {
            case KEY -> new ItemStack(RelicItems.COLOSSUS_KEY);
            case CORE -> new ItemStack(RelicItems.MACHINE_CORE);
            case EMERALDS -> new ItemStack(Items.EMERALD, 3);
        };
        if (delivery.reward != Reward.EMERALDS) {
            var table = ResourceKey.create(Registries.LOOT_TABLE, RelicItems.id(delivery.reward == Reward.CORE ? "gameplay/vault_core" : "gameplay/trial_key"));
            var params = new net.minecraft.world.level.storage.loot.LootParams.Builder(player.level())
                    .create(net.minecraft.world.level.storage.loot.parameters.LootContextParamSets.EMPTY);
            var results = player.level().getServer().reloadableRegistries().getLootTable(table).getRandomItems(params);
            if (results.size() != 1 || results.getFirst().getCount() != reward.getCount() || !ItemStack.isSameItemSameComponents(results.getFirst(), reward)) {
                LOG.error("Fixed relic reward table {} changed or missing; delivery {} remains queued", table, delivery.id);
                return;
            }
            reward = results.getFirst().copy();
        }
        // Conservative: only admit a complete reward. No shared drops or partial payouts.
        int space = 0;
        for (ItemStack slot : player.getInventory().getNonEquipmentItems()) {
            if (slot.isEmpty()) space += reward.getMaxStackSize();
            else if (ItemStack.isSameItemSameComponents(slot, reward)) space += slot.getMaxStackSize() - slot.getCount();
        }
        if (space < reward.getCount()) return;
        if (delivery.reward != Reward.KEY && payment.isEmpty()) return;
        if (delivery.reward == Reward.CORE && !payment.is(RelicItems.COLOSSUS_KEY)) return;
        if (delivery.reward == Reward.EMERALDS && (!payment.is(Items.FILLED_MAP) || !delivery.source.equals(payment.get(MAP_ORIGIN)))) return;
        delivery.phase = DeliveryPhase.IN_FLIGHT; journal.flush();
        if (delivery.reward != Reward.KEY) payment.shrink(1);
        int expected = reward.getCount();
        player.getInventory().add(reward);
        if (!reward.isEmpty()) throw new IllegalStateException("Validated reward insertion failed (" + expected + "); delivery held: " + delivery.id);
        var copy = new HashSet<>(receipts(player)); copy.add(delivery.id);
        ((AttachmentTarget)player).setAttached(RECEIPTS, Set.copyOf(copy));
        player.getInventory().setChanged();
        ((de.relics.mixin.PlayerListSaveInvoker)player.level().getServer().getPlayerList()).relics$savePlayer(player);
        // Vanilla catches save exceptions. Verify the receipt actually reached player.dat before acknowledging.
        try {
            var file = player.level().getServer().getWorldPath(LevelResource.PLAYER_DATA_DIR).resolve(player.getStringUUID() + ".dat");
            var data = NbtIo.readCompressed(file, NbtAccounter.unlimitedHeap());
            boolean saved = data.getCompoundOrEmpty(AttachmentTarget.NBT_ATTACHMENT_KEY).getListOrEmpty("relics:delivery_receipts")
                    .stream().anyMatch(tag -> delivery.id.equals(tag.asString().orElse(null)));
            if (saved) { delivery.phase = DeliveryPhase.DELIVERED; journal.flush(); }
            else LOG.error("Receipt not verified on disk for {}; retain IN_FLIGHT", delivery.id);
        } catch (Exception e) { LOG.error("Receipt verification failed for {}; retain IN_FLIGHT", delivery.id, e); }
    }
    public static ItemStack createPendingMap(ServerLevel level, String id) {
        GameplayLedger journal = ledger(level.getServer());
        if (journal.state.origins.containsKey(id)) throw new IllegalArgumentException("Map origin already exists");
        Origin origin = new Origin(); origin.id = id; journal.state.origins.put(id, origin); journal.flush();
        ItemStack map = new ItemStack(Items.FILLED_MAP); map.set(MAP_ORIGIN, id); updateMap(map, level); return map;
    }
    public static boolean updateMap(ItemStack map, ServerLevel level) {
        String id = map.get(MAP_ORIGIN); if (id == null) return false;
        GameplayLedger journal = ledger(level.getServer()); Origin origin = journal.state.origins.get(id);
        if (origin == null) { map.remove(DataComponents.MAP_ID); setMapStatus(map, "invalid"); return true; }
        if (journal.resolveOrigin(origin)) journal.flush();
        if (origin.phase != OriginPhase.MAP_RESOLVED) {
            map.remove(DataComponents.MAP_ID); map.remove(DataComponents.MAP_DECORATIONS);
            setMapStatus(map, origin.phase == OriginPhase.COMPENSATED ? "compensated" : journal.state.targetUnavailable ? "unavailable" : "pending");
            return true;
        }
        ServerLevel targetLevel = level.getServer().getLevel(ResourceKey.create(Registries.DIMENSION,
                net.minecraft.resources.Identifier.parse(origin.target.dimension())));
        if (targetLevel == null) { setMapStatus(map, "pending"); return true; }
        MapItemSavedData saved = origin.mapId == null ? null : MapItem.getSavedData(new MapId(origin.mapId), targetLevel);
        if (!ExpeditionMaps.matches(saved, origin.target)) {
            ItemStack resolved = MapItem.create(targetLevel, origin.target.x(), origin.target.z(), (byte)2, true, true);
            origin.mapId = resolved.get(DataComponents.MAP_ID).id(); journal.flush();
        }
        map.set(DataComponents.MAP_ID, new MapId(origin.mapId));
        MapItemSavedData.addTargetDecoration(map, pos(origin.target), "relics_colossus", MapDecorationTypes.TARGET_X);
        setMapStatus(map, "resolved"); return false;
    }
    private static void setMapStatus(ItemStack map, String status) {
        Component name = Component.translatable("item.relics.expedition_map." + status);
        if (!name.equals(map.get(DataComponents.ITEM_NAME))) map.set(DataComponents.ITEM_NAME, name);
        ItemLore lore = new ItemLore(List.of(Component.translatable("tooltip.relics.map." + status)));
        if (!lore.equals(map.get(DataComponents.LORE))) map.set(DataComponents.LORE, lore);
    }
    private static void reserveCompensation(ServerPlayer player, Origin origin, ItemStack map) {
        GameplayLedger journal = ledger(player.level().getServer());
        Delivery delivery = journal.reserveCompensation(origin, player.getUUID().toString());
        if (delivery == null) return;
        journal.flush();
        attemptDelivery(player, delivery, map);
    }
}
