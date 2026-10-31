package de.relics.distribution;

import java.util.List;
import java.util.Set;
import static de.relics.distribution.DistributionPlanner.Family;

/** Validated immutable new-world settings. Chances are basis points, never guaranteed sites. */
public record DistributionSettings(int cellSize,int minDistance,int obeliskDistance,int regionRadius,
                                   List<Integer> outside,List<Integer> inside,BiomeRules biomes) {
    public DistributionSettings(int cellSize,int minDistance,int obeliskDistance,int regionRadius,List<Integer> outside,List<Integer> inside) {
        this(cellSize,minDistance,obeliskDistance,regionRadius,outside,inside,BiomeRules.STANDARD);
    }
    public static final String POLICY="relics-distribution-v3-settings";
    public static final List<Integer> OUTSIDE=List.of(3000,250,250,200,200,200);
    public static final List<Integer> INSIDE=List.of(3000,1500,1500,200,200,200);
    public static final DistributionSettings EXPEDITION=new DistributionSettings(5000,2000,15000,6000,OUTSIDE,INSIDE);
    public static final DistributionSettings BALANCED=new DistributionSettings(3000,1200,9000,3600,OUTSIDE,INSIDE);
    public static final DistributionSettings DISCOVERY=new DistributionSettings(2000,800,6000,2400,OUTSIDE,INSIDE);
    public DistributionSettings {
        biomes=biomes==null?BiomeRules.STANDARD:biomes;
        outside=List.copyOf(outside);inside=List.copyOf(inside);
        if(cellSize<1500 || cellSize>10000)throw new IllegalArgumentException("relics.settings.error.cell");
        if(minDistance<512 || minDistance>Math.min(4000,cellSize))throw new IllegalArgumentException("relics.settings.error.distance");
        if(regionRadius<500 || regionRadius>12000)throw new IllegalArgumentException("relics.settings.error.region");
        if(obeliskDistance<minDistance || obeliskDistance<=2*regionRadius || obeliskDistance>4*cellSize)
            throw new IllegalArgumentException("relics.settings.error.obelisks");
        validateShares(outside);validateShares(inside);
        if(!outside.getFirst().equals(inside.getFirst()))throw new IllegalArgumentException("relics.settings.error.anchor");
    }
    private static void validateShares(List<Integer> values) {
        if(values.size()!=6 || values.stream().anyMatch(v->v<0 || v>10000)
                || values.stream().mapToInt(Integer::intValue).sum()>10000)
            throw new IllegalArgumentException("relics.settings.error.chances");
    }
    public Family ticket(int value,boolean regional) {
        if(value<0 || value>=10000)throw new IllegalArgumentException("Ticket outside 0..9999");
        // Preserve the historical ticket layout when its approved shares are unchanged.
        if(outside.equals(OUTSIDE) && inside.equals(INSIDE))return DistributionPlanner.ticket(value,regional);
        List<Integer> shares=regional?inside:outside;int end=0;
        for(int i=0;i<6;i++){end+=shares.get(i);if(value<end)return Family.values()[i+1];}
        return Family.EMPTY;
    }
    public boolean mayMatch(int value,Set<Family> requested) {
        return requested.contains(ticket(value,false)) || requested.contains(ticket(value,true));
    }
    public int empty(boolean regional){return 10000-(regional?inside:outside).stream().mapToInt(Integer::intValue).sum();}
}
