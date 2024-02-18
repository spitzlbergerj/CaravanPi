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
import pkgutil
import ast
import pkg_resources
import xml.etree.ElementTree as ET
import re
import socket
import struct

from flask import render_template
from flask import Markup
from time import sleep

# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles

cplib = CaravanPiFiles()

# Globale Variable zur Speicherung der Ergebnisse
check_list = [
	{'name': 'Raspberry Pi', 'key': 'check_raspberrypi', 'run_check': True},
	{'name': 'github CaravanPi Version', 'key': 'check_github_version', 'run_check': True},
	{'name': 'CaravanPi Defaults XML', 'key': 'check_caravanpi_xml', 'run_check': True},
	{'name': 'Python Bibliotheken', 'key': 'check_python_modules', 'run_check': True},
	{'name': 'MagicMirror', 'key': 'check_magicmirror', 'run_check': True},
	{'name': 'MariaDB', 'key': 'check_mariadb', 'run_check': True},
	{'name': 'Grafana', 'key': 'check_grafana', 'run_check': True},
	{'name': 'Apache Webserver', 'key': 'check_apache', 'run_check': True},
	{'name': '1-Wire Bus', 'key': 'check_1_wire', 'run_check': True},
	{'name': 'I2C Bus', 'key': 'check_i2c', 'run_check': True},
	{'name': 'Wägezelle HX711', 'key': 'check_hx711', 'run_check': True},
	{'name': 'Netzwerk', 'key': 'check_network', 'run_check': True},
	{'name': 'Crontab pi', 'key': 'check_crontab_pi', 'run_check': True},
	{'name': 'Crontab root', 'key': 'check_crontab_root', 'run_check': True},
]

# Initialisiere check_results automatisch basierend auf check_list
check_results = {check['key']: {'result': None, 'color': None} for check in check_list}

# Globale Variable Pfad zur CaravanPi Installation
path2caravanpi = "/home/pi/CaravanPi"  

# Globale Variable mit den erwarteten I2C Bus Geräten
i2c_bus_number = 1  
i2c_expected_device_addresses = [0x20, 0x21, 0x53, 0x76, 0x77]  # erwartete i2c Adressen 21, 22, 53, 76 und 77

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
# CaravanPi github Version 
#
# Diese Prüfung verwendet absichtlich bash Kommandos und nicht das python Modul GitPython,
# mit dem etliches einfacher ginge. Ich wollte jedoch keine weitere Abhängigkeit zu einem 
# python Modul, das nur hier in der check Routine benötigt wird, aber nicht für den Caravan Pi an sich
#
# hier wird immer die lokale Version unabhängig vom lokalen branch mit den main branch auf github.com verglichen
# ----------------------------------------------------------------------------------------------

def run_git_command(command):
	try:
		result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		return result.stdout.strip()
	except subprocess.CalledProcessError as e:
		return e.stderr

def check_github_version():
	# Wechseln in das Repository-Verzeichnis
	subprocess.os.chdir(path2caravanpi)

	# Aktualisieren der Informationen vom Remote-Repository
	run_git_command("git fetch")

	# Abfrage der aktuellen Commit-ID
	current_version = run_git_command("git rev-parse HEAD")
	last_commit_date_remote = run_git_command(f"git -C {path2caravanpi} log -1 --format=%cd origin/master --date=short")
	last_commit_date_local = run_git_command(f"git -C {path2caravanpi} log -1 --format=%cd --date=short")

	# Abfrage der Anzahl der Commits hinter dem 'main' des Remote-Repositories
	commits_behind = run_git_command("git rev-list HEAD..origin/master --count")

	# Abfrage der Anzahl der Commits vor dem 'main' des Remote-Repositories
	commits_ahead = run_git_command("git rev-list origin/master..HEAD --count")

	# Erstellung der HTML-Tabelle:
	table_html = f"""
	<table>
		<tr style="padding: 0px;">
			<td style="padding: 0px;">github.com:</td>
			<td style="padding: 0px;">{last_commit_date_remote}</td>
		</tr>
		<tr style="padding: 0px;">
			<td style="padding: 0px;">Raspberry:</td>
			<td style="padding: 0px;">{last_commit_date_local}</td>
		</tr>
		<tr style="padding: 0px;">
			<td style="padding: 0px;">lokal hinter github:</td>
			<td style="padding: 0px;">{commits_behind} commits</td>
		</tr>
		<tr style="padding: 0px;">
			<td style="padding: 0px;">lokal vor github:</td>
			<td style="padding: 0px;">{commits_ahead} commits</td>
		</tr>
	</table>
	"""

	return Markup(table_html)


