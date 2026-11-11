package de.relics;

import de.relics.distribution.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import static de.relics.distribution.DistributionPlanner.*;
import static de.relics.distribution.ColossusSearch.Rejection.*;

/** Search coverage, refinement, saved cursors and preservation of released world contracts. */
public final class ColossusSearchTests {
    private static int assertions;
    private static void check(boolean value,String message){assertions++;if(!value)throw new AssertionError(message);}
    private static List<Candidate> ring(long seed,int x,int z,int lower,int upper,ColossusSearch.Progress progress) {
        return ColossusSearch.fineAnnulus(seed,x,z,lower,upper,-1000000,-1000000,1000000,1000000,progress);
    }
    private static DistributionSettings revision2(DistributionSettings s) {
        return new DistributionSettings(s.cellSize(),s.minDistance(),s.obeliskDistance(),s.regionRadius(),s.outside(),s.inside(),s.biomes(),s.colossusMinDistance(),2);
    }
    public static void main(String[] args)throws Exception {
        long[] seeds={701448007947040131L,2090676289L,731204L};
        // Derived independently from the published Beta 3 Fabric 1.21.1 JAR, not this implementation.
        String[] historical={"033ef86a6db490582ecb6be1c3a174b9a26aeda53cae81a05c0e54263b0da588",
                "02ad41ee0c01df3b492c56a3f4f80957134447a7155a8b93b18c44176985f964",
                "3de56de136aec4e4fe3c1fd6a94b92d781e99f4c4454851a5a20a7f44acb0dc4"};
        for(int i=0;i<seeds.length;i++) {
            long seed=seeds[i];MessageDigest digest=MessageDigest.getInstance("SHA-256");
            for(int lower=4000;lower<16000;lower+=4000)
                for(Candidate c:ColossusSearch.annulus(seed,-272,-336,lower,lower+4000,-100000,-100000,100000,100000,2))
                    digest.update((c.toString()+"\n").getBytes(StandardCharsets.UTF_8));
            check(HexFormat.of().formatHex(digest.digest()).equals(historical[i]),"revision 2 candidate order matches the published artifact exactly");
            var progress=new ColossusSearch.Progress();
            var coarse=ring(seed,-272,-336,4000,5000,progress);
            check(!coarse.isEmpty() && coarse.equals(ring(seed,-272,-336,4000,5000,progress)),"coarse order is deterministic");
            Map<Cell,Integer> coverage=new HashMap<>();Set<Long> positions=new HashSet<>();
            double previous=0;
            for(Candidate c:coarse) {
                double distance=distance(c,-272,-336);
                check(distance>=4000 && distance<5000 && distance>=previous,"coarse pass is nearest first within the band");previous=distance;
                check(c.unique() && Math.floorMod(c.x(),16)==8 && Math.floorMod(c.z(),16)==8,"probes use actual chunk centers");
                check(Math.floorDiv(c.x(),1000)==c.cell().x() && Math.floorDiv(c.z(),1000)==c.cell().z(),"negative coordinates map to the correct fine cell");
                check(positions.add(((long)c.x()<<32)^Integer.toUnsignedLong(c.z())),"coarse points never repeat");
                coverage.merge(c.cell(),1,Integer::sum);
                progress.checked(c,TERRAIN);
            }
            check(coverage.values().stream().allMatch(n->n<=16),"bounded coarse work per search cell");
            check(progress.coarseChecked==coarse.size() && progress.refine(),"terrain failures activate refinement before expanding outward");
            var refined=ring(seed,-272,-336,4000,5000,progress);
            check(!refined.isEmpty(),"promising search cells receive additional probes");
            previous=0;
            for(Candidate c:refined) {
                double distance=distance(c,-272,-336);
                check(distance>=4000 && distance<5000 && distance>=previous,"refinement remains within the near band");previous=distance;
                check(positions.add(((long)c.x()<<32)^Integer.toUnsignedLong(c.z())),"refinement never repeats a coarse point");
                check(progress.refinementCells.contains(c.cell()),"refinement only visits compatible cells");
            }
            int cursor=refined.size()/2;
            var state=new DistributionJournal.State();state.settings=DistributionSettings.DISCOVERY;state.policy=state.settings.policy();
            state.seed=seed;state.spawnX=-272;state.spawnZ=-336;state.lower=4000;state.upper=5000;state.cursor=cursor;
            state.fingerprint="a".repeat(64);state.enabled=Set.of(Family.COLOSSUS);state.frozen=true;
            state.minX=state.minZ=-1000000;state.maxX=state.maxZ=1000000;state.colossusSearch=progress;
            Path file=Path.of(args[0]).resolve("search-"+seed+".json");
            new DistributionJournal(file,state).flush();var restored=new DistributionJournal(file,null).state;
            check(restored.cursor==cursor && restored.colossusSearch.pass==1,"refinement cursor survives restart");
            check(refined.subList(cursor,refined.size()).equals(ring(seed,-272,-336,4000,5000,restored.colossusSearch).subList(cursor,refined.size())),"resumed refinement preserves its exact remaining sequence");
            check(restored.colossusSearch.rejected.get(TERRAIN)==coarse.size(),"rejection totals survive restart");
            check(!restored.colossusSearch.refine(),"a refinement pass cannot restart itself");
            restored.colossusSearch.nextBand();
            check(restored.colossusSearch.pass==0 && restored.colossusSearch.refinementCells.isEmpty() && restored.colossusSearch.bandsCompleted==1,"outward expansion clears only per-band refinement state");
            check(restored.colossusSearch.coarseChecked==coarse.size(),"outward expansion preserves cumulative diagnostics");
        }
        // Every one of a complete 1 km cell's 64 tiles is sampled once, without a 256-block edge gap.
        var full=new ColossusSearch.Progress();var coarse=ring(731204,0,0,0,2000,full);
        Cell cell=new Cell(-1,0);
        for(Candidate c:coarse)if(c.cell().equals(cell))full.checked(c,BIOME_FOOTPRINT);
        check(full.coarseChecked==16,"the coarse pass covers all 16 spread-out tiles in a complete cell");
        check(full.refine(),"a compatible center with a failed footprint is promising");
        var fine=ring(731204,0,0,0,2000,full);check(fine.size()==48,"refinement adds exactly 48 distinct tiles for one cell");
        Set<String> tiles=new HashSet<>();
        for(Candidate c:coarse)if(c.cell().equals(cell))tiles.add(Math.floorDiv(Math.floorMod(c.x(),1000),125)+","+Math.floorDiv(Math.floorMod(c.z(),1000),125));
        for(Candidate c:fine)tiles.add(Math.floorDiv(Math.floorMod(c.x(),1000),125)+","+Math.floorDiv(Math.floorMod(c.z(),1000),125));
        check(tiles.size()==64,"all fine tiles, including the cell edges, have coverage");
        var hopeless=new ColossusSearch.Progress();
        hopeless.checked(coarse.getFirst(),BIOME_CENTER);hopeless.checked(coarse.getLast(),BOUNDS);
        check(!hopeless.refine() && hopeless.refinementCells.isEmpty(),"incompatible biome centers and invalid vertical bounds do not trigger dense probing");
        check(hopeless.rejected.get(BIOME_CENTER)==1 && hopeless.rejected.get(BOUNDS)==1,"rejection reasons stay distinct");
        var edge=ColossusSearch.fineAnnulus(7,-900,900,0,2500,-1200,-100,300,1300,new ColossusSearch.Progress());
        check(!edge.isEmpty() && edge.stream().allMatch(c->c.x()>=-1200 && c.x()<=300 && c.z()>=-100 && c.z()<=1300),"asymmetric finite borders clip fine probes");
        check(ColossusSearch.fineAnnulus(7,0,0,4000,5000,-100,-100,100,100,new ColossusSearch.Progress()).isEmpty(),"a finite border inside the minimum produces no fake candidate");
        Candidate nominal=candidate(7,new Cell(0,0),true);
        check(ColossusSearch.mayContain(nominal,0,0,3),"new fine-cell probes can enter the start gate beyond the old anchor radius");
        check(!ColossusSearch.mayContain(nominal,nominal.chunkX()+300,nominal.chunkZ(),2),"Beta 3's radius gate remains unchanged");
        // Same repeatable opportunities and placements under the new policy, with a fixed destination.
        var s=DistributionSettings.DISCOVERY;var old=revision2(s);
        DistributionPlanner.Validator validator=(c,f)->new Site(c,f.id,2*c.x(),2*c.z(),70,c.x(),0,c.z(),c.x()-20,c.z()-20,c.x()+20,c.z()+20);
        var before=new DistributionPlanner(old.policy(),old,731204,EnumSet.allOf(Family.class),validator,()->null,()->true,0,0,128);
        var after=new DistributionPlanner(s.policy(),s,731204,EnumSet.allOf(Family.class),validator,()->null,()->true,0,0,128);
        for(int x=-5;x<=5;x++)for(int z=-5;z<=5;z++) {
            var c=new Cell(x,z);
            check(before.candidateLocations(c).equals(after.candidateLocations(c)),"repeatable probe coordinates are unchanged");
            check(Objects.equals(before.plan(c),after.plan(c)),"repeatable selection and spacing are unchanged for an identical Colossus destination");
        }
        check(old.policy().equals(DistributionSettings.DISCOVERIES_POLICY),"explicit Beta 3 settings retain their original policy");
        var oldState=new DistributionJournal.State();oldState.settings=old;oldState.policy=old.policy();oldState.frozen=true;
        oldState.fingerprint="b".repeat(64);oldState.enabled=Set.of(Family.COLOSSUS);
        oldState.minX=oldState.minZ=-100000;oldState.maxX=oldState.maxZ=100000;
        oldState.lower=12000;oldState.upper=16000;oldState.cursor=509;oldState.candidatesChecked=1555;
        Path oldFile=Path.of(args[0]).resolve("beta3-cursor.json");new DistributionJournal(oldFile,oldState).flush();
        String bytes=Files.readString(oldFile);var restored=new DistributionJournal(oldFile,null).state;
        check(restored.settings.generationRevision()==2 && restored.cursor==509 && restored.lower==12000 && restored.upper==16000
                && restored.candidatesChecked==1555 && restored.colossusSearch==null,"old pending cursor is not upgraded to the fine search");
        check(Files.readString(oldFile).equals(bytes),"loading a revision 2 journal preserves every byte");
        System.out.println("PASS: "+assertions+" fine Colossus search assertions");
    }
}
