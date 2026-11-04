package de.relics.testmixin;

import de.relics.distribution.*;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.*;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.storage.LevelResource;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import java.nio.file.*;
import java.util.*;

/** Exercises vanilla's real open-world flow twice, then restores and loads the same copied save. */
@Mixin(Minecraft.class)
public abstract class WorldLoadClientChecks {
    @Unique private int relics$ticks,relics$phase,relics$returns;
    @Unique private Map<String,String> relics$before;
    @Unique private Path relics$root(){return Path.of("saves/guard-world");}
    @Unique private Map<String,String> relics$hashes() throws Exception {
        var result=new TreeMap<String,String>();
        try(var walk=Files.walk(relics$root())) {
            for(var path:walk.filter(Files::isRegularFile).toList())if(!path.getFileName().toString().equals("session.lock"))
                result.put(relics$root().relativize(path).toString(),HexFormat.of().formatHex(java.security.MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(path))));
        }
        return result;
    }
    @Unique private void relics$check(boolean value,String detail){if(!value)throw new AssertionError(detail);}
    @Unique private void relics$open(Minecraft client) {
        client.createWorldOpenFlows().openWorld("guard-world",()->{relics$returns++;client.gui.setScreen(new TitleScreen());});
    }
    @Inject(method="tick",at=@At("TAIL"))
    private void relics$loadCheck(CallbackInfo ci) {
        if(!Boolean.getBoolean("relics.worldLoadChecks"))return;
        var client=(Minecraft)(Object)this;
        org.lwjgl.glfw.GLFW.glfwHideWindow(client.getWindow().handle());
        if(++relics$ticks<150 || relics$ticks%20!=0)return;
        var screen=client.gui.screen();
        try {
            if(relics$phase==0) {
                if(!(screen instanceof TitleScreen)){if(relics$ticks>300)client.gui.setScreen(new TitleScreen());return;}
                relics$before=relics$hashes();relics$phase=1;relics$open(client);return;
            }
            if(relics$phase==1 || relics$phase==3) {
                if(!(screen instanceof AlertScreen))return;
                relics$check(screen.getTitle().getString().equals(Component.translatable("relics.load.title").getString()),"Expected the localized Relic load error");
                relics$check(client.getSingleplayerServer()==null && client.level==null,"Rejected world started an integrated server");
                relics$check(relics$hashes().equals(relics$before),"A rejected load changed world files");
                if(relics$phase==1)net.minecraft.client.Screenshot.grab(client,true);
                try(var access=client.getLevelSource().createAccess("guard-world")) {
                    relics$check(access.getLevelPath(LevelResource.ROOT).toAbsolutePath().normalize().equals(relics$root().toAbsolutePath().normalize()),"Reopened wrong world lock");
                }
                Button button=screen.children().stream().filter(Button.class::isInstance).map(Button.class::cast).findFirst().orElseThrow();
                relics$check(button.active,"Return button is inactive");button.onPress(null);
                relics$check(client.gui.screen() instanceof TitleScreen,"Did not return to menu");
                relics$phase++;return;
            }
            if(relics$phase==2) {relics$phase=3;relics$open(client);return;}
            if(relics$phase==4) {
                relics$check(relics$returns==2,"Return callback count differs");
                Files.copy(Path.of("original-journal.json"),relics$root().resolve(WorldLoadCheck.JOURNAL),StandardCopyOption.REPLACE_EXISTING);
                relics$before=relics$hashes();
                System.setProperty("relics.loadChecks.cancelNext","true");
                System.setProperty("relics.loadChecks.previousSeed",Long.toString(dev.worldgen.lithostitched.impl.LithostitchedInternalHooks.WORLD_SEED));
                relics$phase=5;relics$open(client);return;
            }
            if(relics$phase==5 && screen instanceof TitleScreen && relics$returns==3) {
                relics$check(relics$hashes().equals(relics$before),"Cancelling a successful preflight changed world files");
                try(var access=client.getLevelSource().createAccess("guard-world")) { }
                relics$phase=6;relics$open(client);return;
            }
            if(relics$phase==6 && client.level!=null && client.getSingleplayerServer()!=null) {
                String expected=Files.readString(Path.of("original-journal.json"));
                relics$check(Files.readString(relics$root().resolve(WorldLoadCheck.JOURNAL)).equals(expected),"Restored plan changed after loading");
                Files.writeString(Path.of("world-load-proof.txt"),"PASS two real rejected client loads; localized error; all world files unchanged except transient session.lock; lock reacquired; menu callbacks; successful preflight cancelled without writes; global seed restored; restored same world; journal byte-identical\n");
                relics$phase=7;client.stop();
            }
        }catch(Throwable error) {
            try{Files.writeString(Path.of("world-load-failure.txt"),"phase="+relics$phase+" "+error);}catch(Exception ignored){}
            throw new IllegalStateException("Real world-load client probe",error);
        }
    }
}
