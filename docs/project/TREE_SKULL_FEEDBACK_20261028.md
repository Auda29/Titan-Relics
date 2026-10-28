# Skull- und Baumkorrektur vom 28. Oktober 2026

Der Nutzer best?tigte zuletzt **50 Bl?cke Effektradius**. Das ersetzt sowohl
die urspr?nglichen 24 Bl?cke als auch den kurz vorgesehenen Wert 31,2.

## Titan Skull 2

Der braune Klumpen im Screenshot ist der separate Quellsplitter
`09 | Local broken bone chip.001` bei [40,1,-36]. Die neue additive Revision
`titan-skull-2-v2-embedded-side-v1` entfernt exakt 147 Dripstone-Bl?cke.
Alle ?brigen NBT-Blockeintr?ge sind bytegleich erhalten. Abmessungen, Offset,
Bodenh?he 28 und Clip-Tiefe 6 bleiben gleich. Die urspr?ngliche Revision bleibt
f?r ?ltere Welten verf?gbar. Der Modellauftrag wurde mit Astra auf high bearbeitet.

[Vorher/Nachher](../../relics/titan-skull/design/generated/titan-skull-2-v2-embedded-side-v1/before-after.png) ?
[Hashgebundener Modellbericht](../../relics/titan-skull/design/generated/titan-skull-2-v2-embedded-side-v1/MODEL_REPORT.md)

Neue Welten verwenden die Variante ?ber `interiors-20261028-v5`. Eine leere
Aktionsliste im Auswahlzertifikat bindet das neue Template an seine Revision;
es entstehen keine neuen Lootmarker oder Spielmechaniken am Skull. V1 bis V4
und die visuelle Basisauswahl bleiben unver?ndert verf?gbar.

## Leuchtb?sche am Weltenbaum

Die drei Leuchtb?sche im Quellmodell standen auf einzelnen Rooted-Dirt-Bl?cken
in fester H?he. Die begrenzte Fundamentkorrektur des Baums konnte gr??ere
H?henunterschiede darunter nicht schlie?en. Dadurch schwebte das ganze Paar.

Der Terrainprozessor setzt diese drei Busch-/Erdpaare im selben X/Z-Feld auf
nahegelegenen tats?chlichen Boden. Die Suche ist auf sechs Bl?cke nach oben und
unten begrenzt und liest ausschlie?lich im gerade platzierten Chunk. Der
Erdblock ersetzt eine geeignete feste Bodenoberfl?che; darunter muss bereits
fester Untergrund sein. Der Busch ben?tigt freien, trockenen Platz dar?ber.
Quellbl?cke des Baums werden dabei nicht ?berschrieben. Falls kein sicherer
Platz existiert, entfallen beide Bl?cke. Es wird keine Erds?ule angelegt.

Baum-NBT, Wurzeln, Stamm, Krone, Leuchtpilze, Ranken und Amethyst bleiben
unver?ndert. Die Korrektur gilt f?r neue Platzierungen auch in den bisherigen
Weltrevisionen; bereits gespeicherte Strukturen werden nicht umgebaut.

## Aura

Der Radius betr?gt 50 Bl?cke als dreidimensionale Kugel um die Mitte des
gespeicherten Ankerblocks. Die r?umliche Suche umfasst nun auch Anker zwei
32-Block-Zellen weiter. Regeneration I, Wirkung durch W?nde und die f?nf Minuten
Nachwirkung bleiben erhalten. Die ?nderung gilt auch f?r registrierte B?ume
bestehender Welten nach Installation der neuen JAR.

[Pr?fungen, Grenzen und Testbuild](../testing/TREE_SKULL_FEEDBACK_20261028.md).
Zum Pr?fen der neuen Skull-Geometrie und bereits bebauter Baumstellen eine neue
Testwelt verwenden. Bestehende Originalwelten bleiben unangetastet.
