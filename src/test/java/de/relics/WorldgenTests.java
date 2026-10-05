package de.relics;

import net.minecraft.SharedConstants;
import net.minecraft.core.BlockPos;
import net.minecraft.server.Bootstrap;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.placement.RandomSpreadStructurePlacement;
import net.minecraft.world.level.levelgen.structure.placement.RandomSpreadType;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate.StructureBlockInfo;

import java.lang.reflect.Proxy;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;

/** Headless tests of the actual runtime processor; no world or profile writes. */
public final class WorldgenTests {
    private static int assertions;

    private static void check(boolean condition, String message) {
        assertions++;
        if (!condition) {
            throw new AssertionError(message);
        }
    }

    private static StructureBlockInfo cell(int x, int y, int z, BlockState state) {
        return new StructureBlockInfo(new BlockPos(x, y, z), state, null);
    }

    private static ServerLevelAccessor world(int minY, Function<BlockPos, BlockState> states, AtomicInteger reads) {
        return (ServerLevelAccessor) Proxy.newProxyInstance(WorldgenTests.class.getClassLoader(),
                new Class<?>[]{ServerLevelAccessor.class}, (proxy, method, arguments) -> switch (method.getName()) {
                    case "getMinY" -> minY;
                    case "getBlockState" -> {
                        reads.incrementAndGet();
                        yield states.apply((BlockPos) arguments[0]);
                    }
                    default -> throw new AssertionError("Unexpected world call: " + method.getName());
                });
    }

    private static List<StructureBlockInfo> supports(List<StructureBlockInfo> source, int ground,
            ServerLevelAccessor world, BoundingBox box) {
        return new TerrainSupportProcessor(ground).finalizeProcessing(world, BlockPos.ZERO, BlockPos.ZERO,
                source, source, new StructurePlaceSettings().setBoundingBox(box));
    }

