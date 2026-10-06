package de.relics;

import com.google.gson.*;
import net.minecraft.SharedConstants;
import net.minecraft.server.Bootstrap;
import net.minecraft.data.registries.VanillaRegistries;
import net.minecraft.core.QuartPos;
import net.minecraft.world.level.LevelHeightAccessor;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.NoiseGeneratorSettings;
import net.minecraft.world.level.levelgen.RandomState;
import net.minecraft.world.level.levelgen.presets.WorldPresets;
import net.minecraft.world.level.levelgen.structure.placement.RandomSpreadStructurePlacement;
import net.minecraft.world.level.levelgen.structure.placement.RandomSpreadType;
import java.nio.file.*;
import java.util.*;

/** Read-only search nominations, never a substitute for saved natural-start verification. */
public final class NaturalSiteSurvey {
    public static void main(String[] args) throws Exception {
        SharedConstants.tryDetectVersion(); Bootstrap.bootStrap();
        var lookup = VanillaRegistries.createLookup();
        var generator = WorldPresets.createNormalWorldDimensions(lookup).overworld();
        long seed = Long.parseLong(args[1]);
        var state = RandomState.create(lookup, NoiseGeneratorSettings.OVERWORLD, seed);
        var height = LevelHeightAccessor.create(-64, 384);
        var input = JsonParser.parseString(Files.readString(Path.of(args[0]))).getAsJsonObject();
        var spreads = new HashMap<String, RandomSpreadStructurePlacement>();
        for (var e : input.getAsJsonObject("sets").entrySet()) {
            var p = e.getValue().getAsJsonObject().getAsJsonObject("placement");
            spreads.put("relics:" + e.getKey(), new RandomSpreadStructurePlacement(p.get("spacing").getAsInt(),
                    p.get("separation").getAsInt(), RandomSpreadType.LINEAR, p.get("salt").getAsInt()));
        }
        var contracts = input.getAsJsonArray("structures");
        var found = new JsonObject();
        for (var element : contracts) found.add(element.getAsJsonObject().get("id").getAsString(), new JsonArray());
        int wanted = Integer.parseInt(args[3]), limit = Integer.parseInt(args[2]);
        int completedRing = 0;
        for (int ring = 0; ring <= limit; ring++) {
            completedRing = ring;
            for (var element : contracts) {
                var a = element.getAsJsonObject(); String name = a.get("id").getAsString();
                if (found.getAsJsonArray(name).size() >= wanted) continue;
                var spread = spreads.get("relics:" + a.get("family").getAsString());
                var allowed = new HashSet<String>();
                for (var biome : a.getAsJsonArray("biomes")) if (biome.isJsonPrimitive()) allowed.add(biome.getAsString());
                var resource = a.getAsJsonObject("resource");
                var separation = resource.getAsJsonObject("spawn_condition");
                var grid = separation.getAsJsonObject("terrain_condition").getAsJsonObject("condition");
                int radius = grid.get("radius").getAsInt(), distance = grid.get("distance_between_points").getAsInt();
                int ceiling = grid.getAsJsonObject("condition").getAsJsonArray("conditions").get(1).getAsJsonObject()
                        .getAsJsonObject("permitted_range").get("max_inclusive").getAsInt();
                int slope = a.get("slope").getAsInt();
                int uphill = a.has("uphill_slope") ? a.get("uphill_slope").getAsInt() : slope;
                for (int rx = -ring; rx <= ring && found.getAsJsonArray(name).size() < wanted; rx++) {
                    for (int rz = -ring; rz <= ring && found.getAsJsonArray(name).size() < wanted; rz++) {
                        if (Math.max(Math.abs(rx), Math.abs(rz)) != ring) continue;
                        var chunk = spread.getPotentialStructureChunk(seed, rx * spread.spacing(), rz * spread.spacing());
                        int x = chunk.x() * 16, z = chunk.z() * 16;
                        String biome = generator.getBiomeSource().getNoiseBiome(QuartPos.fromBlock(x), 64,
                                QuartPos.fromBlock(z), state.sampler()).unwrapKey().orElseThrow().identifier().toString();
                        if (!allowed.contains(biome)) continue;
                        boolean clear = true;
                        for (var entry : separation.getAsJsonArray("reservations")) {
                            var reservation = entry.getAsJsonObject();
                            if (SeparatedPlacementCondition.candidateConflicts(spreads.get(reservation.get("set").getAsString()),
                                    seed, chunk.x(), chunk.z(), reservation.get("clearance_chunks").getAsInt(),
                                    reservation.has("earlier_only") && reservation.get("earlier_only").getAsBoolean())) {
                                clear = false; break;
                            }
                        }
                        if (!clear) continue;
                        int center = generator.getFirstFreeHeight(x, z, Heightmap.Types.WORLD_SURFACE_WG, height, state);
                        if (center < 63 || center > ceiling) continue;
                        int startY = center + resource.getAsJsonObject("delegate").getAsJsonObject("start_height")
                                .get("absolute").getAsInt() + a.getAsJsonObject("worldgen_template").getAsJsonArray("anchor").get(1).getAsInt();
                        biome = generator.getBiomeSource().getNoiseBiome(QuartPos.fromBlock(x), QuartPos.fromBlock(startY),
                                QuartPos.fromBlock(z), state.sampler()).unwrapKey().orElseThrow().identifier().toString();
                        if (!allowed.contains(biome)) continue;
                        int min = center, max = center;
                        outer: for (int sx = x - radius; sx <= x + radius; sx += distance) {
                            for (int sz = z - radius; sz <= z + radius; sz += distance) {
                                int surface = generator.getFirstFreeHeight(sx, sz, Heightmap.Types.WORLD_SURFACE_WG, height, state);
                                if (center - surface > slope || surface - center > uphill || surface < 63 || surface > ceiling) { clear = false; break outer; }
                                int floor = generator.getFirstFreeHeight(sx, sz, Heightmap.Types.OCEAN_FLOOR_WG, height, state);
                                if (floor != surface) { clear = false; break outer; }
                                String sampleBiome = generator.getBiomeSource().getNoiseBiome(QuartPos.fromBlock(sx),
                                        QuartPos.fromBlock(center), QuartPos.fromBlock(sz), state.sampler())
                                        .unwrapKey().orElseThrow().identifier().toString();
                                if (sampleBiome.contains("ocean") || sampleBiome.contains("river") ||
                                        (a.get("family").getAsString().equals("titan_skull") && !name.equals("titan_skull_rock") && !allowed.contains(sampleBiome))) {
                                    clear = false; break outer;
                                }
                                min = Math.min(min, surface); max = Math.max(max, surface);
                            }
                        }
                        if (!clear) continue;
                        var candidate = new JsonObject(); candidate.addProperty("x", x); candidate.addProperty("z", z);
                        candidate.addProperty("biome", biome); candidate.addProperty("center_y", center);
                        candidate.addProperty("min_height", min); candidate.addProperty("max_height", max);
                        found.getAsJsonArray(name).add(candidate);
                        System.out.println(name + " " + candidate); System.out.flush();
                    }
                }
            }
            boolean complete = true;
            for (var entry : found.entrySet()) if (entry.getValue().getAsJsonArray().size() < wanted) complete = false;
            if (complete) break;
        }
        var result = new JsonObject(); result.addProperty("seed", seed);
        result.addProperty("rings_searched", completedRing);
        result.addProperty("scope", "Vanilla nominations; must pass actual natural generation with exact artifact");
        result.add("candidates", found);
        Files.writeString(Path.of(args[4]), new GsonBuilder().setPrettyPrinting().create().toJson(result));
        System.out.println("Survey complete: " + result);
        System.exit(0);
    }
}
