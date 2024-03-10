#!/usr/bin/python3
# coding=utf-8
# clean_MariaDB
#
# löschen aller alten Einträge in der MariaDB
#
# Aufruf-Parameter
# systemStat2file.py -f
# 	-s	display values on screen 
#   -t Tage   wie viele Tage sollen erhalten bleiben
#
# erzeugt mit Hilfe von ChatGPT 4
#-------------------------------------------------------------------------------

import sys
from datetime import datetime, timedelta
import argparse


# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles




def main():
	parser = argparse.ArgumentParser(description='MariaDB bereinigen')
	parser.add_argument('-d', '--days', type=int, default=365,
						help='Anzahl der Tage, die erhalten bleiben sollen')
	parser.add_argument('-s', '--screen', action='store_true',
						help='Ausgabe am Bildschirm')

	args = parser.parse_args()

	# Erstellen der Instanzen der Librarys
	cplib = CaravanPiFiles()

	
	# Verbindungsdaten für Ihre MariaDB
	MariaDBhost = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/MariaDBhost"), "str")
	MariaDBuser = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/MariaDBuser"), "str")
	MariaDBpasswd = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/MariaDBpasswd"), "str")
	MariaDBdatabase = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/MariaDBdatabase"), "str")

	# Datenbank oeffnen
	connection = cplib.create_db_connection()

	try:
		with connection.cursor() as cursor:
			# Tabellennamen abrufen
			cursor.execute("SHOW TABLES")
			tables = cursor.fetchall()

			# Für jede Tabelle die alten Daten löschen
			for table in tables:
				delete_query = f"DELETE FROM {table[0]} WHERE zeitstempel < NOW() - INTERVAL {args.days} DAY"
				print(delete_query)
				cplib.execute_query(connection, delete_query, None)
		
		# Änderungen in der Datenbank speichern
		connection.commit()

	finally:
		connection.close() 

if __name__ == "__main__":
	main()

