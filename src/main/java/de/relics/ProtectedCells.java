package de.relics;

import com.mojang.serialization.Codec;
import com.mojang.serialization.DataResult;
import net.minecraft.core.BlockPos;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.LongStream;

/** Sparse per-section 4096-bit masks; exact cells, not the whole structure box. */
public final class ProtectedCells {
    public static final Codec<ProtectedCells> CODEC = Codec.unboundedMap(Codec.STRING, Codec.LONG.listOf())
            .comapFlatMap(ProtectedCells::decode, ProtectedCells::encode);
    private final Map<Integer, long[]> sections = new HashMap<>();

    public synchronized void add(BlockPos pos) {
        int index = index(pos);
        sections.computeIfAbsent(pos.getY() >> 4, ignored -> new long[64])[index >> 6] |= 1L << (index & 63);
    }

    public synchronized boolean contains(BlockPos pos) {
        var bits = sections.get(pos.getY() >> 4);
        int index = index(pos);
        return bits != null && (bits[index >> 6] & (1L << (index & 63))) != 0;
    }

    private static int index(BlockPos pos) {
        return (pos.getY() & 15) * 256 + (pos.getZ() & 15) * 16 + (pos.getX() & 15);
    }

    private synchronized Map<String, List<Long>> encode() {
        var result = new HashMap<String, List<Long>>();
        sections.forEach((y, bits) -> result.put(y.toString(), LongStream.of(bits).boxed().toList()));
        return result;
    }

    private static DataResult<ProtectedCells> decode(Map<String, List<Long>> saved) {
        var result = new ProtectedCells();
        try {
            for (var entry : saved.entrySet()) {
                int section = Integer.parseInt(entry.getKey());
                if (entry.getValue().size() != 64) {
                    return DataResult.error(() -> "Relic protection section must contain 64 longs");
                }
                result.sections.put(section, entry.getValue().stream().mapToLong(Long::longValue).toArray());
            }
        } catch (NumberFormatException exception) {
            return DataResult.error(() -> "Invalid relic protection section coordinate");
        }
        return DataResult.success(result);
    }
}