# ---------------------------------------------------------------------------------------------
# Testen der Defaults Datei
# ----------------------------------------------------------------------------------------------

def check_caravanpi_xml():
	filepath = os.path.join(path2caravanpi, "defaults/caravanpiConfig.xml")

	# Überprüfen, ob die Datei existiert
	if not os.path.exists(filepath):
		print (f"Datei {filepath} existiert nicht")
		return False

	try:
		with open(filepath, 'r', encoding='utf-8') as file:
			xml_content = file.read()

		# XML-Datei parsen
		root = ET.fromstring(xml_content)

		# Überprüfen, ob der Root-Tag korrekt ist
		if root.tag != 'CaravanPiConfigurations':
			print (f"das Root Tag ist nicht CaravanPiConfigurations")
			return False

		# Überprüfen, ob alle Kinder-Elemente und ihre Werte vorhanden sind
		for child in root.iter():
			if not list(child) and (child.text is None or child.text.strip() == ''):
				print (f"es fehlen Werte: {child.text}")
				return False
	except ET.ParseError:
		# Fehler beim Parsen der XML-Datei
		print (f"Das Parsen schlug fehl")
		return False

	# Wenn alles in Ordnung ist
	return True	


# ---------------------------------------------------------------------------------------------
# Prüfe, ob alle nicht Standard Python module, die in den Python Skripten verwendet werden, auch installiert sind
# ----------------------------------------------------------------------------------------------

