# Beta: echte Client- und Netzwerkprüfung

Nachtrag vom 4. November: Die späteren [Gameplay-](BETA_CLIENT_GAMEPLAY_ACCEPTANCE_20261104.md)
und [Rendererprüfungen](BETA_RENDERER_ACCEPTANCE_20261104.md) schließen Punkt 4
für den lokalen Kandidaten ab. Dieser Bericht bewahrt den damaligen Teilstand.

Stand der ersten Prüfrunde: 4. November 2026. **Teilabnahme, Punkt 4 damals offen.** Keine Veröffentlichung. Grundlage ist Commit `57d0b5625bec618a8152705003b4c351988e8708` mit den bereits vorhandenen Discovery-Änderungen des Root-Agenten.

Auf Fabric und NeoForge, jeweils Minecraft 1.21.1 und 26.2, wurden aktuelle Spieler-JARs gebaut und echte grafische Java-Clients automatisiert gestartet. Die Testfenster blieben versteckt. Die geprüften Welt- und Turmaufnahmen stammen aus Minecraft Screenshot.grab und wurden mit view_image angesehen.

Die [strukturierte Evidenz](beta-client-acceptance-20261104.json) enthält vollständige SHA256, Prozess-IDs, Start-/Endzeiten, Beitrittszeilen, Szenarien, Pfade und Loghashes. Testhelfer, Probe-JARs, Welten, Argumentdateien und vollständige Logs liegen unter `build/beta-client-acceptance-20261104/`. Diese lokalen Build-Belege müssen für eine spätere Reproduktion erhalten bleiben.

## Bestandene Fälle

- Neue Welt über CreateWorldScreen, Seed 731204, ohne `config/relics-distribution.json`. Der neue Weltdraft und die tatsächlich eingefrorenen Journal-Einstellungen entsprechen vollständig `DistributionSettings.DISCOVERY`. Die Probe schreibt keine Installationsvorgaben.
- Vollständiges Beenden des ersten Spielprozesses, erneuter Java-Prozess mit derselben gespeicherten Welt, erfolgreicher Weltstart und weiterhin DISCOVERY im Journal. Das belegt das Laden der Einstellungen; eine Belohnungs- oder Inventarpersistenzprüfung ist damit nicht verbunden.
- Ein grafischer Hostclient mit integriertem Server und ein separater grafischer Gastclient sind gleichzeitig verbunden. Der Testlistener bindet ausschließlich an `127.0.0.1`. Hostzähler erreicht zwei Spieler; Serverlogs nennen die TCP-Verbindungen.
- Der Gast beendet seinen gesamten Prozess und verbindet sich aus einem weiteren neuen Clientprozess erneut. Beide Gastverbindungen erhalten dieselbe Offline-UUID `b2c6551d-8ddf-3bc0-84e1-962967c209f5`; der Host hat UUID `00000000-0000-0000-0000-000000000001`. Alle zwölf Netzwerkprozesse enden mit Exitcode 0.
- Der Gast kommt nach dem Hoststart hinzu. Das ist ausschließlich ein später Verbindungsbeitritt, kein Test der Belohnungsberechtigung nach Beginn oder Ende eines Reliktereignisses.

Es wurden keine simulierten ServerPlayer als echte Clients gezählt. Der Host benutzt die normale lokale Spielerverbindung; der Gast verbindet sich über echtes Loopback-TCP. Das ist keine Dedicated-Server-Abnahme.

## Prozesse und Laufzeiten

| Ziel | Host-PID | Gast-PIDs, Erstbeitritt / Wiederbeitritt | Hostlaufzeit |
|---|---:|---|---:|
| fabric 1.21.1 | 27928 | 4968 / 26456 | 207.45 s |
| fabric 26.2 | 35304 | 36140 / 36496 | 207.55 s |
| neoforge 1.21.1 | 35524 | 33468 / 33060 | 208.57 s |
| neoforge 26.2 | 12456 | 35060 / 36600 | 212.08 s |

Die Verbindung blieb jeweils ungefähr 20 Sekunden pro Gastbeitritt bestehen. Zwischen den Gastprozessen liegt zusätzlich eine Pause von 15 Sekunden und die neue Clientstartzeit. Die Hostprobe umfasst 3600 Clientticks nach Öffnen des Listeners. Diese rund dreieinhalb Minuten sind ausdrücklich keine längere Gameplay-Sitzung.

## Renderer und Testarena

Der Operator-Test platziert `relics:ruined_tower_gameplay_v10` bei `0 -50 0`, lädt die benötigten Chunks und teleportiert den Zuschauer zur Kamera `55 100 -65`. Das ist eine künstliche Testarena über beziehungsweise im Meer, keine natürliche Strukturplatzierung und keine Survival-Reise. Die Aufnahmen zeigen Turmsegmente, Steintexturen und Treppen auf allen vier Zielen ohne sichtbare fehlende Texturen in diesem Ausschnitt. Die Turmspitze ist abgeschnitten. Innenräume, Gesamtmodell, andere Reliktfamilien und die 1.21.1-Adaptionen Farn/Kupfertruhe sind dadurch nicht abgenommen.

- [fabric 1.21.1](images/beta-client-20261104-fabric-1.21.1.png)
- [fabric 26.2](images/beta-client-20261104-fabric-26.2.png)
- [neoforge 1.21.1](images/beta-client-20261104-neoforge-1.21.1.png)
- [neoforge 26.2](images/beta-client-20261104-neoforge-26.2.png)

