package de.relics;

import de.relics.distribution.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import static de.relics.distribution.DistributionPlanner.*;

public final class LocationSearchTests {
    private static int checks;
    private static void check(boolean value,String message){checks++;if(!value)throw new AssertionError(message);}
    private static Site site(Candidate c,Family family){return new Site(c,family.id,2*c.x(),2*c.z(),70,c.x()-40,0,c.z()-40,c.x()-40,c.z()-40,c.x()+40,c.z()+40);}
    public static void main(String[] args) {
        for(long seed:new long[]{0,-1,731204,-48291736,20260913,Long.MIN_VALUE})for(int x=-8;x<=8;x++)for(int z=-8;z<=8;z++) {
            Cell cell=new Cell(x,z);Candidate anchor=candidate(seed,cell,false);var probes=LocationSearch.positions(seed,anchor);
            check(probes.size()==64 && probes.getFirst().equals(anchor),"bounded probes retain original first position");
            Set<String> distinct=new HashSet<>();
            for(Candidate probe:probes) {
                check(probe.cell().equals(cell) && probe.ticket()==anchor.ticket() && probe.priority()==anchor.priority() && probe.rotation()==anchor.rotation(),"one cell/ticket/priority/rotation");
                check(Math.hypot((double)probe.x()-anchor.x(),(double)probe.z()-anchor.z())<=LocationSearch.RADIUS,"local search radius");
                check(Math.floorDiv(probe.x(),CELL)==x && Math.floorDiv(probe.z(),CELL)==z,"owning cell retained");
                check(Math.floorMod(probe.x(),CELL)>=MARGIN && Math.floorMod(probe.x(),CELL)<=CELL-MARGIN
                        && Math.floorMod(probe.z(),CELL)>=MARGIN && Math.floorMod(probe.z(),CELL)<=CELL-MARGIN,"cell margin retained");
                check(Math.floorMod(probe.x(),16)==8 && Math.floorMod(probe.z(),16)==8,"chunk-center alignment");
                check(LocationSearch.mayContain(anchor,probe.chunkX(),probe.chunkZ()),"every chosen position is covered by natural-start gate");
                distinct.add(probe.x()+","+probe.z());
            }
            check(distinct.size()==64 && probes.equals(LocationSearch.positions(seed,anchor)),"deterministic distinct probes");
            check(LocationSearch.positions(seed,candidate(seed,cell,true)).size()==1,"unique stream is unchanged");
        }
        long seed=731204;Cell chosen=null;
        for(int x=-20;x<20 && chosen==null;x++)for(int z=-20;z<20;z++)if(candidate(seed,new Cell(x,z),false).ticket()<3000){chosen=new Cell(x,z);break;}
        Cell cell=chosen;Candidate anchor=candidate(seed,cell,false);Candidate fit=LocationSearch.positions(seed,anchor).get(3);AtomicInteger calls=new AtomicInteger();
        Validator validate=(c,f)->{calls.incrementAndGet();return f==Family.OBELISK && c.cell().equals(cell) && c.x()==fit.x() && c.z()==fit.z()?site(c,f):null;};
        var old=new DistributionPlanner(LEGACY_POLICY,seed,EnumSet.allOf(Family.class),validate,()->null,()->true,0,0,128);
        check(old.plan(cell)==null,"saved v1 worlds retain original single position");
        var current=new DistributionPlanner(POLICY,seed,EnumSet.allOf(Family.class),validate,()->null,()->true,0,0,128);
        Site found=current.plan(cell);check(found!=null && found.candidate().equals(fit),"new policy finds fixed-family nearby valid location");
        int before=calls.get();check(current.plan(cell).equals(found) && calls.get()==before,"cached planning is stable");
        // A completely unsuitable cell remains empty; a family cannot borrow another ticket.
        var none=new DistributionPlanner(POLICY,seed,EnumSet.allOf(Family.class),(c,f)->null,()->null,()->true,0,0,128);
        check(none.plan(cell)==null,"all rejected positions leave an empty opportunity");
        // Moving beyond an accepted region edge must not obtain a new family.
        boolean edgeCovered=false;
        for(long s=0;s<100 && !edgeCovered;s++) {
            Candidate ob=candidate(s,new Cell(0,0),false);if(ob.ticket()>=3000)continue;
            for(int x=-2;x<=2 && !edgeCovered;x++)for(int z=-2;z<=2 && !edgeCovered;z++) {
                Candidate c=candidate(s,new Cell(x,z),false);
                if(c.ticket()<3250 || c.ticket()>=4500 || distance(c,ob.x(),ob.z())>REGION)continue;
                Candidate moved=LocationSearch.positions(s,c).stream().filter(p->distance(p,ob.x(),ob.z())>REGION).findFirst().orElse(null);
                if(moved==null)continue;
                Set<Family> evaluated=new HashSet<>();
                Validator boundary=(p,f)->{
                    if(f==Family.OBELISK)return p.equals(ob)?site(p,f):null;
                    if(!p.cell().equals(c.cell()))return null;
                    evaluated.add(f);return p.equals(moved)?site(p,f):null;
                };
                var edge=new DistributionPlanner(POLICY,s,EnumSet.allOf(Family.class),boundary,()->null,()->true,0,0,128);
                check(edge.candidateChoice(c.cell()).asset().equals(Family.SKULL.id),"nominal region fixes skull family");
                check(edge.plan(c.cell())==null && evaluated.equals(Set.of(Family.SKULL)),"crossing region edge rejects without a replacement ticket");
                edgeCovered=true;
            }
        }
        check(edgeCovered,"region-edge regression exercised");
        // A generation job near the initial spawn must be resolvable before the
        // unique destination is committed. This covers all nested neighborhoods.
        for(int n=0;n<30;n++) {
            long s=mix(n+731204);Candidate here=candidate(s,new Cell(0,0),false);
            var boot=new DistributionPlanner(POLICY,s,EnumSet.allOf(Family.class),LocationSearchTests::site,()->null,()->false,here.x(),here.z(),128);
            try{boot.plan(here.cell());check(true,"bootstrap local dependency halo is safe");}
            catch(Pending blocked){throw new AssertionError("Initial spawn would wait on its own unique initialization",blocked);}
        }
        // Deliberately choose sites at the far side of their search disks.
        // Cross-cell spacing and initial-spawn dependency halos must remain safe.
        for(int n=0;n<12;n++) {
            long s=mix(n+90127);Candidate here=candidate(s,new Cell(0,0),false);
            Map<Cell,Candidate> fits=new HashMap<>();
            Validator shifted=(c,f)->{
                Candidate selected=fits.computeIfAbsent(c.cell(),key->LocationSearch.positions(s,candidate(s,key,false)).stream()
                        .max(Comparator.comparingDouble(p->distance(p,here.x(),here.z()))).orElseThrow());
                return c.x()==selected.x() && c.z()==selected.z()?site(c,f):null;
            };
            var boot=new DistributionPlanner(POLICY,s,EnumSet.allOf(Family.class),shifted,()->null,()->false,here.x(),here.z(),128);
            try{
                Site choice=boot.candidateChoice(here.cell());
                check(true,"preselection never blocks nominal bootstrap chunk");
                if(choice!=null) {
                    var selectedBoot=new DistributionPlanner(POLICY,s,EnumSet.allOf(Family.class),shifted,()->null,()->false,choice.candidate().x(),choice.candidate().z(),128);
                    selectedBoot.plan(here.cell());
                    check(true,"full decision at selected bootstrap chunk has bounded dependencies");
                }
            }
            catch(Pending blocked){throw new AssertionError("Shifted search deadlocks initial spawn",blocked);}
            var forward=new DistributionPlanner(POLICY,s,EnumSet.allOf(Family.class),shifted,()->null,()->true,0,0,128);
            var reverse=new DistributionPlanner(POLICY,s,EnumSet.allOf(Family.class),shifted,()->null,()->true,0,0,128);
            List<Cell> cells=new ArrayList<>();for(int x=-5;x<=5;x++)for(int z=-5;z<=5;z++)cells.add(new Cell(x,z));
            Map<Cell,Site> expected=new HashMap<>();List<Site> sites=new ArrayList<>();
            for(Cell key:cells){Site result=forward.plan(key);expected.put(key,result);if(result!=null)sites.add(result);}
            Collections.reverse(cells);for(Cell key:cells)check(Objects.equals(reverse.plan(key),expected.get(key)),"moved sites are independent of exploration order");
            for(int i=0;i<sites.size();i++)for(int j=i+1;j<sites.size();j++) {
                Site a=sites.get(i),b=sites.get(j);check(!within(a,b,SEPARATION,false),"moved sites respect general separation");
                if(a.asset().equals("obelisk") && b.asset().equals("obelisk"))check(!within(a,b,OBELISK_SEPARATION,false),"moved Obelisks respect region separation");
            }
        }
        System.out.println("PASS: "+checks+" versioned location-search assertions");
    }
}
