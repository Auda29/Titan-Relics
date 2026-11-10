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
        return new DistributionPlanner(settings.policy(),settings,seed,EnumSet.allOf(Family.class),
                DistributionSettingsTests::site,()->null,()->true,0,0,128);
    }
    private static void rejected(Runnable operation,String message){boolean failed=false;try{operation.run();}catch(RuntimeException expected){failed=true;}check(failed,message);}
    public static void main(String[] args)throws Exception {
        Path root=Path.of(args[0]),file=root.resolve("config/settings.json");
        check(DistributionSettings.EXPEDITION.colossusMinDistance()==15000
                && DistributionSettings.BALANCED.colossusMinDistance()==8000
                && DistributionSettings.DISCOVERY.colossusMinDistance()==4000,"presets include distinct Colossus distances");
        check(DistributionConfig.read(file).equals(DistributionSettings.DISCOVERY) && !Files.exists(file),"missing config selects the highest-frequency preset without writing");
        DistributionConfig.directory(root.resolve("unconfigured"));
        check(DistributionConfig.forNewWorld(root.resolve("untouched-world")).equals(DistributionSettings.DISCOVERY),"new worlds inherit Discoveries when no installation or world choice exists");
        check(!Files.exists(DistributionConfig.file()) && !Files.exists(root.resolve("untouched-world")),"default lookup creates neither a config nor a world directory");
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
        var legacyConfig=JsonParser.parseString(valid).getAsJsonObject();
        legacyConfig.getAsJsonObject("settings").remove("colossusMinDistance");
        Path legacyFile=root.resolve("legacy-settings.json");Files.writeString(legacyFile,legacyConfig.toString());
        check(DistributionConfig.read(legacyFile).cellSize()==2000
                && DistributionConfig.read(legacyFile).colossusMinDistance()==30000,"old configs retain historical Colossus distance, independent of density");
        check(Files.readString(legacyFile).equals(legacyConfig.toString()),"reading old config never rewrites it");
        for(String bad:List.of("0","3999","100001","8000.5","null")) {
            var invalid=JsonParser.parseString(valid).getAsJsonObject();
            invalid.getAsJsonObject("settings").add("colossusMinDistance",JsonParser.parseString(bad));
            Path badFile=root.resolve("bad-colossus.json");Files.writeString(badFile,invalid.toString());
            rejected(()->DistributionConfig.read(badFile),"invalid Colossus distance rejected: "+bad);
        }
        DistributionConfig.write(file,DistributionSettings.BALANCED);
        check(Files.readString(file.resolveSibling("settings.json.bak")).equals(valid),"explicit save preserves old file");
        for(String bad:List.of(valid.replace("2000","2000.5"),valid.replace("\"format\": 1","\"format\": 1.5"),
                valid.replace("\"format\": 1","\"format\": 2"),valid.replace("\"format\": 1","\"extra\": 0, \"format\": 1"),
                valid.replace("\"cellSize\"","\"unknown\""),valid.replace("6000","4000"),"{}","broken")) {
            Files.writeString(file,bad);rejected(()->DistributionConfig.read(file),"malformed/unsafe config rejected");
            check(Files.readString(file).equals(bad),"invalid file preserved");
        }
        for(boolean region:new boolean[]{false,true})for(int ticket=0;ticket<10000;ticket++)
            check(DistributionSettings.LEGACY_EXPEDITION.ticket(ticket,region)==DistributionPlanner.ticket(ticket,region),"historical ticket layout unchanged");
        var towerOnly=new DistributionSettings(2000,800,6000,2400,List.of(0,0,0,10000,0,0),List.of(0,0,0,10000,0,0));
        var none=new DistributionSettings(2000,800,6000,2400,Collections.nCopies(6,0),Collections.nCopies(6,0));
        var closer=new DistributionSettings(2000,800,6000,2400,towerOnly.outside(),towerOnly.inside(),BiomeRules.STANDARD,8000);
        var pendingPlanner=new DistributionPlanner(closer.policy(),closer,731204,EnumSet.allOf(Family.class),
                DistributionSettingsTests::site,()->null,()->false,0,0,128);
        check(pendingPlanner.plan(new Cell(0,0))!=null,"spawn neighborhood remains safe before closer Colossus resolves");
        boolean pending=false;try{pendingPlanner.plan(new Cell(4,0));}catch(Pending expected){pending=true;}
        check(pending,"closer Colossus shrinks the safe unresolved planning disk");
        for(int ticket=0;ticket<10000;ticket++)check(towerOnly.mayMatch(ticket,Set.of(Family.TOWER))
                && !towerOnly.mayMatch(ticket,Set.of(Family.SKULL)),"locate uses customized shares including formerly empty tickets");
        rejected(()->new DistributionSettings(2000,800,6000,2400,List.of(0,0,0,10001,0,0),List.of(0,0,0,10000,0,0)),"overfull shares rejected");
        rejected(()->new DistributionSettings(2000,800,6000,2400,List.of(1,0,0,0,0,0),Collections.nCopies(6,0)),"anchor chance independent of region");
        rejected(()->new DistributionPlanner(POLICY,towerOnly,1,Set.of(),(c,f)->null,()->null,()->true,0,0,0),"old policy cannot adopt new settings");
        for(var settings:List.of(DistributionSettings.EXPEDITION,DistributionSettings.BALANCED,DistributionSettings.DISCOVERY,DistributionSettings.LEGACY_EXPEDITION,towerOnly,none)) {
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
            if(settings==DistributionSettings.LEGACY_EXPEDITION) {
                var legacy=new DistributionPlanner(POLICY,731204,EnumSet.allOf(Family.class),DistributionSettingsTests::site,()->null,()->true,0,0,128);
                for(Cell cell:cells)check(Objects.equals(results.get(cell),legacy.plan(cell)),"default v3 plans exactly match released v2");
            }
        }
        var oldSearch=annulus(731204,-336,80,4000,8000,-100000,-100000,100000,100000);
        check(ColossusSearch.annulus(731204,-336,80,4000,8000,-100000,-100000,100000,100000,1).equals(oldSearch),"released unique candidate order is byte-for-byte reproducible");
        var nearby=ColossusSearch.annulus(731204,-336,80,4000,8000,-100000,-100000,100000,100000,2);
        check(nearby.size()>oldSearch.size(),"new search tests multiple local positions rather than abandoning a cell");
        check(nearby.equals(ColossusSearch.annulus(731204,-336,80,4000,8000,-100000,-100000,100000,100000,2)),"new search resumes the same candidate cursor after restart");
        check(new HashSet<>(nearby).size()==nearby.size(),"unique local probes never repeat");
        double last=0;
        for(Candidate c:nearby){double d=distance(c,-336,80);check(c.unique() && d>=4000 && d<8000 && d>=last,"new probes are unique, inside the ring and nearest first");last=d;}
        for(boolean regional:new boolean[]{false,true}) {
            var counts=new EnumMap<Family,Integer>(Family.class);
            for(int t=0;t<10000;t++)counts.merge(DistributionSettings.DISCOVERY.ticket(t,regional),1,Integer::sum);
            check(counts.get(Family.SKULL)==(regional?2500:1500) && counts.get(Family.SKULL_2)==(regional?2500:1500),"new skull weights are exact before terrain rejection");
            check(counts.get(Family.TOWER)==200 && counts.get(Family.TREE)==200 && counts.get(Family.SMALL)==200,"non-skull family shares preserved");
        }
        check(DistributionSettings.DISCOVERY.generationRevision()==2 && DistributionSettings.LEGACY_EXPEDITION.generationRevision()==1,"new and released generation contracts remain distinct");
        for(Family f:Family.values())if(f!=Family.EMPTY)check(DistributionSettings.DISCOVERY.biomes().rule(f).mode()==BiomeRules.Mode.LANDSCAPES,"presets include matching landscapes for every family");
        var predicate=JsonParser.parseString("{\"type\":\"lithostitched:all_of\",\"conditions\":[{\"type\":\"lithostitched:in_biome\",\"biomes\":\"#relics:has_structure/titan_skull\"},{\"type\":\"relics:dry_land\"},{\"type\":\"lithostitched:not\",\"condition\":{\"type\":\"lithostitched:in_biome\",\"biomes\":\"#minecraft:is_ocean\"}}]}").getAsJsonObject();
        check(GenerationRules.terrain(predicate,Family.SKULL,BiomeRules.Mode.LANDSCAPES,1).equals(predicate),"old landscape worlds keep their original footprint predicates");
        check(GenerationRules.terrain(predicate,Family.SKULL,BiomeRules.Mode.STANDARD,2).equals(predicate),"explicit Standard biome mode keeps original palette gates");
        var expanded=GenerationRules.terrain(predicate,Family.SKULL,BiomeRules.Mode.LANDSCAPES,2);
        check(expanded.getAsJsonArray("conditions").size()==2 && expanded.toString().contains("#minecraft:is_ocean") && expanded.toString().contains("relics:dry_land"),"expanded footprints retain ocean and dry-land protections");
        check(predicate.getAsJsonArray("conditions").size()==3,"effective rules never mutate pinned historical assets");
        var slope=JsonParser.parseString("{\"type\":\"lithostitched:height_filter\",\"heightmap\":\"WORLD_SURFACE_WG\",\"range_type\":\"heightmap_relative\",\"permitted_range\":{\"min_inclusive\":-4,\"max_inclusive\":4}}").getAsJsonObject();
        check(GenerationRules.terrain(slope,Family.SKULL_2,BiomeRules.Mode.LANDSCAPES,1).equals(slope),"old Sword Skull slope preserved");
        check(GenerationRules.terrain(slope,Family.SKULL_2,BiomeRules.Mode.LANDSCAPES,2).getAsJsonObject("permitted_range").get("max_inclusive").getAsInt()==8,"new Sword Skull permits modest rolling terrain");
        var encodedSlope=slope.deepCopy();JsonArray encodedRange=new JsonArray();encodedRange.add(-4);encodedRange.add(4);encodedSlope.add("permitted_range",encodedRange);
        var actualCodec=GenerationRules.terrain(encodedSlope,Family.SKULL_2,BiomeRules.Mode.LANDSCAPES,2);
        check(actualCodec.getAsJsonArray("permitted_range").get(1).getAsInt()==8,"native 1.21.1 codec array form is widened without object casts");
        check(encodedSlope.getAsJsonArray("permitted_range").get(0).getAsInt()==-4,"native encoded source remains immutable");
        check(DistributionSettings.DISCOVERY.policy().equals("relics-distribution-v4-discoveries") && DistributionSettings.LEGACY_EXPEDITION.policy().equals("relics-distribution-v3-settings"),"new journals use a policy rejected by released binaries");
        rejected(()->new DistributionPlanner(DistributionSettings.LEGACY_POLICY,DistributionSettings.DISCOVERY,1,Set.of(),(c,f)->null,()->null,()->true,0,0,0),"new rules cannot masquerade as a released plan");
        // New global defaults must not alter the checksummed per-world snapshot.
        Path world=root.resolve("world.json");var initial=new DistributionJournal.State();initial.settings=towerOnly;initial.policy=towerOnly.policy();
        initial.fingerprint="a".repeat(64);initial.enabled=EnumSet.allOf(Family.class);initial.minX=initial.minZ=-100000;initial.maxX=initial.maxZ=100000;initial.frozen=true;
        new DistributionJournal(world,initial).flush();DistributionConfig.write(file,DistributionSettings.EXPEDITION);
        check(new DistributionJournal(world,null).state.settings.equals(towerOnly),"world keeps independent settings after defaults change");
        initial.settings=biomeSettings;new DistributionJournal(root.resolve("biome-world.json"),initial).flush();
        check(new DistributionJournal(root.resolve("biome-world.json"),null).state.settings.biomes().equals(custom),"saved biome rules survive restart");
        Path closerWorld=root.resolve("closer-world.json");
        var closerState=new DistributionJournal.State();closerState.settings=closer;closerState.policy=closer.policy();
        closerState.fingerprint="b".repeat(64);closerState.enabled=EnumSet.allOf(Family.class);closerState.minX=closerState.minZ=-100000;
        closerState.maxX=closerState.maxZ=100000;closerState.frozen=true;closerState.lower=8000;closerState.upper=16000;
        var closeCandidate=annulus(731204,0,0,8000,16000,-100000,-100000,100000,100000).getFirst();
        closerState.unique=site(closeCandidate,Family.COLOSSUS);new DistributionJournal(closerWorld,closerState).flush();
        var restoredClose=new DistributionJournal(closerWorld,null).state;
        check(restoredClose.unique.equals(closerState.unique) && restoredClose.colossusMinDistance()==8000,"closer Colossus and ring survive restart");
        var oldEnvelope=JsonParser.parseString(Files.readString(root.resolve("biome-world.json"))).getAsJsonObject();
        var oldPayload=JsonParser.parseString(oldEnvelope.get("payload").getAsString()).getAsJsonObject();
        oldPayload.getAsJsonObject("settings").remove("colossusMinDistance");
        oldPayload.getAsJsonObject("settings").remove("generationRevision");
        oldEnvelope.addProperty("payload",oldPayload.toString());oldEnvelope.addProperty("sha256",DistributionJournal.hash(oldPayload.toString()));
        Path oldWorld=root.resolve("released-world.json");Files.writeString(oldWorld,oldEnvelope.toString());
        check(new DistributionJournal(oldWorld,null).state.colossusMinDistance()==30000,"released worlds keep 30000 even when other fields match Discoveries");
        check(new DistributionJournal(oldWorld,null).state.settings.generationRevision()==1,"missing revision retains the released algorithm");
        check(Files.readString(oldWorld).equals(oldEnvelope.toString()),"old world read preserves original journal bytes");
        var future=new DistributionJournal.State();future.settings=DistributionSettings.DISCOVERY;future.policy=DistributionSettings.POLICY;
        future.fingerprint="c".repeat(64);future.enabled=EnumSet.allOf(Family.class);future.minX=future.minZ=-100000;future.maxX=future.maxZ=100000;future.frozen=true;
        Path futureFile=root.resolve("new-revision.json");new DistributionJournal(futureFile,future).flush();
        check(new DistributionJournal(futureFile,null).state.settings.generationRevision()==2,"new policy and revision survive a save/reload");
        var mismatch=JsonParser.parseString(Files.readString(futureFile)).getAsJsonObject();var mismatchedPayload=JsonParser.parseString(mismatch.get("payload").getAsString()).getAsJsonObject();
        mismatchedPayload.addProperty("policy",DistributionSettings.LEGACY_POLICY);mismatch.addProperty("payload",mismatchedPayload.toString());mismatch.addProperty("sha256",DistributionJournal.hash(mismatchedPayload.toString()));
        Files.writeString(futureFile,mismatch.toString());rejected(()->new DistributionJournal(futureFile,null),"mismatched policy and revision are rejected without migration");
        var envelope=JsonParser.parseString(Files.readString(world)).getAsJsonObject();
        var payload=JsonParser.parseString(envelope.get("payload").getAsString()).getAsJsonObject();payload.remove("settings");
        envelope.addProperty("payload",payload.toString());envelope.addProperty("sha256",DistributionJournal.hash(payload.toString()));Files.writeString(world,envelope.toString());
        String damaged=Files.readString(world);rejected(()->new DistributionJournal(world,null),"v3 snapshot without settings fails closed");check(Files.readString(world).equals(damaged),"damaged world not reset");
        System.out.println("PASS: "+assertions+" distribution settings assertions");
    }
}
