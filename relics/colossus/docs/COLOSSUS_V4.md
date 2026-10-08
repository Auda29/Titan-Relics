# Colossus V4 — Ingame-Erkenntnisse und Überarbeitung

Stand: 2. Oktober 2026.
Status: **V4-Modell-/Exportstudien erstellt; Variante B mit dem offenen
Maschinengerüst wurde am 2. Oktober 2026 vom Nutzer ausgewählt.** Grundlage ist der [Colossus V3](COLOSSUS_V3.md)
in Alpha 3; V3 bleibt unverändert erhalten und im Build ausgewählt.
Ergebnisse, Vergleichsbilder und Befehle: [V4 export studies](COLOSSUS_V4_EXPORTS.md).

**Nachtrag: V4.1-Handkorrektur.** Die aufgerichtete V4-Hand erinnerte den Nutzer
an Iron Mans Schusshaltung. Gewünscht und umgesetzt ist nun eine flach liegende,
nach oben geöffnete rechte Hand mit hochgekrümmten Fingern. Bei zusätzlicher
Verschüttung sollen möglichst die Fingerspitzen erkennbar bleiben.
[V4.1 mit Vergleich und höherer Geländeprobe](COLOSSUS_V4_1.md).
Die Brustauswahl B bleibt bestehen. Der Nutzer hat das Aussehen des Colossus
inklusive V4.1-Handkorrektur am 2. Oktober 2026 bestätigt.

## Grundlage und Ziel

Der Nutzer bewertet den Colossus in seiner bisherigen Form bereits als sehr gut.
Die monumentale Wirkung und das Gesamtdesign sollen erhalten bleiben. Nach der
Präzisierung vom 2. Oktober 2026 konzentriert sich V4 auf **die zu saubere
Rückseite, die schwer erkennbare Hand und den einfachen Zylinder im Brustinneren**.

Screenshot-Grundlage aus dem Profil „Relic Test“, Ordner `screenshots/`:

- `2026-10-01_21.34.29.png` und `2026-10-01_21.34.32.png`: Bodenperspektive.
- `2026-10-01_21.34.46.png`: Vorder-/Seitenansicht mit abgetrenntem Arm.
- `2026-10-01_21.35.24.png`: Rückansicht.

Die Bilder liegen lokal; diese Notizen betten sie nicht ins Repository ein.
Natürliche Platzierung und bekannte technische Grenzen stehen im
[Alpha-3-Testbericht](../../../docs/testing/ALPHA_3_TEST_REPORT.md).

## Was erhalten bleiben soll

- Monumentaler Maßstab und breite, schwere Schulterpartie.
- Runder Taucherhelm, schmales Visier und seitliche Maschinenanschlüsse.
- Eigenständiger abgetrennter Arm und unterirdische Körperfortsetzung.
- Warme Metalltöne, Patina und Bewuchs als gemeinsame Materialidee.
- Gute Erkennbarkeit und Entdeckungswirkung aus der Spielerperspektive.
- Der vorhandene liegende, abgetrennte Arm bleibt als solcher bestehen; die
  Überarbeitung betrifft vor allem die Hand und gegebenenfalls ihren Anschluss.

Die Bilder begründen keine pauschale Verkleinerung. V3-Abmessungen und Bodenniveau
bleiben zunächst die Ausgangsbasis, nicht bereits festgelegte V4-Exportwerte.

## Präzisierter Änderungsumfang

| Beobachtung | Geplante Überarbeitung |
| --- | --- |
| Die Rückseite wirkt deutlich zu sauber und intakt. | Wenige größere, asymmetrische Panzerbrüche, ausgefranste Plattenränder, sichtbare Schichtdicken und stellenweise freiliegende innere Konstruktion vorsehen. Die schwere gerundete Panzerform erhalten. |
| Die Hand ist schwer als Hand erkennbar. | Eine gedrehte beziehungsweise aufwärts gerichtete Hand erproben, deren Finger aus dem Erdreich herausragen. Handfläche, abgesetzter Daumen, Fingerglieder und Zwischenräume müssen lesbar werden; der Arm bleibt grundsätzlich wie vorhanden liegen. |
| Ein großer runder Zylinder im Brustinneren wirkt zu einfach. | Ausgewählt: Variante B ersetzt ihn durch ein offenes, beschädigtes Maschinengerüst. Variante A ohne Zylinder bleibt als Vergleich erhalten. |

### Hand: nach oben ragende Finger

