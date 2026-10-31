package de.relics.platform.client;
import de.relics.client.DistributionMenus;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.ModContainer;
import net.neoforged.neoforge.client.gui.IConfigScreenFactory;
@Mod(value="relics",dist=Dist.CLIENT)
public final class RelicClient {
    public RelicClient(ModContainer container){container.registerExtensionPoint(IConfigScreenFactory.class,(mod,parent)->DistributionMenus.defaults(parent));}
}
