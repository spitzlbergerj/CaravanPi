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
import getopt

# -----------------------------------------------
# Sensoren libraries aus CaravanPi einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from hx711 import HX711
from CaravanPiFilesClass import CaravanPiFiles

# -------------------------
# call options 
# -------------------------
shortOptions = 'hg:'
longOptions = ['gasscale=']

def usage():
	print ("---------------------------------------------------------------------")
	print (sys.argv[0], "-h -g <nr>")
	print ("  -h          show this guide")
	print ("  -g nr       number of gas scale cylinder (default 1)\n")



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

	# -------------------------
	# process call parameters
	# -------------------------
	opts = []
	args = []
	gasCylinderNumber = 1
	tare = 0
	emptyWeight = 0
	fullWeight = 0

	try:
		opts, args = getopt.getopt(sys.argv[1:], shortOptions, longOptions)
	except getopt.GetoptError:
		print("ERROR: options not correct")
		usage()
		sys.exit()
	
	for o, a in opts:
		if o == "--help" or o == "-h":
			print("HELP")
			usage()
			sys.exit()
		elif o == "--gasscale" or o == "-g":
			gasCylinderNumber = int(a)

	for a in args:
		print("further argument: ", a)

	# -------------------------
	# gpio warnings off
	# -------------------------
	GPIO.setwarnings(False)

	# -------------------------
	# read defaults
	# -------------------------
	(emptyWeight, fullWeight, pin_dout, pin_sck, channel, refUnit) = CaravanPiFiles.readGasScale(gasCylinderNumber)
	print ("bisherige Werte:")
	print ("Leergewicht Flasche: ", emptyWeight)
	print ("max. Gas-Gewicht: ", fullWeight)
	print ("Pin DOUT: ", pin_dout)
	print ("Pin SCK: ", pin_sck)
	print ("Channel: >>", channel, "<<")
	print ("Reference Unit: ", refUnit)

	hx = HX711(pin_dout, pin_sck)
	hx.set_reading_format("MSB", "MSB")

	if channel == "A":
		hx.set_reference_unit_A(refUnit)
	elif channel == "B":
		hx.set_reference_unit_B(refUnit)
	else:
		print("invalid HX711 channel: ", channel)		
		print("set channel to A")
		channel = "A"		
		hx.set_reference_unit_A(refUnit)

	hx.reset()

	try:
		# read sensor
		if channel == "B":
			weight = hx.get_weight_B(5)
		else:
			weight = hx.get_weight_A(5)

		print ("aktuelle Messung Gaswaage: ", weight)

		if (weight<0):
			weight=weight*(-1)

		print ("aktuelle Messung Gaswaage: ", weight)


		nettoWeight = weight - tare - emptyWeight
		nettoLevel = (nettoWeight/fullWeight) * 100

		print ("Nettogewicht Gas: ", nettoWeight)
		print ("Nettofüllgrad: ", nettoLevel)

		write2file(nettoWeight, nettoLevel)

	except (KeyboardInterrupt, SystemExit):
		cleanAndExit()
	
	cleanAndExit()


if __name__ == "__main__":
	main()
