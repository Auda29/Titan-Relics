package de.relics.distribution;

import java.util.*;
import static de.relics.distribution.DistributionPlanner.*;

/** One fixed family ticket; bounded nearby terrain probes, never replacement family rolls. */
public final class LocationSearch {
    public static final int RADIUS=3072, ATTEMPTS=64;
    private static final long DOMAIN=0x493fba7d6e21c805L;
    private LocationSearch() { }
    public static List<Candidate> positions(long seed,Candidate anchor) {
        if(anchor.unique())return List.of(anchor);
        List<Candidate> result=new ArrayList<>();result.add(anchor);Set<Long> seen=new HashSet<>();seen.add(0L);
        long left=(long)anchor.cell().x()*CELL+MARGIN,right=(long)(anchor.cell().x()+1)*CELL-MARGIN;
        long near=(long)anchor.cell().z()*CELL+MARGIN,far=(long)(anchor.cell().z()+1)*CELL-MARGIN;
        int reach=RADIUS/16,side=reach*2+1;
        for(int ordinal=0;ordinal<8192 && result.size()<ATTEMPTS;ordinal++) {
            long rank=stream(seed,anchor.cell(),DOMAIN^mix(ordinal));
            int x=(int)Long.remainderUnsigned(rank,side)-reach;
            int z=(int)Long.remainderUnsigned(mix(rank^DOMAIN),side)-reach;
            if((x*x+z*z)*256>RADIUS*RADIUS)continue;
            int px=anchor.x()+16*x,pz=anchor.z()+16*z;
            if(px<left || px>right || pz<near || pz>far)continue;
            long packed=((long)x<<32)^Integer.toUnsignedLong(z);if(!seen.add(packed))continue;
            result.add(new Candidate(anchor.cell(),px,pz,anchor.ticket(),anchor.priority(),anchor.rotation(),false));
        }
        // A deterministic geometric fallback completes the probe list only, not
        // a quota of accepted models. Terrain is never consulted here.
        for(int x=-reach;x<=reach && result.size()<ATTEMPTS;x++)for(int z=-reach;z<=reach && result.size()<ATTEMPTS;z++) {
            int px=anchor.x()+16*x,pz=anchor.z()+16*z;
            if((x*x+z*z)*256>RADIUS*RADIUS || px<left || px>right || pz<near || pz>far)continue;
            if(!seen.add(((long)x<<32)^Integer.toUnsignedLong(z)))continue;
            result.add(new Candidate(anchor.cell(),px,pz,anchor.ticket(),anchor.priority(),anchor.rotation(),false));
        }
        return List.copyOf(result);
    }
    public static boolean mayContain(Candidate anchor,int chunkX,int chunkZ) {
        long x=(long)chunkX*16+8-anchor.x(),z=(long)chunkZ*16+8-anchor.z();
        return x*x+z*z<=(long)RADIUS*RADIUS;
    }
}
