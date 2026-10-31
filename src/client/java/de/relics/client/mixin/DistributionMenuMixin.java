package de.relics.client.mixin;

import de.relics.client.DistributionSettingsScreen;

import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.TitleScreen;
import net.minecraft.client.gui.screens.options.OptionsScreen;
import net.minecraft.network.chat.Component;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin({TitleScreen.class,OptionsScreen.class})
public abstract class DistributionMenuMixin extends Screen {
    protected DistributionMenuMixin(Component title){super(title);}
    @Inject(method="init",at=@At("TAIL"))
    private void relics$settings(CallbackInfo ci) {
        addRenderableWidget(Button.builder(Component.translatable("relics.settings.open"),
                button->minecraft.gui.setScreen(new DistributionSettingsScreen((Screen)(Object)this)))
                .bounds(8,8,126,20).build());
    }
}
