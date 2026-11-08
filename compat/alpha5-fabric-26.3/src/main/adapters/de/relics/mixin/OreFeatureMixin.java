package de.relics.mixin;

import com.llamalad7.mixinextras.injector.wrapmethod.WrapMethod;
import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import de.relics.RelicProtection;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.feature.OreFeature;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import java.util.function.Function;

/** Ore writes go straight to chunk sections and bypass WorldGenRegion.setBlock. */
@Mixin(OreFeature.class)
public abstract class OreFeatureMixin {
    @WrapMethod(method = "doPlace")
    private boolean relics$oreContext(WorldGenLevel level, RandomSource random,
            double x1, double x2, double z1, double z2, double y1, double y2,
            int minX, int minY, int minZ, int width, int height, Operation<Boolean> original) {
        WorldGenLevel previous = RelicProtection.ORE_LEVEL.get();
        RelicProtection.ORE_LEVEL.set(level);
        try {
            return original.call(level, random, x1, x2, z1, z2, y1, y2, minX, minY, minZ, width, height);
        } finally {
            if (previous == null) {
                RelicProtection.ORE_LEVEL.remove();
            } else {
                RelicProtection.ORE_LEVEL.set(previous);
            }
        }
    }

}
