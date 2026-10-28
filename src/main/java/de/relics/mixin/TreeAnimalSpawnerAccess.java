package de.relics.mixin;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.*;
import net.minecraft.world.level.*;
import net.minecraft.world.level.biome.MobSpawnSettings;
import net.minecraft.world.level.chunk.*;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Invoker;
import java.util.Optional;

@Mixin(NaturalSpawner.class)
public interface TreeAnimalSpawnerAccess {
    @Invoker("isRightDistanceToPlayerAndSpawnPoint")
    static boolean relics$distance(ServerLevel level,ChunkAccess chunk,BlockPos.MutableBlockPos pos,double distance){throw new AssertionError();}
    @Invoker("getRandomSpawnMobAt")
    static Optional<MobSpawnSettings.SpawnerData> relics$selection(ServerLevel level,StructureManager structures,ChunkGenerator generator,MobCategory category,RandomSource random,BlockPos pos){throw new AssertionError();}
    @Invoker("isValidSpawnPostitionForType")
    static boolean relics$type(ServerLevel level,MobCategory category,StructureManager structures,ChunkGenerator generator,MobSpawnSettings.SpawnerData data,BlockPos.MutableBlockPos pos,double distance){throw new AssertionError();}
    @Invoker("getMobForSpawn")
    static Mob relics$mob(ServerLevel level,EntityType<?> type){throw new AssertionError();}
    @Invoker("isValidPositionForMob")
    static boolean relics$position(ServerLevel level,Mob mob,double distance){throw new AssertionError();}
}
