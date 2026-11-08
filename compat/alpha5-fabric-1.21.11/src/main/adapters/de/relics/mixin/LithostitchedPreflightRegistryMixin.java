package de.relics.mixin;
import com.llamalad7.mixinextras.injector.wrapoperation.*;
import de.relics.distribution.EarlyLithostitchedPreparation;
import net.minecraft.core.RegistryAccess;
import net.minecraft.server.MinecraftServer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
/** These pinned hooks read only the server registry access; use the identical frozen stem during preflight. */
@Mixin(targets={"dev.worldgen.lithostitched.impl.LithostitchedInternalHooks",
    "dev.worldgen.lithostitched.impl.worldgen.modifier.ModifierManager",
    "dev.worldgen.lithostitched.worldgen.surface.SurfaceRuleManager",
    "dev.worldgen.lithostitched.impl.worldgen.biomeinjector.internal.BiomeInjectorManager"})
public abstract class LithostitchedPreflightRegistryMixin {
    @WrapOperation(method="*",at=@At(value="INVOKE",target="Lnet/minecraft/server/MinecraftServer;registryAccess()Lnet/minecraft/core/RegistryAccess$Frozen;"))
    private static RegistryAccess.Frozen relics$registries(MinecraftServer server,Operation<RegistryAccess.Frozen> original) {
        var inputs=EarlyLithostitchedPreparation.inputs();return inputs==null?original.call(server):inputs.registries();
    }
}
