package de.relics.distribution;

import com.google.gson.*;
import java.util.TreeSet;

/** JSON objects are unordered; arrays retain their world-generation order. */
public final class PlanningFingerprint {
    public static final int FORMAT=1;
    public static final String RECOVERY_PROPERTY="relics.distribution.legacyFingerprintMigration";
    /** An explicit recovery approval is tied to both the old save and this exact new setup. */
    public static boolean legacyMatches(String saved,String raw,String current,String approval) {
        return saved.equals(raw) || (saved+":"+current).equals(approval);
    }
    private PlanningFingerprint() { }
    public static String hash(JsonElement signature) {
        return DistributionJournal.hash(canonical(signature).toString());
    }
    public static JsonElement canonical(JsonElement value) {
        if(value.isJsonObject()) {
            var result=new JsonObject();
            for(String key:new TreeSet<>(value.getAsJsonObject().keySet()))
                result.add(key,canonical(value.getAsJsonObject().get(key)));
            return result;
        }
        if(value.isJsonArray()) {
            var result=new JsonArray();
            for(JsonElement item:value.getAsJsonArray())result.add(canonical(item));
            return result;
        }
        return value.deepCopy();
    }
}
