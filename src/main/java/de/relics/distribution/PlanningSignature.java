package de.relics.distribution;

import com.google.gson.*;
import com.mojang.serialization.JsonOps;
import net.minecraft.core.RegistryAccess;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.RegistryOps;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.structure.*;
import net.minecraft.world.level.levelgen.structure.pools.StructureTemplatePool;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureProcessorType;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import static de.relics.distribution.DistributionPlanner.*;

/** Read-only environment capture. Requires loaded registries, never a running level. */
public final class PlanningSignature {
    private PlanningSignature() { }

    public static JsonObject manifest() {
        try(InputStream stream=PlanningSignature.class.getResourceAsStream("/relics.integration.json")) {
            if(stream==null)throw new IllegalStateException("Missing integration contracts");
            return JsonParser.parseString(new String(stream.readAllBytes(),StandardCharsets.UTF_8)).getAsJsonObject();
        }catch(Exception error){throw new IllegalStateException("Cannot read integration contracts",error);}
    }

    /** Preserve the released insertion order as well as canonical hash contents. */
    public static JsonObject capture(RegistryAccess registries,ChunkGenerator generator,ResourceManager resources,String interiors) {
        if(!de.relics.gameplay.NaturalInteriors.LEGACY.equals(interiors) && !de.relics.gameplay.NaturalInteriors.supports(interiors))
            throw new IllegalStateException("Unsupported frozen interior revision");
        JsonObject manifest=manifest(),signature=new JsonObject();signature.add("templates",manifest);
        var ops=RegistryOps.create(JsonOps.INSTANCE,registries);
        signature.add("generator",ChunkGenerator.CODEC.encodeStart(ops,generator).getOrThrow());
        JsonArray environment=new JsonArray();
        for(var entry:registries.lookupOrThrow(Registries.BIOME).entrySet().stream().sorted(java.util.Comparator.comparing(e->e.getKey().identifier().toString())).toList()) {
            JsonObject biome=new JsonObject();biome.addProperty("id",entry.getKey().identifier().toString());
            biome.add("value",net.minecraft.world.level.biome.Biome.DIRECT_CODEC.encodeStart(ops,entry.getValue()).getOrThrow());environment.add(biome);
        }
        signature.add("biomes",environment);
        JsonObject tags=new JsonObject();
        registries.lookupOrThrow(Registries.BIOME).getTags().sorted(java.util.Comparator.comparing(t->t.key().location().toString())).forEach(tag->{
            JsonArray values=new JsonArray();tag.stream().map(h->h.unwrapKey().orElseThrow().identifier().toString()).sorted().forEach(values::add);
            tags.add(tag.key().location().toString(),values);
        });
        signature.add("biomeTags",tags);
        var sets=registries.lookupOrThrow(Registries.STRUCTURE_SET);
        for(Family family:Family.values())if(family!=Family.EMPTY)
            signature.add("set/"+family.id,StructureSet.DIRECT_CODEC.encodeStart(ops,sets.getOptional(id(family.id)).orElseThrow()).getOrThrow());
        var structures=registries.lookupOrThrow(Registries.STRUCTURE);
        var pools=registries.lookupOrThrow(Registries.TEMPLATE_POOL);
        var processors=registries.lookupOrThrow(Registries.PROCESSOR_LIST);
        for(JsonElement item:manifest.getAsJsonArray("structures")) {
            var entry=item.getAsJsonObject();String name=entry.get("id").getAsString();
            verifyTemplate(resources,name+"_worldgen.nbt",entry.getAsJsonObject("worldgen_template").get("sha256").getAsString());
            signature.add("structure/"+name,Structure.DIRECT_CODEC.encodeStart(ops,structures.getOptional(id(name)).orElseThrow()).getOrThrow());
            signature.add("processors/"+name,StructureProcessorType.DIRECT_CODEC.encodeStart(ops,processors.getOptional(id(name+"_terrain")).orElseThrow()).getOrThrow());
            signature.add("pool/"+name,StructureTemplatePool.DIRECT_CODEC.encodeStart(ops,pools.getOptional(id(name)).orElseThrow()).getOrThrow());
            if(de.relics.gameplay.NaturalInteriors.hasAsset(interiors,name)) {
                JsonObject selected=null;
                for(var candidate:de.relics.gameplay.NaturalInteriors.manifest(interiors).getAsJsonArray("structures"))
                    if(candidate.getAsJsonObject().get("id").getAsString().equals(name))selected=candidate.getAsJsonObject();
                if(selected==null)throw new IllegalStateException("Missing approved interior "+name);
                var template=selected.getAsJsonObject("worldgen_template");
                verifyTemplate(resources,template.get("path").getAsString(),template.get("sha256").getAsString());
                signature.add("interior/"+name,selected);
            }
        }
        return signature;
    }

    private static net.minecraft.resources.Identifier id(String name){return net.minecraft.resources.Identifier.fromNamespaceAndPath("relics",name);}

    private static void verifyTemplate(ResourceManager resources,String path,String expected) {
        try(var input=resources.getResource(id("structure/"+path)).orElseThrow().open()) {
            String actual=java.util.HexFormat.of().formatHex(java.security.MessageDigest.getInstance("SHA-256").digest(input.readAllBytes()));
            if(!actual.equals(expected))throw new IllegalStateException("Pinned template differs: "+path);
        }catch(Exception error){throw new IllegalStateException("Cannot verify template: "+path,error);}
    }
}
