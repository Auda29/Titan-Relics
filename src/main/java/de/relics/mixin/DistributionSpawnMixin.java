package de.relics.mixin;

import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import com.llamalad7.mixinextras.injector.wrapoperation.WrapOperation;
import de.relics.distribution.DistributionRuntime;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.progress.LevelLoadListener;
import net.minecraft.world.level.storage.ServerLevelData;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(MinecraftServer.class)
public abstract class DistributionSpawnMixin {
    @WrapOperation(method="createLevels",at=@At(value="INVOKE",target="Lnet/minecraft/server/MinecraftServer;setInitialSpawn(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/level/storage/ServerLevelData;ZZLnet/minecraft/server/level/progress/LevelLoadListener;)V"))
    private void relics$initialSpawn(ServerLevel level,ServerLevelData data,boolean bonus,boolean debug,LevelLoadListener listener,Operation<Void> original) {
        if(!debug && level.getServer().getWorldGenSettings().options().generateStructures())DistributionRuntime.attach(level,true);
        original.call(level,data,bonus,debug,listener);
        DistributionRuntime.finishSpawn(level);
    }
    @Inject(method="prepareLevels",at=@At("HEAD"))
    private void relics$loadPlanning(CallbackInfo ci) {
        DistributionRuntime.attach(((MinecraftServer)(Object)this).overworld(),false);
    }
}
