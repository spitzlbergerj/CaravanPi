#! /usr/bin/python3
# coding=utf-8
#-------------------------------------------------------------------------------

import sys
# Importieren der angepassten CaravanPiFiles Klasse
from CaravanPiFilesClass import CaravanPiFiles

def main():
    # Erstellen einer Instanz der Klasse
    cp_files = CaravanPiFiles()

    # Lesen der Konfigurationen und Ausgabe der Ergebnisse
    print("CaravanPiDefaults:", cp_files.readCaravanPiDefaults())
    print("Adjustment:", cp_files.readAdjustment())
    print("Dimensions:", cp_files.readDimensions())
    print("Voltage Levels:", cp_files.readVoltageLevels())
    print("Test Color:", cp_files.readTestColor())

if __name__ == "__main__":
    main()
