# Modkompatibilität und Leistung

Stand 4. November 2026; geprüft am lokalen Beta-Kandidaten auf Basis von
Alpha 5.0.5. Das ist keine Aussage über bereits installierte oder veröffentlichte
JARs. Vollständiges Verfahren und Messwerte: [Prüfbericht](../testing/BETA_COMPATIBILITY_20261104.md).

## Geprüfte Kombinationen

| Umgebung | Geprüfte Versionen / Umfang |
|---|---|
| Einfaches Referenzsetup | Fabric und NeoForge, Minecraft 1.21.1 und 26.2 |
| TerraVista, Fabric 26.2 | BOP 26.2.0.0.28; Tectonic 3.0.28; Terralith 2.6.4; Dungeons & Taverns 5.3.2; Lithostitched 1.8.0+beta6 |
| TerraVista-Grafik | Voxy 0.2.19-beta; Voxy World Gen V2 2.4.3; Iris 1.11.2; Sodium 0.9.1; BSL 10.1.5 |
| Living World, Fabric 1.21.1 | BOP 21.1.0.14; Tectonic 3.0.28; Terralith 2.6.2; Dungeons & Taverns 1-v4.4.4; Lithostitched 1.8.0 |
| Living-World-Grafik | DH 3.3.3; Iris 1.8.8; Sodium 0.6.13; BSL 10.1.8; Serene Seasons 10.1.0.9; SSDH 1.0.3+terravista.dh3.1 |

Die konkreten Modlisten und Hashes stehen in der [Evidenz](../testing/beta-compatibility-20261104.json).
Gemeinsame Terrain-, Biom- und Strukturerzeugung bestand in zwei Testseeds je
Modpack. Die Grafikvarianten liefen jeweils begrenzt; daraus folgt keine
Garantie für alle Versionen, Seeds oder Modpack-Einstellungen.

## Distant Horizons

Bei DH 3.3.3 kann der Modus `FEATURES` den geplanten Reliktstart auslassen.
Dadurch kann ein Relikt erst nach dem normalen Annähern erscheinen. Der Fehler
wurde vor dem ersten Besuch mit einem echten DH-Generatorauftrag reproduziert.

Für neu berechnete entfernte Bereiche ist `INTERNAL_SERVER` der erfolgreich
geprüfte Weg. Die zugehörige DH-Konfiguration lautet:

```toml
chunkGeneratorMode = "INTERNAL_SERVER"
```

Die Bezeichnung bzw. Position im Menü kann je nach DH-Version abweichen.
Regulär erzeugte Relikt-Chunks wurden anschließend im tatsächlichen DH-LOD
aus 400 Blöcken Entfernung dargestellt, ohne normales Laden des Zielchunks.
Ein Moduswechsel ist kein geprüfter Reparaturweg für bereits gespeicherte
unvollständige LOD-Daten. Nutzer-Caches nicht ohne gesonderte Diagnose löschen.

## Voxy, Shader und Jahreszeiten

Voxy mit und ohne BSL sowie Living World mit und ohne Shader und Saisonbrücke
bestanden die dokumentierten Clientprüfungen. Serene Seasons wurde auch im
Winter mit anschließender Prozessneustart-/Weltladeprüfung untersucht.
Der frühere Nutzerbefund einer Verbesserung ohne Saisonadapter bleibt eine
versions- und setupspezifische Beobachtung. Eine generelle Unverträglichkeit
von Serene Seasons und Relic ist damit nicht belegt.

Die Voxy-Ferngenerierung war in den Tests auf acht Chunks Radius und zwei
Aufgaben begrenzt. Eine Freigabe für sehr große Radien oder viele parallele
Aufgaben ist daraus nicht abzuleiten. DH-Ferngenerierung wurde getrennt von
den kurzen Grafikvergleichen untersucht.

`Voxy World Gen V2 2.4.3` ist in diesem Modpack nicht als Dedicated-Server-Mod
geeignet: Sein LWJGL-Zugriff scheitert dort auch ohne Relic. Das Addon wurde
deshalb ausschließlich in den Serverreferenzen weggelassen. Ein funktionierendes
Client-Modpack ist nicht automatisch ein vollständiges Server-Modpaket.

## Speicher und Bestandswelten

Relic erhöht in den Messungen den Prozessspeicher deutlich. Mit vier GiB
Java-Heap erreichte Living World bis zu 4,16 GiB Prozessspeicher. Heap und
gesamter Prozessspeicher sind verschiedene Werte; Reserven für Betriebssystem,
Grafik und andere Programme bleiben nötig. Die Messungen begründen weder
eine allgemeine RAM-Mindestanforderung noch eine langfristige Speicherleckfreiheit.

Ein bestehender Reliktplan bleibt eingefroren. Änderungen an Biomen,
Datenpaketen oder der Modliste können dessen gespeicherte Umgebung verändern;
die verständliche Weltladeprüfung ist keine automatische Migration.
Vor Änderungen an einer bestehenden Spielwelt eine Sicherung anlegen und
bei einer Ablehnung das ursprüngliche Setup wiederherstellen.

Ungeprüft bleiben insbesondere andere Modpack-/Adapterversionen, NeoForge-
Varianten dieser Fabric-Modpacks, umfangreiche Langzeit-/FPS-Lasten und das
automatische Nachbessern alter LOD-Caches.