def check_python_modules():
	standard_lib = set(sys.builtin_module_names)
	standard_lib.update({module.name for module in pkgutil.iter_modules()})

	# Verzeichnis, das durchsucht werden soll
	search_dir = path2caravanpi

	# Liste für gefundene Nicht-Standard-Module
	non_standard_modules = set()

	# Liste für installierte Module
	installed_packages = {pkg.key for pkg in pkg_resources.working_set}

	# Durchsuchen des Verzeichnisses nach Python-Dateien
	for root, _, files in os.walk(search_dir):
		for file in files:
			if file.endswith('.py'):
				file_path = os.path.join(root, file)
				with open(file_path, 'r') as f:
					try:
						# Parsen des Inhalts der Datei
						tree = ast.parse(f.read(), file_path)

						# Extrahieren der Import-Anweisungen
						for node in ast.walk(tree):
							if isinstance(node, ast.Import):
								for name in node.names:
									module_name = name.name.split('.')[0]
									if module_name and module_name not in standard_lib and not module_name.startswith('CaravanPi'):
										print (f"Nicht Standard-Modul {module_name} in Datei {file_path}")
										non_standard_modules.add(module_name)
							elif isinstance(node, ast.ImportFrom):
								module_name = node.module.split('.')[0] if node.module else None
								if module_name and module_name not in standard_lib and not module_name.startswith('CaravanPi'):
									print (f"Nicht Standard-Modul {module_name} in Datei {file_path} (from)")
									non_standard_modules.add(module_name)
					except SyntaxError as e:
						print(f"Fehler beim Parsen der Datei {file_path}: {e}")

	# Überprüfen, ob die Module installiert sind
	installed_non_standard_modules = non_standard_modules & installed_packages
	not_installed_modules = non_standard_modules - installed_packages

	# print("Standard-Module:", standard_lib)
	# print("Installierte Nicht-Standard-Module:", installed_non_standard_modules)
	# nein.print("Nicht installierte Module:", not_installed_modules)
	
	if len(not_installed_modules) == 0:
		return f"OK"
	else:
		return f"{', '.join(not_installed_modules)} nicht installiert"

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
			return False, "kein 1-Wire-Verzeichnis"

		# Liste alle Geräte im 1-Wire-Bus auf
		device_folders = glob.glob(base_dir + '28*')  # 28* ist der übliche Präfix für DS18B20-Geräte

		if not device_folders:
			print("Keine 1-Wire-Geräte gefunden.")
			return False, "keine Devices"

		# Extrahiere den letzten Teil jedes Pfades und füge diese zu einem String zusammen
		device_ids_komma = ', '.join(os.path.basename(folder) for folder in device_folders)
		device_ids_break = Markup('<br>'.join(os.path.basename(folder) for folder in device_folders))

		print(f"Gefundene 1-Wire-Geräte: {device_ids_komma}")
		return True, device_ids_break

	except Exception as e:
		print(f"Fehler beim Überprüfen des 1-Wire-Bus: {e}")
		return False, "Fehler"

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
	global i2c_expected_device_addresses  # Globale Variable ansprechen

	# Einlesen der Anzahlen für Waagen, Tanks, Klimasensoren
	caravanpiDefaults_tuple = cplib.readCaravanPiDefaults()
	if caravanpiDefaults_tuple is None:
		expected_climates = 1
	else:
		expected_climates = caravanpiDefaults_tuple[13] if caravanpiDefaults_tuple[13] is not None else 0

	# Anpassen der erwarteten I2C-Geräteadressen basierend auf expected_climates
	if expected_climates == 1:
		# Entfernen von 76, wenn es in der Liste ist
		i2c_expected_device_addresses = [addr for addr in i2c_expected_device_addresses if addr != 0x77]
	elif expected_climates == 0:
		# Entfernen von 76 und 77, wenn sie in der Liste sind
		i2c_expected_device_addresses = [addr for addr in i2c_expected_device_addresses if addr not in (0x76, 0x77)]

	found_devices_hex = set(scan_i2c_bus(i2c_bus_number))  # Hex-Strings wie '0x20'
	expected_devices = set(i2c_expected_device_addresses)  # Ganzzahlen

	# Konvertieren der gefundenen Hex-Strings in Dezimalzahlen für den Vergleich
	found_devices_dec = set(int(addr, 16) for addr in found_devices_hex)

	# Umwandeln der erwarteten Geräteadressen in Hex-Strings ohne "0x" für die Ausgabe
	expected_devices_str = sorted([format(addr, 'x') for addr in expected_devices], key=lambda x: int(x, 16))
	
	# Umwandeln der gefundenen Geräteadressen in Hex-Strings ohne "0x" für die Ausgabe
	found_devices_str = sorted([format(addr, 'x') for addr in found_devices_dec], key=lambda x: int(x, 16))

	if found_devices_dec == expected_devices:
		return True, Markup(f"OK<br>erwartet: {','.join(expected_devices_str)}<br>gefunden: {','.join(found_devices_str)}")
	elif found_devices_dec.issubset(expected_devices):
		missing_devices = expected_devices - found_devices_dec
		missing_devices_str = sorted([format(addr, 'x') for addr in missing_devices], key=lambda x: int(x, 16))
		return False, Markup(f"fehlende Devices!<br>erwartet: {','.join(expected_devices_str)}<br>gefunden: {','.join(found_devices_str)}<br>fehlend: {','.join(missing_devices_str)}")
	else:
		extra_devices = found_devices_dec - expected_devices
		extra_devices_str = sorted([format(addr, 'x') for addr in extra_devices], key=lambda x: int(x, 16))
		return False, Markup(f"zu viele Devices!<br>erwartet: {','.join(expected_devices_str)}<br>gefunden: {','.join(found_devices_str)}<br>zusätzlich: {','.join(extra_devices_str)}")
	
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
# Netzwerk untersuchen
# ---------------------------------------------------------------------------------------------
	
def is_netaddr_installed():
	try:
		import netaddr
		print(f"Modul 'netaddr' ist installiert.")
		return True
	except ImportError:
		print(f"Modul 'netaddr' ist nicht installiert. Bitte installieren Sie es mit 'pip install netaddr'.")
		return False
	
