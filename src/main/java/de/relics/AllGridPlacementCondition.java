package de.relics;

import com.mojang.serialization.Codec;
import com.mojang.serialization.DataResult;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import dev.worldgen.lithostitched.api.worldgen.placementcondition.PlacementCondition;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.core.QuartPos;
import net.minecraft.world.level.levelgen.Heightmap;

/** Exact all-points grid with early rejection, rather than counting every failed site. */
public record AllGridPlacementCondition(int radius, int distance, int allowedCount,
        PlacementCondition condition) implements PlacementCondition {
    public static final MapCodec<AllGridPlacementCondition> CODEC = RecordCodecBuilder
            .<AllGridPlacementCondition>mapCodec(instance -> instance.group(
                    Codec.intRange(1, 128).fieldOf("radius").forGetter(AllGridPlacementCondition::radius),
                    Codec.intRange(1, 128).fieldOf("distance_between_points").forGetter(AllGridPlacementCondition::distance),
                    Codec.intRange(1, 10000).fieldOf("allowed_count").forGetter(AllGridPlacementCondition::allowedCount),
                    PlacementCondition.BASE_CODEC.fieldOf("condition").forGetter(AllGridPlacementCondition::condition)
            ).apply(instance, AllGridPlacementCondition::new)).validate(grid -> {
                int side = 2 * grid.radius / grid.distance + 1;
                return grid.allowedCount == side * side ? DataResult.success(grid)
                        : DataResult.error(() -> "all_grid must require every sample");
            });

    @Override
    public boolean test(Context context, BlockPos pos) {
        boolean debug = ((pos.getX() >> 4) + "," + (pos.getZ() >> 4))
                .equals(System.getProperty("relics.debugTerrainChunk"));
        for (int x = pos.getX() - radius; x <= pos.getX() + radius; x += distance) {
            for (int z = pos.getZ() - radius; z <= pos.getZ() + radius; z += distance) {
                BlockPos sample = new BlockPos(x, pos.getY(), z);
                if (!condition.test(context, sample)) {
                    if (debug) {
                        int surface = context.generator().getFirstFreeHeight(x, z, Heightmap.Types.WORLD_SURFACE_WG,
                                context.heightAccessor(), context.randomState());
                        int floor = context.generator().getFirstFreeHeight(x, z, Heightmap.Types.OCEAN_FLOOR_WG,
                                context.heightAccessor(), context.randomState());
                        var biome = context.biomeSource().getNoiseBiome(QuartPos.fromBlock(x), QuartPos.fromBlock(pos.getY()),
                                QuartPos.fromBlock(z), context.randomState().sampler());
                        System.out.println("Relic terrain sample rejected: " + sample + " centerY=" + pos.getY()
                                + " surface=" + surface + " floor=" + floor + " biome="
                                + context.registries().lookupOrThrow(Registries.BIOME).getKey(biome.value()));
                    }
                    return false;
                }
            }
        }
        return true;
    }

    @Override
    public MapCodec<? extends PlacementCondition> codec() {
        return CODEC;
    }
}
