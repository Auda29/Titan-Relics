package de.relics.client;
import com.terraformersmc.modmenu.api.ModMenuApi;
import com.terraformersmc.modmenu.api.ConfigScreenFactory;
import net.minecraft.client.gui.screens.Screen;
/** Loaded by Mod Menu only; no mandatory dependency or dedicated-server linkage. */
public final class RelicModMenu implements ModMenuApi {
    @Override public ConfigScreenFactory<? extends Screen> getModConfigScreenFactory(){return DistributionMenus::defaults;}
}
