# CaravanPi
System zur Messung und Anzeige verschiedener Werte in Wohnwagen und Reisemobilen, u.a. Klimawerte, Füllstände und Niveaudaten. Magic Mirror wird für die Präsentation verwendet.

# Konfigurationswerte

Eine ganze Reihe von Sensoren muss vor dem Einsatz justiert werden. Es ist zum Beispiel fast unmöglich, den 3-Achsen-Positionssensor im Bezug zum Caravan absolut waagerecht zu montieren. Die Kompensationswerte werden in einer xml Datei in diesem Verzeichnis gespeichert. Außerdem werden in dieser xml Werte wie das Leergewicht der Gasflasche gespeichert, die Abmessungen des Wohnwagens und eine ganze Reihe von Konfigurationswerten für den CaravanPi an sich.


## allgemeine Konfiguration - caravanpiDefaults

countGasScales
  Anzahl Gasflaschenwaagen

countTanks
  Anzahl Tanks

write2file
  sind die Wertze Dateien im Verzeichnis values zu schreiben? 0 = nein, 1 = ja

write2MariaDB
  sollen die Werte in die Datenbank geschriebenwerden? 0 = nein, 1 = ja

send2MQTT
  sollen die Werte per MQTT versandt werden? 0 = nein, 1 = ja

MariaDBhost
MariaDBuser
MariaDBpasswd
MariaDBdatabase
  Anmeldeinformationen für die Datenbank

MQTTbroker
MQTTport
MQTTuser
MQTTpassword
  Anmeldeinformationenfür den MQTT Broker


## Abmessungen des Wohnwagens oder Wohnmobils 

- length over all
  - length of the caravan over all 
- width
  - width of the caravan over all
- lenght body
  - legth of the body of the caravan without drawbar
  
## Gaswaage und Gasflasche (gasScaleDefaults1)

- tare
  - value from gas scale without a gas cylinder 
- empty weight
  - weight of the empty gas cylinder
- full weight
  - weight of the full gas cylinder

## Bedeutung einger Konfigurationswerte

- adjustX
  - X-Wert, wenn der Wohnwagen in horizontaler Position steht
- adjustY
  - Y-Wert, wenn der Wohnwagen in horizontaler Position steht
- adjustZ
  - Z-Wert, wenn der Wohnwagen in horizontaler Position steht
- toleranceX
  - Abweichung in X-Richtung, die noch als horizontal angesehen wird 
- toleranceY
  - Abweichung in Y-Richtung, die noch als horizontal gilt
- approximationX
  - bei welcher Abweichung von der Horizontalen sollen die LEDs blinken
- approximation Y
  - bei welcher Abweichung von der Horizontalen die LEDs blinken sollen
- distRight
  - Abstand des Sensors von der rechten Seite
- distFront
  - Abstand des Sensors von der Frontseite
- distAxis
  - Abstand des Sensors von der Achse in Längsrichtung


