#!/usr/bin/python
# coding=utf-8
# temp2file.py
#
# schreibt die aus den DS1820 gelesenen temperaturwerte ans Ende einer Datei 
# pro Sensor wird eine Datei mit Zeitstemple und Temperaturwert gefüllt
#
#-------------------------------------------------------------------------------

import os, sys, time, datetime

# Global für vorhandene Temperatursensoren
tempSensorBezeichnung = [] #Liste mit den einzelnen Sensoren-Kennungen
tempSensorAnzahl = 0 #INT für die Anzahl der gelesenen Sensoren
tempSensorWert = [] #Liste mit den einzelnen Sensor-Werten

def ds1820einlesen():
    global tempSensorBezeichnung, tempSensorAnzahl, programmStatus
    #Verzeichnisinhalt auslesen mit allen vorhandenen Sensorbezeichnungen 28-xxxx
    try:
        for x in os.listdir("/sys/bus/w1/devices"):
            if (x.split("-")[0] == "28") or (x.split("-")[0] == "10"):
                tempSensorBezeichnung.append(x)
                tempSensorAnzahl = tempSensorAnzahl + 1
        return 0
    except:
        # Auslesefehler
        print ("Der Verzeichnisinhalt konnte nicht ausgelesen werden.")
        return -1

def ds1820auslesen():
    global tempSensorBezeichnung, tempSensorAnzahl, tempSensorWert, programmStatus
    x = 0
    try:
        # 1-wire Slave Dateien gem. der ermittelten Anzahl auslesen 
        while x < tempSensorAnzahl:
            dateiName = "/sys/bus/w1/devices/" + tempSensorBezeichnung[x] + "/w1_slave"
            file = open(dateiName)
            filecontent = file.read()
            file.close()
            # Temperaturwerte auslesen und konvertieren
            stringvalue = filecontent.split("\n")[1].split(" ")[9]
            sensorwert = float(stringvalue[2:]) / 1000
            temperatur = "{:.2f}".format(sensorwert) #Sensor- bzw. Temperaturwert auf 2 Dezimalstellen formatiert
            tempSensorWert.insert(x,temperatur) #Wert in Liste aktualisieren
            x = x + 1
    except:
        # Fehler bei Auslesung der Sensoren
        print ("Die Auslesung der DS1820 Sensoren war nicht möglich.")
        programmStatus = 0

def write2file(sensor, wert):
	try:
		dateiName = "/home/pi/CaravanPi/values/" + sensor
		file = open(dateiName, 'a')
		str_from_time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		file.write("\n"+ sensor + " " + str_from_time_now + " " + wert)
		file.close()
		return 0
	except:
		# Schreibfehler
		print ("Die Datei konnte nicht geschrieben werden.")
		return -1




# Anzahl und Bezeichnungen der vorhandenen Temperatursensoren einlesen und auswerten, falls einlesen OK
if ds1820einlesen() == 0: 
	# Temperaturausgabe in Schleife
	x = 0
	ds1820auslesen()
	while x < tempSensorAnzahl:
		write2file(tempSensorBezeichnung[x],tempSensorWert[x])
		x = x + 1
