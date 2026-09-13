# Relic Mod: technischer Umsetzungsplan

Stand: 13.09.2026

Status: Entwicklungsplan für die vollständige Version 0.1. Alpha 2 für Minecraft 26.2 / Fabric 0.19.5 ergänzt Verfall und Geländeübergänge. Der aktuelle Implementierungsstand steht in der [README](README.md), tatsächlich ausgeführte Prüfungen im [Alpha-2-Testbericht](docs/ALPHA_2_TEST_REPORT.md). Die nachfolgenden vollständigen Abnahmekriterien sind damit nicht automatisch erfüllt.

Dieses Dokument beschreibt Architektur, Bauprozess, Generierung und Abnahme. Die [Lore-Bibel](LORE-BIBLE.md) beschreibt Atmosphäre und gestalterische Anforderungen. Der [ursprüngliche Modplan](Minecraft-Relikte-Modplan.md) bleibt als Ausgangsdokument erhalten. Neue Zahlen und technische Festlegungen unten sind Vorschläge für die Prototypen, keine bereits gemessenen Eigenschaften.

## 1. Ziel und Umfang

Version 0.1 ergänzt die Oberwelt um zwei seltene, natürlich generierte Strukturen: einen Wüstenobelisk und einen überwachsenen Koloss. Beide bestehen zunächst aus Vanilla-Blöcken. Der Koloss erhält einen zugänglichen Innenraum und ein zugehöriges abgetrenntes Bauteil.

Die Mod soll sich in das vorhandene Modpack mit Terralith, Tectonic, Biomes O' Plenty und Dungeons & Taverns einfügen. Gelände und Biome bleiben Aufgabe dieser Umgebung. Unsere Arbeit betrifft Strukturvorlagen, Standortwahl, lokale Einbettung und Häufigkeit.

| Umfang | Inhalt |
| --- | --- |
| Version 0.1 | Obelisk und Koloss; je eine fertige Grundform; natürliche Generierung; Geländeprüfungen; reproduzierbare Ausrichtung; Auswahl und Dichte konfigurierbar |
| Nach erfolgreicher Grundform | Je eine zweite kontrollierte Variante, sofern sie mit dem gleichen Prüfaufwand abgenommen werden kann |
| Späterer Ausbau | Ruinenturm und Titanenschädel, danach gesonderter Weltenbaum-Prototyp |
| Optionale spätere Ideen | Eigenständig platzierte Maschinenfragmente, eingeschlossener Uralter, gespaltenes Monument |
| Außerhalb von 0.1 | Bewegliche Mechs, Bosskämpfe, eigene Dimensionen, neue Materialien, Quests, neue Sounds, nachträgliche Generierung in bestehenden Chunks |

Ein Arm, der zum Koloss gehört, zählt zu dessen Strukturverbund. Ein unabhängig generierter Arm mit eigener Standortwahl wäre ein zusätzlicher Relikttyp und gehört nicht automatisch zu 0.1.

## 2. Zielumgebung verbindlich erfassen

Vor Projektgerüst und Exportformaten wird ein aktueller Modpack-Export ausgewertet. Frühere Angaben zu Minecraft 1.21.1 und Fabric bleiben unbestätigt.

| Festlegung | Benötigter Nachweis |
| --- | --- |
| Minecraft und Loader | Exakte Versionen aus dem aktuellen Profil oder Export |
| Worldgen-Mods | Dateinamen, Versionen und Abhängigkeiten von Terralith, Tectonic, Biomes O' Plenty und Dungeons & Taverns |
| Lithostitched | Passende veröffentlichte Version für genau diese Umgebung |
| Java und Buildwerkzeuge | Anforderungen des gewählten Loaders und reproduzierbar festgeschriebene Versionen |
| Weltparameter | Weltpreset, Dimension, relevante Worldgen-Konfiguration und vorhandene Datapacks |
| Clientdarstellung | Tatsächlich verwendete Sichtweite, Grafikmods, LOD-Mods und Shader separat erfassen |
| Testrechner | CPU, RAM, JVM-Speichergrenze und Datenträger für vergleichbare Laufzeitmessungen |

Ergebnis ist ein später anzulegender Umgebungsnachweis mit Modliste, relevanten Konfigurationen und SHA-256-Prüfsummen. Zugangsdaten, Kontoinformationen und persönliche Spielstände gehören nicht hinein. Vollständige fremde Mod-JARs werden nicht ins Repository übernommen.

