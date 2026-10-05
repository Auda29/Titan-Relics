package de.relics;

import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import dev.worldgen.lithostitched.api.worldgen.placementcondition.PlacementCondition;
import net.minecraft.core.BlockPos;
import net.minecraft.core.RegistryAccess;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.placement.RandomSpreadStructurePlacement;

import java.util.List;

/** Reserve space around higher-priority candidates without loading their chunks. */
public record SeparatedPlacementCondition(List<Reservation> reservations,
        PlacementCondition terrainCondition) implements PlacementCondition {
    public record Reservation(Identifier set, int clearanceChunks, boolean earlierOnly) {
        static final Codec<Reservation> CODEC = RecordCodecBuilder.create(instance -> instance.group(
                Identifier.CODEC.fieldOf("set").forGetter(Reservation::set),
                Codec.intRange(1, 32).fieldOf("clearance_chunks").forGetter(Reservation::clearanceChunks),
                Codec.BOOL.optionalFieldOf("earlier_only", false).forGetter(Reservation::earlierOnly)
        ).apply(instance, Reservation::new));
    }

    public static final MapCodec<SeparatedPlacementCondition> CODEC = RecordCodecBuilder.mapCodec(instance ->
            instance.group(Reservation.CODEC.listOf().fieldOf("reservations")
                            .forGetter(SeparatedPlacementCondition::reservations),
                    PlacementCondition.CODEC.fieldOf("terrain_condition")
                            .forGetter(SeparatedPlacementCondition::terrainCondition)
            ).apply(instance, SeparatedPlacementCondition::new));

    @Override
    public boolean test(Structure.GenerationContext context, BlockPos pos) {
        // The stub's rounded center can differ from the start chunk. Use the
        // actual generation context, not a guessed chunk from the terrain offset.
        boolean clear = clear(context.registryAccess(), context.seed(), context.chunkPos().x(), context.chunkPos().z());
        if ((context.chunkPos().x() + "," + context.chunkPos().z()).equals(System.getProperty("relics.debugTerrainChunk"))) {
            System.out.println("Relic candidate " + context.chunkPos() + " reservation clear=" + clear);
        }
        return clear && terrainCondition.test(context, pos);
    }

    @Override
    public boolean test(Context context, BlockPos pos) {
        // Feature contexts have no structure start; conservative one-chunk padding.
        return clear(context.registries(), context.seed(), pos.getX() >> 4, pos.getZ() >> 4, 1)
                && terrainCondition.test(context, pos);
    }

    private boolean clear(RegistryAccess registries, long seed, int cx, int cz) {
        return clear(registries, seed, cx, cz, 0);
    }

    private boolean clear(RegistryAccess registries, long seed, int cx, int cz, int extra) {
        var sets = registries.lookupOrThrow(Registries.STRUCTURE_SET);
        for (var reservation : reservations) {
            var set = sets.getOptional(reservation.set()).orElseThrow(() ->
                    new IllegalStateException("Missing reserved structure set: " + reservation.set()));
            if (set.structures().isEmpty()) {
                continue; // World-specific disabling also releases the reservation.
            }
            if (!(set.placement() instanceof RandomSpreadStructurePlacement spread)) {
                throw new IllegalStateException("Reserved relic set must use random_spread: " + reservation.set());
            }
            int radius = reservation.clearanceChunks() + extra;
            if (candidateConflicts(spread, seed, cx, cz, radius, reservation.earlierOnly())) {
                return false;
            }
        }
        return true;
    }

    static boolean candidateConflicts(RandomSpreadStructurePlacement spread, long seed, int cx, int cz, int radius) {
        return candidateConflicts(spread, seed, cx, cz, radius, false);
    }

    static boolean candidateConflicts(RandomSpreadStructurePlacement spread, long seed, int cx, int cz, int radius,
            boolean earlierOnly) {
        int spacing = spread.spacing();
        for (int rx = Math.floorDiv(cx - radius, spacing); rx <= Math.floorDiv(cx + radius, spacing); rx++) {
            for (int rz = Math.floorDiv(cz - radius, spacing); rz <= Math.floorDiv(cz + radius, spacing); rz++) {
                var candidate = spread.getPotentialStructureChunk(seed, rx * spacing, rz * spacing);
                if (earlierOnly && !(candidate.x() < cx || (candidate.x() == cx && candidate.z() < cz))) {
                    continue; // Same-family ties are lexicographic; never reject ourselves or form a cycle.
                }
                if (Math.abs(candidate.x() - cx) <= radius && Math.abs(candidate.z() - cz) <= radius) {
                    return true;
                }
            }
        }
        return false;
    }

    @Override
    public MapCodec<? extends PlacementCondition> codec() {
        return CODEC;
    }
}
