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

import math

# -----------------------------------------------
# libraries from CaravanPi 
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from filesClass import CaravanPiFiles

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
# dimensions Caravan (in mm)
lengthOverAll = 0
lengthBody = 0
width = 0

# files
filePosition = "/home/pi/CaravanPi/values/position"

def checkTolerance(origValue, adjustValue, toleranceValue):
	# values within the tolerance are evaluated as horizontal
	
	# value adjustment
	value = origValue - adjustValue
	
	if (abs(value) < toleranceValue):
		# value within tolerance 
		value = 0
	
	return value

def write2file(x, y, z, adjustX, adjustY, adjustZ, diffHL, diffHR, diffVL, diffVR, diffZL, diffZR, diffVo):
	global filePosition

	try:
		dateiName = filePosition
		file = open(dateiName, 'a')
		str_from_time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		strX = '{:.6f}'.format(x)
		strY = '{:.6f}'.format(y)
		strZ = '{:.6f}'.format(z)
		strAdjustX = '{:.0f}'.format(adjustX)
		strAdjustY = '{:.0f}'.format(adjustY)
		strDiffHL = '{:.0f}'.format(diffHL)
		strDiffHR = '{:.0f}'.format(diffHR)
		strDiffVL = '{:.0f}'.format(diffVL)
		strDiffVR = '{:.0f}'.format(diffVR)
		strDiffZL = '{:.0f}'.format(diffZL)
		strDiffZR = '{:.0f}'.format(diffZR)
		strDiffVo = '{:.0f}'.format(diffVo)

		valueStr = "\n"+ str_from_time_now + " adjusted & tolerant: " + strAdjustX + " " + strAdjustY + " original: " + strX + " " + strY + " " + strZ + " differences: " + strDiffHL + " " + strDiffHR + " " + strDiffVL + " " + strDiffVR + " " + strDiffZL + " " + strDiffZR + " " + strDiffVo

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
	# To calculate the horizontal distance from the horizontal, the position of the sensor in relation to the outer walls of the caravan or to the axis is necessary.
	# --> distRight, distFront, distAxis
	(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, distRight, distFront, distAxis) = CaravanPiFiles.readAdjustment()
	# dimensions of the caravan
	(lengthOverAll, width, lengthBody) = CaravanPiFiles.readDimensions()
	
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
		
	tolX = checkTolerance(x, adjustX, toleranceX)
	tolY = checkTolerance(y, adjustY, toleranceY)
		
	# calculate the horizontal distance
	# Attention: If the 3-axis sensor is mounted behind the axis (in driving direction), 
	# the distance to the axis is positive. Otherwise this constant is negative.
	distLeft = width - distRight
	distBack = lengthBody - distFront
	
	# ADXL345 data sheet:
	# resolution typical 3.9 mg = 0.0039g
	# arcsin(0.0039) = 0.223454 degree
	#
	# diff = dist * sin(angle)
	#
	# x is the gravity in longitudinal direction
	# arcsin (gravity) = angle
	# sin(angle) = sin(arcsin(gravity)) = gravity
	
	# difference negative = position is "too high"
	diffHL = round((distLeft * tolY / 10) + (distBack * tolX / 10) * -1)
	diffHR = round((distRight * tolY / 10) + (distBack * tolX / 10) * -1)
	diffVL = round((distLeft * tolY / 10) + (distFront * tolX / 10))
	diffVR = round((distRight * tolY / 10) + (distFront * tolX / 10))
	diffZL = round((distLeft * tolY / 10) + (distAxis * tolX / 10))
	diffZR = round((distRight * tolY / 10) + (distAxis * tolX / 10))

	if distRight <= (width/2):
		diffVo = round((((width/2) - distRight) * tolY / 10) + ((distFront + (lengthOverAll - lengthBody)) * tolX / 10))
	else:
		diffVo = round((((width/2) - distLeft) * tolY / 10) + ((distFront + (lengthOverAll - lengthBody)) * tolX / 10))
	
	print ("width: ", width)
	print ("distRight: ", distRight)
	print ("distLeft: ", distLeft)
	print ("lengthOverAll: ", lengthOverAll)
	print ("lengthBody: ", lengthBody)
	print ("distFront: ", distFront)
	print ("distAxis: ", distAxis)
	print ("diffHL: ", diffHL)
	print ("diffHR: ", diffHR)
	print ("diffVL: ", diffVL)
	print ("diffVR: ", diffVR)
	print ("diffZL: ", diffZL)
	print ("diffZR: ", diffZR)
	print ("diffVo: ", diffVo)
	print ("x", tolX)
	print ("y", tolY)

	write2file(x, y, z, tolX, tolY, z-adjustZ, diffHL, diffHR, diffVL, diffVR, diffZL, diffZR, diffVo)

if __name__ == "__main__":
	main()
