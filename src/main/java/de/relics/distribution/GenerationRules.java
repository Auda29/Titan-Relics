package de.relics.distribution;

import com.google.gson.*;
import static de.relics.distribution.DistributionPlanner.Family;

/** Effective predicates are revisioned in settings; pinned historical assets stay unchanged. */
public final class GenerationRules {
    private GenerationRules() { }

    static final int BUILD_PADDING=8;

    static boolean fitsBuildHeight(int bottom,int top,int minY,int maxY) {
        return bottom>=minY+BUILD_PADDING && top<=maxY-BUILD_PADDING;
    }

    /** The center envelope is checked against the rotated template box. These
     * limits describe the surrounding land, where there is no template top. */
    record LandscapeGrid(int radius,int step,int maxFall,int maxRise) {
        boolean accepts(int center,int surface,int floor,boolean nearFoundation) {
            int rise=surface-center;
            return floor>=63 && surface==floor
                    && rise>=-(nearFoundation?maxFall:16) && rise<=(nearFoundation?maxRise:16);
        }
    }

    static LandscapeGrid landscapeGrid(JsonObject original,Family family) {
        JsonObject grid=original.getAsJsonObject("condition");
        if(!grid.get("type").getAsString().equals("relics:all_grid"))
            throw new IllegalStateException("Unknown terrain grid");
        int radius=grid.get("radius").getAsInt(),step=grid.get("distance_between_points").getAsInt();
        if(step<=0 || radius!=2*step || grid.get("allowed_count").getAsInt()!=25)
            throw new IllegalStateException("Revision 4 requires a 5 by 5 terrain grid");
        return switch(family) {
            case COLOSSUS -> new LandscapeGrid(radius,step,16,16);
            case OBELISK,TOWER -> new LandscapeGrid(radius,step,6,6);
            case SKULL -> new LandscapeGrid(radius,step,12,12);
            // Lithostitched's legacy relative value is center minus sample.
            case SMALL -> new LandscapeGrid(radius,step,4,12);
            // Bounded models use these rises at actual low contact columns.
            case TREE -> new LandscapeGrid(radius,step,6,6);
            case SKULL_2 -> new LandscapeGrid(radius,step,8,8);
            default -> throw new IllegalArgumentException("No terrain grid for "+family);
        };
    }

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
