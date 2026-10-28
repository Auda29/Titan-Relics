package de.relics.testmixin;
import net.minecraft.client.Minecraft;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
@Mixin(Minecraft.class)
public abstract class FingerprintClientStop {
    @Unique private int relics$probeTicks;
    @Inject(method="tick",at=@At("TAIL"))
    private void relics$finish(CallbackInfo ci) {
        var client=(Minecraft)(Object)this;
        if(Boolean.getBoolean("relics.capturePlanningFingerprint") && client.level!=null
                && java.nio.file.Files.exists(java.nio.file.Path.of("planning-signature.json")) && ++relics$probeTicks>=100)client.stop();
    }
}
