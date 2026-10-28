package de.relics.validation.mixin;
import net.minecraft.network.Connection;
import io.netty.channel.Channel;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;
@Mixin(Connection.class)
public interface ConnectionChannelAccess {
    @Accessor("channel") void relics$channel(Channel channel);
}
