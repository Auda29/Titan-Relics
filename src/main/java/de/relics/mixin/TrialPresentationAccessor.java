package de.relics.mixin;

import net.minecraft.world.level.block.entity.trialspawner.TrialSpawnerStateData;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;

@Mixin(TrialSpawnerStateData.class)
public interface TrialPresentationAccessor {
    @Accessor("nextMobSpawnsAt") long relics$nextSpawn();
    @Accessor("nextMobSpawnsAt") void relics$nextSpawn(long time);
}
