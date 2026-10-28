package de.relics.testmixin;

import de.relics.distribution.TerrainValidator;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyArg;

/** Test-only capture before the saved-world compatibility check; never packaged for players. */
@Mixin(value=TerrainValidator.class,remap=false)
public abstract class PlanningFingerprintProbe {
    @ModifyArg(method="<init>(Lnet/minecraft/server/level/ServerLevel;IIIILjava/lang/String;)V",at=@At(value="INVOKE",
            target="Lde/relics/distribution/DistributionJournal;hash(Ljava/lang/String;)Ljava/lang/String;",remap=false),index=0,remap=false)
    private String relics$captureSignature(String signature) {
        if(Boolean.getBoolean("relics.capturePlanningFingerprint")) {
            try {
                java.nio.file.Files.writeString(java.nio.file.Path.of("planning-signature.json"),signature);
                System.out.println("PLANNING_SIGNATURE_CAPTURED "+de.relics.distribution.DistributionJournal.hash(signature));
            }catch(java.io.IOException error){throw new IllegalStateException("Cannot capture test planning signature",error);}
        }
        return signature;
    }
}
