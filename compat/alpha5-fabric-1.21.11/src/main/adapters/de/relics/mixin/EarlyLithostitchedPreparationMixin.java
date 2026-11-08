package de.relics.mixin;
import com.llamalad7.mixinextras.injector.wrapmethod.WrapMethod;
import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import de.relics.distribution.EarlyLithostitchedPreparation;
import dev.worldgen.lithostitched.impl.LithostitchedVersion;
import net.minecraft.server.MinecraftServer;
import org.spongepowered.asm.mixin.Mixin;
@Mixin(targets="dev.worldgen.lithostitched.impl.LithostitchedInternalHooks",remap=false)
public abstract class EarlyLithostitchedPreparationMixin {
    @WrapMethod(method="onServerAboutToStart",remap=false)
    private static void relics$prepared(MinecraftServer server,Operation<Void> original) {
        if(EarlyLithostitchedPreparation.inputs()!=null || !EarlyLithostitchedPreparation.consume(server.registryAccess(),LithostitchedVersion.getSeed(server)))original.call(server);
    }
}
