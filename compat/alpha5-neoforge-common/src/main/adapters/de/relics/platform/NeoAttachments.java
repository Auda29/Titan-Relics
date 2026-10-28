package de.relics.platform;

import com.mojang.serialization.Codec;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.attachment.IAttachmentHolder;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;
import java.util.function.*;

/** Persistent native attachments with non-allocating absent reads. No Fabric storage is used. */
public final class NeoAttachments {
    private static final DeferredRegister<net.neoforged.neoforge.attachment.AttachmentType<?>> TYPES=
            DeferredRegister.create(NeoForgeRegistries.ATTACHMENT_TYPES,"relics");
    private NeoAttachments() { }
    public static void initialize(IEventBus bus){TYPES.register(bus);}
    public record AttachmentType<T>(Supplier<net.neoforged.neoforge.attachment.AttachmentType<T>> nativeType) { }
    public static final class Builder<T> {
        private Supplier<T> initializer=()->{throw new IllegalStateException("Attachment has no initializer");};
        private Codec<T> codec;
        private boolean copy;
        public Builder<T> initializer(Supplier<T> supplier){initializer=supplier;return this;}
        public Builder<T> persistent(Codec<T> value){codec=value;return this;}
        public Builder<T> copyOnDeath(){copy=true;return this;}
    }
    public static final class AttachmentRegistry {
        public static <T> AttachmentType<T> create(ResourceLocation id,UnaryOperator<Builder<T>> configure) {
            if(!id.getNamespace().equals("relics"))throw new IllegalArgumentException("Foreign attachment");
            var value=configure.apply(new Builder<T>());
            var type=TYPES.register(id.getPath(),()->{
                var builder=net.neoforged.neoforge.attachment.AttachmentType.builder(value.initializer);
                Codec<T> codec=value.codec;
                if(codec!=null) {
                    // Retain the established native placed-cell section wrapper.
                    if(id.getPath().equals("placed_cells"))codec=codec.fieldOf("sections").codec();
                    builder.serialize(codec);
                }
                if(value.copy)builder.copyOnDeath();
                return builder.build();
            });
            return new AttachmentType<>(type);
        }
    }
    public record AttachmentTarget(IAttachmentHolder holder) {
        public static final String NBT_ATTACHMENT_KEY="neoforge:attachments";
        public static AttachmentTarget of(Object object){return new AttachmentTarget((IAttachmentHolder)object);}
        public <T> T getAttached(AttachmentType<T> type){var key=type.nativeType().get();return holder.hasData(key)?holder.getData(key):null;}
        public <T> T getAttachedOrCreate(AttachmentType<T> type){return holder.getData(type.nativeType().get());}
        public <T> void setAttached(AttachmentType<T> type,T value){holder.setData(type.nativeType().get(),value);}
    }
}
