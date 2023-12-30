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
import xml.dom.minidom

class CaravanPiFiles:

	# -----------------------------------------------
	# global variables
	# -----------------------------------------------

	xml_file_path = "/home/pi/CaravanPi/defaults/caravanpiConfig.xml"

	# -----------------------------------------------
	# COMPATIBILITY CODE - Anfang
	# -----------------------------------------------
	# Mapping for caravanpiDefaults file
	mappings = {
		"caravanpiDefaults": [
			"countGasScales", 
			"countTanks", 
			"write2MariaDB", 
			"send2MQTT", 
			"MQTTserver", 
			"MQTTport", 
			"MQTTuser", 
			"MQTTpassword", 
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
			"fullWeight", 
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
	# -----------------------------------------------
	# COMPATIBILITY CODE - Ende
	# -----------------------------------------------

	def __init__(self):
		# COMPATIBILITY CODE - Pruefen, ob alte Dateien in das xml File migriert werden muessen
		self.check_create_xml()
		self.migrate_old_configs()

	def format_xml(element, level=0):
		indent = "\n" + level*"  "
		if len(element):
			if not element.text or not element.text.strip():
				element.text = indent + "  "
			if not element.tail or not element.tail.strip():
				element.tail = indent
			for elem in element:
				format_xml(elem, level+1)
			if not elem.tail or not elem.tail.strip():
				elem.tail = indent
		else:
			if level and (not element.tail or not element.tail.strip()):
				element.tail = indent

	# ---------------------------------------------------------------------------------------------
	# CaravanPiDefaults
	#
	# meaning of data fields
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

	def readCaravanPiDefaults(self):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		defaults_element = root.find("caravanpiDefaults")
		if defaults_element is not None:
			return (
				defaults_element.find("countGasScales").text if defaults_element.find("countGasScales") is not None else None,
				defaults_element.find("countTanks").text if defaults_element.find("countTanks") is not None else None,
				defaults_element.find("write2MariaDB").text if defaults_element.find("write2MariaDB") is not None else None,
				defaults_element.find("send2MQTT").text if defaults_element.find("send2MQTT") is not None else None,
				defaults_element.find("MQTTserver").text if defaults_element.find("MQTTserver") is not None else None,
				defaults_element.find("MQTTport").text if defaults_element.find("MQTTport") is not None else None,
				defaults_element.find("MQTTuser").text if defaults_element.find("MQTTuser") is not None else None,
				defaults_element.find("MQTTpassword").text if defaults_element.find("MQTTpassword") is not None else None
			)
		else:
			return None

	def writeCaravanPiDefaults(self, countGasScales, countTanks, write2MariaDB, send2MQTT, MQTTserver, MQTTport, MQTTUser, MQTTpassword):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		defaults_element = root.find("caravanpiDefaults")
		if defaults_element is None:
			defaults_element = ET.SubElement(root, "caravanpiDefaults")
		
		for key, value in [("countGasScales", countGasScales), ("countTanks", countTanks), ("write2MariaDB", write2MariaDB), ("send2MQTT", send2MQTT), ("MQTTserver", MQTTserver), ("MQTTport", MQTTport), ("MQTTUser", MQTTUser), ("MQTTpassword", MQTTpassword)]:
			element = defaults_element.find(key)
			if element is None:
				element = ET.SubElement(defaults_element, key)
			element.text = str(value)
		
		# Formatieren des XML-Baums vor dem Speichern
		format_xml(root)

		# Schreiben der formatierten XML-Daten in die Datei
		tree.write(self.xml_file_path)

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
				adjustment_element.find("adjustX").text if adjustment_element.find("adjustX") is not None else None,
				adjustment_element.find("adjustY").text if adjustment_element.find("adjustY") is not None else None,
				adjustment_element.find("adjustZ").text if adjustment_element.find("adjustZ") is not None else None,
				adjustment_element.find("toleranceX").text if adjustment_element.find("toleranceX") is not None else None,
				adjustment_element.find("toleranceY").text if adjustment_element.find("toleranceY") is not None else None,
				adjustment_element.find("approximationX").text if adjustment_element.find("approximationX") is not None else None,
				adjustment_element.find("approximationY").text if adjustment_element.find("approximationY") is not None else None,
				adjustment_element.find("distRight").text if adjustment_element.find("distRight") is not None else None,
				adjustment_element.find("distFront").text if adjustment_element.find("distFront") is not None else None,
				adjustment_element.find("distAxis").text if adjustment_element.find("distAxis") is not None else None
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
		format_xml(root)

		# Schreiben der formatierten XML-Daten in die Datei
		tree.write(self.xml_file_path)

	# ---------------------------------------------------------------------------------------------
	# dimensions
	#
	# content of file
	# 		length over all		length of the caravan over all 
	#		width				width of the caravan over all
	#		length body			legth of the body of the caravan without drawbar
	# ----------------------------------------------------------------------------------------------

	def readDimensions(self):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		dimensions_element = root.find("dimensionsCaravan")
		if dimensions_element is not None:
			return (
				dimensions_element.find("lengthOverAll").text if dimensions_element.find("lengthOverAll") is not None else None,
				dimensions_element.find("width").text if dimensions_element.find("width") is not None else None,
				dimensions_element.find("lengthBody").text if dimensions_element.find("lengthBody") is not None else None
			)
		else:
			return None

	def writeDimensions(self, lengthOverAll, width, lengthBody):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		dimensions_element = root.find("dimensionsCaravan")
		if dimensions_element is None:
			dimensions_element = ET.SubElement(root, "dimensionsCaravan")
		
		for key, value in [("lengthOverAll", lengthOverAll), ("width", width), ("lengthBody", lengthBody)]:
			element = dimensions_element.find(key)
			if element is None:
				element = ET.SubElement(dimensions_element, key)
			element.text = str(value)
		
		# Formatieren des XML-Baums vor dem Speichern
		format_xml(root)

		# Schreiben der formatierten XML-Daten in die Datei
		tree.write(self.xml_file_path)


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
				gas_scale_element.find("emptyWeight").text if gas_scale_element.find("emptyWeight") is not None else None,
				gas_scale_element.find("fullWeight").text if gas_scale_element.find("fullWeight") is not None else None,
				gas_scale_element.find("pin_dout").text if gas_scale_element.find("pin_dout") is not None else None,
				gas_scale_element.find("pin_sck").text if gas_scale_element.find("pin_sck") is not None else None,
				gas_scale_element.find("strChannel").text if gas_scale_element.find("strChannel") is not None else None,
				gas_scale_element.find("refUnit").text if gas_scale_element.find("refUnit") is not None else None
			)
		else:
			return None

	def writeGasScale(self, gasCylinderNumber, test, screen, emptyWeight, fullWeight, pin_dout, pin_sck, strChannel, refUnit):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		gas_scale_element = root.find(f"gasScaleDefaults{gasCylinderNumber}")
		if gas_scale_element is None:
			gas_scale_element = ET.SubElement(root, f"gasScaleDefaults{gasCylinderNumber}")
		
		# Create or update each configuration item
		for key, value in [("emptyWeight", emptyWeight), ("fullWeight", fullWeight), ("pin_dout", pin_dout), ("pin_sck", pin_sck), ("strChannel", strChannel), ("refUnit", refUnit)]:
			element = gas_scale_element.find(key)
			if element is None:
				element = ET.SubElement(gas_scale_element, key)
			element.text = str(value)
		
		# Formatieren des XML-Baums vor dem Speichern
		format_xml(root)

		# Schreiben der formatierten XML-Daten in die Datei
		tree.write(self.xml_file_path)


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
				tank_element.find("level1").text if tank_element.find("level1") is not None else None,
				tank_element.find("level2").text if tank_element.find("level2") is not None else None,
				tank_element.find("level3").text if tank_element.find("level3") is not None else None,
				tank_element.find("level4").text if tank_element.find("level4") is not None else None
			)
		else:
			return None

	def writeFillLevels(self, tankNumber, test, screen, level1, level2, level3, level4):
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
		format_xml(root)

		# Schreiben der formatierten XML-Daten in die Datei
		tree.write(self.xml_file_path)

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
				voltage_element.find("level1").text if voltage_element.find("level1") is not None else None,
				voltage_element.find("level2").text if voltage_element.find("level2") is not None else None,
				voltage_element.find("level3").text if voltage_element.find("level3") is not None else None
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
		format_xml(root)

		# Schreiben der formatierten XML-Daten in die Datei
		tree.write(self.xml_file_path)


	# ---------------------------------------------------------------------------------------------
	# testColor
	#
	# content of file
	# 		color			Color to show for testing LEDs 
	# ----------------------------------------------------------------------------------------------

	def readTestColor(self):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		test_color_element = root.find("testColor")
		if test_color_element is not None:
			return test_color_element.find("color").text if test_color_element.find("color") is not None else None
		else:
			return None

	def writeTestColor(self, color):
		tree = ET.parse(self.xml_file_path)
		root = tree.getroot()
		test_color_element = root.find("testColor")
		if test_color_element is None:
			test_color_element = ET.SubElement(root, "testColor")
		
		color_element = test_color_element.find("color")
		if color_element is None:
			color_element = ET.SubElement(test_color_element, "color")
		color_element.text = str(color)
		
		# Formatieren des XML-Baums vor dem Speichern
		format_xml(root)

		# Schreiben der formatierten XML-Daten in die Datei
		tree.write(self.xml_file_path)


	# -----------------------------------------------
	# COMPATIBILITY CODE - Anfang bis Dateiende
	# -----------------------------------------------

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

		# Setting additional fields to empty
		for additional_key in ["write2MariaDB", "send2MQTT", "MQTTserver", "MQTTport", "MQTTuser", "MQTTpassword"]:
			ET.SubElement(defaults_element, additional_key).text = ""

		tree.write(self.xml_file_path)
		shutil.move(file_path, os.path.join(os.path.dirname(file_path), "/home/pi/CaravanPi/defaults/_alt", os.path.basename(file_path)))
		
