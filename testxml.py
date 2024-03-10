#! /usr/bin/python3
# coding=utf-8
#-------------------------------------------------------------------------------

import sys
# Importieren der angepassten CaravanPiFiles Klasse
from CaravanPiFilesClass import CaravanPiFiles

def main():
	# Erstellen einer Instanz der Klasse
	cplib = CaravanPiFiles()

	# Lesen der Konfigurationen und Ausgabe der Ergebnisse
	print("CaravanPiDefaults:", cplib.readCaravanPiDefaults())
	print("Adjustment:", cplib.readAdjustment())
	print("Dimensions:", cplib.readDimensions())
	print("Voltage Levels:", cplib.readVoltageLevels())
	print("Test Color:", cplib.readTestColor())

	print("write2file mit readItem:", cplib.readCaravanPiConfigItem("caravanpiDefaults/write2MariaDB"), "true" if cplib.readCaravanPiConfigItem("caravanpiDefaults/write2MariaDB") else "false")

if __name__ == "__main__":
	main()
