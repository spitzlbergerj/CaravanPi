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


def write2file(wert):
	try:
		dateiName = "/home/pi/CaravanPi/values/gasScale"
		file = open(dateiName, 'a')
		str_from_time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		strWert = '{:.0f}'.format(wert)
		file.write("\n"+ str_from_time_now + " " + strWert)
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

try:
	weight = hx.get_weight(5)
	write2file(weight - TARA - LEERGEWICHT)

except (KeyboardInterrupt, SystemExit):
	cleanAndExit()
