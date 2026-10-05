package de.relics.mixin;

import com.llamalad7.mixinextras.injector.wrapmethod.WrapMethod;
import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import de.relics.RelicProtection;
import de.relics.TerrainSupportProcessor;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import org.spongepowered.asm.mixin.Mixin;

@Mixin(StructureTemplate.class)
public abstract class StructureTemplateMixin {
    @WrapMethod(method = "placeInWorld")
    private boolean relics$allowOwnPlacement(ServerLevelAccessor level, BlockPos origin, BlockPos reference,
            StructurePlaceSettings settings, RandomSource random, int flags, Operation<Boolean> original) {
        boolean relic = settings.getProcessors().stream().anyMatch(TerrainSupportProcessor.class::isInstance);
        if (!relic) {
            return original.call(level, origin, reference, settings, random, flags);
        }
        int depth = RelicProtection.RELIC_PLACEMENT_DEPTH.get();
        RelicProtection.RELIC_PLACEMENT_DEPTH.set(depth + 1);
        try {
            return original.call(level, origin, reference, settings, random, flags);
        } finally {
            if (depth == 0) {
                RelicProtection.RELIC_PLACEMENT_DEPTH.remove();
            } else {
                RelicProtection.RELIC_PLACEMENT_DEPTH.set(depth);
            }
        }
    }
}
