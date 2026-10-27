package de.relics.mixin;

import de.relics.distribution.DistributionRuntime;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.arguments.ResourceOrTagKeyArgument;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.server.commands.LocateCommand;
import net.minecraft.world.level.levelgen.structure.Structure;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import java.time.Duration;
import com.mojang.datafixers.util.Pair;

@Mixin(LocateCommand.class)
public abstract class DistributionLocateMixin {
    @Inject(method="locateStructure",at=@At("HEAD"),cancellable=true)
    private static void relics$locate(CommandSourceStack source,ResourceOrTagKeyArgument.Result<Structure> requested,CallbackInfoReturnable<Integer> ci) {
        var runtime=DistributionRuntime.get(source.getLevel());if(runtime==null)return;
        var registry=source.registryAccess().lookupOrThrow(Registries.STRUCTURE);
        var matching=registry.listElements().filter(requested).toList();
        if(matching.isEmpty() || matching.stream().anyMatch(h->!h.key().identifier().getNamespace().equals("relics")))return;
        BlockPos origin=BlockPos.containing(source.getPosition());long started=System.nanoTime();
        source.sendSuccess(()->Component.literal("Relikt-Standort wird geprüft. Die Suche läuft im Hintergrund."),false);
        runtime.locate(requested,origin).whenComplete((site,error)->source.getServer().execute(()->{
            if(error!=null)source.sendFailure(Component.literal("Relikt-Suche angehalten: "+error.getMessage()));
            else if(site==null)source.sendFailure(Component.literal("Kein gültiges Ziel im Suchbereich. Wiederholbare Relikte: 500.000 Blöcke; großer Koloss: gespeicherter weltweiter Standort."));
            else {
                var coordinates=Component.literal("["+site.x()+", ~, "+site.z()+"]").withStyle(style->style
                        .withColor(net.minecraft.ChatFormatting.GREEN)
                        .withClickEvent(new net.minecraft.network.chat.ClickEvent.SuggestCommand("/tp @s "+site.x()+" ~ "+site.z())));
                // Vanilla's horizontal helper multiplies int deltas. Our global
                // destination can exceed its squared-distance int range.
                int distance=(int)Math.round(Math.hypot((double)site.x()-origin.getX(),(double)site.z()-origin.getZ()));
                source.sendSuccess(()->Component.translatable("commands.locate.structure.success",requested.asPrintable(),coordinates,distance),false);
            }
        }));
        ci.setReturnValue(1);
    }
}
