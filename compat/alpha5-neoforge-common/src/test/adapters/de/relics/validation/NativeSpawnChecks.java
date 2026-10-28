package de.relics.validation;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.living.FinalizeSpawnEvent;

/** Verify that a native mod cancellation reaches the production extra-spawn path. */
public final class NativeSpawnChecks {
    public static boolean cancel;
    public static int cancelled;
    private NativeSpawnChecks() { }
    public static void initialize() {
        NeoForge.EVENT_BUS.addListener((FinalizeSpawnEvent event)->{
            if(cancel){event.setSpawnCancelled(true);cancelled++;}
        });
    }
}
