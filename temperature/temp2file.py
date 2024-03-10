#!/usr/bin/python
# coding=utf-8
# temp2file.py
#
# schreibt die aus den DS1820 gelesenen temperaturwerte ans Ende einer Datei 
# pro Sensor wird eine Datei mit Zeitstemple und Temperaturwert gefüllt
#
#-------------------------------------------------------------------------------

import os
import sys
import argparse


# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles


# Global für vorhandene Temperatursensoren
tempSensorBezeichnung = [] #Liste mit den einzelnen Sensoren-Kennungen
tempSensorAnzahl = 0 #INT für die Anzahl der gelesenen Sensoren
tempSensorWert = [] #Liste mit den einzelnen Sensor-Werten

def ds1820_sensoren_ermitteln():
	global tempSensorBezeichnung, tempSensorAnzahl
	#Verzeichnisinhalt auslesen mit allen vorhandenen Sensorbezeichnungen 28-xxxx
	try:
		for x in os.listdir("/sys/bus/w1/devices"):
			if (x.split("-")[0] == "28") or (x.split("-")[0] == "96"):
				tempSensorBezeichnung.append(x)
				tempSensorAnzahl = tempSensorAnzahl + 1
		return 0
	except:
		# Auslesefehler
		print ("Der Verzeichnisinhalt konnte nicht ausgelesen werden.")
		return -1

def ds1820_werte_auslesen():
	global tempSensorBezeichnung, tempSensorAnzahl, tempSensorWert
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
			
		return 0
	except:
		# Fehler bei Auslesung der Sensoren
		print ("Die Auslesung der DS1820 Sensoren war nicht möglich.")
		return -1


def main():
	# ArgumentParser-Objekt erstellen
	parser = argparse.ArgumentParser(description='Lesen aller Temperatursensoren am 1-Wire-Bus')
	parser.add_argument('-s', '--screen', action='store_true',
						help='Ausgabe auf dem Bildschirm')
	parser.add_argument('-c', '--check', action='store_true', 
						help='Führt den Funktionstest aus')

	# Argumente parsen
	args = parser.parse_args()

	# Anzahl und Bezeichnungen der vorhandenen Temperatursensoren einlesen und auswerten, falls einlesen OK
	if ds1820_sensoren_ermitteln() != 0: 
		# Fehler, keine Sensorwertze vorhanden/lesbar
		return 1
	
	# Lesen der Sensoren erfolgreich
	
	# Temperaturen lesen
	if ds1820_werte_auslesen() != 0: 
		# Fehler, Sensorwerte nicht lesbar
		return 1

	if args.check:
		# nur Check, daher Abschluss hier
		if args.screen:
			print("erfolgreich")
		return 0
	
	cplib = CaravanPiFiles()
	x = 0
	while x < tempSensorAnzahl:
		# Sensorwerte verarbeiten
		# Erstellen einer Instanz der CaravanPi Library
		cplib.handle_sensor_values(
			args.screen,								# Anzeige am Bildschirm?
			"temperatursensor",							# sensor_name = Datenbankname
			f"DS1820-{tempSensorBezeichnung[x]}",		# sensor_id = Filename und Spalte in der Datenbank
			["temperatur"],								# Liste Spaltennamen
			(float(tempSensorWert[x]),)					# Tupel Sensorwerte
		)    
		x = x + 1

	return 0          

if __name__=="__main__":
	result = main()
	sys.exit(result)