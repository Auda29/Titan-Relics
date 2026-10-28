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

        source = List.of(cell(2, 0, 2, Blocks.OAK_LOG.defaultBlockState()),
                cell(3, 5, 3, Blocks.DEEPSLATE_BRICKS.defaultBlockState()),
                cell(4, 9, 4, Blocks.TERRACOTTA.defaultBlockState()),
                cell(5, 11, 5, Blocks.OAK_LOG.defaultBlockState()),
                cell(6, 8, 6, Blocks.OAK_LEAVES.defaultBlockState()),
                cell(7, 9, 7, Blocks.BONE_BLOCK.defaultBlockState()),
                cell(7, 6, 7, Blocks.DIRT.defaultBlockState()));
        var settings = new StructurePlaceSettings().setBoundingBox(box);
        var bushes=List.of(cell(8,20,8,Blocks.ROOTED_DIRT.defaultBlockState()),
                cell(8,21,8,Blocks.FIREFLY_BUSH.defaultBlockState()),
                cell(9,21,9,Blocks.SPRUCE_LOG.defaultBlockState()));
        var treeProcessor=new TerrainSupportProcessor(21,true,Blocks.DIRT.defaultBlockState(),true,2,3,true);
        var planted=treeProcessor.finalizeProcessing(world(-64,p->p.getY()<=16
                ? Blocks.GRASS_BLOCK.defaultBlockState():Blocks.AIR.defaultBlockState(),reads),
                BlockPos.ZERO,BlockPos.ZERO,bushes,bushes,settings);
        check(planted.stream().anyMatch(i->i.pos().equals(new BlockPos(8,17,8)) && i.state().is(Blocks.FIREFLY_BUSH)),
                "Bush moves down four blocks onto actual terrain instead of a floating socket");
        check(planted.stream().anyMatch(i->i.pos().equals(new BlockPos(8,16,8)) && i.state().is(Blocks.ROOTED_DIRT)),
                "Bush soil replaces the surface, with no earth pillar");
        check(planted.stream().filter(i->i.pos().getX()==8).count()==2 && planted.contains(bushes.get(2)),
                "Only the source bush pair moves; other art and all intervening air stay intact");
        planted=treeProcessor.finalizeProcessing(world(-64,p->p.getY()<=24
                ? Blocks.DIRT.defaultBlockState():Blocks.AIR.defaultBlockState(),reads),
                BlockPos.ZERO,BlockPos.ZERO,bushes,bushes,settings);
        check(planted.stream().anyMatch(i->i.pos().equals(new BlockPos(8,25,8)) && i.state().is(Blocks.FIREFLY_BUSH)),
                "Bush follows uphill terrain too");
        for(var terrain:List.<Function<BlockPos,BlockState>>of(p->Blocks.AIR.defaultBlockState(),
                p->p.getY()<=16?Blocks.STONE.defaultBlockState():Blocks.WATER.defaultBlockState(),
                p->p.getY()<=16?Blocks.CHEST.defaultBlockState():Blocks.AIR.defaultBlockState())) {
            planted=treeProcessor.finalizeProcessing(world(-64,terrain,reads),BlockPos.ZERO,BlockPos.ZERO,bushes,bushes,settings);
            check(planted.stream().noneMatch(i->i.pos().getX()==8),"No bush or detached socket over void, water or container");
        }
        var blocked=List.of(bushes.get(0),bushes.get(1),cell(8,17,8,Blocks.SPRUCE_LOG.defaultBlockState()));
        planted=treeProcessor.finalizeProcessing(world(-64,p->p.getY()<=16?Blocks.DIRT.defaultBlockState():Blocks.AIR.defaultBlockState(),reads),
                BlockPos.ZERO,BlockPos.ZERO,blocked,blocked,settings);
        check(planted.contains(blocked.get(2)) && planted.stream().noneMatch(i->i.state().is(Blocks.FIREFLY_BUSH)),
                "A planned root blocks relocation and is never overwritten");
        var outside=List.of(cell(-1,20,0,Blocks.ROOTED_DIRT.defaultBlockState()),cell(-1,21,0,Blocks.FIREFLY_BUSH.defaultBlockState()));
        planted=treeProcessor.finalizeProcessing(world(-64,p->{throw new AssertionError("Neighboring chunk read for bush");},reads),
                BlockPos.ZERO,BlockPos.ZERO,outside,outside,settings);
        check(planted.equals(outside),"Bush logic never reads or writes outside the owning chunk");
        result = new TerrainSupportProcessor(10, true, Blocks.SANDSTONE.defaultBlockState())
                .finalizeProcessing(world(-64, pos -> pos.getY() <= -3 ? Blocks.STONE.defaultBlockState()
                        : Blocks.WATER.defaultBlockState(), reads), BlockPos.ZERO, BlockPos.ZERO, source, source, settings);
        check(result.stream().anyMatch(c -> c.pos().equals(new BlockPos(2, -1, 2)) && c.state().is(Blocks.SANDSTONE)),
                "Support raw-Y0 art below the finite template in a water pocket");
        check(result.stream().anyMatch(c -> c.pos().equals(new BlockPos(7, 8, 7))),
                "Connect bone above a separate lower soil cell, not only the soil bottom");
        check(result.stream().noneMatch(c -> c.pos().getX() == 5 && c.pos().getY() < 11),
                "Raised root arches remain open");
        check(result.stream().noneMatch(c -> c.pos().getX() == 6 && c.pos().getY() < 8),
                "Low leaves do not create earth pillars");
        check(result.stream().map(c -> c.pos().asLong()).distinct().count() == result.size(), "No duplicate supports");
        check(result.subList(0, source.size()).equals(source), "Every authored state retained with art supports enabled");
        for (int x : new int[]{2, 3, 4, 7}) {
            final int column = x;
            check(result.stream().anyMatch(c -> c.pos().getX() == column && c.pos().getY() == -2),
                    "Every low solid column reaches native rock");
        }

        source = List.of(cell(3, 4, 3, Blocks.SPRUCE_LOG.defaultBlockState()),
                cell(4, 7, 4, Blocks.SPRUCE_LOG.defaultBlockState()));
        result = new TerrainSupportProcessor(5, true, Blocks.DIRT.defaultBlockState(), true)
                .finalizeProcessing(world(-64, pos -> pos.getY() <= -3 ? Blocks.STONE.defaultBlockState()
                        : Blocks.AIR.defaultBlockState(), reads), BlockPos.ZERO, BlockPos.ZERO, source, source, settings);
        check(result.size() == 8, "Only the low root grows six blocks down to substrate");
        check(result.subList(2, result.size()).stream().allMatch(c -> c.state().is(Blocks.SPRUCE_LOG)),
                "Root continuation uses original wood, never a soil pedestal");
        check(result.stream().noneMatch(c -> c.pos().getX() == 4 && c.pos().getY() < 7),
                "Higher intentional root arches are retained");

        source = List.of(cell(3, 5, 3, Blocks.BONE_BLOCK.defaultBlockState()),
                cell(4, 5, 4, Blocks.MOSS_BLOCK.defaultBlockState()),
                cell(5, 4, 5, Blocks.SPRUCE_LOG.defaultBlockState()),
                cell(6, 1, 6, Blocks.SPRUCE_LOG.defaultBlockState()));
        result = new TerrainSupportProcessor(5, true, Blocks.DIRT.defaultBlockState(), true, 2, 3, true)
                .finalizeProcessing(world(-64, pos -> pos.getY() <= (pos.getX() == 5 ? 0 : 2)
                        ? Blocks.STONE.defaultBlockState() : Blocks.AIR.defaultBlockState(), reads),
                        BlockPos.ZERO, BlockPos.ZERO, source, source, settings);
        check(result.size() == 8, "Two short anatomical contacts get two cells each");
        check(result.subList(4, result.size()).stream().noneMatch(c -> c.state().is(Blocks.DIRT)),
                "Short Skull contacts preserve bone/moss material rather than an earth belt");
        check(result.stream().noneMatch(c -> c.pos().getX() == 5 && c.pos().getY() < 4),
                "A three-cell cavity is left wholly open, with no hanging partial column");
        check(result.stream().noneMatch(c -> c.pos().getX() == 6 && c.pos().getY() < 1),
                "Deep root endpoints do not build piers through caves");

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
