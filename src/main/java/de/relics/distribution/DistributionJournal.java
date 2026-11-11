package de.relics.distribution;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Separate atomic planning journal; never resets a malformed or incompatible save. */
public final class DistributionJournal {
    private static final Gson JSON = new GsonBuilder().setPrettyPrinting().create();
    public static final class State {
        public String policy = DistributionPlanner.POLICY;
        public DistributionSettings settings;
        public SurfaceStructurePolicy.State surfaceStructures;
        public String interiors = "legacy";
        public long seed;
        public String fingerprint;
        public int fingerprintFormat;
        public int spawnX, spawnZ, bootstrapX, bootstrapZ;
        public boolean frozen, unavailable;
        public String unavailableReason;
        public int minX, minZ, maxX, maxZ;
        public Set<DistributionPlanner.Family> enabled;
        public DistributionPlanner.Site unique;
        public int lower = 30000, upper = 60000, cursor;
        public long candidatesChecked, slices, maxEvaluationNanos;
        public ColossusSearch.Progress colossusSearch;
        public int colossusMinDistance(){return settings==null?DistributionPlanner.UNIQUE_MIN:settings.colossusMinDistance();}
    }
    private record Envelope(int version, String sha256, String payload) { }
    public static String interiorRevision(Path file) {
        try {
            var envelope=JSON.fromJson(Files.readString(file),Envelope.class);
            if(envelope==null || !supported(envelope.version()) || !hash(envelope.payload()).equals(envelope.sha256()))throw new IllegalStateException("Invalid snapshot checksum");
            return JSON.fromJson(envelope.payload(),State.class).interiors;
        }catch(Exception error){throw new IllegalStateException("Preserve and inspect planning snapshot",error);}
    }
    public final State state;
    public long replacementRetries;
    private final Path file;
    public DistributionJournal(Path file, State initial) {
        this.file=file;
        try {
            if (Files.exists(file)) {
                Envelope envelope = JSON.fromJson(Files.readString(file),Envelope.class);
                if (envelope == null || !supported(envelope.version) || !hash(envelope.payload).equals(envelope.sha256))
                    throw new IllegalStateException("Invalid planning journal checksum/schema");
                state=JSON.fromJson(envelope.payload,State.class);
            } else state=Objects.requireNonNull(initial);
            if(Files.exists(file)) {
                Envelope e=JSON.fromJson(Files.readString(file),Envelope.class);
                if(e.version()!=format(state))throw new IllegalStateException("Structure-policy envelope does not match its state");
            }
            validate();
        } catch (Exception error) { throw new IllegalStateException("Preserve and inspect planning journal: "+file,error); }
    }
    private static boolean supported(int version){return version==1 || version==2;}
    private static int format(State state){return state.surfaceStructures==null?1:2;}
    private void validate() {
        if(state!=null && state.surfaceStructures!=null)state.surfaceStructures.validate();
        if (state==null || state.interiors==null || !Set.of("legacy","interiors-20261027-v1","interiors-20261028-v2","interiors-20261028-v3","interiors-20261028-v4","interiors-20261028-v5","interiors-20261111-v6").contains(state.interiors)
                || !Set.of(DistributionPlanner.POLICY,DistributionPlanner.LEGACY_POLICY,DistributionSettings.LEGACY_POLICY,DistributionSettings.DISCOVERIES_POLICY,DistributionSettings.POLICY).contains(state.policy) || state.fingerprint==null
                || DistributionSettings.settingsPolicy(state.policy) != (state.settings!=null)
                || state.settings!=null && DistributionSettings.settingsPolicy(state.policy) && !state.policy.equals(state.settings.policy())
                || state.settings!=null && state.settings.generationRevision()==3 && state.colossusSearch==null
                || !state.fingerprint.matches("[a-f0-9]{64}") || state.fingerprintFormat<0
                || state.fingerprintFormat>PlanningFingerprint.FORMAT || state.enabled==null || state.cursor<0
                || state.lower<state.colossusMinDistance() || state.upper<=state.lower || state.minX>=state.maxX || state.minZ>=state.maxZ
                || state.unique!=null && (!state.frozen || state.unavailable || !state.unique.candidate().unique()
                    || DistributionPlanner.distance(state.unique.candidate(),state.spawnX,state.spawnZ)<state.colossusMinDistance()))
            throw new IllegalStateException("Invalid planning snapshot");
        if(state.colossusSearch!=null)state.colossusSearch.validate();
    }
    /** Preserve the complete old plan before replacing its hash representation. Never reset destinations. */
    public void migrateFingerprint(String fingerprint) {
        if(state.fingerprintFormat!=0)throw new IllegalStateException("Only legacy fingerprints can migrate");
        if(fingerprint==null || !fingerprint.matches("[a-f0-9]{64}"))throw new IllegalArgumentException("Invalid new fingerprint");
        String old=state.fingerprint;
        Path backup=file.resolveSibling(file.getFileName()+".pre-canonical-"+old+".bak");
        try {
            byte[] original=Files.readAllBytes(file);
            if(Files.exists(backup)) {
                if(!java.util.Arrays.equals(original,Files.readAllBytes(backup)))
                    throw new IllegalStateException("Existing migration backup differs; preserve both journals");
            } else {
                try(FileChannel channel=FileChannel.open(backup,StandardOpenOption.CREATE_NEW,StandardOpenOption.WRITE)) {
                    ByteBuffer buffer=ByteBuffer.wrap(original);
                    while(buffer.hasRemaining())channel.write(buffer);
                    channel.force(true);
                }
            }
            state.fingerprint=fingerprint;state.fingerprintFormat=PlanningFingerprint.FORMAT;
            try {flush();}catch(RuntimeException error){state.fingerprint=old;state.fingerprintFormat=0;throw error;}
        }catch(Exception error){throw new IllegalStateException("Legacy planning fingerprint migration failed; preserve the save",error);}
    }
    public void flush() {
        validate();
        try {
            Files.createDirectories(file.getParent());
            String payload=JSON.toJson(state);
            byte[] data=JSON.toJson(new Envelope(format(state),hash(payload),payload)).getBytes(StandardCharsets.UTF_8);
            Path temporary=Files.createTempFile(file.getParent(),"relics-plan-",".pending");
            try {
                try (FileChannel channel=FileChannel.open(temporary,StandardOpenOption.WRITE)) {
                    ByteBuffer buffer=ByteBuffer.wrap(data);
                    while(buffer.hasRemaining()) channel.write(buffer);
                    channel.force(true);
                }
                // Windows readers/backup scanners can briefly deny delete sharing.
                // Retry the SAME fsynced atomic replacement; never use a stale or
                // non-atomic fallback, and fail closed after the bounded retry.
                for(int attempt=0;;attempt++) {
                    try {Files.move(temporary,file,StandardCopyOption.ATOMIC_MOVE,StandardCopyOption.REPLACE_EXISTING);break;}
                    catch(AccessDeniedException busy) {
                        if(attempt>=6)throw busy;
                        replacementRetries++;
                        java.util.concurrent.locks.LockSupport.parkNanos(1000000L<<attempt);
                        if(Thread.currentThread().isInterrupted())throw busy;
                    }
                }
            } finally { Files.deleteIfExists(temporary); }
        } catch(Exception error) { throw new IllegalStateException("Planning snapshot cannot be committed: "+file,error); }
    }
    public static String hash(String text) {
        try { return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(text.getBytes(StandardCharsets.UTF_8))); }
        catch(Exception error) { throw new IllegalStateException(error); }
    }
}
