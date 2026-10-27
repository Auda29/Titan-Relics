package de.relics.distribution;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;
import java.util.function.Function;

/** Preserve Minecraft's serial worldgen lane across an asynchronous planning dependency. */
public final class WorldgenGate {
    private WorldgenGate() { }

    public static <P,R> CompletableFuture<R> resume(CompletableFuture<P> plan,
            Function<P,CompletableFuture<R>> generate,Executor worldgenExecutor) {
        // The caller already runs on the native worldgen dispatcher. Most
        // chunks have no relic candidate: keep their native synchronous path.
        // Pending work MUST re-enter that same dispatcher, never the generic
        // ForkJoin pool, before mutating chunks or completing their status step.
        return plan.isDone() ? plan.thenCompose(generate) : plan.thenComposeAsync(generate,worldgenExecutor);
    }
}
