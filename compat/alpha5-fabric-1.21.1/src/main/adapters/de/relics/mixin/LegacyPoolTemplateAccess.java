package de.relics.mixin;
import com.mojang.datafixers.util.Either;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.levelgen.structure.pools.SinglePoolElement;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;
@Mixin(SinglePoolElement.class)
public interface LegacyPoolTemplateAccess {
    @Accessor("template") Either<ResourceLocation,StructureTemplate> relics$template();
}
