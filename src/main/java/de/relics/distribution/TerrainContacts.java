package de.relics.distribution;

import de.relics.TerrainSupportProcessor;
import java.util.*;
import java.util.function.IntPredicate;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.NoiseColumn;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate.StructureBlockInfo;

/** Frozen low undersides for a template with bounded terrain support. */
final class TerrainContacts {
    private record Contact(int y,int reach) { }
    private record Column(int x,int z,int minSubstrate,List<Contact> contacts) { }
    @FunctionalInterface interface BaseTerrain { NoiseColumn column(int x,int z); }
    private final List<Column> columns;

    TerrainContacts(List<StructureBlockInfo> blocks,TerrainSupportProcessor processor) {
        int ground=processor.groundY();
        var authored=new HashSet<BlockPos>();
        var movedBushSoil=new HashSet<BlockPos>();
        for(var block:blocks) {
            var state=block.state();
            if(!state.is(Blocks.JIGSAW) && !state.is(Blocks.STRUCTURE_BLOCK)
                    && TerrainSupportProcessor.supportsTerrainContact(state))
                authored.add(block.pos());
            if(processor.rootSupport() && state.is(Blocks.FIREFLY_BUSH))
                movedBushSoil.add(block.pos().below());
        }

        var soilBottoms=new HashMap<Long,Integer>();
        for(var block:blocks) {
            BlockPos p=block.pos();
            if(p.getY()<=ground && TerrainSupportProcessor.isSupportSoil(block.state())
                    && !(block.state().is(Blocks.ROOTED_DIRT) && movedBushSoil.contains(p)))
                soilBottoms.merge(BlockPos.asLong(p.getX(),0,p.getZ()),p.getY(),Math::min);
        }
        var byColumn=new HashMap<Long,List<Contact>>();
        for(var block:blocks) {
            BlockPos p=block.pos();
            var state=block.state();
            if(p.getY()>ground || state.is(Blocks.JIGSAW) || state.is(Blocks.STRUCTURE_BLOCK)
                    || state.is(Blocks.ROOTED_DIRT) && movedBushSoil.contains(p))continue;
            boolean soil=TerrainSupportProcessor.isSupportSoil(state);
            if(!soil && !TerrainSupportProcessor.isSupportArt(state))continue;
            long column=BlockPos.asLong(p.getX(),0,p.getZ());
            BlockPos below=p.below();
            if(authored.contains(below) && !movedBushSoil.contains(below))continue;
            boolean canExtend=soil?p.getY()==soilBottoms.get(column):processor.supportArt();
            boolean outsideContactBand=processor.surfaceContactDepth()>=0 && p.getY()<ground-processor.surfaceContactDepth();
            int reach=canExtend && !outsideContactBand?processor.maxSupportDepth():0;
            // Another authored run within reach can end the extension earlier.
            // Its own lowest contact is also tested if it needs support.
            boolean authoredSupport=false;
            for(int gap=1;gap<=reach;gap++) {
                BlockPos socket=below.below(gap);
                if(authored.contains(socket) && !movedBushSoil.contains(socket)) {
                    authoredSupport=true;
                    break;
                }
            }
            if(!authoredSupport)byColumn.computeIfAbsent(column,k->new ArrayList<>())
                    .add(new Contact(p.getY(),reach));
        }
        columns=byColumn.entrySet().stream().map(e->{
            BlockPos p=BlockPos.of(e.getKey());
            var contacts=List.copyOf(e.getValue());
            int minSubstrate=contacts.stream().mapToInt(c->c.y-1-c.reach).max().orElseThrow();
            return new Column(p.getX(),p.getZ(),minSubstrate,contacts);
        // Check the most demanding elevations across the footprint first.
        }).sorted(Comparator.comparingInt(Column::minSubstrate).reversed()
                .thenComparingLong(c->DistributionPlanner.mix(BlockPos.asLong(c.x,0,c.z)))
                .thenComparingInt(Column::x).thenComparingInt(Column::z)).toList();
    }

    boolean fits(BlockPos origin,Rotation rotation,int maximumSurface,int maxY,int minY,BaseTerrain terrain) {
        for(Column contactColumn:columns) {
            BlockPos offset=StructureTemplate.transform(new BlockPos(contactColumn.x,0,contactColumn.z),
                    net.minecraft.world.level.block.Mirror.NONE,rotation,BlockPos.ZERO);
            NoiseColumn column=terrain.column(origin.getX()+offset.getX(),origin.getZ()+offset.getZ());
            for(Contact contact:contactColumn.contacts) {
                int bottom=origin.getY()+contact.y;
                if(!reachesSubstrate(bottom,contact.reach,minY,
                        y->TerrainSupportProcessor.supportsTerrainContact(column.getBlock(y))))return false;
            }
            // Keep the old uphill allowance at real contacts and reject wet
            // support columns even when they fall between coarse grid points.
            int top=maxY;
            while(top>=minY && column.getBlock(top).isAir())top--;
            if(top+1>maximumSurface || top<minY
                    || !Heightmap.Types.OCEAN_FLOOR_WG.isOpaque().test(column.getBlock(top)))return false;
        }
        return true;
    }

    static boolean reachesSubstrate(int bottom,int reach,int minY,IntPredicate substrate) {
        for(int y=bottom-1;y>=minY && y>=bottom-1-reach;y--)
            if(substrate.test(y))return true;
        return false;
    }
}
