package de.relics.client.mixin;

import de.relics.client.*;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.tabs.GridLayoutTab;
import net.minecraft.client.gui.screens.worldselection.CreateWorldScreen;
import net.minecraft.network.chat.Component;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(targets="net.minecraft.client.gui.screens.worldselection.CreateWorldScreen$WorldTab")
public abstract class WorldGenerationTabMixin extends GridLayoutTab {
    protected WorldGenerationTabMixin(){super(Component.empty());}
    @Inject(method="<init>",at=@At("TAIL"))
    private void relics$world(CreateWorldScreen owner,CallbackInfo ci) {
        var button=Button.builder(Component.translatable("relics.settings.world_button"),b->DistributionMenus.world(owner)).width(310).build();
        layout.addChild(button,3,0,1,2);
        owner.getUiState().addListener(state->button.active=state.isGenerateStructures() && !state.isDebug());
        button.active=owner.getUiState().isGenerateStructures() && !owner.getUiState().isDebug();
    }
}
