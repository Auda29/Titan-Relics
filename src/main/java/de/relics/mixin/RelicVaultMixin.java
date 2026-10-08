package de.relics.mixin;

import de.relics.gameplay.RelicGameplay;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.vault.VaultBlockEntity;
import net.minecraft.world.level.block.entity.vault.VaultConfig;
import net.minecraft.world.level.block.entity.vault.VaultServerData;
import net.minecraft.world.level.block.entity.vault.VaultSharedData;
import net.minecraft.world.level.block.state.BlockState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(VaultBlockEntity.Server.class)
public abstract class RelicVaultMixin {
    @Inject(method = "tryInsertKey", at = @At("HEAD"), cancellable = true)
    private static void relics$claim(ServerLevel level, BlockPos pos, BlockState state, VaultConfig config,
            VaultServerData data, VaultSharedData shared, Player player, ItemStack key, CallbackInfo ci) {
        if (RelicGameplay.claimVault(level, pos, player, key)) ci.cancel();
    }
    @Inject(method = "tick", at = @At("HEAD"), cancellable = true)
    private static void relics$tick(ServerLevel level, BlockPos pos, BlockState state, VaultConfig config,
            VaultServerData data, VaultSharedData shared, CallbackInfo ci) {
        if (RelicGameplay.tickVault(level, pos, shared)) ci.cancel();
    }
}
