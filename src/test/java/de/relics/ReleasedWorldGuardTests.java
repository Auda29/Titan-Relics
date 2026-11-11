package de.relics;

import de.relics.distribution.DistributionJournal;
import com.google.gson.JsonParser;
import java.nio.file.*;
import java.util.Arrays;

/** Compile and run against a released JAR, never the candidate's classes. */
public final class ReleasedWorldGuardTests {
    public static void main(String[] args)throws Exception {
        Path file=Path.of(args[0]);byte[] before=Files.readAllBytes(file);boolean rejected=false;
        try {new DistributionJournal(file,null);}catch(IllegalStateException expected){rejected=true;}
        if(!rejected)throw new AssertionError("Released binary accepted the new world policy");
        // A supported historical control proves rejection is not caused by corrupt JSON.
        var control=JsonParser.parseString(new String(before,java.nio.charset.StandardCharsets.UTF_8)).getAsJsonObject();
        var payload=JsonParser.parseString(control.get("payload").getAsString()).getAsJsonObject();
        payload.addProperty("policy","relics-distribution-v3-settings");
        payload.remove("surfaceStructures");control.addProperty("version",1);
        control.addProperty("payload",payload.toString());control.addProperty("sha256",DistributionJournal.hash(payload.toString()));
        Path temporary=Files.createTempFile(file.getParent(),"released-guard-control-",".json");
        try {Files.writeString(temporary,control.toString());new DistributionJournal(temporary,null);}
        finally {Files.deleteIfExists(temporary);}
        if(!Arrays.equals(before,Files.readAllBytes(file)))throw new AssertionError("Rejected plan was rewritten");
        System.out.println("PASS: released binary rejects the new policy without changing the plan");
    }
}
