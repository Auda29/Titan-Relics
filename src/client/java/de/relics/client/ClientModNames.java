package de.relics.client;
import net.fabricmc.loader.api.FabricLoader;
public final class ClientModNames {
    private ClientModNames(){}
    public static String name(String id){return FabricLoader.getInstance().getModContainer(id).map(m->m.getMetadata().getName()).orElse(id);}
}
