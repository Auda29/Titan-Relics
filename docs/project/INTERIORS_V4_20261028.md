# Innenraumstand V4 vom 28. Oktober 2026

Gro?er Koloss V7 ist vorl?ufig und Obelisk V6 ist vom Nutzer abgenommen.
Ihre exportierte Geometrie, Spielmarker und abgeleiteten Templates bleiben exakt erhalten.
Kleiner Koloss V11, Turmruine V10 und das neue Monolith-Muster brauchen noch
Niklas' Sichtpr?fung im Spiel.

## ?nderungen

- Kleiner Koloss: unterer Zugang sechs Bl?cke k?rzer, neuer Start [62,14,46].
  Oberer Truhenstand, beide Treppen und s?mtliche Marker bleiben erhalten.
  [V10/V11-Vergleich](../../relics/colossus/design/generated/small-colossus-v11-short-entry/comparison-v10-v11.png).
- Turmruine: genau eine Truhe in einem besch?digten Maschinenrahmen, mittig
  an der R?ckwand gegen?ber dem Eingang, [58,15,55], Richtung north.
  Begehbarer Bedienbereich und freier Deckelraum; Lootbudget und Endermen bleiben gleich.
  [Blick vom Eingang](../../relics/ruined-tower/design/generated/ruined-tower-v10-chest/entry-review.png).
- Monolith: getrennte schmale vertikale Zeichen mit kantigen Abzweigungen.
  Die alten Masken ?bermalten transparente R?stungsfl?chen und teilten sich
  Brust- und f?lschlich eingezeichnete Beinfl?chen. Neue Masken respektieren
  die tats?chlichen Fl?chen und Aussparungen. Materialfarbe bleibt frei w?hlbar.
  [Vergleich auf nativer R?stungsgeometrie](reviews/monolith-trim-20261028/comparison-review.png).

## Integration und Welten

Der [kombinierte Index](reviews/interiors-short-entry-tower-20261028-handoff.json)
?bernimmt Small V11 und Tower V10 ausdr?cklich aus beiden getrennten Handoffs;
kein Index ?berschreibt dabei das jeweils andere neue Modell. Die unver?nderten
Modelle Gro?er Koloss V7, Obelisk V6 und Weltenbaum V5 stammen aus dem bisherigen Stand.

Neue Welten verwenden `interiors-20261028-v4`. Die Manifeste und Templates von
V1, V2 und V3 bleiben bytegleich erhalten. Auch neu erzeugte Chunks einer bereits
bestehenden Welt verwenden deren gespeicherte Revision. Zum Pr?fen der neuen
Geometrie deshalb eine neue Testwelt erstellen. Keine alten Welten l?schen.

Terrain wird nur in begrenzten, vom Quellmodell freien Zellen ger?umt.
Die Erz-Erweiterung gilt in V4 auch f?r die Turmtruhe. Native B?sche werden
in den begrenzten freien Zellen der beiden neuen Modelle ebenfalls entfernt; Quellbl?cke und fremde
Strukturen bleiben gesch?tzt. Die Friedlich-Absturzkorrektur bleibt erhalten.

## Monolith-Reproduktion

`tools/ArmorUvEvidence.java` liest die 60 Fl?chen samt UVs aus
`HumanoidModel.createArmorMeshSet` des gepinnten 26.2-Clients, mit innerem
Offset 0,5 und ?u?erem Offset 1. `tools/prepare_monolith_review.py` ben?tigt
`--client`, `--java-home` und `--before-archive` (vorheriger Spielerbuild oder
lokales Vorher-ZIP). Es extrahiert native Texturen ausschlie?lich unter `build/`,
ordnet die zwei Graustufen den nativen Materialpaletten zu und schreibt die
[UV-/Alpha-Evidenz](reviews/monolith-native-armor-26.2.json).
Danach Blender mit `--background --python tools/render_monolith_trim.py` ausf?hren.
`tools/compose_monolith_review.py` beschriftet die sechs erzeugten Ansichten.
Die Vergleichstafel zeigt vorne/hinten sowie Smaragd, Amethyst und
Kupfer auf der echten R?stungsgeometrie. Licht und neutrale Puppe sind Pr?fmittel;
die Bilder sind keine Screenshots aus Minecraft.

Nur die zwei Besatzmasken ?ndern sich an den ausgelieferten Kunstressourcen.
Itembilder, Atlasdefinition, Schmiederezepte, Materialzuordnung und Werte bleiben
identisch. Bestehende verzierte R?stungen zeigen das Muster nach Spielneustart
oder Ressourcen-Neuladen ebenfalls in alten Welten.

## Pr?fung und Build

Der [Testbericht](../testing/INTERIORS_V4_20261028.md) enth?lt die Ergebnisse der
Export-, Clearance-, Naturgenerierungs-, Drehungs-, Neustart- und Upgradepr?fungen
sowie den finalen JAR-Hash und Installationsstatus.
