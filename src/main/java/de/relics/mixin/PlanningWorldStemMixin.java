package de.relics.mixin;

import de.relics.distribution.EarlyBiomePreparation;
import de.relics.distribution.EarlyLithostitchedPreparation;
import net.minecraft.server.WorldStem;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Vanilla can cancel at its backup/resource-pack screens after a successful preflight. */
@Mixin(WorldStem.class)
public abstract class PlanningWorldStemMixin {
    @Inject(method="close",at=@At("HEAD"))
    private void relics$discardPreparation(CallbackInfo ci) {
        var registries=((WorldStem)(Object)this).registries().compositeAccess();
        EarlyBiomePreparation.discard(registries);
        EarlyLithostitchedPreparation.discard(registries);
    }
}
