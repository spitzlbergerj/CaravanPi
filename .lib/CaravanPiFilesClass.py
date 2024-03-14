#!/usr/bin/python3
# coding=utf-8
# filesClass.py
#
# liest und schreibt Werte aus den und in die default files
# 
# 2023-12 	Umbau zur Nutzung eines xml Files anststt vieler Konfigurationsdateien
#         	dabei soll die "Abwaertskompatibilitaet" erhalten bleiben. 
#         	dieser Kompatibilitaetscode (mit COMPATIBILITY CODE markiert) kann spaeter entfernt werden
#         	Coding wurde unterstuetzt von ChatGPT4
#
#			Die Parameter test und screen in den Schreibfunktionen sind mit der Einfuehrung der xml Struktur 
#			obsolet geworden und sind lediglich aus Kompatibilitaetsgruednen noch da.
#
#-------------------------------------------------------------------------------

# import sys
import xml.etree.ElementTree as ET
import os
import shutil
import mysql.connector
from mysql.connector import Error
import paho.mqtt.client as mqtt
import datetime

class CaravanPiFiles:

	# -----------------------------------------------
	# global variables
	# -----------------------------------------------

	xml_file_path = "/home/pi/CaravanPi/defaults/caravanpiConfig.xml"

	values_file_path = "/home/pi/CaravanPi/values/"

	write2file = None

	write2MariaDB = None
	MariaDBhost = None
	MariaDBuser = None
	MariaDBpasswd = None
	MariaDBdatabase = None

	send2MQTT = None
	MQTTbroker = None
	MQTTport = None
	MQTTuser = None
	MQTTpassword = None

	# ---------------------------------------------------------------------------------------------
	# __init__
	#
	# wird jedesmal aufgerufen, wenn die Class erzeugt wird
	# prüft, ob die Umstellung auf XML Datei noch zu machen ist
	# setzt die globalen Variablen zur MariaDB und zum XML Versand
	# ----------------------------------------------------------------------------------------------

	def __init__(self):
		# COMPATIBILITY CODE - Pruefen, ob alte Dateien in das xml File migriert werden muessen
		self.check_create_xml()
		self.migrate_old_configs()
		# COMPATIBILITY CODE Ende

		# lesen der CaravanPiDefaults und setzen der Class globalen Parameter 
		self.update_settings()

	# ---------------------------------------------------------------------------------------------
		# universelle Typumwandlung
	# ---------------------------------------------------------------------------------------------
	def typwandlung(self, wert, ziel_typ):
		if ziel_typ == "int":
			return int(wert)
		elif ziel_typ == "float":
			return float(wert)
		elif ziel_typ == "bool":
			# "true", "True", "1", etc. werden als True behandelt.
			# "0" ist false
			return wert.lower() in ["true", "1", "yes"]
		elif ziel_typ == "str":
			return str(wert)
		elif ziel_typ == "list":
			# Annahme: Wert ist ein komma-separierter String
			return wert.split(',')
		elif ziel_typ == "dict":
			# Sehr einfache Implementierung; in der Praxis würde man JSON oder einen ähnlichen Ansatz verwenden
			return dict(item.split(':') for item in wert.split(','))
		else:
			raise ValueError(f"Unbekannter Zieltyp: {ziel_typ}")

	# ---------------------------------------------------------------------------------------------
	# update_settings
	#
	# setzt die globalen Variable
	# Funktion sollte in jeder  Schreibfunktion für Sensorwerte aufgerufen werden, damit das
	# Schreiben der MariaDB und das Senden der MQTT Telegramme veranlasst wird, falls neu gesetzt
	# ----------------------------------------------------------------------------------------------
	def update_settings(self):
		# Aktualisiert die Klassenattribute basierend auf der XML-Datei
		self.write2file = self.typwandlung(self.readCaravanPiConfigItem("caravanpiDefaults/write2file"), "bool")
		self.write2MariaDB = self.typwandlung(self.readCaravanPiConfigItem("caravanpiDefaults/write2MariaDB"), "bool")
		self.MariaDBhost = self.typwandlung(self.readCaravanPiConfigItem("caravanpiDefaults/MariaDBhost"), "str")
		self.MariaDBuser = self.typwandlung(self.readCaravanPiConfigItem("caravanpiDefaults/MariaDBuser"), "str")
		self.MariaDBpasswd = self.typwandlung(self.readCaravanPiConfigItem("caravanpiDefaults/MariaDBpasswd"), "str")
		self.MariaDBdatabase = self.typwandlung(self.readCaravanPiConfigItem("caravanpiDefaults/MariaDBdatabase"), "str")
		self.send2MQTT = self.typwandlung(self.readCaravanPiConfigItem("caravanpiDefaults/send2MQTT"), "bool")
		self.MQTTbroker = self.typwandlung(self.readCaravanPiConfigItem("caravanpiDefaults/MQTTbroker"), "str")
		self.MQTTport = self.typwandlung(self.readCaravanPiConfigItem("caravanpiDefaults/MQTTport"), "int")
		self.MQTTuser = self.typwandlung(self.readCaravanPiConfigItem("caravanpiDefaults/MQTTuser"), "str")
		self.MQTTpassword = self.typwandlung(self.readCaravanPiConfigItem("caravanpiDefaults/MQTTpassword"), "str")

	# ---------------------------------------------------------------------------------------------
	# format_xml
	#
	# formatiert die XML, so dass diese besser lesbar wird
	# ----------------------------------------------------------------------------------------------
	def format_xml(self, element, level=0):
		indent = "\n" + level * "  "
		if len(element):  # Wenn das Element Kinder hat
			if not element.text or not element.text.strip():
				element.text = indent + "  "
			if not element.tail or not element.tail.strip():
				element.tail = indent
			for sub_element in element:
				self.format_xml(sub_element, level + 1)
			if not element.tail or not element.tail.strip():
				element.tail = indent
		else:  # Wenn das Element keine Kinder hat
			if level and (not element.tail or not element.tail.strip()):
				element.tail = indent

	# ---------------------------------------------------------------------------------------------
	# is_float
	#
	# prüft einen String-Wert auf den Typ float
	# ----------------------------------------------------------------------------------------------

	def is_float(self, value):
		try:
			float(value)
			return True
		except ValueError:
			return False

	# =========================================================================================================================================================
	# 
	# Schreiben und Lesen der Default Werte
	# 
	# =========================================================================================================================================================

	# ---------------------------------------------------------------------------------------------
	# CaravanPi Config Items
	# ----------------------------------------------------------------------------------------------

	def find_or_create_element_by_path(self, root, path, create_if_missing=False):
		# ---------------------------------------------------------------------------------------------
		# Findet oder erstellt ein Element basierend auf einem '/' getrennten Pfad.
		# ---------------------------------------------------------------------------------------------
		current_element = root
		for part in path.split('/'):
			next_element = current_element.find(part)
			if next_element is None and create_if_missing:
				next_element = ET.SubElement(current_element, part)
			elif next_element is None:
				return None
			current_element = next_element
		return current_element	
	

	def readCaravanPiConfigItem(self, element_path):
		# ---------------------------------------------------------------------------------------------
		# Liest einen Wert basierend auf dem übergebenen XML-Pfad.
		# element_path ist so anzugeben "parent/child/grandchild"
		# ---------------------------------------------------------------------------------------------
		if not os.path.exists(self.xml_file_path):
			print("Die XML-Datei wurde nicht gefunden.")
			return None
		
		try:
			tree = ET.parse(self.xml_file_path)
			root = tree.getroot()
		except ET.ParseError as e:
			print(f"Fehler beim Parsen der XML-Datei: {e}")
			return None
		
		elem = self.find_or_create_element_by_path(root, element_path, create_if_missing=False)
		if elem is not None:
			return elem.text
		else:
			print(f"Element mit dem Pfad '{element_path}' nicht gefunden.")
			return None


	def writeCaravanPiConfigItem(self, element_path, value):
		# ---------------------------------------------------------------------------------------------
		# Schreibt oder aktualisiert einen Wert basierend auf dem übergebenen XML-Pfad.
		# ---------------------------------------------------------------------------------------------

		if not os.path.exists(self.xml_file_path):
			print("Die XML-Datei wurde nicht gefunden.")
			return -1

		try:
			tree = ET.parse(self.xml_file_path)
			root = tree.getroot()
		except ET.ParseError as e:
			print(f"Fehler beim Parsen der XML-Datei: {e}")
			return -1

		final_element = self.find_or_create_element_by_path(root, element_path, create_if_missing=True)
		# print(ET.tostring(final_element, encoding='unicode'))

		final_element.text = str(value)
		# print(ET.tostring(final_element, encoding='unicode'))

		# Formatieren des XML-Baums vor dem Speichern
		self.format_xml(root)
		# print(ET.tostring(root, encoding='unicode'))

		try:
			tree.write(self.xml_file_path, encoding='utf-8', xml_declaration=True)
			return 0
		except IOError as e:
			print(f"Fehler beim Schreiben in die XML-Datei: {e}")
			return -1


	# ---------------------------------------------------------------------------------------------
	# CaravanPiDefaults
	# ----------------------------------------------------------------------------------------------

	def readCaravanPiDefaults(self):
		# ---------------------------------------------------------------------------------------------
		# Liest die CaravanPi Default Werte aus der XML
		# ---------------------------------------------------------------------------------------------
		if not os.path.exists(self.xml_file_path):
			print("Die XML-Datei wurde nicht gefunden.")
			return -1

		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		defaults_element = root.find("caravanpiDefaults")
		defaults = {}

		if defaults_element is not None:
			for child in defaults_element:
				if child.text.isdigit():
					defaults[child.tag] = int(child.text)
				elif child.text.lower() in ['1', 'true']:
					defaults[child.tag] = True
				elif child.text.lower() in ['0', 'false']:
					defaults[child.tag] = False
				else:
					defaults[child.tag] = child.text

		return defaults


	def writeCaravanPiDefaults(self, config_dict):

		if not os.path.exists(self.xml_file_path):
			print("Die XML-Datei wurde nicht gefunden.")
			return -1

		try:
			tree = ET.parse(self.xml_file_path)
			root = tree.getroot()
			defaults_element = root.find("caravanpiDefaults")
			if defaults_element is None:
				defaults_element = ET.SubElement(root, "caravanpiDefaults")
			
			# Konvertierung der booleschen Werte in "0" oder "1" für spezifische Schlüssel
			for key in [
							"write2file", 
							"write2MariaDB", 
							"send2MQTT", 
							"stromPiInstalled", 
							"gassensorInstalled", 
							"gassensorAlarmActive", 
							"gassensorAlarmResume", 
							"v230CheckInstalled", 
							"v230CheckAlarmActive", 
							"v230CheckAlarmResume", 
							"v12BatteryCheckInstalled", 
							"v12BatteryCheckAlarmActive", 
							"v12BatteryCheckAlarmResume", 
							"v12CarCheckInstalled",
							"v12CarCheckAlarmActive",
							"v12CarCheckAlarmResume",
						]:
				if key in config_dict:
					config_dict[key] = '1' if config_dict[key] else '0'

			for key, value in config_dict.items():
				if value is not None:  # Überspringe None-Werte
					# Benutze die angepasste Funktion, um den Pfad zu behandeln
					final_element = self.find_or_create_element_by_path(defaults_element, key, create_if_missing=True)
					final_element.text = str(value)

			# Formatieren des XML-Baums vor dem Speichern
			self.format_xml(root)

			# Schreiben der formatierten XML-Daten in die Datei
			tree.write(self.xml_file_path, encoding='utf-8', xml_declaration=True)
			return 0
		
		except Exception as e:
			print(f"Fehler beim Schreiben in die XML-Datei: {e}")
			return -1

					
	# ---------------------------------------------------------------------------------------------
	# adjustmentPosition
	#
	# content of file
	# 		adjustment X		X value, if caravan is in horizontal position
	#		adjustment Y		Y value, if caravan is in horizontal position
	#		adjustment Z		Z value, if caravan is in horizontal position
	#		tolerance X			deviation in X direction, which is still considered horizontal 
	#		tolerance Y			deviation in Y direction, which is still considered horizontal
	#		approximation X		at which deviation from the horizontal the LEDs should flash
	#		approximation Y		at which deviation from the horizontal the LEDs should flash
	#		distance right		distance of the sensor from the right side
	#		distance front		distance of the sensor from the front side
	# 		distance axis		Distance of the sensor from the axis in longitudinal direction
	# ----------------------------------------------------------------------------------------------

	def readAdjustment(self):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		adjustment_element = root.find("adjustmentPosition")
		if adjustment_element is not None:
			return (
				float(adjustment_element.find("adjustX").text) if adjustment_element.find("adjustX") is not None and self.is_float(adjustment_element.find("adjustX").text) else None,
				float(adjustment_element.find("adjustY").text) if adjustment_element.find("adjustY") is not None and self.is_float(adjustment_element.find("adjustY").text) else None,
				float(adjustment_element.find("adjustZ").text) if adjustment_element.find("adjustZ") is not None and self.is_float(adjustment_element.find("adjustZ").text) else None,
				float(adjustment_element.find("toleranceX").text) if adjustment_element.find("toleranceX") is not None and self.is_float(adjustment_element.find("toleranceX").text) else None,
				float(adjustment_element.find("toleranceY").text) if adjustment_element.find("toleranceY") is not None and self.is_float(adjustment_element.find("toleranceY").text) else None,
				float(adjustment_element.find("approximationX").text) if adjustment_element.find("approximationX") is not None and self.is_float(adjustment_element.find("approximationX").text) else None,
				float(adjustment_element.find("approximationY").text) if adjustment_element.find("approximationY") is not None and self.is_float(adjustment_element.find("approximationY").text) else None,
				int(adjustment_element.find("distRight").text) if adjustment_element.find("distRight") is not None and adjustment_element.find("distRight").text.isdigit() else None,
				int(adjustment_element.find("distFront").text) if adjustment_element.find("distFront") is not None and adjustment_element.find("distFront").text.isdigit() else None,
				int(adjustment_element.find("distAxis").text) if adjustment_element.find("distAxis") is not None and adjustment_element.find("distAxis").text.isdigit() else None
			)
		else:
			return None

	def writeAdjustment(self, adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, distRight, distFront, distAxis):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		adjustment_element = root.find("adjustmentPosition")
		if adjustment_element is None:
			adjustment_element = ET.SubElement(root, "adjustmentPosition")
		
		for key, value in [("adjustX", adjustX), ("adjustY", adjustY), ("adjustZ", adjustZ), ("toleranceX", toleranceX), ("toleranceY", toleranceY), ("approximationX", approximationX), ("approximationY", approximationY), ("distRight", distRight), ("distFront", distFront), ("distAxis", distAxis)]:
			element = adjustment_element.find(key)
			if element is None:
				element = ET.SubElement(adjustment_element, key)
			element.text = str(value)
		
		# Formatieren des XML-Baums vor dem Speichern
		self.format_xml(root)

		# Schreiben der formatierten XML-Daten in die Datei
		tree.write(self.xml_file_path, encoding='utf-8', xml_declaration=True)

	# ---------------------------------------------------------------------------------------------
	# dimensions
	#
	# content of file
	# 		length over all		length of the caravan over all 
	#		width over all		width of the caravan over all
	#		length body			legth of the body of the caravan without drawbar
	# ----------------------------------------------------------------------------------------------

	def readDimensions(self):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		dimensions_element = root.find("dimensionsCaravan")
		if dimensions_element is not None:
			return (
				int(dimensions_element.find("lengthOverAll").text) if dimensions_element.find("lengthOverAll") is not None and dimensions_element.find("lengthOverAll").text.isdigit() else None,
				int(dimensions_element.find("widthOverAll").text) if dimensions_element.find("widthOverAll") is not None and dimensions_element.find("widthOverAll").text.isdigit() else None,
				int(dimensions_element.find("lengthBody").text) if dimensions_element.find("lengthBody") is not None and dimensions_element.find("lengthBody").text.isdigit() else None
			)
		else:
			return None

	def writeDimensions(self, lengthOverAll, widthOverAll, lengthBody):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		dimensions_element = root.find("dimensionsCaravan")
		if dimensions_element is None:
			dimensions_element = ET.SubElement(root, "dimensionsCaravan")
		
		for key, value in [("lengthOverAll", lengthOverAll), ("widthOverAll", widthOverAll), ("lengthBody", lengthBody)]:
			element = dimensions_element.find(key)
			if element is None:
				element = ET.SubElement(dimensions_element, key)
			element.text = str(value)
		
		# Formatieren des XML-Baums vor dem Speichern
		self.format_xml(root)

		# Schreiben der formatierten XML-Daten in die Datei
		tree.write(self.xml_file_path, encoding='utf-8', xml_declaration=True)


	# ---------------------------------------------------------------------------------------------
	# gas scale
	#
	# content of file
	#		empty weight	weight of the empty gas cylinder
	#		full weight		weight of the full gas cylinder
	#       pin_dout		GPIO Pin HX711 DOUT / DT
	# 		pin_sck			GPIO Pin HX711 SCK
	# 		channel			Channel at HX711, only A or B
	# 		refUnit			reference unit as divisor for HX711 values
	#
	# ----------------------------------------------------------------------------------------------

	def readGasScale(self, gasCylinderNumber):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		gas_scale_element = root.find(f"gasScaleDefaults{gasCylinderNumber}")
		
		if gas_scale_element is not None:
			return (
				int(gas_scale_element.find("emptyWeight").text) if gas_scale_element.find("emptyWeight") is not None and gas_scale_element.find("emptyWeight").text.isdigit() else None,
				int(gas_scale_element.find("gasWeightMax").text) if gas_scale_element.find("gasWeightMax") is not None and gas_scale_element.find("gasWeightMax").text.isdigit() else None,
				int(gas_scale_element.find("pin_dout").text) if gas_scale_element.find("pin_dout") is not None and gas_scale_element.find("pin_dout").text.isdigit() else None,
				int(gas_scale_element.find("pin_sck").text) if gas_scale_element.find("pin_sck") is not None and gas_scale_element.find("pin_sck").text.isdigit() else None,
				gas_scale_element.find("strChannel").text if gas_scale_element.find("strChannel") is not None else None,
				float(gas_scale_element.find("refUnit").text) if gas_scale_element.find("refUnit") is not None and self.is_float(gas_scale_element.find("refUnit").text) else None
			)
		else:
			return None

	def writeGasScale(self, gasCylinderNumber, emptyWeight, gasWeightMax, pin_dout, pin_sck, strChannel, refUnit):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		gas_scale_element = root.find(f"gasScaleDefaults{gasCylinderNumber}")
		if gas_scale_element is None:
			gas_scale_element = ET.SubElement(root, f"gasScaleDefaults{gasCylinderNumber}")
		
		# Create or update each configuration item
		for key, value in [("emptyWeight", emptyWeight), ("gasWeightMax", gasWeightMax), ("pin_dout", pin_dout), ("pin_sck", pin_sck), ("strChannel", strChannel), ("refUnit", refUnit)]:
			element = gas_scale_element.find(key)
			if element is None:
				element = ET.SubElement(gas_scale_element, key)
			element.text = str(value)
		
		# Formatieren des XML-Baums vor dem Speichern
		self.format_xml(root)

		# Schreiben der formatierten XML-Daten in die Datei
		tree.write(self.xml_file_path, encoding='utf-8', xml_declaration=True)


	# ---------------------------------------------------------------------------------------------
	# filling levels
	#
	# level 1 is the smallest amount of water, level 4 is the largest amount of water in the tank
	#
	# content of file
	# 		liter level 1		amount of water in the tank at level 1 
	#		liter level 2		amount of water in the tank at level 2
	#		liter level 3		amount of water in the tank at level 3
	#		liter level 4		amount of water in the tank at level 4
	# ----------------------------------------------------------------------------------------------

	def readFillLevels(self, tankNumber):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		tank_element = root.find(f"tankDefaults{tankNumber}")
		if tank_element is not None:
			return (
				float(tank_element.find("level1").text) if tank_element.find("level1") is not None and self.is_float(tank_element.find("level1").text) else None,
				float(tank_element.find("level2").text) if tank_element.find("level2") is not None and self.is_float(tank_element.find("level2").text) else None,
				float(tank_element.find("level3").text) if tank_element.find("level3") is not None and self.is_float(tank_element.find("level3").text) else None,
				float(tank_element.find("level4").text) if tank_element.find("level4") is not None and self.is_float(tank_element.find("level4").text) else None
			)
		else:
			return None

	def writeFillLevels(self, tankNumber, level1, level2, level3, level4):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		tank_element = root.find(f"tankDefaults{tankNumber}")
		if tank_element is None:
			tank_element = ET.SubElement(root, f"tankDefaults{tankNumber}")
		
		# Create or update each configuration item
		for key, value in [("level1", level1), ("level2", level2), ("level3", level3), ("level4", level4)]:
			element = tank_element.find(key)
			if element is None:
				element = ET.SubElement(tank_element, key)
			element.text = str(value)
		
		# Formatieren des XML-Baums vor dem Speichern
		self.format_xml(root)

		# Schreiben der formatierten XML-Daten in die Datei
		tree.write(self.xml_file_path, encoding='utf-8', xml_declaration=True)

	# ---------------------------------------------------------------------------------------------
	# wide Voltage Level
	#
	# level 1 is the smallest amount of voltage, level 3 is the largest amount of voltage
	#
	# content of file
	# 		voltage level 1		 battery 25% 
	#		voltage level 2		 battery 50%
	#		voltage level 3		 Battery 100%
	# ----------------------------------------------------------------------------------------------

	def readVoltageLevels(self):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		voltage_element = root.find("voltageDefaults")
		if voltage_element is not None:
			return (
				float(voltage_element.find("level1").text) if voltage_element.find("level1") is not None and self.is_float(voltage_element.find("level1").text) else None,
				float(voltage_element.find("level2").text) if voltage_element.find("level2") is not None and self.is_float(voltage_element.find("level2").text) else None,
				float(voltage_element.find("level3").text) if voltage_element.find("level3") is not None and self.is_float(voltage_element.find("level3").text) else None
			)
		else:
			return None

	def writeVoltageLevels(self, level1, level2, level3):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		voltage_element = root.find("voltageDefaults")
		if voltage_element is None:
			voltage_element = ET.SubElement(root, "voltageDefaults")
		
		for key, value in [("level1", level1), ("level2", level2), ("level3", level3)]:
			element = voltage_element.find(key)
			if element is None:
				element = ET.SubElement(voltage_element, key)
			element.text = str(value)
		
		# Formatieren des XML-Baums vor dem Speichern
		self.format_xml(root)

		# Schreiben der formatierten XML-Daten in die Datei
		tree.write(self.xml_file_path, encoding='utf-8', xml_declaration=True)


	# =========================================================================================================================================================
	# 
	# Schreiben und Lesen der jeweils aktuellen Sensor Werte
	# 
	# =========================================================================================================================================================


	def handle_sensor_values(self, toScreen, sensor_name, sensor_id, value_identifiers, sensor_values):
		# Funktion zum Verarbeiten der ermittelten Sensorwerte
		# Die Werte werden per print ausgegeben, falls toScreen auf true steht
		# Falls die zentrale Konfig das Schreiben in die MariaDB vorsieht, so wird das angestossen
		# Falls MQTT Messages versandt werden sollen, so wird dies angestossen
		#
		# sensor_values: ein Tupel mit den konkreten Sensorwerten
		# value_identifiers: eine Liste mit den Feldbezeichnern fuer die Sensorwerte.
		

		try:
			# sind beide Listen/Tupel gleich lang?
			if len(sensor_values) != len(value_identifiers):
				raise ValueError(f"Die Tupel fuer Werte ({len(sensor_values)} Elemente: {sensor_values}) und Bezeichner ({len(value_identifiers)} Elemente {value_identifiers}) sind unterschiedlich lang")

			# Bildschirmausgabe
			if toScreen:
				print(f"{datetime.datetime.now():%Y%m%d%H%M%S} - {sensor_name} - {sensor_id}")
				for identifier, value in zip(value_identifiers, sensor_values):
					print(f"{identifier}: {value}")

			# Schreiben in die Datei
			if self.write2file:
				print("Datei schreiben")
				self.write_to_file(sensor_id, sensor_values)

			# Schreiben in die MariaDB
			if self.write2MariaDB:
				print("Datenbank schreiben")

				# Datenbank oeffnen
				connection = self.create_db_connection()

				# Daten in die Tabelle schreiben
				table_columns = ['sensor_id', 'zeitstempel']
				table_values = (sensor_id, None)
				self.insert_into_table(connection, sensor_name, table_columns + value_identifiers, table_values + sensor_values)
				
				# Datenbank schliessen
				connection.close()

			if self.send2MQTT:
				print("senden an MQTT")

				# MQTT Connection oeffnen
				client = self.create_mqtt_connection()

				# Daten versenden
				self.send_mqtt_messages(client, sensor_name, sensor_id, value_identifiers, sensor_values)
				
				# Datenbank schliessen
				client.disconnect()

			return 0
		except Error as e:
			# Fehler
			print ("ERROR - Die Sensordaten konnten nicht geschrieben/gesendet werden: Fehler: '{e}'")
			return -1
			



	# =========================================================================================================================================================
	# 
	# Ausgabe in die Werte Datei
	# 
	# =========================================================================================================================================================

	# ---------------------------------------------------------------------------------------------
	# write_to_file
	# Schreiben der Sensorwerte in eine Datei
	# ----------------------------------------------------------------------------------------------
	def write_to_file(self, filename, sensor_values):
		# Vollstaendiger Dateipfad
		file_path = os.path.join(self.values_file_path, filename)

		# Erstellen des Zeitstempels
		timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

		# Erstellen der Zeile fuer die Ausgabe
		output_line = f"{filename} {timestamp} " + " ".join(map(str, sensor_values)) + "\n"

		# Schreiben in die Datei
		with open(file_path, 'a') as file:
			file.write(output_line)


	# =========================================================================================================================================================
	# 
	# Datenbank Funktionen MariaDB
	# 
	# =========================================================================================================================================================

	# ---------------------------------------------------------------------------------------------
	# create_db_connection
	# Datenbank Verbindung aufbauen
	# ----------------------------------------------------------------------------------------------

	def create_db_connection(self):
		# zunächst die Defaultwerte in der Default xml lesen
		self.update_settings()

		connection = None
		try:
			connection = mysql.connector.connect(
				host=self.MariaDBhost,
				user=self.MariaDBuser,
				passwd=self.MariaDBpasswd,
				database=self.MariaDBdatabase
			)
		except Error as e:
			print(f"ERROR - MariaDB - Fehler aufgetreten: '{e}'")

		return connection

	# ---------------------------------------------------------------------------------------------
	# execute_query
	# beliebige SQL Querys ausführen
	# ----------------------------------------------------------------------------------------------

	def execute_query(self, connection, query, data):
		cursor = connection.cursor()
		try:
			cursor.execute(query, data)
			connection.commit()
			print("Query successful")
		except Error as e:
			print(f"ERROR - MariaDB - Fehler aufgetreten: '{e}'")

	# ---------------------------------------------------------------------------------------------
	# insert_into_table
	# Einfügen von Daten in eine beliebige Tabelle
	# Struktur und Werte werden als Tupel übergeben
	# Achtung: Falls eine Spalte zeitstempel in columns vorkommt, wird automatisch CURRENT_TIMESTAMP eingefügt.
	#          in diesem Fall muss schon beim Aufruf an der richtigen Stelle in values ein Wert, z.B. none, vorhanden sein
	# ----------------------------------------------------------------------------------------------

	def insert_into_table(self, connection, table_name, columns, values):
		# Stellen Sie sicher, dass Subtopics und Values die gleiche Länge haben
		if len(columns) != len(values):
			raise ValueError("Spalten und Values müssen die gleiche Anzahl von Elementen haben.")

		# Überprüfen, ob 'zeitstempel' in den Spalten ist und CURRENT_TIMESTAMP einsetzen
		timestamp_index = None
		if "zeitstempel" in columns:
			timestamp_index = columns.index("zeitstempel")
			columns = [col for col in columns if col != "zeitstempel"]  # 'zeitstempel' aus den Spalten entfernen
			values = tuple(value for i, value in enumerate(values) if i != timestamp_index)  # entsprechenden Wert entfernen

		# Erstellen der SQL-Abfrage
		columns_string = ', '.join(columns + (["zeitstempel"] if timestamp_index is not None else []))
		values_string = ', '.join(['%s'] * len(values) + (["CURRENT_TIMESTAMP"] if timestamp_index is not None else []))
		query = f"INSERT INTO {table_name} ({columns_string}) VALUES ({values_string})"

		# Ausführen der Abfrage
		self.execute_query(connection, query, values)


	# =========================================================================================================================================================
	# 
	# MQTT Funktionen
	# 
	# =========================================================================================================================================================

	# ---------------------------------------------------------------------------------------------
	# create_mqtt_connection
	# MQTT Verbindung aufbauen
	# ----------------------------------------------------------------------------------------------

	def create_mqtt_connection(self):
		# zunächst die Defaultwerte in der Default xml lesen
		self.update_settings()

		client = None
		try:
			client = mqtt.Client()
			client.tls_set()  # Aktiviere TLS ohne spezifische Zertifikate
			client.username_pw_set(self.MQTTuser,self.MQTTpassword)
			client.connect(self.MQTTbroker, self.MQTTport, 60)

			print("MQTT connection successful")

		except Error as e:
			print(f"ERROR - MQTT - Fehler aufgetreten: '{e}'")

		return client

	# ---------------------------------------------------------------------------------------------
	# send_mqtt_messages
	# Senden von Daten an einen MQTT Broker
	# Struktur und Werte werden als Tupel übergeben
	# ----------------------------------------------------------------------------------------------

	def send_mqtt_messages(self, mqtt_client, typtopic, sensortopic, subtopics, values):
		base_topic = "CaravanPi"

		# Stellen Sie sicher, dass Subtopics und Values die gleiche Länge haben
		if len(subtopics) != len(values):
			raise ValueError("Subtopics und Values müssen die gleiche Anzahl von Elementen haben.")

		# Senden jeder Nachricht
		for subtopic, value in zip(subtopics, values):
			topic = f"{base_topic}/{typtopic}" + (f"/{sensortopic}" if sensortopic else "") + f"/{subtopic}"
			mqtt_client.publish(topic, value)
			print("MQTT send successful", topic, value)


	# =========================================================================================================================================================
	# COMPATIBILITY CODE - Anfang bis Dateiende
	# =========================================================================================================================================================

	# Mapping for caravanpiDefaults file
	mappings = {
		"caravanpiDefaults": [
			"countGasScales", 
			"countTanks", 
		],
		"adjustmentPosition": [
			"adjustX", 
			"adjustY", 
			"adjustZ", 
			"toleranceX", 
			"toleranceY", 
			"approximationX", 
			"approximationY", 
			"distRight", 
			"distFront", 
			"distAxis"
		],
		"dimensionsCaravan": [
			"lengthOverAll", 
			"widthOverAll", 
			"lengthBody"
		],
		"gasScaleDefaults": [
			"emptyWeight", 
			"gasWeightMax", 
			"pin_dout", 
			"pin_sck", 
			"strChannel", 
			"refUnit"
		],
		"tankDefaults": [
			"level1", 
			"level2", 
			"level3", 
			"level4"
		],
		"voltageDefaults": [
			"level1", 
			"level2", 
			"level3"
		],
		"testColor": [
			"color"
		]
	}

	# ---------------------------------------------------------------------------------------------
	# check_create_xml
	# Prüfen, ob es schon ein xml File gibt. Falls nein, dieses anlegen.
	# ----------------------------------------------------------------------------------------------
	def check_create_xml(self):
		# Create XML file if it doesn't exist
		if not os.path.exists(self.xml_file_path):
			root = ET.Element("CaravanPiConfigurations")
			tree = ET.ElementTree(root)
			tree.write(self.xml_file_path)

	# ---------------------------------------------------------------------------------------------
	# migrate_old_configs
	# Ueberfuehren der alten Konfigurationsdateien in das neue xml File.
	# ----------------------------------------------------------------------------------------------
	def migrate_old_configs(self):
		# List of old configuration files
		old_files = [
			"/home/pi/CaravanPi/defaults/caravanpiDefaults",
			"/home/pi/CaravanPi/defaults/adjustmentPosition",
			"/home/pi/CaravanPi/defaults/dimensionsCaravan",
			"/home/pi/CaravanPi/defaults/gasScaleDefaults1",
			"/home/pi/CaravanPi/defaults/gasScaleDefaults2",
			"/home/pi/CaravanPi/defaults/gasScaleDefaults3",
			"/home/pi/CaravanPi/defaults/gasScaleDefaults4",
			"/home/pi/CaravanPi/defaults/tankDefaults1",
			"/home/pi/CaravanPi/defaults/tankDefaults2",
			"/home/pi/CaravanPi/defaults/tankDefaults3",
			"/home/pi/CaravanPi/defaults/tankDefaults4",
			"/home/pi/CaravanPi/defaults/voltageDefaults",
			"/home/pi/CaravanPi/defaults/testColor",
		]
		for file in old_files:
			if os.path.exists(file):
				self.migrate_file(file)

	# ---------------------------------------------------------------------------------------------
	# migrate_file
	# Ueberfuehren einer alten Konfigurationsdatei
	# ----------------------------------------------------------------------------------------------

	def migrate_file(self, file_path):
		# Check if the file exists, if not, exit the function
		if not os.path.exists(file_path):
			print(f"File not found: {file_path}")
			return

		# Extract the base name and number (if any) from the file name
		file_name = os.path.basename(file_path)
		# Assuming the number is at the end of the file name and is one digit
		if file_name[-1].isdigit():
			base_name = file_name[:-1]
			number = file_name[-1]
		else:
			base_name = file_name
			number = ""

		# Create "_alt" directory if it does not exist
		alt_dir = os.path.join(os.path.dirname(file_path), "_alt")
		if not os.path.exists(alt_dir):
			os.makedirs(alt_dir)

		# Spezialfall fuer caravanpiDefaults, da diese Ueberschriften enthaelt
		if base_name == "caravanpiDefaults":
			self.migrate_caravanpi_defaults(file_path)
			return

		# Choose the mapping based on the base name
		mapping = self.mappings.get(base_name, [])

		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		# Adjust the XML element name to include the number for gasScaleDefaults and tankDefaults
		config_element_name = f"{base_name}{number}" if number else base_name
		config_element = ET.SubElement(root, config_element_name)

		with open(file_path, 'r') as file:
			for index, line in enumerate(file):
				value = line.strip()
				key = mapping[index] if index < len(mapping) else f"unknown{index}"
				ET.SubElement(config_element, key).text = value

		tree.write(self.xml_file_path)

		# Move the original file to the "_alt" directory
		shutil.move(file_path, os.path.join("/home/pi/CaravanPi/defaults/_alt", os.path.basename(file_path)))


	def migrate_caravanpi_defaults(self, file_path):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		defaults_element = ET.SubElement(root, "caravanpiDefaults")

		with open(file_path, 'r') as file:
			for line in file:
				line = line.strip()
				if "Anzahl Waagen" in line:
					key = "countGasScales"
					continue  # Skip to the next iteration to read the value
				elif "Anzahl Tanks" in line:
					key = "countTanks"
					continue  # Skip to the next iteration to read the value
				elif line:  # Check if line is not empty
					ET.SubElement(defaults_element, key).text = line

		# Setting additional fields to empty or false
		for additional_key in ["write2file"]:
			ET.SubElement(defaults_element, additional_key).text = "1"

		for additional_key in ["write2MariaDB", "send2MQTT"]:
			ET.SubElement(defaults_element, additional_key).text = "0"

		for additional_key in ["MariaDBhost", "MariaDBuser", "MariaDBpasswd", "MariaDBdatabase", "MQTTbroker", "MQTTport", "MQTTuser", "MQTTpassword"]:
			ET.SubElement(defaults_element, additional_key).text = ""

		tree.write(self.xml_file_path)
		shutil.move(file_path, os.path.join(os.path.dirname(file_path), "/home/pi/CaravanPi/defaults/_alt", os.path.basename(file_path)))
		
