package de.relics.mixin;

import net.minecraft.world.level.block.entity.vault.VaultSharedData;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;
import java.util.Set;
import java.util.UUID;

@Mixin(VaultSharedData.class)
public interface VaultPresentationAccessor {
    @Accessor("connectedPlayers") Set<UUID> relics$connected();
    @Accessor("connectedPlayers") void relics$connected(Set<UUID> players);
}
