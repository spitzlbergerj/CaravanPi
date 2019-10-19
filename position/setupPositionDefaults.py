#!/usr/bin/python3
# coding=utf-8
# position2file.py
#
# explore default values for the position sensor
# adjustments, tolerances, approximation values
# and write them to the defaults file
#
# Aufruf-Parameter
# setupPositionDefaults.py <file> <print>
# <file> path and filename for the defaults file
# <print> if exist and =1 then print values
#-------------------------------------------------------------------------------

import time, datetime
import statistics
import signal
import sys
from time import sleep
import os

import board
import busio
import adafruit_adxl34x

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

# files
fileAdjustments = "/home/pi/CaravanPi/defaults/adjustmentPosition"

# -------------------------
# 3-axis-sensor 
# -------------------------

def readAdjustment():
	global fileAdjustments
	
	try:
		dateiName = fileAdjustments
		file = open(dateiName)
		strAdjustX = file.readline()
		strAdjustY = file.readline()
		strAdjustZ = file.readline()
		strtoleranceX = file.readline()
		strtoleranceY = file.readline()
		strApproximationX = file.readline()
		strApproximationY = file.readline()
		file.close()
		adjustX = float(strAdjustX)
		adjustY = float(strAdjustY)
		adjustZ = float(strAdjustZ)
		toleranceX = float(strtoleranceX)
		toleranceY = float(strtoleranceY)
		approximationX = float(strApproximationX)
		approximationY = float(strApproximationY)
		return(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY)
	except:
		# Lesefehler
		print ("readAdjustment: The file could not be read.")
		return(0,0,0,0,0,0,0)

def writeAdjustments(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, shouldBePrinted):
	global fileAdjustments
	
	try:
		dateiName = fileAdjustments
		# test
		dateiName = fileAdjustments+"-test"

		file = open(dateiName, 'w')
		strAdjustX = '{:.6f}'.format(adjustX) + "\n"
		strAdjustY = '{:.6f}'.format(adjustY) + "\n"
		strAdjustZ = '{:.6f}'.format(adjustZ) + "\n"
		strtoleranceX = '{:.6f}'.format(toleranceX) + "\n"
		strtoleranceY = '{:.6f}'.format(toleranceY) + "\n"
		strApproximationX = '{:.6f}'.format(approximationX) + "\n"
		strApproximationY = '{:.6f}'.format(approximationY) + "\n"
		file.write(strAdjustX)
		file.write(strAdjustY)
		file.write(strAdjustZ)
		file.write(strtoleranceX)
		file.write(strtoleranceY)
		file.write(strApproximationX)
		file.write(strApproximationY)
		file.close()
		
		if (shouldBePrinted == 1):
			print("adjustX: "+strAdjustX)
			print("adjustY: "+strAdjustY)
			print("adjustZ: "+strAdjustZ)
			print("toleranceX: "+strtoleranceX)
			print("toleranceY: "+strtoleranceY)
			print("approximationX: "+strApproximationX)
			print("approximationY: "+strApproximationY)

		return 0
	except:
		print("writeAdjustments: The file could not be written - unprocessed Error:", sys.exc_info()[0])
		raise
		return -1

	
def main():
	# -------------------------
	# main 
	# -------------------------

	# process call parameters
	shouldBePrinted = 0
	if len(sys.argv) >= 3:
		shouldBePrinted = 1

	# test
	shouldBePrinted = 1


	# read defaults
	# The 3-axis sensor may not be installed exactly horizontally. The values to compensate for this installation difference are read from a file.
	# --> adjustX, adjustY, adjustZ
	# In addition, the LEDs should already indicate "horizontal" as soon as the deviation from the horizontal is within a tolerance.
	# --> approximationX, approximationY
	(adjustX_orig, adjustY_orig, adjustZ_orig, toleranceX_orig, toleranceY_orig, approximationX_orig, approximationY_orig) = readAdjustment()
	
	# read sensor
	i=0
	arrayX = []
	arrayY = []
	arrayZ = []
	
	# read sensor 200 times and put values in a list
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
	
	writeAdjustments(x, y, z, toleranceX_orig, toleranceY_orig, approximationX_orig, approximationY_orig, shouldBePrinted)


if __name__ == "__main__":
	main()
