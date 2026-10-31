package de.relics.distribution;

import com.google.gson.GsonBuilder;
import de.relics.gameplay.GameplayLedger.Point;
import de.relics.gameplay.RelicGameplay;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.commands.Commands;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.*;
import net.minecraft.world.level.chunk.*;
import net.minecraft.world.level.levelgen.structure.*;
import net.minecraft.world.level.storage.LevelResource;
import org.slf4j.LoggerFactory;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.*;
import static de.relics.distribution.DistributionPlanner.*;

/** Serial planning actor and asynchronous STRUCTURE_STARTS dependency. Never waits on a chunk. */
public final class DistributionRuntime implements AutoCloseable {
    public static final int LOCATE_RADIUS=500000;
    private static final org.slf4j.Logger LOG=LoggerFactory.getLogger("relics/distribution");
    private static final Map<ServerLevel,DistributionRuntime> LEVELS=new ConcurrentHashMap<>();
    private static final Map<ChunkGeneratorStructureState,DistributionRuntime> STATES=new ConcurrentHashMap<>();
    private record Generation(DistributionRuntime runtime,Site site) { }
    private static final ThreadLocal<Generation> GENERATING=new ThreadLocal<>();
    private final ServerLevel level;
    private final ScheduledExecutorService actor;
    private final TerrainValidator validator;
    private final DistributionJournal journal;
    private final DistributionPlanner planner;
    private final CompletableFuture<Void> ready=new CompletableFuture<>();
    private final Map<Cell,CompletableFuture<Site>> decisions=new LinkedHashMap<>(64,.75f,true);
    private final Map<Cell,CompletableFuture<Site>> selections=new LinkedHashMap<>(64,.75f,true);
    private volatile Site unique;
    private volatile boolean unavailable,closed;
    private volatile Throwable failure;
    private List<Candidate> annulus;
    private long materialized;

