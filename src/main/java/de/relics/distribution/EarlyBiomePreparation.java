package de.relics.distribution;

import net.minecraft.core.RegistryAccess;
import java.util.Map;
import java.util.WeakHashMap;

/** Run Fabric's normal biome modifiers before preflight, once for these loaded registries. */
public final class EarlyBiomePreparation {
    private static final Map<RegistryAccess,Boolean> PREPARED=new WeakHashMap<>();
    private EarlyBiomePreparation() { }
    public static synchronized void prepare(RegistryAccess registries) {
        if(PREPARED.containsKey(registries))return;
        net.fabricmc.fabric.impl.biome.modification.BiomeModificationImpl.INSTANCE.finalizeWorldGen(registries);
        PREPARED.put(registries,Boolean.TRUE);
    }
    /** Consume only our early invocation. All other Fabric calls keep their original checks. */
    public static synchronized boolean consume(RegistryAccess registries){return PREPARED.remove(registries)!=null;}
    public static synchronized void discard(RegistryAccess registries){PREPARED.remove(registries);}
}
