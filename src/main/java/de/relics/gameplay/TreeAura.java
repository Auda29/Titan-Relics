package de.relics.gameplay;

public final class TreeAura {
    private TreeAura() { }
    /** Feet-to-builder-block-center sphere, inclusive boundary and no visibility test. */
    public static boolean contains(GameplayLedger.Point anchor, double x, double y, double z) {
        double dx = x - (anchor.x() + 0.5), dy = y - (anchor.y() + 0.5), dz = z - (anchor.z() + 0.5);
        return dx * dx + dy * dy + dz * dz <= 24 * 24;
    }
}
