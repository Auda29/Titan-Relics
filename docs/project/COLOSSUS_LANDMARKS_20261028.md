# Koloss V7: lokale Landmarken, 28.10.2026

V7 ist eine blockgenaue Ableitung des freigegebenen V6-NBT mit SHA-256 `4c65e4cc8fd57dbccacf765241df70951a95e65e886b4ac4f17d9ebaf96c3b99`. Der ursprüngliche Katalogursprung bleibt in der Design-JSON erhalten; deren Änderungszahlen beziehen sich auf V6. NBT-Abmessungen `181 x 209 x 235`, Ground-Y `77` und DataVersion `3105` sind unverändert. Gegen V6 wurden 73 Blöcke hinzugefügt, vier entfernt und fünf ersetzt. Alle Änderungen liegen an den drei beschriebenen Stellen einschließlich der beiden alten Platzhalterpositionen. Außenschale, Hand/Finger, offenes Visier und übrige Maschinenreste bleiben außerhalb dieser Stellen erhalten.

## Orte und Räume

Koordinaten sind rohe Template-Koordinaten `[x,y,z]` vor Rotation und späterer Fundamentverschiebung.

- Armtruhe: `[110,78,70]`, Richtung `south`, weiterhin genau eine Truhe. Offene Rückwand mit seitlichen Pfeilern markiert den Fund; der Kupferblock ist nur der bestehende Truhen-Platzhalter. Die zusätzliche Region `arm_clearance` reicht von `[109,78,70]` bis `[112,82,73]` und ergänzt die vorhandenen Wegregionen. Die Zellen direkt über dem Deckel und der Zugang sind leer und abgedeckt.
- Trial Spawner: `[94,169,183]`, zuvor `[94,169,193]`. Vier Pfeiler und unterbrochene Querträger bilden einen offenen Wachrahmen. Der geschnitzte Tiefenschiefer ist der Spawner-Platzhalter.
- Golem: `[94,169,190]`, zuvor `[94,169,183]`. Die registrierte Rolle bleibt gleich; seine Fläche `[93,168,189]` bis `[95,168,191]` trägt den Golem, `[93,169,189]` bis `[95,172,191]` ist frei.
- Vault: `[94,169,164]`, Richtung `south`, zuvor `[84,169,190]`. Der Platzhalter sitzt als Instrument der mittleren der fünf Crewstationen auf dem Boden und ist von der Raumseite zugänglich. `cockpit_clearance` von `[93,169,164]` bis `[95,173,165]` ergänzt die bestehende Region am Konsolenrand.
- Luke: unverändert `[118,169,182]`, Richtung `east`. Die alten Spawner- und Vault-Platzhalter sind entfernt.

Die beiden neuen Regionen verwenden dieselben zugelassenen nativen Terrainblöcke wie V6. Der vorhandene Integrationsalgorithmus bildet daraus nur Zellen, die im exportierten NBT keinen Strukturblock enthalten. V7 selbst verändert keine Runtime-Integration; die tatsächliche Räumung muss bei der Integration mit diesem Schutz übernommen und im Spiel geprüft werden. Keine globale Terraformierung, keine zusätzlichen Belohnungen oder Bedienfunktionen.

## Prüfung und Bilder

Der bestehende Handoff-Validator prüfte Quellhash, native 26.2-Registry, Marker, Stützen, Freiräume, zusammengebaute 127 Kacheln, NBT/Schematic-Gleichheit und Pfade. Vier neue Regressionstests bestanden: lokale V6-Differenz und vier unveränderte Stationen, Wege Arm/Luke, Golemraum und Deckel, Clearance sowie Koordinaten und Blickrichtungen in vier rechnerischen Rotationen. Der Pfadtest verwendet ein konservatives zwei Blöcke hohes Spielermodell und ist kein Laufzeittest. Das NBT enthält 228100 Blöcke und hat SHA-256 `88bda1cb8edeabee23bd61562f9388f2ad2dd41cceebcb06934fb09788d837d3`.

Die Blender-Datei wurde nach dem Speichern in einem neuen Blender-5.2-Prozess geöffnet. Fünf Marker und ihre Positionen sowie 32 Meshgruppen-Objekte wurden geprüft; 247 Flächen der drei geänderten Gruppen stimmen mit dem NBT überein. Die Bilder zeigen die exportierte Geometrie; die Detailbilder sind räumlich begrenzte Ausschnitte, keine Änderungen am Export. Die Beleuchtung dient der Prüfung. Die schwebend erscheinenden Kupferstücke im Armbild sind durch die Ausschnittgrenze getrennte Teile der alten Außenschale.

- [Gesamtansicht](../../relics/colossus/design/generated/colossus-v7-landmarks/overview-review.png)
- [Armfund und Truhen-Platzhalter](../../relics/colossus/design/generated/colossus-v7-landmarks/arm-review.png)
- [Wachstruktur und Spawner-Platzhalter](../../relics/colossus/design/generated/colossus-v7-landmarks/guard-review.png)
- [Mittlere Station und Vault-Platzhalter](../../relics/colossus/design/generated/colossus-v7-landmarks/vault-review.png)
- [Hashgebundener Handoff](reviews/colossus-landmarks-20261028-handoff.json)

Die 1.122 Dateien der vorliegenden Baseline wurden byteweise gegen ihre gespeicherten Hashes geprüft und blieben unverändert. Die vier anderen Einträge im Handoff wurden unverändert übernommen.

**Noch nicht runtime-integriert.** Natürliche Generierung, Chunk-Grenzen, Rotationen im Spiel, vorhandene Welten, tatsächliches Licht und echte Truhen-/Spawner-/Vault-Funktion sind mit V7 nicht getestet. Die Bilder sind keine visuelle Endabnahme; diese bleibt beim Nutzer.

## Anschließende Integration

Die obige Grenze beschreibt den Modellauftrag. V7 wurde danach mit einer neuen,
gespeicherten Innenraumrevision in die natürliche Generierung eingebunden.
V6-Vorlagen und Marker bleiben für vorhandene Welten erhalten. Die anschließenden
Serverprüfungen und der neue Testbuild sind im
[Integrationsbericht](../testing/COLOSSUS_LANDMARKS_20261028.md) dokumentiert.
