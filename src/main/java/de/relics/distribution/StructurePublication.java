package de.relics.distribution;

import java.util.concurrent.*;
import java.util.function.*;

/** Hold exactly one native cache publication until filtering completes on its native lane. */
public final class StructurePublication {
    private Runnable publish;
    private boolean released;
    public void capture(Runnable operation) {
        if(publish!=null || released)throw new IllegalStateException("Duplicate structure publication");
        publish=operation;
    }
    public <T> CompletableFuture<T> finish(CompletableFuture<T> generated,Function<T,CompletableFuture<Runnable>> filter,Executor nativeLane) {
        return WorldgenGate.resume(generated,chunk->{
            if(publish==null)throw new IllegalStateException("Unsupported structure-start pipeline: native publication was not captured");
            return WorldgenGate.resume(filter.apply(chunk),apply->{
                if(released)throw new IllegalStateException("Structure publication already released");
                apply.run();released=true;publish.run();return CompletableFuture.completedFuture(chunk);
            },nativeLane);
        },nativeLane);
    }
}
