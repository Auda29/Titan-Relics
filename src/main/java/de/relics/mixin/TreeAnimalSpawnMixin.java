package de.relics.mixin;

import com.llamalad7.mixinextras.injector.wrapoperation.*;
import de.relics.gameplay.TreeAnimals;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.*;
import net.minecraft.world.level.NaturalSpawner;
import net.minecraft.world.level.chunk.*;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import java.util.List;

@Mixin(NaturalSpawner.class)
public abstract class TreeAnimalSpawnMixin {
    @WrapOperation(method="spawnForChunk",at=@At(value="INVOKE",target="Lnet/minecraft/world/level/NaturalSpawner;spawnCategoryForChunk(Lnet/minecraft/world/entity/MobCategory;Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/level/chunk/LevelChunk;Lnet/minecraft/world/level/NaturalSpawner$SpawnPredicate;Lnet/minecraft/world/level/NaturalSpawner$AfterSpawnCallback;)V"))
    private static void relics$context(MobCategory category,ServerLevel level,LevelChunk chunk,
            NaturalSpawner.SpawnPredicate predicate,NaturalSpawner.AfterSpawnCallback after,Operation<Void> original,
            ServerLevel enclosingLevel,LevelChunk enclosingChunk,NaturalSpawner.SpawnState state,List<MobCategory> categories) {
        if(category!=MobCategory.CREATURE){original.call(category,level,chunk,predicate,after);return;}
        TreeAnimals.withContext(state,predicate,after,()->original.call(category,level,chunk,predicate,after));
    }
    @WrapOperation(method="spawnCategoryForPosition(Lnet/minecraft/world/entity/MobCategory;Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/level/chunk/ChunkAccess;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/level/NaturalSpawner$SpawnPredicate;Lnet/minecraft/world/level/NaturalSpawner$AfterSpawnCallback;)V",at=@At(value="INVOKE",target="Lnet/minecraft/world/level/NaturalSpawner$AfterSpawnCallback;run(Lnet/minecraft/world/entity/Mob;Lnet/minecraft/world/level/chunk/ChunkAccess;)V"))
    private static void relics$extra(NaturalSpawner.AfterSpawnCallback callback,Mob mob,ChunkAccess chunk,Operation<Void> original) {
        original.call(callback,mob,chunk); // Charge the normal spawn before checking either cap again.
        if(mob.level() instanceof ServerLevel level)TreeAnimals.afterNaturalSpawn(level,mob,chunk);
    }
}
