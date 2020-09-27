#!/usr/bin/python3
# coding=utf-8
# setupGasscaleDefaults.py
#
# explore default values for the gas scale sensor
# (empty tara) and write them to the defaults file
#
# Aufruf-Parameter
# setupGasscaleDefaults.py -h -t -s -w <seconds>
# 	-h	display guide 
# 	-t	write values to a separate testfile 
# 	-s	display values on screen 
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
shortOptions = 'htsw:'
longOptions = ['help', 'test', 'screen', 'wait=']

def usage():
	print ("---------------------------------------------------------------------")
	print (sys.argv[0], "-h -f")
	print ("  -h          show this guide")
	print ("  -t          write values not to origin file but to a testfile")
	print ("  -s          display values on this screen")
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
	calibrationWait = 0 # seconds
	gasCylinderNumber = 1
	
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
		elif o == "--test" or o == "-t":
			print("output not to origin file but to test file")
			writeTestFile = 1
		elif o == "--screen" or o == "-s":
			print("output also to this screen")
			displayScreen = 1
		elif o == "--wait" or o == "-w":
			calibrationWait = int(a)

	for a in args:
		print("further argument: ", a)
		
	# read defaults
	(tare, emptyWeight, fullWeight) = CaravanPiFiles.readGasScale(gasCylinderNumber)
	
	# start sensor
	hx = HX711(23, 24)
	hx.set_reading_format("MSB", "MSB")
	hx.set_reference_unit(205)

	hx.reset()
	
	# Wait if there was a waiting time parameter
	i=0
	while i < calibrationWait:
		sleep(1)
		i+=1
	
	# read sensor
	weight = hx.get_weight(5)
	
	# write new defaults
	CaravanPiFiles.writeGasScale(gasCylinderNumber, writeTestFile, displayScreen, weight, emptyWeight, fullWeight)
	
	# cleanup GPIO
	hx.GPIOcleanup()

if __name__ == "__main__":
	main()
