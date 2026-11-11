package de.relics.distribution;

import com.google.gson.*;
import static de.relics.distribution.DistributionPlanner.Family;

/** Effective predicates are revisioned in settings; pinned historical assets stay unchanged. */
public final class GenerationRules {
    private GenerationRules() { }
    public static JsonObject terrain(JsonObject original,Family family,BiomeRules.Mode mode,int revision) {
        JsonObject result=original.deepCopy();
        if(revision==1)return result;
        if(revision!=2 && revision!=3)throw new IllegalArgumentException("Unknown terrain revision");
        adjust(result,family,mode);
        return result;
    }
    private static void adjust(JsonElement value,Family family,BiomeRules.Mode mode) {
        if(value.isJsonObject()) {
            JsonObject node=value.getAsJsonObject();
            if(node.has("type") && node.get("type").getAsString().equals("lithostitched:all_of")) {
                JsonArray kept=new JsonArray();
                for(JsonElement item:node.getAsJsonArray("conditions")) {
                    JsonObject condition=item.getAsJsonObject();
                    boolean palette=condition.get("type").getAsString().equals("lithostitched:in_biome")
                            && condition.has("biomes") && condition.get("biomes").isJsonPrimitive()
                            && condition.get("biomes").getAsString().startsWith("#relics:has_structure/");
                    if(mode==BiomeRules.Mode.STANDARD || !palette)kept.add(item);
                }
                node.add("conditions",kept);
            }
            if(family==Family.SKULL_2 && node.has("type") && node.get("type").getAsString().equals("lithostitched:height_filter")
                    && node.has("range_type") && node.get("range_type").getAsString().equals("heightmap_relative")) {
                JsonElement range=node.get("permitted_range");
                if(range.isJsonArray()) {
                    JsonArray values=range.getAsJsonArray();
                    if(values.size()!=2 || values.get(0).getAsInt()!=-4 || values.get(1).getAsInt()!=4)
                        throw new IllegalStateException("Unrecognized Sword Skull terrain contract");
                    JsonArray widened=new JsonArray();widened.add(-8);widened.add(8);node.add("permitted_range",widened);
                }else {
                    JsonObject values=range.getAsJsonObject();
                    if(values.get("min_inclusive").getAsInt()!=-4 || values.get("max_inclusive").getAsInt()!=4)
                        throw new IllegalStateException("Unrecognized Sword Skull terrain contract");
                    values.addProperty("min_inclusive",-8);values.addProperty("max_inclusive",8);
                }
            }
            for(var entry:node.entrySet())adjust(entry.getValue(),family,mode);
        }else if(value.isJsonArray())for(JsonElement child:value.getAsJsonArray())adjust(child,family,mode);
    }
}
