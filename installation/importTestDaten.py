#!/usr/bin/python
# coding=utf-8
# importTestDaten.py
#
# importiert Testdaten in die mariadb aus einem Set an Daten. 
# Dabei gibt der Benutzer einen zeitpunkt an, ab dem die Daten dann importiert werden.
#
#-------------------------------------------------------------------------------

import os
import sys
import argparse
from datetime import datetime, timedelta
# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles

sensor_mapping = {
	"temperatursensor": {
		"spaltennamen": ["temperatur"],
		"daten_zuordnung": [0],  # Angabe, dass der dritte Wert in der Zeile der Temperatur entspricht
		"datentypen": ["float"],  # Angabe des Datentyps für jede Spalte
		"wertebereiche": {
			"temperatur": (-50, 50)  # Gültige Werte liegen zwischen -50 und 50 Grad Celsius
		}
	},
	"klimasensor": {
		"spaltennamen": ["temperatur", "luftdruck", "luftfeuchtigkeit"],
		"daten_zuordnung": [0, 1, 2],  # Angabe, welcher Wert der Zeile welcher Spalte entspricht
		"datentypen": ["float", "float", "float"],  # Angabe des Datentyps für jede Spalte
		"wertebereiche": {
			"temperatur": (-50, 50),
			"luftdruck": (800, 1200),  # Gültige Werte liegen zwischen 800 und 1200 hPa
			"luftfeuchtigkeit": (0, 100)  # Gültige Werte liegen zwischen 0% und 100%
		}
	},
	"gasfuellgrad": {
		"spaltennamen": ["gewicht", "fuellgrad"],
		"daten_zuordnung": [0, 1],
		"datentypen": ["float", "float"],  # Angabe des Datentyps für jede Spalte
		"wertebereiche": {
			"gewicht": (0, 8000),  # Annahme: gültige Werte in irgendeiner Einheit
			"fuellgrad": (0, 100)  # Annahme: Alarm ist ein boolescher Wert
		}
	},
	"ausrichtung": {
		"spaltennamen": ["x-achse", "y-achse", "z-achse"],
		"daten_zuordnung": [0, 1, 2],
		"datentypen": ["float"],  # Angabe des Datentyps für jede Spalte
		"wertebereiche": {
			"x-achse": (-180, 180),
			"y-achse": (-180, 180),
			"z-achse": (-180, 180)
		}
	}
}

def ist_gueltiger_tabellenname(tabellenname):
	"""Überprüft, ob der gegebene Tabellenname gültig ist."""
	return tabellenname in sensor_mapping

def get_user_input(prompt):
	"""Fragt den Benutzer interaktiv nach Eingaben, basierend auf einem vorgegebenen Hinweis."""
	return input(prompt)

def parse_arguments():
	"""Verwendet argparse, um Kommandozeilenargumente zu verarbeiten."""
	parser = argparse.ArgumentParser(description="Lädt Testdaten in eine MariaDB-Datenbank.")
	parser.add_argument("-s", "--startdatum", help="Startdatum im Format YYYYMMDD", required=False)
	parser.add_argument("-d", "--dateiname", help="Pfad und Dateiname der Testdaten", required=False)
	parser.add_argument("-t", "--tabellenname", help="Name der Datenbanktabelle", required=False)

	args = parser.parse_args()
	return args

def convert_timestamp(original_timestamp, user_start_date):
	# Format des originalen Zeitstempels und des Startdatums des Benutzers
	original_format = "%Y%m%d%H%M%S"
	user_date_format = "%Y%m%d"
	
	# Konvertierung des originalen Zeitstempels und des Startdatums in datetime-Objekte
	original_datetime = datetime.strptime(original_timestamp, original_format)
	user_start_datetime = datetime.strptime(user_start_date, user_date_format)
	
	# Berechnung des Unterschieds in Tagen zwischen dem ursprünglichen Datum und dem Startdatum des Benutzers
	base_date = datetime(2022, 1, 1)  # Basisdatum, 20220101
	days_difference = (user_start_datetime - base_date).days
	
	# Erzeugung des neuen Datums durch Hinzufügen der Tagesdifferenz zum ursprünglichen Datum
	new_date = original_datetime + timedelta(days=days_difference)
	
	# Rückgabe des neuen Zeitstempels im gleichen Format
	return new_date.strftime(original_format)

