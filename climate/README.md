# CaravanPi
System zur Messung und Anzeige verschiedener Werte in Wohnwagen und Reisemobilen, u.a. Klimawerte, Füllstände und Niveaudaten. Magic Mirror wird für die Präsentation verwendet.

# Python Skripte

## climate2file.py
python3 /home/pi/CaravanPi/climate/climate2file.py [-h] [-i {76,77}] [-f] [-s] [-c]

Lesen des Klimasensors und Verarbeiten der Sensorwerte

optional arguments:
    -h, --help                  show this help message and exit
    -i {76,77}, --i2c {76,77}   I2C Bus Adresse (76 (default) oder 77)
    -f, --file                  schreiben in ein File - obsoloet durch globale xml Konfiguration
    -s, --screen                ausgeben am Bildschirm
    -c, --check                 führt nur einen Funktionscheck des Sensors aus



# Climate sensors

Ich verwende den Bosch BME280 zur Bestimmung der Temperatur, des Luftdrucks und der Luftfeuchtigkeit. Der Sensor ermittelt diese Daten zuverlässig auf kleinstem Raum. Ich verwende zwei dieser Sensoren. Einer überwacht den Innenraum des Wohnwagens, einer den Außenbereich. Dort habe ich ihn auf dem Dach, allerdings beschattet durch eine Antennenplattform, angebracht.


## I2C Bus Extender
Der von mir verwendete BME280 kann über den I2C-Bus angesprochen werden. Da ich die beiden Sensoren optimal im und am Wohnwagen platzieren möchte (z.B. weit weg von Wärmequellen wie Raspberry oder Kühlschrank), sind I2C Bus Extender notwendig. Als Kabel verwende ich ein Cat6 Kabel.

# BME280 bzw. BME680
Im Verzeichnis beispielskripte finden sich Skripte, die statt dem BME280 den BME680 verwenden, der neben den Werten des BME280 auch noch einen Luftqualitätswert ausgibt.
