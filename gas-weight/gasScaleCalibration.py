#!/usr/bin/python3
# coding=utf-8
# gasScaleCalibration.py
#
# explore default value for the gas scale sensor
# (reference unit) and write it to the defaults file
#
# Aufruf-Parameter
# setupGasscaleDefaults.py -h -t -s -w <seconds>
# 	-c	display html code
# 	-e	test weight
#   -g  gasscalecylinder number
# 	-h	display guide 
# 	-s	display values on screen 
# 	-t	write values to a separate testfile 
#	-w seconds
#-------------------------------------------------------------------------------

import time, datetime
import statistics
import signal
import sys
from time import sleep
import os
import getopt

# -----------------------------------------------
# libraries from CaravanPi 
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from hx711 import HX711
from CaravanPiFilesClass import CaravanPiFiles

# -------------------------
# call options 
# -------------------------
shortOptions = 'ce:hg:stw:'
longOptions = ['code', 'weight=', 'help', 'gasscale=', 'screen', 'test', 'wait=']

def usage():
	print ("---------------------------------------------------------------------")
	print (sys.argv[0], "-h -g <nr> -t -s -w <sec>")
	print ("  -c          display Values with html-code")
	print ("  -e gramm    test weigth in gramm")
	print ("  -h          show this guide")
	print ("  -g nr       number of gas scale cylinder (default 1)\n")
	print ("  -s          display values on this screen")
	print ("  -t          write values not to origin file but to a testfile")
	print ("  -w seconds  waiting time until the values are read out from the sensor (default 0 seconds)\n")


