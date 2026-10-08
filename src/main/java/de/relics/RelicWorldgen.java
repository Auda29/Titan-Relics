package de.relics;

import com.mojang.serialization.MapCodec;
import dev.worldgen.lithostitched.api.registry.LithostitchedRegistries;
import dev.worldgen.lithostitched.api.worldgen.placementcondition.PlacementCondition;
import net.fabricmc.api.ModInitializer;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;

/** Placement infrastructure only; no gameplay, ticks or changes to existing chunks. */
public final class RelicWorldgen implements ModInitializer {
    @Override
    @SuppressWarnings("unchecked")
    public void onInitialize() {
        de.relics.gameplay.RelicItems.initialize();
        de.relics.gameplay.RelicGameplay.initialize();
        RelicProtection.initialize();
        Registry.register(BuiltInRegistries.STRUCTURE_PROCESSOR,
                Identifier.fromNamespaceAndPath("relics", "terrain_support"), TerrainSupportProcessor.CODEC);
        var registry = (Registry<MapCodec<? extends PlacementCondition>>) BuiltInRegistries.REGISTRY
                .getValue(LithostitchedRegistries.PLACEMENT_CONDITION_TYPE.identifier());
        if (registry == null) {
            throw new IllegalStateException("Lithostitched placement registry is unavailable");
        }
        Registry.register(registry, Identifier.fromNamespaceAndPath("relics", "separated"),
                SeparatedPlacementCondition.CODEC);
        Registry.register(registry, Identifier.fromNamespaceAndPath("relics", "all_grid"),
                AllGridPlacementCondition.CODEC);
        Registry.register(registry, Identifier.fromNamespaceAndPath("relics", "dry_land"),
                DryLandPlacementCondition.CODEC);
    }
}