def is_fping_installed():
	try:
		subprocess.check_output(["fping", "-v"])  # Versucht, die Version von fping zu bekommen
		return True
	except subprocess.CalledProcessError:
		# fping ist nicht korrekt installiert oder nicht im PATH
		return False
	except FileNotFoundError:
		# fping ist nicht installiert
		return False

def get_own_ip_mask():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# doesn't even have to be reachable
		s.connect(('10.255.255.255', 1))
		IP = s.getsockname()[0]
	finally:
		s.close()
	mask = '255.255.255.0'
	return IP, mask

def check_network():
	if not is_netaddr_installed():
		return False, "Netzwerkprüfung gescheitert: netaddr nicht installiert"
	else:
		from netaddr import IPNetwork
	
	if not is_fping_installed():
		return True, "Netzwerkprüfung gescheitert: fping nicht installiert"
	
	try:
		own_ip, own_mask = get_own_ip_mask()
		subnet = str(IPNetwork(f"{own_ip}/{own_mask}").cidr)
		command = f"fping -aAnqs -g {subnet} -r 1"
		print(command)
		result = subprocess.run(command, shell=True, text=True, capture_output=True)
		# print(result)
		
		# Verarbeitung des Scan-Ergebnisses
		if result.returncode in [0, 1]:  # Erfolg oder teilweiser Erfolg
			device_info = re.findall(r'(\d+\.\d+\.\d+\.\d+)[^\s]*\s+([^\s]+)', result.stdout)
			# Entfernen der Domain (z.B. ".fritz.box") vom Hostnamen und Zusammenführen von IP und gekürztem Hostnamen
			devices_formatted = [f"{ip} - {name.split('.')[0]}" for ip, name in device_info]
			# print(devices_formatted)
			device_list_html = Markup('<br>'.join(devices_formatted))
			# print(device_list_html)
			return True, f"{device_list_html}"
		else:
			return False, f"Netzwerkprüfung gescheitert: fping-Fehler mit Exit-Status {result.returncode}"
	except Exception as e:
		return False, f"Netzwerkprüfung gescheitert: Fehler: {str(e)}"

# ---------------------------------------------------------------------------------------------
# Crontab untersuchen
# ---------------------------------------------------------------------------------------------

# Funktion zum Überprüfen, ob ein Skriptname in nicht-auskommentierten Zeilen vorkommt
def is_script_present(crontab_lines, script_name):
	pattern = fr'^\s*[^#]*\b{script_name}\b'
	return any(re.search(pattern, line) for line in crontab_lines)

# Zählt, wie oft ein Skript in nicht-auskommentierten Zeilen vorkommt
def count_script_occurrences(crontab_lines, script_name):
	count = 0
	for line in crontab_lines:
		if not line.strip().startswith('#') and script_name in line:
			count += 1
	return count

