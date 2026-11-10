package de.relics.distribution;

import java.util.*;
import static de.relics.distribution.DistributionPlanner.*;

/** Revision 2 tests nearby positions in each intersecting cell, nearest first. */
public final class ColossusSearch {
    private ColossusSearch() { }
    public static boolean mayContain(Candidate nominal,int chunkX,int chunkZ,int revision) {
        return revision==1?nominal.chunkX()==chunkX && nominal.chunkZ()==chunkZ:LocationSearch.mayContain(nominal,chunkX,chunkZ);
    }
    public static List<Candidate> annulus(long seed,int spawnX,int spawnZ,int lower,int upper,
                                          int minX,int minZ,int maxX,int maxZ,int revision) {
        if(revision==1)return DistributionPlanner.annulus(seed,spawnX,spawnZ,lower,upper,minX,minZ,maxX,maxZ);
        if(revision!=2)throw new IllegalArgumentException("Unknown Colossus search revision");
        List<Candidate> result=new ArrayList<>();
        int firstX=Math.floorDiv(Math.max(minX,spawnX-upper),CELL),lastX=Math.floorDiv(Math.min(maxX,spawnX+upper),CELL);
        int firstZ=Math.floorDiv(Math.max(minZ,spawnZ-upper),CELL),lastZ=Math.floorDiv(Math.min(maxZ,spawnZ+upper),CELL);
        for(int x=firstX;x<=lastX;x++)for(int z=firstZ;z<=lastZ;z++) {
            long left=(long)x*CELL+MARGIN-spawnX,right=(long)(x+1)*CELL-MARGIN-spawnX;
            long near=(long)z*CELL+MARGIN-spawnZ,far=(long)(z+1)*CELL-MARGIN-spawnZ;
            double dx=left<=0 && right>=0?0:Math.min(Math.abs(left),Math.abs(right));
            double dz=near<=0 && far>=0?0:Math.min(Math.abs(near),Math.abs(far));
            if(Math.hypot(dx,dz)>=upper || Math.hypot(Math.max(Math.abs(left),Math.abs(right)),Math.max(Math.abs(near),Math.abs(far)))<lower)continue;
            Candidate anchor=candidate(seed,new Cell(x,z),true);
            Candidate local=new Candidate(anchor.cell(),anchor.x(),anchor.z(),anchor.ticket(),anchor.priority(),anchor.rotation(),false);
            for(Candidate p:LocationSearch.positions(seed,local,CELL)) {
                double distance=distance(p,spawnX,spawnZ);
                if(distance>=lower && distance<upper && p.x()>=minX && p.x()<=maxX && p.z()>=minZ && p.z()<=maxZ)
                    result.add(new Candidate(p.cell(),p.x(),p.z(),p.ticket(),p.priority(),p.rotation(),true));
            }
        }
        result.sort(Comparator.comparingDouble((Candidate c)->distance(c,spawnX,spawnZ))
                .thenComparing(DistributionPlanner::priority).thenComparingInt(Candidate::x).thenComparingInt(Candidate::z));
        return List.copyOf(result);
    }
}
