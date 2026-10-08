package de.relics.mixin;

import de.relics.gameplay.CoreFurnace;
import de.relics.gameplay.RelicItems;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.NonNullList;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.AbstractCookingRecipe;
import net.minecraft.world.item.crafting.RecipeManager;
import net.minecraft.world.item.crafting.SingleRecipeInput;
import net.minecraft.world.level.block.AbstractFurnaceBlock;
import net.minecraft.world.level.block.entity.AbstractFurnaceBlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(AbstractFurnaceBlockEntity.class)
public abstract class CoreFurnaceMixin implements CoreFurnace {
    @Shadow protected NonNullList<ItemStack> items;
    @Shadow private int litTimeRemaining;
    @Shadow private int litTotalTime;
    @Shadow private int cookingTimer;
    @Shadow private int cookingTotalTime;
    @Shadow @Final private RecipeManager.CachedCheck<SingleRecipeInput, ? extends AbstractCookingRecipe> quickCheck;
    @Shadow private static boolean canBurn(NonNullList<ItemStack> items, int maximum, ItemStack output) { throw new AssertionError(); }
    @Shadow private static void burn(NonNullList<ItemStack> items, ItemStack input, ItemStack output) { throw new AssertionError(); }
    @Unique private boolean relics$coreMode;

    @Override public void relics$resetCoreProgress() {
        if (relics$coreMode) {
            cookingTimer = 0; litTimeRemaining = 0; litTotalTime = 0; relics$coreMode = false;
            var furnace = (AbstractFurnaceBlockEntity)(Object)this;
            if (furnace.getLevel() instanceof ServerLevel level) {
                var state = level.getBlockState(furnace.getBlockPos());
                if (state.hasProperty(AbstractFurnaceBlock.LIT) && state.getValue(AbstractFurnaceBlock.LIT))
                    level.setBlock(furnace.getBlockPos(), state.setValue(AbstractFurnaceBlock.LIT, false), 3);
                furnace.setChanged();
            }
        }
    }
    @Inject(method = "loadAdditional", at = @At("TAIL"))
    private void relics$load(ValueInput input, CallbackInfo ci) { relics$coreMode = input.getBooleanOr("relics_core_mode", false); }
    @Inject(method = "saveAdditional", at = @At("TAIL"))
    private void relics$save(ValueOutput output, CallbackInfo ci) { output.putBoolean("relics_core_mode", relics$coreMode); }
    @Inject(method = "setItem", at = @At("HEAD"))
    private void relics$switch(int slot, ItemStack stack, CallbackInfo ci) {
        if (slot == 1 && items.get(1) != stack) relics$resetCoreProgress();
    }
    @Inject(method = "canPlaceItem", at = @At("HEAD"), cancellable = true)
    private void relics$insert(int slot, ItemStack stack, CallbackInfoReturnable<Boolean> cir) {
        if (slot == 1 && RelicItems.core(stack)) cir.setReturnValue(stack.getCount() == 1 && RelicItems.remaining(stack, true) > 0);
    }
    @Inject(method = "canTakeItemThroughFace", at = @At("HEAD"), cancellable = true)
    private void relics$extract(int slot, ItemStack stack, Direction side, CallbackInfoReturnable<Boolean> cir) {
        if (slot == 1 && RelicItems.core(stack)) cir.setReturnValue(side == Direction.DOWN && RelicItems.remaining(stack, true) == 0);
    }
    @Inject(method = "serverTick", at = @At("HEAD"), cancellable = true)
    private static void relics$tick(ServerLevel level, BlockPos pos, BlockState state, AbstractFurnaceBlockEntity furnace, CallbackInfo ci) {
        CoreFurnaceMixin self = (CoreFurnaceMixin)(Object) furnace;
        ItemStack core = self.items.get(1);
        if (!RelicItems.core(core)) { self.relics$resetCoreProgress(); return; }
        // Ordinary fuel already paid for is allowed to finish before changing modes.
        if (!self.relics$coreMode && self.litTimeRemaining > 0) return;
        ci.cancel();
        boolean entering = !self.relics$coreMode;
        int oldProgress = self.cookingTimer, oldTotal = self.cookingTotalTime;
        int oldCharge = RelicItems.remaining(core, true);
        if (!self.relics$coreMode) { self.cookingTimer = 0; self.relics$coreMode = true; }
        self.litTimeRemaining = 0;
        self.litTotalTime = 0;
        boolean progress = false;
        var recipe = self.quickCheck.getRecipeFor(new SingleRecipeInput(self.items.get(0)), level).orElse(null);
        if (core.getCount() == 1 && RelicItems.remaining(core, true) > 0 && recipe != null) {
            var input = self.items.get(0);
            var result = recipe.value().assemble(new SingleRecipeInput(input));
            if (!input.isEmpty() && !result.isEmpty() && canBurn(self.items, furnace.getMaxStackSize(), result)) {
                progress = true;
                self.cookingTotalTime = recipe.value().cookingTime();
                if (++self.cookingTimer >= self.cookingTotalTime) {
                    burn(self.items, input, result);
                    RelicItems.setRemaining(core, true, RelicItems.remaining(core, true) - 1);
                    self.cookingTimer = 0;
                    furnace.setRecipeUsed(recipe);
                    if (RelicItems.remaining(core, true) == 0) progress = false;
                }
            }
        }
        if (!progress) self.cookingTimer = 0;
        if (state.getValue(AbstractFurnaceBlock.LIT) != progress) level.setBlock(pos, state.setValue(AbstractFurnaceBlock.LIT, progress), 3);
        if (entering || oldProgress != self.cookingTimer || oldTotal != self.cookingTotalTime
                || oldCharge != RelicItems.remaining(core, true)) furnace.setChanged();
    }
}
