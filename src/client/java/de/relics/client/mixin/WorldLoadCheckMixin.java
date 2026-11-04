package de.relics.client.mixin;

import de.relics.distribution.WorldLoadCheck;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.AlertScreen;
import net.minecraft.client.gui.screens.worldselection.WorldOpenFlows;
import net.minecraft.network.chat.Component;
import net.minecraft.server.WorldStem;
import net.minecraft.server.packs.repository.PackRepository;
import net.minecraft.world.level.storage.LevelResource;
import net.minecraft.world.level.storage.LevelStorageSource;
import org.spongepowered.asm.mixin.*;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(WorldOpenFlows.class)
public abstract class WorldLoadCheckMixin {
    @Inject(method="openWorldCheckWorldStemCompatibility",at=@At("HEAD"),cancellable=true)
    private void relics$preflight(LevelStorageSource.LevelStorageAccess storage,WorldStem stem,PackRepository packs,Runnable returnToMenu,CallbackInfo ci) {
        try {WorldLoadCheck.verify(storage.getLevelPath(LevelResource.ROOT),stem);}
        catch(WorldLoadCheck.Problem problem) {
            ci.cancel();
            WorldLoadCheck.closeRejected(stem,storage,problem);
            org.slf4j.LoggerFactory.getLogger("relics/world-load").warn("Relic world load rejected before saving: "+storage.getLevelId(),problem);
            Component message=Component.translatable("relics.load.world",storage.getLevelId())
                    .append("\n\n").append(Component.translatable("relics.load.reason."+problem.reason))
                    .append("\n\n").append(Component.translatable("relics.load.recovery"));
            Minecraft.getInstance().gui.setScreen(new AlertScreen(returnToMenu,Component.translatable("relics.load.title"),message));
        }
    }
}
