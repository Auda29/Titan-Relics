package de.relics.gameplay;

import net.minecraft.world.level.saveddata.maps.MapItemSavedData;

public final class ExpeditionMaps {
    private ExpeditionMaps() { }
    /** Equivalent to 26.2 createFresh at scale 2, without allocating a 16 KiB map each tick. */
    public static int center(int coordinate) { return (int)(Math.floorDiv((long)coordinate + 64, 512) * 512 + 192); }
    public static boolean matches(MapItemSavedData map, GameplayLedger.Point target) {
        return map != null && map.dimension.identifier().toString().equals(target.dimension()) && map.scale == 2
                && map.centerX == center(target.x()) && map.centerZ == center(target.z());
    }
}
