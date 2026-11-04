package de.relics.testmixin;

import net.minecraft.client.gui.screens.worldselection.WorldOpenFlows;
import net.minecraft.server.WorldStem;
import net.minecraft.server.packs.repository.PackRepository;
import net.minecraft.world.level.storage.LevelStorageSource;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Cancel at vanilla's next screen boundary, after the production preflight has succeeded. */
@Mixin(WorldOpenFlows.class)
public abstract class WorldLoadCancelProbe {
    @Inject(method="openWorldCheckWorldStemCompatibility",at=@At(value="INVOKE",target="Lnet/minecraft/client/gui/screens/worldselection/WorldOpenFlows;openWorldLoadBundledResourcePack(Lnet/minecraft/world/level/storage/LevelStorageSource$LevelStorageAccess;Lnet/minecraft/server/WorldStem;Lnet/minecraft/server/packs/repository/PackRepository;Ljava/lang/Runnable;)V"),cancellable=true)
    private void relics$cancelPrepared(LevelStorageSource.LevelStorageAccess storage,WorldStem stem,PackRepository packs,Runnable returnToMenu,CallbackInfo ci) throws Exception {
        if(!Boolean.getBoolean("relics.loadChecks.cancelNext"))return;
        System.clearProperty("relics.loadChecks.cancelNext");
        stem.close();storage.close();
        long expected=Long.parseLong(System.getProperty("relics.loadChecks.previousSeed"));
        if(dev.worldgen.lithostitched.impl.LithostitchedInternalHooks.WORLD_SEED!=expected)
            throw new AssertionError("Cancelled preflight left Lithostitched's global seed changed");
        returnToMenu.run();ci.cancel();
    }
}
