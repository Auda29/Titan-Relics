package de.relics.mixin;

import de.relics.distribution.DistributionRuntime;
import net.minecraft.world.level.levelgen.structure.*;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(Structure.class)
public abstract class DistributionStructureMixin {
    @Inject(method="generate",at=@At("HEAD"),cancellable=true)
    private void relics$validatedStart(CallbackInfoReturnable<StructureStart> ci) {
        StructureStart start=DistributionRuntime.generate((Structure)(Object)this);
        if(start!=null)ci.setReturnValue(start);
    }
}
