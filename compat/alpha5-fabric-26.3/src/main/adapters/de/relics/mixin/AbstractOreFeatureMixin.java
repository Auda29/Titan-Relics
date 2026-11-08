package de.relics.mixin;
import de.relics.RelicProtection;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.feature.AbstractOreFeature;
import net.minecraft.world.level.levelgen.feature.BlockReplacement;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import java.util.function.Function;
/** Ore veins write directly to chunk sections; reject protected cells in the shared predicate. */
@Mixin(AbstractOreFeature.class)
public abstract class AbstractOreFeatureMixin {
    @Inject(method="canPlaceOre",at=@At("HEAD"),cancellable=true)
    private void relics$exclude(BlockState state,Function<BlockPos,BlockState> getter,RandomSource random,
            BlockReplacement target,BlockPos.MutableBlockPos pos,CallbackInfoReturnable<Boolean> ci) {
        WorldGenLevel level=RelicProtection.ORE_LEVEL.get();
        if(level!=null && RelicProtection.protectedAt(level,pos))ci.setReturnValue(false);
    }
}
