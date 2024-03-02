#!/usr/bin/python3
# coding=utf-8
# change_crontab.py
#
# Ändern der Crontab aufgrund von Konfigurationsänderungen
#
# Aufruf-Parameter
# systemStat2file.py -f
# 	-s	display values on screen 
#   -i Intervall   Abfrageintervall in Sekunden default = 300
#
# erzeugt mit Hilfe von ChatGPT 4
#-------------------------------------------------------------------------------

from crontab import CronTab
import time
import sys
import argparse


# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles



def update_crontab(script_dir, script_name, interval, kommentar=None):
	cron = CronTab(user=True)  # Nutzt die Crontab des aktuellen Benutzers

	for job in cron:
		print(f"--- {job.is_enabled()} --- {job.command} --- {job.comment}")

		if script_name in job.command:
			print("... wird gelöscht")
			kommentar=job.comment
			cron.remove(job)  # Entfernt den aktuellen Job, wenn er existiert

	if kommentar is None:
		kommentar=script_name

	if interval:  # Fügt den Job nur hinzu, wenn ein Intervall angegeben ist
		print(" ... wird neu hinzugefügt")
		job = cron.new(command=f'python3 -u /home/pi/CaravanPi/{script_dir}/{script_name}.py  > /home/pi/CaravanPi/.log/{script_name}.log 2>&1', comment=kommentar)
		job.setall(interval)

	print(cron.render())
	#cron.write()
		
	return 0


def main():
	parser = argparse.ArgumentParser(description='Systemstatistiken überwachen')
	parser.add_argument('-j', '--job', type=char,
						help='Job, der geändert werden soll, Skriptname')
	parser.add_argument('-d', '--dir', type=char,
						help='in welchem Verzeichnis ist das Skript')
	parser.add_argument('-c', '--comment', type=char,
						help='Kommentar, der eingefügt werden soll')
	parser.add_argument('-m', '--minutes', type=int,
						help='Anzahl der Minuten zwischen den Ausführungen 1 - 59')
	parser.add_argument('-s', '--screen', action='store_true',
						help='Ausgabe am Bildschirm')

	args = parser.parse_args()
	
	normal_interval = args.interval
	high_temp_interval = 30  # Abfrageintervall bei hoher Temperatur: 30 Sekunden
	interval = normal_interval

	try:
		update_crontab('temperature', 'temp2file.py', '*/59 * * * *')
		  
	except KeyboardInterrupt:
		if args.screen:
			print("\nWARNING - Programm wurde durch Benutzer unterbrochen. Beende...")
		sys.exit(0)

if __name__ == "__main__":
	main()

