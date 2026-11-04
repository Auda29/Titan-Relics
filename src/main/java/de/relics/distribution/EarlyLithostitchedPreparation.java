package de.relics.distribution;

import dev.worldgen.lithostitched.Lithostitched;
import dev.worldgen.lithostitched.impl.LithostitchedInternalHooks;
import net.minecraft.core.RegistryAccess;
import net.minecraft.core.registries.Registries;
import java.util.*;

/** Lithostitched's seed-dependent modifiers normally run after the first vanilla save. */
public final class EarlyLithostitchedPreparation {
    private record Prepared(long seed,long previousSeed) { }
    private static final Map<RegistryAccess,Prepared> PREPARED=new WeakHashMap<>();
    private EarlyLithostitchedPreparation() { }
    public static synchronized void prepare(RegistryAccess registries,long seed) {
        if(PREPARED.containsKey(registries)) {
            if(PREPARED.get(registries).seed()!=seed)throw new IllegalStateException("Prepared registries have a different seed");
            return;
        }
        long previous=LithostitchedInternalHooks.WORLD_SEED;
        try {
            LithostitchedInternalHooks.applyModifiersAndInjections(registries,Lithostitched.registry(registries,Registries.LEVEL_STEM),seed);
            PREPARED.put(registries,new Prepared(seed,previous));
        }catch(RuntimeException error){LithostitchedInternalHooks.WORLD_SEED=previous;throw error;}
    }
    public static synchronized boolean consume(RegistryAccess registries,long seed) {
        Prepared prepared=PREPARED.remove(registries);
        if(prepared==null)return false;
        if(prepared.seed()!=seed)throw new IllegalStateException("Server seed changed after preflight");
        return true;
    }
    public static synchronized void discard(RegistryAccess registries) {
        Prepared prepared=PREPARED.remove(registries);
        if(prepared!=null)LithostitchedInternalHooks.WORLD_SEED=prepared.previousSeed();
    }
}
