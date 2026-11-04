package de.relics;

import com.google.gson.*;
import de.relics.distribution.*;
import java.nio.file.*;
import java.util.*;

/** Compatibility decisions must neither invent old evidence nor touch rejected saves. */
public final class WorldLoadCheckTests {
    private static int assertions;
    private static void check(boolean value){assertions++;if(!value)throw new AssertionError("World-load assertion "+assertions);}
    private static JsonObject signature() {
        return JsonParser.parseString("""
                {"generator":{"type":"minecraft:noise","biomes":"#relics:colossus"},
                 "biomes":[{"id":"minecraft:plains","value":{"temperature":0.8}}],
                 "biomeTags":{"sereneseasons:tropical_biomes":["minecraft:plains"],
                   "relics:colossus":["minecraft:plains"],"c:is_forest":[],"other:unknown":["minecraft:plains"]}}
                """).getAsJsonObject();
    }
    private static Map<String,String> files(Path root) throws Exception {
        Map<String,String> hashes=new TreeMap<>();
        try(var walk=Files.walk(root)){for(Path file:walk.filter(Files::isRegularFile).toList())hashes.put(root.relativize(file).toString(),DistributionJournal.hash(Files.readString(file)));}
        return hashes;
    }
    public static void main(String[] args) throws Exception {
        Path root=Path.of(args[0]).resolve("load-guard");Files.createDirectories(root);
        var baseline=signature();var state=new DistributionJournal.State();
        state.fingerprint=PlanningFingerprint.hash(baseline);state.fingerprintFormat=1;
        var changed=baseline.deepCopy();changed.getAsJsonObject("biomeTags").remove("sereneseasons:tropical_biomes");
        check(PlanningProvenance.compare(root,state,baseline)==PlanningProvenance.Match.EXACT);
        check(PlanningProvenance.compare(root,state,changed)==PlanningProvenance.Match.DIFFERENT);
        check(files(root).isEmpty());
        PlanningProvenance.remember(root,state,baseline);var original=files(root);
        check(PlanningProvenance.compare(root,state,changed)==PlanningProvenance.Match.COSMETIC_TAGS);
        PlanningProvenance.remember(root,state,changed);check(files(root).equals(original));
        for(String key:List.of("relics:colossus","c:is_forest","other:unknown")) {
            var invalid=baseline.deepCopy();invalid.getAsJsonObject("biomeTags").remove(key);
            check(PlanningProvenance.compare(root,state,invalid)==PlanningProvenance.Match.DIFFERENT);
        }
        var invalid=baseline.deepCopy();invalid.getAsJsonObject("generator").addProperty("type","other:generator");
        check(PlanningProvenance.compare(root,state,invalid)==PlanningProvenance.Match.DIFFERENT);
        invalid=baseline.deepCopy();invalid.getAsJsonArray("biomes").get(0).getAsJsonObject().addProperty("id","other:biome");
        check(PlanningProvenance.compare(root,state,invalid)==PlanningProvenance.Match.DIFFERENT);
        for(String reference:List.of("sereneseasons:tropical_biomes","#sereneseasons:tropical_biomes")) {
            var referenced=baseline.deepCopy();referenced.getAsJsonObject("generator").addProperty("biomes",reference);
            var missing=referenced.deepCopy();missing.getAsJsonObject("biomeTags").remove("sereneseasons:tropical_biomes");
            check(!PlanningFingerprint.hash(PlanningProvenance.relevant(referenced)).equals(PlanningFingerprint.hash(PlanningProvenance.relevant(missing))));
        }
        check(files(root).equals(original));
        Files.writeString(root.resolve(PlanningProvenance.FILE),"{}");original=files(root);
        try {PlanningProvenance.compare(root,state,baseline);throw new AssertionError("Corrupt evidence accepted");}catch(IllegalStateException expected){assertions++;}
        check(files(root).equals(original));
        Path legacy=root.resolve("legacy");Files.createDirectories(legacy);state.fingerprintFormat=0;state.fingerprint=DistributionJournal.hash(baseline.toString());
        PlanningProvenance.remember(legacy,state,baseline);
        check(PlanningProvenance.compare(legacy,state,baseline)==PlanningProvenance.Match.EXACT);
        check(PlanningProvenance.compare(legacy,state,changed)==PlanningProvenance.Match.DIFFERENT);
        String previous=System.getProperty(PlanningFingerprint.RECOVERY_PROPERTY);
        try {
            System.setProperty(PlanningFingerprint.RECOVERY_PROPERTY,state.fingerprint+":"+PlanningFingerprint.hash(changed));
            check(PlanningProvenance.compare(legacy,state,changed)==PlanningProvenance.Match.DIFFERENT);
        }finally {
            if(previous==null)System.clearProperty(PlanningFingerprint.RECOVERY_PROPERTY);
            else System.setProperty(PlanningFingerprint.RECOVERY_PROPERTY,previous);
        }
        state.fingerprintFormat=1;state.fingerprint=PlanningFingerprint.hash(baseline);
        check(PlanningProvenance.compare(legacy,state,baseline)==PlanningProvenance.Match.EXACT);
        check(PlanningProvenance.compare(legacy,state,changed)==PlanningProvenance.Match.COSMETIC_TAGS);
        state.fingerprint="0".repeat(64);original=files(legacy);
        try {PlanningProvenance.compare(legacy,state,baseline);throw new AssertionError("Evidence for another plan accepted");}catch(IllegalStateException expected){assertions++;}
        check(files(legacy).equals(original));
        System.out.println("PASS: "+assertions+" world-load provenance, rejection and preservation assertions");
    }
}
