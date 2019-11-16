#!/usr/bin/python3
# coding=utf-8
# setupPositionDefaults.py
#
# explore default values for the position sensor
# adjustments, tolerances, approximation values
# and write them to the defaults file
#
# Aufruf-Parameter
# setupPositionDefaults.py -h -t -s -w <seconds>
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

# 3-axis-sensor (adafruit)
import board
import busio
import adafruit_adxl34x

# buzzer
import RPi.GPIO as io

# -----------------------------------------------
# libraries from CaravanPi 
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles
from CaravanPiFunctionsClass import CaravanPiFunctions

# -----------------------------------------------
# global variables
# -----------------------------------------------
# initiate 3-axis-sensor
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# Correction of axis values
adjustX = 0
adjustY = 0
adjustZ = 0
# what is still considered horizontal
toleranceX = 0
toleranceY = 0
# When should the approach color be selected?
approximationX = 0
approximationY = 0
# Distance of the 3-axis sensor to the right side (in driving direction) and to the front of the caravan 
# If the 3-axis sensor is mounted behind the axis (in driving direction), 
# the distance to the axis (distAxis) is positive. Otherwise this constant is negative.
# in mm
distRight = 0
distFront = 0
distAxis = 0

# buzzer
BUZZER_PIN = 26

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
	print ("  -w seconds  waiting time until the values are read out from the sensor (default 120 seconds)\n")


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
	calibrationWait = 120 # seconds
	
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
		
	

	# buzzer
	io.setmode(io.BCM)
	io.setup(BUZZER_PIN, io.OUT)
	io.output(BUZZER_PIN, io.LOW)

	# read defaults
	# The 3-axis sensor may not be installed exactly horizontally. The values to compensate for this installation difference are read from a file.
	# --> adjustX, adjustY, adjustZ
	# In addition, the LEDs should already indicate "horizontal" as soon as the deviation from the horizontal is within a tolerance.
	# --> approximationX, approximationY
	(adjustX_orig, adjustY_orig, adjustZ_orig, toleranceX_orig, toleranceY_orig, approximationX_orig, approximationY_orig, distRight, distFront, distAxis) = CaravanPiFiles.readAdjustment()
	
	# read sensor
	i=0
	arrayX = []
	arrayY = []
	arrayZ = []
	
	# Wait 2 minutes so that any vibrations of the caravan can subside
	# during this waiting time slow beeping of the buzzer
	while i < calibrationWait:
		io.output(BUZZER_PIN, io.HIGH)
		sleep(.1)
		io.output(BUZZER_PIN, io.LOW)
		sleep(.9)
		i+=1
		
	# buzzer beeps rapidly to signal imminent measurement
	i=0
	while i < 5:
		io.output(BUZZER_PIN, io.HIGH)
		sleep(.1)
		io.output(BUZZER_PIN, io.LOW)
		sleep(.1)
		i+=1

	
	# read sensor 200 times and put values in a list
	i=0
	while i < 200:
		(x, y, z) = accelerometer.acceleration
		arrayX.append(x)
		arrayY.append(y)
		arrayZ.append(z)
		i += 1
		# no sleep here, because the accuracy of Python/Raspberry Sleep is not sufficient anyway
		# instead a high number of passes over the loop variable
		
	# normalize values over the calculation of the median (extreme values/outliers are not considered)
	# Adjustment of the values by subtraction of the initial value
	x = statistics.median(arrayX)

	# determine the index of the first occurrence of x in the list
	try:
		i = arrayX.index(x)
		# set the counterparts for y and z belonging to the value x
		y = arrayY[i]
		z = arrayZ[i]
	except (ValueError, IndexError):
		# the median did not result in a value that appears in the list (i.e. an actually calculated value).
		# Then set the other median values as well
		y = statistics.median(arrayY)
		z = statistics.median(arrayZ)
	
	CaravanPiFiles.writeAdjustment(writeTestFile, displayScreen, x, y, z, toleranceX_orig, toleranceY_orig, approximationX_orig, approximationY_orig, distRight, distFront, distAxis)

	# signal the program position2file.py that default values have changed
	pid = CaravanPiFunctions.process_running("position2file.py")
	os.kill(pid, signal.SIGUSR1)

	# long beep of the buzzer to signal completion
	io.output(BUZZER_PIN, io.HIGH)
	sleep(1)
	io.output(BUZZER_PIN, io.LOW)
	io.cleanup()


if __name__ == "__main__":
	main()