def check_crontab_pi():
	# Einlesen der Anzahlen für Waagen, Tanks, Klimasensoren
	caravanpiDefaults_tuple = cplib.readCaravanPiDefaults()
	if caravanpiDefaults_tuple is None:
		expected_scales = 1
		expected_tanks = 1
		expected_climates = 1
	else:
		expected_scales = caravanpiDefaults_tuple[0] if caravanpiDefaults_tuple[0] is not None else 0
		expected_tanks = caravanpiDefaults_tuple[1] if caravanpiDefaults_tuple[1] is not None else 0
		expected_climates = caravanpiDefaults_tuple[13] if caravanpiDefaults_tuple[13] is not None else 0

	command = ['crontab', '-l', '-u', 'pi']
	
	# Crontab auslesen
	result = subprocess.run(command, capture_output=True, text=True)
	crontab_lines = result.stdout.split('\n')

	# Titel für jede Prüfung
	titles = {
		'flask_main': 'flask wird gestartet',
		'temp2file_regular': 'Temperatursensoren auslesen',
		'position2file_regular': 'Lagesensor auslesen',
		'tactileSwitches_boot': 'Taster aktivieren',
		'systemstat2file_boot': 'Systeminfos auslesen',
		'RTCSerial_boot': 'StromPi Uhr synchronisieren',
		'scales': 'Gaswaagen auslesen',
		'tanks': 'Tanks auslesen',
		'climates': 'Klimasensoren auslesen'
	}

	checks_passed = []

	checks = ['flask_main', 'temp2file_regular', 'position2file_regular', 'tactileSwitches_boot', 'systemstat2file_boot', 'RTCSerial_boot', 'scales', 'tanks', 'climates']
	check_functions = {
		'flask_main': lambda: is_script_present(crontab_lines, 'flask-main.py'),
		'temp2file_regular': lambda: is_script_present(crontab_lines, 'temp2file.py'),
		'position2file_regular': lambda: is_script_present(crontab_lines, 'position2file.py'),
		'tactileSwitches_boot': lambda: is_script_present(crontab_lines, 'tactileSwitches.py'),
		'systemstat2file_boot': lambda: is_script_present(crontab_lines, 'systemstat2file.py'),
		'RTCSerial_boot': lambda: is_script_present(crontab_lines, 'RTCSerial.py'),
		# 'scales': lambda: (scales_count := count_script_occurrences(crontab_lines, r'gasscale2file -g \d+'), scales_count == expected_scales),
		# 'tanks': lambda: (tanks_count := count_script_occurrences(crontab_lines, r'tankFilllevel2file -t \d+'), tanks_count == expected_tanks),
		# 'climates': lambda: (climates_count := count_script_occurrences(crontab_lines, r'climate2file -i (76|77)'), climates_count == expected_climates * 2)
		'scales': lambda: (count := count_script_occurrences(crontab_lines, 'gasScale2file.py'), count == expected_scales),
		'tanks': lambda: (count := count_script_occurrences(crontab_lines, 'freshLevels2file.py') + count_script_occurrences(crontab_lines, 'wasteLevels2file.py'), count == expected_tanks),
		'climates': lambda: (count := count_script_occurrences(crontab_lines, 'climate2file.py'), count == expected_climates)	}

	print(titles)
	print(checks)
	print(check_functions)

	for check in checks:
		title = titles[check]  # Titel für die aktuelle Prüfung
		if check in ['scales', 'tanks', 'climates']:
			count, result = check_functions[check]()
			if result:
				checks_passed.append(f"{title}: OK")
			else:
				error_message = Markup(f"<span style='color: red;'>Fehler ({count} statt {expected_scales if check == 'scales' else expected_tanks if check == 'tanks' else expected_climates * 2})</span>")
				checks_passed.append(f"{title}: {error_message}")
		else:
			result = check_functions[check]()
			if result:
				checks_passed.append(f"{title}: OK")
			else:
				error_message = Markup("<span style='color: red;'>Fehler</span>")
				checks_passed.append(f"{title}: {error_message}")

	# Zusammenführen der Ausgabezeilen mit <br> für die HTML-Ausgabe
	output_html = Markup('<br>'.join(checks_passed))

	return True, output_html

def check_crontab_root():
	# Bestimmt den Befehl basierend auf dem übergebenen Benutzer
	command = ['sudo', 'crontab', '-l', '-u', 'root']
	
	# Crontab auslesen
	result = subprocess.run(command, capture_output=True, text=True)
	crontab_lines = result.stdout.split('\n')

	# Titel für jede Prüfung
	titles = {
		'backup': 'Backup Skript starten',
		'pir': 'Bewegunssensor aktivieren',
		'logrotate': 'Logdateien rotieren',
	}

	checks_passed = []

	checks = ['backup', 'pir', 'logrotate']
	check_functions = {
		'backup': lambda: is_script_present(crontab_lines, 'backup.sh'),
		'pir': lambda: is_script_present(crontab_lines, 'pir.py'),
		'logrotate': lambda: is_script_present(crontab_lines, 'logrotate'),
	}

	print(titles)
	print(checks)
	print(check_functions)

	for check in checks:
		title = titles[check]  # Titel für die aktuelle Prüfung
		result = check_functions[check]()
		if result:
			checks_passed.append(f"{title}: OK")
		else:
			error_message = Markup("<span style='color: red;'>Fehler</span>")
			checks_passed.append(f"{title}: {error_message}")

	# Zusammenführen der Ausgabezeilen mit <br> für die HTML-Ausgabe
	output_html = Markup('<br>'.join(checks_passed))

	return True, output_html