def main():
	# -------------------------
	# main 
	# -------------------------

	# -------------------------
	# process call parameters
	# -------------------------
	opts = []
	args = []
	writeTestFile = 0
	displayScreen = 0
	displayCode = 0
	calibrationWait = 0 # seconds
	gasCylinderNumber = 1
	testgewicht = 1
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], shortOptions, longOptions)
	except getopt.GetoptError:
		print("ERROR: options not correct")
		usage()
		sys.exit()
	
	for o, a in opts:
		if o == "--code" or o == "-c":
			displayCode = 1
		elif o == "--help" or o == "-h":
			print("HELP")
			usage()
			sys.exit()
		elif o == "--gasscale" or o == "-g":
			gasCylinderNumber = int(a)
		elif o == "--screen" or o == "-s":
			print("output also to this screen")
			displayScreen = 1
		elif o == "--test" or o == "-t":
			writeTestFile = 1
		elif o == "--weight" or o == "-e":
			testgewicht = int(a)
		elif o == "--wait" or o == "-w":
			calibrationWait = int(a)

	for a in args:
		print("further argument: ", a)
		
	# read defaults
	(emptyWeight, fullWeight, pin_dout, pin_sck, channel, refUnit) = CaravanPiFiles.readGasScale(gasCylinderNumber)
	
	if displayScreen == 1:
		print("Die Kalibrierung wird gestartet ....")
		print("... vorbereiten der Wägezelle und des HX711 ...")
	
	if displayCode == 1:
		print("Content-Type: text/html; charset=utf-8\n\n")
		print("<html>")
		print("<head>")
		print("<title>CaravanPi Konfiguration</title>")
		print("<meta http-equiv='refresh' content='20; URL=gas-scale.php'>")
		print("<link rel='stylesheet' type='text/css' href='css/main.css'>")
		print("<link rel='stylesheet' type='text/css' href='css/custom.css'>")
		print("</head>")
		print("<body>")
		print('<header class="header">CaravanPi Konfiguration - Kalibrirung der Waage f&uuml;r Gasflasche ', gasCylinderNumber,'</header>')
		print("Die Kalibrierung wird gestartet ....<br/><br/>")
		print("... vorbereiten der W&auml;gezelle und des HX711 ...<br/>")

	# test GPIO Pins
	if pin_dout == 0 or pin_sck == 0:
		if displayCode == 1:
			print("GPIO Pins des HX711 sind nicht richtig gesetzt<br/>")
			print("PIN DOUT: ", pin_dout, "<br/>")
			print("PIN SCK: ", pin_sck, "<br/>")
			print("ABBRUCH<br/>")
			print("<br/><br/>Sie werden in K&uuml;rze zur Eingabeseite weitergeleitet")
			print("</body>")
			print("</html>")
		if displayScreen == 1:
			print("GPIO Pins des HX711 sind nicht richtig gesetzt")
			print("PIN DOUT: ", pin_dout)
			print("PIN SCK: ", pin_sck)
			print("ABBRUCH")
		exit(-1)


	# start sensor
	hx = HX711(pin_dout, pin_sck)
	hx.set_reading_format("MSB", "MSB")

	if displayScreen == 1:
		print("... setzen des Referenzwertes auf 1 ...")
	
	if displayCode == 1: 
		print("... setzen des Referenzwertes auf 1 ...<br/>")

	if channel == "A":
		hx.set_reference_unit_A(1)
	elif channel == "B":
		hx.set_reference_unit_B(1)
	else:
		print("invalid HX711 channel: ", channel)		
		print("set channel to A")
		channel = "A"		
		hx.set_reference_unit_A(1)

	hx.reset()
	
	# Wait if there was a waiting time parameter
	i=0
	while i < calibrationWait:
		sleep(1)
		i+=1
	
	if displayScreen == 1:
		print("... mehrmaliges Wiegen des Testgewichts ...")

	if displayCode == 1: 
		print("... mehrmaliges Wiegen des Testgewichts ...<br/><br/>")

	# read sensor
	if channel == "B":
		weight = hx.get_weight_B(19)
	else:
		weight = hx.get_weight_A(19)

	if displayScreen == 1:
		print("... für das Testgewichts von ",testgewicht, " Gramm wurde ein Referenzwert von ", weight ," ermittelt ...")

	if displayCode == 1: 
		print("... f&uuml;r das Testgewichts von ",testgewicht, " Gramm wurde ein Referenzwert von ", weight ," ermittelt ...<br/>")

	refUnit = weight / testgewicht

	if displayScreen == 1:
		print("... daraus ergibt sich ein Referenzwert von ", refUnit, " ...")
		print("... setzen des Referenzwertes auf ", refUnit, " ...")

	if displayCode == 1: 
		print("... daraus ergibt sich ein Referenzwert von ", refUnit, " ...<br/><br/>")
		print("... setzen des Referenzwertes auf ", refUnit, " ...<br/>")

	if channel == "B":
		hx.set_reference_unit_B(refUnit)
	else:
		hx.set_reference_unit_A(refUnit)

	hx.reset()

	if displayScreen == 1:
		print("... erneutes mehrmaliges Wiegen des Testgewichts ...")

	if displayCode == 1: 
		print("... erneutes mehrmaliges Wiegen des Testgewichts ...<br/><br/>")

	# read sensor
	if channel == "B":
		weight = hx.get_weight_B(5)
	else:
		weight = hx.get_weight_A(5)
	
	if displayScreen == 1:
		print("... für das Testgewichts von ",testgewicht, " Gramm wurde nun ein Gewicht von ", weight ," Gramm ermittelt ...")
		print("... der neue Referenzwert wird in die Default Datei geschrieben ...")

	if displayCode == 1: 
		print("... f&uuml;r das Testgewichts von ",testgewicht, " Gramm wurde nun ein Gewicht von ", weight ," Gramm ermittelt ...<br/><br/>")
		print("... der neue Referenzwert wird in die Default Datei geschrieben ...<br/><br/>")

	# write new defaults
	CaravanPiFiles.writeGasScale(gasCylinderNumber, writeTestFile, displayScreen, emptyWeight, fullWeight, pin_dout, pin_sck, channel, refUnit)
	
	# cleanup GPIO
	hx.GPIOcleanup()

	if displayCode == 1:
		print("... damit wurde die Kalibrierung der Waage f&uuml;r die Gasflasche ", gasCylinderNumber, " abgeschlossen.<br/><br/>")
		print("<br/><br/>Sie werden in K&uuml;rze zur Eingabeseite weitergeleitet")
		print("</body>")
		print("</html>")


if __name__ == "__main__":
	main()
