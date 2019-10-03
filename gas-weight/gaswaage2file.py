#! /usr/bin/python2
# coding=utf-8
# temp2file.py
#
# liest die Gaswaage ein und schreibt den Wert in eine Datei
#
#-------------------------------------------------------------------------------

import time
import sys
import datetime
import RPi.GPIO as GPIO


# -----------------------------------------------
# Sensoren libraries aus CaravanPi einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from hx711 import HX711

GPIO.setwarnings(False)

TARA = 0
LEERGEWICHT = 0

def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()

def readTara():
	global TARA
	try:
		dateiName = "/home/pi/CaravanPi/defaults/gasScaleTare"
		file = open(dateiName)
		strTara = file.read()
		file.close()
		TARA = float(strTara)
		return 0
	except:
		# Lesefehler
		print ("Die Datei konnte nicht gelesen werden.")
		return -1

def readLeergewicht():
	global LEERGEWICHT
	try:
		dateiName = "/home/pi/CaravanPi/defaults/gasCylinderEmptyWeight"
		file = open(dateiName)
		strLeergewicht = file.read()
		file.close()
		LEERGEWICHT = float(strLeergewicht)
		return 0
	except:
		# Lesefehler
		print ("Die Datei konnte nicht gelesen werden.")
		return -1

def readVollGewicht():
	global VOLLGEWICHT
	try:
		dateiName = "/home/pi/CaravanPi/defaults/gasCylinderFullWeight"
		file = open(dateiName)
		strVollGewicht = file.read()
		file.close()
		VOLLGEWICHT = float(strVollGewicht)
		return 0
	except:
		# Lesefehler
		print ("Die Datei konnte nicht gelesen werden.")
		return -1


def write2file(wert, relativ):
	try:
		dateiName = "/home/pi/CaravanPi/values/gasScale"
		file = open(dateiName, 'a')
		str_from_time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		strWert = '{:.0f}'.format(wert)
		strRelativ = '{:.0f}'.format(relativ)
		file.write("\n"+ "gasScale " + str_from_time_now + " " + strWert + " " + strRelativ)
		file.close()
		return 0
	except:
		# Schreibfehler
		print ("Die Datei konnte nicht geschrieben werden.")
		return -1

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(205)

hx.reset()

# kein Tara auf die Waage anwenden, weil Gewicht dauerhaft auf Waage steht
# Tara ueber separates Skript in Datei geschrieben und hier nur ausgelesen

readTara()
readLeergewicht()
readVollGewicht()

try:
	weight = hx.get_weight(5)
	# Test
	weight = 2845
	
	nettoWeight = weight - TARA - LEERGEWICHT
	nettoLevel = (nettoWeight/VOLLGEWICHT) * 100
	# print ("Werte: ", weight, TARA, LEERGEWICHT, nettoWeight, VOLLGEWICHT, nettoLevel)
	write2file(nettoWeight, nettoLevel)

except (KeyboardInterrupt, SystemExit):
	cleanAndExit()
