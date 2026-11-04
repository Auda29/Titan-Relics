package de.relics.mixin;

import com.llamalad7.mixinextras.injector.wrapmethod.WrapMethod;
import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import de.relics.distribution.EarlyLithostitchedPreparation;
import net.minecraft.core.Registry;
import net.minecraft.core.RegistryAccess;
import net.minecraft.world.level.dimension.LevelStem;
import org.spongepowered.asm.mixin.Mixin;

@Mixin(targets="dev.worldgen.lithostitched.impl.LithostitchedInternalHooks",remap=false)
public abstract class EarlyLithostitchedPreparationMixin {
    @WrapMethod(method="applyModifiersAndInjections",remap=false)
    private static void relics$prepared(RegistryAccess registries,Registry<LevelStem> dimensions,long seed,Operation<Void> original) {
        if(!EarlyLithostitchedPreparation.consume(registries,seed))original.call(registries,dimensions,seed);
    }
}
