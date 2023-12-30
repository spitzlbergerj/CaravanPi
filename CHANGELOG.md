# CaravanPi Change Log

deutsch | english
----- | -----
In dieser Datei werde ich alle relevanten Änderungen am CaravanPi dokumentieren | All notable changes to this project will be documented in this file.

---

## v2.0 Einführung MariaDB, Grafana, neues Backup, Configs per xml (noch in Arbeit)

- **Konfiguration per xml Datei**
  Bisher wurden für die Konfiguration der CaravnaPi Skripte Testdateien verwendet. Diese enthielten nur die Werte, nicht aber die Felderklärungen. Das machte das Lesen der Konfigurationsdateien praktisch unmöglich. Nun wurden diese Textdateien durch eine xml Datei ersetzt, in der alle Konfigurationen enthalten sind. Die xml Datei ist besser lesbar (Optimierung noch ausstehend, dass die xml datei mit Zeilenumbrüchen geschrieben wird).
  Die Lese und Schreibskripte sind abwärtskompatibel. Werden alte Konfigurationsdateien gefunden, so werden diese in die xml Datei umgewandelt und in einem _alt Verzeichnis gesichert.

- **Backup Skript ersetzt**
  CaravanPi hatte bisher ein eigenes backup Skript. Dieses habe ich durch ein eigenes Repository ersetzt. 
  Fortan wird https://github.com/spitzlbergerj/Raspberry-Pi-Backup-Cloud genutzt.
  Noch offen: Dokumentation der Sicherung der MariaDB

- **Einführung einer Datenbank zur Speicherung der Sensorwerte**

- **Einführung von Grafana zur Darstellung der Sensorwerte als Verlauf**

- **Überwachung der Landstrom-Versorgung und der Bordbatterie-Versorgung**

- **Integration der Überwachung einer Liontron Litium Batterie**

- **Dokumentation der Internet-Verbindung über eine Starlink-Antenne**


## V 1.1 - Fehlerkorrekturen und Erweiterungen

### Hinzugefügt (Added)

- **mehrere Gasflaschen-Waagen**
  Es können nun mehrere Gasflaschen Waagen angesteuert werden. Dabei sind über die Software grundsätzlich beinahe beliebig 
  viele Waagen möglich (Beschränkung über die freien GPIO Ports). Allerdings sieht die Konfigurationswebsite derzeit nur die 
  Konfiguration von zwei Waagen vor. Über die direkte Bearbeitung der Konfigurationsdateien über einen Editor können jedoch sehr 
  einfach weitere Waagen angesteuert werden. Die CaravanPi Platinen V3 und V4 haben beim eingelöteten Breakout Board nur den 
  Channel A des HX711 an die randliegenden Klemmen geführt. Der Channel B ist jedoch leicht erreichbar und kann zusätzlich 
  verlötet werden. Die Platine V5 wird die Kontakte des Channel B auf Klemmen führen.
  - Skripte in .lib schreiben defaults mit angehängter Flaschennummer
  - defaults für Gasflaschenwaagen enthalten nun GPIO Pin Nummern zur Ansteuerung HX711 sowie die Kanalbezeichnung A oder B und die sog. Reference Unit
  - tactileSwitches.py wurde erweitert, so dass kurzer Druck Flasche 1 kalibriert, langer Druck Flasche 2
  - html Python und PHP Skripte entsprechend angepasst
  - Skritpte teilweise umbenannt

- **logrotate - Aufnahme Spannungsaufzeichnungen**
  die Datei values/voltage wird nun ebenfalls durchrotiert

### Aktualisiert (Updated)

### Korrigiert (Fixed)
- **Kalibrierung Gasflaschen-Waagen**
  Die Kallibrierung des Waagensensors HX711 war falsch programmiert. Statt einer tatsächlcihen Kalibrierung wurde lediglich das Tara 
  angepasst. Dies führte jedoch zu falschen Werten. Die Kalibrierung wurden nun vollständig neu programmiert.



## V 1.0 - Erstes Release vor der "ersten Ausfahrt"

### Hinzugefügt (Added)

- **Grundfunktionalitäten**
