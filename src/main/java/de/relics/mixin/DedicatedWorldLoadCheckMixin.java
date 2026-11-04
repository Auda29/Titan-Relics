package de.relics.mixin;

import com.llamalad7.mixinextras.sugar.Local;
import de.relics.distribution.WorldLoadCheck;
import net.minecraft.server.Main;
import net.minecraft.server.WorldStem;
import net.minecraft.world.level.storage.LevelResource;
import net.minecraft.world.level.storage.LevelStorageSource;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(Main.class)
public abstract class DedicatedWorldLoadCheckMixin {
    @Inject(method="main",at=@At(value="INVOKE",target="Lnet/minecraft/server/WorldStem;registries()Lnet/minecraft/core/LayeredRegistryAccess;"),cancellable=true)
    private static void relics$preflight(String[] args,CallbackInfo ci,@Local WorldStem stem,@Local LevelStorageSource.LevelStorageAccess storage,
            @Local net.minecraft.server.dedicated.DedicatedServerSettings settings) {
        try {WorldLoadCheck.verify(storage.getLevelPath(LevelResource.ROOT),stem,settings.getProperties().maxWorldSize);}
        catch(WorldLoadCheck.Problem problem) {
            ci.cancel();
            WorldLoadCheck.closeRejected(stem,storage,problem);
            org.slf4j.LoggerFactory.getLogger("relics/world-load").error("Relic world load rejected before saving: "+storage.getLevelId()
                    +". Restore the original mods, datapacks and generator; keep the world and relic journal. Reason="+problem.reason,problem);
        }
    }
}