    public static void main(String[] arguments) {
        SharedConstants.tryDetectVersion();
        Bootstrap.bootStrap();
        var protectedCells = new ProtectedCells();
        var edge = new BlockPos(-1, -64, -1);
        protectedCells.add(edge);
        protectedCells.add(new BlockPos(0, 319, 0));
        check(protectedCells.contains(edge), "Protection bit masks retain negative coordinates and word edges");
        check(!protectedCells.contains(edge.above()) && !protectedCells.contains(edge.east()),
                "Protection does not fill nearby omitted cells");
        var encoded = ProtectedCells.CODEC.encodeStart(com.mojang.serialization.JsonOps.INSTANCE, protectedCells).getOrThrow();
        var decoded = ProtectedCells.CODEC.parse(com.mojang.serialization.JsonOps.INSTANCE, encoded).getOrThrow();
        check(decoded.contains(edge) && decoded.contains(new BlockPos(0, 319, 0)), "Protection masks persist losslessly");
        check(ProtectedCells.CODEC.parse(com.mojang.serialization.JsonOps.INSTANCE,
                com.google.gson.JsonParser.parseString("{\"0\":[1]}")).error().isPresent(), "Reject invalid protection masks");
        var box = new BoundingBox(0, -64, 0, 15, 319, 15);
        var reads = new AtomicInteger();
        var source = List.of(cell(3, 20, 3, Blocks.DIRT.defaultBlockState()));
        var result = supports(source, 20, world(-64, pos -> pos.getY() <= 12
                ? Blocks.STONE.defaultBlockState() : Blocks.AIR.defaultBlockState(), reads), box);
        check(result.size() == 8, "Seven-block downhill gap must be filled");
        check(result.subList(1, 8).stream().allMatch(info -> info.state().is(Blocks.DIRT)), "Earth stays earth");
        check(source.size() == 1 && result.getFirst() == source.getFirst(), "Source cells are not rewritten");

        source = List.of(cell(4, 20, 4, Blocks.SAND.defaultBlockState()));
        result = supports(source, 20, world(-64, pos -> pos.getY() <= 15
                ? Blocks.STONE.defaultBlockState() : Blocks.WATER.defaultBlockState(), reads), box);
        check(result.size() == 5, "Water below a sand base must not leave a floating skirt");
        check(result.subList(1, 5).stream().allMatch(info -> info.state().is(Blocks.SANDSTONE)), "Sand uses stable fill");

        source = List.of(cell(3, 20, 3, Blocks.DIRT.defaultBlockState()),
                cell(3, 17, 3, Blocks.BONE_BLOCK.defaultBlockState()),
                cell(7, 30, 7, Blocks.MOSS_BLOCK.defaultBlockState()));
        result = supports(source, 20, world(-64, pos -> Blocks.AIR.defaultBlockState(), reads), box);
        check(result.size() == 5, "Do not overwrite planned fossil cells or grow supports from high moss");
        check(result.subList(3, 5).stream().allMatch(info -> info.pos().getY() > 17), "Original model is protected");
        check(result.stream().noneMatch(info -> info.pos().getX() == 5), "Unrelated arch/void columns remain empty");

        int before = reads.get();
        source = List.of(cell(-1, 20, 0, Blocks.DIRT.defaultBlockState()));
        result = supports(source, 20, world(-64, pos -> { throw new AssertionError("Read outside current chunk"); }, reads), box);
        check(result.size() == 1 && reads.get() == before, "No reads or writes in a neighbouring chunk");

        source = List.of(cell(0, -62, 0, Blocks.RED_SAND.defaultBlockState()));
        result = supports(source, 20, world(-64, pos -> Blocks.AIR.defaultBlockState(), reads), box);
        check(result.size() == 3 && result.getLast().pos().getY() == -64, "Stop at dimension minimum");
        check(result.getLast().state().is(Blocks.RED_SANDSTONE), "Red sand uses stable matching fill");

        source = List.of(cell(0, 20, 0, Blocks.GRAVEL.defaultBlockState()));
        result = supports(source, 20, world(-64, pos -> pos.getY() < 18
                ? Blocks.CHEST.defaultBlockState() : Blocks.OAK_LEAVES.defaultBlockState(), reads), box);
        check(result.size() == 3 && result.getLast().state().is(Blocks.STONE), "Leaves do not support gravel; stop at protected blocks");

        source = List.of(cell(0, 20, 0, Blocks.DIRT.defaultBlockState()));
        result = supports(source, 20, world(-64, pos -> pos.getY() == 19 ? Blocks.GRAVEL.defaultBlockState()
                : pos.getY() <= 15 ? Blocks.STONE.defaultBlockState() : Blocks.AIR.defaultBlockState(), reads), box);
        check(result.size() == 5, "Native falling gravel over a cave must not become a false support");

        var calls = new AtomicInteger();
        var gridCondition = new dev.worldgen.lithostitched.api.worldgen.placementcondition.PlacementCondition() {
            public boolean test(Context context, BlockPos pos) { return calls.incrementAndGet() != 3; }
            public com.mojang.serialization.MapCodec<? extends dev.worldgen.lithostitched.api.worldgen.placementcondition.PlacementCondition> codec() { throw new AssertionError(); }
        };
        check(!new AllGridPlacementCondition(100, 50, 25, gridCondition).test(
                (dev.worldgen.lithostitched.api.worldgen.placementcondition.PlacementCondition.Context) null, BlockPos.ZERO)
                && calls.get() == 3, "Reject an all-points grid immediately at the first failed sample");

        // Compare the fast region-bound calculation against a wider brute-force
        // search, including negative coordinates, boundaries and all presets.
        for (int spacing : new int[]{24, 48, 72}) {
            var spread = new RandomSpreadStructurePlacement(spacing, spacing / 2,
                    RandomSpreadType.LINEAR, 206091303);
            for (long seed : new long[]{0, 731204, -129}) {
                for (int cx : new int[]{-145, -73, -48, -1, 0, 47, 72, 145}) {
                    for (int cz : new int[]{-96, -1, 0, 23, 96}) {
                        int radius = 17;
                        boolean brute = false, earlierBrute = false;
                        for (int rx = -8; rx <= 8; rx++) {
                            for (int rz = -8; rz <= 8; rz++) {
                                var candidate = spread.getPotentialStructureChunk(seed, rx * spacing, rz * spacing);
                                boolean close = Math.abs(candidate.x() - cx) <= radius && Math.abs(candidate.z() - cz) <= radius;
                                brute |= close;
                                earlierBrute |= close && (candidate.x() < cx || (candidate.x() == cx && candidate.z() < cz));
                            }
                        }
                        check(SeparatedPlacementCondition.candidateConflicts(spread, seed, cx, cz, radius) == brute,
                                "Reservation disagrees with exhaustive candidate search");
                        check(SeparatedPlacementCondition.candidateConflicts(spread, seed, cx, cz, radius, true) == earlierBrute,
                                "Same-family priority disagrees with exhaustive candidate search");
                    }
                }
            }
        }
        System.out.println("Worldgen Java tests passed: " + assertions + " assertions");
    }
}
