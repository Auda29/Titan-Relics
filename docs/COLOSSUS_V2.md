# Colossus v2 – ursprünglicher Referenzentwurf

Colossus v2 bezeichnet den ersten Entwurf nach der Instagram-Referenz
[Archaean Colossi](https://www.instagram.com/reel/DaoBxUEiBNa/).
Die nachfolgende Erweiterung mit unterirdischem Bauch und abgerissener Hüfte
heißt **[Colossus v3](COLOSSUS_V3.md)**.

| Kennzahl | Colossus v2 |
| --- | --- |
| Abmessungen X/Y/Z | 181 × 160 × 227 Blöcke |
| Gesetzte Blöcke | 182.734 |
| Blocktypen | 11 |
| Teilvorlagen | 100 |

- Config: `design/colossus-v2.json`
- Generator: `tools/create_colossus_v2.py`
- Ausgaben: `design/generated/colossus-v2/`
- Bearbeitbare Quelle: `colossus-v2-source.blend`
- Referenzvergleich: `colossus-v2-reference-review.png`

Die lokalen Werkzeuge und die Konvertierungskette stehen im
[Blender-Workflow](BLENDER_WORKFLOW.md). Der Generator wird in Blender ausgeführt;
Konvertierung und Vorschauen verwenden `--config design/colossus-v2.json`
beziehungsweise `node tools/obj_to_schem.cjs design/colossus-v2.json`.