Zunächst wird genau eine Kombination aus Minecraft-Version und Loader unterstützt. Weitere Versionen oder Loader werden erst nach der ersten funktionierenden Veröffentlichung geplant.

## 3. Architektur und Entscheidungspunkte

### 3.1 Vorgesehene Aufteilung

| Ebene | Verantwortung |
| --- | --- |
| Modverpackung | Metadaten, Abhängigkeiten, Ressourcen und gegebenenfalls minimaler Loader-Code |
| Strukturvorlagen | Blockformen, Innenräume, Anschlusspunkte und feste Varianten |
| Worldgen-Daten | Biome-Zuordnung, Strukturverbünde, Auswahl, Verteilung und Prozessoren |
| Lithostitched | Zuerst zu prüfende Grundlage für zusätzliche Platzierungsbedingungen und Strukturzusammensetzung |
| Eigener Code bei nachgewiesenem Bedarf | Fehlende Standortprüfungen, Konfigurationsanbindung oder geeignete Diagnosemöglichkeiten |
| Entwicklungswerkzeuge | Export, Prüfung der Ressourcen und reproduzierbare Testabläufe |

Die aktuelle Lithostitched-Dokumentation beschreibt unter anderem Rasterprüfungen, Biome- und Höhenbedingungen. Sie belegt damit mögliche Bausteine für die Standortwahl. Sie belegt noch keine vollständige Prüfung unserer konkreten Bauwerksgrundflächen. [Quelle: Placement Conditions](https://github.com/Apollounknowndev/lithostitched/wiki/Placement-Conditions).

Die Dokumentation beschreibt außerdem einen erweiterten Jigsaw-Strukturtyp und einen delegierenden Strukturtyp für zusätzliche Bedingungen. Ob und wie sie für unsere Zielversion und zusammenhängenden Kolossbauteile geeignet sind, wird am Prototyp geprüft. [Quelle: Structure Types](https://github.com/Apollounknowndev/lithostitched/wiki/Structure-Types).

Dokumentationsprüfung: 13.09.2026. Vor Umsetzung sind die tatsächlich verwendete Bibliotheksversion und deren Datenformate maßgeblich. Wiki-Beispiele werden nicht ungeprüft als fertige Projektdateien übernommen.

### 3.2 Technischer Durchstich vor Architekturausbau

Der erste Versuch beantwortet vier konkrete Fragen:

1. Lassen sich unsere Ressourcen in der gewählten Umgebung laden und als installierbare Mod paketieren?
2. Entsteht der Obelisk natürlich an passenden Standorten?
3. Lässt sich die grobe Kolossform vollständig über Chunk-Grenzen platzieren?
4. Können ungeeignete Standorte verworfen werden, ohne zusätzliche Generierungsschleifen oder lange Stillstände auszulösen?

Ein bestandener Obelisk-Test ersetzt den Koloss-Test nicht. Erst danach wird entschieden, ob die datenbasierte Architektur genügt. Falls eine Funktion fehlt, dokumentieren wir Anforderung, gescheiterten Versuch, kleinsten erforderlichen Codeumfang und dessen Prüfaufwand.

### 3.3 Client und Server

Die Generierung muss auf dem integrierten Server und auf einem dedizierten Server funktionieren. Die minimal benötigten Client-Abhängigkeiten werden durch einen Verbindungstest bestimmt und anschließend dokumentiert. Die Verwendung von Vanilla-Blöcken allein ist noch kein Nachweis, dass jede Modkomponente ausschließlich serverseitig installiert werden kann.

## 4. Bauwerke als wartbare Quelldaten

### 4.1 Vorgeschlagene Projektablage

Nach Festlegung des Loaders soll das Repository folgende logische Bereiche erhalten. Dies ist eine Planung, die Ordner existieren noch nicht:

| Bereich | Inhalt |
| --- | --- |
| `docs/` | Umgebungsnachweis, technische Entscheidungen, Bauanleitung und Abnahmeprotokolle |
| `design/` | Eigene Blockpaletten, Ansichten und Maßstabsstudien |
| `structures-src/` | Bearbeitbare Exporte eigener Bauwerke und zugehörige Beschreibungsdateien |
| `src/main/resources/` | Paketierbare Struktur- und Worldgen-Ressourcen im Format der Zielversion |
| `src/main/java/` | Nur tatsächlich benötigter Programmcode |
| `tools/` | Reproduzierbare Export- und Validierungsskripte |
| `test-fixtures/` | Kleine Prüfvorlagen, Seeds und definierte Erkundungsrouten |

Registrypfade und Strukturverzeichnisse unterhalb der Ressourcen werden erst anhand der Zielversion festgelegt. Lokale Testwelten und Laufzeitdaten bleiben außerhalb der versionierten Quellen. Referenzvideos dienen der Sichtung und werden nicht mit der Mod ausgeliefert.

### 4.2 Bau- und Exportablauf

Für die Alpha wurde der Bauprozess auf automatische Erzeugung umgestellt: `tools/relic_assets.py` erstellt Geometrie und NBT-Vorlagen, `tools/render_preview.py` liefert Vorschauen. Änderungen erfolgen zunächst am Generator und werden erneut geprüft. Die unten beschriebene Kreativ-Bauwelt bleibt eine optionale Möglichkeit zur gestalterischen Nacharbeit; Handbau ist keine Voraussetzung für den Alpha-Build.

1. Eine getrennte Kreativ-Bauwelt für die Zielversion anlegen.
2. Ein Bau- und Exportwerkzeug auswählen und dessen Version dokumentieren. Die erste Entscheidung erfolgt durch einen kleinen Export-und-Import-Versuch.
3. Pro Relikt eine grobe Form ohne Oberflächendetails bauen. Ansichten mit Spielerfigur sowie Breite, Höhe und Tiefe festhalten.
4. Ursprung, Ausrichtung, Bodenniveau, Eingänge und zusammengehörige Teile markieren.
5. In einer sauberen Testwelt reimportieren. Blockzustände, Abmessungen und Luftbereiche vergleichen.
6. Große Bauwerke nur soweit aufteilen, wie Export und Platzierung es benötigen. Übergänge mit einer einfachen Testpalette sichtbar machen.
7. Aus geprüften Quellen die auszuliefernden Ressourcen erzeugen. Exportwerkzeug, Quellrevision und Dateiprüfsummen dokumentieren.

Bearbeitbare Exporte sind die maßgebliche Quelle. Änderungen an generierten Ressourcen müssen entweder erneut aus dieser Quelle erzeugt oder ausdrücklich zurückgeführt werden. Ein erneuter Export derselben Quelle soll inhaltlich dasselbe Bauwerk erzeugen; etwaige wechselnde Metadaten werden erkannt und normalisiert.

### 4.3 Beschreibungsdaten pro Bauwerk

Vorläufiger Namespace-Vorschlag: `relics`. Vor dem ersten Spielstand mit der Mod auf Namenskonflikte prüfen und festlegen.

| Angabe | Zweck |
| --- | --- |
| Relikt-ID und Varianten-ID | Dauerhafte Zuordnung zwischen Bauwerk, Worldgen und Prüfbericht |
| Quellen und Exportversion | Nachvollziehbare Änderungen und reproduzierbare Exporte |
| Abmessungen und Ursprung | Platzierung ohne versehentliche Versätze |
| Pflichtteile und optionale Teile | Erkennen unvollständiger Strukturverbünde |
| Anschlüsse und Transformationen | Definierte Position und Drehung jedes Teils |
| Kontaktflächen zum Boden | Füße, Rumpfbasis oder Fundament gezielt prüfen |
| Freizuhaltende Räume | Eingänge, Sichtöffnungen und begehbare Innenräume schützen |
| Gesamte Prüfgrundfläche | Auch Arm, Geröll und lokale Einbettung berücksichtigen |
| Zulässige Palette | Unbeabsichtigte Abhängigkeiten und falsche Blockzustände finden |

### 4.4 Luft, Gelände und empfindliche Blöcke

Für jede Vorlage unterscheiden wir Bereiche, in denen vorhandenes Gelände bleiben darf, und Bereiche, die bewusst ausgeräumt werden müssen. Ein großer rechteckiger Export darf nicht unabsichtlich einen rechteckigen Hohlraum in den Hügel schneiden. Die konkrete Behandlung von Luft und ausgelassenen Blöcken wird mit dem gewählten Format getestet.

Nach Platzierung und Neuladen werden Wasser, fallende Blöcke, Blätter, Ranken und wassergefüllte Blockzustände geprüft. Baublöcke mit laufenden Updates oder Block-Entities werden nur dort verwendet, wo sie einen sichtbaren Zweck erfüllen. Ganze Welten dienen nicht als alleinige Sicherung der Bauwerke.

## 5. Prototypen und gestalterische Verträge

Die folgenden Größen sind erste Bauversuche. Sie sind keine Zusage, dass die gewählte Strukturtechnik diese Abmessungen bereits unterstützt. Reihenfolge der Maße: Breite × Höhe × Tiefe, in Blöcken.

| ID-Vorschlag | Erster Bauversuch | Muss im Prototyp sichtbar sein | Noch nicht nötig |
| --- | --- | --- | --- |
| `relics:obelisk` | Schaft etwa 7 × 64 × 7; lokale Basis bis etwa 25 × 25 Grundfläche | Schlanke, oben flache Silhouette; kontrollierter Bodenkontakt; freier Blick auf mindestens eine breite Seite | Mehrere Paletten, Beute, Effekte |
| `relics:colossus` | Sichtbarer Körper etwa 80 × 64 × 64; Verbund mit Arm zunächst höchstens etwa 128 × 96 Grundfläche | Erkennbarer Kopf und Rumpf; teilweise begrabener Körper; abgetrennter Arm; ein zugänglicher Innenraum | Mehrere Posen, vollständige Maschinenausstattung, eigenständige Siedlung |

Die Testformen werden aus mehreren Entfernungen in einer flachen Bauwelt und im Zielterrain beurteilt. Scheitert eine Form am Maßstab oder an der Platzierung, werden Größe, Pose oder Aufteilung angepasst, bevor Details entstehen.

Für den Koloss beginnt die Arbeit mit einer festen Pose und einer festen relativen Armposition. Pflichtteile erhalten keine zufällige Auswahl, die sie versehentlich entfallen lassen kann. Eine zweite Pose ist ein eigener Entwurf mit eigener Prüfung.

## 6. Standortwahl und Generierung

### 6.1 Reproduzierbarer Ablauf

Der folgende Ablauf ist ein fachliches Modell. Die konkrete Reihenfolge der Engine-Aufrufe wird anhand der Zielversion umgesetzt:

1. Aus Weltseed und Verteilungsregeln einen Kandidaten bestimmen.
2. Relikttyp, vorbereitete Variante und Ausrichtung reproduzierbar wählen.
3. Daraus die vollständige Prüfgrundfläche und alle kritischen Kontaktpunkte ableiten.
4. Biome, Geländehöhen, Wasserbedingungen, verfügbare Bauhöhe und relevante Abstände prüfen.
5. Kandidaten bei Verletzung einer Pflichtbedingung verwerfen.
6. Pflichtteile als zusammenhängenden Verbund platzieren und die definierte lokale Einbettung anwenden.
7. Optionale Details mit derselben reproduzierbaren Zufallsgrundlage ergänzen.

Die Prüfung muss zur tatsächlich gewählten Variante und Drehung passen. Eine akzeptierte schmale Grundfläche darf nicht nachträglich durch eine ungeprüfte breite Pose ersetzt werden.

Zulässige Drehungen sind anfangs die vier horizontalen Vierteldrehungen. Spiegelungen werden erst nach eigener Prüfung aktiviert. Für Zufallsauswahl werden weder Uhrzeit noch globale, von der Erkundungsreihenfolge abhängige Zufallszustände verwendet.

### 6.2 Geländeregeln

| Bedingung | Obelisk | Koloss |
| --- | --- | --- |
| Umgebung | Trockene, offene Wüsten- oder geeignete Badlands-Flächen | Offene Graslandschaften und breite, mäßig bewegte Hügel |
| Kontakt zum Boden | Fundament darf teilweise versanden; keine frei schwebende Basis | Rumpfbasis und Armkontakt werden getrennt geprüft |
| Höhenunterschiede | Kleine Basis erlaubt einen enger begrenzten Bodeneingriff | Gesamte Pose muss zu den Höhen über der großen Grundfläche passen |
| Wasser | Kein ungewollt überfluteter Sockel | Kein gefluteter Eingang; keine zufällig im Fluss liegenden Pflichtteile |
| Bauhöhe | Oberkante mit Reserve unter der Dimensionsgrenze | Höchster Teil und tiefste Einbettung innerhalb der Weltgrenzen |
| Eingänge | Äußerer Erkundungsbereich bleibt erreichbar | Mindestens ein vorgesehener Zugang bleibt offen |

Ein Biome-Tag allein belegt weder Trockenheit noch freie Sicht. Höhenabfragen, Biomeprüfungen und Prüfungen tatsächlicher Oberflächenbedingungen sind unterschiedliche Aufgaben. Die verfügbaren Prüfungen werden an Grenzfällen bewertet.

Rasterprüfungen werden um gezielte Punkte an Eingängen, Fundamenträndern und Armauflagen ergänzt, soweit die gewählte Technik dies erlaubt. Ein grobes Raster gilt nicht als Garantie, kleine Wasserläufe oder Geländekanten vollständig zu erkennen.

Abfragen dürfen keine unkontrollierte Erzeugung benachbarter Chunks oder zyklische Abhängigkeiten auslösen. Wenn eine gewünschte Bedingung in der richtigen Generierungsphase nicht verfügbar ist, wird die Anforderung oder Umsetzung ausdrücklich angepasst.

### 6.3 Einbettung und Überlagerungen

Die lokale Einbettung gehört zum Entwurf: Sand an der Basis, Erde über dem Unterkörper, Geröll an Bruchkanten und Bewuchs an geschützten Flächen. Ihr räumlicher Umfang wird pro Vorlage begrenzt. Eine großflächige Planierung, um jede Pose passend zu machen, ist nicht vorgesehen.

Abstände zwischen unseren Relikten und Überlagerungen mit fremden Strukturen werden getrennt behandelt. Eine mögliche Ausschlussregel zwischen Strukturgruppen ist nicht automatisch eine genaue Kollisionsprüfung ihrer Baukörper. Die verwendete Methode und bekannte Grenzen werden dokumentiert.

## 7. Häufigkeit und Konfiguration

Als Bedienkonzept sind das Ein- und Ausschalten einzelner Relikttypen sowie drei Dichteprofile vorgesehen: selten, normal und häufig. Die Profile erhalten erst nach Erkundungstests konkrete Verteilungswerte. Sie garantieren keine feste Zahl von Funden, weil ungeeignete Standorte verworfen werden.

Die technische Anbindung wird im Durchstich entschieden: datenbasierte Varianten beziehungsweise Overrides oder eine kleine Konfigurationskomponente. Es wird kein Laufzeitmenü versprochen, bevor dessen Anbindung an die Worldgen-Daten geklärt ist.

| Verhalten | Geplante Regel |
| --- | --- |
| Wirksamkeit | Einstellungen vor Weltstart beziehungsweise Serverstart laden; Änderungen betreffen künftige Generierung |
| Bestehende Relikte | Bleiben bei späterer Deaktivierung erhalten |
| Bestehende Welten | Keine Nachgenerierung in bereits erzeugten Chunks |
| Fehlerhafte Werte | Verständliche Fehlermeldung; Grenzen und Rückfallverhalten dokumentieren |
| Diagnose | Effektiv verwendetes Profil und aktivierte Relikte protokollieren |
| Mehrspieler | Servereinstellung bestimmt die Generierung |

Dichteversuche zählen Kandidaten, Ablehnungen und tatsächliche Platzierungen. Geplant sind Ablehnungsgründe wie unpassendes Biom, Wasser, zu große Höhendifferenz, Bauhöhe und Abstand. Falls die Bibliothek diese Daten nicht bereitstellt, wird zunächst ein Entwicklungswerkzeug oder eine begrenzte Diagnoseergänzung geprüft. Die Auswertung ist ein Arbeitspaket, keine bereits vorhandene Fähigkeit.

## 8. Phasen mit überprüfbarem Ergebnis

| Phase | Arbeit | Fertig, wenn … |
| --- | --- | --- |
| P0: Zielumgebung | Export auswerten, Versionen festhalten, Testinstanz und Ausgangsmessung vorbereiten | Die dokumentierte Umgebung auf einem frischen Teststand startet |
| P1: Projekt und Export | Modgerüst, Minimalressource, kleiner Export-und-Import-Versuch | Build erzeugt ein ladbares Artefakt; Vorlage übersteht den Import vollständig |
| P2: Obelisk | Grobform bauen, natürlich generieren, Basis und Standort prüfen | Mehrere natürliche Exemplare ohne manuelle Korrektur stehen |
| P3: Koloss-Risiko | Grobform samt Arm zusammensetzen; Drehungen, Chunk-Grenzen und Gelände prüfen | Verbund bleibt vollständig; Eingang und Bodenkontakte funktionieren |
| P4: Gestaltung | Oberflächen, Innenraum und lokale Spuren ergänzen | Beide Motive erfüllen die Gestaltungskriterien der Lore-Bibel |
| P5: Verteilung | Dichteprofile, Diagnose und Strukturabstände prüfen | Tatsächliche Fundhäufigkeit und Verwerfungsgründe sind nachvollziehbar |
| P6: Integration | Vollständiges Modpack, dedizierter Server, Speichern und Neuladen, Leistung | Die Abnahmematrix ist mit konkreten Nachweisen ausgefüllt |
| P7: Veröffentlichung | Installation, Abhängigkeiten, Lizenzwahl, Changelog und Artefaktprüfung | Genau das geprüfte Artefakt ist nachvollziehbar ausgeliefert |

Die Koloss-Grobform kann während P2 gestalterisch entstehen. Die technische Platzierung wird spätestens in P3 geprüft und vor seiner Detailgestaltung abgeschlossen. Für P3 gilt: erst Fehlerursache eingrenzen, dann Pose, Maße oder Platzierung ändern. Ein erfolgreicher Obelisk rechtfertigt kein Überspringen dieser Phase.

## 9. Prüfplan für Version 0.1

### 9.1 Ressourcen und Build

- JSON-Syntax und tatsächliches Laden der Daten in der Zielversion prüfen.
- Fehlende Ressourcenreferenzen, falsche Namespaces und unbekannte Blockzustände erkennen.
- NBT-Abmessungen, Pflichtteile, Verbindungspunkte und zulässige Paletten prüfen.
- Aus einem sauberen Checkout bauen und Inhalt des fertigen Artefakts kontrollieren.
- Den dedizierten Server starten und eine Clientverbindung mit der dokumentierten Installation prüfen.

Automatisierte Tests konzentrieren sich auf selbst implementierte Logik und fehleranfällige Datenbeziehungen. Die optische Abnahme erfolgt in Minecraft.

### 9.2 Generierung und Spielbarkeit

Vorgeschlagene feste Test-Seeds: `731204`, `-48291736` und `20260913`. Diese Werte sind noch nicht erprobt. Vor Messbeginn wird für jeden Seed dieselbe begrenzte Erkundungsfläche beziehungsweise Route festgelegt.

| Testfall | Vorgehen | Akzeptanz |
| --- | --- | --- |
| Natürliche Exemplare | Pro Relikttyp mindestens fünf Exemplare insgesamt, verteilt über mindestens drei Seeds, dokumentieren | Keine Pflichtteile fehlen; Einbettung und Zugang funktionieren |
| Zu wenige Funde | Gesamte vereinbarte Fläche prüfen und Kandidatenquote auswerten | Ursache erklärt; Dichte oder Regeln vor neuer Abnahme angepasst |
| Vier Drehungen | Dieselbe Vorlage gezielt in jeder zugelassenen Ausrichtung platzieren | Anschlüsse, Armposition und Zugänge bleiben korrekt |
| Chunk-Grenzen | Mehrteilige Bauwerke entlang kritischer Übergänge prüfen | Keine abgeschnittenen oder verschobenen Teile |
| Erkundungsreihenfolge | Gleichen Seed und Bereich in frischen Welten aus unterschiedlichen Richtungen erzeugen | Strukturentscheidung und Geometrie bleiben innerhalb identischer Version und Konfiguration reproduzierbar |
| Speichern und Neuladen | Teilweise erkundeten Bereich speichern, neu laden und vervollständigen | Keine Lücken, Verdoppelungen oder beschädigten Ressourcenreferenzen |
| Geländekanten | Flachland, Hang, Wassergrenze und Biome-Übergang gezielt abdecken | Gültige Standorte passen; ungültige werden nachvollziehbar verworfen |
| Fremde Strukturen | Nähe zu Dungeons & Taverns und weiteren Strukturen untersuchen | Keine beobachteten schweren Überschneidungen; verbleibende Grenzen dokumentiert |
| Konfiguration | Relikttyp deaktivieren und Profile in jeweils frischen Bereichen prüfen | Effektive Einstellungen stimmen mit beobachteter Generierung überein |
| Erkundung | Ohne Flugmodus die geplanten Wege begehen | Hauptraum des Kolosses ohne Blockabbau oder Spezialausrüstung erreichbar |

Manuelle Platzierungen dienen gezielten Grenztests. Sie werden im Prüfbericht klar von natürlichen Funden getrennt. Der Suchbereich wird nicht stillschweigend so lange vergrößert, bis eine zu geringe Fundrate verborgen bleibt.

### 9.3 Darstellung und Laufzeit

Beide Bauwerke werden ohne Shader sowie mit dem tatsächlich verwendeten Grafikprofil betrachtet. Prüfentfernungen: zunächst 32, 96 und 192 Blöcke, soweit die eingestellte Sichtweite diese Darstellung ermöglicht. Das sind feste Vergleichspositionen, keine garantierte Renderdistanz.

Für Leistungsmessungen dienen zwei getrennte frische Welten je Seed: vollständiges Modpack ohne unsere Erweiterung und dieselbe Umgebung mit ihr. Route, JVM-Parameter und sonstige Einstellungen bleiben gleich. Nach einem Aufwärmdurchlauf sind drei vergleichbare Messpaare vorgesehen.

Erfasst werden Gesamtzeit für die festgelegte Chunkmenge, Chunkzeiten soweit messbar, auffällige Pausen, maximaler Speicherbedarf und Fehlerprotokolle. Für die Darstellung wird zusätzlich dieselbe Kameraansicht am Relikt verglichen. Messinstrumente und eventuelle Grenzen der Zuordnung werden im Bericht genannt.

Konkrete Zeit- und Speicherbudgets werden nach der Ausgangsmessung und vor der Abnahme festgeschrieben. Ohne diese Grenzen gilt die Leistungsprüfung als offen. Abstürze, wiederkehrende Generierungsfehler und reproduzierbar unvollständige Bauwerke verhindern die Freigabe unabhängig vom Durchschnittswert.

## 10. Änderungen und Veröffentlichung

Nach der ersten Veröffentlichung bleiben verwendete Ressourcen-IDs stabil. Änderungen an Verteilung, Vorlagen oder Zufallsauswahl werden als Änderungen für neue Chunks dokumentiert. Gleicher Seed allein garantiert keine identische Welt über verschiedene Modversionen hinweg.

Vor Veröffentlichung sind Projektname und Lizenz zu entscheiden. Eigene Blockbauten und Quellen werden von fremden Referenzmedien getrennt. Ein Release erhält Installationshinweise, genaue Abhängigkeiten, bekannte Einschränkungen, Changelog und eine Prüfsumme des getesteten Artefakts.

Beim späteren Veröffentlichen werden Git-Tag, hochgeladenes Artefakt und heruntergeladene Prüfsumme abgeglichen. Eine angenommene Plattformübertragung gilt erst nach separater Prüfung als öffentlich verfügbar. Dieser Plan löst noch keine Veröffentlichung aus.

## 11. Offene Entscheidungen und nächste Arbeit

| Entscheidung | Zeitpunkt |
| --- | --- |
| Zielversionen und Loader | P0, vor Projektgerüst |
| Bauwerkzeug, Exportformat und Namespace | P1, vor größeren Bauwerken |
| Eignung von Lithostitched und Bedarf an eigenem Code | P2 und P3 |
| Endgültige Prototypmaße und erlaubte Geländetoleranzen | Nach den Grobformen in P2 und P3 |
| Konfigurationsformat und Dichtewerte | P5 |
| Leistungsgrenzen | Nach Ausgangsmessung, vor P6-Abnahme |
| Zweite Varianten | Nach geprüfter Grundform, ohne Verzögerung notwendiger Fehlerkorrekturen |
| Name, Lizenz und Veröffentlichungsziel | Vor P7 |

Die nächste ausführbare Aufgabe ist P0: das tatsächliche Modpack erfassen. Danach folgt ein kleiner Export-und-Import-Versuch mit einer ladbaren Minimalstruktur. Ein detaillierter Koloss beginnt erst, wenn seine grobe Form technisch tragfähig ist.
