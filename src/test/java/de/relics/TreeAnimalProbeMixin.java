package de.relics.testmixin;
import de.relics.TreeAnimalChecks;
import de.relics.gameplay.TreeAnimals;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.level.chunk.ChunkAccess;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
@Mixin(TreeAnimals.class)
public abstract class TreeAnimalProbeMixin {
    @Inject(method="afterNaturalSpawn",at=@At("HEAD"),remap=false)
    private static void before(ServerLevel level,Mob source,ChunkAccess chunk,CallbackInfoReturnable<Boolean> ci){TreeAnimalChecks.before();}
    @Inject(method="afterNaturalSpawn",at=@At("RETURN"),remap=false)
    private static void after(ServerLevel level,Mob source,ChunkAccess chunk,CallbackInfoReturnable<Boolean> ci){TreeAnimalChecks.after(ci.getReturnValue());}
}
