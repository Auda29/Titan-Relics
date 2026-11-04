package de.relics.distribution;

import com.google.gson.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Set;

/** Evidence for old hash-only saves. Never rewrites the plan or guesses its former environment. */
public final class PlanningProvenance {
    public static final String FILE="data/relics_planning_environment_v1.json";
    private static final Set<String> COSMETIC_TAGS=Set.of("sereneseasons:blacklisted_biomes",
            "sereneseasons:tropical_biomes","sereneseasons:lesser_color_change_biomes");
    public enum Match { EXACT, COSMETIC_TAGS, DIFFERENT }
    private PlanningProvenance() { }

    public static Match compare(Path root,DistributionJournal.State state,JsonObject current) {
        Path file=root.resolve(FILE);
        JsonObject saved=Files.exists(file)?read(file,state):null;
        String canonical=PlanningFingerprint.hash(current);
        boolean exact=state.fingerprintFormat==0
                ? PlanningFingerprint.legacyMatches(state.fingerprint,DistributionJournal.hash(current.toString()),canonical,
                        System.getProperty(PlanningFingerprint.RECOVERY_PROPERTY,""))
                : state.fingerprint.equals(canonical);
        if(exact) {
            // A recovery flag cannot make an existing, verified old reference describe a different setup.
            if(saved!=null && state.fingerprintFormat==0 && !PlanningFingerprint.hash(saved).equals(canonical))return Match.DIFFERENT;
            return Match.EXACT;
        }
        if(saved==null || state.fingerprintFormat==0)return Match.DIFFERENT;
        return PlanningFingerprint.hash(relevant(saved)).equals(PlanningFingerprint.hash(relevant(current)))
                ? Match.COSMETIC_TAGS:Match.DIFFERENT;
    }

    private static JsonObject read(Path file,DistributionJournal.State state) {
        try {
            JsonObject evidence=JsonParser.parseString(Files.readString(file)).getAsJsonObject();
            JsonObject signature=evidence.getAsJsonObject("signature");
            String hash=state.fingerprintFormat==0?DistributionJournal.hash(signature.toString()):PlanningFingerprint.hash(signature);
            String recorded=evidence.get("fingerprint").getAsString();
            if(evidence.get("version").getAsInt()!=1 || !state.fingerprint.equals(hash)
                    || !(recorded.equals(PlanningFingerprint.hash(signature)) || recorded.equals(DistributionJournal.hash(signature.toString()))))
                throw new IllegalStateException("Environment evidence does not match the saved plan");
            return signature;
        }catch(Exception error){throw new IllegalStateException("Preserve and inspect environment evidence: "+file,error);}
    }

    /** Only the three diagnosed season tags may vary, and only when no captured input references them. */
    public static JsonObject relevant(JsonObject signature) {
        JsonObject result=signature.deepCopy();
        JsonObject tags=result.getAsJsonObject("biomeTags");
        if(tags==null)return result;
        JsonObject inputs=result.deepCopy();inputs.remove("biomeTags");
        for(String name:COSMETIC_TAGS)if(!references(inputs,name))tags.remove(name);
        return result;
    }
    private static boolean references(JsonElement element,String tag) {
        if(element.isJsonObject())return element.getAsJsonObject().entrySet().stream().anyMatch(e->references(e.getValue(),tag));
        if(element.isJsonArray()) {for(var value:element.getAsJsonArray())if(references(value,tag))return true;return false;}
        return element.isJsonPrimitive() && element.getAsJsonPrimitive().isString()
                && (element.getAsString().equals(tag) || element.getAsString().equals("#"+tag));
    }

    /** Called only after the complete runtime validation succeeds. Existing evidence is immutable. */
    public static void remember(Path root,DistributionJournal.State state,JsonObject signature) {
        Path file=root.resolve(FILE);
        if(Files.exists(file)){read(file,state);return;}
        String hash=state.fingerprintFormat==0?DistributionJournal.hash(signature.toString()):PlanningFingerprint.hash(signature);
        if(!state.fingerprint.equals(hash))throw new IllegalStateException("Cannot invent evidence for a different saved environment");
        JsonObject evidence=new JsonObject();evidence.addProperty("version",1);evidence.addProperty("fingerprint",hash);
        evidence.add("signature",signature);
        Path temporary=null;
        try {
            Files.createDirectories(file.getParent());
            temporary=Files.createTempFile(file.getParent(),"relics-environment-",".pending");
            Files.writeString(temporary,evidence.toString(),StandardCharsets.UTF_8);
            Files.move(temporary,file,StandardCopyOption.ATOMIC_MOVE);
        }catch(Exception error){throw new IllegalStateException("Cannot preserve environment evidence: "+file,error);}
        finally {if(temporary!=null)try{Files.deleteIfExists(temporary);}catch(java.io.IOException ignored){}}
    }
}
