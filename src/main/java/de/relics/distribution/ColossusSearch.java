package de.relics.distribution;

import java.util.*;
import static de.relics.distribution.DistributionPlanner.*;

/** Versioned, deterministic destination search. Historical cursors retain their exact order. */
public final class ColossusSearch {
    private ColossusSearch() { }
    public static final int SEARCH_CELL=1000, BAND=1000;
    private static final long DOMAIN=0x5e31a2f9b74c806dL;
    public enum Rejection { BIOME_CENTER, BIOME_FOOTPRINT, BOUNDS, TERRAIN, DISTANCE }
    /** Persisted alongside the cursor, so a restart never loses refinement candidates or diagnoses. */
    public static final class Progress {
        public int pass, bandsCompleted;
        public long coarseChecked, refinementChecked;
        public Set<Cell> refinementCells=new LinkedHashSet<>();
        public Map<Rejection,Long> rejected=new EnumMap<>(Rejection.class);
        public void checked(Candidate candidate,Rejection reason) {
            if(pass==0)coarseChecked++;else refinementChecked++;
            if(reason!=null)rejected.merge(reason,1L,Long::sum);
            // A compatible center and valid vertical envelope warrant a denser footprint search.
            if(pass==0 && (reason==Rejection.BIOME_FOOTPRINT || reason==Rejection.TERRAIN))refinementCells.add(candidate.cell());
        }
        public boolean refine() {
            if(pass!=0 || refinementCells.isEmpty())return false;
            pass=1;return true;
        }
        public void nextBand(){pass=0;bandsCompleted++;refinementCells.clear();}
        public void validate() {
            if(pass<0 || pass>1 || bandsCompleted<0 || coarseChecked<0 || refinementChecked<0 || refinementCells==null
                    || refinementCells.contains(null) || rejected==null || rejected.entrySet().stream().anyMatch(e->e.getKey()==null || e.getValue()==null || e.getValue()<0))
                throw new IllegalStateException("Invalid Colossus search progress");
        }
    }
    public static boolean mayContain(Candidate nominal,int chunkX,int chunkZ,int revision) {
        return switch(revision){case 1->nominal.chunkX()==chunkX && nominal.chunkZ()==chunkZ;
            case 2->LocationSearch.mayContain(nominal,chunkX,chunkZ);
            // Fine-grid probes cover the entire cell rather than a radius around the old anchor.
            case 3->true;default->throw new IllegalArgumentException("Unknown Colossus search revision");};
    }
    public static List<Candidate> annulus(long seed,int spawnX,int spawnZ,int lower,int upper,
                                          int minX,int minZ,int maxX,int maxZ,int revision) {
        if(revision==1)return DistributionPlanner.annulus(seed,spawnX,spawnZ,lower,upper,minX,minZ,maxX,maxZ);
        if(revision==3)return fineAnnulus(seed,spawnX,spawnZ,lower,upper,minX,minZ,maxX,maxZ,new Progress());
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
    public static List<Candidate> fineAnnulus(long seed,int spawnX,int spawnZ,int lower,int upper,
                                              int minX,int minZ,int maxX,int maxZ,Progress progress) {
        progress.validate();
        List<Candidate> result=new ArrayList<>();
        int firstX=Math.floorDiv(Math.max(minX,spawnX-upper),SEARCH_CELL),lastX=Math.floorDiv(Math.min(maxX,spawnX+upper),SEARCH_CELL);
        int firstZ=Math.floorDiv(Math.max(minZ,spawnZ-upper),SEARCH_CELL),lastZ=Math.floorDiv(Math.min(maxZ,spawnZ+upper),SEARCH_CELL);
        for(int x=firstX;x<=lastX;x++)for(int z=firstZ;z<=lastZ;z++) {
            Cell cell=new Cell(x,z);
            if(progress.pass==1 && !progress.refinementCells.contains(cell))continue;
            long left=(long)x*SEARCH_CELL-spawnX,right=left+SEARCH_CELL;
            long near=(long)z*SEARCH_CELL-spawnZ,far=near+SEARCH_CELL;
            double dx=left<=0 && right>=0?0:Math.min(Math.abs(left),Math.abs(right));
            double dz=near<=0 && far>=0?0:Math.min(Math.abs(near),Math.abs(far));
            if(Math.hypot(dx,dz)>=upper || Math.hypot(Math.max(Math.abs(left),Math.abs(right)),Math.max(Math.abs(near),Math.abs(far)))<lower)continue;
            // One chunk-aligned, seed-jittered point in each 125-block tile.
            // The first pass covers 16 spread-out tiles; refinement fills the other 48.
            for(int px=0;px<8;px++)for(int pz=0;pz<8;pz++) {
                boolean coarse=px%2==0 && pz%2==0;
                if(coarse!=(progress.pass==0))continue;
                int ordinal=px*8+pz;
                long rank=stream(seed,cell,DOMAIN^mix(ordinal));
                int bx=tilePoint(x,px,rank),bz=tilePoint(z,pz,mix(rank^DOMAIN));
                double distance=Math.hypot((double)bx-spawnX,(double)bz-spawnZ);
                if(distance<lower || distance>=upper || bx<minX || bx>maxX || bz<minZ || bz>maxZ)continue;
                result.add(new Candidate(cell,bx,bz,(int)Long.remainderUnsigned(rank,10000),mix(rank),
                        (int)(mix(rank^1)&3),true));
            }
        }
        result.sort(Comparator.comparingDouble((Candidate c)->distance(c,spawnX,spawnZ))
                .thenComparing(DistributionPlanner::priority).thenComparingInt(Candidate::x).thenComparingInt(Candidate::z));
        return List.copyOf(result);
    }
    private static int tilePoint(int cell,int tile,long rank) {
        long lower=(long)cell*SEARCH_CELL+(long)tile*125,upper=lower+125;
        long first=-Math.floorDiv(-(lower-8),16),last=Math.floorDiv(upper-1-8,16);
        return Math.toIntExact((first+Long.remainderUnsigned(rank,last-first+1))*16+8);
    }
}
