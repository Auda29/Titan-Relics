package de.relics.mixin;
import com.llamalad7.mixinextras.injector.wrapoperation.*;
import de.relics.distribution.EarlyLithostitchedPreparation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
/** Lithostitched 2.0.6 fetches an unused level local. Preflight has a stem, no running server. */
@Mixin(targets="dev.worldgen.lithostitched.impl.worldgen.biomeinjector.internal.BiomeInjectorManager")
public abstract class LithostitchedPreflightLevelMixin {
    @WrapOperation(method="applyBiomeInjectors",at=@At(value="INVOKE",target="Lnet/minecraft/server/MinecraftServer;getLevel(Lnet/minecraft/resources/ResourceKey;)Lnet/minecraft/server/level/ServerLevel;"))
    private static ServerLevel relics$unusedLevel(MinecraftServer server,ResourceKey<Level> key,Operation<ServerLevel> original) {
        return EarlyLithostitchedPreparation.preparing()?null:original.call(server,key);
    }
}
