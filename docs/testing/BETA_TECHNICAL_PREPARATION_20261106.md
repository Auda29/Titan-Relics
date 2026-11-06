# Technische Beta-Vorbereitung vom 6. November 2026

Der unveröffentlichte Kandidat **0.1.0-beta.1** ist lokal für alle vier Ziele
gebaut. Die [JSON-Evidenz](BETA_TECHNICAL_PREPARATION_20261106.json) bindet
Dateinamen, SHA-256, Quellrevision und Prüfstatus. Das ist keine öffentliche
Beta-Freigabe und keine neue vollständige Survival-/Client-Abnahme.

## Fertiggestellt

- Anzeigename Titan Relics in Fabric-/NeoForge-Metadaten und Release-Titeln;
  `relics`-IDs, Spielregeln und gespeicherte Weltpläne bleiben erhalten.
- Generierte Strukturressourcen aus den vorhandenen, hashgeprüften Modellquellen
  wiederhergestellt. Alle vier Builds bestehen Metadaten-/Assetprüfungen und
  enthalten die kanonische MIT-Lizenz und aktuellen Credits.
- Modrinth per API mit Beschreibung, MIT, Kategorien, Quell-/Wiki-/Issue-Links
  und [zugeschriebenem CC-BY-Start-Icon](../../assets/branding/README.md)
  konfiguriert. Rückvergleich bestätigt weiterhin `draft` und null Versionen.
- Uploadwerkzeug und separater manueller Workflow vorbereitet. Standard ist
  ein lesender Plan. Freigabemarker, vollständige Paketprüfung, feste Projekt-IDs,
  persistente Uploadbelege und Download-Prüfsummen verhindern versehentliche
  Veröffentlichung beziehungsweise stille Doppeluploads.
- Echten lesenden Upload-Plan mit allen vier tatsächlichen JARs gegen beide
  Plattformen ausgeführt. Die gepinnten Modrinth-Abhängigkeiten und benötigten
  CurseForge-Namen sind auflösbar. Es wurde keine Datei hochgeladen.

## Prüfungen und behobener CI-Fehler

Alle **185 Python-Tests** bestanden. Die zwölf Upload-/Projektkonfigurationstests
und elf bestehenden Release-Grenztests bestanden zusätzlich gezielt nach den
abschließenden Helper-Änderungen. `actionlint` 1.7.12 akzeptiert alle drei
Workflows. Die Java-Prüfungen bestanden mit 677 Gameplay-Assertions,
65 statischen Mixin-Zielverträgen und 764 Worldgen-Assertions. Die Verteilungs-
und Einstellungsprüfungen bestanden ebenfalls; synthetische Terrain-Seeds
werden dadurch nicht als neuer natürlicher Survival-Test ausgegeben.

Die früheren CI-Läufe scheiterten im Testhelfer `GameplayMixinTargets`, weil
dieser ausschließlich `@Mixin(value=...)` auslas. Zwei vorhandene Mixins
benennen ihr Ziel über `targets`. Der Helfer unterstützt jetzt beide ausdrücklich
angegebenen Formen und prüft weiter genau ein Ziel. Keine Produktions-Mixins
wurden für diesen Testfehler abgeschaltet oder verändert.

Ein isolierter echter Fabric-26.2-Server bestand zwei Boots einschließlich
Rezeptpaketen, Kern/Magnet, Begegnungs-/Belohnungszuständen, Baumaura,
Tierpopulation und unverändertem Weltplan nach Änderung der Installationsvorgabe.
Die genaue getestete JAR-Prüfsumme steht im JSON. Es wurden keine Nutzerprofile
oder vorhandenen Spielwelten bearbeitet.

Lokale Downloads hatten vorübergehende DNS-Fehler. Für NeoForge 1.21.1 musste
zusätzlich zu JDK 25 ein JDK 21 als Minecraft-Werkzeugkette installiert werden.
Danach bestanden beide NeoForge-Builds. Die Toolchains liegen unter ignoriertem
`build/toolchains/`; sie sind keine zusätzlichen Spielerabhängigkeiten.

## Testpakete

Die Dateien liegen lokal unter `dist/release/` mit `SHA256SUMS.txt`. Passend zum
Spielprofil genau ein JAR auswählen. Sie sind keine bereits veröffentlichten
Modrinth-/CurseForge-Downloads. Der Survival-Test soll den tatsächlich ausgewählten
Kandidaten und dessen Spiel-/Loaderziel festhalten.

## Verbleibende Grenzen

Die vorhandene GitHub-OAuth-Anmeldung hat keine `workflow`-Berechtigung. GitHub
hat deshalb den Push der neuen `.github/workflows/publish-platforms.yml`
zurückgewiesen. Die Datei ist lokal erhalten und geprüft; die übrigen Änderungen
sind separat gepusht. Für ihre Aktivierung ist eine zusätzliche berechtigte
GitHub-Anmeldung erforderlich. Es wurde nicht versucht, die Beschränkung zu umgehen.

Die dokumentierte CurseForge-Autoren-API kann Dateien und Versionsmetadaten,
aber nicht die allgemeine Projektseite bearbeiten. Beschreibung, MIT, Credits,
Links und Icon müssen dort im Autorendashboard abgeglichen werden. Die fertigen
[Seitenangaben](../releases/CURSEFORGE_DRAFT.md) und die 400×400-PNG liegen bereit.

Offen bleiben die Nutzer-Survival-Abnahme, die ausdrückliche Veröffentlichung,
Plattformzulässigkeit und Moderation. Keine neuen Client-Screenshots oder
vollständigen Modpack-Langzeitprüfungen werden behauptet. Der zusätzliche
Main-Branch-CI-Lauf ist vom lokalen Nachweis getrennt und kann noch laufen.
