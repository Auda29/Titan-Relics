package de.relics.distribution;

import dev.worldgen.lithostitched.impl.LithostitchedInternalHooks;
import net.minecraft.core.RegistryAccess;
import java.util.*;

/** Run the pinned 1.7.2 registry/seed hooks before vanilla's first save. */
public final class EarlyLithostitchedPreparation {
    public record Inputs(RegistryAccess.Frozen registries,long seed) { }
    private static final ThreadLocal<Inputs> INPUTS=new ThreadLocal<>();
    private static final Map<RegistryAccess,Long> PREPARED=new WeakHashMap<>();
    private EarlyLithostitchedPreparation() { }
    public static Inputs inputs(){return INPUTS.get();}
    public static synchronized void prepare(RegistryAccess registries,long seed) {
        if(PREPARED.containsKey(registries)) {
            if(PREPARED.get(registries)!=seed)throw new IllegalStateException("Prepared registries have a different seed");
            return;
        }
        if(INPUTS.get()!=null)throw new IllegalStateException("Nested Lithostitched preflight");
        INPUTS.set(new Inputs((RegistryAccess.Frozen)registries,seed));
        try {LithostitchedInternalHooks.onServerAboutToStart(null);PREPARED.put(registries,seed);}
        finally {INPUTS.remove();}
    }
    public static synchronized boolean consume(RegistryAccess registries,long seed) {
        Long prepared=PREPARED.remove(registries);
        if(prepared==null)return false;
        if(prepared!=seed)throw new IllegalStateException("Server seed changed after preflight");
        return true;
    }
    public static synchronized void discard(RegistryAccess registries){PREPARED.remove(registries);}
}
