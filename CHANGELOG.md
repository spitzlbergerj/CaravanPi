# CaravanPi Change Log

In dieser Datei werde ich alle relevanten Änderungen am CaravanPi dokumentieren

---

## v2.0 Einführung MariaDB, Grafana, neues Backup, Configs per xml (noch in Arbeit - development branch)

- **Konfiguration per xml Datei**
  Bisher wurden für die Konfiguration der CaravnaPi Skripte Testdateien verwendet. Diese enthielten nur die Werte, nicht aber die Felderklärungen. Das machte das Lesen der Konfigurationsdateien praktisch unmöglich. Nun wurden diese Textdateien durch eine xml Datei ersetzt, in der alle Konfigurationen enthalten sind. Die xml Datei ist besser lesbar (Optimierung noch ausstehend, dass die xml datei mit Zeilenumbrüchen geschrieben wird).
  Die Lese und Schreibskripte sind abwärtskompatibel. Werden alte Konfigurationsdateien gefunden, so werden diese in die xml Datei umgewandelt und in einem _alt Verzeichnis gesichert.

- **Backup Skript ersetzt**
  CaravanPi hatte bisher ein eigenes backup Skript. Dieses habe ich durch ein eigenes Repository ersetzt. 
  Fortan wird https://github.com/spitzlbergerj/Raspberry-Pi-Backup-Cloud genutzt.
  Noch offen: Dokumentation der Sicherung der MariaDB

- **Einführung einer Datenbank zur Speicherung der Sensorwerte**
  Die Sensorwerte können nun nicht nur in Files abgelegt werden, sondern auch in einer MariaDB. Die Zugangsdaten zur MariaDB werden in der XML abgelgt. Der Connect und die Schreibvorgänge in die Datenbank übernehmen  zentrale Funktionen in der CaravanPiFiles Class.

- **Einführung des Sendes der Sensorwerte per MQTT**
  Die Sensorwerte können nun per MQTT Messages versandt werden. Im Moment ist die Ansteuerung eines Cloud MQTT Servers vorgesehen, der für den Login User und passwort benötigt und ein Login mit TLS ohne Clientzertifikate erlaubt. Dies sind z.B. die Cloud MQTT Broker von EMQX und HiveMQ, die beide kostenfreie Accounts anbieten. Den Connect und die Sendevorgänge an den Broker übernehmen zentrale Funktionen in der CaravanPiFiles Class.

- **allgemeine Bereinigung und Härtung der vorhandenen Funktionen**
  Alle vorhandenen Skripte zur Ermittlung der Sensorwerte wurden überprüft, optimiert und insbesondere gehärtet, so dass Fehlersituationen in den Skripten abgefangen und behandelt werden, ohne die Funktionen zum Absturz zu bekommen. Das regelmäßige überprüfen der Log-Daten auf Fehlerzustände ist daher wichtiger geworden. Alle Fehlerzustände werden mit einem einleitenden ERROR kenntlicher gemacht.

- **Einführung von Grafana zur Darstellung der Sensorwerte als Verlauf**
   Neben der Datenbank MariaDB und der Datenbank-Managementsoftware phpmyadmin kommt nun Grafana zur grafischen Darstellung der Sensorwerte und deren Verlauf zum Einsatz.

- **Umstellung der CaravanPi Website auf Flask Framework**
   Die CaravanPi Website basiert nun auf dem Python Framework Flask und ist dadurch bei weitem flexibler geworden.
   Über die Website kann die Statusprüfung angestoßen werden, die Konfiguration kann eingetragen werden, Testroutinen können gestarte werden.
   Zudem sind auch Shortcuts für die Grafana Website, phpMyAdmin oder auch den magicMirror enthalten.

- **Der Status des CaravanPi kann nun über eine Statusabfrage geprüft werden**
   Alle wesentlichen Komponenten des Aufbaus werden dabei der Reihe nach geprüft und getestet. Die Konfiguration durch den Nutzer wird dabei berücksichtigt, so dass nur die Teile geprüft werden, die auch verbaut wurden.

- **Überwachung der Landstrom-Versorgung und der Bordbatterie-Versorgung**
   Als ganz neue Features wurden die Überwachung der 230V Landstromversorgung und zweier 12V Batterien (Bordbatterie und Fahrzeugbatterie) hinzugefügt.

- **Gasalarmsensor integriert**
   Zur Überwachung eventueller Propan oder Butan Konzentrationen im Caravan wurde ein MQ-2 Sensor hinzugefügt.

- **Integration der Überwachung einer Liontron Litium Batterie**
   Auch das Batteriemanagement eine LiPo batterie kann nun angesteuert und ausgelesen werden. Beispielhaft LionTron.

- **Installationsskript**
   Ein Installationsskript kann nun die Installation des CaravanPi inkl. Magicmirror, MariaDB, Grafana, myPhpAdmin und aller benötigten Libraies übernehmen.
   Dabei werden alte Konfigurationsdateien migriert. Ein Update sollte also problemfrei möglich sein, ist aber noch nicht endgültig getestet.

- **Ansteuerung von Aktoren wie ESP82 D1 mini oder Shelly integriert**
   Beispielhaft wurde ein D1 mini als Aktor integriert und die Kommunikation von und zum CaravanPi eingebaut

- **Dokumentation der Internet-Verbindung über eine Starlink-Antenne**
   noch nachzuholen.



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
