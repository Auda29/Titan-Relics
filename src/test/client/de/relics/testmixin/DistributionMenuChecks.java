package de.relics.testmixin;

import de.relics.client.DistributionSettingsScreen;
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
    @Unique private int relics$ticks,relics$phase;
    @Unique private boolean relics$captured;
    @Unique private boolean relics$capture(Minecraft client) {
        if(relics$captured){relics$captured=false;return true;}
        Screenshot.grab(client,true);relics$captured=true;relics$phase--;return false;
    }
    @Unique private void relics$press(String key) {
        Button button=relics$screen.children().stream().filter(Button.class::isInstance).map(Button.class::cast)
                .filter(b->b.getMessage().getString().equals(Component.translatable(key).getString())).findFirst().orElseThrow();
        if(!button.active)throw new AssertionError("Inactive button: "+key);button.onPress(null);
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
                case 0 -> {relics$check(relics$screen instanceof TitleScreen,"Title screen ready");relics$press("relics.settings.open");}
                case 1 -> {
                    relics$check(relics$screen instanceof DistributionSettingsScreen,"Title button opens menu");
                    relics$press("relics.settings.preset.discovery");
                    relics$check(relics$fields().getFirst().getValue().equals("2000"),"Preset fills fields");
                    relics$fields().getFirst().setValue("0");
                    relics$check(relics$screen.children().stream().filter(Button.class::isInstance).map(Button.class::cast)
                            .anyMatch(b->!b.active && b.getMessage().getString().equals(Component.translatable("relics.settings.save").getString())),"Invalid input disables save");
                    relics$screen.onClose();relics$check(!Files.exists(DistributionConfig.file()),"Cancel writes nothing");
                    client.gui.setScreen(new OptionsScreen(client.gui.screen(),client.options,false));
                }
                case 2 -> relics$press("relics.settings.open");
                case 3 -> {relics$check(relics$screen instanceof DistributionSettingsScreen,"Options button opens menu");relics$press("relics.settings.preset.discovery");}
                case 4 -> {if(relics$capture(client))relics$press("relics.settings.next");}
                case 5 -> {relics$fields().get(0).setValue("25");relics$fields().get(1).setValue("3,25");}
                case 6 -> {if(relics$capture(client))relics$press("relics.settings.next");}
                case 7 -> {relics$fields().get(2).setValue("5");relics$press("relics.settings.next");}
                case 8 -> {
                    relics$check(relics$fields().get(0).getValue().equals("25"),"Obelisk chance synchronized across pages");
                    if(relics$capture(client))relics$press("relics.settings.next");
                }
                case 9 -> relics$press("relics.settings.save");
                case 10 -> {
                    relics$check(relics$screen instanceof OptionsScreen,"Save returns to parent");var saved=DistributionConfig.load();
                    relics$check(saved.cellSize()==2000 && saved.outside().get(0)==2500 && saved.inside().get(0)==2500
                            && saved.outside().get(1)==325 && saved.outside().get(5)==500,"Preset plus edits persisted");
                    relics$press("relics.settings.open");
                }
                case 11 -> {
                    relics$check(relics$fields().getFirst().getValue().equals("2000"),"Reopening reads saved values");
                    String before=Files.readString(DistributionConfig.file());relics$press("relics.settings.preset.expedition");
                    relics$screen.onClose();relics$check(Files.readString(DistributionConfig.file()).equals(before),"Cancel preserves existing config");
                    Files.writeString(Path.of("menu-proof.txt"),"PASS title/options; presets; invalid input; all five pages; decimal percentages; synced Obelisk chance; save/reopen; cancel preserves file\n");
                    client.stop();
                }
            }
        }catch(Throwable failure){
            try{Files.writeString(Path.of("menu-failure.txt"),failure.toString());}catch(Exception ignored){}
            throw new IllegalStateException("Distribution menu probe",failure);
        }
    }
}