Die Drehung ist ein Vorschlag des Nutzers, dessen konkrete Pose noch zu prüfen
ist. Die Hand darf teilweise verschüttet bleiben, soll aber durch unterschiedlich
gebeugte, einzeln erkennbare Finger und einen seitlichen Daumen als mechanische
Hand lesbar sein. Nicht den gesamten Arm aufrichten oder durch eine neue Armform
ersetzen. Handgelenk und Übergang zum vorhandenen Unterarm müssen zur Pose passen.

### Brustinneres: Variante B ausgewählt

Der Nutzer hat am 2. Oktober 2026 **Variante B mit dem Maschinengerüst** ausgewählt.
Die beiden ausgearbeiteten Möglichkeiten sind:

1. **A – Entfernen (Vergleich):** offenerer Brusthohlraum mit verbleibender
   innerer Konstruktion.
2. **B – Ersetzen (ausgewählt):** offenes, beschädigtes Maschinengerüst aus
   unterbrochenen Ringen, Trägern und wenigen Leitungen.

Die beiden Exportstudien bearbeiten `Buried chest piston`, den glatten Zylinder
am unteren vorderen Brustbruch. Der Halskragen bleibt erhalten. Der Vergleich
zeigt das Original sowie Entfernen (A) und das ausgewählte offene Gerüst (B).
Die Gestaltung legt weder eine neue Maschine noch Loot oder die endgültige
Innenraumaufteilung fest.

### Frühere Beobachtungen

Die ursprünglichen Notizen nannten außerdem Materialwirkung, Geländekontakt und
Kopf-Hals-Übergang. Diese Punkte begründen nach der aktuellen Rückmeldung **keine
pauschale Überarbeitung** der Palette, Verschüttung oder Halskonstruktion. Sie
bleiben Hintergrundbeobachtungen; notwendige lokale Anschlüsse der drei gezielten
Änderungen sind bei deren Umsetzung zu prüfen.

## Prioritäten

1. **Rückseite:** die zu intakte Oberfläche gezielt aufbrechen.
2. **Hand:** Finger und Daumen lesbar machen; die aufwärts gerichtete Pose prüfen.
3. **Brustzylinder:** das ausgewählte offene Maschinengerüst (B) als V4-Grundlage verwenden.

## Prüfkriterien für V4

- [ ] Boden-, Front-, Seiten- und Rückansicht in echtem Gelände vergleichen.
- [ ] Gesamtsilhouette, Maßstab und der grundsätzlich vorhandene Arm bleiben erhalten.
- [ ] Die Rückseite wirkt beschädigt, bleibt aber als schwere Panzerung erkennbar.
- [ ] Handfläche, einzelne Finger, Daumen und Gelenkbereich sind auch ohne Shader lesbar.
- [ ] Die vorgeschlagene aufwärts gerichtete Handpose im Erdreich vergleichen; Finger werden nicht vollständig verschluckt.
- [ ] Handgelenk und liegender Arm sind bei der gewählten Pose konstruktiv verbunden.
- [ ] Der identifizierte Brustzylinder ist entfernt oder nachvollziehbar umgestaltet; keine neue dominante glatte Zylinderform.
- [ ] Änderungen am Brustinneren lassen Öffnungen und die bestehende Außenwirkung erhalten.
- [ ] Alle vier natürlichen Rotationen und unterschiedliche Geländehöhen prüfen.
- [ ] Ganze Struktur einschließlich Arm weiterhin vollständig über Chunkgrenzen erzeugen.

## Abgrenzung

### Lore-/Gameplay-Review vom 2. Oktober 2026

Der **große Colossus soll einmal pro Spielwelt** natürlich vorkommen; geplante
kleinere Kolosse dürfen mehrfach vorkommen. Modellvarianten oder Versionsnummern
begründen keine zusätzlichen großen Fundorte. Diese Regel ist in Alpha 3 noch
nicht umgesetzt.

Die Review nennt für den V3-Export **141.523 kupferbasierte Blöcke und 5.609
Roheisenblöcke**. Diese V3-Zahlen wurden nachgezählt, sind aber keine Materialbilanz
von V4.1. Massenabbau könnte Kern und Magnet wirtschaftlich überstrahlen und das
einmalige gemeinsame Wahrzeichen zerstören.

**Historischer Review-Stand vor den Materialstudien:** Materialbilanz und
tatsächlich gewinnbare Ressourcen prüfen und die Bergungsökonomie abstimmen.
Verwertbares
Metall gezielt konzentrieren und große Flächen wirtschaftlich unkritischer
darstellen war zunächst ein Vorschlag ohne Palettenfreigabe. **Dieser Status ist
durch die unten dokumentierte Auswahl von Materialstudie B überholt.** Weiterhin
sind weder Abbauschutz noch ein Verbot normaler Minecraft-Interaktion beschlossen.

