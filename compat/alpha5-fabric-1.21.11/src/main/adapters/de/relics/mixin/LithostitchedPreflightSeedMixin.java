package de.relics.mixin;
import de.relics.distribution.EarlyLithostitchedPreparation;
import net.minecraft.server.MinecraftServer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
@Mixin(targets="dev.worldgen.lithostitched.impl.LithostitchedVersion",remap=false)
public abstract class LithostitchedPreflightSeedMixin {
    @Inject(method="getSeed",at=@At("HEAD"),cancellable=true,remap=false)
    private static void relics$seed(MinecraftServer server,CallbackInfoReturnable<Long> ci) {
        var inputs=EarlyLithostitchedPreparation.inputs();if(inputs!=null)ci.setReturnValue(inputs.seed());
    }
}
