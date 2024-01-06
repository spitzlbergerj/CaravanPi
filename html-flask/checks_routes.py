#
#
#

import os
import glob
import sys
import subprocess
import requests
import importlib.util
import smbus2

from flask import render_template
from time import sleep

# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles


# Globale Variable zur Speicherung der Ergebnisse
check_list = [
    {'name': 'Raspberry Pi', 'key': 'check_raspberrypi', 'run_check': True},
    {'name': 'MagicMirror', 'key': 'check_magicmirror', 'run_check': True},
    {'name': 'MariaDB', 'key': 'check_mariadb', 'run_check': True},
    {'name': 'Grafana', 'key': 'check_grafana', 'run_check': True},
    {'name': 'Apache Webserver', 'key': 'check_apache', 'run_check': True},
    {'name': '1-Wire Bus', 'key': 'check_1_wire', 'run_check': True},
    {'name': 'I2C Bus', 'key': 'check_i2c', 'run_check': True},
    {'name': 'Wägezelle HX711', 'key': 'check_hx711', 'run_check': True},
]

# Initialisiere check_results automatisch basierend auf check_list
check_results = {check['key']: {'result': None, 'color': None} for check in check_list}

# Globale Variable mit den erwarteten I2C Bus Geräten
i2c_bus_number = 1  
i2c_expected_device_addresses = [0x15, 0x16, 0x35, 0x4c, 0x4d]  # Hexadezimalwerte der Adressen 21, 22, 53, 76 und 77

# =========================================================================================================================================================
# 
# check Routinen
# 
# =========================================================================================================================================================

# ---------------------------------------------------------------------------------------------
# Raspberry Pi Version 
# ----------------------------------------------------------------------------------------------

def check_raspberrypi():
	try:
		with open('/proc/cpuinfo', 'r') as f:
			for line in f:
				if line.startswith('Revision'):
					revision = line.split(':')[1].strip()
					return interpret_revision(revision)
	except Exception as e:
		return f"Fehler beim Auslesen: {e}"

def interpret_revision(revision):
	# Stand 2024-01-06
	# siehe https://github.com/raspberrypi/documentation/blob/develop/documentation/asciidoc/computers/raspberry-pi/revision-codes.adoc
	pi_models = {
		'900021': 'Raspberry Pi A+',
		'900032': 'Raspberry Pi B+',
		'900092': 'Raspberry Pi Zero',
		'900093': 'Raspberry Pi Zero',
		'9000c1': 'Raspberry Pi Zero W',
		'9020e0': 'Raspberry Pi 3A+',
		'920092': 'Raspberry Pi Zero',
		'920093': 'Raspberry Pi Zero',
		'900061': 'Raspberry Pi CM1',
		'a01040': 'Raspberry Pi 2B',
		'a01041': 'Raspberry Pi 2B',
		'a02082': 'Raspberry Pi 3B',
		'a020a0': 'Raspberry Pi CM3',
		'a020d3': 'Raspberry Pi 3B+',
		'a02042': 'Raspberry Pi 2B',
		'a21041': 'Raspberry Pi 2B',
		'a22042': 'Raspberry Pi 2B',
		'a22082': 'Raspberry Pi 3B',
		'a220a0': 'Raspberry Pi CM3',
		'a32082': 'Raspberry Pi 3B',
		'a52082': 'Raspberry Pi 3B',
		'a22083': 'Raspberry Pi 3B',
		'a02100': 'Raspberry Pi CM3+',
		'a03111': 'Raspberry Pi 4B',
		'b03111': 'Raspberry Pi 4B',
		'b03112': 'Raspberry Pi 4B',
		'b03114': 'Raspberry Pi 4B',
		'b03115': 'Raspberry Pi 4B',
		'c03111': 'Raspberry Pi 4B',
		'c03112': 'Raspberry Pi 4B',
		'c03114': 'Raspberry Pi 4B',
		'c03115': 'Raspberry Pi 4B',
		'd03114': 'Raspberry Pi 4B',
		'd03115': 'Raspberry Pi 4B',
		'c03130': 'Raspberry Pi 400',
		'a03140': 'Raspberry Pi CM4',
		'b03140': 'Raspberry Pi CM4',
		'c03140': 'Raspberry Pi CM4',
		'd03140': 'Raspberry Pi CM4',
		'902120': 'Raspberry Pi Zero 2 W',
		'c04170': 'Raspberry Pi 5',
		'd04170': 'Raspberry Pi 5',
		# Weitere Revisionsnummern können hier hinzugefügt werden
	}	
	model = pi_models.get(revision, 'Unbekanntes Modell')
	return f"{model} ({revision})"	


