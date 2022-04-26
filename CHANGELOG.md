# CaravanPi Change Log

deutsch | english
----- | -----
In dieser Datei werde ich alle relevanten Änderungen am CaravanPi dokumentieren | All notable changes to this project will be documented in this file.

---

## V 1.1 - Fehlerkorrekturen und Erweiterungen (noch in Arbeit)

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
