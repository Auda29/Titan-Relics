package de.relics;

import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureProcessor;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate.StructureBlockInfo;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/** Connect exposed low model undersides to actual substrate, in this chunk only. */
public record TerrainSupportProcessor(int groundY, boolean supportArt, BlockState artFill) implements StructureProcessor {
    public static final MapCodec<TerrainSupportProcessor> CODEC = RecordCodecBuilder.mapCodec(instance ->
            instance.group(Codec.intRange(0, 319).fieldOf("ground_y")
                            .forGetter(TerrainSupportProcessor::groundY),
                    Codec.BOOL.optionalFieldOf("support_art", false).forGetter(TerrainSupportProcessor::supportArt),
                    BlockState.CODEC.optionalFieldOf("art_fill", Blocks.DIRT.defaultBlockState())
                            .forGetter(TerrainSupportProcessor::artFill)).apply(instance, TerrainSupportProcessor::new));

    public TerrainSupportProcessor(int groundY) {
        this(groundY, false, Blocks.DIRT.defaultBlockState());
    }
    private static final Set<Block> SOILS = Set.of(Blocks.DIRT, Blocks.ROOTED_DIRT, Blocks.COARSE_DIRT,
            Blocks.GRASS_BLOCK, Blocks.MOSS_BLOCK, Blocks.PODZOL, Blocks.SAND, Blocks.SANDSTONE,
            Blocks.SMOOTH_SANDSTONE, Blocks.RED_SAND, Blocks.RED_SANDSTONE, Blocks.GRAVEL,
            Blocks.STONE, Blocks.ANDESITE, Blocks.TUFF);

    @Override
    public List<StructureBlockInfo> finalizeProcessing(ServerLevelAccessor level, BlockPos origin,
            BlockPos reference, List<StructureBlockInfo> originals, List<StructureBlockInfo> processed,
            StructurePlaceSettings settings) {
        // Minecraft 26.2 supplies only this chunk's cells unless a processor asks
        // for the entire piece. Never read or write a neighbouring chunk here.
        var bottoms = new HashMap<Long, StructureBlockInfo>();
        var authored = new HashSet<Long>();
        for (var info : processed) {
            authored.add(info.pos().asLong());
            if (info.pos().getY() > origin.getY() + groundY || !SOILS.contains(info.state().getBlock())) {
                continue;
            }
            long column = BlockPos.asLong(info.pos().getX(), 0, info.pos().getZ());
            var previous = bottoms.get(column);
            if (previous == null || info.pos().getY() < previous.pos().getY()) {
                bottoms.put(column, info);
            }
        }
        var result = new ArrayList<>(processed);
        var starts = new ArrayList<>(bottoms.values());
        if (supportArt) {
            // Check every exposed run end, not just the lowest soil in a column:
            // a root may bridge air above a separate authored soil deposit.
            for (var info : processed) {
                if (info.pos().getY() <= origin.getY() + groundY
                        && eligibleArt(info.state()) && !authored.contains(info.pos().below().asLong())) {
                    starts.add(info);
                }
            }
        }
        var added = new HashSet<Long>();
        for (var bottom : starts) {
            BlockState fill = SOILS.contains(bottom.state().getBlock()) ? fillState(bottom.state()) : artFill;
            for (BlockPos pos = bottom.pos().below(); pos.getY() >= level.getMinY(); pos = pos.below()) {
                if (authored.contains(pos.asLong()) || added.contains(pos.asLong()) || (settings.getBoundingBox() != null
                        && !settings.getBoundingBox().isInside(pos))) {
                    break;
                }
                BlockState existing = level.getBlockState(pos);
                if (!replaceable(existing)) {
                    break;
                }
                result.add(new StructureBlockInfo(pos, fill, null));
                added.add(pos.asLong());
            }
        }
        if (level instanceof net.minecraft.server.level.WorldGenRegion) {
            RelicProtection.record(level, result);
        }
        return result;
    }

    private static boolean eligibleArt(BlockState state) {
        return !SOILS.contains(state.getBlock()) && !state.isAir() && !state.hasBlockEntity()
                && state.getFluidState().isEmpty() && !state.canBeReplaced()
                && !(state.getBlock() instanceof net.minecraft.world.level.block.LeavesBlock)
                && !state.is(Blocks.STRUCTURE_VOID);
    }

    private static boolean replaceable(BlockState state) {
        // Stop at all solid/protected blocks. Leaves and thin vegetation are not
        // a foundation; fluids must not leave a floating soil skirt either.
        return !state.hasBlockEntity() && (state.isAir() || !state.getFluidState().isEmpty()
                || state.canBeReplaced() || state.getBlock() instanceof net.minecraft.world.level.block.LeavesBlock
                || state.getBlock() instanceof net.minecraft.world.level.block.FallingBlock);
    }

    private static BlockState fillState(BlockState state) {
        Block block = state.getBlock();
        if (block == Blocks.SAND || block == Blocks.SANDSTONE || block == Blocks.SMOOTH_SANDSTONE) {
            return Blocks.SANDSTONE.defaultBlockState();
        }
        if (block == Blocks.RED_SAND || block == Blocks.RED_SANDSTONE) {
            return Blocks.RED_SANDSTONE.defaultBlockState();
        }
        if (block == Blocks.STONE || block == Blocks.ANDESITE || block == Blocks.TUFF || block == Blocks.GRAVEL) {
            return Blocks.STONE.defaultBlockState();
        }
        return Blocks.DIRT.defaultBlockState();
    }

    @Override
    public MapCodec<? extends StructureProcessor> codec() {
        return CODEC;
    }
}