# ---------------------------------------------------------------------------------------------
# MagicMirror über pm2 status
# ----------------------------------------------------------------------------------------------

def check_magicmirror():
	try:
		# Führe das Kommando 'pm2 status' aus und erfasse die Ausgabe
		result = subprocess.run(['pm2', 'status'], stdout=subprocess.PIPE, text=True)

		# Überprüfe jede Zeile der Ausgabe
		for line in result.stdout.split('\n'):
			if 'MagicMirror' in line and 'online' in line:
				return True

		return False

	except Exception as e:
		print(f"Ein Fehler ist aufgetreten: {e}")
		return False
	
# ---------------------------------------------------------------------------------------------
# MariaDB über den Aufbau einer Verbindung
# ----------------------------------------------------------------------------------------------
def check_mariadb():
	try:
		cplib = CaravanPiFiles()
		connection = cplib.create_db_connection()

		# Überprüfen Sie, ob die Verbindung erfolgreich hergestellt wurde
		if connection is not None:
			connection.disconnect() # Schließen Sie die Verbindung, wenn sie erfolgreich hergestellt wurde
			return True
		else:
			return False
		
	except Exception as e:
		print(f"Ein Fehler ist aufgetreten: {e}")
		return False
	
# ---------------------------------------------------------------------------------------------
# Grafana über das Aufrufen der Website
# ----------------------------------------------------------------------------------------------
def check_grafana():
	try:
		# Verwende localhost, da das Skript auf demselben Gerät läuft
		response = requests.get("http://localhost:3000/login")
		if response.status_code == 200:
			return True
		else:
			return False
	except Exception as e:
		print(f"Fehler beim Verbinden zu Grafana: {e}")
		return False
	
# ---------------------------------------------------------------------------------------------
# Apache Webserver über den Dienst
# ----------------------------------------------------------------------------------------------
def check_apache():
	# Der Dienstname variiert je nach Distribution (z.B. 'httpd' oder 'apache2')
	apache_service_name = 'apache2'  # oder 'httpd' für andere Distributionen

	# Überprüfe, ob der Apache-Dienst existiert
	try:
		subprocess.run(['systemctl', 'is-active', '--quiet', apache_service_name], check=True)
		return True
	except subprocess.CalledProcessError:
		print("Apache Webserver ist entweder nicht installiert oder nicht aktiv.")
		return False

# ---------------------------------------------------------------------------------------------
# 1-wire Bus prüfen
# ----------------------------------------------------------------------------------------------
def check_1_wire():
    # Pfad, wo die 1-Wire-Geräte im Dateisystem erscheinen
    base_dir = '/sys/bus/w1/devices/'

    try:
        # Stelle sicher, dass der 1-Wire-Ordner existiert
        if not os.path.exists(base_dir):
            print("1-Wire-Ordner nicht gefunden. Ist der 1-Wire-Bus aktiviert?")
            return False

        # Liste alle Geräte im 1-Wire-Bus auf
        device_folders = glob.glob(base_dir + '28*')  # 28* ist der übliche Präfix für DS18B20-Geräte

        if not device_folders:
            print("Keine 1-Wire-Geräte gefunden.")
            return False

        print(f"Gefundene 1-Wire-Geräte: {device_folders}")
        return True

    except Exception as e:
        print(f"Fehler beim Überprüfen des 1-Wire-Bus: {e}")
        return False

# ---------------------------------------------------------------------------------------------
# i2c und die erwarteten Geräte über smbus2
# ----------------------------------------------------------------------------------------------
def scan_i2c_bus(bus_number):
	bus = smbus2.SMBus(bus_number)
	device_addresses = []
	for device in range(128):
		try:
			bus.read_byte(device)
			device_addresses.append(hex(device))
		except:  # Gerät an dieser Adresse existiert nicht
			continue
	bus.close()
	return device_addresses

