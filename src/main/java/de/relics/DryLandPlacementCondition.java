package de.relics;

import com.mojang.serialization.MapCodec;
import dev.worldgen.lithostitched.api.worldgen.placementcondition.PlacementCondition;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.levelgen.Heightmap;

/** Compare actual base terrain and fluid surface, not an assumed sea-level cutoff. */
public final class DryLandPlacementCondition implements PlacementCondition {
    public static final DryLandPlacementCondition INSTANCE = new DryLandPlacementCondition();
    public static final MapCodec<DryLandPlacementCondition> CODEC = MapCodec.unit(INSTANCE);

    @Override
    public boolean test(Context context, BlockPos pos) {
        int surface = context.generator().getFirstFreeHeight(pos.getX(), pos.getZ(), Heightmap.Types.WORLD_SURFACE_WG,
                context.heightAccessor(), context.randomState());
        int solid = context.generator().getFirstFreeHeight(pos.getX(), pos.getZ(), Heightmap.Types.OCEAN_FLOOR_WG,
                context.heightAccessor(), context.randomState());
        return surface == solid;
    }

    @Override
    public MapCodec<? extends PlacementCondition> codec() {
        return CODEC;
    }
}
