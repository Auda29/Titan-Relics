package de.relics.gameplay;

/** Persisted provenance set only by the managed natural structure-start planner. */
public interface NaturalPiece {
    void relics$setSite(String certificate);
    String relics$site();
}
