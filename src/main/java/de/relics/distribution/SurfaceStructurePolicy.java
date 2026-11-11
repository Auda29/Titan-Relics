package de.relics.distribution;

import java.util.*;
import static de.relics.distribution.DistributionPlanner.*;

/** Separate, frozen foreign-structure rule. Never changes relic tickets or terrain decisions. */
public final class SurfaceStructurePolicy {
    public static final int REVISION=1, BOOTSTRAP_RADIUS=1024, MAX_CELLS=64;
    private static final long DOMAIN=0x4bcd350f92e76a81L;
    private SurfaceStructurePolicy() { }
    public record State(int revision,int bootstrapRadius,List<String> targets,List<String> exempt) {
        public State {
            if(revision!=REVISION || bootstrapRadius!=BOOTSTRAP_RADIUS)throw new IllegalArgumentException("Unknown surface-structure policy");
            targets=checked(targets);exempt=checked(exempt);
            if(targets.stream().anyMatch(id->id.startsWith("relics:")))throw new IllegalArgumentException("Relics cannot be filtered");
        }
        public void validate(){new State(revision,bootstrapRadius,targets,exempt);}
        public boolean eligible(String id){return !id.startsWith("relics:") && targets.contains(id) && !exempt.contains(id);}
    }
    private static List<String> checked(List<String> ids) {
        if(ids==null || ids.size()>4096 || ids.stream().anyMatch(id->id==null || !id.matches("[a-z0-9_.-]+:[a-z0-9_./-]+")))
            throw new IllegalArgumentException("Invalid surface-structure IDs");
        var sorted=ids.stream().distinct().sorted().toList();
        if(sorted.size()!=ids.size())throw new IllegalArgumentException("Duplicate surface-structure IDs");
        return sorted;
    }
    public record Box(int minX,int minY,int minZ,int maxX,int maxY,int maxZ) {
        public Box {if(minX>maxX || minY>maxY || minZ>maxZ)throw new IllegalArgumentException("Inverted bounds");}
        public boolean intersects(Box b){return minX<=b.maxX && maxX>=b.minX && minY<=b.maxY && maxY>=b.minY && minZ<=b.maxZ && maxZ>=b.minZ;}
    }
    /** Exactly one independent bit per foreign start, even when several relics touch it. */
    public static boolean selected(long seed,String dimension,String id,int chunkX,int chunkZ) {
        long key=DOMAIN^mix(seed)^mix(((long)chunkX<<32)^Integer.toUnsignedLong(chunkZ));
        for(byte b:(dimension+"\0"+id).getBytes(java.nio.charset.StandardCharsets.UTF_8))key=mix(key^(b&255));
        return (mix(key)&1)==0;
    }
    public static boolean bootstrap(State policy,int bootstrapX,int bootstrapZ,int chunkX,int chunkZ,List<Box> pieces) {
        long radius=policy.bootstrapRadius();
        long x=(long)chunkX*16,z=(long)chunkZ*16;
        if(x<=bootstrapX+radius && x+15>=bootstrapX-radius && z<=bootstrapZ+radius && z+15>=bootstrapZ-radius)return true;
        // Preserve buildings reaching into the initial spawn area, including starts outside it.
        return pieces.stream().anyMatch(b->b.minX<=bootstrapX+radius && b.maxX>=bootstrapX-radius && b.minZ<=bootstrapZ+radius && b.maxZ>=bootstrapZ-radius);
    }
    /** All potentially intersecting centers, bounded before allocating or requesting plans. */
    public static Optional<List<Cell>> cells(List<Box> pieces,int cellSize,int padding) {
        Set<Cell> result=new LinkedHashSet<>();
        for(Box b:pieces) {
            long minX=Math.floorDiv((long)b.minX-padding,cellSize),maxX=Math.floorDiv((long)b.maxX+padding,cellSize);
            long minZ=Math.floorDiv((long)b.minZ-padding,cellSize),maxZ=Math.floorDiv((long)b.maxZ+padding,cellSize);
            if((maxX-minX+1)*(maxZ-minZ+1)>MAX_CELLS)return Optional.empty();
            for(long x=minX;x<=maxX;x++)for(long z=minZ;z<=maxZ;z++) {
                result.add(new Cell(Math.toIntExact(x),Math.toIntExact(z)));
                if(result.size()>MAX_CELLS)return Optional.empty();
            }
        }
        return Optional.of(List.copyOf(result));
    }
}
