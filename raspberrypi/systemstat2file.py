#!/usr/bin/python3
# coding=utf-8
# systemStat2file.py
#
# zyklische Abfrage einiger Systemwerte
# Intervall 5 Minuten (oder laut Parameter)
# Bei CPU Temperaturen über 75°C wird das Intervall auf 30 Sekunden verkürzt
#
# Aufruf-Parameter
# systemStat2file.py -f
# 	-h	display guide 
# 	-f	write values to file 
# 	-s	display values on screen 
#   -i Intervall   Abfrageintervall in Sekunden default = 300
#
# erzeugt mit Hilfe von ChatGPT 4
#-------------------------------------------------------------------------------

import os
import time
import sys
import argparse
import psutil
import subprocess


# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles


def get_cpu_temperature():
	# CPU-Temperatur lesen (Raspberry Pi spezifisch)
	try:
		temp = psutil.sensors_temperatures().get('cpu_thermal', [])[0].current
		return temp
	except Exception as e:
		print(f"Fehler beim Auslesen der CPU-Temperatur: {e}")
		return None

def get_gpu_temperature():
	try:
		gpu_temp_output = subprocess.check_output(['/usr/bin/vcgencmd', 'measure_temp']).decode()
		gpu_temp = float(gpu_temp_output.split('=')[1].split("'")[0])
		return gpu_temp
	except Exception as e:
		print(f"Fehler beim Auslesen der GPU-Temperatur: {e}")
		return None

def get_cpu_usage():
	try:
		return psutil.cpu_percent(interval=1)
	except Exception as e:
		print(f"Fehler beim Auslesen der CPU-Auslastung: {e}")
		return None

def get_ram_usage():
	try:
		return psutil.virtual_memory().percent
	except Exception as e:
		print(f"Fehler beim Auslesen der RAM-Auslastung: {e}")
		return None

def get_disk_usage():
	try:
		return psutil.disk_usage('/').percent
	except Exception as e:
		print(f"Fehler beim Auslesen der Festplatten-Auslastung: {e}")
		return None
	
def get_network_traffic(interface='eth0'):
	try:
		net_io = psutil.net_io_counters(pernic=True)
		traffic = net_io.get(interface, None)
		if traffic:
			return traffic.bytes_recv / (1024 ** 2)
		else:
			return 0
	except Exception as e:
		print(f"Fehler beim Auslesen des Netzwerkverkehrs: {e}")
		return None
	
def get_process_count():
	try:
		return len(psutil.pids())
	except Exception as e:
		print(f"Fehler beim Auslesen der Prozessanzahl: {e}")
		return None
	
def get_system_uptime():
	try:
		return time.time() - psutil.boot_time()
	except Exception as e:
		print(f"Fehler beim Auslesen der System-Uptime: {e}")
		return None
		
def main():
	parser = argparse.ArgumentParser(description='Systemstatistiken überwachen')
	parser.add_argument('-i', '--interval', type=int, default=300,
						help='Intervall in Sekunden für regelmäßige Abfragen (Standard: 300 Sekunden)')
	parser.add_argument('-f', '--file', action='store_true',
						help='Ausgabe in ein File - obsoloet durch globale xml Konfiguration')
	parser.add_argument('-s', '--screen', action='store_true',
						help='Ausgabe am Bildschirm')

	args = parser.parse_args()
	
	normal_interval = args.interval
	high_temp_interval = 30  # Abfrageintervall bei hoher Temperatur: 30 Sekunden
	interval = normal_interval

	try:
		while True:
			cpu_temp = get_cpu_temperature()
			gpu_temp = get_gpu_temperature()
			cpu_usage = get_cpu_usage()
			ram_usage = get_ram_usage()
			disk_usage = get_disk_usage()
			net_traffic = get_network_traffic()
			process_count = get_process_count()
			system_uptime = get_system_uptime()

			# Erstellen einer Instanz der CaravanPi Library
			cplib = CaravanPiFiles()
			cplib.handle_sensor_values(
				args.screen,        # Anzeige am Bildschirm?
				"raspberrypi",      # sensor_name = Datenbankname 
				"raspberrypi",      # sensor_id = Filename und Spalte in der Datenbank
				["cpu_temp", "gpu_temp", "cpu_usage", "ram_usage", "disk_usage", "net_traffic", "process_count"], # Liste Spaltennamen
				(cpu_temp, gpu_temp, cpu_usage, ram_usage, disk_usage, net_traffic, process_count) # Tupel Sensorwerte
			)

			# Anpassung des Intervalls basierend auf der CPU-Temperatur
			if cpu_temp > 75 and interval != high_temp_interval:
				interval = high_temp_interval
			elif cpu_temp <= 75 and interval != normal_interval:
				interval = normal_interval

			time.sleep(interval)
	except KeyboardInterrupt:
		if args.screen:
			print("\nProgramm wurde durch Benutzer unterbrochen. Beende...")
		sys.exit(0)

if __name__ == "__main__":
	main()
