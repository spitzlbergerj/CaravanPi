#!/usr/bin/python3
# coding=utf-8
# gasScaleCalibration.py
#
# Ermitteln der refUnit, der Kalibrierungsgröße, des HX711, so dass anschließend zuverlässig das anliegende Gewicht ermittelt werden kann
#
# Aufruf-Parameter
# setupGasscaleDefaults.py -h -t -s -w <seconds>
# 	-e	Testgewicht in Gramm
#   -g  Nummer der Gasflaschen Waage
# 	-s	Ausgabe von Infos am Bildschirm 
#	-w  Wartezeit bevor die Kalibrierung startet
#
# 2024-02-19, Josef Spitzlberger
# Anpassungen, da die Kalibrierung keine zuverlässigen Werte brachte
# -------------------------------------------------------------------------------

import sys
from time import sleep
import argparse

# -------------------------------------------------------------------------------
# libraries from CaravanPi 
# -------------------------------------------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from hx711 import HX711
from CaravanPiFilesClass import CaravanPiFiles


# -------------------------------------------------------------------------------
# main 
# -------------------------------------------------------------------------------

def main():

	# -------------------------------------------------------------------------------
	# Verarbeiten der Aufrufparameter
	# -------------------------------------------------------------------------------

	parser = argparse.ArgumentParser(description='Kalibrierung der Gaswaagen')

	# Argumente definieren
	parser.add_argument('-e', '--weight', type=float, default=1, help='Testgewicht auf der Waage in Gramm (default leere Waage)')
	parser.add_argument('-g', '--gasscale', type=int, default=1, help='Nummer der Gaswaage (default 1)')
	parser.add_argument('-s', '--screen', action='store_true', help='Werte am Bildschirm anzeigen')
	parser.add_argument('-w', '--wait', type=int, default=0, help='Wartezeit bis zur Kalibrierung in Sekunden (default 0 Sekunden)')

	args = parser.parse_args()
	
	# -------------------------------------------------------------------------------
	# Prüfung und Anpassung von weight
	# Das Testgewicht wird nachher für eine Division benötigt. Daher darf es nicht 0 sein
	# -------------------------------------------------------------------------------
	if args.weight == 0:
		args.weight = 1

	cplib = CaravanPiFiles()

	# -------------------------------------------------------------------------------
	# Lesen der Defaultwerte aus der Config Datei
	# -------------------------------------------------------------------------------
	(emptyWeight, gasWeightMax, pin_dout, pin_sck, channel, refUnit) = cplib.readGasScale(args.gasscale)
	
	if args.screen:
		print("Die Kalibrierung wird gestartet ....")
		print("... vorbereiten der Wägezelle und des HX711 ...")
	
	# test GPIO Pins
	if pin_dout == 0 or pin_sck == 0:
		if args.screen:
			print("GPIO Pins des HX711 sind nicht richtig gesetzt")
			print("PIN DOUT: ", pin_dout)
			print("PIN SCK: ", pin_sck)
			print("ABBRUCH")
		exit(-1)


	# -------------------------------------------------------------------------------
	# Sensor initialisieren
	# -------------------------------------------------------------------------------
	hx711 = HX711(pin_dout, pin_sck)

	# -------------------------------------------------------------------------------
	# setzen der Leserichtung der RAW Daten. MSB ist default für beides
	# -------------------------------------------------------------------------------
	hx711.set_reading_format("MSB", "MSB")

	if args.screen:
		print("... setzen des Referenzwertes auf 1 ...")
	
	if channel == "A":
		hx711.set_reference_unit_A(1)
	elif channel == "B":
		hx711.set_reference_unit_B(1)
	else:
		print("invalid HX711 channel: ", channel)		
		print("set channel to A")
		channel = "A"		
		hx711.set_reference_unit_A(1)

	hx711.reset()
	
	# Wait if there was a waiting time parameter
	i=0
	if args.screen:
		print("... warten, um Schwingungen zu vermeiden ...")

	while i < args.wait:
		sleep(1)
		i+=1
	
	if args.screen:
		print("... mehrmaliges Wiegen des Testgewichts ...")

	# read sensor
	if channel == "B":
		weight = hx711.get_weight_B(19)
	else:
		weight = hx711.get_weight_A(19)

	if args.screen:
		print(f"... für das Testgewichts von {args.weight} Gramm wurde ein Referenzwert von {weight} ermittelt ...")

	refUnit = weight / args.weight

	if args.screen:
		print("... daraus ergibt sich ein Referenzwert von ", refUnit, " ...")
		print("... setzen des Referenzwertes auf ", refUnit, " ...")

	if channel == "B":
		hx711.set_reference_unit_B(refUnit)
	else:
		hx711.set_reference_unit_A(refUnit)

	hx711.reset()

	if args.screen:
		print("... erneutes mehrmaliges Wiegen des Testgewichts ...")

	# read sensor
	if channel == "B":
		weight = hx711.get_weight_B(5)
	else:
		weight = hx711.get_weight_A(5)
	
	if args.screen:
		print(f"... für das Testgewichts von {args.weight} Gramm wurde nun ein Gewicht von {weight} Gramm ermittelt ...")
		print("... der neue Referenzwert wird in die Default Datei geschrieben ...")

	# write new defaults
	cplib.writeGasScale(args.gasscale, emptyWeight, gasWeightMax, pin_dout, pin_sck, channel, refUnit)
	
	
	# cleanup GPIO
	hx711.GPIOcleanup()

	return 0

if __name__ == "__main__":
	main()
