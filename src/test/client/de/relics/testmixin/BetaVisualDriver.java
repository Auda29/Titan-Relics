package de.relics.clientqa;

import net.minecraft.client.Minecraft;
import java.nio.file.*;
import com.google.gson.*;

/** Labelled renderer captures from explicit operator-prepared model fixtures. */
public final class BetaVisualDriver {
    private static JsonArray scenes;
    private static int index;
    private static long captureAt;
    private static long nextSceneAt;
    public static void tick(Minecraft c)throws Exception{
        if(System.currentTimeMillis()<nextSceneAt)return;
        if(scenes==null)scenes=JsonParser.parseString(Files.readString(Path.of("visual-cases.json"))).getAsJsonArray();
        if(index>=scenes.size()){Files.writeString(Path.of("visual-proof.txt"),"Captured "+index+" labelled scenes; requires human image review");c.stop();return;}
        var scene=scenes.get(index).getAsJsonObject();
        if(captureAt==0){
            if(scene.has("camera")){
                c.options.setCameraType(net.minecraft.client.CameraType.valueOf(scene.get("camera").getAsString()));

            }
            c.getSingleplayerServer().submit(()->{var s=c.getSingleplayerServer();for(var command:scene.getAsJsonArray("commands"))s.getCommands().performPrefixedCommand(s.createCommandSourceStack(),command.getAsString());return true;}).get();
            captureAt=System.currentTimeMillis()+scene.get("wait_ms").getAsLong();return;
        }
        if(System.currentTimeMillis()<captureAt)return;
        // Initial login/game-mode packets can reset the camera after scene setup.
        // Reapply it after the server commands, then allow a rendered frame to settle.
        if(scene.has("camera") && c.options.getCameraType()!=net.minecraft.client.CameraType.valueOf(scene.get("camera").getAsString())){
            c.options.setCameraType(net.minecraft.client.CameraType.valueOf(scene.get("camera").getAsString()));
            captureAt=System.currentTimeMillis()+500;return;
        }
        var state=new JsonObject();
        state.addProperty("label",scene.get("label").getAsString());
        state.addProperty("camera",c.options.getCameraType().name());
        state.addProperty("spectator",c.player.isSpectator());
        state.addProperty("x",c.player.getX());state.addProperty("y",c.player.getY());state.addProperty("z",c.player.getZ());
        Files.writeString(Path.of("visual-state.jsonl"),state.toString()+"\n",StandardOpenOption.CREATE,StandardOpenOption.APPEND);
        net.minecraft.client.Screenshot.grab(c,true);
        Files.writeString(Path.of("visual-actions.log"),System.currentTimeMillis()+" "+scene.get("label").getAsString()+"\n",StandardOpenOption.CREATE,StandardOpenOption.APPEND);
        index++;captureAt=0;nextSceneAt=System.currentTimeMillis()+2000;
    }
}
