# Minecraft 1.20.1: Prüfung eines Backports

Stand: 12. November 2026. Geprüfter Quellstand
`a9b90e3188b39b7f3b4ecba6d8396046bdd03795`, auf Basis von Beta 4.
Der Nutzer hat die zunächst genannte Version 1.20.2 zu 1.20.1 korrigiert.

## Ergebnis

Ein vollständiger Backport ist ein plausibles eigenes Entwicklungsprojekt.
Die grundlegenden Loader- und Worldgen-Abhängigkeiten sind verfügbar.
Ein veröffentlichungsfähiger 1.20.1-Build ist damit noch nicht nachgewiesen.
Unsere aktuellen Profile lassen sich nicht durch einen Versionswechsel allein
übernehmen. Die größten Anpassungen betreffen Koloss-Begegnung, Belohnung,
Gegenstandsdaten und die ältere Lithostitched-Schnittstelle.

Diese Prüfung umfasst Quellcode, offizielle Versionsinformationen und die
heruntergeladenen Abhängigkeits-JARs. Es wurde kein Titan-Relics-1.20.1-Profil
kompiliert und kein Minecraft-1.20.1-Client oder -Server gestartet.

## Tatsächlich geprüfte Grundlage

Die folgenden Veröffentlichungen wurden über die Modrinth-Projekt-API ermittelt,
heruntergeladen und gegen den SHA-512-Wert des Herausgebers geprüft. Anschließend
wurden Klassenpfade und Metadaten direkt aus den JARs gelesen.