    private DistributionRuntime(ServerLevel level,boolean fresh) {
        this.level=level;
        Path file=level.getServer().getWorldPath(LevelResource.ROOT).resolve("data/relics_distribution_v1.json");
        var border=level.getWorldBorder();
        DistributionJournal.State initial=new DistributionJournal.State();
        initial.interiors=fresh?de.relics.gameplay.NaturalInteriors.REVISION:DistributionJournal.interiorRevision(file);
        if(fresh){initial.settings=DistributionConfig.load();initial.policy=DistributionSettings.POLICY;}
        initial.seed=level.getSeed();
        int absolute=Math.min(29999984,level.getServer().getAbsoluteMaxWorldSize());
        initial.minX=(int)Math.ceil(Math.max(-absolute,border.getMinX())); initial.maxX=(int)Math.floor(Math.min(absolute,border.getMaxX()));
        initial.minZ=(int)Math.ceil(Math.max(-absolute,border.getMinZ())); initial.maxZ=(int)Math.floor(Math.min(absolute,border.getMaxZ()));
        validator=new TerrainValidator(level,initial.minX,initial.minZ,initial.maxX,initial.maxZ,initial.interiors);
        initial.fingerprint=validator.fingerprint;initial.fingerprintFormat=PlanningFingerprint.FORMAT;initial.enabled=Set.copyOf(validator.enabled);
        BlockPos approximate=level.getChunkSource().randomState().sampler().findSpawnPosition();
        initial.bootstrapX=Math.floorDiv(approximate.getX(),16)*16+8;initial.bootstrapZ=Math.floorDiv(approximate.getZ(),16)*16+8;
        journal=new DistributionJournal(file,initial);
        var s=journal.state;
        boolean legacy=s.fingerprintFormat==0;
        boolean fingerprintMatches=legacy
                ? PlanningFingerprint.legacyMatches(s.fingerprint,validator.legacyFingerprint,validator.fingerprint,
                        System.getProperty(PlanningFingerprint.RECOVERY_PROPERTY,""))
                : s.fingerprint.equals(validator.fingerprint);
        if(s.seed!=initial.seed || !fingerprintMatches || !s.enabled.equals(initial.enabled)
                || s.minX!=initial.minX || s.maxX!=initial.maxX || s.minZ!=initial.minZ || s.maxZ!=initial.maxZ)
            throw new IllegalStateException("Relic planning settings/generator/assets/border differ from the frozen save. "
                    +"Preserve the save and verify the original setup. Saved fingerprint="+s.fingerprint
                    +", current fingerprint="+validator.fingerprint+", format="+s.fingerprintFormat);
        if(!fresh && !s.frozen)throw new IllegalStateException("Interrupted initial spawn has no frozen relic snapshot; preserve the save for recovery.");
        if(s.unique!=null && !s.unique.equals(validator.validate(s.unique.candidate(),Family.COLOSSUS)))
            throw new IllegalStateException("Saved unique destination no longer matches the exact terrain/transform contract");
        if(legacy) {
            boolean recovery=!s.fingerprint.equals(validator.legacyFingerprint);
            journal.migrateFingerprint(validator.fingerprint);
            LOG.info("Migrated {} legacy planning fingerprint to canonical JSON format; original journal backed up",
                    recovery?"explicitly approved":"exactly matching");
        }
        unique=s.unique;unavailable=s.unavailable;
        planner=new DistributionPlanner(s.policy,s.settings==null?DistributionSettings.EXPEDITION:s.settings,s.seed,s.enabled,validator,()->unique,()->unavailable,s.bootstrapX,s.bootstrapZ,128);
        actor=Executors.newSingleThreadScheduledExecutor(r->{Thread t=new Thread(r,"Relic planning "+s.seed);t.setDaemon(true);return t;});
        if(fresh)journal.flush();
        if(s.frozen)startResolver();
        LOG.info("Attached {} relic planning snapshot {}",fresh?"new":"saved",s.fingerprint);
    }
    public static void initialize() {
        ServerLifecycleEvents.SERVER_STOPPING.register(server->{for(var runtime:List.copyOf(LEVELS.values()))if(runtime.level.getServer()==server)runtime.close();});
        ServerLifecycleEvents.END_DATA_PACK_RELOAD.register((server,resources,success)->{
            if(!success)return;
            for(var runtime:LEVELS.values())if(runtime.level.getServer()==server) {
                var s=runtime.journal.state;
                try {
                    var current=new TerrainValidator(runtime.level,s.minX,s.minZ,s.maxX,s.maxZ,s.interiors);
                    if(!current.fingerprint.equals(s.fingerprint) || !current.enabled.equals(s.enabled))
                        throw new IllegalStateException("Datapack reload changed frozen relic settings. Restore the original setup and restart; policy migration requires a fresh world.");
                    LOG.info("Relic distribution settings unchanged after datapack reload");
                }catch(Throwable error){runtime.fail(error);}
            }
        });
        ServerTickEvents.START_SERVER_TICK.register(DistributionRuntime::publishTarget);
        CommandRegistrationCallback.EVENT.register((dispatcher,registries,environment)->dispatcher.register(
            Commands.literal("relicsdistribution").requires(source->source.permissions().hasPermission(net.minecraft.server.permissions.Permissions.COMMANDS_GAMEMASTER))
                .then(Commands.literal("status").executes(context->{
                    DistributionRuntime runtime=get(context.getSource().getLevel());
                    if(runtime==null){context.getSource().sendSuccess(()->Component.literal("Legacy world: Alpha 4.9 placement retained. Gameplay distribution requires a fresh world."),false);return 0;}
                    runtime.actor.execute(()->{
                        String report=runtime.status();
                        context.getSource().getServer().execute(()->context.getSource().sendSuccess(()->Component.literal(report),false));
                    });return 1;
                }))
                .then(Commands.literal("plan").then(Commands.argument("x",com.mojang.brigadier.arguments.IntegerArgumentType.integer(-29999984,29999984))
                    .then(Commands.argument("z",com.mojang.brigadier.arguments.IntegerArgumentType.integer(-29999984,29999984)).executes(context->{
                        var source=context.getSource();var runtime=get(source.getLevel());if(runtime==null)return 0;
                        Cell cell=new Cell(Math.floorDiv(com.mojang.brigadier.arguments.IntegerArgumentType.getInteger(context,"x"),runtime.planner.cellSize()),
                                Math.floorDiv(com.mojang.brigadier.arguments.IntegerArgumentType.getInteger(context,"z"),runtime.planner.cellSize()));
                        runtime.decision(cell).whenComplete((site,error)->source.getServer().execute(()->{
                            if(error!=null)source.sendFailure(Component.literal("Relic plan paused: "+error.getMessage()));
                            else source.sendSuccess(()->Component.literal("Relic plan "+cell+": "+new GsonBuilder().create().toJson(site)),false);
                        }));return 1;
                    }))))
                .then(Commands.literal("map").executes(context->{
                    var source=context.getSource();var player=source.getPlayerOrException();
                    if(get(source.getServer().overworld())==null)throw new com.mojang.brigadier.exceptions.SimpleCommandExceptionType(Component.literal("Natural expedition maps require a gameplay distribution world.")).create();
                    var map=RelicGameplay.createPendingMap(source.getLevel(),"distribution:operator:"+UUID.randomUUID());
                    if(!player.getInventory().add(map))player.drop(map,false);
                    return 1;
                }))));
    }
    public static DistributionRuntime get(ServerLevel level){return LEVELS.get(level);}
    public String interiorRevision(){return journal.state.interiors;}
    public static void attach(ServerLevel level,boolean fresh) {
        if(level.dimension()!=Level.OVERWORLD || LEVELS.containsKey(level))return;
        Path file=level.getServer().getWorldPath(LevelResource.ROOT).resolve("data/relics_distribution_v1.json");
        if(!fresh && !Files.exists(file)) { LOG.info("Existing world has no gameplay distribution snapshot; preserving legacy relic placement");return; }
        var runtime=new DistributionRuntime(level,fresh);
        LEVELS.put(level,runtime);STATES.put(level.getChunkSource().getGeneratorState(),runtime);
    }
    public static void finishSpawn(ServerLevel level) {
        var runtime=get(level);if(runtime==null)return;
        BlockPos pos=level.getServer().getWorldData().overworldData().getRespawnData().pos();
        var s=runtime.journal.state;
        if(Math.hypot((double)pos.getX()-s.bootstrapX,(double)pos.getZ()-s.bootstrapZ)>128)
            throw new IllegalStateException("Initial spawn exceeded vanilla's bounded spawn search; relic planning cannot safely continue");
        s.spawnX=pos.getX();s.spawnZ=pos.getZ();s.frozen=true;runtime.journal.flush();runtime.startResolver();
    }
    private void startResolver() {
        if(unique!=null || unavailable){ready.complete(null);return;}
        actor.execute(()->guard(this::resolveSlice));
    }
    private void resolveSlice() {
        if(closed || failure!=null)return;
        var s=journal.state;
        if(!s.enabled.contains(Family.COLOSSUS)) {s.unavailable=true;s.unavailableReason="disabled before destination";commitResolution();return;}
        long deadline=System.nanoTime()+2000000;
        for(int n=0;n<8;n++) {
            if(closed)return;
            if(annulus==null)annulus=DistributionPlanner.annulus(s.seed,s.spawnX,s.spawnZ,s.lower,s.upper,s.minX,s.minZ,s.maxX,s.maxZ);
            if(s.cursor>=annulus.size()) {
                double farthest=Math.max(Math.max(Math.hypot((double)s.minX-s.spawnX,(double)s.minZ-s.spawnZ),Math.hypot((double)s.maxX-s.spawnX,(double)s.maxZ-s.spawnZ)),
                        Math.max(Math.hypot((double)s.minX-s.spawnX,(double)s.maxZ-s.spawnZ),Math.hypot((double)s.maxX-s.spawnX,(double)s.minZ-s.spawnZ)));
                if(s.upper>farthest+2){s.unavailable=true;s.unavailableReason="finite frozen world border exhausted";commitResolution();return;}
                s.lower=s.upper;s.upper=Math.addExact(s.upper,20000);s.cursor=0;annulus=null;
                break;
            }
            Candidate candidate=annulus.get(s.cursor);
            long start=System.nanoTime();Site site=validator.validate(candidate,Family.COLOSSUS);
            s.maxEvaluationNanos=Math.max(s.maxEvaluationNanos,System.nanoTime()-start);s.candidatesChecked++;
            if(site!=null) {
                long dx=(long)site.x2()-2L*s.spawnX,dz=(long)site.z2()-2L*s.spawnZ;
                if(dx*dx+dz*dz>=4L*UNIQUE_MIN*UNIQUE_MIN){s.unique=site;commitResolution();return;}
            }
            s.cursor++;
            if(System.nanoTime()>=deadline)break;
        }
        s.slices++;journal.flush();if(!closed)actor.schedule(()->guard(this::resolveSlice),1,TimeUnit.MILLISECONDS);
    }
    private void commitResolution() {
        journal.flush();unique=journal.state.unique;unavailable=journal.state.unavailable;
        ready.complete(null);
        LOG.info("Relic destination {} after {} candidates; slowest terrain evaluation {} ms",unique==null?journal.state.unavailableReason:unique,journal.state.candidatesChecked,journal.state.maxEvaluationNanos/1000000.0);
    }
    private void guard(Runnable operation){try{operation.run();}catch(Throwable error){fail(error);}}
    private void fail(Throwable error) {
        if(failure!=null || closed)return;failure=error;LOG.error("Relic planning stopped; no speculative placement or replacement destination",error);
        ready.completeExceptionally(error);
        synchronized(decisions){for(var future:decisions.values())future.completeExceptionally(error);}
        synchronized(selections){for(var future:selections.values())future.completeExceptionally(error);}
    }
    private CompletableFuture<Site> decision(Cell cell) {
        return request(cell,false);
    }
    private CompletableFuture<Site> request(Cell cell,boolean selectionOnly) {
        var requests=selectionOnly?selections:decisions;
        synchronized(requests) {
            var existing=requests.get(cell);if(existing!=null)return existing;
            if(failure!=null)return CompletableFuture.failedFuture(failure);
            if(closed)return CompletableFuture.failedFuture(new CancellationException("World stopping"));
            var future=new CompletableFuture<Site>();requests.put(cell,future);
            // Completed entries alone may be evicted. Pending requests are shared.
            if(requests.size()>2048) {
                var iterator=requests.entrySet().iterator();
                while(requests.size()>2048 && iterator.hasNext()){var e=iterator.next();if(e.getValue().isDone())iterator.remove();}
            }
            actor.execute(()->evaluate(cell,future,selectionOnly));return future;
        }
    }
    private void evaluate(Cell cell,CompletableFuture<Site> future,boolean selectionOnly) {
        try {
            if(failure!=null)throw new IllegalStateException("Planning paused",failure);
            future.complete(selectionOnly?planner.candidateChoice(cell):planner.plan(cell));
        } catch(Pending pending) {
            ready.whenComplete((ignored,error)->{if(error!=null)future.completeExceptionally(error);else actor.execute(()->evaluate(cell,future,selectionOnly));});
        } catch(Throwable error){future.completeExceptionally(error);fail(error);}
    }
    private CompletableFuture<Site> ordinaryAt(Cell cell,ChunkPos pos) {
        if(journal.state.policy.equals(LEGACY_POLICY))return decision(cell);
        return request(cell,true).thenCompose(site->site!=null && site.candidate().chunkX()==pos.x() && site.candidate().chunkZ()==pos.z()
                ?decision(cell):CompletableFuture.completedFuture(null));
    }
    public static CompletableFuture<ChunkAccess> beforeStarts(ServerLevel level,ChunkAccess chunk,
            Supplier<CompletableFuture<ChunkAccess>> original,Executor worldgenExecutor) {
        var runtime=get(level);if(runtime==null)return original.get();
        if(runtime.failure!=null)return CompletableFuture.failedFuture(runtime.failure);
        ChunkPos pos=chunk.getPos();
        int size=runtime.planner.cellSize();
        Cell cell=new Cell(Math.floorDiv(pos.getMinBlockX(),size),Math.floorDiv(pos.getMinBlockZ(),size));
        Cell largeCell=new Cell(Math.floorDiv(pos.getMinBlockX(),CELL),Math.floorDiv(pos.getMinBlockZ(),CELL));
        Candidate ordinary=runtime.planner.ordinaryCandidate(cell),large=candidate(level.getSeed(),largeCell,true);
        CompletableFuture<Site> result;
        boolean ordinaryChunk=runtime.journal.state.policy.equals(LEGACY_POLICY)
                ?pos.x()==ordinary.chunkX() && pos.z()==ordinary.chunkZ():LocationSearch.mayContain(ordinary,pos.x(),pos.z());
        boolean possibleLarge=distance(large,runtime.journal.state.bootstrapX,runtime.journal.state.bootstrapZ)>=UNIQUE_MIN-182;
        if(pos.x()==large.chunkX() && pos.z()==large.chunkZ() && possibleLarge) {
            result=runtime.ready.thenCompose(ignored->runtime.unique!=null && runtime.unique.candidate().cell().equals(largeCell)
                    ?CompletableFuture.completedFuture(runtime.unique):ordinaryChunk?runtime.ordinaryAt(cell,pos):CompletableFuture.completedFuture(null));
        } else if(ordinaryChunk)result=runtime.ordinaryAt(cell,pos);
        else result=CompletableFuture.completedFuture(null);
        return WorldgenGate.resume(result,site->{
            if(runtime.failure!=null)return CompletableFuture.failedFuture(runtime.failure);
            Site placed=site!=null && site.candidate().chunkX()==pos.x() && site.candidate().chunkZ()==pos.z()?site:null;
            GENERATING.set(new Generation(runtime,placed));
            try{return original.get();}finally{GENERATING.remove();}
        },worldgenExecutor);
    }
    /** null means this is not a managed relic placement. */
    public static Boolean placement(Object placement,ChunkGeneratorStructureState state,int chunkX,int chunkZ) {
        var runtime=STATES.get(state);if(runtime==null)return null;
        Family family=runtime.validator.placement(placement);if(family==null)return null;
        Generation current=GENERATING.get();
        return current!=null && current.runtime==runtime && current.site!=null
                && current.site.candidate().chunkX()==chunkX && current.site.candidate().chunkZ()==chunkZ
                && family.id.equals(familyOf(current.site.asset()));
    }
    private static String familyOf(String asset){return asset.startsWith("titan_skull_") && !asset.equals("titan_skull_2")?"titan_skull":asset;}
    public static StructureStart generate(Structure structure) {
        Generation current=GENERATING.get();if(current==null)return null;
        String asset=current.runtime.validator.structure(structure);if(asset==null)return null;
        if(current.site==null || !current.site.asset().equals(asset))return StructureStart.INVALID_START;
        current.runtime.actor.execute(()->current.runtime.materialized++);
        return current.runtime.validator.start(current.site);
    }
    private static void publishTarget(MinecraftServer server) {
        var runtime=get(server.overworld());if(runtime==null || !runtime.ready.isDone() || runtime.failure!=null)return;
        var ledger=RelicGameplay.ledger(server);Site site=runtime.unique;
        Point target=site==null?null:new Point("minecraft:overworld",site.x(),site.surface(),site.z());
        if(ledger.state.committedTarget!=null && !ledger.state.committedTarget.equals(target))
            throw new IllegalStateException("Gameplay ledger destination conflicts with frozen distribution snapshot");
        if(!Objects.equals(ledger.state.committedTarget,target) || ledger.state.targetUnavailable!=runtime.unavailable) {
            ledger.state.committedTarget=target;ledger.state.targetUnavailable=runtime.unavailable;ledger.flush();
        }
    }
    public CompletableFuture<Site> locate(Predicate<Holder<Structure>> requested,BlockPos origin) {
        var result=new CompletableFuture<Site>();
        ready.whenComplete((ignored,error)->{
            if(error!=null){result.completeExceptionally(error);return;}
            actor.execute(()->{
                Site initial=unique!=null && requested.test(validator.holder(unique.asset()))?unique:null;
                var families=validator.repeatableFamilies(requested);
                if(families.isEmpty()){result.complete(initial);return;}
                List<Candidate> cells=new ArrayList<>();
                int radius=LOCATE_RADIUS;
                int margin=journal.state.policy.equals(LEGACY_POLICY)?0:LocationSearch.RADIUS;
                for(int x=Math.floorDiv(origin.getX()-radius-margin,planner.cellSize());x<=Math.floorDiv(origin.getX()+radius+margin,planner.cellSize());x++)
                    for(int z=Math.floorDiv(origin.getZ()-radius-margin,planner.cellSize());z<=Math.floorDiv(origin.getZ()+radius+margin,planner.cellSize());z++) {
                        Candidate c=planner.ordinaryCandidate(new Cell(x,z));
                        if(distance(c,origin.getX(),origin.getZ())<=radius+margin+2 && planner.mayMatch(c.ticket(),families))cells.add(c);
                    }
                cells.sort(Comparator.comparingDouble(c->distance(c,origin.getX(),origin.getZ())));
                locateSlice(cells,0,initial,requested,origin,result);
            });
        });return result;
    }
    private void locateSlice(List<Candidate> cells,int cursor,Site best,Predicate<Holder<Structure>> requested,BlockPos origin,CompletableFuture<Site> result) {
        if(result.isDone())return;
        if(failure!=null){result.completeExceptionally(failure);return;}
        try {
            long deadline=System.nanoTime()+2000000;
            for(int count=0;count<8 && cursor<cells.size();count++,cursor++) {
                Candidate c=cells.get(cursor);
                if(best!=null && locateLowerBound(c,origin)>Math.hypot((double)best.x()-origin.getX(),(double)best.z()-origin.getZ())+2)break;
                Site site=planner.plan(c.cell());
                if(site!=null && Math.hypot((double)site.x()-origin.getX(),(double)site.z()-origin.getZ())<=LOCATE_RADIUS
                        && requested.test(validator.holder(site.asset())) && (best==null
                        || Math.hypot((double)site.x()-origin.getX(),(double)site.z()-origin.getZ())<Math.hypot((double)best.x()-origin.getX(),(double)best.z()-origin.getZ())))best=site;
                if(System.nanoTime()>=deadline){cursor++;break;}
            }
            if(cursor>=cells.size() || best!=null && locateLowerBound(cells.get(cursor),origin)>Math.hypot((double)best.x()-origin.getX(),(double)best.z()-origin.getZ())+2)result.complete(best);
            else {int next=cursor;Site found=best;actor.schedule(()->locateSlice(cells,next,found,requested,origin,result),1,TimeUnit.MILLISECONDS);}
        }catch(Throwable error){result.completeExceptionally(error);fail(error);}
    }
    private double locateLowerBound(Candidate candidate,BlockPos origin) {
        return distance(candidate,origin.getX(),origin.getZ())-(journal.state.policy.equals(LEGACY_POLICY)?0:LocationSearch.RADIUS);
    }
    public Holder<Structure> holder(Site site){return validator.holder(site.asset());}
    public com.mojang.datafixers.util.Pair<BlockPos,Holder<Structure>> mapTarget(net.minecraft.core.HolderSet<Structure> requested) {
        Site site=unique;
        if(failure!=null)throw new IllegalStateException("Relic planning paused",failure);
        if(site==null || !requested.contains(validator.holder(site.asset())))return null;
        return com.mojang.datafixers.util.Pair.of(new BlockPos(site.x(),site.surface(),site.z()),validator.holder(site.asset()));
    }
    public String status() {
        var report=new LinkedHashMap<String,Object>();report.put("policy",journal.state.policy);report.put("snapshot",journal.state);
        report.put("pending",!ready.isDone());report.put("failure",failure==null?null:failure.toString());
        report.put("opportunityQueries",planner.opportunities);report.put("terrainChecks",planner.terrainChecks);report.put("terrainRejected",planner.terrainRejected);
        report.put("spacingRejected",planner.spacingRejected);report.put("acceptedQueries",planner.acceptedQueries);report.put("materializedStartEvents",materialized);
        report.put("locationAttempts",planner.locationAttempts);
        return new GsonBuilder().create().toJson(report);
    }
    @Override public void close() {
        closed=true;
        var cancellation=new CancellationException("World stopping; pending planning will resume from its journal");
        ready.completeExceptionally(cancellation);
        synchronized(decisions){for(var future:decisions.values())future.completeExceptionally(cancellation);}
        synchronized(selections){for(var future:selections.values())future.completeExceptionally(cancellation);}
        actor.shutdown();
        try{if(!actor.awaitTermination(5,TimeUnit.SECONDS))actor.shutdownNow();}catch(InterruptedException interrupted){actor.shutdownNow();Thread.currentThread().interrupt();}
        LEVELS.remove(level);STATES.remove(level.getChunkSource().getGeneratorState());
    }
}
