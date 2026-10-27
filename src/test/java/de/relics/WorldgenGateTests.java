package de.relics;

import de.relics.distribution.WorldgenGate;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/** Executor ownership and dependency publication, without sleeps or a Minecraft mock. */
public final class WorldgenGateTests {
    private static int checks;
    private static void check(boolean value,String message){checks++;if(!value)throw new AssertionError(message);}
    public static void main(String[] args)throws Exception {
        Thread caller=Thread.currentThread();AtomicReference<Thread> generated=new AtomicReference<>();
        var immediate=WorldgenGate.resume(CompletableFuture.completedFuture(7),value->{
            generated.set(Thread.currentThread());return CompletableFuture.completedFuture(value+1);
        },task->{throw new AssertionError("Already planned work was needlessly dispatched");});
        check(immediate.getNow(-1)==8 && generated.get()==caller,"synchronous native lane is retained");
        Queue<Runnable> nativeLane=new ConcurrentLinkedQueue<>();CompletableFuture<Integer> pending=new CompletableFuture<>();
        AtomicInteger published=new AtomicInteger();
        var waiting=WorldgenGate.resume(pending,value->{
            check(Thread.currentThread()==caller,"planner completion must not mutate a chunk");
            return CompletableFuture.completedFuture(value);
        },nativeLane::add).thenApply(value->{published.set(value);return value;});
        Thread planner=new Thread(()->pending.complete(11),"planning-worker");planner.start();planner.join();
        check(!waiting.isDone() && published.get()==0,"planning completion alone cannot publish native status");
        check(nativeLane.size()==1,"pending continuation queued exactly once");nativeLane.remove().run();
        check(waiting.getNow(-1)==11 && published.get()==11,"status publication completes on the native lane");
        AtomicInteger mutations=new AtomicInteger();var failed=WorldgenGate.resume(CompletableFuture.failedFuture(new IllegalStateException("invalid plan")),
                value->{mutations.incrementAndGet();return CompletableFuture.completedFuture(value);},nativeLane::add);
        check(failed.isCompletedExceptionally() && mutations.get()==0 && nativeLane.isEmpty(),"failed plan cannot generate");
        var stopped=new CompletableFuture<Integer>();var canceled=WorldgenGate.resume(stopped,value->{mutations.incrementAndGet();return CompletableFuture.completedFuture(value);},nativeLane::add);
        stopped.cancel(false);check(canceled.isCompletedExceptionally() && mutations.get()==0,"canceled plans cannot generate");
        ExecutorService lane=Executors.newSingleThreadExecutor(r->new Thread(r,"native-worldgen"));
        ExecutorService planners=Executors.newFixedThreadPool(4);
        try {
            List<CompletableFuture<Integer>> jobs=new ArrayList<>();AtomicInteger active=new AtomicInteger(),completed=new AtomicInteger();
            for(int i=0;i<1000;i++) {
                int id=i;var plan=new CompletableFuture<Integer>();var result=new CompletableFuture<Integer>();jobs.add(result);
                lane.execute(()->WorldgenGate.resume(plan,value->{
                    if(!Thread.currentThread().getName().equals("native-worldgen") || active.incrementAndGet()!=1)
                        throw new AssertionError("Concurrent/out-of-lane native generation");
                    completed.incrementAndGet();active.decrementAndGet();return CompletableFuture.completedFuture(value);
                },lane).whenComplete((value,error)->{if(error!=null)result.completeExceptionally(error);else result.complete(value);}));
                planners.execute(()->plan.complete(id));
            }
            CompletableFuture.allOf(jobs.toArray(CompletableFuture[]::new)).get(15,TimeUnit.SECONDS);
            check(completed.get()==1000 && active.get()==0,"all concurrent planning jobs serialize native mutations");
            for(int i=0;i<jobs.size();i++)check(jobs.get(i).getNow(-1)==i,"dependency results retain ownership");
        } finally {planners.shutdownNow();lane.shutdownNow();}
        System.out.println("PASS: "+checks+" worldgen executor/dependency assertions");
    }
}
