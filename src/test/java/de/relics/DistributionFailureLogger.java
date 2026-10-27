package de.relics;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.minecraft.ReportType;
import net.minecraft.ReportedException;
import java.nio.file.*;

/** Test-only exception logger. Does not call the planner or alter chunk execution. */
public final class DistributionFailureLogger implements ModInitializer {
    @Override public void onInitialize() {
        ServerLifecycleEvents.SERVER_STARTED.register(server->{
            for(Thread worker:Thread.getAllStackTraces().keySet()) {
                if(!worker.getName().startsWith("Worker-Main-"))continue;
                var original=worker.getUncaughtExceptionHandler();
                worker.setUncaughtExceptionHandler((thread,error)->{
                    for(Throwable cause=error;cause!=null;cause=cause.getCause()) {
                        if(cause instanceof ReportedException reported) {
                            try {Files.writeString(Path.of("generation-failure-details.txt"),reported.getReport().getFriendlyReport(ReportType.CRASH));}
                            catch(Exception loggingFailure){loggingFailure.printStackTrace();}
                            break;
                        }
                    }
                    if(original!=null)original.uncaughtException(thread,error);
                });
            }
        });
    }
}
