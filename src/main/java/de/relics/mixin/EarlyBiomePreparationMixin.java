package de.relics.mixin;

import com.llamalad7.mixinextras.injector.wrapmethod.WrapMethod;
import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import de.relics.distribution.EarlyBiomePreparation;
import net.minecraft.core.RegistryAccess;
import org.spongepowered.asm.mixin.Mixin;

@Mixin(targets="net.fabricmc.fabric.impl.biome.modification.BiomeModificationImpl",remap=false)
public abstract class EarlyBiomePreparationMixin {
    @WrapMethod(method="finalizeWorldGen",remap=false)
    private void relics$prepared(RegistryAccess registries,Operation<Void> original) {
        if(!EarlyBiomePreparation.consume(registries))original.call(registries);
    }
}
