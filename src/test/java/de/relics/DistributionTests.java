package de.relics;

import de.relics.distribution.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import static de.relics.distribution.DistributionPlanner.*;

/** Production pure planner/journal tests. Synthetic terrain is explicitly not Minecraft acceptance. */
public final class DistributionTests {
    private static long assertions;
    private static void check(boolean test,String message){assertions++;if(!test)throw new AssertionError(message);}
    private static Site site(Candidate c,Family family){return new Site(c,family.id,2*c.x(),2*c.z(),70,c.x()-50,0,c.z()-50,c.x()-50,c.z()-50,c.x()+50,c.z()+50);}
    private static DistributionPlanner planner(long seed,Validator validate,Site unique) {
        return new DistributionPlanner(seed,EnumSet.allOf(Family.class),validate,()->unique,()->unique==null,0,0,128);
    }
    public static void main(String[] args)throws Exception {
        for(boolean inside:new boolean[]{false,true}) {
            Map<Family,Integer> counts=new EnumMap<>(Family.class);
            for(int i=0;i<10000;i++)counts.merge(ticket(i,inside),1,Integer::sum);
            int[] expected=inside?new int[]{0,3000,1500,1500,200,200,200,3400}:new int[]{0,3000,250,250,200,200,200,5900};
            for(Family f:Family.values())check(counts.getOrDefault(f,0)==expected[f.ordinal()],"exact ticket share "+inside+f);
        }
        for(long seed:new long[]{0,1,-1,731204,Long.MIN_VALUE,Long.MAX_VALUE})
            for(int x=-20;x<=20;x++)for(int z=-20;z<=20;z++) {
                Cell cell=new Cell(x,z);Candidate c=candidate(seed,cell,false);
                check(Math.floorDiv(c.x(),CELL)==x && Math.floorDiv(c.z(),CELL)==z,"negative floor division");
                check(Math.floorMod(c.x(),16)==8 && Math.floorMod(c.z(),16)==8,"chunk center");
                check(Math.floorMod(c.x(),CELL)>=MARGIN && Math.floorMod(c.x(),CELL)<=CELL-MARGIN,"margin");
                check(c.equals(candidate(seed,cell,false)),"repeatable serialization");
                check(!c.equals(candidate(seed,cell,true)),"independent unique stream");
            }
        // Whole-token frozen vectors expose accidental RNG/serialization changes.
        check(mix(0)==0 && mix(1)==6238072747940578789L,"SplitMix64 vectors");
        Candidate a=new Candidate(new Cell(-1,0),0,0,0,3,0,false),b=new Candidate(new Cell(0,-1),2000,0,0,3,0,false);
        check(priority(a,b)<0,"signed tie break");
        check(!within(site(a,Family.TOWER),site(b,Family.TOWER),2000,false),"exact distance allowed");
        check(within(site(a,Family.TOWER),site(b,Family.TOWER),2000,true),"inclusive boundary");
        var half=new Site(b,"obelisk",3999,0,70,0,0,0,0,0,0,0);
        check(within(site(a,Family.TOWER),half,2000,false),"half-block comparison");
        List<Candidate> ring=annulus(731204,-131,257,30000,60000,-100000,-100000,100000,100000);
        Set<Cell> actual=new HashSet<>();for(Candidate c:ring){actual.add(c.cell());check(distance(c,-131,257)>=30000 && distance(c,-131,257)<60000,"annulus membership");}
        Set<Cell> brute=new HashSet<>();for(int x=-20;x<=20;x++)for(int z=-20;z<=20;z++) {
            Candidate c=candidate(731204,new Cell(x,z),true);double d=distance(c,-131,257);if(d>=30000 && d<60000)brute.add(c.cell());
        }
        check(actual.equals(brute),"annulus iterator agrees with exhaustive enumeration");
        for(int i=1;i<ring.size();i++)check(priority(ring.get(i-1),ring.get(i))<=0,"annulus stable rank");
        AtomicInteger checks=new AtomicInteger();
        var reject=planner(731204,(c,f)->{checks.incrementAndGet();return null;},null);
        for(int x=-5;x<=5;x++)for(int z=-5;z<=5;z++)check(reject.plan(new Cell(x,z))==null,"invalid terrain never rerolled");
        // Pending results cannot poison either accepted-anchor or terrain caches.
        var pending=new DistributionPlanner(731204,EnumSet.allOf(Family.class),(c,f)->site(c,f),()->null,()->false,0,0,128);
        boolean blocked=false;for(int x=30;x<40 && !blocked;x++)try{pending.plan(new Cell(x,30));}catch(Pending expected){blocked=true;}
        check(blocked,"unresolved large site holds far decisions");
        // Thirty predetermined seeds; order, all pair distances and region classification
        // are checked on the production planner with deterministic synthetic terrain.
        for(int sample=0;sample<30;sample++) {
            long seed=mix(731204L+sample);Validator terrain=(c,f)->(stream(seed,c.cell(),0x123456789abcdefL)&7)==0?null:site(c,f);
            var forward=planner(seed,terrain,null);var backward=planner(seed,terrain,null);
            List<Cell> cells=new ArrayList<>();for(int x=-12;x<12;x++)for(int z=-12;z<12;z++)cells.add(new Cell(x,z));
            Map<Cell,Site> expected=new HashMap<>();for(Cell cell:cells)expected.put(cell,forward.plan(cell));
            Collections.reverse(cells);List<Site> found=new ArrayList<>();
            for(Cell cell:cells){Site s=backward.plan(cell);check(Objects.equals(s,expected.get(cell)),"exploration order seed "+sample);if(s!=null)found.add(s);}
            for(int i=0;i<found.size();i++)for(int j=i+1;j<found.size();j++) {
                Site first=found.get(i),second=found.get(j);check(!within(first,second,2000,false),"general separation");
                if(first.asset().equals("obelisk") && second.asset().equals("obelisk"))check(!within(first,second,15000,false),"Obelisk separation");
            }
        }
        Path file=Path.of(args[0]).resolve("distribution.json");
        DistributionJournal.State initial=new DistributionJournal.State();initial.seed=731204;initial.fingerprint="a".repeat(64);
        initial.enabled=EnumSet.allOf(Family.class);initial.minX=initial.minZ=-100000;initial.maxX=initial.maxZ=100000;
        var journal=new DistributionJournal(file,initial);journal.state.frozen=true;journal.state.cursor=7;journal.flush();
        var restored=new DistributionJournal(file,null);check(restored.state.cursor==7 && restored.state.seed==731204,"atomic cursor reload");
        Files.writeString(file,Files.readString(file).replace("731204","731205"));
        boolean corrupt=false;try{new DistributionJournal(file,null);}catch(IllegalStateException expected){corrupt=true;}
        check(corrupt,"checksum failure does not reset planning");
        System.out.println("PASS: "+assertions+" distribution assertions, 30 synthetic-terrain seeds; no claim of Minecraft terrain acceptance");
    }
}
