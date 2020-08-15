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
from CaravanPiFilesClass import CaravanPiFiles


def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()

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

def main():
	# -------------------------
	# main 
	# -------------------------
	GPIO.setwarnings(False)
	
	tare = 0
	emptyWeight = 0
	fullWeight = 0
	
	hx = HX711(5, 6)
	hx.set_reading_format("MSB", "MSB")
	hx.set_reference_unit(205)

	hx.reset()

	(tare, emptyWeight, fullWeight) = CaravanPiFiles.readGasScale()

	try:
		weight = hx.get_weight(5)
		
		nettoWeight = weight - tare - emptyWeight
		nettoLevel = (nettoWeight/fullWeight) * 100
		write2file(nettoWeight, nettoLevel)

	except (KeyboardInterrupt, SystemExit):
		cleanAndExit()
	
	cleanAndExit()


if __name__ == "__main__":
	main()
