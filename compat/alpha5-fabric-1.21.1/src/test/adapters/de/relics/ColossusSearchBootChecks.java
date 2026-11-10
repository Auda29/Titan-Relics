package de.relics;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerWorldEvents;
import net.minecraft.world.level.GameRules;

/** Test-only: avoid unrelated spawn-area pregeneration in serial destination-search audits. */
public final class ColossusSearchBootChecks implements ModInitializer {
    @Override public void onInitialize() {
        ServerWorldEvents.LOAD.register((server,level)->
                level.getGameRules().getRule(GameRules.RULE_SPAWN_CHUNK_RADIUS).set(0,server));
    }
}
