package de.relics;

import com.google.gson.*;
import com.mojang.serialization.JsonOps;
import de.relics.distribution.*;
import dev.worldgen.lithostitched.api.worldgen.placementcondition.PlacementCondition;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.minecraft.core.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.RegistryOps;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.structure.*;
import net.minecraft.world.level.levelgen.structure.pools.StructurePoolElement;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplateManager;
import java.lang.reflect.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import static de.relics.distribution.DistributionPlanner.*;

/** Diagnostic-only mod. Runs actual production validation on the existing serial actor.
 * Reflection reads frozen inputs; production fields, resources and rules are never changed. */
public final class DistributionAuditMod implements ModInitializer {
    private static final Gson JSON=new GsonBuilder().setPrettyPrinting().create();
    private static Object field(Object object,String name) {
        try {Field f=object.getClass().getDeclaredField(name);f.setAccessible(true);return f.get(object);}
        catch(Exception e){throw new IllegalStateException(name,e);}
    }
    private static Object invoke(Object object,String name,Class<?>[] types,Object... args) {
        try {Method m=object.getClass().getDeclaredMethod(name,types);m.setAccessible(true);return m.invoke(object,args);}
        catch(Exception e){throw new IllegalStateException(name,e);}
    }
    @Override public void onInitialize() {
        ServerLifecycleEvents.SERVER_STARTED.register(server->{
            DistributionRuntime runtime=DistributionRuntime.get(server.overworld());
            if(runtime==null)throw new IllegalStateException("Audit requires an isolated fresh gameplay world");
            @SuppressWarnings("unchecked") CompletableFuture<Void> ready=(CompletableFuture<Void>)field(runtime,"ready");
            var actor=(ScheduledExecutorService)field(runtime,"actor");
            ready.whenComplete((ignored,error)->{
                if(error!=null)throw new IllegalStateException(error);
                actor.execute(()->{
                    try {new Audit(server.overworld(),runtime).run();}
                    catch(Throwable failure){failure.printStackTrace();System.out.println("RELIC_AUDIT_FAILED "+failure);}
                });
            });
        });
    }
    private record Leaf(String reason,PlacementCondition condition) { }
    private record Grid(int radius,int step,List<Leaf> leaves) { }
    private record Validation(Candidate candidate,Family family,String asset,String primary,
                              Map<String,Integer> failedSamples,Site site,String biome,int surface) { }
    private static final class Audit {
        final ServerLevel level;
        final DistributionRuntime runtime;
        final TerrainValidator real;
        final DistributionJournal.State snapshot;
        final Map<String,Object> profiles;
        final PlacementCondition.Context context;
        final Map<String,Grid> grids=new HashMap<>();
        final Map<String,Validation> validations=new LinkedHashMap<>();
        final Set<String> explainedProbes=new HashSet<>();
        final Map<String,Integer> probeOutcomes=new TreeMap<>();
        final DistributionPlanner planner;
        long validationCalls;
        @SuppressWarnings("unchecked") Audit(ServerLevel level,DistributionRuntime runtime)throws Exception {
            this.level=level;this.runtime=runtime;real=(TerrainValidator)field(runtime,"validator");
            snapshot=((DistributionJournal)field(runtime,"journal")).state;
            profiles=(Map<String,Object>)field(real,"profiles");
            context=new PlacementCondition.Context(level.registryAccess(),level.getChunkSource().getGenerator(),
                (net.minecraft.world.level.LevelHeightAccessor)field(real,"height"),level.getChunkSource().randomState(),
                level.getChunkSource().getGenerator().getBiomeSource(),level.getSeed());
            var ops=RegistryOps.create(JsonOps.INSTANCE,level.registryAccess());
            for(String asset:profiles.keySet()) {
                String path="/data/relics/worldgen/structure/"+asset+".json";
                JsonObject structure;
                try(var input=DistributionAuditMod.class.getResourceAsStream(path)) {
                    structure=JsonParser.parseString(new String(Objects.requireNonNull(input).readAllBytes(),StandardCharsets.UTF_8)).getAsJsonObject();
                }
                var terrain=structure.getAsJsonObject("spawn_condition").getAsJsonObject("terrain_condition");
                if(!terrain.get("type").getAsString().equals("lithostitched:offset")
                        || terrain.getAsJsonArray("offset").asList().stream().anyMatch(v->v.getAsInt()!=0))throw new AssertionError("Unknown terrain offset");
                var grid=terrain.getAsJsonObject("condition");
                if(!grid.get("type").getAsString().equals("relics:all_grid"))throw new AssertionError("Unknown grid");
                List<Leaf> leaves=new ArrayList<>();
                for(JsonElement item:grid.getAsJsonObject("condition").getAsJsonArray("conditions")) {
                    var node=item.getAsJsonObject();String type=node.get("type").getAsString();
                    String reason=switch(type) {
                        case "lithostitched:height_filter" -> node.get("range_type").getAsString().equals("heightmap_relative")?"slope":"absolute_height";
                        case "relics:dry_land" -> "water_surface";
                        case "lithostitched:not" -> "ocean_or_river_biome";
                        case "lithostitched:in_biome" -> "palette_grid_biome";
                        default -> throw new AssertionError("Unclassified predicate "+type);
                    };
                    leaves.add(new Leaf(reason,PlacementCondition.BASE_CODEC.parse(ops,node).getOrThrow()));
                }
                grids.put(asset,new Grid(grid.get("radius").getAsInt(),grid.get("distance_between_points").getAsInt(),List.copyOf(leaves)));
            }
            planner=new DistributionPlanner(snapshot.policy,level.getSeed(),snapshot.enabled,this::validate,()->snapshot.unique,
                    ()->snapshot.unavailable,snapshot.bootstrapX,snapshot.bootstrapZ,128);
        }
        private String key(Candidate c,Family family){return c.cell().x()+","+c.cell().z()+":"+family;}
        private Site validate(Candidate c,Family family) {
            validationCalls++;
            Site actual=real.validate(c,family);
            String key=key(c,family);
            String probeKey=key+":"+c.x()+","+c.z();
            if(explainedProbes.add(probeKey)) {
                Validation previous=validations.get(key);
                Validation detail=snapshot.policy.equals(LEGACY_POLICY) || previous==null || actual!=null?explain(c,family,actual)
                        :new Validation(c,family,null,"local_probe_rejected",Map.of(),null,null,0);
                probeOutcomes.merge(actual!=null?"accepted":"rejected",1,Integer::sum);
                if(previous==null || previous.site==null || actual!=null)validations.put(key,detail);
            }
            if(actual!=null && validations.get(key).site!=null && !Objects.equals(validations.get(key).site,actual))
                throw new AssertionError("Accepted location changed on repeated search");
            return actual;
        }
        @SuppressWarnings("unchecked") private Validation explain(Candidate c,Family family,Site actual) {
            int surface=context.generator().getFirstFreeHeight(c.x(),c.z(),Heightmap.Types.WORLD_SURFACE_WG,context.heightAccessor(),context.randomState());
            var biome=context.biomeSource().getNoiseBiome(QuartPos.fromBlock(c.x()),QuartPos.fromBlock(surface),QuartPos.fromBlock(c.z()),context.randomState().sampler());
            String biomeId=level.registryAccess().lookupOrThrow(Registries.BIOME).getKey(biome.value()).toString();
            String asset=null;Object profile=null;
            for(var entry:profiles.entrySet()) {
                Object p=entry.getValue();var holder=(Holder<Structure>)field(p,"holder");
                if(field(p,"family")==family && holder.value().biomes().contains(biome)) {
                    if(profile!=null)throw new AssertionError("Ambiguous palette");asset=entry.getKey();profile=p;
                }
            }
            if(profile==null) {
                if(actual!=null)throw new AssertionError("Production accepted incompatible center biome");
                return new Validation(c,family,null,"center_biome",Map.of(),null,biomeId,surface);
            }
            var element=(StructurePoolElement)field(profile,"element");var templates=(StructureTemplateManager)field(real,"templates");
            Rotation rotation=Rotation.values()[c.rotation()];var zero=element.getBoundingBox(templates,BlockPos.ZERO,rotation);
            BlockPos origin=new BlockPos(c.x()-Math.floorDiv(zero.minX()+zero.maxX(),2),surface-(int)field(profile,"ground"),c.z()-Math.floorDiv(zero.minZ()+zero.maxZ(),2));
            var box=element.getBoundingBox(templates,origin,rotation);
            String bounds=null;
            if(box.minX()<snapshot.minX || box.maxX()>snapshot.maxX || box.minZ()<snapshot.minZ || box.maxZ()>snapshot.maxZ)bounds="world_border";
            else if(box.minY()<context.heightAccessor().getMinY()+8 || box.maxY()>context.heightAccessor().getMaxY()-8)bounds="vertical_bounds";
            if(bounds!=null) {
                if(actual!=null)throw new AssertionError("Production accepted invalid bounds");
                return new Validation(c,family,asset,bounds,Map.of(),null,biomeId,surface);
            }
            Grid grid=grids.get(asset);Map<String,Integer> failures=new LinkedHashMap<>();
            for(Leaf leaf:grid.leaves) {
                int count=0;
                for(int x=c.x()-grid.radius;x<=c.x()+grid.radius;x+=grid.step)
                    for(int z=c.z()-grid.radius;z<=c.z()+grid.radius;z+=grid.step)
                        if(!leaf.condition.test(context,new BlockPos(x,surface,z)))count++;
                if(count>0)failures.put(leaf.reason,count);
            }
            if((actual==null)!=(!failures.isEmpty()))throw new AssertionError("Diagnostic predicates disagree with production for "+asset+" "+c+" "+failures);
            return new Validation(c,family,asset,failures.isEmpty()?"accepted_terrain":failures.keySet().iterator().next(),failures,actual,biomeId,surface);
        }
        @SuppressWarnings("unchecked") private List<Site> anchors(Candidate c) {
            Site nominal=new Site(c,"",2*c.x(),2*c.z(),0,0,0,0,0,0,0,0);
            if(!snapshot.policy.equals(LEGACY_POLICY))return (List<Site>)invoke(planner,"anchorsAt",new Class<?>[]{Site.class,int.class},nominal,REGION);
            int extra=snapshot.policy.equals(LEGACY_POLICY)?0:LocationSearch.RADIUS;
            List<Candidate> neighbors=(List<Candidate>)invoke(planner,"neighbors",new Class<?>[]{Site.class,int.class},nominal,REGION+2+extra);
            List<Site> result=new ArrayList<>();
            for(Candidate neighbor:neighbors) {
                Site anchor=(Site)invoke(planner,"obelisk",new Class<?>[]{Candidate.class},neighbor);
                if(anchor!=null && within(nominal,anchor,REGION+2,true))result.add(anchor);
            }
            return result;
        }
        void run()throws Exception {
            long started=System.nanoTime();
            int loX=snapshot.spawnX-60000,hiX=snapshot.spawnX+60000,loZ=snapshot.spawnZ-60000,hiZ=snapshot.spawnZ+60000;
            List<Map<String,Object>> cells=new ArrayList<>();List<Site> accepted=new ArrayList<>();
            Map<String,Integer> outcomes=new TreeMap<>(),assigned=new TreeMap<>(),acceptedTypes=new TreeMap<>();
            for(int x=Math.floorDiv(loX,CELL);x<=Math.floorDiv(hiX-1,CELL);x++)
                for(int z=Math.floorDiv(loZ,CELL);z<=Math.floorDiv(hiZ-1,CELL);z++) {
                    Candidate c=candidate(level.getSeed(),new Cell(x,z),false);
                    if(c.x()<loX || c.x()>=hiX || c.z()<loZ || c.z()>=hiZ)continue;
                    Site site=planner.plan(c.cell());List<Site> nearby=anchors(c);
                    Family family=ticket(c.ticket(),!nearby.isEmpty());
                    assigned.merge(family.name(),1,Integer::sum);
                    String reason;
                    if(site!=null) {reason="accepted";accepted.add(site);acceptedTypes.merge(family.name(),1,Integer::sum);}
                    else if(family==Family.EMPTY)reason="empty_ticket";
                    else {
                        Validation validation=validations.get(key(c,family));
                        if(validation==null)throw new AssertionError("Missing validation attribution "+c+" "+family);
                        if(validation.site==null)reason=snapshot.policy.equals(LEGACY_POLICY)?validation.primary:"no_valid_local_position";
                        else if(snapshot.unique!=null && within(validation.site,snapshot.unique,SEPARATION,false))reason="large_colossus_spacing";
                        else reason="neighbor_spacing_or_priority";
                    }
                    outcomes.merge(reason,1,Integer::sum);
                    Map<String,Object> record=new LinkedHashMap<>();record.put("candidate",c);record.put("inside_obelisk_region",!nearby.isEmpty());
                    record.put("family",family);record.put("outcome",reason);if(site!=null)record.put("site",site);cells.add(record);
                }
            for(int i=0;i<accepted.size();i++)for(int j=i+1;j<accepted.size();j++) {
                Site a=accepted.get(i),b=accepted.get(j);
                if(within(a,b,SEPARATION,false))throw new AssertionError("Accepted sites violate separation");
                if(a.asset().equals("obelisk") && b.asset().equals("obelisk") && within(a,b,OBELISK_SEPARATION,false))throw new AssertionError("Accepted Obelisks violate separation");
            }
            // Compare fresh production decisions in reverse order. This reuses
            // the actual runtime planner and its independent caches.
            var production=(DistributionPlanner)field(runtime,"planner");
            for(int i=cells.size()-1;i>=0;i--) {
                Map<String,Object> row=cells.get(i);Candidate c=(Candidate)row.get("candidate");
                if(!Objects.equals(row.get("site"),production.plan(c.cell())))throw new AssertionError("Production/reverse-order plan differs "+c.cell());
            }
            Map<String,Object> output=new LinkedHashMap<>();output.put("seed",level.getSeed());output.put("snapshot",snapshot);
            output.put("window",List.of(loX,loZ,hiX,hiZ));output.put("cell_count",cells.size());output.put("assigned",assigned);output.put("outcomes",outcomes);
            output.put("accepted_by_family",acceptedTypes);output.put("accepted_sites",accepted);output.put("cells",cells);
            output.put("unique_validation_count",validations.size());output.put("validation_calls",validationCalls);output.put("validations",validations.values());
            output.put("distinct_location_probes",explainedProbes.size());output.put("probe_outcomes",probeOutcomes);
            output.put("production_reverse_order_match",true);output.put("elapsed_seconds",(System.nanoTime()-started)/1e9);
            Path target=Path.of(System.getProperty("relics.audit.output","audit.json"));Files.writeString(target,JSON.toJson(output)+"\n");
            System.out.println("RELIC_AUDIT_READY seed="+level.getSeed()+" cells="+cells.size()+" accepted="+accepted.size()+" seconds="+((System.nanoTime()-started)/1e9));
        }
    }
}
