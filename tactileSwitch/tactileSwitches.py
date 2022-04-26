#!/usr/bin/python3
# coding=utf-8
# tactileSwitches.py
#
# use tactile switches to start python scripts
#
# Aufruf-Parameter
# tactileSwitches.py -f
# 	-h	display guide 
# 	-f	write values to file 
# 	-s	display values on screen 
#
#-------------------------------------------------------------------------------

import time, datetime
import signal
import sys
from time import sleep
from datetime import datetime
import getopt
import RPi.GPIO as GPIO
import subprocess
import os


# tactile switch calibration position sensor
pinSwitchPosition = 19
# tactile switch calibration gasscale
pinSwitchGasscale = 22

# if gas scale button pressed for at least this long then Flasche 2. if less then Flasche 1.
scaleSelectMinSeconds = 3

# button debounce time in seconds
debounceSeconds = 0.01

buttonPressedTime = None


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
	print ("ACHTUNG: Kalibrierung Lage Sensor wird gestartet!")
	subprocess.run(["python3","/home/pi/CaravanPi/position/setupPositionDefaults.py","-w","5"])
	print ("ACHTUNG: Kalibrierung Lage Sensor wurde beendet")

def switchInterruptGasscale(channel):  
	# -------------------------
	# switchInterruptGasscale 
	# tactile switch was pressed start calibrating the gas scale
	# -------------------------
	global buttonPressedTime

	print ("Interrupt - buttonPressedTime: ", buttonPressedTime)

	if (GPIO.input(channel)):
		# button is down
		print ("button down")
		if buttonPressedTime is None:
			print("set buttonPressedTime")
			buttonPressedTime = datetime.now()
	else:
		# button is up
		print ("button up")
		if buttonPressedTime is not None:
			print ("buttonPressedTime not None")
			elapsed = (datetime.now() - buttonPressedTime).total_seconds()
			buttonPressedTime = None
			if elapsed >= scaleSelectMinSeconds:
				# button pressed for more than specified time, Flasche 2
				print ("ACHTUNG: Kalibrierung Gaswaage Flasche 2 wird gestartet!")
				subprocess.run(["python3","/home/pi/CaravanPi/gas-weight/gasScaleCalibration.py", "-s", "-e", "1", "-g", "2", "-w", "5"])
				print ("ACHTUNG: Kalibrierung Gaswaage Flasche 2 wurde beendet")
			elif elapsed >= debounceSeconds:
				# button pressed for a shorter time, Flasche 1
				print ("ACHTUNG: Kalibrierung Gaswaage Flasche 1 wird gestartet!")
				subprocess.run(["python3","/home/pi/CaravanPi/gas-weight/gasScaleCalibration.py", "-s", "-e", "1", "-g", "1", "-w", "5"])
				print ("ACHTUNG: Kalibrierung Gaswaage Flasche 1 wurde beendet")



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

	# Gasflaschenkalibrierung - kurzer Druck = Flasche 1 - langer Druck = Flasche 2
	GPIO.setup(pinSwitchGasscale, GPIO.IN)
	GPIO.add_event_detect(pinSwitchGasscale, GPIO.BOTH, callback = switchInterruptGasscale)
	
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
