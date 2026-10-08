package de.relics.gameplay;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.nio.file.StandardOpenOption;
import java.security.MessageDigest;
import java.util.HashMap;
import java.util.HashSet;
import java.util.HexFormat;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

/** Save-wide write-ahead ledger. Corrupt/unknown files fail closed, never reset claims. */
public final class GameplayLedger {
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    public enum TrialPhase { READY, SPAWN_PENDING, ACTIVE, ENTITY_UNKNOWN, COOLDOWN }
    public enum OriginPhase { PENDING, MAP_RESOLVED, COMPENSATED }
    public enum DeliveryPhase { QUEUED, IN_FLIGHT, DELIVERED, AMBIGUOUS }
    public enum Reward { KEY, CORE, EMERALDS }
    public record Point(String dimension, int x, int y, int z) {
        public Point {
            if (dimension == null || !dimension.matches("[a-z0-9_.-]+:[a-z0-9/._-]+") || Math.abs((long)x) > 30000000 || Math.abs((long)z) > 30000000)
                throw new IllegalArgumentException("Invalid saved gameplay anchor");
        }
    }
    public static final class Site {
        public String id;
        public boolean fixture;
        public Point spawner, golemSpawn, vault;
        public TrialPhase phase = TrialPhase.READY;
        public String encounter, golem;
        public long cooldown;
        public Set<String> participants = new HashSet<>();
    }
    public static final class Origin {
        public String id;
        public OriginPhase phase = OriginPhase.PENDING;
        public Point target;
        public Integer mapId;
    }
    public static final class Delivery {
        public String id, player, source;
        public Reward reward;
        public DeliveryPhase phase = DeliveryPhase.QUEUED;
    }
    public static final class State {
        public int version = 1;
        public Map<String, Site> sites = new HashMap<>();
        public Map<String, Point> trees = new HashMap<>();
        public Map<String, Origin> origins = new HashMap<>();
        public Map<String, Delivery> deliveries = new HashMap<>();
        public Map<String, String> vaultClaims = new HashMap<>();
        public Set<String> terminalGolems = new HashSet<>();
        public boolean targetUnavailable;
        public Point committedTarget;
    }
    private record Envelope(int version, String sha256, String payload) { }
    private final Path file;
    public final State state;
    public GameplayLedger(Path file) {
        this.file = file;
        try {
            if (Files.exists(file)) {
                Envelope envelope = GSON.fromJson(Files.readString(file), Envelope.class);
                if (envelope == null || envelope.version != 1 || !hash(envelope.payload).equals(envelope.sha256))
                    throw new IllegalStateException("Invalid gameplay journal envelope");
                state = GSON.fromJson(envelope.payload, State.class);
                validate();
            } else state = new State();
        } catch (Exception e) { throw new IllegalStateException("Gameplay ledger cannot be read; preserve it and investigate: " + file, e); }
    }
    private void validate() {
        if (state == null || state.version != 1 || state.sites == null || state.origins == null || state.trees == null
                || state.deliveries == null || state.vaultClaims == null || state.terminalGolems == null) throw new IllegalStateException("Unknown/incomplete gameplay state");
        state.terminalGolems.forEach(UUID::fromString);
        state.sites.forEach((id, site) -> {
            if (!id.equals(site.id) || site.phase == null || site.participants == null || site.spawner == null
                    || site.golemSpawn == null || site.vault == null) throw new IllegalStateException("Invalid site " + id);
            if (site.phase != TrialPhase.READY && site.phase != TrialPhase.COOLDOWN) {
                UUID.fromString(site.encounter); UUID.fromString(site.golem);
            }
            site.participants.forEach(UUID::fromString);
        });
        state.origins.forEach((id, origin) -> {
            if (!id.equals(origin.id) || origin.phase == null || origin.phase == OriginPhase.MAP_RESOLVED && origin.target == null)
                throw new IllegalStateException("Invalid map origin " + id);
        });
        state.deliveries.forEach((id, delivery) -> {
            if (!id.equals(delivery.id) || delivery.phase == null || delivery.reward == null || delivery.source == null)
                throw new IllegalStateException("Invalid delivery " + id);
            UUID.fromString(delivery.player);
        });
        state.vaultClaims.forEach((claim, delivery) -> {
            if (!state.deliveries.containsKey(delivery) || state.deliveries.get(delivery).reward != Reward.CORE)
                throw new IllegalStateException("Vault claim missing its delivery: " + claim);
        });
    }
    public void flush() {
        validate();
        try {
            Files.createDirectories(file.getParent());
            String payload = GSON.toJson(state);
            byte[] bytes = GSON.toJson(new Envelope(1, hash(payload), payload)).getBytes(StandardCharsets.UTF_8);
            Path temporary = Files.createTempFile(file.getParent(), "relics-ledger-", ".pending");
            try {
                try (FileChannel channel = FileChannel.open(temporary, StandardOpenOption.WRITE)) {
                    ByteBuffer buffer = ByteBuffer.wrap(bytes);
                    while (buffer.hasRemaining()) channel.write(buffer);
                    channel.force(true);
                }
                // No non-atomic or backup fallback: a stale claim file is worse than stopping.
                Files.move(temporary, file, StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING);
            } finally { Files.deleteIfExists(temporary); }
        } catch (Exception e) { throw new IllegalStateException("Cannot commit gameplay ledger " + file, e); }
    }
    private static String hash(String text) {
        try { return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(text.getBytes(StandardCharsets.UTF_8))); }
        catch (Exception e) { throw new IllegalStateException(e); }
    }
    public Delivery queue(String id, String player, Reward reward, String source) {
        Delivery existing = state.deliveries.get(id);
        if (existing != null) {
            if (!player.equals(existing.player) || reward != existing.reward || !source.equals(existing.source))
                throw new IllegalArgumentException("Conflicting delivery ID " + id);
            return existing;
        }
        Delivery delivery = new Delivery();
        delivery.id = id; delivery.player = player; delivery.reward = reward; delivery.source = source;
        state.deliveries.put(id, delivery);
        return delivery;
    }
    public Delivery reserveVault(Site site, String player) {
        String claim = site.id + ":" + player;
        if (state.vaultClaims.containsKey(claim)) return null;
        Delivery delivery = queue("vault:" + claim, player, Reward.CORE, site.id);
        state.vaultClaims.put(claim, delivery.id);
        return delivery;
    }
    public boolean completeEncounter(Site site, String golem, String encounter, boolean defeated, long time) {
        if (!java.util.Objects.equals(site.golem, golem) || !java.util.Objects.equals(site.encounter, encounter)
                || site.phase == TrialPhase.COOLDOWN || site.phase == TrialPhase.READY) return false;
        if (defeated) for (String player : site.participants)
            queue("trial:" + site.encounter + ":" + player, player, Reward.KEY, site.id);
        site.phase = TrialPhase.COOLDOWN; site.cooldown = time + 36000;
        state.terminalGolems.add(golem);
        site.participants.clear(); return true;
    }
    public boolean resolveOrigin(Origin origin) {
        if (origin.phase != OriginPhase.PENDING || state.committedTarget == null || state.targetUnavailable) return false;
        origin.target = state.committedTarget; origin.phase = OriginPhase.MAP_RESOLVED; return true;
    }
    public Delivery reserveCompensation(Origin origin, String player) {
        if (origin.phase != OriginPhase.PENDING || !state.targetUnavailable) return null;
        Delivery delivery = queue("map:" + origin.id, player, Reward.EMERALDS, origin.id);
        origin.phase = OriginPhase.COMPENSATED; return delivery;
    }
    /** A receipt proves the inventory transaction saved. Absence after dispatch is ambiguous. */
    public boolean reconcile(Delivery delivery, Set<String> receipts) {
        if (receipts.contains(delivery.id)) {
            if (delivery.phase == DeliveryPhase.DELIVERED) return false;
            delivery.phase = DeliveryPhase.DELIVERED; return true;
        }
        if (delivery.phase == DeliveryPhase.IN_FLIGHT || delivery.phase == DeliveryPhase.DELIVERED) {
            delivery.phase = DeliveryPhase.AMBIGUOUS; return true;
        }
        return false;
    }
}
