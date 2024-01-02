# CaravanPi
System zur Messung und Anzeige verschiedener Werte in Wohnwagen und Reisemobilen, u.a. Klimawerte, Füllstände und Niveaudaten. Magic Mirror wird für die Präsentation verwendet.

# Climate sensors

Ich verwende den Bosch BME280 zur Bestimmung der Temperatur, des Luftdrucks und der Luftfeuchtigkeit. Der Sensor ermittelt diese Daten zuverlässig auf kleinstem Raum. Ich verwende zwei dieser Sensoren. Einer überwacht den Innenraum des Wohnwagens, einer den Außenbereich. Dort habe ich ihn auf dem Dach, allerdings beschattet durch eine Antennenplattform, angebracht.


## I2C Bus Extender
Der von mir verwendete BME280 kann über den I2C-Bus angesprochen werden. Da ich die beiden Sensoren optimal im und am Wohnwagen platzieren möchte (z.B. weit weg von Wärmequellen wie Raspberry oder Kühlschrank), sind I2C Bus Extender notwendig. Als Kabel verwende ich ein Cat6 Kabel.

# BME280 bzw. BME680
Im Verzeichnis beispielskripte finden sich Skripte, die statt dem BME280 den BME680 verwenden, der neben den Werten des BME280 auch noch einen Luftqualitätswert ausgibt.
