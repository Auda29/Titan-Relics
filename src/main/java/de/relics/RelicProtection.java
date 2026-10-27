package de.relics;

import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentTarget;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.WorldGenRegion;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate.StructureBlockInfo;

import java.util.List;
import java.util.HashMap;
import net.minecraft.world.level.chunk.ChunkAccess;

/** Only world-generation writes are guarded. Normal mining/building is untouched. */
public final class RelicProtection {
    private static final AttachmentType<ProtectedCells> CELLS = AttachmentRegistry.create(
            Identifier.fromNamespaceAndPath("relics", "placed_cells"),
            builder -> builder.initializer(ProtectedCells::new).persistent(ProtectedCells.CODEC));
    public static final ThreadLocal<Integer> RELIC_PLACEMENT_DEPTH = ThreadLocal.withInitial(() -> 0);
    public static final ThreadLocal<WorldGenLevel> ORE_LEVEL = new ThreadLocal<>();

    public static void initialize() {
        // Register the persistent attachment before chunk data is loaded.
    }

    public static void record(ServerLevelAccessor level, List<StructureBlockInfo> blocks) {
        if (!(level instanceof WorldGenRegion region)) {
            return;
        }
        // The processor provides only cells in the current chunk; no remote loads.
        var chunks = new HashMap<Long, ChunkAccess>();
        var masks = new HashMap<Long, ProtectedCells>();
        for (var info : blocks) {
            if (info.state().isAir()) {
                continue;
            }
            BlockPos pos = info.pos();
            long key = net.minecraft.world.level.ChunkPos.pack(pos.getX() >> 4, pos.getZ() >> 4);
            var cells = masks.computeIfAbsent(key, ignored -> {
                var chunk = region.getChunk(pos.getX() >> 4, pos.getZ() >> 4);
                chunks.put(key, chunk);
                return ((AttachmentTarget) chunk).getAttachedOrCreate(CELLS);
            });
            cells.add(pos);
        }
        chunks.values().forEach(ChunkAccess::markUnsaved);
    }

    public static boolean protectedAt(WorldGenLevel level, BlockPos pos) {
        if (!(level instanceof WorldGenRegion region) || RELIC_PLACEMENT_DEPTH.get() > 0
                || !region.isWithinWriteZone(pos)) {
            return false;
        }
        var chunk = region.getChunk(pos.getX() >> 4, pos.getZ() >> 4);
        var cells = ((AttachmentTarget) chunk).getAttached(CELLS);
        return cells != null && cells.contains(pos);
    }
    /** Empty approved passage cells also need protection from later features. */
    public static void recordCell(WorldGenLevel level,BlockPos pos) {
        if(!(level instanceof WorldGenRegion region) || !region.isWithinWriteZone(pos))
            throw new IllegalStateException("Natural interior write outside owning chunk");
        var chunk=region.getChunk(pos.getX()>>4,pos.getZ()>>4);
        ((AttachmentTarget)chunk).getAttachedOrCreate(CELLS).add(pos);chunk.markUnsaved();
    }
}
