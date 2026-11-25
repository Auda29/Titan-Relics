package de.relics.distribution;

import com.google.gson.JsonParser;
import de.relics.TerrainSupportProcessor;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.nbt.NbtAccounter;
import net.minecraft.nbt.NbtIo;
import net.minecraft.nbt.NbtUtils;
import net.minecraft.world.level.NoiseColumn;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate.StructureBlockInfo;
import static de.relics.distribution.DistributionPlanner.Family;

public final class TerrainRevisionTests {
    private static final Path DATA=Path.of("src/main/resources/data/relics");
    private record TreeSite(int center,int edge,boolean matchingEdge,boolean water,int contactDrop) { }

    public static void run() throws IOException {
        checkBiomeRouting();
        checkFrozenGeometry();
        checkRockSkullSlope();
        checkContactLimits();
    }

    private static void checkRockSkullSlope() throws IOException {
        var rock=JsonParser.parseString(Files.readString(DATA.resolve("worldgen/structure/titan_skull_rock.json")))
                .getAsJsonObject().getAsJsonObject("spawn_condition").getAsJsonObject("terrain_condition");
        var grid=GenerationRules.landscapeGrid(rock,Family.SKULL);
        var relativeFilter=rock.getAsJsonObject("condition").getAsJsonObject("condition")
                .getAsJsonArray("conditions").get(0).getAsJsonObject();
        relativeFilter.add("permitted_range",JsonParser.parseString("[-18,12]"));
        check(grid.equals(GenerationRules.landscapeGrid(rock,Family.SKULL)),"codec array preserves rock skull slope");
        for(boolean nearFoundation:new boolean[]{true,false}) {
            check(grid.accepts(100,118,118,nearFoundation),"rock skull accepts +18 dry uphill");
            check(!grid.accepts(100,119,119,nearFoundation),"rock skull rejects +19 uphill");
        }
    }

    private static void checkBiomeRouting() {
        var rules=BiomeRules.LANDSCAPES;
        var coniferous=Set.of("c:is_tree/coniferous");
        for(int revision=1;revision<=3;revision++)
            check(rules.profile(Family.TREE,"example:grove",coniferous,List.of(),revision)==null,"legacy tag routing");
        check("world_tree".equals(rules.profile(Family.TREE,"example:grove",coniferous,List.of(),4)),"convention-tagged grove");
        check(rules.profile(Family.TREE,"example:forest",Set.of(),List.of(),4)==null,"no name inference");
        check("titan_skull_sand".equals(rules.profile(Family.SKULL,"example:dunes",Set.of("c:is_desert"),List.of(),4)),"center chooses sand palette");
        check("titan_skull_rock".equals(rules.profile(Family.SKULL,"example:peak",Set.of("c:is_mountain/peak"),List.of(),4)),"center chooses rock palette");
        var custom=rules.with(Family.TREE,new BiomeRules.Rule(BiomeRules.Mode.CUSTOM,Set.of("example:estuary","example:upland")));
        check(custom.profile(Family.TREE,"example:estuary",Set.of("c:is_river"),List.of(),4)==null,"river survives center override");
        check(custom.profile(Family.TREE,"example:upland",Set.of(),List.of(),4)!=null,"custom center accepts an exact untagged ID");
        check(custom.profile(Family.TREE,"example:grove",coniferous,List.of(),4)==null,"custom center rejects unselected biomes");
        check(BiomeRules.STANDARD.profile(Family.SKULL,"example:grove",coniferous,List.of(),4)==null,"standard requires pinned center biome tag");
        check("titan_skull_sand".equals(BiomeRules.STANDARD.profile(Family.SKULL,"example:dunes",Set.of(),List.of("titan_skull_sand"),4)),"standard pinned center palette");
        check(ColossusSearch.annulus(731204,0,0,4000,5000,-10000,-10000,10000,10000,3)
                .equals(ColossusSearch.annulus(731204,0,0,4000,5000,-10000,-10000,10000,10000,4)),"same fine Colossus candidates");
    }

