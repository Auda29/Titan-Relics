import net.minecraft.server.Bootstrap;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.world.level.block.Block;

/** Query the locally installed native server registry, not a guessed block state. */
public final class InteriorRegistryEvidence {
    public static void main(String[] args) {
        net.minecraft.SharedConstants.tryDetectVersion();
        Bootstrap.bootStrap();
        Identifier id = Identifier.parse("minecraft:black_stained_glass");
        Block block = BuiltInRegistries.BLOCK.getValue(id);
        if (!id.equals(BuiltInRegistries.BLOCK.getKey(block))) throw new IllegalStateException("Missing block");
        if (!block.getStateDefinition().getProperties().isEmpty()) throw new IllegalStateException("Unexpected properties");
        System.out.println("minecraft:black_stained_glass: properties=[]; states=" + block.getStateDefinition().getPossibleStates().size());
    }
}
