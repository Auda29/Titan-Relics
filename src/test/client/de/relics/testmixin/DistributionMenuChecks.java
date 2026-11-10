package de.relics.testmixin;

import de.relics.client.*;
import net.minecraft.client.gui.screens.worldselection.CreateWorldScreen;
import net.minecraft.client.gui.components.tabs.TabNavigationBar;
import net.minecraft.world.level.storage.LevelResource;
import de.relics.distribution.*;
import net.minecraft.client.Minecraft;
import net.minecraft.client.Screenshot;
import net.minecraft.client.gui.components.*;
import net.minecraft.client.gui.screens.*;
import net.minecraft.client.gui.screens.options.OptionsScreen;
import net.minecraft.network.chat.Component;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import java.nio.file.*;
import java.util.*;

/** Isolated real-client probe, packaged only by test_distribution_client.py. */
@Mixin(Minecraft.class)
public abstract class DistributionMenuChecks {
    @Unique private Screen relics$screen;
    @Unique private CreateWorldScreen relics$creation;
    @Unique private int relics$ticks,relics$phase;
    @Unique private boolean relics$captured;
    @Unique private boolean relics$capture(Minecraft client) {
        if(relics$captured){relics$captured=false;return true;}
        Screenshot.grab(client,true);relics$captured=true;relics$phase--;return false;
    }
    @Unique private void relics$press(String key) {relics$pressLabel(Component.translatable(key).getString());}
    @Unique private void relics$pressLabel(String label) {
        Button button=relics$screen.children().stream().filter(Button.class::isInstance).map(Button.class::cast)
                .filter(b->b.getMessage().getString().equals(label)).findFirst().orElseThrow(()->new AssertionError("Missing "+label+" at phase "+relics$phase+" on "+relics$screen.getClass().getName()+" buttons "+relics$screen.children().stream().filter(Button.class::isInstance).map(Button.class::cast).map(b->b.getMessage().getString()).toList()));
        if(!button.active)throw new AssertionError("Inactive button: "+label);button.onPress(null);
        relics$screen=Minecraft.getInstance().gui.screen();
    }
    @Unique private List<EditBox> relics$fields(){return relics$screen.children().stream().filter(EditBox.class::isInstance).map(EditBox.class::cast).toList();}
    @Unique private void relics$check(boolean value,String message){if(!value)throw new AssertionError(message);}
    @Inject(method="tick",at=@At("TAIL"))
    private void relics$checkMenu(CallbackInfo ci) {
        if(!Boolean.getBoolean("relics.menuChecks"))return;
        var client=(Minecraft)(Object)this;
        org.lwjgl.glfw.GLFW.glfwHideWindow(client.getWindow().handle());
        if(++relics$ticks<150 || relics$ticks%30!=0)return;
        relics$screen=client.gui.screen();
        if(relics$phase==0 && !(relics$screen instanceof TitleScreen)) {
            if(relics$ticks>=300)client.gui.setScreen(new TitleScreen());
            return;
        }
        try {
            switch(relics$phase++) {
                case 0 -> {
                    relics$check(relics$screen.children().stream().filter(Button.class::isInstance).map(Button.class::cast).noneMatch(v->v.getMessage().getString().equals(Component.translatable("relics.settings.open").getString())),"No title button");
                    var parent=new OptionsScreen(relics$screen,client.options,false);client.gui.setScreen(parent);
                    relics$check(parent.children().stream().filter(Button.class::isInstance).map(Button.class::cast).noneMatch(v->v.getMessage().getString().equals(Component.translatable("relics.settings.open").getString())),"No options button");
                    if(Boolean.getBoolean("relics.menuChecks.modmenu")) {
                        var api=Class.forName("de.relics.client.RelicModMenu").getConstructor().newInstance();
                        var factory=api.getClass().getMethod("getModConfigScreenFactory").invoke(api);
                        client.gui.setScreen((Screen)Class.forName("com.terraformersmc.modmenu.api.ConfigScreenFactory").getMethod("create",Screen.class).invoke(factory,parent));
                    }else client.gui.setScreen(DistributionMenus.defaults(parent));
                }
                case 1 -> {
                    if(!(relics$screen instanceof DistributionSettingsScreen)){relics$phase--;return;}
                    relics$press("relics.settings.preset.balanced");relics$press("relics.settings.save");
                    relics$check(DistributionConfig.load().cellSize()==3000 && DistributionConfig.load().colossusMinDistance()==8000,"Mod-list defaults save density and Colossus distance");
                    Screen parent=relics$screen;CreateWorldScreen.openFresh(client,()->client.gui.setScreen(parent));
                }
                case 2 -> {
                    if(!(relics$screen instanceof CreateWorldScreen)){relics$phase--;return;}
                    relics$creation=(CreateWorldScreen)relics$screen;
                    relics$creation.getUiState().setName("Relic Settings Probe");relics$creation.getUiState().setSeed("731204");
                    relics$check(relics$screen.children().stream().filter(Button.class::isInstance).map(Button.class::cast).noneMatch(v->v.getMessage().getString().equals(Component.translatable("relics.settings.world_button").getString())),"Not on Game tab");
                    relics$creation.children().stream().filter(TabNavigationBar.class::isInstance).map(TabNavigationBar.class::cast).findFirst().orElseThrow().selectTab(1,false);
                }
                case 3 -> {if(relics$capture(client))relics$press("relics.settings.world_button");}
                case 4 -> {
                    if(!relics$capture(client))break;
                    relics$check(relics$fields().isEmpty(),"Simple view has no technical input fields");
                    relics$press("relics.settings.advanced");
                    relics$check(relics$fields().getFirst().getValue().equals("3000"),"New world inherits defaults");
                    relics$press("relics.settings.simple");relics$press("relics.settings.preset.discovery");
                    relics$press("relics.settings.advanced");
                    relics$check(relics$fields().size()==5 && relics$fields().get(4).getValue().equals("4000"),"Discoveries preset updates editable Colossus distance");
                    relics$fields().get(4).setValue("9000");
                    relics$press("relics.settings.simple");
                    relics$check(relics$screen.getNarrationMessage().getString().contains(Component.translatable("relics.settings.preset.custom").getString()),"Simple view identifies custom values");
                    relics$press("relics.settings.advanced");
                    relics$check(relics$fields().get(4).getValue().equals("9000"),"Switching views preserves unsaved custom edits");
                    relics$fields().getFirst().setValue("0");
                    relics$check(relics$screen.children().stream().filter(Button.class::isInstance).map(Button.class::cast).anyMatch(v->!v.active && v.getMessage().getString().equals(Component.translatable("relics.settings.apply").getString())),"Invalid input blocks Apply");
                    relics$fields().getFirst().setValue("2000");
                    for(int i=0;i<5;i++)relics$press("relics.settings.next");relics$press("relics.settings.biomes");
                    relics$press("relics.settings.mode.landscapes");relics$press("relics.settings.mode.custom");relics$fields().getFirst().setValue("minecraft:desert");
                }
                case 5 -> {if(relics$capture(client)){
                    String label=relics$screen.children().stream().filter(Button.class::isInstance).map(Button.class::cast).map(b->b.getMessage().getString()).filter(s->s.endsWith("minecraft:desert")).findFirst().orElseThrow();
                    relics$pressLabel(label);if(label.startsWith("[x]"))relics$pressLabel("[ ] minecraft:desert");relics$press("relics.settings.apply");
                }}
                case 6 -> {
                    relics$press("relics.settings.apply");var draft=((WorldDistributionDraft)relics$creation).relics$draft();
                    relics$check(draft.cellSize()==2000 && draft.biomes().rule(DistributionPlanner.Family.COLOSSUS).selected().contains("minecraft:desert"),"World draft contains density and biome edits");
                    relics$check(DistributionConfig.load().cellSize()==3000 && DistributionConfig.load().biomes().equals(BiomeRules.LANDSCAPES),"World edits never change defaults");
                    relics$press("relics.settings.world_button");relics$press("relics.settings.preset.expedition");relics$screen.onClose();
                    relics$check(((WorldDistributionDraft)relics$creation).relics$draft().cellSize()==2000,"Cancel preserves draft");
                    relics$screen=client.gui.screen();relics$press("selectWorld.create");
                }
                case 7 -> {
                    var server=client.getSingleplayerServer();if(server==null || client.level==null){relics$phase--;return;}
                    Path root=server.getWorldPath(LevelResource.ROOT),file=root.resolve("data/relics_distribution_v1.json");
                    if(!Files.exists(file)){relics$phase--;return;}var state=new DistributionJournal(file,null).state;if(!state.frozen){relics$phase--;return;}
                    relics$check(state.settings.cellSize()==2000 && state.settings.colossusMinDistance()==9000
                            && state.lower>=9000 && state.settings.biomes().rule(DistributionPlanner.Family.COLOSSUS).selected().contains("minecraft:desert"),"Actual world froze density, custom Colossus distance and biomes");
                    relics$check(DistributionConfig.read(root.resolve(DistributionConfig.WORLD_FILE)).equals(state.settings),"Creation handoff equals journal");
                    Files.writeString(Path.of("menu-world-path.txt"),root.toString());
                    client.gui.setScreen(DistributionMenus.defaults(new OptionsScreen(null,client.options,false)));
                }
                case 8 -> {
                    relics$check(relics$screen instanceof DistributionSettingsScreen,"Saved-world viewer");
                    relics$check(relics$screen.children().stream().filter(Button.class::isInstance).map(Button.class::cast).noneMatch(v->v.getMessage().getString().equals(Component.translatable("relics.settings.preset.discovery").getString())),"Saved-world presets read only");
                    relics$check(relics$fields().isEmpty(),"Saved world opens with a simple summary");
                    relics$press("relics.settings.advanced");relics$press("relics.settings.tab.diagnostics");
                }
                case 9 -> {if(relics$capture(client)){
                    Files.writeString(Path.of("menu-proof.txt"),"PASS world-generation tab; no title/options button; mod-list defaults; loaded biome registry; landscape/custom search; scoped Apply/Cancel; actual world creation; frozen density/biomes; read-only diagnostics\n");client.stop();
                }}
            }
        }catch(Throwable failure){
            try{Files.writeString(Path.of("menu-failure.txt"),failure.toString());}catch(Exception ignored){}
            throw new IllegalStateException("Distribution menu probe",failure);
        }
    }
}
