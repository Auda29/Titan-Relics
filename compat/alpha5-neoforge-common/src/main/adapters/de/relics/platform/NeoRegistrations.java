package de.relics.platform;

import net.minecraft.core.Registry;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.RegisterEvent;
import java.util.*;

/** Construct stable values first, then bind them in the matching native registry event. */
public final class NeoRegistrations {
    private record Pending<T>(ResourceKey<? extends Registry<T>> registry,ResourceLocation id,T value) { }
    private static final List<Pending<?>> PENDING=new ArrayList<>();
    private NeoRegistrations() { }
    public static <V,T extends V> T register(Registry<V> registry,ResourceLocation id,T value) {
        PENDING.add(new Pending<>(registry.key(),id,value));return value;
    }
    public static void initialize(IEventBus bus){bus.addListener((RegisterEvent event)->registerPending(event));}
    @SuppressWarnings({"rawtypes","unchecked"}) private static void registerPending(RegisterEvent event) {
        for(var pending:PENDING)if(event.getRegistryKey().equals(pending.registry()))
            event.register((ResourceKey)pending.registry(),pending.id(),()->pending.value());
    }
}
