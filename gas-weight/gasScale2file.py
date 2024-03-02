#!/usr/bin/python
# coding=utf-8
# gasweight2file.py
#
# liest die Gaswaage ein und schreibt den Wert in eine Datei
#
#-------------------------------------------------------------------------------

import sys
import datetime
import RPi.GPIO as GPIO
import argparse

# -----------------------------------------------
# Sensoren libraries aus CaravanPi einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from hx711 import HX711
from CaravanPiFilesClass import CaravanPiFiles


def clean():
	print("Cleaning...")
	GPIO.cleanup()

def main():
	# -------------------------
	# main 
	# -------------------------

	# -------------------------
	# process call parameters
	# -------------------------
	args = []
	gasCylinderNumber = 1
	tare = 0
	emptyWeight = 0
	gasWeightMax = 0

	# ArgumentParser-Objekt erstellen
	parser = argparse.ArgumentParser(description='Lesen der Gasflaschenwaage und Verarbeiten der Sensorwerte')
	parser.add_argument('-g', '--gasscale', type=str, choices=['1', '2'], default='1',
						help='Nr der Gasflaschenwaage (1 (default) oder 2)')
	parser.add_argument('-s', '--screen', action='store_true',
						help='ausgeben am Bildschirm')
	parser.add_argument('-c', '--check', action='store_true', 
						help='Führt den Funktionstest der Gasflaschenwaage aus')

	# Argumente parsen
	args = parser.parse_args()
	
	gasCylinderNumber = int(args.gasscale)

	# -------------------------
	# gpio warnings off
	# -------------------------
	GPIO.setwarnings(False)

	# Erstellen der Instanzen der Librarys
	cplib = CaravanPiFiles()

	# -------------------------
	# read defaults
	# -------------------------
	(emptyWeight, gasWeightMax, pin_dout, pin_sck, channel, refUnit) = cplib.readGasScale(gasCylinderNumber)

	if args.screen:
		print ("bisherige Werte:")
		print ("Leergewicht Flasche: ", emptyWeight)
		print ("max. Gas-Gewicht: ", gasWeightMax)
		print ("Pin DOUT: ", pin_dout)
		print ("Pin SCK: ", pin_sck)
		print ("Channel: ", channel)
		print ("Reference Unit: ", refUnit)

	# Erstellen der Instanzen der Librarys
	hxlib = HX711(pin_dout, pin_sck)

	try:
		if hxlib.error_status:
			raise RuntimeError("Fehler bei der Initialisierung des HX711")

		if args.check:
			# kein Fehler
			clean()
			return 0

		hxlib.set_reading_format("MSB", "MSB")

		if channel == "A":
			hxlib.set_reference_unit_A(refUnit)
		elif channel == "B":
			hxlib.set_reference_unit_B(refUnit)
		else:
			print("invalid HX711 channel: ", channel)		
			print("set channel to A")
			channel = "A"		
			hxlib.set_reference_unit_A(refUnit)

		hxlib.reset()

		# read sensor
		if channel == "B":
			weight = hxlib.get_weight_B(5)
		else:
			weight = hxlib.get_weight_A(5)

		if (weight<0):
			weight=weight*(-1)

		nettoWeight = weight - tare - emptyWeight
		nettoLevel = (nettoWeight/gasWeightMax) * 100

		# Werte schreiben bzw. senden
		cplib.handle_sensor_values(
			args.screen,							# Anzeige am Bildschirm?
			"gasfuellgrad",							# sensor_name = Datenbankname
			f"gasscale-{gasCylinderNumber:.0f}",		# sensor_id = Filename und Spalte in der Datenbank
			["gewicht", "fuellgrad",],				# Liste Spaltennamen
			(float(nettoWeight), float(nettoLevel),)			# Tupel Sensorwerte
		)

	except RuntimeError as e:
		print(f"ERROR - HX711 - Initialisierungsfehler: {e}")
		clean()
		return 1
	
	except Error as e:
		print(f"ERROR - HX711 - anderer Fehler: {e}")
		clean()
		return 1
	
	clean()
	return 0


if __name__=="__main__":
	result = main()
	sys.exit(result)