package de.relics.gameplay;

import com.mojang.brigadier.arguments.StringArgumentType;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.minecraft.commands.Commands;
import net.minecraft.commands.arguments.coordinates.BlockPosArgument;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.permissions.Permissions;
import net.minecraft.world.level.block.Blocks;

/** Opt-in fixtures: never exposed on ordinary saves, never rewrite structure templates. */
public final class GameplayFixtures {
    private GameplayFixtures() { }
    public static void initialize() {
        if (!Boolean.getBoolean("relics.gameplayFixtures")) return;
        CommandRegistrationCallback.EVENT.register((dispatcher, registry, environment) -> dispatcher.register(
            Commands.literal("relicsfixture").requires(source -> source.permissions().hasPermission(Permissions.COMMANDS_GAMEMASTER))
                .then(Commands.literal("site").then(Commands.argument("name", StringArgumentType.word())
                    .then(Commands.argument("spawner", BlockPosArgument.blockPos())
                    .then(Commands.argument("golem", BlockPosArgument.blockPos())
                    .then(Commands.argument("vault", BlockPosArgument.blockPos()).executes(context -> {
                        var level = context.getSource().getLevel();
                        BlockPos spawner = BlockPosArgument.getLoadedBlockPos(context, "spawner");
                        BlockPos golem = BlockPosArgument.getLoadedBlockPos(context, "golem");
                        BlockPos vault = BlockPosArgument.getLoadedBlockPos(context, "vault");
                        if (!level.getBlockState(spawner).is(Blocks.TRIAL_SPAWNER) || !level.getBlockState(vault).is(Blocks.VAULT))
                            throw new IllegalArgumentException("Place a trial spawner and vault first");
                        RelicGameplay.registerFixture(level, StringArgumentType.getString(context, "name"), spawner, golem, vault);
                        context.getSource().sendSuccess(() -> Component.literal("Registered isolated fixture; no natural integration"), false);
                        return 1;
                    }))))))
                .then(Commands.literal("tree").then(Commands.argument("name", StringArgumentType.word())
                    .then(Commands.argument("anchor", BlockPosArgument.blockPos()).executes(context -> {
                        RelicGameplay.registerFixtureTree(context.getSource().getLevel(), StringArgumentType.getString(context, "name"),
                                BlockPosArgument.getLoadedBlockPos(context, "anchor")); return 1;
                    }))))
                .then(Commands.literal("map").then(Commands.argument("origin", StringArgumentType.word()).executes(context -> {
                    var player = context.getSource().getPlayerOrException();
                    if (player.getInventory().getFreeSlot() < 0) throw new IllegalArgumentException("Need a free inventory slot");
                    player.getInventory().add(RelicGameplay.createPendingMap(player.level(), "fixture:" + StringArgumentType.getString(context, "origin")));
                    return 1;
                })))
                .then(Commands.literal("target").then(Commands.argument("target", BlockPosArgument.blockPos()).executes(context -> {
                    var journal = RelicGameplay.ledger(context.getSource().getServer());
                    var target = RelicGameplay.point(context.getSource().getLevel(), BlockPosArgument.getBlockPos(context, "target"));
                    if (journal.state.committedTarget != null && !journal.state.committedTarget.equals(target))
                        throw new IllegalArgumentException("Committed fixture destination cannot move");
                    journal.state.committedTarget = target; journal.state.targetUnavailable = false; journal.flush(); return 1;
                })))
                .then(Commands.literal("unavailable").executes(context -> {
                    var journal = RelicGameplay.ledger(context.getSource().getServer());
                    journal.state.targetUnavailable = true; journal.flush(); return 1;
                }))
                .then(Commands.literal("status").executes(context -> {
                    var state = RelicGameplay.ledger(context.getSource().getServer()).state;
                    context.getSource().sendSuccess(() -> Component.literal("Fixture sites=" + state.sites.size() + ", trees=" + state.trees.size()
                            + ", claims=" + state.vaultClaims.size() + ", origins=" + state.origins.size()
                            + ", held=" + state.deliveries.values().stream().filter(d -> d.phase == GameplayLedger.DeliveryPhase.AMBIGUOUS).count()), false);
                    return 1;
                }))));
    }
}
