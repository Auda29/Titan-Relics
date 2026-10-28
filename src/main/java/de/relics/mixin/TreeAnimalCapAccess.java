package de.relics.mixin;

import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.level.*;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Invoker;

@Mixin(NaturalSpawner.SpawnState.class)
public interface TreeAnimalCapAccess {
    @Invoker("canSpawnForCategoryGlobal") boolean relics$global(MobCategory category);
    @Invoker("canSpawnForCategoryLocal") boolean relics$local(MobCategory category,ChunkPos chunk);
}
