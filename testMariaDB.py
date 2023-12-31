#! /usr/bin/python3
# coding=utf-8
#-------------------------------------------------------------------------------

import sys
# Importieren der angepassten CaravanPiFiles Klasse
from CaravanPiFilesClass import CaravanPiFiles

def main():
    # Erstellen einer Instanz der Klasse
    cp_files = CaravanPiFiles()

    # MariaDB verbinden und Ausgabe der Ergebnisse
    cp_files.climateWrite("4711", "0815", 23, 68, 34)



if __name__ == "__main__":
    main()
