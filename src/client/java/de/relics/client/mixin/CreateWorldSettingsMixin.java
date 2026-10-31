package de.relics.client.mixin;

import de.relics.client.*;
import de.relics.distribution.*;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.worldselection.CreateWorldScreen;
import net.minecraft.world.level.storage.LevelResource;
import net.minecraft.world.level.storage.LevelStorageSource;
import org.spongepowered.asm.mixin.*;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.*;
import com.llamalad7.mixinextras.injector.wrapoperation.*;
import java.nio.file.Path;
import java.util.Optional;

@Mixin(CreateWorldScreen.class)
public abstract class CreateWorldSettingsMixin implements WorldDistributionDraft {
    @Unique private DistributionSettings relics$settings;
    @Override public DistributionSettings relics$draft(){if(relics$settings==null)relics$settings=DistributionConfig.load();return relics$settings;}
    @Override public void relics$draft(DistributionSettings value){relics$settings=value;}
    @Inject(method="init",at=@At("HEAD"),cancellable=true)
    private void relics$defaults(CallbackInfo ci){
        var self=(CreateWorldScreen)(Object)this;
        if(DistributionMenus.completeDefaults(self))ci.cancel();
    }
    @Unique private void relics$write(Optional<LevelStorageSource.LevelStorageAccess> result) {
        result.ifPresent(access->DistributionConfig.write(access.getLevelPath(LevelResource.ROOT).resolve(DistributionConfig.WORLD_FILE),relics$draft()));
    }
    // WORLD_WRITE_BEGIN
    @WrapOperation(method="createNewWorld",at=@At(value="INVOKE",target="Lnet/minecraft/client/gui/screens/worldselection/CreateWorldScreen;createNewWorldDirectory(Lnet/minecraft/client/Minecraft;Ljava/lang/String;Ljava/nio/file/Path;)Ljava/util/Optional;"))
    private Optional<LevelStorageSource.LevelStorageAccess> relics$create(Minecraft client,String folder,Path packs,Operation<Optional<LevelStorageSource.LevelStorageAccess>> original) {
        var result=original.call(client,folder,packs);relics$write(result);return result;
    }
    // WORLD_WRITE_END
}
