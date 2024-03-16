#!/usr/bin/python3
# coding=utf-8
#
# CaravanPiConfigItemWrite 
#
# ./CaravanPiConfigItemWrite.py 'caravanpiDefaults/MariaDBpasswd' 'neuesPasswort'
#
#-------------------------------------------------------------------------------

import sys
import os
from datetime import datetime 
import xml.etree.ElementTree as ET
import argparse  

# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles


def parse_arguments():
	parser = argparse.ArgumentParser(description="Schreibe Konfigurationsitems in die CaravanPi-Konfigurationsdatei.")
	parser.add_argument('--element_path', type=str, help="Der XML-Pfad des Elements, das aktualisiert oder hinzugefügt werden soll.")
	parser.add_argument('--value', type=str, help="Der Wert, der für das Element gesetzt werden soll.")
	return parser.parse_args()

def main():
	args = parse_arguments()

	cplib = CaravanPiFiles()

	# Schreibe die übergebenen Werte in die XML-Datei
	result = cplib.writeCaravanPiConfigItem(args.element_path, args.value)
	if result != 0:
		print(f"Fehler beim Schreiben der Konfiguration für {args.element_path}")
		return -1

	return 0

if __name__=="__main__":
	result = main()
	sys.exit(result)