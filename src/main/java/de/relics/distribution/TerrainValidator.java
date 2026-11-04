package de.relics.distribution;

import com.google.gson.*;
import com.mojang.serialization.JsonOps;
import de.relics.SeparatedPlacementCondition;
import dev.worldgen.lithostitched.worldgen.structure.DelegatingStructure;
import net.minecraft.core.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.*;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.*;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.RandomState;
import net.minecraft.world.level.levelgen.structure.*;
import net.minecraft.world.level.levelgen.structure.pieces.PiecesContainer;
import net.minecraft.world.level.levelgen.structure.placement.RandomSpreadStructurePlacement;
import net.minecraft.world.level.levelgen.structure.pools.StructurePoolElement;
import net.minecraft.world.level.levelgen.structure.templatesystem.*;
import java.io.InputStream;
import java.util.*;
import static de.relics.distribution.DistributionPlanner.*;

/** One serialized worker owns all generator queries. No level.getChunk or live terrain reads. */
public final class TerrainValidator implements Validator {
    private record Profile(String id, Family family, int ground, int sx, int sy, int sz,
                           Holder.Reference<Structure> holder, StructurePoolElement element,
                           SeparatedPlacementCondition condition) { }
    private final RegistryAccess registries;
    private final ChunkGenerator generator;
    private final RandomState random;
    private final StructureTemplateManager templates;
    private final LevelHeightAccessor height;
    private final long seed;
    private final int minX,minZ,maxX,maxZ;
    private final Map<String,Profile> profiles=new LinkedHashMap<>();
    private final Map<Structure,String> structureIds=new IdentityHashMap<>();
    private final Map<Object,Family> placements=new IdentityHashMap<>();
    public final Set<Family> enabled=EnumSet.noneOf(Family.class);
    public final String fingerprint;
    public final String legacyFingerprint;
    public final JsonObject signature;
    private final String interiors;
    private final BiomeRules biomeRules;
    public final java.util.concurrent.atomic.LongAdder biomeRejectedProbes=new java.util.concurrent.atomic.LongAdder(),terrainRejectedProbes=new java.util.concurrent.atomic.LongAdder(),boundsRejectedProbes=new java.util.concurrent.atomic.LongAdder();