def check_i2c():
	found_devices = set(scan_i2c_bus(i2c_bus_number))
	expected_devices = set(i2c_expected_device_addresses)

	if found_devices == expected_devices:
		return "OK"
	elif found_devices.issubset(expected_devices):
		missing_devices = expected_devices - found_devices
		# return f"Fehler - folgende Devices fehlen: {', '.join(missing_devices)}"
		return f"Fehler - nur folgende Devices gefunden: {', '.join(found_devices)}"
	else:
		extra_devices = found_devices - expected_devices
		# return f"Fehler - unerwartete Devices gefunden: {', '.join(extra_devices)}"
		return f"Fehler - unerwartete Devices gefunden"

# ---------------------------------------------------------------------------------------------
# hx711 prüfen
# ----------------------------------------------------------------------------------------------
def check_hx711():
	script_path = "/home/pi/CaravanPi/gas-weight/gasScale2file.py"
	args = ["python3", "-u", script_path, "-g", "1", "-s", "-c"]

	try:
		# Führe das externe Skript aus und erhalte den Rückgabestatus
		result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

		if result.returncode == 0:
			print("HX711-Prüfung erfolgreich: ", result.stdout)
			return True
		else:
			print("HX711-Prüfung fehlgeschlagen: ", result.stderr)
			return False

	except Exception as e:
		print(f"Fehler beim Ausführen des Skripts: {e}")
		return False

# ---------------------------------------------------------------------------------------------
# sind bestimmte python module installiert?
# ----------------------------------------------------------------------------------------------

def check_python_modul(module_name):
	module_spec = importlib.util.find_spec(module_name)
	return module_spec is not None

	"""
	# Code Schnipsel
	# falls Modul smbus installiert ist, bindes es ein

	smbus2 = None

	if is_module_installed('smbus2'):
		smbus2 = importlib.import_module('smbus2')
		print("Modul 'smbus2' erfolgreich importiert.")
	else:
		print("Modul 'smbus2' ist nicht installiert. Bitte installieren Sie es, um fortzufahren.")

	# Beispiel, wie das Modul verwendet wird, vorausgesetzt, es ist installiert
	if smbus2:
		# Hier können Sie Funktionen von smbus2 verwenden
		pass

	"""
# 
# alle Routen 
#

