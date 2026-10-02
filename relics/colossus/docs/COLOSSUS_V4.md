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

Dies ist eine visuelle Überarbeitung, keine Umsetzung von Maschinenkern, Magnet,
Prüfung, Loot oder endgültigen Innenräumen. Schutz vor Terrain-Features und die
teure natürliche Suche bleiben eigene technische Aufgaben. Bei geänderten
Abmessungen müssen Bodenniveau, Platzierungsfilter und Zentrierung neu geprüft
werden; V4 wird nicht allein durch diese Notizen zum Standard-Build.