Die ersten Arena-Versuche waren ungültig: Das Log meldete `Diese Position ist nicht geladen`, und die Aufnahme zeigte Himmel. Nach dauerhaftem Laden der Chunks, verzögerter Platzierung und Anpassung der Kamera wurden die vier oben verlinkten Aufnahmen erstellt. Frühe `arena-proof.txt`-Marker sind allein kein Platzierungsnachweis. Ausschlaggebend sind die abschließenden Logmeldungen zur geladenen Vorlage und die angesehenen Bilder.

## Noch auszuführen

- Tatsächliches Crafting inklusive Ergebnisentnahme und Zutatenverbrauch für Template-Duplizierung, Maschinenkern-Aufladung, Magnetreparatur und Schmiedevorlage. Geladene Rezeptzahlen sind kein Crafting-Nachweis.
- Vollständige Reliktinteraktionen mit persönlichen Belohnungen, physischen Drops und Schlüsselverbrauch. Es wurden keine Belohnungen direkt vergeben.
- Zwei Spieler während desselben Reliktereignisses, getrennte persönliche Ansprüche, Wiederbeitritt mit bereits erhaltenen Belohnungen und späte Ankunft nach Ereignisfortschritt.
- Inventar-, Schlüssel- und Belohnungszustand nach Save/Reload und vollständigem Neustart.
- Längere gemeinsame Gameplay-Sitzung; die kurzen Verbindungsproben ersetzen sie nicht.
- Vollständige grafische Bedienungs-/Modellprüfung aller Familien und sichtbare Prüfung der spezifischen 1.21.1-Ersatzblöcke.

Für diese offenen Fälle liegt weder ein Bestehen noch ein belegter Produktfehler vor. Der hier erstellte automatisierte Ablauf steuert Weltanlage, Neustart, Verbindung und eine Turmkamera. Er führt die noch fehlenden Crafting- und Reliktinteraktionen nicht aus. Eine vollständige Abnahme wäre daher unbelegt. Die natürliche Survival-Reise aus Punkt 3 bleibt beim Nutzer; Punkte 5/6 wurden nicht bearbeitet.

## Vorherige Weltladebelege

Die [Weltladeabnahme](BETA_WORLD_LOAD_GUARD_20261104.md) und ihre [Evidenz](beta-world-load-guard-20261104.json) belegen bereits auf allen vier Zielen Menü-Rückkehr, Lockfreigabe, Schreibfreiheit bei Ablehnung, Wiederherstellung und Abbruch nach erfolgreicher Vorprüfung. Diese Fälle bleiben als bestandene vorherige Tests ausgewiesen. Sie wurden hier nicht nochmals vollständig mit den neuen Discovery-JARs gefahren und werden nicht auf neue SHA256 umetikettiert.

## Artefakte

- `relics-0.1.0-alpha.5.0.5+mc1.21.1.jar`
  SHA256 `a10c4e665798568064ffb8eb37a25c8ded86d193ae5e4e3d785c3091243b9c16`
- `relics-0.1.0-alpha.5.0.5+mc26.2.jar`
  SHA256 `9ce11af173ebfd5e2db2ad85a38133c1b1bcc7832154a4dee0c5ee1df01a6508`
- `relics-0.1.0-alpha.5.0.5+mc1.21.1-neoforge.jar`
  SHA256 `86bb9380a3ed80d9bd2a15d51d1e444f2faba3a0aa53832acce52defce5cf50d`
- `relics-0.1.0-alpha.5.0.5+mc26.2-neoforge.jar`
  SHA256 `bfd259fe5369e3ad42a00550e11f20f44459b5a748a317d29d8f359233dee486`

Die bei den Netzwerkfällen geladenen Mod-JARs wurden gegen diese Hashes verglichen. Fabric 26.2 wurde mit `tools/build.py --skip-generation` gebaut; die drei Ports mit `tools/build_alpha5_port.py`. Java 21 stammt aus `C:/Program Files/Java/jdk-21.0.10`; Java 25 aus `C:/Users/wecke/.gradle/jdks/eclipse_adoptium-25-amd64-windows.2`. Die 1.21.1-Preparation und die Fabric-Probekompilierung liefen nacheinander.

## Einschränkungen und Erhaltung

Die Logs enthalten erwartbare Authentifizierungs-/Realmsfehler durch das isolierte Offlinetoken 0. Frühe Fixtures erbten `simulationDistance:2`, das Vanilla ablehnt; die letzten Arena-Fixtures verwenden 5. Beim erzwungenen Laden vieler Chunks erscheinen Überlastungswarnungen. Daraus wird keine Performancefreigabe abgeleitet. Fehler und Loglevel wurden nicht gefiltert; NeoForge 26.2 verwendet den vorhandenen Loggeradapter.

Keine Produktionsdatei wurde von diesem Testauftrag verändert. Neu sind dieser Bericht, die JSON-Evidenz und vier PNGs unter `docs/testing/images/`; alle Hilfsprogramme und Testszenarien liegen unter `build/`. Keine Commits, Pushes, Tags, Releases, PRs oder weiteren Agenten. Es laufen keine Testclients dieses Auftrags mehr.

Alle 38 anfangs erfassten geänderten/ungetrackten Dateien sind SHA256-gleich geblieben. Auch die sieben Referenzhashes aus `build/alpha5-0-5-release-20261103/preservation.json` stimmen überein. Insbesondere wurden die vier Root-Änderungen, die Roadmap, fremde Alpha-4.9-Dateien und die fremden Auditwerkzeuge nicht verändert. Nutzerprofile und vorhandene Welten wurden weder gestartet noch bearbeitet.
