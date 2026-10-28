package de.relics;

import de.relics.platform.*;
import de.relics.gameplay.*;
import de.relics.distribution.DistributionRuntime;
import dev.worldgen.lithostitched.api.registry.LithostitchedRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.registries.RegisterEvent;

@Mod("relics")
public final class RelicWorldgen {
    public static final net.minecraft.world.level.levelgen.structure.templatesystem.StructureProcessorType<TerrainSupportProcessor> TERRAIN_SUPPORT=()->TerrainSupportProcessor.CODEC;
    public RelicWorldgen(IEventBus modBus) {
        NeoAttachments.initialize(modBus);NeoRegistrations.initialize(modBus);NeoEvents.initialize(modBus);
        RelicItems.initialize();RelicGameplay.initialize();NaturalInteriors.initialize();DistributionRuntime.initialize();RelicProtection.initialize();
        modBus.addListener(this::register);
    }
    private void register(RegisterEvent event) {
        if(event.getRegistryKey().equals(Registries.ITEM))RelicItems.registerItems();
        event.register(Registries.STRUCTURE_PROCESSOR,ResourceLocation.fromNamespaceAndPath("relics","terrain_support"),()->TERRAIN_SUPPORT);
        event.register(LithostitchedRegistries.PLACEMENT_CONDITION_TYPE,ResourceLocation.fromNamespaceAndPath("relics","separated"),()->SeparatedPlacementCondition.CODEC);
        event.register(LithostitchedRegistries.PLACEMENT_CONDITION_TYPE,ResourceLocation.fromNamespaceAndPath("relics","all_grid"),()->AllGridPlacementCondition.CODEC);
        event.register(LithostitchedRegistries.PLACEMENT_CONDITION_TYPE,ResourceLocation.fromNamespaceAndPath("relics","dry_land"),()->DryLandPlacementCondition.CODEC);
    }
}
