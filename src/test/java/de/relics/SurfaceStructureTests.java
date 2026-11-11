package de.relics;

import de.relics.distribution.*;
import com.google.gson.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import static de.relics.distribution.DistributionPlanner.*;
import static de.relics.distribution.SurfaceStructurePolicy.*;

/** Frozen saves, complete-stage publication and geometry regressions independent of a running server. */
public final class SurfaceStructureTests {
    private static int checks;
    private static void check(boolean ok,String why){checks++;if(!ok)throw new AssertionError(why);}
    private static void rejects(Runnable r,String why){boolean rejected=false;try{r.run();}catch(RuntimeException expected){rejected=true;}check(rejected,why);}
    public static void main(String[] args)throws Exception {
        var policy=new State(1,1024,List.of("minecraft:village_plains","test:mine"),List.of("test:mine"));
        check(policy.eligible("minecraft:village_plains") && !policy.eligible("test:mine") && !policy.eligible("relics:colossus") && !policy.eligible("other:unknown"),"explicit targets, exemptions and unknown preservation");
        rejects(()->new State(2,1024,List.of(),List.of()),"unknown revision refused");
        rejects(()->new State(1,1024,List.of("relics:obelisk"),List.of()),"own relic cannot be filtered");
        rejects(()->new State(1,1024,List.of("test:one","test:one"),List.of()),"ambiguous duplicate IDs refused");
        Map<String,Boolean> order=new HashMap<>();int selected=0;
        for(int i=0;i<10000;i++){String id="test:start_"+i;boolean bit=selected(731204,"minecraft:overworld",id,-81,i);order.put(id,bit);if(bit)selected++;}
        check(selected>4700 && selected<5300,"independent half-sampling across 10000 start IDs");
        for(int i=9999;i>=0;i--)check(order.get("test:start_"+i)==selected(731204,"minecraft:overworld","test:start_"+i,-81,i),"reverse/repeated requests keep the same decision");
        check(bootstrap(policy,8,8,0,0,List.of()),"initial start chunk always preserved");
        check(bootstrap(policy,8,8,200,200,List.of(new Box(0,70,0,10,80,10))),"distant start reaching initial area preserved");
        check(!bootstrap(policy,8,8,200,200,List.of(new Box(3200,70,3200,3210,80,3210))),"distant structure eligible after bootstrap");
        var cells=cells(List.of(new Box(-2001,70,-1,-1999,80,1)),2000,128).orElseThrow();
        check(cells.contains(new Cell(-2,-1)) && cells.contains(new Cell(-1,0)),"negative boundary and neighboring center cells included");
        check(cells(List.of(new Box(-1000000,0,-1000000,1000000,10,1000000)),1500,128).isEmpty(),"oversized unsupported shape bounded before planning");
        var shape=new TemplateOccupancy(5,6,7,List.of(new int[]{1,2,3}));
        int[][] offsets={{1,3},{-3,1},{-1,-3},{3,-1}};
        for(int rot=0;rot<4;rot++) {
            int x=-100+offsets[rot][0],z=-200+offsets[rot][1];
            check(shape.intersects(new Box(x,72,z,x,72,z),-100,70,-200,rot),"rotated occupied voxel");
            check(!shape.intersects(new Box(x,73,z,x,80,z),-100,70,-200,rot),"vertical separation");
            check(!shape.intersects(new Box(x+1,72,z,x+1,72,z),-100,70,-200,rot),"empty model volume not collision");
        }
        Path file=Path.of(args[0]).resolve("surface-journal.json");
        var state=new DistributionJournal.State();state.fingerprint="a".repeat(64);state.seed=731204;state.enabled=EnumSet.allOf(Family.class);
        state.minX=state.minZ=-100000;state.maxX=state.maxZ=100000;state.frozen=true;
        var old=new DistributionJournal(file,state);old.flush();String original=Files.readString(file);
        check(JsonParser.parseString(original).getAsJsonObject().get("version").getAsInt()==1,"old saves keep envelope 1");
        var loaded=new DistributionJournal(file,null);check(loaded.state.surfaceStructures==null,"missing filter remains disabled");loaded.flush();check(Files.readString(file).equals(original),"legacy save bytes remain identical");
        state.surfaceStructures=policy;var fresh=new DistributionJournal(file.resolveSibling("new-surface.json"),state);fresh.flush();
        var envelope=JsonParser.parseString(Files.readString(file.resolveSibling("new-surface.json"))).getAsJsonObject();
        check(envelope.get("version").getAsInt()==2,"new policy has downgrade-rejecting envelope");
        check(new DistributionJournal(file.resolveSibling("new-surface.json"),null).state.surfaceStructures.equals(policy),"policy snapshot survives reload");
        envelope.addProperty("version",1);Path invalid=file.resolveSibling("wrong-surface.json");Files.writeString(invalid,envelope.toString());
        rejects(()->new DistributionJournal(invalid,null),"policy cannot silently enter old envelope");
        // Querying plans for foreign starts must not change the distribution or depend on query order.
        var settings=DistributionSettings.DISCOVERY;
        DistributionPlanner.Validator terrain=(c,f)->new Site(c,f==Family.SKULL?"titan_skull_sand":f.id,2*c.x(),2*c.z(),70,c.x(),50,c.z(),c.x()-50,c.z()-50,c.x()+50,c.z()+50);
        for(int seed=0;seed<8;seed++) {
            var a=new DistributionPlanner(settings.policy(),settings,seed,EnumSet.allOf(Family.class),terrain,()->null,()->true,0,0,128);
            var b=new DistributionPlanner(settings.policy(),settings,seed,EnumSet.allOf(Family.class),terrain,()->null,()->true,0,0,128);
            Map<Cell,Site> baseline=new HashMap<>();
            for(int x=-4;x<=4;x++)for(int z=-4;z<=4;z++)baseline.put(new Cell(x,z),a.plan(new Cell(x,z)));
            for(int x=5;x>=-5;x--)for(int z=5;z>=-5;z--)b.plan(new Cell(x,z));
            for(var e:baseline.entrySet())check(Objects.equals(e.getValue(),b.plan(e.getKey())),"foreign-query halo leaves relic plans unchanged");
        }
        Queue<Runnable> lane=new ConcurrentLinkedQueue<>();AtomicInteger applied=new AtomicInteger(),published=new AtomicInteger();
        var publication=new StructurePublication();publication.capture(published::incrementAndGet);var pending=new CompletableFuture<Runnable>();
        var result=publication.finish(CompletableFuture.completedFuture(17),chunk->pending,lane::add);
        Thread planner=new Thread(()->pending.complete(applied::incrementAndGet));planner.start();planner.join();
        check(!result.isDone() && published.get()==0 && applied.get()==0,"no cache/status publication while decision pending");
        check(lane.size()==1,"exactly one native continuation");lane.remove().run();
        check(result.getNow(-1)==17 && published.get()==1 && applied.get()==1,"filter then single native publication");
        rejects(()->publication.capture(()->{}),"duplicate publication forbidden");
        var failed=new StructurePublication();failed.capture(published::incrementAndGet);
        check(failed.finish(CompletableFuture.completedFuture(0),v->CompletableFuture.failedFuture(new IllegalStateException("failed")),lane::add).isCompletedExceptionally(),"failed plan cannot publish");
        check(published.get()==1,"failed plan did not release cache");
        System.out.println("PASS: "+checks+" surface-structure policy/geometry/publication assertions");
    }
}
