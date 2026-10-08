package de.relics.gameplay;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

/** Versioned, bounded item data. Unknown versions fail decoding rather than refill. */
public record ItemBudget(int version, int remaining) {
    public ItemBudget {
        if (version != 1 || remaining < 0) throw new IllegalArgumentException("Invalid relic item budget");
    }

    public static Codec<ItemBudget> codec(int capacity) {
        return RecordCodecBuilder.create(instance -> instance.group(
                Codec.intRange(1, 1).fieldOf("version").forGetter(ItemBudget::version),
                Codec.intRange(0, capacity).fieldOf("remaining").forGetter(ItemBudget::remaining)
        ).apply(instance, ItemBudget::new));
    }
}