    private static void checkFrozenGeometry() throws IOException {
        var maxima=Map.of("colossus",180,"obelisk",135,"titan_skull",249,"titan_skull_dry",249,
                "titan_skull_sand",249,"titan_skull_rock",255,"titan_skull_2",204,"ruined_tower",92,
                "small_colossus",245,"world_tree",108);
        for(var asset:maxima.entrySet()) {
            String name=asset.getKey();
            int center=asset.getValue();
            var tag=NbtIo.readCompressed(DATA.resolve("structure/"+name+"_worldgen.nbt"),NbtAccounter.unlimitedHeap());
            int size=tag.getListOrEmpty("size").getIntOr(1,0);
            var config=JsonParser.parseString(Files.readString(DATA.resolve("worldgen/processor_list/"+name+"_terrain.json")))
                    .getAsJsonObject().getAsJsonArray("processors").get(0).getAsJsonObject();
            int bottom=center-config.get("ground_y").getAsInt();
            check(GenerationRules.fitsBuildHeight(bottom,bottom+size-1,-64,319),name+" fits just below top padding");
            check(!GenerationRules.fitsBuildHeight(bottom+1,bottom+size,-64,319),name+" clips top padding one block higher");
        }
    }

    private static void checkContactLimits() throws IOException {
        var tree=JsonParser.parseString(Files.readString(DATA.resolve("worldgen/structure/world_tree.json")))
                .getAsJsonObject().getAsJsonObject("spawn_condition").getAsJsonObject("terrain_condition");
        var grid=GenerationRules.landscapeGrid(tree,Family.TREE);
        check(grid.radius()==56 && grid.step()==28,"five by five dry-land grid spans the rooted area");
        check(grid.accepts(106,117,117,false),"uphill margin above the template center cap");
        check(!grid.accepts(106,117,116,false),"even shallow water fails at the margin");
        check(!grid.accepts(106,123,123,false),"extreme variation fails at the margin");
        check(!grid.accepts(64,62,62,false),"minimum dry-floor height is preserved");
        check(TerrainContacts.reachesSubstrate(24,2,-64,y->y==21),"two missing blocks are supported");
        check(!TerrainContacts.reachesSubstrate(24,2,-64,y->y==20),"three missing blocks fail");
        var config=new TerrainSupportProcessor(24,true,Blocks.DIRT.defaultBlockState(),true,2,3,true);
        var log=Blocks.OAK_LOG.defaultBlockState();
        var roots=new TerrainContacts(List.of(new StructureBlockInfo(new BlockPos(0,21,0),log,null),
                new StructureBlockInfo(new BlockPos(1,20,0),log,null)),config);
        var cave=column(99,Blocks.STONE.defaultBlockState());
        for(int y=93;y<=95;y++)cave.setBlock(y,Blocks.AIR.defaultBlockState());
        var filled=column(99,Blocks.STONE.defaultBlockState());
        var origin=new BlockPos(0,76,0);
        check(roots.fits(origin,Rotation.NONE,106,-64,(x,z)->100,(x,z)->100,(x,z)->x==0?filled:cave),
                "buried root can cross a cave");
        for(int y=94;y<=96;y++)cave.setBlock(y,Blocks.AIR.defaultBlockState());
        check(!roots.fits(origin,Rotation.NONE,106,-64,(x,z)->100,(x,z)->100,(x,z)->cave),
                "a contact-band root still needs substrate within reach");

        for(String asset:List.of("world_tree_gameplay_worldgen","titan_skull_2_side_v1_worldgen")) {
            boolean root=asset.startsWith("world_tree");
            int ground=root?24:28;
            var processor=new TerrainSupportProcessor(ground,true,Blocks.DIRT.defaultBlockState(),root,2,root?3:6,true);
            var contacts=new TerrainContacts(readBlocks(asset),processor);
            var siteOrigin=new BlockPos(-391,100-ground,-257);
            TerrainContacts.BaseTerrain unexpectedColumn=(x,z)->{throw new AssertionError("heightmap must reject first");};
            for(var rotation:Rotation.values()) {
                check(contacts.fits(siteOrigin,rotation,106,-64,(x,z)->100,(x,z)->100,(x,z)->filled),
                        asset+" flat ground passes in "+rotation);
                check(!contacts.fits(siteOrigin,rotation,106,-64,(x,z)->97,(x,z)->97,unexpectedColumn),
                        asset+" unsupported slope fails in "+rotation);
                check(!contacts.fits(siteOrigin,rotation,106,-64,(x,z)->100,(x,z)->99,unexpectedColumn),
                        asset+" wet contact fails in "+rotation);
                check(!contacts.fits(siteOrigin,rotation,106,-64,(x,z)->107,(x,z)->107,unexpectedColumn),
                        asset+" excessive uphill fails in "+rotation);
            }
            if(root)compareTreeSites(grid,contacts,ground);
        }
    }