**Historische Materialstudie A, durch B abgelöst.** Der Nutzer möchte begrenzte
Rohstoffbergung, während der Colossus erkennbar bleibt; die Form muss vollständig
erhalten bleiben. Die [separate Studie](COLOSSUS_MATERIAL_STUDY.md) ersetzt
großflächiges Metall durch Granit, Terrakotta und Andesit. Alle 223.161 belegten
Blockpositionen und 491 Blender-Meshes bleiben geometrisch identisch zu V4.1.
Statt 129.253 Kupfer- und 8.821 Roheisenblöcken enthält der Vorschlag 197 Kupfer-
und 10 Roheisenblöcke an drei zusammenhängenden Bergungsstellen. A bleibt als
Vergleich erhalten und ist nicht ausgewählt; die ursprüngliche V4.1 bleibt erhalten.

**Überarbeitung B:** Die erste Studie enthält dem Nutzer zu wenig Kupfer und
verändert sich beim Abbau optisch zu wenig. Gewünscht sind unter 50.000
Kupferblöcke und unter 256 Roheisen-Items, mit plausiblen Resten nach dem Abbau.
[Studie B](COLOSSUS_MATERIAL_STUDY_B.md) enthält 25.423 Kupferblöcke und zehn
Roheisenblöcke (= 90 Items). Größere Panzerungsflächen sind abbaubar; Kopf, Hals
und verbleibende Verbindungen bleiben erhalten. Die Form vor dem Abbau ist exakt
identisch, die Verbindungsprüfung bestanden. Am 2. Oktober 2026 hat der Nutzer
Variante B einschließlich des gezeigten Zustands nach dem Metallabbau optisch
freigegeben („ja so sieht das gut aus“). B ist damit die gewählte Materialfassung.

**Aktueller Stand:** Palette und Mengen von Materialstudie B sind als Assetauswahl
freigegeben und in Alpha 4.9 integriert. Bergungswert und Balance zu Kern/Magnet
bleiben zu prüfen. Die ursprüngliche Golem-Rolle ist jetzt als Cockpit-
Verteidigungsroboter festgelegt; heutige Auslösung, dauerhafter Kernnutzen,
Multiplayer-Belohnungen und Umsetzung der einmaligen Generierung bleiben offen.
Materialstudie B ist nicht mit der früheren Brustgeometrie-Auswahl B zu verwechseln.

**Lore-Präzisierung vom 8. Oktober:** Alle Kolosse waren bemannt; der große war
zentral, die kleineren seine Begleiter. Der Golem war ein Verteidigungsroboter im
Cockpit. Wartungssystem oder späterer Einbau sind damit keine offenen Alternativen
mehr. Der große Colossus hatte fünf, jeder kleine zwei annähernd spielergroße,
eventuell etwas größere Bediener. Der große Körperhohlraum bleibt bestehen;
ausgebaut wird hauptsächlich der Kopf als Cockpit. Eine erkennbare Luke ist der
vorgesehene Zugang, aber die Spieler finden/errichten ihren Aufstieg selbst.
Keine komplette interne Treppe oder neue Deckfolge ist beschlossen. Kleine
Kolosse bleiben betretbar, mit sehr verfallenem Innenraum und praktisch verlorenem
Cockpit aus ursprünglich schwächerem Material. Genaue Luke/Stationen, heutige
Auslösung und sichtbare Verbindungen zum Titanenkonflikt sind noch zu planen. Maschinenfragmente im
Knochen oder korrespondierende Schäden sind weiterhin Vorschläge, keine Modell-
Freigaben. Erst die Dokumentation aller Relikte und Konsistenzprüfung abschließen;
diese Lore-Antworten verändern keine bestehenden Exporte.
Details und Prioritäten: [Lore-/Gameplay-Review](../../../docs/project/LORE_GAMEPLAY_REVIEW.md).

Dies ist eine visuelle Überarbeitung, keine Umsetzung von Maschinenkern, Magnet,
Prüfung, Loot oder endgültigen Innenräumen. Schutz vor Terrain-Features und die
teure natürliche Suche bleiben eigene technische Aufgaben. Bei geänderten
Abmessungen müssen Bodenniveau, Platzierungsfilter und Zentrierung neu geprüft
werden; V4 wird nicht allein durch diese Notizen zum Standard-Build.
