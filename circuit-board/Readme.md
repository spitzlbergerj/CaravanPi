# Platinen Fertigung
In diesem Directory finden Sie alle Dateien, um eine Platine bei einem Dienstleister bestellen und fertigen lassen zu können.

# Versionen
Die CaravanPi Platine existiert inzwischen in mehreren Versionen

Version | Beschreibung
-----------|----
Version 1 | allererste Versuche, nicht für eine Auftragsproduktion geeignet
Version 2 | erste Version, die ich bei einem Dienstleister habe produzieren lassen <br/> enthält jedoch einen Fehler. Die Verdrahtung des VCC des Radar-Sensors war fälschlicherweise 3,3 V anstatt 5V
Version 3 | korrigierte Version, die ich erstmals bei JLCPCB inkl. SMD Bestückung habe fertigen lassen
Version 4 | Umstellung aller IC auf SMD

# Fertigung bei JLCPCB

Bei JLCPCB.com können Platinen sehr günstig, in hoher Qualität und inkl. SMD Bestückung online bestellt werden. Den Bestellprozess habe ich ausführlich beschrieben. Alle benötigten Dateien sind in den jeweiligen Unterverzeichnissen der Versionen enthalten.

Achtung, manchmal sind nicht alle Bauteile bei JLCPCB vorrätig. Dies betrifft insbesondere die ICs MCP23017 und P82B715P. Wer auch selbst SMD löten beherrscht kann dennoch bestellen. Ansonsten lohnt meist das warten von einer Woche. Dann sind die Teile meist wieder vorrätig.

Der Versand aus China dauert etwa 10 - 15 Tage.

Bei der Einfuhr nach Deutschland werden Zollgebührenn fällig. Für 5 Platinen inkl. SMD Bestückung der Version 3 ohne MCP23017 habe ich im Juni 2021 22 EUR Zoll bezahlt.

# Abmessungen

Platine Abmessungen
![CaravanPiPlatine](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/CaravanPi_V3_Maße.png)  

# 3D Druck Bauteile für die CaravanPi Platine

Ich habe zwei Halterungen zur Montage der Platine in einem größeren Gehäuse konsturiert, so dass die Platine quasi mit doppelseitigem Klebeband montiert werden kann. Eine Halterung enthält Möglichkeiten zur Kabelführung