# ==============================================================================================
#
# was ist der nächste Check?
#
# ==============================================================================================

def find_next_route(current_key):
	current_index = next((index for (index, d) in enumerate(check_list) if d["key"] == current_key), None)
	if current_index is not None:
		for next_check in check_list[current_index + 1:]:
			if next_check['run_check']:
				return 'route_' + next_check['key']
	return 'route_check_final'


# ==============================================================================================
#
# FLASK Routen
#
# ==============================================================================================

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
		if check_info:
			next_route = find_next_route('check_raspberrypi')
			if check_info['run_check']:
				# Check durchführen
				result = check_raspberrypi()
				check_results['check_raspberrypi']['result'] = result
				check_results['check_raspberrypi']['color'] = 'green'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	

		return render_template('check_base_template.html', title='Check Raspberry Pi', current_check='check_raspberrypi', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_github_version')
	def route_check_github_version():
		# Github version
		check_info = next((item for item in check_list if item['key'] == 'check_github_version'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info:
			next_route = find_next_route('check_github_version')
			if check_info['run_check']:
				# Check durchführen
				result = check_github_version()
				check_results['check_github_version']['result'] = result
				check_results['check_github_version']['color'] = 'green'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	

		return render_template('check_base_template.html', title='Check github Version', current_check='check_github_version', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_caravanpi_xml')
	def route_check_caravanpi_xml():
		# Suchen des MagicMirror-Check in der check_list
		check_info = next((item for item in check_list if item['key'] == 'check_caravanpi_xml'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info:
			next_route = find_next_route('check_caravanpi_xml')
			if check_info['run_check']:
				# Check durchführen
				result = check_caravanpi_xml()
				check_results['check_caravanpi_xml']['result'] = 'OK' if result else 'Fehler'
				check_results['check_caravanpi_xml']['color'] = 'green' if result else 'red'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	
		
		return render_template('check_base_template.html', title='Check MagicMirror', current_check='check_caravanpi_xml', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_python_modules')
	def route_check_python_modules():
		# Github version
		check_info = next((item for item in check_list if item['key'] == 'check_python_modules'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info:
			next_route = find_next_route('check_python_modules')
			if check_info['run_check']:
				# Check durchführen
				result = check_python_modules()
				check_results['check_python_modules']['result'] = result
				check_results['check_python_modules']['color'] = 'green' if result == "OK" else 'red'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	

		return render_template('check_base_template.html', title='Check github Version', current_check='check_python_modules', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_magicmirror')
	def route_check_magicmirror():
		# Suchen des MagicMirror-Check in der check_list
		check_info = next((item for item in check_list if item['key'] == 'check_magicmirror'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info:
			next_route = find_next_route('check_magicmirror')
			if check_info['run_check']:
				# Check durchführen
				result = check_magicmirror()
				check_results['check_magicmirror']['result'] = 'OK' if result else 'Fehler'
				check_results['check_magicmirror']['color'] = 'green' if result else 'red'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	
		
		return render_template('check_base_template.html', title='Check MagicMirror', current_check='check_magicmirror', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_mariadb')
	def route_check_mariadb():
		check_info = next((item for item in check_list if item['key'] == 'check_mariadb'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info:
			next_route = find_next_route('check_mariadb')
			if check_info['run_check']:
				# Check durchführen
				result = check_mariadb()
				check_results['check_mariadb']['result'] = 'OK' if result else 'Fehler'
				check_results['check_mariadb']['color'] = 'green' if result else 'red'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	

		return render_template('check_base_template.html', title='Check MariaDB', current_check='check_mariadb', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_grafana')
	def route_check_grafana():
		check_info = next((item for item in check_list if item['key'] == 'check_grafana'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info:
			next_route = find_next_route('check_grafana')
			if check_info['run_check']:
				# Check durchführen
				result = check_grafana()
				check_results['check_grafana']['result'] = 'OK' if result else 'Fehler'
				check_results['check_grafana']['color'] = 'green' if result else 'red'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	

		return render_template('check_base_template.html', title='Check Grafana', current_check='check_grafana', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_apache')
	def route_check_apache():
		check_info = next((item for item in check_list if item['key'] == 'check_apache'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info:
			next_route = find_next_route('check_apache')
			if check_info['run_check']:
				# Check durchführen
				result = check_apache()
				check_results['check_apache']['result'] = 'OK' if result else 'Fehler'
				check_results['check_apache']['color'] = 'green' if result else 'red'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	

		return render_template('check_base_template.html', title='Check Apache Webserver', current_check='check_apache', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_1_wire')
	def route_check_1_wire():
		check_info = next((item for item in check_list if item['key'] == 'check_1_wire'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info:
			next_route = find_next_route('check_1_wire')
			if check_info['run_check']:
				# Check durchführen
				result, result_text = check_1_wire()
				check_results['check_1_wire']['result'] = result_text if result else 'Fehler'
				check_results['check_1_wire']['color'] = 'green' if result else 'red'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	

		return render_template('check_base_template.html', title='Check 1-Wire Bus', current_check='check_1_wire', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_i2c')
	def route_check_i2c():
		check_info = next((item for item in check_list if item['key'] == 'check_i2c'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info:
			next_route = find_next_route('check_i2c')
			if check_info['run_check']:
				# Check durchführen
				result, result_text = check_i2c()
				check_results['check_i2c']['result'] = result_text if result else 'Fehler'
				check_results['check_i2c']['color'] = 'green' if result else 'red'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	

		return render_template('check_base_template.html', title='Check I2C Bus', current_check='check_i2c', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_hx711')
	def route_check_hx711():
		check_info = next((item for item in check_list if item['key'] == 'check_hx711'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info:
			next_route = find_next_route('check_hx711')
			if check_info['run_check']:
				# Check durchführen
				result = check_hx711()
				check_results['check_hx711']['result'] = 'OK' if result else 'Fehler'
				check_results['check_hx711']['color'] = 'green' if result else 'red'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	

		return render_template('check_base_template.html', title='Check Wägezelle HX711', current_check='check_hx711', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_network')
	def route_check_network():
		# Github version
		check_info = next((item for item in check_list if item['key'] == 'check_network'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info:
			next_route = find_next_route('check_network')
			if check_info['run_check']:
				# Check durchführen
				result, result_text = check_network()
				check_results['check_network']['result'] = result_text if result else 'Fehler'
				check_results['check_network']['color'] = 'green' if result else 'red'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	

		return render_template('check_base_template.html', title='Check Netzwerk', current_check='check_network', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_crontab_pi')
	def route_check_crontab_pi():
		# Github version
		check_info = next((item for item in check_list if item['key'] == 'check_crontab_pi'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info:
			next_route = find_next_route('check_crontab_pi')
			if check_info['run_check']:
				# Check durchführen
				result, result_text = check_crontab_pi()
				check_results['check_crontab_pi']['result'] = result_text if result else 'Fehler'
				check_results['check_crontab_pi']['color'] = 'green' if result else 'red'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	

		return render_template('check_base_template.html', title='Check Crontab', current_check='check_crontab_pi', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_crontab_root')
	def route_check_crontab_root():
		# Github version
		check_info = next((item for item in check_list if item['key'] == 'check_crontab_root'), None)

		# Überprüfen, ob der Check ausgeführt werden soll
		if check_info:
			next_route = find_next_route('check_crontab_root')
			if check_info['run_check']:
				# Check durchführen
				result, result_text = check_crontab_root()
				check_results['check_crontab_root']['result'] = result_text if result else 'Fehler'
				check_results['check_crontab_root']['color'] = 'green' if result else 'red'
			else:
				# Weiterleitung zum nächsten Check, wenn dieser Check übersprungen werden soll
				return redirect(url_for(next_route))
		else:
			# Weiterleitung zum Ende, wenn der Check nicht gefunden wurde
			return redirect(url_for('route_check_final'))	

		return render_template('check_base_template.html', title='Check Crontab', current_check='check_crontab_root', check_list=check_list, check_results=check_results, next_check_route=next_route)

	@app.route('/check_final')
	def route_check_final():
		return render_template('check_base_template.html', title='Alle Checks abgeschlossen', current_check='Ende', check_list=check_list, check_results=check_results, next_check_route=None)