def verarbeite_datei(dateiname, startdatum, tabellenname):
	cplib = CaravanPiFiles()

	# Datenbankverbindung erstellen
	connection = cplib.create_db_connection()
	
	with open(dateiname, "r") as file:

		zaehler = 0

		for zeile in file:
			# zum Testen nur 10 Zeilen lesen
			if zaehler > 3:
				break

			# Für test nächste zeile aktivieren
			# zaehler += 1

			werte = zeile.strip().split()
			if not werte:
				continue  # Überspringen leerer Zeilen

			# print(f"Werte: {werte}")

			sensor_id, timestamp, *datenwerte = werte
			neuer_timestamp = convert_timestamp(timestamp, startdatum)

			# print(f"Datenwerte: {datenwerte} neuer Zeitstempel: {neuer_timestamp}")

			# Validierung der Datenwerte gemäß der Konfiguration in sensor_mapping
			spaltennamen = sensor_mapping[tabellenname]["spaltennamen"]
			daten_zuordnung = sensor_mapping[tabellenname]["daten_zuordnung"]
			datentypen = sensor_mapping[tabellenname]["datentypen"]  
			wertebereiche = sensor_mapping[tabellenname].get("wertebereiche", {})

			# Anpassung für den direkten Schreibvorgang
			table_columns = ['sensor_id', 'zeitstempel'] + spaltennamen
			table_values = [sensor_id, neuer_timestamp]

			for index, spalte, datentyp in zip(daten_zuordnung, spaltennamen, datentypen):

				# print (f"Index: {index}, Spalte: {spalte}, Typ: {datentyp}")

				roh_wert = datenwerte[index]  

				# print (f"Roh: {roh_wert}")

				try:
					if datentyp == "float":
						wert = float(roh_wert)
					elif datentyp == "int":
						wert = int(roh_wert)
					else:
						wert = roh_wert  # Standardfall für String o.ä.
				except ValueError:
					print(f"Konvertierungsfehler für {spalte} in Zeile: {zeile.strip()}")
					break

				if spalte in wertebereiche:
					min_wert, max_wert = wertebereiche[spalte]
					if not (min_wert <= wert <= max_wert):
						print(f"Ungültiger Wert für {spalte} in Zeile: {zeile.strip()}")
						break

				table_values.append(wert)

			else:
				try:
					# Daten in die Tabelle schreiben
					print(f"gelesene Werte Datei: {werte} ")
					print(f"zeitstempel Datei: {timestamp} neuer Zeitstempel: {neuer_timestamp}")
					print(f"Schreibe Werte für {tabellenname} in die DB: {table_columns}, {tuple(table_values)}")
					cplib.insert_into_table(connection, tabellenname, table_columns, tuple(table_values))
				except Exception as e:
					print(f"Fehler beim Schreiben in die Datenbank: {e}")


	# Datenbank schließen
	connection.close()


def main():
	args = parse_arguments()

	# Überprüfen, ob die Argumente vorhanden sind, ansonsten den Benutzer fragen
	startdatum = args.startdatum if args.startdatum else get_user_input("Bitte geben Sie das Startdatum im Format YYYYMMDD an: ")
	dateiname = args.dateiname if args.dateiname else get_user_input("Bitte geben Sie den Pfad und Dateinamen an: ")
	tabellenname = args.tabellenname if args.tabellenname else get_user_input("Bitte geben Sie den Tabellennamen an: ")

	# Überprüfung auf Gültigkeit des Tabellennamens
	while not ist_gueltiger_tabellenname(tabellenname):
		print(f"Der Tabellenname '{tabellenname}' ist ungültig. Gültige Namen sind: {', '.join(sensor_mapping.keys())}.")
		tabellenname = get_user_input("Bitte geben Sie einen gültigen Tabellennamen an: ")

	# Überprüfen, ob die Datei existiert
	if not os.path.isfile(dateiname):
		print(f"Die Datei '{dateiname}' existiert nicht.")
		return

	# Überprüfen, ob das Startdatum gültig ist
	try:
		datetime.strptime(startdatum, "%Y%m%d")
	except ValueError:
		print("Das Startdatum hat ein ungültiges Format. Bitte verwenden Sie das Format YYYYMMDD.")
		return

	print(f"Startdatum: {startdatum}, Dateiname: {dateiname}, Tabellenname: {tabellenname}")

	# Aufruf der Funktion zur Verarbeitung der Datei
	verarbeite_datei(dateiname, startdatum, tabellenname)
	
if __name__ == "__main__":
	main()