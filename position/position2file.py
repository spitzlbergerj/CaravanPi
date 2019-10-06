#!/usr/bin/python3
# coding=utf-8
# position2file.py
#
# schreibt die aus dem Beschleunigungssensor ADXL345 gelesenen Lagewerte in eine Datei
# lediglich zur generellen Anzeige nutzen.
# zum Wohnwagen ausrichten anderes Skript nutzen
#
#-------------------------------------------------------------------------------

import time, datetime
import statistics
import sys

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
filePosition = "/home/pi/CaravanPi/values/position"
fileAdjustments = "/home/pi/CaravanPi/defaults/adjustmentPosition"

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

def checkTolerance(origValue, adjustValue, toleranceValue):
	# values within the tolerance are evaluated as horizontal
	
	# value adjustment
	value = origValue - adjustValue
	
	if (abs(value) < toleranceValue):
		# value within tolerance 
		value = 0
	
	return value

def write2file(x, y, z, adjustX, adjustY, adjustZ):
	global filePosition

	try:
		dateiName = filePosition
		file = open(dateiName, 'a')
		str_from_time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		strX = '{:.6f}'.format(x)
		strY = '{:.6f}'.format(y)
		strZ = '{:.6f}'.format(z)
		strAdjustX = '{:.6f}'.format(adjustX)
		strAdjustY = '{:.6f}'.format(adjustY)

		valueStr = "\n"+ str_from_time_now + " adjusted & tolerant: " + strAdjustX + " " + strAdjustY + " original: " + strX + " " + strY + " " + strZ

		file.write(valueStr)
		file.close()

		# print(valueStr)
		
		return 0
	except:
		print("write2file: The file could not be written - unprocessed Error:", sys.exc_info()[0])
		raise
		return -1

def main():
	# -------------------------
	# main 
	# -------------------------
	
	# read defaults
	# The 3-axis sensor may not be installed exactly horizontally. The values to compensate for this installation difference are read from a file.
	# --> adjustX, adjustY, adjustZ
	# In addition, the LEDs should already indicate "horizontal" as soon as the deviation from the horizontal is within a tolerance.
	# --> approximationX, approximationY
	(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY) = readAdjustment()
	
	# read sensor 50 times and put values in a list
	i=0
	arrayX = []
	arrayY = []
	arrayZ = []
	
	while i < 50:
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
		
	write2file(x, y, z, checkTolerance(x, adjustX, toleranceX), checkTolerance(y, adjustY, toleranceY), z-adjustZ)

if __name__ == "__main__":
	main()
