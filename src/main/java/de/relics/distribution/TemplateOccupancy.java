package de.relics.distribution;

import java.util.*;
import static de.relics.distribution.SurfaceStructurePolicy.Box;

/** Immutable local solid-cell index; empty canopy/skull volume never counts as collision. */
public final class TemplateOccupancy {
    private final Map<Long,BitSet> columns;
    private final int sx,sy,sz;
    public TemplateOccupancy(int sx,int sy,int sz,Collection<int[]> solid) {
        this.sx=sx;this.sy=sy;this.sz=sz;Map<Long,BitSet> built=new HashMap<>();
        for(int[] p:solid) {
            if(p.length!=3 || p[0]<0 || p[0]>=sx || p[1]<0 || p[1]>=sy || p[2]<0 || p[2]>=sz)throw new IllegalArgumentException("Invalid template cell");
            built.computeIfAbsent(key(p[0],p[2]),k->new BitSet()).set(p[1]);
        }
        columns=Map.copyOf(built);
    }
    private static long key(int x,int z){return ((long)x<<32)^Integer.toUnsignedLong(z);}
    private static int[] inverse(int x,int z,int rotation) {
        return switch(rotation){case 0->new int[]{x,z};case 1->new int[]{z,-x};case 2->new int[]{-x,-z};case 3->new int[]{-z,x};default->throw new IllegalArgumentException("Invalid rotation");};
    }
    public boolean intersects(Box box,int ox,int oy,int oz,int rotation) {
        int loY=Math.max(0,box.minY()-oy),hiY=Math.min(sy-1,box.maxY()-oy);if(loY>hiY)return false;
        int minX=Integer.MAX_VALUE,minZ=Integer.MAX_VALUE,maxX=Integer.MIN_VALUE,maxZ=Integer.MIN_VALUE;
        for(int x:new int[]{box.minX(),box.maxX()})for(int z:new int[]{box.minZ(),box.maxZ()}) {
            int[] p=inverse(x-ox,z-oz,rotation);minX=Math.min(minX,p[0]);maxX=Math.max(maxX,p[0]);minZ=Math.min(minZ,p[1]);maxZ=Math.max(maxZ,p[1]);
        }
        for(int x=Math.max(0,minX);x<=Math.min(sx-1,maxX);x++)for(int z=Math.max(0,minZ);z<=Math.min(sz-1,maxZ);z++) {
            BitSet ys=columns.get(key(x,z));if(ys==null)continue;int first=ys.nextSetBit(loY);if(first>=0 && first<=hiY)return true;
        }
        return false;
    }
}