    private static void compareTreeSites(GenerationRules.LandscapeGrid grid,TerrainContacts contacts,int ground) {
        // Each site's center is allowed. One outer sample varies, and the
        // remaining samples match the dry center. The drop is inside the model
        // between coarse samples, where only the contact check sees it.
        var sites=List.of(
                new TreeSite(100,100,true,false,0),
                new TreeSite(100,100,false,false,0),
                new TreeSite(100,110,true,false,0),
                new TreeSite(100,112,false,false,0),
                new TreeSite(108,112,false,false,0),
                new TreeSite(109,110,true,false,0),
                new TreeSite(100,105,false,true,0),
                new TreeSite(100,117,false,false,0),
                new TreeSite(100,100,true,false,3)
        );
        int legacyAccepted=0,revision4Accepted=0;
        for(var site:sites) {
            boolean withinCeiling=GenerationRules.fitsBuildHeight(site.center-ground,
                    site.center-ground+227,-64,319);
            if(withinCeiling && site.matchingEdge && !site.water && site.edge<=108
                    && Math.abs(site.edge-site.center)<=6)legacyAccepted++;
            var contactColumn=column(site.center-1-site.contactDrop,Blocks.STONE.defaultBlockState());
            if(withinCeiling && grid.accepts(site.center,site.edge,site.edge-(site.water?1:0),false)
                    && contacts.fits(new BlockPos(0,site.center-ground,0),Rotation.NONE,site.center+6,
                    -64,(x,z)->site.center-site.contactDrop,(x,z)->site.center-site.contactDrop,
                    (x,z)->contactColumn))revision4Accepted++;
        }
        check(legacyAccepted==2 && revision4Accepted==5,"fragmented and rolling Tree fixtures accept 2/9 then 5/9");
        System.out.printf("World Tree geometry fixtures: revision 3 accepted %d/%d, revision 4 accepted %d/%d%n",
                legacyAccepted,sites.size(),revision4Accepted,sites.size());
    }

    private static List<StructureBlockInfo> readBlocks(String asset) throws IOException {
        var tag=NbtIo.readCompressed(DATA.resolve("structure/"+asset+".nbt"),NbtAccounter.unlimitedHeap());
        var palette=tag.getListOrEmpty("palette").compoundStream()
                .map(state->NbtUtils.readBlockState(BuiltInRegistries.BLOCK,state)).toList();
        return tag.getListOrEmpty("blocks").compoundStream().map(block->{
            var pos=block.getListOrEmpty("pos");
            return new StructureBlockInfo(new BlockPos(pos.getIntOr(0,0),pos.getIntOr(1,0),pos.getIntOr(2,0)),
                    palette.get(block.getIntOr("state",-1)),null);
        }).toList();
    }

    private static NoiseColumn column(int top,BlockState cap) {
        var states=new BlockState[384];
        Arrays.fill(states,Blocks.AIR.defaultBlockState());
        Arrays.fill(states,0,top+64,Blocks.STONE.defaultBlockState());
        states[top+64]=cap;
        return new NoiseColumn(-64,states);
    }

    private static void check(boolean condition,String message) {
        if(!condition)throw new AssertionError(message);
    }
}
