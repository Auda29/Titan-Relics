package de.relics;

import de.relics.distribution.*;
import com.google.gson.*;
import java.nio.file.*;
import java.util.*;
import static de.relics.distribution.DistributionPlanner.*;

/** Settings persistence, historical compatibility and actual custom-grid planning. */
public final class DistributionSettingsTests {
    private static int assertions;
    private static void check(boolean value,String message){assertions++;if(!value)throw new AssertionError(message);}
    private static Site site(Candidate c,Family f){return new Site(c,f.id,2*c.x(),2*c.z(),70,c.x(),0,c.z(),c.x()-40,c.z()-40,c.x()+40,c.z()+40);}
    private static DistributionPlanner planner(DistributionSettings settings,long seed) {
        return new DistributionPlanner(DistributionSettings.POLICY,settings,seed,EnumSet.allOf(Family.class),
                DistributionSettingsTests::site,()->null,()->true,0,0,128);
    }
    private static void rejected(Runnable operation,String message){boolean failed=false;try{operation.run();}catch(RuntimeException expected){failed=true;}check(failed,message);}
    public static void main(String[] args)throws Exception {
        Path root=Path.of(args[0]),file=root.resolve("config/settings.json");
        check(DistributionConfig.read(file).equals(DistributionSettings.EXPEDITION) && !Files.exists(file),"missing config has historical defaults without writing");
        DistributionConfig.write(file,DistributionSettings.DISCOVERY);
        var custom=BiomeRules.STANDARD.with(Family.OBELISK,new BiomeRules.Rule(BiomeRules.Mode.CUSTOM,Set.of("example:new_dunes")));
        check(custom.profile(Family.OBELISK,"example:new_dunes",Set.of(),List.of()).equals("obelisk"),"explicit unknown mod biome accepted");
        check(custom.profile(Family.OBELISK,"minecraft:desert",Set.of(),List.of("obelisk"))==null,"custom list replaces baseline");
        var landscapes=BiomeRules.STANDARD.with(Family.OBELISK,new BiomeRules.Rule(BiomeRules.Mode.LANDSCAPES,Set.of()));
        check(landscapes.profile(Family.OBELISK,"example:new_dunes",Set.of("c:is_desert"),List.of()).equals("obelisk"),"mod tag expands matching landscapes");
        check(landscapes.profile(Family.OBELISK,"example:unknown",Set.of(),List.of())==null,"unclassified biomes never guessed from names");
        check(BiomeRules.STANDARD.profile(Family.OBELISK,"example:new_dunes",Set.of("c:is_desert"),List.of())==null,"standard does not silently expand");
        var skulls=BiomeRules.STANDARD.with(Family.SKULL,new BiomeRules.Rule(BiomeRules.Mode.LANDSCAPES,Set.of()));
        check(skulls.profile(Family.SKULL,"example:overlap",Set.of("c:is_desert","c:is_dry"),List.of()).equals("titan_skull_sand"),"landscape overlap chooses one deterministic palette");
        rejected(()->new BiomeRules(Map.of("typo",new BiomeRules.Rule(BiomeRules.Mode.STANDARD,Set.of()))),"unknown family rejected");
        rejected(()->new BiomeRules.Rule(BiomeRules.Mode.CUSTOM,Set.of("broken biome")),"invalid biome identifier rejected");
        var biomeSettings=new DistributionSettings(2000,800,6000,2400,DistributionSettings.OUTSIDE,DistributionSettings.INSIDE,custom);
        DistributionConfig.write(root.resolve("biomes.json"),biomeSettings);
        check(DistributionConfig.read(root.resolve("biomes.json")).equals(biomeSettings),"biome choices persist in config");
        DistributionConfig.directory(root.resolve("defaults"));DistributionConfig.save(DistributionSettings.BALANCED);
        Path freshWorld=root.resolve("new-world");DistributionConfig.write(freshWorld.resolve(DistributionConfig.WORLD_FILE),biomeSettings);
        check(DistributionConfig.forNewWorld(freshWorld).equals(biomeSettings),"world creation file wins over installation defaults");
        check(DistributionConfig.load().equals(DistributionSettings.BALANCED),"world draft never changes defaults");
        String valid=Files.readString(file);
        check(DistributionConfig.read(file).equals(DistributionSettings.DISCOVERY),"all fields roundtrip");
        DistributionConfig.write(file,DistributionSettings.BALANCED);
        check(Files.readString(file.resolveSibling("settings.json.bak")).equals(valid),"explicit save preserves old file");
        for(String bad:List.of(valid.replace("2000","2000.5"),valid.replace("\"format\": 1","\"format\": 1.5"),
                valid.replace("\"format\": 1","\"format\": 2"),valid.replace("\"format\": 1","\"extra\": 0, \"format\": 1"),
                valid.replace("\"cellSize\"","\"unknown\""),valid.replace("6000","4000"),"{}","broken")) {
            Files.writeString(file,bad);rejected(()->DistributionConfig.read(file),"malformed/unsafe config rejected");
            check(Files.readString(file).equals(bad),"invalid file preserved");
        }
        for(boolean region:new boolean[]{false,true})for(int ticket=0;ticket<10000;ticket++)
            check(DistributionSettings.EXPEDITION.ticket(ticket,region)==DistributionPlanner.ticket(ticket,region),"historical ticket layout unchanged");
        var towerOnly=new DistributionSettings(2000,800,6000,2400,List.of(0,0,0,10000,0,0),List.of(0,0,0,10000,0,0));
        var none=new DistributionSettings(2000,800,6000,2400,Collections.nCopies(6,0),Collections.nCopies(6,0));
        for(int ticket=0;ticket<10000;ticket++)check(towerOnly.mayMatch(ticket,Set.of(Family.TOWER))
                && !towerOnly.mayMatch(ticket,Set.of(Family.SKULL)),"locate uses customized shares including formerly empty tickets");
        rejected(()->new DistributionSettings(2000,800,6000,2400,List.of(0,0,0,10001,0,0),List.of(0,0,0,10000,0,0)),"overfull shares rejected");
        rejected(()->new DistributionSettings(2000,800,6000,2400,List.of(1,0,0,0,0,0),Collections.nCopies(6,0)),"anchor chance independent of region");
        rejected(()->new DistributionPlanner(POLICY,towerOnly,1,Set.of(),(c,f)->null,()->null,()->true,0,0,0),"old policy cannot adopt new settings");
        for(var settings:List.of(DistributionSettings.EXPEDITION,DistributionSettings.BALANCED,DistributionSettings.DISCOVERY,towerOnly,none)) {
            var forward=planner(settings,731204);var backward=planner(settings,731204);
            var cells=new ArrayList<Cell>();var results=new HashMap<Cell,Site>();
            for(int x=-8;x<=8;x++)for(int z=-8;z<=8;z++) {
                Cell cell=new Cell(x,z);cells.add(cell);Candidate c=forward.ordinaryCandidate(cell);
                check(Math.floorDiv(c.x(),settings.cellSize())==x && Math.floorDiv(c.z(),settings.cellSize())==z,"custom grid handles negative coordinates");
                for(Candidate p:forward.candidateLocations(cell))check(Math.floorDiv(p.chunkX()*16,settings.cellSize())==x
                        && Math.floorDiv(p.chunkZ()*16,settings.cellSize())==z,"every local probe maps to its generation gate cell");
                results.put(cell,forward.plan(cell));
            }
            Collections.reverse(cells);List<Site> sites=new ArrayList<>();
            for(Cell cell:cells){Site s=backward.plan(cell);check(Objects.equals(s,results.get(cell)),"custom settings independent of exploration order");if(s!=null)sites.add(s);}
            for(int i=0;i<sites.size();i++)for(int j=i+1;j<sites.size();j++) {
                check(!within(sites.get(i),sites.get(j),settings.minDistance(),false),"custom minimum distance");
                if(sites.get(i).asset().equals("obelisk") && sites.get(j).asset().equals("obelisk"))check(!within(sites.get(i),sites.get(j),settings.obeliskDistance(),false),"custom Obelisk separation");
            }
            if(settings==towerOnly)check(sites.size()>100 && sites.stream().allMatch(s->s.asset().equals("ruined_tower")),"100 percent tower yields real tower plans");
            if(settings==none)check(sites.isEmpty(),"zero shares disable all repeatable relics");
            if(settings==DistributionSettings.EXPEDITION) {
                var legacy=new DistributionPlanner(POLICY,731204,EnumSet.allOf(Family.class),DistributionSettingsTests::site,()->null,()->true,0,0,128);
                for(Cell cell:cells)check(Objects.equals(results.get(cell),legacy.plan(cell)),"default v3 plans exactly match released v2");
            }
        }
        // New global defaults must not alter the checksummed per-world snapshot.
        Path world=root.resolve("world.json");var initial=new DistributionJournal.State();initial.settings=towerOnly;initial.policy=DistributionSettings.POLICY;
        initial.fingerprint="a".repeat(64);initial.enabled=EnumSet.allOf(Family.class);initial.minX=initial.minZ=-100000;initial.maxX=initial.maxZ=100000;initial.frozen=true;
        new DistributionJournal(world,initial).flush();DistributionConfig.write(file,DistributionSettings.EXPEDITION);
        check(new DistributionJournal(world,null).state.settings.equals(towerOnly),"world keeps independent settings after defaults change");
        initial.settings=biomeSettings;new DistributionJournal(root.resolve("biome-world.json"),initial).flush();
        check(new DistributionJournal(root.resolve("biome-world.json"),null).state.settings.biomes().equals(custom),"saved biome rules survive restart");
        var envelope=JsonParser.parseString(Files.readString(world)).getAsJsonObject();
        var payload=JsonParser.parseString(envelope.get("payload").getAsString()).getAsJsonObject();payload.remove("settings");
        envelope.addProperty("payload",payload.toString());envelope.addProperty("sha256",DistributionJournal.hash(payload.toString()));Files.writeString(world,envelope.toString());
        String damaged=Files.readString(world);rejected(()->new DistributionJournal(world,null),"v3 snapshot without settings fails closed");check(Files.readString(world).equals(damaged),"damaged world not reset");
        System.out.println("PASS: "+assertions+" distribution settings assertions");
    }
}
