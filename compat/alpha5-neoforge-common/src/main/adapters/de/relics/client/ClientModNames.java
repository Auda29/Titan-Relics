package de.relics.client;
import net.neoforged.fml.ModList;
public final class ClientModNames {
    private ClientModNames(){}
    public static String name(String id){return ModList.get().getModContainerById(id).map(m->m.getModInfo().getDisplayName()).orElse(id);}
}