def register_checks_routes(app):

	@app.route('/checks')
	def check_home():
		# Results zurücksetzen
		global check_results
		check_results = {check['key']: {'result': None, 'color': None} for check in check_list}
		return render_template('check_base_template.html', title='Start der Checks', current_check='Start', check_list=check_list, check_results=check_results, next_check_route='route_check_raspberrypi')
	
	@app.route('/check_raspberrypi')
	def route_check_raspberrypi():
		# Suchen des Raspberry Pi Check in der check_list
		check_info = next((item for item in check_list if item['key'] == 'check_raspberrypi'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info and check_info['run_check']:
			# Check durchführen
			result = check_raspberrypi()
			check_results['check_raspberrypi']['result'] = result
			check_results['check_raspberrypi']['color'] = 'green'
		else:
			# Ansonsten in results als nicht ausgeführt definieren
			check_results['check_raspberrypi']['result'] = 'Nicht ausgeführt'
			check_results['check_raspberrypi']['color'] = 'grey'
		return render_template('check_base_template.html', title='Check Raspberry Pi', current_check='check_raspberrypi', check_list=check_list, check_results=check_results, next_check_route='route_check_magicmirror')

	@app.route('/check_magicmirror')
	def route_check_magicmirror():
		# Suchen des MagicMirror-Check in der check_list
		check_info = next((item for item in check_list if item['key'] == 'check_magicmirror'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info and check_info['run_check']:
			# Check durchführen
			result = check_magicmirror()
			check_results['check_magicmirror']['result'] = 'OK' if result else 'Fehler'
			check_results['check_magicmirror']['color'] = 'green' if result else 'red'
		else:
			# Ansonsten in results als nicht ausgeführt definieren
			check_results['check_magicmirror']['result'] = 'Nicht ausgeführt'
			check_results['check_magicmirror']['color'] = 'grey'

		return render_template('check_base_template.html', title='Check MagicMirror', current_check='check_magicmirror', check_list=check_list, check_results=check_results, next_check_route='route_check_mariadb')

	@app.route('/check_mariadb')
	def route_check_mariadb():
		check_info = next((item for item in check_list if item['key'] == 'check_mariadb'), None)
		if check_info and check_info['run_check']:
			result = check_mariadb()
			check_results['check_mariadb']['result'] = 'OK' if result else 'Fehler'
			check_results['check_mariadb']['color'] = 'green' if result else 'red'
		else:
			check_results['check_mariadb']['result'] = 'Nicht ausgeführt'
			check_results['check_mariadb']['color'] = 'grey'
		return render_template('check_base_template.html', title='Check MariaDB', current_check='check_mariadb', check_list=check_list, check_results=check_results, next_check_route='route_check_grafana')

	@app.route('/check_grafana')
	def route_check_grafana():
		check_info = next((item for item in check_list if item['key'] == 'check_grafana'), None)
		if check_info and check_info['run_check']:
			result = check_grafana()
			check_results['check_grafana']['result'] = 'OK' if result else 'Fehler'
			check_results['check_grafana']['color'] = 'green' if result else 'red'
		else:
			check_results['check_grafana']['result'] = 'Nicht ausgeführt'
			check_results['check_grafana']['color'] = 'grey'
		return render_template('check_base_template.html', title='Check Grafana', current_check='check_grafana', check_list=check_list, check_results=check_results, next_check_route='route_check_apache')

	@app.route('/check_apache')
	def route_check_apache():
		check_info = next((item for item in check_list if item['key'] == 'check_apache'), None)
		if check_info and check_info['run_check']:
			result = check_apache()
			check_results['check_apache']['result'] = 'OK' if result else 'Fehler'
			check_results['check_apache']['color'] = 'green' if result else 'red'
		else:
			check_results['check_apache']['result'] = 'Nicht ausgeführt'
			check_results['check_apache']['color'] = 'grey'
		return render_template('check_base_template.html', title='Check Apache Webserver', current_check='check_apache', check_list=check_list, check_results=check_results, next_check_route='route_check_1_wire')

	@app.route('/check_1_wire')
	def route_check_1_wire():
		check_info = next((item for item in check_list if item['key'] == 'check_1_wire'), None)
		if check_info and check_info['run_check']:
			result = check_1_wire()
			check_results['check_1_wire']['result'] = 'OK' if result else 'Fehler'
			check_results['check_1_wire']['color'] = 'green' if result else 'red'
		else:
			check_results['check_1_wire']['result'] = 'Nicht ausgeführt'
			check_results['check_1_wire']['color'] = 'grey'
		return render_template('check_base_template.html', title='Check 1-Wire Bus', current_check='check_1_wire', check_list=check_list, check_results=check_results, next_check_route='route_check_i2c')

	@app.route('/check_i2c')
	def route_check_i2c():
		check_info = next((item for item in check_list if item['key'] == 'check_i2c'), None)
		if check_info and check_info['run_check']:
			result = check_i2c()
			check_results['check_i2c']['result'] = result
			check_results['check_i2c']['color'] = 'green' if result == "OK" else 'red'
		else:
			check_results['check_i2c']['result'] = 'Nicht ausgeführt'
			check_results['check_i2c']['color'] = 'grey'
		return render_template('check_base_template.html', title='Check I2C Bus', current_check='check_i2c', check_list=check_list, check_results=check_results, next_check_route='route_check_hx711')

	@app.route('/check_hx711')
	def route_check_hx711():
		check_info = next((item for item in check_list if item['key'] == 'check_hx711'), None)
		if check_info and check_info['run_check']:
			result = check_hx711()
			check_results['check_hx711']['result'] = 'OK' if result else 'Fehler'
			check_results['check_hx711']['color'] = 'green' if result else 'red'
		else:
			check_results['check_hx711']['result'] = 'Nicht ausgeführt'
			check_results['check_hx711']['color'] = 'grey'
		return render_template('check_base_template.html', title='Check Wägezelle HX711', current_check='check_hx711', check_list=check_list, check_results=check_results, next_check_route='route_check_final')


	@app.route('/check_final')
	def route_check_final():
		return render_template('check_base_template.html', title='Alle Checks abgeschlossen', current_check='Ende', check_list=check_list, check_results=check_results, next_check_route=None)
