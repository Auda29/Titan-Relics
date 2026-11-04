package de.relics.distribution;

import com.google.gson.JsonObject;
import net.minecraft.server.WorldStem;
import net.minecraft.world.level.dimension.LevelStem;
import net.minecraft.world.level.levelgen.NoiseBasedChunkGenerator;
import java.nio.file.*;
import java.util.*;

/** Read-only preflight, before vanilla saves level.dat or starts an integrated server. */
public final class WorldLoadCheck {
    public static final String JOURNAL="data/relics_distribution_v1.json";
    private WorldLoadCheck() { }
    public static final class Problem extends IllegalStateException {
        public final String reason;
        public Problem(String reason,String detail,Throwable cause){super(detail,cause);this.reason=reason;}
    }
    public static void verify(Path root,WorldStem stem) {
        verify(root,stem,29999984);
    }
    public static void verify(Path root,WorldStem stem,int absoluteMaxSize) {
        if(!Files.exists(root.resolve(JOURNAL)))return;
        try {
            var state=new DistributionJournal(root.resolve(JOURNAL),null).state;
            if(!state.frozen)throw new Problem("unfinished","Interrupted initial relic plan; restore a complete world backup",null);
            // STEM_INPUTS_BEGIN
            var settings=stem.worldDataAndGenSettings().genSettings();
            var options=settings.options();
            var generator=settings.dimensions().dimensions().get(LevelStem.OVERWORLD).generator();
            // STEM_INPUTS_END
            if(state.seed!=options.seed())throw new Problem("seed","World seed differs from the saved relic plan",null);
            if(!options.generateStructures())throw new Problem("structures","Structure generation was disabled after the relic plan was frozen",null);
            if(generator.getClass()!=NoiseBasedChunkGenerator.class)throw new Problem("generator","Unsupported Overworld generator: "+generator.getClass().getName(),null);
            // BORDER_INPUTS_BEGIN
            Path borderFile=root.resolve("dimensions/minecraft/overworld/data/minecraft/world_border.dat");
            var border=new net.minecraft.world.level.border.WorldBorder();
            if(Files.exists(borderFile)) {
                var tag=net.minecraft.nbt.NbtIo.readCompressed(borderFile,net.minecraft.nbt.NbtAccounter.unlimitedHeap());
                border=net.minecraft.world.level.border.WorldBorder.CODEC.parse(net.minecraft.nbt.NbtOps.INSTANCE,tag.getCompoundOrEmpty("data")).getOrThrow();
            }
            border.applyInitialSettings(0);
            // BORDER_INPUTS_END
            int absolute=Math.min(29999984,absoluteMaxSize);
            if(state.minX!=(int)Math.ceil(Math.max(-absolute,border.getMinX())) || state.maxX!=(int)Math.floor(Math.min(absolute,border.getMaxX()))
                    || state.minZ!=(int)Math.ceil(Math.max(-absolute,border.getMinZ())) || state.maxZ!=(int)Math.floor(Math.min(absolute,border.getMaxZ())))
                throw new Problem("border","World border differs from the frozen relic plan",null);
            EarlyBiomePreparation.prepare(stem.registries().compositeAccess());
            EarlyLithostitchedPreparation.prepare(stem.registries().compositeAccess(),options.seed());
            JsonObject current=PlanningSignature.capture(stem.registries().compositeAccess(),generator,stem.resourceManager(),state.interiors);
            var enabled=EnumSet.noneOf(DistributionPlanner.Family.class);
            for(var family:DistributionPlanner.Family.values())if(family!=DistributionPlanner.Family.EMPTY
                    && !current.getAsJsonObject("set/"+family.id).getAsJsonArray("structures").isEmpty())enabled.add(family);
            if(!state.enabled.equals(enabled))throw new Problem("structures","Enabled relic families differ from the frozen plan",null);
            if(PlanningProvenance.compare(root,state,current)==PlanningProvenance.Match.DIFFERENT)
                throw new Problem("environment","Relic environment differs from the frozen save. Saved fingerprint="+state.fingerprint
                        +", current fingerprint="+PlanningFingerprint.hash(current)+". No verified harmless transition is available.",null);
        }catch(Problem problem){throw problem;}
        catch(Exception error){throw new Problem("unknown","Relic preflight could not verify the saved environment",error);}
    }
    /** Release both resources independently; a cleanup failure never permits world startup. */
    public static void closeRejected(WorldStem stem,AutoCloseable storage,Problem problem) {
        EarlyBiomePreparation.discard(stem.registries().compositeAccess());
        EarlyLithostitchedPreparation.discard(stem.registries().compositeAccess());
        for(AutoCloseable resource:List.of(stem,storage))try{resource.close();}catch(Exception error){problem.addSuppressed(error);}
    }
}
