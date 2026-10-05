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

/** Fill only below the lowest near-ground earth cell, in the current placement box. */
public record TerrainSupportProcessor(int groundY) implements StructureProcessor {
    public static final MapCodec<TerrainSupportProcessor> CODEC = RecordCodecBuilder.mapCodec(instance ->
            instance.group(Codec.intRange(0, 319).fieldOf("ground_y")
                    .forGetter(TerrainSupportProcessor::groundY)).apply(instance, TerrainSupportProcessor::new));
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
        for (var bottom : bottoms.values()) {
            BlockState fill = fillState(bottom.state());
            for (BlockPos pos = bottom.pos().below(); pos.getY() >= level.getMinY(); pos = pos.below()) {
                if (authored.contains(pos.asLong()) || (settings.getBoundingBox() != null
                        && !settings.getBoundingBox().isInside(pos))) {
                    break;
                }
                BlockState existing = level.getBlockState(pos);
                if (!replaceable(existing)) {
                    break;
                }
                result.add(new StructureBlockInfo(pos, fill, null));
            }
        }
        if (level instanceof net.minecraft.server.level.WorldGenRegion) {
            RelicProtection.record(level, result);
        }
        return result;
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