| Bestandteil | Geprüfte Veröffentlichung | Befund |
|---|---|---|
| Lithostitched Fabric | [1.4.12-fabric-20.1](https://modrinth.com/mod/lithostitched/version/f9bClSa7) | 1.20/1.20.1 deklariert; passende Grundlage vorhanden, ältere API. |
| Lithostitched Forge | [1.4.12-forge-20.1](https://modrinth.com/mod/lithostitched/version/Uqt1Zm1l) | 1.20/1.20.1 deklariert; Forge wäre ein gesondertes Loader-Ziel. |
| Fabric API | [0.92.12+1.20.1](https://modrinth.com/mod/fabric-api/version/rvI2dfzR) | Fabric Loader mindestens 0.16.10 und Java mindestens 17 deklariert. Das Paket enthält bereits `fabric-data-attachment-api-v1`. |
| Fabric Loader | [Offizielle 1.20.1-Metadaten](https://meta.fabricmc.net/v2/versions/loader/1.20.1) | Loader-Veröffentlichungen vorhanden. Die konkrete Kombination muss ein Port-Profil fest pinnen und ausführen. |
| Minecraft Java | [Mojang-Versionsmanifest](https://piston-meta.mojang.com/mc/game/version_manifest_v2.json) | Das verknüpfte 1.20.1-Profil nennt Java 17 als Laufzeitbasis. Unsere bisher ältesten Spieler-JARs zielen auf Java 21. |

Die Attachment-API muss also nicht pauschal als fehlend behandelt werden.
Die benötigten Klassen `AttachmentRegistry`, `AttachmentType`, `AttachmentTarget`
und `AttachmentRegistry.Builder` sind im geprüften Fabric-API-Paket vorhanden.
Methodensignaturen, Persistenz und Verhalten unserer Anwendung sind noch nicht
gegen dieses Paket kompiliert oder im Spiel nachgewiesen. Ältere Fabric-API-
Veröffentlichungen für 1.20.1 sind dadurch nicht mitgeprüft.

Die Download-Metadaten, SHA-256-Werte und lokalen Paketprüfungen bleiben unter
`build/compatibility-1.20.1/dependencies.json` nachvollziehbar.

## Anpassungen im Projekt

### Koloss-Begegnung und persönliche Belohnung

Vault und Trial-Spawner gehören zum neueren Spielumfang. Die offiziellen
[1.21-Release-Hinweise](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21)
beschreiben diese Blöcke und den Vault-Zugang per Schlüssel.

Unser Code verwendet deren Klassen unmittelbar, unter anderem in
`RelicGameplay`, `NaturalInteriors`, `RelicTrialMixin`, `RelicVaultMixin` und
`RelicPresentation`. Der aktuelle Ansatz baut auf diesen nativen Blöcken auf.
Für 1.20.1 braucht es eigene Begegnungs-/Belohnungsadapter oder eine zuvor
geprüfte zusätzliche Backport-Abhängigkeit. Nur die sichtbaren Blöcke durch
eine normale Truhe und einen gewöhnlichen Spawner auszutauschen würde die
bisherigen Regeln nicht erhalten.

Erhalten bleiben müssten insbesondere der Golem-Ablauf, Teilnahme und Abbruch,
persönliche Schlüssel-/Belohnungsansprüche, Neustartverhalten und Schutz vor
mehrfacher Ausgabe. Die vorhandene Relics-Buchführung ist dafür eine Grundlage,
aber kein Nachweis, dass der neue Adapter bereits funktioniert.

### Gegenstände, Karten und Rezepte

Minecraft stellte das Gegenstandsformat erst mit
[1.20.5 auf strukturierte Komponenten um](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-20-5),
Abschnitt `Item Data Format`. `RelicItems` registriert eigene Komponenten für
Kernladung, Magnetverschleiß und Kartenherkunft. `RelicGameplay` liest und schreibt
weitere Komponenten für Karten, Namen und Beschreibungstexte.

Für 1.20.1 sind eine NBT-basierte Speicherung und passende Synchronisierung
einzuplanen. Rezepte, Itemmodelle, Inventar-/Aufnahmeaktionen und Tooltips müssen
gegen die ältere Spiel-API angepasst werden. Gleiche Spielregeln brauchen dabei
Tests für Speichern, Reparatur/Aufladen und die Vermeidung von Duplizierung.

Für ein Java-17-Ziel sind zusätzlich neuere Java-Sprach-/Bibliotheksverwendungen
in den übernommenen Quellen zu prüfen. Eine Angabe in den Mod-Metadaten allein
ändert weder den Bytecode noch die verwendeten Java-APIs.

### Generierung und Lithostitched

Im geprüften Lithostitched-1.4.12-Paket liegen `PlacementCondition` und die
Registrierung unter anderen Paketpfaden. `DelegatingStructure` ist vorhanden.
Die aktuell importierten Klassen `api.registry.LithostitchedRegistries` und
`impl.LithostitchedInternalHooks` fehlen unter diesen Namen. Auch die von uns
verwendeten Symbole `WORLD_SEED` und `applyModifiersAndInjections` wurden in den
Klassen des Fabric-Pakets nicht gefunden.

Betroffen sind insbesondere `RelicWorldgen`, die Placement-Conditions,
`EarlyLithostitchedPreparation` einschließlich Mixin und `TerrainValidator`.
Das belegt Anpassungsbedarf, nicht die Unmöglichkeit einer älteren Umsetzung.
Die deterministische Standortwahl, Biomvorbereitung, Signaturen, Chunkgrenzen
und Neustartpersistenz müssen nach dem Umbau gesondert nachgewiesen werden.

### Modelle, Client und Loader

Die bisherigen 1.21.1-Adapter ersetzen bereits neuere Dekorationen und passen
Rezepte, Trims, Itemmodelle sowie Menüs an. Für 1.20.1 müssen alle tatsächlich
ausgelieferten Blockpaletten zusätzlich gegen dessen Registry geprüft werden.
Ein bestandener 1.21.1-Export ist dafür kein Beleg. Die Formen der Relikte sollen
erhalten bleiben; Materialersetzungen wären gesondert festzuhalten.

Fabric ist als erstes isoliertes Port-Ziel naheliegend. Forge benötigt einen
eigenen Adapter für Registrierung, Events, Datenhaltung und Pakete. Unser
NeoForge-1.21.1-Profil ersetzt diese Arbeit nicht. Historische NeoForged-
1.20.1-Artefakte existieren in der
[älteren Forge-Artefaktfamilie](https://maven.neoforged.net/releases/net/neoforged/forge/1.20.1-47.1.106/);
daraus wird hier keine heutige Loader-Empfehlung oder geprüfte Kompatibilität
abgeleitet. Die endgültige Loader-Auswahl ist Teil der Port-Planung.

## Sinnvolle Reihenfolge und Nachweise

1. Isoliertes Fabric-1.20.1-Profil mit festgelegten Abhängigkeiten und geprüftem
   Java-Ziel aufsetzen. Zunächst Registrierung, Paketressourcen, Menü und Laden
   einer neuen Welt nachweisen.
2. Natürliche Reliktgenerierung mit dem vorhandenen Planer anbinden. Echte
   Starts, Modell-/Bodenkontakt, Gebäudefilter und Neustart prüfen.
3. Gegenstandsdaten und Rezepte portieren. Danach die Koloss-Begegnung und
   persönliche Belohnung vollständig anbinden und testen.
4. Client-/Server-Interaktionen und Mehrspieler einschließlich erneuter Anmeldung,
   Truhen, Karten, Kern, Magnet und Baum prüfen. Forge erst als weiteren expliziten
   Zielumfang ergänzen.
5. Erst nach erfolgreichem Prototyp die Release-CI, Plattformabhängigkeiten und
   Downloadverifikation für eine neue Veröffentlichung erweitern. Der bestehende
   Beta-4-Tag und dessen Acht-Dateien-Vertrag bleiben erhalten.

Ein reiner Strukturen-Prototyp wäre ein Entwicklungsnachweis. Er dürfte nicht
als vollständiger Titan-Relics-Release mit der bisherigen Gameplay-Beschreibung
veröffentlicht werden. Eine abgespeckte Edition wäre eine gesonderte Produktwahl.
Ein Downgrade vorhandener 1.21-/26.x-Welten wird nicht zugesagt.

## Einordnung für den ersten stabilen Release

Der Backport sollte den laufenden Beta-4-Survival-Test und die
[Abnahme für 1.0.0](../testing/FULL_RELEASE_ACCEPTANCE.md) nicht verändern.
1.20.1 ist keine Voraussetzung für deren Abschluss. Ein belastbarer Aufwand oder
Termin lässt sich erst nach dem ersten kompilierenden und laufenden Prototyp
angeben. Diese Prüfung verspricht noch keinen Veröffentlichungstermin und
legt weder eine neue Supportzusage noch einen Release-Tag an.