    public TerrainValidator(ServerLevel level, int minX,int minZ,int maxX,int maxZ) {
        this(level,minX,minZ,maxX,maxZ,de.relics.gameplay.NaturalInteriors.LEGACY);
    }
    public TerrainValidator(ServerLevel level,int minX,int minZ,int maxX,int maxZ,String interiors) {
        this(level,minX,minZ,maxX,maxZ,interiors,BiomeRules.STANDARD);
    }
    public TerrainValidator(ServerLevel level,int minX,int minZ,int maxX,int maxZ,String interiors,BiomeRules biomeRules) {
        this.biomeRules=Objects.requireNonNull(biomeRules);
        if(!de.relics.gameplay.NaturalInteriors.LEGACY.equals(interiors) && !de.relics.gameplay.NaturalInteriors.supports(interiors))
            throw new IllegalStateException("Unsupported frozen interior revision");
        this.interiors=interiors;
        registries=level.registryAccess(); generator=level.getChunkSource().getGenerator();
        random=level.getChunkSource().randomState(); templates=level.getStructureManager(); seed=level.getSeed();
        height=LevelHeightAccessor.create(level.getMinY(),level.getHeight());
        this.minX=minX;this.minZ=minZ;this.maxX=maxX;this.maxZ=maxZ;
        // The current adapter relies on pure base-height/noise-biome queries.
        // Unknown custom generator implementations must supply their own proof.
        if (generator.getClass()!=net.minecraft.world.level.levelgen.NoiseBasedChunkGenerator.class)
            throw new IllegalStateException("Gameplay distribution currently requires the noise-based Overworld generator");
        JsonObject manifest=PlanningSignature.manifest();
        var structures=registries.lookupOrThrow(Registries.STRUCTURE);
        var sets=registries.lookupOrThrow(Registries.STRUCTURE_SET);
        var pools=registries.lookupOrThrow(Registries.TEMPLATE_POOL);
        signature=PlanningSignature.capture(registries,generator,level.getServer().getResourceManager(),interiors);
        var ops=RegistryOps.create(JsonOps.INSTANCE,registries);
        for(Family family:Family.values()) {
            if(family==Family.EMPTY)continue;
            var set=sets.getOptional(id(family.id)).orElseThrow();
            JsonObject placement=net.minecraft.world.level.levelgen.structure.placement.StructurePlacement.CODEC.encodeStart(ops,set.placement()).getOrThrow().getAsJsonObject();
            if(!(set.placement() instanceof RandomSpreadStructurePlacement spread)
                    || placement.get("salt").getAsInt()!=salt(family) || spread.spacing()!=spacing(family) || spread.separation()!=spacing(family)/2
                    || placement.has("frequency") && placement.get("frequency").getAsFloat()!=1f || placement.has("exclusion_zone"))
                throw new IllegalStateException("Legacy density overrides are incompatible with gameplay distribution: "+family.id);
            placements.put(set.placement(),family);
            if(!set.structures().isEmpty()) {
                Set<String> expected=new TreeSet<>(),actual=new TreeSet<>();
                for(JsonElement entry:manifest.getAsJsonArray("structures")) {
                    var a=entry.getAsJsonObject();if(a.get("family").getAsString().equals(family.id))expected.add("relics:"+a.get("id").getAsString());
                }
                for(var entry:set.structures()) {
                    actual.add(entry.structure().unwrapKey().orElseThrow().identifier().toString());
                    if(entry.weight()!=1)throw new IllegalStateException("Relic family weights must not multiply shared tickets");
                }
                if(!actual.equals(expected) || set.structures().size()!=actual.size())throw new IllegalStateException("Partial/foreign relic family overrides are unsupported: "+family.id);
                enabled.add(family);
            }
        }
        for(JsonElement data:manifest.getAsJsonArray("structures")) {
            JsonObject a=data.getAsJsonObject();String name=a.get("id").getAsString();
            Family family=Arrays.stream(Family.values()).filter(f->f.id.equals(a.get("family").getAsString())).findFirst().orElseThrow();
            var holder=structures.getOrThrow(ResourceKey.create(Registries.STRUCTURE,id(name)));
            if(!(holder.value() instanceof DelegatingStructure structure)
                    || !(structure.config().spawnCondition().orElseThrow() instanceof SeparatedPlacementCondition condition))
                throw new IllegalStateException("Unsupported relic structure/terrain override: "+name);
            var pool=pools.getOptional(id(name)).orElseThrow();
            if(pool.size()!=1)throw new IllegalStateException("Relic pool must contain exactly one pinned template: "+name);
            StructurePoolElement element=pool.getRandomTemplate(RandomSource.create(0));
            JsonArray size=a.getAsJsonObject("worldgen_template").getAsJsonArray("size");
            int ground=a.getAsJsonObject("worldgen_template").getAsJsonObject("foundation").get("ground_y").getAsInt();
            JsonObject delegate=signature.getAsJsonObject("structure/"+name).getAsJsonObject("delegate");
            if(!delegate.get("type").getAsString().equals("minecraft:jigsaw") || delegate.get("size").getAsInt()!=1
                    || !delegate.get("start_pool").getAsString().equals("relics:"+name)
                    || !delegate.get("start_jigsaw_name").getAsString().equals("relics:center")
                    || !delegate.get("project_start_to_heightmap").getAsString().equals("WORLD_SURFACE_WG")
                    || delegate.getAsJsonObject("start_height").get("absolute").getAsInt()!=1-ground
                    || delegate.has("terrain_adaptation") && !delegate.get("terrain_adaptation").getAsString().equals("none")
                    || element.getClass()!=net.minecraft.world.level.levelgen.structure.pools.SinglePoolElement.class)
                throw new IllegalStateException("Unsupported jigsaw transform override: "+name);
            try(InputStream stream=level.getServer().getResourceManager().getResource(id("structure/"+name+"_worldgen.nbt")).orElseThrow().open()) {
                String actual=java.util.HexFormat.of().formatHex(java.security.MessageDigest.getInstance("SHA-256").digest(stream.readAllBytes()));
                if(!actual.equals(a.getAsJsonObject("worldgen_template").get("sha256").getAsString()))
                    throw new IllegalStateException("Natural template differs from the selected export: "+name);
            }catch(Exception error){throw new IllegalStateException("Cannot verify natural template: "+name,error);}
            var processors=registries.lookupOrThrow(Registries.PROCESSOR_LIST).getOptional(id(name+"_terrain")).orElseThrow();
            // Preload the template on the server thread, before the serialized planner uses it.
            var box=element.getBoundingBox(templates,BlockPos.ZERO,Rotation.NONE);
            if(box.getXSpan()!=size.get(0).getAsInt() || box.getYSpan()!=size.get(1).getAsInt() || box.getZSpan()!=size.get(2).getAsInt())
                throw new IllegalStateException("Pinned template geometry differs: "+name);
            if(de.relics.gameplay.NaturalInteriors.hasAsset(interiors,name)) {
                JsonObject selected=null;
                for(var item:de.relics.gameplay.NaturalInteriors.manifest(interiors).getAsJsonArray("structures"))
                    if(item.getAsJsonObject().get("id").getAsString().equals(name))selected=item.getAsJsonObject();
                if(selected==null)throw new IllegalStateException("Missing approved interior "+name);
                String template=selected.getAsJsonObject("worldgen_template").get("path").getAsString();
                try(var stream=level.getServer().getResourceManager().getResource(id("structure/"+template)).orElseThrow().open()) {
                    if(!java.util.HexFormat.of().formatHex(java.security.MessageDigest.getInstance("SHA-256").digest(stream.readAllBytes()))
                            .equals(selected.getAsJsonObject("worldgen_template").get("sha256").getAsString()))throw new IllegalStateException("Approved template differs");
                }catch(Exception error){throw new IllegalStateException("Cannot verify approved interior",error);}
                var json=new JsonObject();json.addProperty("element_type","minecraft:single_pool_element");
                json.addProperty("location","relics:"+template.substring(0,template.length()-4));json.addProperty("processors","relics:"+name+"_terrain");json.addProperty("projection","rigid");
                element=StructurePoolElement.CODEC.parse(ops,json).getOrThrow();
                var chosen=element.getBoundingBox(templates,BlockPos.ZERO,Rotation.NONE);
                if(chosen.getXSpan()!=box.getXSpan() || chosen.getYSpan()!=box.getYSpan() || chosen.getZSpan()!=box.getZSpan())throw new IllegalStateException("Approved interior transform changed");
            }
            profiles.put(name,new Profile(name,family,ground,box.getXSpan(),box.getYSpan(),box.getZSpan(),holder,element,condition));
            structureIds.put(holder.value(),name);
        }
        legacyFingerprint=DistributionJournal.hash(signature.toString());
        fingerprint=PlanningFingerprint.hash(signature);
    }
    private static int spacing(Family f) {return switch(f){case COLOSSUS,TOWER->80;case OBELISK,SKULL_2->64;case SKULL,SMALL->48;case TREE->96;default->throw new IllegalArgumentException();};}
    private static int salt(Family f) {return switch(f){case OBELISK->206091301;case COLOSSUS->206091302;case SKULL->206091303;case SMALL->206091304;case TREE->206091305;case TOWER->206091306;case SKULL_2->206091307;default->throw new IllegalArgumentException();};}
    public static Identifier id(String name){return Identifier.fromNamespaceAndPath("relics",name);}
    public Family placement(Object placement){return placements.get(placement);}
    public String structure(Structure structure){return structureIds.get(structure);}
    public Holder.Reference<Structure> holder(String asset){return profiles.get(asset).holder;}
    public boolean hasRepeatable(java.util.function.Predicate<Holder<Structure>> requested){return profiles.values().stream().anyMatch(p->p.family!=Family.COLOSSUS && requested.test(p.holder));}
    public Set<Family> repeatableFamilies(java.util.function.Predicate<Holder<Structure>> requested) {
        Set<Family> result=EnumSet.noneOf(Family.class);
        for(var profile:profiles.values())if(profile.family!=Family.COLOSSUS && requested.test(profile.holder))result.add(profile.family);
        return result;
    }
    private Profile biomeProfile(Holder<net.minecraft.world.level.biome.Biome> biome,Family family) {
        List<String> compatible=profiles.values().stream().filter(p->p.family==family && p.holder.value().biomes().contains(biome)).map(Profile::id).toList();
        Set<String> tags=new HashSet<>();biome.tags().forEach(tag->tags.add(tag.location().toString()));
        String selected=biomeRules.profile(family,biome.unwrapKey().orElseThrow().identifier().toString(),tags,compatible);
        if(selected==null)return null;
        Profile profile=profiles.get(selected);if(profile==null || profile.family!=family)throw new IllegalStateException("No pinned profile for biome selection: "+selected);
        return profile;
    }
    public boolean hasPossibleBiome(Family family){return generator.getBiomeSource().possibleBiomes().stream().anyMatch(b->biomeProfile(b,family)!=null);}
    @Override public Site validate(Candidate c,Family family) {
        int surface=generator.getFirstFreeHeight(c.x(),c.z(),Heightmap.Types.WORLD_SURFACE_WG,height,random);
        var biome=generator.getBiomeSource().getNoiseBiome(QuartPos.fromBlock(c.x()),QuartPos.fromBlock(surface),QuartPos.fromBlock(c.z()),random.sampler());
        // Biome tags choose one crowned palette. No failed-palette or family reroll.
        Profile p=biomeProfile(biome,family);if(p==null){biomeRejectedProbes.increment();return null;}
        Rotation rotation=Rotation.values()[c.rotation()];
        var zero=p.element.getBoundingBox(templates,BlockPos.ZERO,rotation);
        int ox=c.x()-Math.floorDiv(zero.minX()+zero.maxX(),2),oz=c.z()-Math.floorDiv(zero.minZ()+zero.maxZ(),2);
        BlockPos origin=new BlockPos(ox,surface-p.ground,oz);
        var box=p.element.getBoundingBox(templates,origin,rotation);
        if(box.minX()<minX || box.maxX()>maxX || box.minZ()<minZ || box.maxZ()>maxZ
                || box.minY()<height.getMinY()+8 || box.maxY()>height.getMaxY()-8){boundsRejectedProbes.increment();return null;}
        var context=new Structure.GenerationContext(registries,generator,generator.getBiomeSource(),random,templates,
                seed,new ChunkPos(c.chunkX(),c.chunkZ()),height,b->biomeRules.rule(family).mode()==BiomeRules.Mode.STANDARD?p.holder.value().biomes().contains(b):b.equals(biome));
        if(!p.condition.terrainCondition().test(context,new BlockPos(c.x(),surface,c.z()))){terrainRejectedProbes.increment();return null;}
        return new Site(c,p.id,box.minX()+box.maxX(),box.minZ()+box.maxZ(),surface,origin.getX(),origin.getY(),origin.getZ(),box.minX(),box.minZ(),box.maxX(),box.maxZ());
    }
    public StructureStart start(Site site) {
        Profile p=profiles.get(site.asset());var origin=new BlockPos(site.originX(),site.originY(),site.originZ());
        Rotation rotation=Rotation.values()[site.candidate().rotation()];
        var piece=new PoolElementStructurePiece(templates,p.element,origin,p.element.getGroundLevelDelta(),rotation,
                p.element.getBoundingBox(templates,origin,rotation),LiquidSettings.IGNORE_WATERLOGGING);
        if(de.relics.gameplay.NaturalInteriors.hasAsset(interiors,site.asset()))
            ((de.relics.gameplay.NaturalPiece)(Object)piece).relics$setSite(de.relics.gameplay.NaturalInteriors.certificate(seed,site,interiors));
        return new StructureStart(p.holder.value(),new ChunkPos(site.candidate().chunkX(),site.candidate().chunkZ()),0,new PiecesContainer(List.of(piece)));
    }
}
