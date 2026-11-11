package de.relics.client;

import de.relics.distribution.*;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.worldselection.CreateWorldScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.storage.LevelResource;
import java.nio.file.*;
import java.util.*;

/** Client-only routing. Drafts belong to their creation screen, never global defaults. */
public final class DistributionMenus {
    private static Screen defaultsParent;
    private DistributionMenus(){}
    public static void world(CreateWorldScreen owner) {
        var draft=(WorldDistributionDraft)owner;
        DistributionSettings initial;boolean error=false;try{initial=draft.relics$draft();}catch(RuntimeException failure){initial=DistributionSettings.EXPEDITION;error=true;}
        var screen=new DistributionSettingsScreen(owner,initial,draft::relics$draft,
                ClientBiomeCatalog.from(owner.getUiState().getSettings().worldgenLoadContext()),"scope.world",Map.of());
        if(error)screen.loadError();Minecraft.getInstance().gui.setScreen(screen);
    }
    public static Screen defaults(Screen parent) {
        var client=Minecraft.getInstance();
        if(client.level!=null) {
            var server=client.getSingleplayerServer();DistributionSettings saved=null;Map<String,Long> diagnostic=Map.of();
            if(server!=null) {
                Path file=server.getWorldPath(LevelResource.ROOT).resolve("data/relics_distribution_v1.json");
                if(Files.exists(file)){var state=new DistributionJournal(file,null).state;saved=state.settings==null?DistributionSettings.LEGACY_EXPEDITION:state.settings;}
                var runtime=DistributionRuntime.get(server.overworld());if(runtime!=null)diagnostic=runtime.diagnostics();
            }
            if(saved==null)return new UnavailableSettingsScreen(parent);
            return new DistributionSettingsScreen(parent,saved,null,
                    ClientBiomeCatalog.from(client.level.registryAccess()),saved==null?"scope.unavailable":"scope.saved",diagnostic);
        }
        return new DefaultsLoadingScreen(parent);
    }
    public static boolean completeDefaults(CreateWorldScreen creation) {
        if(defaultsParent==null)return false;
        Screen parent=defaultsParent;defaultsParent=null;
        var catalog=ClientBiomeCatalog.from(creation.getUiState().getSettings().worldgenLoadContext());
        DistributionSettings initial;boolean error=false;try{initial=DistributionConfig.load();}catch(RuntimeException failure){initial=DistributionSettings.EXPEDITION;error=true;}
        var screen=new DistributionSettingsScreen(parent,initial,DistributionConfig::save,catalog,"scope.defaults",Map.of());
        if(error)screen.loadError();Minecraft.getInstance().gui.setScreen(screen);
        return true;
    }
    private static final class DefaultsLoadingScreen extends Screen {
        private final Screen parent;private boolean started;
        private DefaultsLoadingScreen(Screen parent){super(Component.translatable("relics.settings.loading"));this.parent=parent;}
        @Override protected void init(){if(!started){started=true;defaultsParent=parent;CreateWorldScreen.openFresh(minecraft,()->minecraft.gui.setScreen(parent));}}
        @Override public void onClose(){defaultsParent=null;minecraft.gui.setScreen(parent);}
    }
    private static final class UnavailableSettingsScreen extends Screen {
        private final Screen parent;
        private UnavailableSettingsScreen(Screen parent){super(Component.translatable("relics.settings.scope.unavailable"));this.parent=parent;}
        @Override protected void init(){addRenderableWidget(net.minecraft.client.gui.components.Button.builder(Component.translatable("gui.done"),b->onClose()).bounds(width/2-100,height-28,200,20).build());}
        @Override public void onClose(){minecraft.gui.setScreen(parent);}
        @Override public void extractRenderState(net.minecraft.client.gui.GuiGraphicsExtractor graphics,int mouseX,int mouseY,float delta){
            super.extractRenderState(graphics,mouseX,mouseY,delta);graphics.centeredText(font,title,width/2,20,0xffffffff);
            graphics.textWithWordWrap(font,Component.translatable("relics.settings.server_unavailable"),20,60,width-40,0xffcccccc);
        }
    }
}
