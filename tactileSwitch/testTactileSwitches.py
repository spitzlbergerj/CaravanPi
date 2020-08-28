#!/usr/bin/python3
# coding=utf-8
# testTactileSwitches.py
#
# use tactile switches to start python scripts
#
# Aufruf-Parameter
# tactileSwitches.py -f
# 	-h	display guide 
#
#-------------------------------------------------------------------------------

import time, datetime
import signal
import sys
from time import sleep
import getopt
import RPi.GPIO as GPIO
import subprocess
import os


# tactile switch calibration position sensor
pinSwitchPosition = 23
# tactile switch calibration gasscale
pinSwitchGasscale = 24
# tactile switch to set the current position in transverse direction as horizontal
pinSwitchNowHorizontal = 12
# tactile switch to activate the 'live' mode
pinSwitchLive = 13
pinLEDLive = 16
 

# -------------------------
# call options 
# -------------------------
shortOptions = 'h'
longOptions = ['help']

def usage():
	print ("---------------------------------------------------------------------")
	print (sys.argv[0], "-h")
	print ("  -h   show this guide")

def switchInterruptPosition(channel):  
	# -------------------------
	# switchInterruptPosition
	# tactile switch was pressed start calibrating the position sensor
	# -------------------------
	print ("Taster Kalibrierung Lage Sensor wurde gedrückt")

def switchInterruptGasscale(channel):  
	# -------------------------
	# switchInterruptGasscale 
	# tactile switch was pressed start calibrating the gas scale
	# -------------------------
	print ("Taster Kalibrierung Gaswaage wurde gedrückt")

def switchInterruptNowHorizontal(channel):  
	# -------------------------
	# switchInterruptGasscale 
	# tactile switch was pressed start calibrating the gas scale
	# -------------------------
	print ("Taster Querlage = Horizontal wurde gedrückt")

def switchInterruptLive(channel):  
	# -------------------------
	# switchInterruptGasscale 
	# tactile switch was pressed start calibrating the gas scale
	# -------------------------
	print ("Taster Live-Modus wurde gedrückt")
	print ("--> LED Live Modus leuchtet für 1/2 Sekunde")
	GPIO.output(pinLEDLive, True)
	time.sleep(.5)
	GPIO.output(pinLEDLive, False)



def main():
	# -------------------------
	# main 
	# -------------------------

	# -------------------------
	# process call parameters
	# -------------------------
	opts = []
	args = []
	writeFile = 0
	displayScreen = 0
	
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

	for a in args:
		print("further argument: ", a)


	# -------------------------
	# tactile switches
	# -------------------------
	GPIO.setmode(GPIO.BCM)
	
	GPIO.setup(pinSwitchPosition, GPIO.IN)
	GPIO.add_event_detect(pinSwitchPosition, GPIO.RISING, callback = switchInterruptPosition, bouncetime = 400)

	GPIO.setup(pinSwitchGasscale, GPIO.IN)
	GPIO.add_event_detect(pinSwitchGasscale, GPIO.RISING, callback = switchInterruptGasscale, bouncetime = 400)
	
	GPIO.setup(pinSwitchNowHorizontal, GPIO.IN)
	GPIO.add_event_detect(pinSwitchNowHorizontal, GPIO.RISING, callback = switchInterruptNowHorizontal, bouncetime = 400)

	GPIO.setup(pinSwitchLive, GPIO.IN)
	GPIO.add_event_detect(pinSwitchLive, GPIO.RISING, callback = switchInterruptLive, bouncetime = 400)

	GPIO.setup(pinLEDLive, GPIO.OUT)	
	GPIO.output(pinLEDLive, False)
	
	# -------------------------
	# endless loop
	# -------------------------
	while True:
		try:
			time.sleep(.5)						
		except KeyboardInterrupt:
			GPIO.cleanup()
			break
		except:
			print("unprocessed Error:", sys.exc_info()[0])
			GPIO.cleanup()
			raise


if __name__ == "__main__":
	main()
