package de.relics.mixin;

import de.relics.gameplay.DefenseGolem;
import net.minecraft.world.entity.animal.golem.IronGolem;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.golem.AbstractGolem;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(IronGolem.class)
public abstract class DefenseGolemMixin extends AbstractGolem implements DefenseGolem {
    @Unique private String relics$encounter;
    @Unique private boolean relics$goalAdded;
    protected DefenseGolemMixin(EntityType<? extends AbstractGolem> type, Level level) { super(type, level); }
    @Override public String relics$encounter() { return relics$encounter; }
    @Override public void relics$mark(String encounter) {
        relics$encounter = encounter;
        if (encounter != null && !relics$goalAdded) {
            // Native range/visibility/navigation/attack. No boundary, teleport, health or damage edits.
            targetSelector.addGoal(0, new NearestAttackableTargetGoal<>(this, Player.class, 0, true, false,
                    (target, world) -> target instanceof Player player && player.isAlive() && !player.isCreative() && !player.isSpectator()));
            relics$goalAdded = true;
        }
    }
    @Inject(method = "addAdditionalSaveData", at = @At("TAIL"))
    private void relics$save(ValueOutput output, CallbackInfo ci) {
        if (relics$encounter != null) output.putString("relics_defense_encounter", relics$encounter);
    }
    @Inject(method = "readAdditionalSaveData", at = @At("TAIL"))
    private void relics$load(ValueInput input, CallbackInfo ci) { relics$mark(input.getStringOr("relics_defense_encounter", null)); }
}
