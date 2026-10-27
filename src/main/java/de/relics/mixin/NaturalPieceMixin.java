package de.relics.mixin;

import com.llamalad7.mixinextras.injector.wrapmethod.WrapMethod;
import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import de.relics.gameplay.*;
import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.*;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.structure.*;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePieceSerializationContext;
import org.spongepowered.asm.mixin.*;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(PoolElementStructurePiece.class)
public abstract class NaturalPieceMixin implements NaturalPiece {
    @Unique private String relics$certificate;
    public void relics$setSite(String certificate){relics$certificate=certificate;}
    public String relics$site(){return relics$certificate;}
    @Inject(method="<init>(Lnet/minecraft/world/level/levelgen/structure/pieces/StructurePieceSerializationContext;Lnet/minecraft/nbt/CompoundTag;)V",at=@At("RETURN"))
    private void relics$load(StructurePieceSerializationContext context,CompoundTag tag,CallbackInfo ci){
        relics$certificate=tag.getString("relics_natural_site").orElse(null);
    }
    @Inject(method="addAdditionalSaveData",at=@At("TAIL"))
    private void relics$save(StructurePieceSerializationContext context,CompoundTag tag,CallbackInfo ci){
        if(relics$certificate!=null)tag.putString("relics_natural_site",relics$certificate);
    }
    @WrapMethod(method="postProcess")
    private void relics$place(WorldGenLevel level,StructureManager manager,ChunkGenerator generator,
            RandomSource random,BoundingBox box,ChunkPos chunk,BlockPos pivot,Operation<Void> original){
        original.call(level,manager,generator,random,box,chunk,pivot);
        if(relics$certificate!=null)NaturalInteriors.afterPlacement(level,manager,box,chunk,
                (PoolElementStructurePiece)(Object)this,relics$certificate);
    }
}
